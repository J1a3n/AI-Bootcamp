"""
AI Bootcamp Unified CLI Runner
Usage:
  python -m harness check 0        (Pre-flight hardware & infrastructure doctor)
  python -m harness check 1.1      (Sprint 1, Slice 1.1)
  python -m harness check 1.2      (Sprint 1, Slice 1.2)
  python -m harness check 1.3      (Sprint 1, Slice 1.3)
  python -m harness check 2.1      (Sprint 2, Slice 2.1)
  python -m harness check 2.2      (Sprint 2, Slice 2.2)
  python -m harness check 3.1      (Sprint 3, Slice 3.1)
  python -m harness check 3.2      (Sprint 3, Slice 3.2)
  python -m harness check 4.1      (Sprint 4, Slice 4.1)
  python -m harness check 4.2      (Sprint 4, Slice 4.2 & Capstone)
"""
import sys
import argparse
from harness.preflight import run_preflight
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

def main():
    parser = argparse.ArgumentParser(description="AI Bootcamp Black-Box Test Harness")
    subparsers = parser.add_subparsers(dest="command")
    
    check_parser = subparsers.add_parser("check", help="Run a checkpoint slice check")
    check_parser.add_argument("slice_id", help="Slice identifier (e.g. 0, 1.1, 1.2, 1.3, 2.1, etc.)")
    
    args = parser.parse_args()
    
    if args.command == "check":
        slice_id = str(args.slice_id).strip()
        if slice_id in DISPATCHER:
            success = DISPATCHER[slice_id]()
            sys.exit(0 if success else 1)
        else:
            print(f"Unknown slice identifier: '{slice_id}'")
            print(f"Available slices: {', '.join(DISPATCHER.keys())}")
            sys.exit(1)
    else:
        # Default behavior: run preflight
        run_preflight()

if __name__ == "__main__":
    main()
