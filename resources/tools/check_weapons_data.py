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


def _weapon_has_clsid_on_pylon(
    data: dict[str, Any],
    pylon_idx: int,
    allowed_by_pylon: dict[int, set[str]],
) -> bool:
    allowed_here = allowed_by_pylon.get(pylon_idx, set())
    clsids = data.get("clsids")
    if not isinstance(clsids, list):
        return False
    for clsid in clsids:
        if isinstance(clsid, str) and clsid.strip() and clsid in allowed_here:
            return True
    return False


def _next_weapon_with_pylon_clsid(
    start_path: Path,
    pylon_idx: int,
    allowed_by_pylon: dict[int, set[str]],
    names_to_paths: dict[str, Path],
    weapon_data_by_path: dict[Path, dict[str, Any]],
) -> tuple[Optional[Path], Optional[str]]:
    """
    From ``start_path``, follow ``fallback`` until a weapon group has at least one
    CLSID pydcs allows on ``pylon_idx``. Returns (path, None) or (None, error).
    """
    visited_skip: set[str] = set()
    current: Optional[Path] = start_path
    while current is not None:
        data = weapon_data_by_path.get(current)
        if data is None:
            return None, f"missing weapon YAML data for {current.as_posix()}"

        wname = data.get("name")
        label = (
            wname.strip() if isinstance(wname, str) and wname.strip() else current.stem
        )
        if isinstance(wname, str) and wname.strip():
            if wname in visited_skip:
                return None, (
                    f"fallback chain cycles at weapon group {wname!r} while searching "
                    f"for a CLSID allowed on pylon {pylon_idx}"
                )
            visited_skip.add(wname.strip())

        if _weapon_has_clsid_on_pylon(data, pylon_idx, allowed_by_pylon):
            return current, None

        fb = data.get("fallback")
        if not isinstance(fb, str) or not fb.strip():
            return None, (
                f"no fallback weapon with any CLSID allowed on pylon {pylon_idx} "
                f"(exhausted chain at weapon group {label!r})"
            )

        next_name = fb.strip()
        nxt = names_to_paths.get(next_name)
        if nxt is None:
            return (
                None,
                f"fallback weapon group {next_name!r} does not exist in resources/weapons",
            )
        current = nxt

    return None, (
        f"exhausted fallback chain without a weapon with a CLSID allowed on pylon "
        f"{pylon_idx}"
    )


def _payload_weapon_introduced_chain_ok(
    weapon_start_path: Path,
    aircraft_name: str,
    aircraft_introduced: int,
    names_to_paths: dict[str, Path],
    weapon_data_by_path: dict[Path, dict[str, Any]],
    pylon_idx: int,
    allowed_by_pylon: Optional[dict[int, set[str]]],
) -> Optional[str]:
    """
    Return None if the weapon group chain is valid for the aircraft: some step has
    empty ``year``, or an int ``year`` not after ``aircraft_introduced``. When ``year``
    forces a fallback, each fallback target must list a CLSID allowed on
    ``pylon_idx`` (pydcs), or that target is skipped and the next fallback is tried.

    If ``allowed_by_pylon`` is None (no pydcs pylon data), fallback targets are not
    filtered by station.
    """
    current: Optional[Path] = weapon_start_path
    visited_names: set[str] = set()

    while current is not None:
        data = weapon_data_by_path.get(current)
        if data is None:
            return f"missing weapon YAML data for {current.as_posix()}"

        wname = data.get("name")
        if isinstance(wname, str) and wname.strip():
            if wname in visited_names:
                return (
                    f"fallback chain cycles at weapon group {wname!r} "
                    f"(aircraft introduced {aircraft_introduced})"
                )
            visited_names.add(wname)

        year = data.get("year")
        if year is None:
            return None
        if not isinstance(year, int):
            # Invalid ``year`` is already reported by ``_validate_weapon_file``.
            return None
        if year <= aircraft_introduced:
            return None
        if 'no_fallback_for' in data and aircraft_name in data['no_fallback_for']:
            return None

        fb = data.get("fallback")
        if not isinstance(fb, str) or not fb.strip():
            label = (
                wname.strip()
                if isinstance(wname, str) and wname.strip()
                else current.stem
            )
            return (
                f"weapon group {label!r} has year {year} not before aircraft introduction "
                f"{aircraft_introduced} but no fallback weapon is defined"
            )

        next_name = fb.strip()
        nxt = names_to_paths.get(next_name)
        if nxt is None:
            return f"fallback weapon group {next_name!r} does not exist in resources/weapons"

        if allowed_by_pylon is None:
            current = nxt
        else:
            nxt2, skip_err = _next_weapon_with_pylon_clsid(
                nxt,
                pylon_idx,
                allowed_by_pylon,
                names_to_paths,
                weapon_data_by_path,
            )
            if skip_err is not None:
                return skip_err
            current = nxt2


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
    weapon_data_by_path: dict[Path, dict[str, Any]] = {}

    for path in yaml_files:
        data, file_issues = _validate_weapon_file(path)
        issues.extend(file_issues)
        if data is None:
            continue

        weapon_data_by_path[path] = data

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

    payload_unit_types: set[str] = set()
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
            if isinstance(unit_name, str) and unit_name.strip():
                payload_unit_types.add(unit_name.strip())

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

            if not (isinstance(unit_name, str) and unit_name.strip()):
                continue

            unit_stem = unit_name.strip()
            aircraft_yaml = aircraft_dir / f"{unit_stem}.yaml"
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
            else:
                valid_indices_opt: Optional[set[int]] = None
                allowed_by_pylon_opt: Optional[dict[int, set[str]]] = None
                dcs_t = plane_map.get(unit_stem) or helicopter_map.get(unit_stem)
                if inspect.isclass(dcs_t) and issubclass(dcs_t, FlyingType):
                    _vi, abp = _valid_pylon_indices_and_allowed_clsids(dcs_t)
                    if _vi is not None:
                        valid_indices_opt = _vi
                        allowed_by_pylon_opt = abp

                for pylon_idx, clsid in pylon_pairs:
                    if clsid == "<CLEAN>":
                        continue
                    if clsid not in weapon_ids:
                        continue
                    if (
                        valid_indices_opt is not None
                        and pylon_idx not in valid_indices_opt
                    ):
                        continue
                    weapon_files = sorted(set(clsid_to_paths.get(clsid, [])))
                    if len(weapon_files) != 1:
                        continue
                    chain_err = _payload_weapon_introduced_chain_ok(
                        weapon_files[0],
                        unit_stem,
                        introduced,
                        names_to_paths,
                        weapon_data_by_path,
                        pylon_idx,
                        allowed_by_pylon_opt,
                    )
                    if chain_err is not None:
                        issues.append(
                            Issue(
                                lua_path,
                                f"weapon introduction vs aircraft {unit_stem!r} (introduced "
                                f"{introduced}), pylon {pylon_idx}, CLSID {clsid}: {chain_err}",
                            )
                        )

    aircraft_yaml_files = _iter_yaml_files(aircraft_dir)
    if not aircraft_yaml_files:
        issues.append(Issue(aircraft_dir, "no aircraft .yaml files found"))
    else:
        for ay_path in aircraft_yaml_files:
            stem = ay_path.stem
            if stem in payload_unit_types:
                continue
            dcs_type = plane_map.get(stem) or helicopter_map.get(stem)
            if dcs_type is None:
                continue
            if not inspect.isclass(dcs_type) or not issubclass(dcs_type, FlyingType):
                continue
            valid_indices, _ = _valid_pylon_indices_and_allowed_clsids(dcs_type)
            if not valid_indices:
                continue
            issues.append(
                Issue(
                    ay_path,
                    f"no customized payload .lua for  {stem!r}",
                )
            )

    return issues


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate weapons YAML, customized payload CLSIDs, payload "
            "pylon assignments against pydcs aircraft definitions, that each "
            "resources/units/aircraft YAML stem for a pydcs plane/helicopter with "
            'weapon pylons matches some payload ["unitType"], and that each payload '
            "CLSID's weapon ``year`` (following ``fallback`` chains) is empty or "
            "not after the aircraft ``introduced`` year; when pydcs pylon data exists, "
            "each fallback must include a CLSID allowed on that payload station until "
            "the chain resolves."
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
