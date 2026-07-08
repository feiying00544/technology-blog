"""PreToolUse hook for commit message validation.

Validates that git commit messages follow [Action][Module]Summary format
and prohibits Co-Authored-By trailers.

Reads hook input JSON from stdin, outputs decision JSON to stdout.

Usage in .claude/settings.local.json:
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/validate-commit-msg.py"
          }
        ]
      }
    ]
  }
}
"""
import sys
import json
import re


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")

    if "git commit" not in command:
        sys.exit(0)

    # Prohibit Co-Authored-By
    if "co-authored-by" in command.lower():
        deny("Co-Authored-By lines are prohibited in this project")

    # Only validate commits with -m flag
    if " -m " not in command and ' -m"' not in command and " -m'" not in command:
        sys.exit(0)

    msg = extract_message(command)
    if not msg:
        sys.exit(0)

    first_line = msg.strip().split("\n")[0].strip()
    pattern = r"^\[(Fix|Modify|Add|Remove)\]\[[A-Za-z,]+\].+"
    if not re.match(pattern, first_line):
        deny(
            "Commit message must match format: [Action][Module]Summary. "
            f"Valid actions: Fix, Modify, Add, Remove. Got: {first_line}"
        )

    sys.exit(0)


def extract_message(command):
    """Extract commit message from various quoting styles."""
    # heredoc: cat <<'EOF'\n...\nEOF
    heredoc_match = re.search(r"<<'EOF'\n(.+?)\nEOF", command, re.DOTALL)
    if heredoc_match:
        return heredoc_match.group(1).strip()

    # single quotes: -m 'message'
    sq_match = re.search(r"-m '([^']+)'", command)
    if sq_match:
        return sq_match.group(1)

    # double quotes: -m "message"
    dq_match = re.search(r'-m "([^"]+)"', command)
    if dq_match:
        return dq_match.group(1)

    return None


def deny(reason):
    """Print deny decision and exit."""
    result = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
