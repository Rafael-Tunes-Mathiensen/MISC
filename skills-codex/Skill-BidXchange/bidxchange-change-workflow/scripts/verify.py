#!/usr/bin/env python
"""Execute the BidXchange validation gate from the personal Codex skill."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path.cwd().resolve()


def bundled_executable(name: str) -> str | None:
    """Resolve tools from PATH or the Codex bundled runtime on Windows."""
    resolved = shutil.which(name) or shutil.which(f"{name}.cmd")
    if resolved:
        return resolved

    runtime = (
        Path.home()
        / ".cache"
        / "codex-runtimes"
        / "codex-primary-runtime"
        / "dependencies"
    )
    candidates = {
        "node": (runtime / "node" / "bin" / "node.exe",),
        "pnpm": (
            runtime / "bin" / "fallback" / "pnpm.cmd",
            runtime / "node" / "bin" / "pnpm.cmd",
        ),
    }
    return next(
        (str(path) for path in candidates.get(name, ()) if path.exists()),
        None,
    )


def validate_project_root() -> None:
    """Ensure the command is running from the BidXchange repository root."""
    required_paths = (
        PROJECT_ROOT / "manage.py",
        PROJECT_ROOT / "docs" / "ARCHITECTURE.md",
        PROJECT_ROOT / "bidxchange",
        PROJECT_ROOT / "accounts",
    )
    if not all(path.exists() for path in required_paths):
        raise RuntimeError("Run this verifier from the BidXchange repository root.")


def run(command: list[str]) -> None:
    """Run a command from the project root and stop on the first failure."""
    print(f"\n> {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


def source_javascript_files() -> list[Path]:
    """Return JavaScript source files owned by the project and Django apps."""
    files: list[Path] = []
    shared_static = PROJECT_ROOT / "static"
    if shared_static.exists():
        files.extend(shared_static.rglob("*.js"))
    for app in ("accounts", "bidxchange"):
        static_root = PROJECT_ROOT / app / "static"
        if static_root.exists():
            files.extend(static_root.rglob("*.js"))
    return sorted(files)


def run_quality_gate() -> None:
    python = sys.executable
    run(["git", "diff", "--check"])
    run([python, "manage.py", "check"])
    run([python, "manage.py", "makemigrations", "--check", "--dry-run"])
    run([python, "manage.py", "collectstatic", "--dry-run", "--noinput"])
    run([python, "-m", "ruff", "check", "."])
    run([python, "-m", "ruff", "format", "--check", "."])

    frontend_check = PROJECT_ROOT / "tools" / "check_frontend.py"
    if frontend_check.exists():
        run([python, str(frontend_check.relative_to(PROJECT_ROOT))])

    node = bundled_executable("node")
    package_json = PROJECT_ROOT / "package.json"
    if package_json.exists():
        local_stylelint = PROJECT_ROOT / "node_modules" / "stylelint" / "bin" / "stylelint.mjs"
        if local_stylelint.exists() and node:
            run(
                [
                    node,
                    str(local_stylelint.relative_to(PROJECT_ROOT)),
                    "static/ui/css/**/*.css",
                    "accounts/static/accounts/css/**/*.css",
                    "bidxchange/static/bidxchange/css/**/*.css",
                ]
            )
        else:
            pnpm = bundled_executable("pnpm")
            if pnpm is None:
                raise RuntimeError("pnpm is required to validate frontend styles.")
            run([pnpm, "lint:styles"])

    javascript_files = source_javascript_files()
    if javascript_files and node is None:
        raise RuntimeError("Node.js is required to validate JavaScript syntax.")
    for path in javascript_files:
        run([node, "--check", str(path.relative_to(PROJECT_ROOT))])


def run_tests(labels: list[str]) -> None:
    run([sys.executable, "manage.py", "test", *labels])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--all", action="store_true", help="Run quality and tests.")
    mode.add_argument("--quality", action="store_true", help="Run quality checks.")
    mode.add_argument("--tests", action="store_true", help="Run Django tests.")
    parser.add_argument(
        "--test-label",
        action="append",
        default=[],
        help="Django test label; repeat to run more than one.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_quality = args.all or args.quality or not args.tests
    run_test_suite = args.all or args.tests or not args.quality

    try:
        validate_project_root()
        if run_quality:
            run_quality_gate()
        if run_test_suite:
            run_tests(args.test_label)
    except (subprocess.CalledProcessError, RuntimeError) as exc:
        print(f"\nValidation failed: {exc}", file=sys.stderr)
        return 1

    print("\nBidXchange validation completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
