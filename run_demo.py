#!/usr/bin/env python3
"""One-command local bootstrap demo for EDAgent."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


ROOT = Path(__file__).resolve().parent


def run_step(name: str, cmd: List[str]) -> Tuple[bool, str]:
    try:
        out = subprocess.run(
            cmd,
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        return True, out.stdout.strip()
    except subprocess.CalledProcessError as e:
        msg = (e.stdout or "") + ("\n" + e.stderr if e.stderr else "")
        return False, msg.strip()


def main() -> int:
    required_dirs = [
        ROOT / "docs" / "knowledge_base",
        ROOT / "docs" / "tool_registry",
        ROOT / "skills",
        ROOT / "scripts" / "common",
        ROOT / "slurm_logs" / "00_meta",
    ]
    for d in required_dirs:
        d.mkdir(parents=True, exist_ok=True)

    steps = [
        ("tool catalog query", ["python3", "scripts/common/tool_catalog.py", "query", "infra", "skill"]),
        (
            "infra stack guard",
            [
                "python3",
                "scripts/common/infra_stack_guard.py",
                "--out-prefix",
                "slurm_logs/00_meta/infra_stack_guard_bootstrap",
            ],
        ),
        (
            "skill system audit",
            [
                "python3",
                "scripts/common/skill_system_audit.py",
                "--out-prefix",
                "slurm_logs/00_meta/skill_system_audit_bootstrap",
            ],
        ),
        ("kb index build", ["python3", "scripts/common/unified_kb_query.py", "build"]),
    ]

    print("EDAgent demo bootstrap start")
    failed_steps = []
    for name, cmd in steps:
        ok, output = run_step(name, cmd)
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {name}: {' '.join(cmd)}")
        if output:
            lines = output.splitlines()
            preview = "\n".join(lines[:8])
            print(preview)
            if len(lines) > 8:
                print("... (truncated)")
        if not ok:
            failed_steps.append(name)

    print()
    if failed_steps:
        print("Bootstrap finished with warnings.")
        print("Failed checks: " + ", ".join(failed_steps))
        print("You can still start with EDAgent; fix warnings for full governance mode.")
    else:
        print("Bootstrap complete.")

    print("Next, ask EDAgent your research direction and target constraints.")
    print("Example: 'My focus is placement for dynamic-power reduction with area/timing guardrails.'")
    return 0


if __name__ == "__main__":
    sys.exit(main())
