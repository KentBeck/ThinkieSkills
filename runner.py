#!/usr/bin/env python3
import argparse
import os
import sys
from typing import Any, Dict

try:
    import yaml  # type: ignore
except Exception as exc:  # pragma: no cover
    print("Missing dependency: pyyaml. Run 'pip install -r requirements.txt'", file=sys.stderr)
    raise


def load_thinkie_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def prompt_user(questions):
    answers: Dict[str, str] = {}
    for q in questions or []:
        prompt = q.get("prompt", "")
        qid = q.get("id")
        if not qid:
            continue
        # Ensure visible separation
        print()
        user_input = input(f"{prompt}\n> ").strip()
        answers[qid] = user_input
    return answers


def render_output(template: str, answers: Dict[str, str]) -> str:
    # Use str.format with missing keys handled by leaving placeholders intact
    class Default(dict):
        def __missing__(self, key):  # type: ignore[override]
            return "{" + key + "}"

    return template.format_map(Default(**answers))


def main():
    parser = argparse.ArgumentParser(description="Run a Thinkie locally from YAML.")
    parser.add_argument(
        "--file",
        help="Path to a Thinkie YAML file (e.g. thinkies/fun_bit.yaml)",
        default=None,
    )
    parser.add_argument(
        "--thinkie",
        help="Known Thinkie id (e.g. fun_bit). Uses ./thinkies/<id>.yaml",
        default="fun_bit",
    )
    args = parser.parse_args()

    yaml_path = args.file
    if not yaml_path:
        yaml_path = os.path.join(os.path.dirname(__file__), "thinkies", f"{args.thinkie}.yaml")

    if not os.path.exists(yaml_path):
        print(f"Thinkie file not found: {yaml_path}", file=sys.stderr)
        sys.exit(1)

    thinkie = load_thinkie_yaml(yaml_path)

    name = thinkie.get("name", "Thinkie")
    intent = thinkie.get("intent", "")
    guidance = (thinkie.get("scaffold") or {}).get("guidance", "")
    questions = thinkie.get("questions", [])
    template = thinkie.get("output_template", "")

    print(f"\n=== {name} ===")
    if intent:
        print(intent)
    if guidance:
        print("\nGuidance:")
        print(guidance)

    answers = prompt_user(questions)

    print("\n--- Suggested Next Step ---\n")
    print(render_output(template, answers))


if __name__ == "__main__":
    main()


