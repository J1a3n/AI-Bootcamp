"""
AI Bootcamp Unified CLI Runner (Multi-Subject Pluggable Architecture)
Usage:
  python -m harness check 0                       (Pre-flight hardware & infrastructure doctor)
  python -m harness check 1.1 [--subject <id>]    (Sprint 1, Slice 1.1)
  python -m harness check 1.2 [--subject <id>]    (Sprint 1, Slice 1.2)
  python -m harness check 1.3 [--subject <id>]    (Sprint 1, Slice 1.3)
  python -m harness check 2.1 [--subject <id>]    (Sprint 2, Slice 2.1)
  python -m harness check 2.2 [--subject <id>]    (Sprint 2, Slice 2.2)
  python -m harness check 3.1 [--subject <id>]    (Sprint 3, Slice 3.1)
  python -m harness check 3.2 [--subject <id>]    (Sprint 3, Slice 3.2)
  python -m harness check 4.1 [--subject <id>]    (Sprint 4, Slice 4.1)
  python -m harness check 4.2 [--subject <id>]    (Sprint 4, Slice 4.2 & Capstone)
  python -m harness tracks                        (List all pluggable subject packs)
  python -m harness select <subject_id>           (Switch active subject track: math, science, humanities, economics)
"""
import os
import sys
import argparse
from harness.preflight import run_preflight
from harness.subjects import (
    get_active_subject,
    set_active_subject,
    list_subject_packs,
    SUBJECT_PACKS,
)
from harness.checks.sprint1 import check_slice_1_1, check_slice_1_2, check_slice_1_3
from harness.checks.sprint2 import check_slice_2_1, check_slice_2_2
from harness.checks.sprint3 import check_slice_3_1, check_slice_3_2
from harness.checks.sprint4 import check_slice_4_1, check_slice_4_2

DISPATCHER = {
    "0": run_preflight,
    "1.1": check_slice_1_1,
    "1.2": check_slice_1_2,
    "1.3": check_slice_1_3,
    "2.1": check_slice_2_1,
    "2.2": check_slice_2_2,
    "3.1": check_slice_3_1,
    "3.2": check_slice_3_2,
    "4.1": check_slice_4_1,
    "4.2": check_slice_4_2,
}


def print_tracks():
    active = get_active_subject()
    print("=" * 68)
    print("  AI BOOTCAMP: PLUGGABLE SUBJECT PACK TRACKS")
    print("=" * 68)
    for pack in list_subject_packs():
        marker = "[ACTIVE]" if pack["id"] == active else "        "
        print(f"  {marker} {pack['id']:<12} — {pack['title']}")
        print(f"                         Persona: {pack['teacher_persona']}")
        print(f"                         Topic:   {pack['sample_topic']}")
    print("-" * 68)
    print("  Switch track anytime: python -m harness select <math|science|humanities|economics>")
    print("=" * 68)


def main():
    parser = argparse.ArgumentParser(description="AI Bootcamp Black-Box Test Harness")
    subparsers = parser.add_subparsers(dest="command")

    check_parser = subparsers.add_parser("check", help="Run a checkpoint slice check")
    check_parser.add_argument("slice_id", help="Slice identifier (e.g. 0, 1.1, 1.2, 1.3, 2.1, etc.)")
    check_parser.add_argument(
        "--subject", "-s",
        help="Optional subject pack override (math, science, humanities, economics)",
        default=None
    )

    subparsers.add_parser("tracks", help="List available pluggable subject packs")

    select_parser = subparsers.add_parser("select", help="Select active subject pack for the bootcamp")
    select_parser.add_argument("subject_id", choices=list(SUBJECT_PACKS.keys()), help="Subject track ID")

    args = parser.parse_args()

    if args.command == "tracks":
        print_tracks()
        sys.exit(0)
    elif args.command == "select":
        pack = set_active_subject(args.subject_id)
        print("=" * 68)
        print(f"  [✓] ACTIVE SUBJECT TRACK SET TO: {pack['title']} ({pack['id']})")
        print(f"  [✓] Teacher Persona: {pack['teacher_persona']}")
        print(f"  [✓] Default Classroom Topic: {pack['sample_topic']}")
        print("=" * 68)
        sys.exit(0)
    elif args.command == "check":
        if args.subject:
            os.environ["BOOTCAMP_SUBJECT"] = args.subject.strip().lower()
        slice_id = str(args.slice_id).strip()
        if slice_id in DISPATCHER:
            success = DISPATCHER[slice_id]()
            sys.exit(0 if success else 1)
        else:
            print(f"Unknown slice identifier: '{slice_id}'")
            print(f"Available slices: {', '.join(DISPATCHER.keys())}")
            sys.exit(1)
    else:
        run_preflight()


if __name__ == "__main__":
    main()
