from __future__ import annotations

import argparse
import contextlib
import importlib
import inspect
import io
import pkgutil
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import yaml


@dataclass(frozen=True)
class Issue:
    path: Path
    message: str

    def __str__(self) -> str:
        return f"{self.path.as_posix()}: {self.message}"


def _load_weapon_ids() -> set[str]:
    # When executed as a script (e.g. `python resources/tools/check_weapons_data.py`)
    # Python's import root is `resources/tools`, not the repo root. Ensure the repo
    # root is on sys.path so imports like `import pydcs_extensions` work.
    repo_root = Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    # Ensure any modded weapons registered via `inject_weapons` are loaded into
    # pydcs before we validate CLSIDs against `dcs.weapons_data.weapon_ids`.
    #
    # Import-time output can be noisy (DCS install detection), so suppress it.
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        import pydcs_extensions

        # Import every submodule under pydcs_extensions to catch modules that
        # are not re-exported by pydcs_extensions/__init__.py but still inject
        # weapons at import time.
        for mod in pkgutil.iter_modules(
            pydcs_extensions.__path__, prefix=f"{pydcs_extensions.__name__}."
        ):
            importlib.import_module(mod.name)

    from dcs.weapons_data import weapon_ids  # type: ignore[import-not-found]

    return set(weapon_ids.keys())


def _iter_yaml_files(root: Path) -> list[Path]:
    return sorted(p for p in root.glob("**/*.yaml") if p.is_file())


def _iter_lua_files(root: Path) -> list[Path]:
    return sorted(p for p in root.glob("**/*.lua") if p.is_file())


_LUA_CLSID_RE = re.compile(r"""\["CLSID"\]\s*=\s*["']([^"']+)["']""", re.IGNORECASE)


_LUA_NAME_RE = re.compile(r"""\["unitType"\]\s*=\s*["']([^"']+)["']""", re.IGNORECASE)

_LUA_NUM_AFTER_CLSID_RE = re.compile(r"""\["num"\]\s*=\s*(\d+)""", re.IGNORECASE)


def _extract_lua_clsids_and_pylon_pairs(
    path: Path,
) -> tuple[set[str], list[tuple[int, str]], list[Issue]]:
    """Read Lua once: unique CLSIDs, (station, CLSID) pairs for payload pylons, issues."""
    issues: list[Issue] = []
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw = path.read_text(encoding="utf-8-sig")

    clsid_matches = list(_LUA_CLSID_RE.finditer(raw))
    clsids = {m.group(1).strip() for m in clsid_matches}
    clsids.discard("")
    if not clsids:
        issues.append(Issue(path, 'no ["CLSID"] entries found'))

    pairs: list[tuple[int, str]] = []
    for i, clsid_m in enumerate(clsid_matches):
        clsid = clsid_m.group(1).strip()
        if not clsid:
            continue
        end = clsid_m.end()
        boundary = len(raw)
        if i + 1 < len(clsid_matches):
            boundary = clsid_matches[i + 1].start()
        segment = raw[end:boundary]
        num_m = _LUA_NUM_AFTER_CLSID_RE.search(segment)
        if num_m is None:
            issues.append(
                Issue(
                    path,
                    f'["CLSID"] = "{clsid}" has no following ["num"] in the same pylon block',
                )
            )
            continue
        pairs.append((int(num_m.group(1)), clsid))
    return clsids, pairs, issues


def _valid_pylon_indices_and_allowed_clsids(
    dcs_type: type[Any],
) -> tuple[Optional[set[int]], dict[int, set[str]]]:
    """Mirror game.data.weapons.Pylon.for_aircraft: pydcs uses inner Pylon* classes."""
    pylons_attr = getattr(dcs_type, "pylons", None)
    if not isinstance(pylons_attr, (set, frozenset)):
        return None, {}

    valid_indices: set[int] = set(pylons_attr)
    allowed: dict[int, set[str]] = defaultdict(set)
    for attr in dcs_type.__dict__.values():
        if not inspect.isclass(attr) or not attr.__name__.startswith("Pylon"):
            continue
        for key, value in attr.__dict__.items():
            if key.startswith("__"):
                continue
            if not isinstance(value, tuple) or len(value) != 2:
                continue
            pylon_number, weapon = value
            if not isinstance(pylon_number, int):
                continue
            if not isinstance(weapon, dict) or "clsid" not in weapon:
                continue
            clsid = weapon["clsid"]
            if isinstance(clsid, str) and clsid:
                allowed[pylon_number].add(clsid)
    return valid_indices, dict(allowed)


def _extract_unit_name_from_lua(path: Path) -> tuple[Optional[str], list[Issue]]:
    issues: list[Issue] = []
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw = path.read_text(encoding="utf-8-sig")

    match = _LUA_NAME_RE.search(raw)
    if match is None:
        return None, [Issue(path, 'no ["unitType"] entry found')]

    name = match.group(1).strip()
    if not name:
        return None, [Issue(path, 'invalid ["unitType"] entry (empty string)')]
    return name, issues


def _validate_weapon_file(path: Path) -> tuple[Optional[dict[str, Any]], list[Issue]]:
    issues: list[Issue] = []
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raw = path.read_text(encoding="utf-8-sig")

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as ex:
        return None, [Issue(path, f"YAML parse error: {ex}")]

    if not isinstance(data, dict):
        return None, [
            Issue(path, f"expected a YAML mapping, got {type(data).__name__}")
        ]

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        issues.append(
            Issue(path, "missing/invalid required key: name (non-empty string)")
        )

    year = data.get("year")
    if year is not None and not isinstance(year, int):
        issues.append(Issue(path, "invalid key: year (must be an int if present)"))

    fallback = data.get("fallback")
    if fallback is not None and (not isinstance(fallback, str) or not fallback.strip()):
        issues.append(
            Issue(path, "invalid key: fallback (must be a non-empty string if present)")
        )

    clsids = data.get("clsids")
    if not isinstance(clsids, list) or not clsids:
        issues.append(
            Issue(path, "missing/invalid required key: clsids (non-empty list)")
        )
    else:
        for i, clsid in enumerate(clsids):
            if not isinstance(clsid, str) or not clsid.strip():
                issues.append(
                    Issue(path, f"invalid clsids[{i}] (must be a non-empty string)")
                )

    return data, issues


def check_weapons_data(
    weapons_dir: Path,
    customized_payloads_dir: Path,
    aircraft_dir: Path,
) -> list[Issue]:
    issues: list[Issue] = []
    yaml_files = _iter_yaml_files(weapons_dir)
    if not yaml_files:
        return [Issue(weapons_dir, "no .yaml files found")]

    try:
        weapon_ids = _load_weapon_ids()
    except Exception as ex:
        return [
            Issue(
                weapons_dir,
                "failed to import pydcs weapon database (including injected weapons): "
                f"{type(ex).__name__}: {ex}",
            )
        ]

    from dcs.helicopters import helicopter_map  # type: ignore[import-not-found]
    from dcs.planes import plane_map  # type: ignore[import-not-found]
    from dcs.unittype import FlyingType  # type: ignore[import-not-found]

    names_to_paths: dict[str, Path] = {}
    clsid_to_paths: dict[str, list[Path]] = defaultdict(list)
    fallback_refs: list[tuple[Path, str]] = []

    for path in yaml_files:
        data, file_issues = _validate_weapon_file(path)
        issues.extend(file_issues)
        if data is None:
            continue

        name = data.get("name")
        if isinstance(name, str) and name.strip():
            if name in names_to_paths:
                issues.append(
                    Issue(
                        path,
                        f'duplicate weapon group name "{name}" (also in '
                        f"{names_to_paths[name].as_posix()})",
                    )
                )
            else:
                names_to_paths[name] = path

        fallback = data.get("fallback")
        if isinstance(fallback, str) and fallback.strip():
            fallback_refs.append((path, fallback))

        clsids = data.get("clsids")
        if isinstance(clsids, list):
            for clsid in clsids:
                if not isinstance(clsid, str) or not clsid.strip():
                    continue
                clsid_to_paths[clsid].append(path)
                if clsid not in weapon_ids:
                    issues.append(Issue(path, f"unknown CLSID (not in pydcs): {clsid}"))

    for path, fallback in fallback_refs:
        if fallback not in names_to_paths:
            issues.append(
                Issue(
                    path, f'fallback "{fallback}" does not match any weapon group name'
                )
            )

    for clsid, paths in clsid_to_paths.items():
        if len(paths) > 1:
            rendered = ", ".join(p.as_posix() for p in sorted(set(paths)))
            issues.append(
                Issue(paths[0], f"CLSID used in multiple files: {clsid} ({rendered})")
            )

    lua_files = _iter_lua_files(customized_payloads_dir)
    if not lua_files:
        issues.append(Issue(customized_payloads_dir, "no .lua files found"))
    else:
        for lua_path in lua_files:
            lua_clsids, pylon_pairs, lua_parse_issues = (
                _extract_lua_clsids_and_pylon_pairs(lua_path)
            )
            unit_name, name_issues = _extract_unit_name_from_lua(lua_path)
            issues.extend(lua_parse_issues)
            issues.extend(name_issues)

            for clsid in sorted(lua_clsids):
                if clsid == "<CLEAN>":
                    continue
                if clsid not in weapon_ids:
                    issues.append(
                        Issue(lua_path, f"unknown CLSID (not in pydcs): {clsid}")
                    )
                weapon_files = sorted(set(clsid_to_paths.get(clsid, [])))
                if not weapon_files:
                    issues.append(
                        Issue(
                            lua_path,
                            "CLSID referenced by customized payload is not present in any "
                            f"resources/weapons YAML: {clsid}",
                        )
                    )
                elif len(weapon_files) != 1:
                    rendered = ", ".join(p.as_posix() for p in weapon_files)
                    issues.append(
                        Issue(
                            lua_path,
                            "CLSID referenced by customized payload must appear in exactly one "
                            f"resources/weapons YAML: {clsid} ({rendered})",
                        )
                    )

            if isinstance(unit_name, str) and unit_name.strip():
                dcs_type = plane_map.get(unit_name) or helicopter_map.get(unit_name)
                if dcs_type is None:
                    issues.append(
                        Issue(
                            lua_path,
                            f"unitType {unit_name!r} is not a pydcs plane or helicopter id",
                        )
                    )
                elif inspect.isclass(dcs_type) and issubclass(dcs_type, FlyingType):
                    valid_indices, allowed_by_pylon = (
                        _valid_pylon_indices_and_allowed_clsids(dcs_type)
                    )
                    if valid_indices is None:
                        issues.append(
                            Issue(
                                lua_path,
                                f"pydcs unit {unit_name!r} has no usable pylons definition",
                            )
                        )
                    else:
                        reported_bad_station: set[int] = set()
                        reported_bad_combo: set[tuple[int, str]] = set()
                        for pylon_idx, clsid in pylon_pairs:
                            if clsid == "<CLEAN>":
                                continue
                            if clsid not in weapon_ids:
                                continue
                            if pylon_idx not in valid_indices:
                                if pylon_idx not in reported_bad_station:
                                    reported_bad_station.add(pylon_idx)
                                    issues.append(
                                        Issue(
                                            lua_path,
                                            "pylon station index "
                                            f"{pylon_idx} is not defined for pydcs unit "
                                            f"{unit_name}",
                                        )
                                    )
                                continue
                            allowed_here = allowed_by_pylon.get(pylon_idx, set())
                            if clsid not in allowed_here:
                                key = (pylon_idx, clsid)
                                if key not in reported_bad_combo:
                                    reported_bad_combo.add(key)
                                    issues.append(
                                        Issue(
                                            lua_path,
                                            "CLSID is not a valid weapon for pylon "
                                            f"{pylon_idx} on pydcs unit {unit_name}: {clsid}",
                                        )
                                    )

            aircraft_yaml = aircraft_dir / f"{unit_name}.yaml"
            if not aircraft_yaml.exists():
                issues.append(
                    Issue(
                        lua_path,
                        f"no matching aircraft YAML found: {aircraft_yaml.as_posix()}",
                    )
                )
                continue

            try:
                aircraft_data = yaml.safe_load(
                    aircraft_yaml.read_text(encoding="utf-8")
                )
            except UnicodeDecodeError:
                aircraft_data = yaml.safe_load(
                    aircraft_yaml.read_text(encoding="utf-8-sig")
                )
            except yaml.YAMLError as ex:
                issues.append(Issue(aircraft_yaml, f"YAML parse error: {ex}"))
                continue

            if not isinstance(aircraft_data, dict):
                issues.append(
                    Issue(
                        aircraft_yaml,
                        f"expected a YAML mapping, got {type(aircraft_data).__name__}",
                    )
                )
                continue

            introduced = aircraft_data.get("introduced")
            if introduced is None:
                issues.append(Issue(aircraft_yaml, "missing required key: introduced"))
            elif not isinstance(introduced, int):
                issues.append(
                    Issue(aircraft_yaml, "invalid key: introduced (must be an int)")
                )

    return issues


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate weapons YAML, customized payload CLSIDs, and payload "
            "pylon assignments against pydcs aircraft definitions."
        )
    )
    parser.add_argument(
        "--weapons-dir",
        type=Path,
        default=Path("resources/weapons"),
        help="Path to the weapons resource directory (default: resources/weapons).",
    )
    parser.add_argument(
        "--customized-payloads-dir",
        type=Path,
        default=Path("resources/customized_payloads"),
        help=(
            "Path to customized payload Lua files "
            "(default: resources/customized_payloads)."
        ),
    )
    parser.add_argument(
        "--aircraft-dir",
        type=Path,
        default=Path("resources/units/aircraft"),
        help="Path to aircraft YAML directory (default: resources/units/aircraft).",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    weapons_dir: Path = args.weapons_dir
    customized_payloads_dir: Path = args.customized_payloads_dir
    aircraft_dir: Path = args.aircraft_dir
    issues = check_weapons_data(weapons_dir, customized_payloads_dir, aircraft_dir)
    if not issues:
        return 0
    for issue in issues:
        print(issue, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
