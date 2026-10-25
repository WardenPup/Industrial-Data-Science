# Human-AI quality assurance

Each exercise uses `exercise/<chapter>.<number>` from the latest approved main.
Work through requirements → AI implementation → automated verification → human
review → revisions → explicit approval. Approval, merging, file deletion and
university submission require explicit user confirmation. A draft PR is not approval.

1. Read official requirements and create `reviews/exercise_<chapter>_<number>.md`
   from `reviews/TEMPLATE.md`. Record acceptance criteria and authentic provenance.
   Obtain approach confirmation unless already authorized for the current scope.
2. Implement on the exercise branch and disclose AI contributions. Keep reasoning
   and code understandable enough for the student to explain independently.
3. Run relevant commands, preserve actual outcomes and unresolved failures. Advance
   through TECHNICALLY_VALIDATED to AWAITING_HUMAN_REVIEW only after technical checks.
4. Present outputs, limitations and questions; stop for real student feedback.
   Record actual feedback before using CHANGES_REQUESTED or review commits.
5. Revise, link changes to feedback, rerun affected checks and request review again.
6. Record APPROVED and the real approval date only after explicit student approval.
   Obtain explicit confirmation for merging; never merge or submit automatically.

## Commits and identity

Use real, nonempty Conventional Commits with scopes such as `10.1` or `workflow`:

```text
ci(10.1): check Python execution and notebook validation

Describe the change and why it is needed.
State the commands actually run and their outcomes, or explicitly state not run.
Disclose that Codex produced or assisted with the change.

AI-Assistance: Codex
Human-Review: Pending
```

Use accurate Human-Review values: Pending, Feedback provided, Approved.
These fields disclose status; they do not prove that review occurred.
Keep authentic author/committer identity and timestamps. Do not impersonate a
student or bot, amend published history, or create empty commits for appearances.
Commits made through the configured account must not be described as independently
student-authored merely because Git identifies that account.

Configure the local default template once:

```text
git config --local commit.template .gitmessage
```

Git templates guide editors; they do not enforce messages passed with `-m`.
CI validates new commit subjects and disclosure trailers. No hooks or checks can
automatically validate a person's understanding or approval. Existing baseline
commits are preserved and excluded from retrospective message enforcement.

## Access and review controls

Before pushing, check authenticated repository write access and ensure no tokens,
datasets or tool binaries are staged. Use existing credential management; never
put tokens in files, commit messages, remote URLs or logs. GitHub checks receive
read-only contents permissions and do not merge, approve or submit anything.

Branch protection and required reviewer rules are not installed by these files.
They may be configured separately by the repository owner; this workflow does not
claim GitHub enforces human approval. The AI must obey the documented stop points.

## Adoption for 10.1

The genuine initial solution already exists in baseline `d243632` on main.
This PR introduces the workflow prospectively on `exercise/10.1`; it neither
recreates earlier stages nor removes existing work. Review the baseline code via
the links in the PR as well as the new diff. Exercise 10.2 waits for review of 10.1.
