import json
import re


def parse_llm_response(text):
    """Parse the LLM response text into a Python dict.

    Handles JSON wrapped in markdown code fences, and converts <red> tags
    to Ren'Py color tags.
    """

    if not text:
        return None

    # Strip markdown code fences if present
    text = text.strip()

    # Try to extract JSON from ```json ... ``` block
    m = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if m:
        text = m.group(1).strip()

    # Find the outermost { ... }
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or start >= end:
        return None
    text = text[start:end + 1]

    try:
        data = json.loads(text)
    except (json.JSONDecodeError, ValueError) as e:
        renpy.log("LLM JSON parse error: {}".format(str(e)))
        return None

    # Validate required top-level keys
    required_keys = ["opening_narrative", "locations", "npcs", "weapons", "accusation_outcomes"]
    for key in required_keys:
        if key not in data:
            renpy.log("LLM response missing key: {}".format(key))
            return None

    # Convert <red> tags in all string values
    data = _convert_red_tags(data)

    return data


def _convert_red_tags(obj):
    """Recursively convert <red>...</red> to Ren'Py {color} tags in all strings."""
    if isinstance(obj, dict):
        return {k: _convert_red_tags(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_red_tags(item) for item in obj]
    elif isinstance(obj, str):
        text = obj
        # Count and validate tags
        open_count = text.count("<red>")
        close_count = text.count("</red>")
        if open_count != close_count:
            # Unbalanced — strip all tags
            text = text.replace("<red>", "").replace("</red>", "")
            return text
        # Convert to Ren'Py color tags
        text = text.replace("<red>", "{color=#ff4444}").replace("</red>", "{/color}")
        return text
    else:
        return obj
