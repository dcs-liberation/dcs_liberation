from __future__ import annotations

import argparse
import contextlib
import logging
import subprocess
import sys
import textwrap
from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from datetime import date
from pathlib import Path
from typing import TextIO, TypeAlias

from game import VERSION


class ReportElement(ABC):
    @abstractmethod
    def __str__(self) -> str:
        ...


class Heading(ReportElement):
    def __init__(self, level: int, text: str) -> None:
        self.level = level
        self.text = text

    def __str__(self) -> str:
        return f"{'#' * self.level} {self.text}"


class H1(Heading):
    def __init__(self, text: str) -> None:
        super().__init__(1, text)


class H2(Heading):
    def __init__(self, text: str) -> None:
        super().__init__(2, text)


class H3(Heading):
    def __init__(self, text: str) -> None:
        super().__init__(3, text)


class Paragraph(ReportElement):
    def __init__(self, text: str) -> None:
        self.text = text

    def __str__(self) -> str:
        return textwrap.fill(self.text, width=80)


class UnorderedList(ReportElement):
    def __init__(self, items: Iterable[str]) -> None:
        self.items = list(items)
        if not self.items:
            raise ValueError("List has no data")

    def __str__(self) -> str:
        return "\n".join(f"* {item}" for item in self.items)


class Reporter:
    def __init__(self, output: TextIO) -> None:
        self.output = output

    def write(self, element: ReportElement) -> None:
        print(f"{element}\n", file=self.output)


ReportStream: TypeAlias = Iterator[ReportElement]


class LinterBase(ABC):
    def stream_reports(self) -> ReportStream:
        ...


class UncheckedDataLinter(LinterBase):
    def stream_reports(self) -> ReportStream:
        yield H2("Unchecked data")
        yield Paragraph("Any types of data not mentioned above are **not checked**.")


class Linter(LinterBase):
    def __init__(self, output: TextIO) -> None:
        self.reporter = Reporter(output)

    def run(self) -> None:
        for report in self.stream_reports():
            self.reporter.write(report)

    def stream_reports(self) -> ReportStream:
        yield H1("Liberation data report")
        yield self.describe_version()
        yield Paragraph(
            "This report documents missing supplemental data in Liberation. This is "
            "only able to report data that is missing as compared to pydcs. If pydcs "
            "is missing DCS data, that cannot be reported."
        )
        yield Paragraph(
            "**Accuracy of data cannot be verified by this report.** If data not "
            "mentioned in this report is present but **wrong**, file a bug."
        )
        yield from UncheckedDataLinter().stream_reports()

    def describe_version(self) -> ReportElement:
        sha = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        return Paragraph(
            f"This report was generated for DCS Liberation {VERSION} ({sha}) on "
            f"{date.today()} with pydcs {self.describe_pydcs()}."
        )

    def describe_pydcs(self) -> str:
        result = subprocess.run(
            ["pip", "freeze"], check=True, capture_output=True, text=True
        )
        pydcs_lines = [l for l in result.stdout.splitlines() if "pydcs" in l]
        if len(pydcs_lines) != 1:
            raise RuntimeError(
                "Could not find unique pydcs package in `pip freeze` output:\n"
                f"{result.stdout}"
            )
        version = pydcs_lines[0]
        if version.startswith("-e git+"):
            return self.format_pip_git(version)
        return version

    @staticmethod
    def format_pip_git(version: str) -> str:
        _, _, version = version.partition("+")
        if version.endswith("#egg=pydcs"):
            version, _, _ = version.rpartition("#")
        _, _, sha = version.partition("@")
        return sha


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "output_path",
        type=Path,
        nargs="?",
        help=(
            "Write the report to the given path. If omitted, the report will be "
            "written to stdout."
        ),
    )

    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args()
    if args.output_path is None:
        context = contextlib.nullcontext(sys.stdout)
    else:
        context = args.output_path.open("w")
    with context as output:
        Linter(output).run()


if __name__ == "__main__":
    main()
