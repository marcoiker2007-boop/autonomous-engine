import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Directory for individual agent micro-apps
os.makedirs("tools", exist_ok=True)

# 1. Define distinct agent strains & prompt variations
agent_strains = [
    {
        "id": "agent_1_seo",
        "name": "Live Meta & OpenGraph Previewer",
        "category": "Marketing & SEO",
        "prompt": "Build an interactive real-time SEO Meta Tag and OpenGraph social card preview tool in dark mode Tailwind CSS.",
    },
    {
        "id": "agent_2_dev",
        "name": "JSON to TypeScript / Python Type Converter",
        "category": "Developer Tools",
        "prompt": "Build a live JSON-to-TypeScript interfaces and Python TypedDict parser with copy buttons in dark mode Tailwind CSS.",
    },
    {
        "id": "agent_3_crypto",
        "name": "Web3 Gas Fee & Gwei Profit Estimator",
        "category": "Crypto & Finance",
        "prompt": "Build a clean Ethereum and Solana gas fee converter and transaction cost estimator in dark mode Tailwind CSS.",
    },
    {
        "id": "agent_4_sales",
        "name": "Cold Outreach Subject Line Analyzer",
        "category": "Copywriting",
        "prompt": "Build a cold email subject line scorer with spam word detection and readability grades in dark mode Tailwind CSS.",
    },
]

deployed_tools = []

for agent in agent_strains:
    system_prompt = f"""
    Build a standalone, single-file HTML utility web application for: {agent['name']}.
    Requirements:
    1. Complete self-contained HTML/CSS/JS (embedded in a single document).
    2. Tailwind CSS CDN with high-contrast, modern dark-mode UI.
    3. Fully interactive client-side logic (no broken buttons or mock placeholders).
    4. Include a clean top banner with a 'Share Tool' and 'Support Developer' button.
    5. Return ONLY valid, raw HTML without Markdown code blocks or explanation.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": system_prompt}],
        temperature=0.7,
    )

    raw_html = response.choices[0].message.content.strip()
    if raw_html.startswith("```html"):
        raw_html = raw_html[7:]
    if raw_html.startswith("```"):
        raw_html = raw_html[3:]
    if raw_html.endswith("```"):
        raw_html = raw_html[:-3]

    filepath = f"tools/{agent['id']}.html"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(raw_html.strip())

    deployed_tools.append(
        {
            "id": agent["id"],
            "name": agent["name"],
            "category": agent["category"],
            "path": filepath,
        }
    )
    print(f"Generated {filepath}")

# 2. Build Central Hub (index.html) linking all deployed agent products
hub_html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Autonomous Venture Hub</title>
  <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen p-8 flex flex-col items-center">
  <div class="max-w-4xl w-full">
    <header class="mb-10 text-center">
      <h1 class="text-4xl font-extrabold tracking-tight bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
        Autonomous Agent Product Farm
      </h1>
      <p class="text-slate-400 mt-2 text-sm">Self-deployed micro-utility network running continuous iteration loops.</p>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      {"".join([f'''
      <div class="p-6 bg-slate-900 border border-slate-800 rounded-xl hover:border-indigo-500 transition shadow-lg">
        <span class="text-xs uppercase tracking-wider text-indigo-400 font-semibold">{t["category"]}</span>
        <h2 class="text-xl font-bold text-slate-100 mt-1 mb-3">{t["name"]}</h2>
        <a href="{t["path"]}" class="inline-block px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-lg text-sm transition">
          Launch Utility &rarr;
        </a>
      </div>
      ''' for t in deployed_tools])}
    </div>
  </div>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(hub_html)

print("Autonomous hub updated successfully.")
