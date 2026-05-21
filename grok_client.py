"""
grok_client.py
Handles all communication with the Grok API (xAI).
Keeps API logic fully separate from UI and prompt logic.
"""

import os
import json
from openai import OpenAI

def get_client() -> OpenAI:
    """
    Initialise the Grok-compatible OpenAI client.
    Reads the API key from Streamlit secrets or environment variable.
    """
    try:
        import streamlit as st
        api_key = st.secrets.get("GROK_API_KEY") or os.environ.get("GROK_API_KEY")
    except Exception:
        api_key = os.environ.get("GROK_API_KEY")

    if not api_key:
        raise ValueError(
            "Grok API key not found. "
            "Add GROK_API_KEY to .streamlit/secrets.toml or as an environment variable."
        )

    return OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",
    )


def call_grok(system_prompt: str, user_prompt: str, model: str = "grok-3") -> dict:
    """
    Send a prompt pair to Grok and return a parsed JSON dict.

    The caller (prompts.py) is responsible for instructing the model
    to return valid JSON. This function parses and returns it.

    Args:
        system_prompt: Sets the role/context for the model.
        user_prompt:   The actual generation request with project details.
        model:         Grok model name. Defaults to grok-3.

    Returns:
        Parsed dict from the model's JSON response.

    Raises:
        ValueError: If the response cannot be parsed as JSON.
        Exception:  Any API-level errors (auth, quota, network).
    """
    client = get_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=2000,
    )

    raw_text = response.choices[0].message.content.strip()

    # Strip markdown code fences if present
    if raw_text.startswith("```"):
        lines = raw_text.splitlines()
        # Remove opening fence (```json or ```)
        lines = lines[1:] if lines[0].startswith("```") else lines
        # Remove closing fence
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw_text = "\n".join(lines).strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Grok response was not valid JSON.\n"
            f"Parse error: {e}\n"
            f"Raw response:\n{raw_text}"
        )
