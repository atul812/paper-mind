import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_research_gaps(accelerating_topics):

    prompt = f"""
You are a senior research scientist.

Accelerating topics:

{accelerating_topics}

Identify:

1. Emerging research gaps
2. Underexplored intersections
3. Future research opportunities

For each provide:

- Title
- Description
- Why it matters
- Potential research question
- Related keywords

Return exactly 3 opportunities.
"""

    response = model.generate_content(prompt)

    return response.text