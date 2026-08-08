"""Helpers for per-model instructions attached to tool sources."""

from html import escape


def get_tool_instruction_ids(tools_dict: dict[str, dict]) -> list[str]:
    """Return stable instruction source IDs for tools actually exposed to the model."""
    result: list[str] = []
    seen: set[str] = set()

    for tool in tools_dict.values():
        instruction_ids = tool.get('instruction_ids') or []
        if isinstance(instruction_ids, str):
            instruction_ids = [instruction_ids]

        if not instruction_ids:
            tool_id = tool.get('tool_id')
            if tool_id:
                if tool.get('type') == 'terminal' or str(tool_id).startswith('terminal:'):
                    instruction_ids = [str(tool_id)]
                elif tool.get('type') != 'builtin':
                    instruction_ids = [f'tool:{tool_id}']

        for instruction_id in instruction_ids:
            if not isinstance(instruction_id, str) or not instruction_id or instruction_id in seen:
                continue
            seen.add(instruction_id)
            result.append(instruction_id)

    return result


def build_tool_instructions_prompt(model: dict, instruction_ids: list[str]) -> str | None:
    """Build a compact system block for configured instructions of active tool sources."""
    configured = model.get('info', {}).get('meta', {}).get('toolInstructions', {})
    if not isinstance(configured, dict):
        return None

    blocks = []
    for instruction_id in instruction_ids:
        instruction = configured.get(instruction_id)
        if not isinstance(instruction, str) or not instruction.strip():
            continue
        blocks.append(f'<tool id="{escape(instruction_id, quote=True)}">{escape(instruction.strip())}</tool>')

    if not blocks:
        return None

    return (
        '<tool_instructions>\n'
        'Use these instructions when deciding whether and how to use the named available tools.\n'
        + '\n'.join(blocks)
        + '\n</tool_instructions>'
    )
