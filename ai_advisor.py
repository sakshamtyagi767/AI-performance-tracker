"""
ai_advisor.py
-------------
Sends system metrics to the Gemini API and retrieves structured
optimization advice.

Uses the new google-genai SDK (google.genai).
The prompt instructs Gemini to reply with valid JSON only,
so we can reliably parse its response in the reporter.
"""

import json
import re
from google import genai
from google.genai import types
from typing import Any

from config import get_api_key, GEMINI_MODEL


# ── Prompt Template ──────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
You are an expert system performance analyst.
You will receive a JSON object containing real-time system metrics.
Your job is to analyze the data and return optimization advice.

IMPORTANT: Reply with ONLY valid JSON - no markdown, no code fences,
no explanation outside the JSON. Use exactly this structure:

{
  "severity": "low | medium | high | critical",
  "overall_health_score": <integer 0-100>,
  "summary": "<one-sentence summary of system health>",
  "recommendations": [
    {
      "priority": "high | medium | low",
      "action": "<what to do>",
      "reason": "<why this helps>",
      "expected_savings": "<e.g. '2 GB RAM freed' or '15% CPU reduction'>"
    }
  ],
  "warnings": ["<any critical warning strings, can be empty list>"]
}
"""


# ── Main Function ─────────────────────────────────────────────────────────────

def get_ai_advice(metrics: dict[str, Any]) -> dict[str, Any]:
    """
    Send system metrics to the Gemini API and return structured advice.

    Args:
        metrics (dict): The system snapshot produced by monitor.collect_snapshot().

    Returns:
        dict: Parsed JSON advice from Gemini with severity, recommendations, etc.

    Raises:
        ValueError: If the API response cannot be parsed as valid JSON.
        Exception: Re-raises any API connectivity or auth errors.
    """
    # Initialise the new google-genai client with our API key
    client = genai.Client(api_key=get_api_key())

    # Convert metrics dict to a nicely formatted JSON string for the prompt
    metrics_json = json.dumps(metrics, indent=2)

    # Make the API call — system prompt is merged into user message
    # (some models like gemma do not support system_instruction)
    full_prompt = f"""{SYSTEM_PROMPT}

Here are my current system metrics. Please analyze them and return your advice as JSON:

{metrics_json}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=full_prompt,
    )

    raw_text: str = response.text.strip()

    # Parse the response
    parsed = _parse_json_response(raw_text)
    return parsed


def _parse_json_response(raw_text: str) -> dict[str, Any]:
    """
    Parse JSON from Gemini's response, handling edge cases like markdown fences.

    Args:
        raw_text (str): The raw string returned by the Gemini API.

    Returns:
        dict: The parsed JSON object.

    Raises:
        ValueError: If no valid JSON could be extracted.
    """
    # First, try parsing the raw text directly
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        pass

    # If that fails, try to extract a JSON block from markdown fences
    fence_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    match = re.search(fence_pattern, raw_text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # Last resort: find the first { ... } block in the text
    brace_pattern = r"\{[\s\S]*\}"
    match = re.search(brace_pattern, raw_text)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(
        f"Could not parse a valid JSON response from Gemini.\n"
        f"Raw response was:\n{raw_text}"
    )
