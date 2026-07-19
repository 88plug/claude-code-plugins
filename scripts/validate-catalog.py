#!/usr/bin/env python3
"""Validate the marketplace catalog index for Grok Build compatibility.

Mirrors xai-org/plugin-marketplace scripts/validate-catalog.py plus 88plug
invariants (Claude ↔ Grok count parity, keywords present).

Enforces, for every plugin with `"source": {"source": "url", ...}`:

  - `sha` field is present and non-empty
  - `sha` is a 40-character lowercase hex string (full commit SHA)

Grok re-verifies `git rev-parse HEAD == sha` after clone. Without a pin,
installs track a mutable ref.

Run:    python3 scripts/validate-catalog.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SHA_RE = re.compile(r"^[0-9a-f]{40}$")

CATALOG_PATHS = [
    Path(".grok-plugin/marketplace.json"),
    Path(".claude-plugin/marketplace.json"),
]


def validate_entry(
    entry: dict,
    idx: int,
    *,
    require_sha: bool,
    require_keywords: bool,
) -> list[str]:
    """Validate one plugin entry.

    Grok catalog: require url pins + keywords (content-addressable install).
    Claude catalog: rolling url sources without sha are intentional — only
    structural checks.
    """
    errors: list[str] = []
    name = entry.get("name") or f"<unnamed at index {idx}>"
    source = entry.get("source")

    if not isinstance(source, dict):
        return errors

    is_url = source.get("source") == "url" or source.get("type") == "url"
    if not is_url:
        return errors

    url = source.get("url")
    if not isinstance(url, str) or not (
        url.startswith("https://") or url.startswith("http://")
    ):
        errors.append(f"plugin '{name}': url source must be http(s)://, got {url!r}")

    sha = source.get("sha")
    if require_sha:
        if not sha:
            errors.append(
                f"plugin '{name}': missing `sha` on url source "
                f"(url={url!r}) — Grok requires full commit pins"
            )
            return errors
        if not isinstance(sha, str):
            errors.append(
                f"plugin '{name}': sha must be a string, got {type(sha).__name__}"
            )
            return errors
        if not SHA_RE.match(sha):
            errors.append(
                f"plugin '{name}': sha {sha!r} is not a 40-character lowercase hex string"
            )
    elif sha is not None:
        if not isinstance(sha, str) or not SHA_RE.match(sha):
            errors.append(
                f"plugin '{name}': optional sha present but invalid: {sha!r}"
            )

    path = source.get("path")
    if path is not None:
        if not isinstance(path, str) or not path.strip():
            errors.append(
                f"plugin '{name}': url source `path` must be a non-empty string when present"
            )
        elif (
            path.startswith("/")
            or "\\" in path
            or any(part in ("..", "") for part in path.split("/"))
        ):
            errors.append(
                f"plugin '{name}': url source `path` {path!r} must be a relative "
                f"subdirectory (no leading '/', no '..', no backslashes)"
            )

    if require_keywords:
        kws = entry.get("keywords")
        if not isinstance(kws, list) or not kws:
            errors.append(
                f"plugin '{name}': missing non-empty `keywords` "
                f"(Grok request matching; derive from tags if needed)"
            )

    return errors


def validate_file(
    path: Path, *, require_sha: bool, require_keywords: bool
) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"{path}: failed to parse: {e}"]

    plugins = data.get("plugins", [])
    if not isinstance(plugins, list):
        return [f"{path}: `plugins` must be an array, got {type(plugins).__name__}"]

    if path.name == "marketplace.json" and path.parent.name == ".grok-plugin":
        if data.get("name") != "88plug":
            return [f"{path}: expected marketplace name '88plug', got {data.get('name')!r}"]

    errors: list[str] = []
    names: list[str] = []
    for idx, entry in enumerate(plugins):
        if not isinstance(entry, dict):
            errors.append(f"{path}: plugin index {idx} must be an object")
            continue
        n = entry.get("name")
        if n:
            names.append(n)
        errors.extend(
            f"{path}: {e}"
            for e in validate_entry(
                entry,
                idx,
                require_sha=require_sha,
                require_keywords=require_keywords,
            )
        )

    if len(names) != len(set(names)):
        errors.append(f"{path}: duplicate plugin names")

    return errors


def main() -> int:
    catalog_files = [p for p in CATALOG_PATHS if p.exists()]
    if not catalog_files:
        print(
            "ERROR: no catalog file found. Expected one of: "
            + ", ".join(str(p) for p in CATALOG_PATHS),
            file=sys.stderr,
        )
        return 1

    all_errors: list[str] = []
    for path in catalog_files:
        # Grok catalog: SHA pins + keywords. Claude: rolling urls, tags only.
        is_grok = path.parent.name == ".grok-plugin"
        all_errors.extend(
            validate_file(
                path,
                require_sha=is_grok,
                require_keywords=is_grok,
            )
        )

    grok = Path(".grok-plugin/marketplace.json")
    claude = Path(".claude-plugin/marketplace.json")
    if grok.exists() and claude.exists():
        g = json.loads(grok.read_text(encoding="utf-8"))
        c = json.loads(claude.read_text(encoding="utf-8"))
        gn = {p["name"] for p in g.get("plugins", []) if isinstance(p, dict) and "name" in p}
        cn = {p["name"] for p in c.get("plugins", []) if isinstance(p, dict) and "name" in p}
        if gn != cn:
            all_errors.append(
                f"Claude/Grok name set mismatch: "
                f"only_claude={sorted(cn - gn)} only_grok={sorted(gn - cn)}"
            )
        idx = Path(".grok-plugin/plugin-index.json")
        if idx.exists():
            index = json.loads(idx.read_text(encoding="utf-8"))
            plugins = index.get("plugins") or {}
            if index.get("version") != 1:
                all_errors.append(
                    f"plugin-index version must be 1, got {index.get('version')!r}"
                )
            if not isinstance(plugins, dict):
                all_errors.append("plugin-index.plugins must be an object map")
            else:
                missing = sorted(gn - set(plugins.keys()))
                extra = sorted(set(plugins.keys()) - gn)
                if missing:
                    all_errors.append(f"plugin-index missing: {missing}")
                if extra:
                    all_errors.append(f"plugin-index extra: {extra}")
                for name, entry in plugins.items():
                    if not isinstance(entry, dict):
                        continue
                    m_sha = next(
                        (
                            p["source"]["sha"]
                            for p in g["plugins"]
                            if p.get("name") == name
                            and isinstance(p.get("source"), dict)
                        ),
                        None,
                    )
                    i_sha = entry.get("sha")
                    if m_sha and i_sha and m_sha != i_sha:
                        all_errors.append(
                            f"plugin-index sha mismatch for {name}: "
                            f"catalog={m_sha[:12]} index={i_sha[:12]}"
                        )

    if all_errors:
        print("Catalog validation failed:", file=sys.stderr)
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    summary = " + ".join(str(p) for p in catalog_files)
    print(f"Catalog OK ({summary})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
