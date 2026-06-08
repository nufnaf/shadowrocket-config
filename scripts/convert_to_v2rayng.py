#!/usr/bin/env python3
"""Convert Surge-format .list files to a v2rayNG-importable rules array.

Output: v2rayng-rules-array.json — a JSON array of `field` rules, ready to
paste into v2rayNG's "import rules from clipboard" / "import rules from file".

Mapping:
  DOMAIN-SUFFIX,foo.com  -> domain:foo.com
  DOMAIN,foo.com         -> full:foo.com
  DOMAIN-KEYWORD,foo     -> keyword:foo
  IP-CIDR,10.0.0.0/8     -> 10.0.0.0/8 (in `ip` array)

Other Surge directives (USER-AGENT, URL-REGEX, etc.) are silently skipped —
v2ray routing has no equivalent.

Run from anywhere; paths are resolved relative to the repo root.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# (filename, outbound_tag) — order mirrors shadowrocket.conf
GROUPS = [
    ("reject.list", "block"),
    ("direct.list", "direct"),
    ("proxy.list", "proxy"),
] + [(f"domains/{name}", "proxy") for name in [
    "autodesk.list", "discord.list", "facebook.list", "github.list",
    "instagram.list", "jetbrains.list", "linkedin.list", "medium.list",
    "openai.list", "claude.list", "copilot.list", "cursor.list",
    "grok.list", "google.list", "perplexity.list", "pornhub.list",
    "reddit.list", "redis.list", "telegram.list", "twitter.list",
    "whatsapp.list", "xvideos.list", "youtube.list",
]]


def parse_list(path: Path):
    domains, ips = [], []
    if not path.exists():
        return domains, ips
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split(",")]
        kind = parts[0].upper()
        val = parts[1] if len(parts) > 1 else ""
        if kind == "DOMAIN-SUFFIX":
            domains.append(f"domain:{val}")
        elif kind == "DOMAIN":
            domains.append(f"full:{val}")
        elif kind == "DOMAIN-KEYWORD":
            domains.append(f"keyword:{val}")
        elif kind in ("IP-CIDR", "IP-CIDR6", "IP6-CIDR"):
            ips.append(val)
    return domains, ips


def main():
    buckets = {tag: {"domain": [], "ip": []} for tag in ("block", "direct", "proxy")}
    for fname, tag in GROUPS:
        d, i = parse_list(REPO / fname)
        buckets[tag]["domain"].extend(d)
        buckets[tag]["ip"].extend(i)

    rules = []
    for tag in ("block", "direct", "proxy"):
        b = buckets[tag]
        if b["domain"]:
            rules.append({"type": "field", "outboundTag": tag, "domain": b["domain"]})
        if b["ip"]:
            rules.append({"type": "field", "outboundTag": tag, "ip": b["ip"]})

    out = REPO / "v2rayng-rules-array.json"
    out.write_text(json.dumps(rules, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"wrote {out.relative_to(REPO)}")
    for tag in ("block", "direct", "proxy"):
        b = buckets[tag]
        print(f"  {tag}: {len(b['domain'])} domains, {len(b['ip'])} ips")


if __name__ == "__main__":
    main()
