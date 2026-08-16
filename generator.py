import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

prompt = """
Build a standalone, single-file HTML/CSS/JavaScript utility web application.
Requirements:
1. Complete in a single `index.html` file (embed all CSS and JS).
2. Clean modern dark-mode UI with Tailwind CSS CDN.
3. Fully functional interactive tool (e.g., SEO Metadata Generator, Regex Tester, or Unit Converter).
4. Return ONLY valid, raw HTML without Markdown backticks or extra commentary.
"""

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
)

content = response.choices[0].message.content.strip()
if content.startswith("```html"):
    content = content[7:]
if content.startswith("```"):
    content = content[3:]
if content.endswith("```"):
    content = content[:-3]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content.strip())

print("Successfully generated index.html")
