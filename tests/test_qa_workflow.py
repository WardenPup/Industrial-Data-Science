"""Check that QA rejects invalid evidence and accepts valid source notebooks."""

import unittest

import nbformat

from scripts.check_commit_messages import validate_message
from scripts.validate_notebooks import validate_notebook


class QAWorkflowTests(unittest.TestCase):
    def test_commit_with_disclosures(self):
        message = (
            "ci(10.1): check execution\n\nAdd checks for repeatable validation.\n\n"
            "AI-Assistance: Codex\nHuman-Review: Pending\n"
        )
        self.assertEqual(validate_message(message), [])

    def test_commit_without_disclosures_is_rejected(self):
        self.assertTrue(validate_message("update stuff"))
        self.assertTrue(validate_message(
            "test(10.1): check export\n\nAdd checks.\n\nAI-Assistance: Codex\nHuman-Review: automatic\n"
        ))

    def test_valid_unexecuted_notebook(self):
        notebook = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell("2 + 2")])
        validate_notebook(notebook)

    def test_saved_error_rejected(self):
        cell = nbformat.v4.new_code_cell("raise ValueError('example')")
        cell.outputs = [nbformat.v4.new_output("error", ename="ValueError", evalue="example", traceback=[])]
        with self.assertRaises(ValueError):
            validate_notebook(nbformat.v4.new_notebook(cells=[cell]))

    def test_invalid_schema_rejected(self):
        notebook = nbformat.v4.new_notebook()
        notebook["metadata"] = "invalid"
        with self.assertRaises(nbformat.ValidationError):
            validate_notebook(notebook)


if __name__ == "__main__":
    unittest.main()
