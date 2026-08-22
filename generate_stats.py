import os
import requests

USERNAME = "snehasish-code"
TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}

def get_stats():
    user_res = requests.get(f"https://api.github.com/users/{USERNAME}", headers=HEADERS).json()
    repos_res = requests.get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100", headers=HEADERS).json()
    
    total_stars = 0
    languages = {}
    
    if isinstance(repos_res, list):
        for repo in repos_res:
            if not repo.get("fork"):
                total_stars += repo.get("stargazers_count", 0)
                lang = repo.get("language")
                if lang:
                    languages[lang] = languages.get(lang, 0) + 1
                    
    public_repos = user_res.get("public_repos", 0)
    followers = user_res.get("followers", 0)
    
    # Generate Stats SVG
    svg_stats = f"""<svg width="450" height="195" viewBox="0 0 450 195" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="450" height="195" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="2"/>
      <text x="30" y="40" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-weight="bold" font-size="18">Snehasish's GitHub Stats</text>
      
      <text x="30" y="80" fill="#94a3b8" font-size="14" font-family="sans-serif">⭐ Total Stars Earned:</text>
      <text x="350" y="80" fill="#7dd3fc" font-size="14" font-weight="bold" font-family="sans-serif">{total_stars}</text>
      
      <text x="30" y="115" fill="#94a3b8" font-size="14" font-family="sans-serif">📦 Public Repositories:</text>
      <text x="350" y="115" fill="#7dd3fc" font-size="14" font-weight="bold" font-family="sans-serif">{public_repos}</text>
      
      <text x="30" y="150" fill="#94a3b8" font-size="14" font-family="sans-serif">👥 Total Followers:</text>
      <text x="350" y="150" fill="#7dd3fc" font-size="14" font-weight="bold" font-family="sans-serif">{followers}</text>
    </svg>"""
    
    with open("stats.svg", "w", encoding="utf-8") as f:
        f.write(svg_stats)

    # Generate Top Languages SVG
    top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:4]
    total_lang_count = sum(languages.values()) or 1
    
    lang_rows = ""
    y = 80
    colors = ["#38bdf8", "#7dd3fc", "#0284c7", "#3b82f6"]
    for i, (lang, count) in enumerate(top_langs):
        pct = round((count / total_lang_count) * 100, 1)
        color = colors[i % len(colors)]
        lang_rows += f"""
        <circle cx="35" cy="{y-5}" r="5" fill="{color}"/>
        <text x="50" y="{y}" fill="#94a3b8" font-size="14" font-family="sans-serif">{lang}</text>
        <text x="350" y="{y}" fill="#7dd3fc" font-size="14" font-weight="bold" font-family="sans-serif">{pct}%</text>
        """
        y += 30

    svg_langs = f"""<svg width="450" height="195" viewBox="0 0 450 195" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="450" height="195" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="2"/>
      <text x="30" y="40" fill="#38bdf8" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-weight="bold" font-size="18">Top Languages</text>
      {lang_rows}
    </svg>"""

    with open("languages.svg", "w", encoding="utf-8") as f:
        f.write(svg_langs)

if __name__ == "__main__":
    get_stats()