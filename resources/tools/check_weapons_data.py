from __future__ import annotations

import argparse
import contextlib
import importlib
import io
import pkgutil
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
        return None, [Issue(path, f"expected a YAML mapping, got {type(data).__name__}")]

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        issues.append(Issue(path, "missing/invalid required key: name (non-empty string)"))

    year = data.get("year")
    if year is not None and not isinstance(year, int):
        issues.append(Issue(path, "invalid key: year (must be an int if present)"))

    fallback = data.get("fallback")
    if fallback is not None and (not isinstance(fallback, str) or not fallback.strip()):
        issues.append(Issue(path, "invalid key: fallback (must be a non-empty string if present)"))

    clsids = data.get("clsids")
    if not isinstance(clsids, list) or not clsids:
        issues.append(Issue(path, "missing/invalid required key: clsids (non-empty list)"))
    else:
        for i, clsid in enumerate(clsids):
            if not isinstance(clsid, str) or not clsid.strip():
                issues.append(Issue(path, f"invalid clsids[{i}] (must be a non-empty string)"))

    return data, issues


def check_weapons_data(weapons_dir: Path) -> list[Issue]:
    issues: list[Issue] = []
    yaml_files = _iter_yaml_files(weapons_dir)
    if not yaml_files:
        return [Issue(weapons_dir, "no .yaml files found")]

    weapon_ids = _load_weapon_ids()

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
            issues.append(Issue(path, f'fallback "{fallback}" does not match any weapon group name'))

    for clsid, paths in clsid_to_paths.items():
        if len(paths) > 1:
            rendered = ", ".join(p.as_posix() for p in sorted(set(paths)))
            issues.append(Issue(paths[0], f"CLSID used in multiple files: {clsid} ({rendered})"))

    return issues


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate resources/weapons YAML files.")
    parser.add_argument(
        "--weapons-dir",
        type=Path,
        default=Path("resources/weapons"),
        help="Path to the weapons resource directory (default: resources/weapons).",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    weapons_dir: Path = args.weapons_dir
    issues = check_weapons_data(weapons_dir)
    if not issues:
        return 0
    for issue in issues:
        print(issue, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

