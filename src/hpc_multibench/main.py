#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The main function for the HPC MultiBench tool."""

from argparse import ArgumentParser
from pathlib import Path

from hpc_multibench.test_plan import TestPlan
from hpc_multibench.tui.interactive_ui import UserInterface

DEFAULT_BASE_OUTPUTS_DIRECTORY = Path("results/")


def get_parser() -> ArgumentParser:  # pragma: no cover
    """Get the argument parser for the tool."""
    parser = ArgumentParser(
        description="A Swiss army knife for comparing programs on HPC resources."
    )
    # As an argument of the base tool not subcommands, due to the ergonomics of
    # running `record` then `report` on same yaml file in sequence
    parser.add_argument(
        "-y",
        "--yaml-path",
        required=True,
        type=Path,
        help="the path to the configuration YAML file",
    )
    parser.add_argument(
        "-o",
        "--outputs-directory",
        type=Path,
        default=DEFAULT_BASE_OUTPUTS_DIRECTORY,
        help="the path to the configuration YAML file",
    )

    sub_parsers = parser.add_subparsers(dest="command", required=True)
    parser_record = sub_parsers.add_parser(
        "record", help="record data from running the test benches"
    )
    parser_interactive = sub_parsers.add_parser(
        "interactive", help="show the interactive TUI"
    )
    sub_parsers.add_parser(
        "report", help="report analysis about completed test bench runs"
    )

    parser_record.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="print but don't submit the generated sbatch files",
    )
    parser_record.add_argument(
        "-w",
        "--wait",
        action="store_true",
        help="wait for the submitted jobs to finish to exit",
    )
    for sub_parser in (parser_record, parser_interactive):
        sub_parser.add_argument(
            "-nc",
            "--no-clobber",
            action="store_true",
            help="don't delete any previous run results of the test benches",
        )
    return parser


def main() -> None:  # pragma: no cover
    """Run the tool."""
    args = get_parser().parse_args()
    test_plan = TestPlan(args.yaml_path, args.outputs_directory)

    if args.command == "record":
        test_plan.record_all(args)

    elif args.command == "report":
        test_plan.report_all(args)

    else:
        args.dry_run = False
        args.wait = False
        UserInterface(test_plan, args).run()
