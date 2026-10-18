"""Generate a contribution graph using GitHub CLI authentication, without dependencies."""
import json
import subprocess
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path


def render(days):
    if len(days) != 31:
        raise ValueError(f"Expected 31 contribution days, received {len(days)}")
    maximum = max(1, max(day["contributionCount"] for day in days))
    points = [(55 + i * 27, 185 - day["contributionCount"] / maximum * 130)
              for i, day in enumerate(days)]
    line = " ".join(f"{x},{y:.2f}" for x, y in points)
    total = sum(day["contributionCount"] for day in days)
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="920" height="250" viewBox="0 0 920 250" role="img" aria-labelledby="title desc">',
           '<title id="title">Actividad de GitHub · últimos 31 días</title>',
           f'<desc id="desc">{total} contribuciones, del {days[0]["date"]} al {days[-1]["date"]} (UTC). Datos visibles para GitHub Actions.</desc>',
           '<rect width="920" height="250" rx="8" fill="#0d1117"/>',
           '<g fill="#39ff14" font-family="sans-serif" font-size="12">',
           '<text x="30" y="30" font-size="18">Actividad de GitHub · últimos 31 días</text>']
    for value, y in [(maximum, 55), (0, 185)]:
        svg.append(f'<text x="20" y="{y + 4}">{value}</text><path d="M55 {y}H865" stroke="#30363d"/>')
    svg += [f'<polygon points="55,185 {line} 865,185" fill="#39ff14" opacity="0.12"/>',
            f'<polyline points="{line}" fill="none" stroke="#39ff14" stroke-width="2"/>']
    for i, (day, (x, y)) in enumerate(zip(days, points)):
        svg.append(f'<circle cx="{x}" cy="{y:.2f}" r="3"><title>{escape(day["date"])}: {day["contributionCount"]}</title></circle>')
        if i % 5 == 0:
            svg.append(f'<text x="{x}" y="210" text-anchor="middle">{day["date"][5:]}</text>')
    svg.append(f'<text x="30" y="235" fill="#8b949e">{total} contribuciones · actualizado {days[-1]["date"]} (UTC)</text></g></svg>\n')
    return "\n".join(svg)


def main():
    today = datetime.now(timezone.utc).date()
    start = today - timedelta(days=30)
    query = '''query($from: DateTime!, $to: DateTime!) {
      user(login: "MateoPalmeiro") {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar { weeks { contributionDays { date contributionCount } } }
        }
      }
    }'''
    payload = {"query": query, "variables": {"from": f"{start}T00:00:00Z", "to": f"{today}T23:59:59Z"}}
    result = subprocess.run(["gh", "api", "graphql", "--input", "-"],
                            input=json.dumps(payload), capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = sorted((day for week in weeks for day in week["contributionDays"]
                   if str(start) <= day["date"] <= str(today)), key=lambda day: day["date"])
    Path("activity.svg").write_text(render(days), encoding="utf-8")


if __name__ == "__main__":
    main()
