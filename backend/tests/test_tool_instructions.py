import importlib.util
import unittest
from pathlib import Path

# Load the pure helper without importing open_webui.__init__, which boots CLI dependencies.
module_path = Path(__file__).parents[1] / 'open_webui' / 'utils' / 'tool_instructions.py'
spec = importlib.util.spec_from_file_location('tool_instructions', module_path)
tool_instructions = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(tool_instructions)
build_tool_instructions_prompt = tool_instructions.build_tool_instructions_prompt
get_tool_instruction_ids = tool_instructions.get_tool_instruction_ids


class ToolInstructionsTests(unittest.TestCase):
    def test_collects_source_ids_once_and_in_order(self):
        tools = {
            'search_memories': {'instruction_ids': ['builtin:memory'], 'type': 'builtin'},
            'add_memory': {'instruction_ids': ['builtin:memory'], 'type': 'builtin'},
            'run_command': {'tool_id': 'terminal:dev', 'type': 'terminal'},
            'repo_search': {'tool_id': 'github', 'type': 'external'},
        }
        self.assertEqual(
            get_tool_instruction_ids(tools),
            ['builtin:memory', 'terminal:dev', 'tool:github'],
        )

    def test_prompt_only_contains_active_configured_sources(self):
        model = {
            'info': {
                'meta': {
                    'toolInstructions': {
                        'builtin:memory': 'Use memory only for durable user facts.',
                        'terminal:dev': 'Use for shell and persistent project work.',
                        'tool:unused': 'This must not be injected.',
                    }
                }
            }
        }
        prompt = build_tool_instructions_prompt(model, ['terminal:dev', 'builtin:memory'])
        self.assertIn('terminal:dev', prompt)
        self.assertIn('builtin:memory', prompt)
        self.assertNotIn('tool:unused', prompt)

    def test_prompt_escapes_structure_and_ignores_empty_values(self):
        model = {
            'info': {
                'meta': {
                    'toolInstructions': {
                        'tool:x': 'Prefer x < y & keep structure.',
                        'tool:empty': '   ',
                    }
                }
            }
        }
        prompt = build_tool_instructions_prompt(model, ['tool:x', 'tool:empty'])
        self.assertIn('x &lt; y &amp; keep structure.', prompt)
        self.assertNotIn('tool:empty', prompt)


if __name__ == '__main__':
    unittest.main()
