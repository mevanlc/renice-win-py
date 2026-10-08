"""Command-line interface for renice-win-py."""

# Copyright (c) 2019, Giampaolo Rodola', Michael Clark. All rights reserved.
# Use of this source code is governed by a BSD-style license.

import argparse
import os

import psutil


PRIORITY_NAMES = ("real", "high", "above", "normal", "below", "idle")


def renice(process_name: str, priority: int) -> None:
    """Set the priority of every process matching *process_name*."""
    matched = False

    for process in psutil.process_iter(attrs=["name", "cmdline"]):
        command = process.info["cmdline"]
        if process.info["name"] != process_name and not (
            command and command[0] == process_name
        ):
            continue

        matched = True
        process.nice(priority)
        actual_priority = psutil.Process(process.pid).nice()
        print(f"{process.pid}\t{process.info['name']}\t{actual_priority}")

    if not matched:
        print("No matching processes found.")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="renice",
        description="Change the priority of Windows processes by name."
    )
    parser.add_argument("process_name", metavar="PROCESS_NAME")
    parser.add_argument("priority", choices=PRIORITY_NAMES)
    return parser


def main() -> None:
    args = _parser().parse_args()

    if os.name != "nt":
        raise SystemExit(
            "Platform not supported (Windows only).\n"
            "Hint: Use the built-in 'renice' command on Linux, Unix, macOS, or BSD."
        )

    priorities = {
        "real": psutil.REALTIME_PRIORITY_CLASS,
        "high": psutil.HIGH_PRIORITY_CLASS,
        "above": psutil.ABOVE_NORMAL_PRIORITY_CLASS,
        "normal": psutil.NORMAL_PRIORITY_CLASS,
        "below": psutil.BELOW_NORMAL_PRIORITY_CLASS,
        "idle": psutil.IDLE_PRIORITY_CLASS,
    }
    renice(args.process_name, priorities[args.priority])


if __name__ == "__main__":
    main()
