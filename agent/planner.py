# agent/planner.py
import os
from openai import OpenAI
import json

client = OpenAI(base_url='https://api.gapgpt.app/v1', api_key=os.getenv('sk-NbWABY0lemmvyZVPxpWSovfH1D1NKwv8gxpGDcp6fYzpk3Kw'))

def plan_search_task(item: str) -> list:
    """We ask LLM to provide a short step-by-step program to find the price.
    Output: List of steps (string)"""
    prompt = (
    f"You are an assistant that returns a short JSON array of steps to find prices for: {item}. "
    "Return a JSON list of short steps, e.g. [\"search google\",\"open top 3 shopping results\",\"extract price and seller\"]"
    )

    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=200,
    )

    content = resp.choices[0].message.content
    text = content.strip() if content is not None else ""

    try:
        steps = json.loads(text)
        if isinstance(steps, list):
            return steps
    except Exception as e:
        print(f"Error parsing JSON: {e}")
    return []