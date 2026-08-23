#!/usr/bin/env python3
import os, json, urllib.request, urllib.error, datetime, html
from pathlib import Path

USERNAME = os.environ.get("PROFILE_USERNAME", "Cyanex1702")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

def request_json(url, method="GET", body=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "cyanex1702-profile-generator",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def esc(v):
    return html.escape(str(v), quote=True)

def svg_shell(inner, width=960, height=260):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
text {{ font-family:"Courier New",monospace; }}
.title {{ fill:#7AFF8A;font-weight:700;letter-spacing:1px; }}
.label {{ fill:#5E9C68;font-size:13px;font-weight:700; }}
.value {{ fill:#D6FFD9;font-size:14px; }}
.dim {{ fill:#456D4C;font-size:11px; }}
.line {{ stroke:#173A1D;stroke-width:1; }}
@keyframes scan {{ from {{ transform:translateY(0) }} to {{ transform:translateY({height}px) }} }}
.scan {{ animation:scan 4s linear infinite; opacity:.24; }}
@keyframes blink {{ 50% {{ opacity:.25; }} }}
.blink {{ animation:blink 1.2s step-end infinite; }}
</style>
<rect width="100%" height="100%" fill="#020703"/>
<rect x="8" y="8" width="{width-16}" height="{height-16}" fill="none" stroke="#173A1D"/>
{inner}
<rect class="scan" x="10" y="0" width="{width-20}" height="2" fill="#7AFF8A"/>
</svg>"""

def save(name, text):
    (ASSETS / name).write_text(text, encoding="utf-8")

def human_age(ts):
    if not ts:
        return "UNKNOWN"
    dt = datetime.datetime.fromisoformat(ts.replace("Z","+00:00"))
    now = datetime.datetime.now(datetime.timezone.utc)
    delta = now - dt
    if delta.days:
        return f"{delta.days}D {delta.seconds//3600:02d}H"
    hours = delta.seconds // 3600
    if hours:
        return f"{hours}H {(delta.seconds%3600)//60:02d}M"
    return f"{delta.seconds//60}M"

def main():
    user = request_json(f"https://api.github.com/users/{USERNAME}")
    repos = request_json(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated")
    events = request_json(f"https://api.github.com/users/{USERNAME}/events/public?per_page=30")

    nonfork = [r for r in repos if not r.get("fork")]
    total_stars = sum(r.get("stargazers_count",0) for r in nonfork)
    total_forks = sum(r.get("forks_count",0) for r in nonfork)
    now = datetime.datetime.now(datetime.timezone.utc)
    active_30 = 0
    langs = {}
    for r in nonfork:
        pushed = r.get("pushed_at")
        if pushed:
            dt = datetime.datetime.fromisoformat(pushed.replace("Z","+00:00"))
            if (now-dt).days <= 30:
                active_30 += 1
        lang = r.get("language")
        if lang:
            langs[lang] = langs.get(lang,0)+1
    top_langs = ", ".join(k.upper() for k,_ in sorted(langs.items(),key=lambda kv:(-kv[1],kv[0]))[:4]) or "MIXED"

    telemetry = svg_shell(f"""
<text x="28" y="34" class="title" font-size="16">SYSTEM TELEMETRY / LIVE</text>
<line x1="28" y1="48" x2="932" y2="48" class="line"/>
<text x="32" y="82" class="label">PUBLIC REPOS</text><text x="245" y="82" class="value">{len(nonfork):02d}</text>
<text x="32" y="112" class="label">VISIBLE STARS</text><text x="245" y="112" class="value">{total_stars:02d}</text>
<text x="32" y="142" class="label">VISIBLE FORKS</text><text x="245" y="142" class="value">{total_forks:02d}</text>
<text x="32" y="172" class="label">FOLLOWERS</text><text x="245" y="172" class="value">{user.get('followers',0):02d}</text>
<text x="500" y="82" class="label">ACTIVE / 30D</text><text x="760" y="82" class="value">{active_30:02d}</text>
<text x="500" y="112" class="label">TOP I/O</text><text x="760" y="112" class="value">{esc(top_langs)}</text>
<text x="500" y="142" class="label">NODE</text><text x="760" y="142" class="value">{esc(USERNAME.upper())}</text>
<text x="500" y="172" class="label">STATE</text><text x="760" y="172" class="value blink">ONLINE</text>
<text x="32" y="214" class="dim">REFRESH :: GITHUB ACTIONS / REST API / {now.strftime('%Y-%m-%d %H:%M UTC')}</text>
""",960,240)
    save("terminal-telemetry.svg", telemetry)

    neofetch = svg_shell(f"""
<text x="28" y="34" class="title" font-size="16">NEOFETCH / {esc(USERNAME.upper())}</text>
<text x="55" y="78" fill="#7AFF8A" font-size="16">        .--.</text>
<text x="55" y="100" fill="#7AFF8A" font-size="16">     .-(    )-.</text>
<text x="55" y="122" fill="#7AFF8A" font-size="16">    (___.__)__)</text>
<text x="55" y="144" fill="#7AFF8A" font-size="16">     [0x1702]</text>
<text x="350" y="74" class="label">HANDLE</text><text x="505" y="74" class="value">{esc(USERNAME.upper())}</text>
<text x="350" y="102" class="label">HOST</text><text x="505" y="102" class="value">GITHUB</text>
<text x="350" y="130" class="label">KERNEL</text><text x="505" y="130" class="value">AI-SYSTEMS / OPEN-SOURCE</text>
<text x="350" y="158" class="label">SHELL</text><text x="505" y="158" class="value">MATRIX-TERM</text>
<text x="350" y="186" class="label">REPOS</text><text x="505" y="186" class="value">{len(nonfork)}</text>
<text x="350" y="214" class="label">TOP I/O</text><text x="505" y="214" class="value">{esc(top_langs)}</text>
""",960,250)
    save("neofetch.svg", neofetch)

    event = events[0] if events else {}
    repo_name = (event.get("repo") or {}).get("name","NO SIGNAL").split("/")[-1]
    event_type = event.get("type","NO EVENT").replace("Event","").upper()
    branch = "N/A"
    commits = ""
    payload = event.get("payload") or {}
    if event.get("type") == "PushEvent":
        ref = payload.get("ref") or ""
        branch = ref.split("/")[-1] if ref else "N/A"
        commits = str(payload.get("size",0))
    created = event.get("created_at","")
    packet = svg_shell(f"""
<text x="28" y="34" class="title" font-size="16">LAST PACKET / PUBLIC EVENT BUS</text>
<line x1="28" y1="48" x2="932" y2="48" class="line"/>
<text x="32" y="82" class="label">REPO</text><text x="245" y="82" class="value">{esc(repo_name.upper())}</text>
<text x="32" y="112" class="label">EVENT</text><text x="245" y="112" class="value">{esc(event_type)}</text>
<text x="32" y="142" class="label">BRANCH</text><text x="245" y="142" class="value">{esc(branch.upper())}</text>
<text x="32" y="172" class="label">COMMITS</text><text x="245" y="172" class="value">{esc(commits or 'N/A')}</text>
<text x="500" y="82" class="label">AGE</text><text x="725" y="82" class="value">{esc(human_age(created))}</text>
<text x="500" y="112" class="label">VISIBILITY</text><text x="725" y="112" class="value">PUBLIC</text>
<text x="500" y="142" class="label">BUS</text><text x="725" y="142" class="value blink">RECEIVED</text>
<text x="32" y="214" class="dim">TIMESTAMP :: {esc(created or 'UNKNOWN')}</text>
""",960,240)
    save("last-packet.svg", packet)

    # Contribution calendar via GraphQL.
    query = """
    query($login:String!){
      user(login:$login){
        contributionsCollection{
          contributionCalendar{
            totalContributions
            weeks{
              contributionDays{
                date
                contributionCount
                contributionLevel
              }
            }
          }
        }
      }
    }
    """
    try:
        gql = request_json(
            "https://api.github.com/graphql",
            method="POST",
            body={"query":query,"variables":{"login":USERNAME}}
        )
        cal = gql["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        days = [d for w in cal["weeks"] for d in w["contributionDays"]]
        colors = {
            "NONE":"#071009",
            "FIRST_QUARTILE":"#0B2B10",
            "SECOND_QUARTILE":"#135C20",
            "THIRD_QUARTILE":"#1F8F35",
            "FOURTH_QUARTILE":"#7AFF8A",
        }
        size,gap,x0,y0=12,3,66,78
        cells=[]
        for idx,d in enumerate(days):
            c=idx//7; r=idx%7
            cells.append(
                f'<rect x="{x0+c*(size+gap)}" y="{y0+r*(size+gap)}" width="{size}" height="{size}" rx="1" fill="{colors.get(d["contributionLevel"],"#071009")}"><title>{esc(d["date"])} :: {d["contributionCount"]}</title></rect>'
            )
        contrib = svg_shell(f"""
<text x="28" y="34" class="title" font-size="16">MATRIX CONTRIBUTION MEMORY / LIVE</text>
<text x="28" y="55" class="dim">TOTAL :: {cal.get("totalContributions",0)} CONTRIBUTIONS / LAST YEAR</text>
{''.join(cells)}
<text x="66" y="224" class="dim">LESS  [ ] [ ] [ ] [ ] [ ]  MORE</text>
""",960,250)
        save("matrix-contributions.svg", contrib)
    except Exception as e:
        print("Contribution calendar refresh skipped:", e)

if __name__ == "__main__":
    main()
