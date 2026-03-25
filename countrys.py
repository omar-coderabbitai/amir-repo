#!/usr/bin/env python3

import argparse
import re
from pathlib import Path


def get_text_files(path: Path) -> list[Path]:
    if path.is_file():
        if path.suffix.lower() != ".txt":
            raise ValueError(f"{path} is not a .txt file.")
        return [path]

    if path.is_dir():
        return sorted(file for file in path.rglob("*.txt") if file.is_file())

    raise ValueError(f"{path} does not exist.")


def count_country_in_file(file_path: Path, pattern: re.Pattern[str]) -> tuple[int, int]:
    matching_items = 0
    total_mentions = 0

    with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            mentions_in_line = len(pattern.findall(line))
            if mentions_in_line:
                matching_items += 1
                total_mentions += mentions_in_line

    return matching_items, total_mentions


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Search .txt files for a country name. Each line is treated as one item. "
            "The script reports how many items contain the country and how many total mentions were found."
        )
    )
    parser.add_argument(
        "country",
        help="Country name to search for, for example: Italy",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="File or folder to search. Defaults to the current folder.",
    )
    args = parser.parse_args()

    search_path = Path(args.path).expanduser().resolve()
    text_files = get_text_files(search_path)

    if not text_files:
        print("No .txt files were found.")
        return

    escaped_country = re.escape(args.country.strip())
    pattern = re.compile(rf"(?i)\b{escaped_country}\b")

    total_files = 0
    total_items = 0
    total_mentions = 0

    for file_path in text_files:
        matching_items, mentions = count_country_in_file(file_path, pattern)
        if matching_items:
            total_files += 1
            total_items += matching_items
            total_mentions += mentions
            print(
                f"{file_path}: {matching_items} item(s) contain '{args.country}', "
                f"{mentions} total mention(s)"
            )

    print("\nSummary")
    print(f"Files searched: {len(text_files)}")
    print(f"Files with matches: {total_files}")
    print(f"Items containing '{args.country}': {total_items}")
    print(f"Total mentions of '{args.country}': {total_mentions}")


if __name__ == "__main__":
    main()
