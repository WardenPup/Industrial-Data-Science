"""Check prospective commit subjects and truthful-disclosure field syntax.

This validates format only; it cannot establish human review or authorship.
"""

import argparse
import re
import subprocess

SUBJECT = re.compile(r"(?:feat|fix|docs|test|ci|chore|refactor|review)\((?:\d+\.\d+|workflow)\)!?: .+\S$")


def validate_message(message: str) -> list[str]:
    lines = message.strip().splitlines()
    errors = []
    if not lines or not SUBJECT.fullmatch(lines[0]):
        errors.append("use type(exercise or workflow): meaningful description")
    if len(lines) < 3 or not lines[2].strip():
        errors.append("include a body describing changes, rationale and actual validation")
    if len(re.findall(r"^AI-Assistance: \S.+$", message, re.MULTILINE)) != 1:
        errors.append("include exactly one explicit AI-Assistance trailer")
    if len(re.findall(r"^Human-Review: (?:Pending|Feedback provided|Approved)$", message, re.MULTILINE)) != 1:
        errors.append("include exactly one valid Human-Review trailer")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--head", default="HEAD")
    args = parser.parse_args()
    base = subprocess.check_output(["git", "merge-base", args.base, args.head], text=True).strip()
    commits = subprocess.check_output(["git", "rev-list", "--reverse", f"{base}..{args.head}"], text=True).splitlines()
    failures = []
    for commit in commits:
        message = subprocess.check_output(["git", "show", "-s", "--format=%B", commit], text=True)
        errors = validate_message(message)
        if errors:
            failures.append(f"{commit[:12]}: {'; '.join(errors)}")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"PASS: {len(commits)} new commit message(s); baseline excluded. Format does not prove human approval.")


if __name__ == "__main__":
    main()
