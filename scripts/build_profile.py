#!/usr/bin/env python3
"""Generate README.md and preview.html from profile.json using only the standard library."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "profile.json"


def load_data() -> dict:
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def markdown_links(data: dict) -> str:
    return " / ".join(
        [
            f"[Email](mailto:{data['email']})",
            f"[GitHub]({data['github']})",
            f"[ORCID](https://orcid.org/{data['orcid']})",
        ]
    )


def publication_markdown(item: dict, index: int | None = None) -> str:
    prefix = f"{index}. " if index is not None else ""
    links = [f"[paper]({item['paper']})"]
    if item.get("code"):
        links.append(f"[code]({item['code']})")
    return (
        f"{prefix}**{item['title']}**  \n"
        f"   {item['authors']}. *{item['venue']}*, {item['details']}. "
        + " / ".join(links)
    )


def build_readme(data: dict) -> str:
    institution = data["institution"]
    lines = [
        "<!-- Generated from profile.json by scripts/build_profile.py. -->",
        f'<img src="{data["avatar"]}" alt="{data["name"]}" width="180" align="right" />',
        "",
        f"# {data['name']}",
        "",
        f"**{data['title']}**  ",
        f"[{institution['name']}]({institution['url']})",
        "",
        markdown_links(data),
        "",
    ]
    for paragraph in data["bio"]:
        lines.extend([paragraph, ""])
    lines.extend(['<br clear="right" />', "", "## Selected Publications", ""])
    for index, publication in enumerate(data["publications"], start=1):
        lines.extend([publication_markdown(publication, index), ""])
    if data.get("preprints"):
        lines.extend(["### Preprint", ""])
        for preprint in data["preprints"]:
            lines.extend([publication_markdown(preprint), ""])
    if data.get("awards"):
        lines.extend(["## Selected Awards", ""])
        lines.extend(f"- {award}" for award in data["awards"])
        lines.append("")
    if data.get("patents_and_service"):
        service = data["patents_and_service"]
        service = service.replace(
            "IEEE Transactions on Neural Networks and Learning Systems",
            "*IEEE Transactions on Neural Networks and Learning Systems*",
        ).replace(
            "IEEE Transactions on Systems, Man, and Cybernetics: Systems",
            "*IEEE Transactions on Systems, Man, and Cybernetics: Systems*",
        )
        lines.extend(["## Patents and Academic Service", "", service, ""])
    return "\n".join(lines)


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def publication_html(item: dict, numbered: bool = True) -> str:
    links = [f'<a href="{esc(item["paper"])}">paper</a>']
    if item.get("code"):
        links.append(f'<a href="{esc(item["code"])}">code</a>')
    content = (
        f'<strong>{esc(item["title"])}</strong>'
        f'<p>{esc(item["authors"])}. <em>{esc(item["venue"])}</em>, '
        f'{esc(item["details"])}. {" / ".join(links)}</p>'
    )
    return f"<li>{content}</li>" if numbered else f"<p>{content}</p>"


def build_preview(data: dict) -> str:
    institution = data["institution"]
    bio = "\n".join(f"<p>{esc(paragraph)}</p>" for paragraph in data["bio"])
    publications = "\n".join(publication_html(item) for item in data["publications"])
    preprints = "\n".join(publication_html(item, numbered=False) for item in data.get("preprints", []))
    awards = "\n".join(f"<li>{esc(award)}</li>" for award in data.get("awards", []))
    service = esc(data.get("patents_and_service", ""))
    service = service.replace(
        "IEEE Transactions on Neural Networks and Learning Systems",
        "<em>IEEE Transactions on Neural Networks and Learning Systems</em>",
    ).replace(
        "IEEE Transactions on Systems, Man, and Cybernetics: Systems",
        "<em>IEEE Transactions on Systems, Man, and Cybernetics: Systems</em>",
    )
    preprint_section = f"<h3>Preprint</h3>{preprints}" if preprints else ""
    awards_section = f"<h2>Selected Awards</h2><ul>{awards}</ul>" if awards else ""
    service_section = f"<h2>Patents and Academic Service</h2><p>{service}</p>" if service else ""
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="color-scheme" content="light dark" />
  <title>{esc(data['name'])}</title>
  <style>
    :root {{ --background:#fff; --text:#1f2328; --border:#d1d9e0; --link:#0969da; }}
    @media (prefers-color-scheme:dark) {{ :root {{ --background:#0d1117; --text:#f0f6fc; --border:#3d444d; --link:#4493f8; }} }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:var(--background); color:var(--text); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; font-size:16px; line-height:1.55; }}
    main {{ width:min(100% - 40px,900px); margin:56px auto 80px; }}
    .avatar {{ float:right; width:180px; height:180px; margin:0 0 24px 40px; object-fit:cover; }}
    h1 {{ margin:0 0 8px; font-size:2.2rem; line-height:1.2; }}
    h2 {{ margin:36px 0 16px; padding-bottom:7px; font-size:1.45rem; line-height:1.3; border-bottom:1px solid var(--border); }}
    h3 {{ margin:26px 0 12px; font-size:1.15rem; }}
    p {{ margin:0 0 16px; }}
    a {{ color:var(--link); text-decoration:none; }}
    a:hover {{ text-decoration:underline; }}
    .position {{ margin-bottom:12px; }} .links {{ margin-bottom:24px; }} .clear {{ clear:both; }}
    ol,ul {{ margin:0 0 16px; padding-left:2em; }} ol>li {{ margin-bottom:16px; }} li p {{ margin:4px 0 0; }}
    @media (max-width:620px) {{ main {{ width:min(100% - 32px,900px); margin-top:32px; }} .avatar {{ float:none; display:block; width:150px; height:150px; margin:0 0 24px; }} }}
  </style>
</head>
<body>
  <!-- Generated from profile.json by scripts/build_profile.py. -->
  <main>
    <img class="avatar" src="{esc(data['avatar'])}" alt="{esc(data['name'])}" />
    <h1>{esc(data['name'])}</h1>
    <p class="position"><strong>{esc(data['title'])}</strong><br /><a href="{esc(institution['url'])}">{esc(institution['name'])}</a></p>
    <p class="links"><a href="mailto:{esc(data['email'])}">Email</a> / <a href="{esc(data['github'])}">GitHub</a> / <a href="https://orcid.org/{esc(data['orcid'])}">ORCID</a></p>
    {bio}
    <div class="clear"></div>
    <h2>Selected Publications</h2>
    <ol>{publications}</ol>
    {preprint_section}
    {awards_section}
    {service_section}
  </main>
</body>
</html>
'''


def main() -> None:
    data = load_data()
    with (ROOT / "README.md").open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(build_readme(data))
    with (ROOT / "preview.html").open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(build_preview(data))
    print("Generated README.md and preview.html from profile.json")


if __name__ == "__main__":
    main()
