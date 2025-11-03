#!/usr/bin/env python3
"""
MCP Server exposing Thinkies to Claude Desktop/Web.

Tools:
- thinkies.list() -> returns available Thinkies (id, name, intent)
- thinkies.run(id: str, answers?: object) -> renders output_template with provided answers

Usage (dev):
  python mcp_server.py

Then add this command as an MCP server in Claude Desktop (Tools → Developer → Add Server).
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

import yaml  # type: ignore

try:
    from mcp.server.fastmcp import FastMCP
except Exception as exc:
    raise SystemExit(
        "Missing dependency 'mcp'. Install with: pip install -r requirements.txt"
    ) from exc


ROOT_DIR = os.path.dirname(__file__)
THINKIES_DIR = os.path.join(ROOT_DIR, "thinkies")


def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def list_thinkie_files() -> List[str]:
    if not os.path.isdir(THINKIES_DIR):
        return []
    return [
        os.path.join(THINKIES_DIR, f)
        for f in os.listdir(THINKIES_DIR)
        if f.endswith(".yaml") or f.endswith(".yml")
    ]


def load_thinkie_by_id(thinkie_id: str) -> Dict[str, Any]:
    candidate = os.path.join(THINKIES_DIR, f"{thinkie_id}.yaml")
    if os.path.exists(candidate):
        return load_yaml(candidate)
    # fallback: scan by id field
    for path in list_thinkie_files():
        data = load_yaml(path)
        if data.get("id") == thinkie_id:
            return data
    raise FileNotFoundError(f"Thinkie not found: {thinkie_id}")


def render_output(template: str, answers: Dict[str, str]) -> str:
    class Default(dict):
        def __missing__(self, key):  # type: ignore[override]
            return "{" + key + "}"

    return template.format_map(Default(**answers))


app = FastMCP("thinkies")


@app.tool()
def thinkies_list() -> dict:
    """List available Thinkies (id, name, intent)."""
    items: List[Dict[str, Any]] = []
    for path in list_thinkie_files():
        data = load_yaml(path)
        items.append(
            {
                "id": data.get("id"),
                "name": data.get("name"),
                "intent": data.get("intent"),
            }
        )
    return {"thinkies": items}


@app.tool(
    args={
        "id": {
            "type": "string",
            "description": "Thinkie id to run (e.g., fun_bit)",
        },
        "answers": {
            "type": "object",
            "description": "Map from question id to answer text (optional). If omitted, questions are returned.",
            "additionalProperties": {"type": "string"},
            "required": False,
        },
    }
)
def thinkies_run(id: str, answers: Optional[Dict[str, str]] = None) -> dict:
    """Run a Thinkie and render its suggested next step using provided answers."""
    data = load_thinkie_by_id(id)
    questions = data.get("questions", [])
    template = data.get("output_template", "")

    # If answers are missing or incomplete, return the question schema to the client
    missing: List[str] = []
    answers = answers or {}
    for q in questions:
        qid = q.get("id")
        if qid and not answers.get(qid):
            missing.append(qid)

    if missing:
        return {
            "status": "needs_input",
            "message": "Please provide answers for the required question ids.",
            "required": missing,
            "questions": questions,
        }

    rendered = render_output(template, answers)
    return {
        "status": "ok",
        "id": data.get("id"),
        "name": data.get("name"),
        "result": rendered,
    }


if __name__ == "__main__":
    # FastMCP will handle stdio transport by default
    app.run()


