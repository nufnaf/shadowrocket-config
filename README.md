# Shadowrocket Config

## How to use

### Shadowrocket (iOS)
Open [Shadowrocket](https://www.shadowrocketdownload.com) and add configuration from url:
`https://raw.githubusercontent.com/nufnaf/shadowrocket-config/master/shadowrocket.conf`

### Clash Meta for Android (CMFA)
Shadowrocket's `.conf` format is not directly readable by CMFA, but the rule-set files in this repo (`domains/*.list`, `direct.list`, `proxy.list`, `reject.list`) use Surge `classical` syntax which Clash Meta supports natively via `rule-providers`. The repo's raw URLs can therefore be referenced directly — rules stay in sync automatically without re-converting.

Steps:

1. Install [ClashMetaForAndroid](https://github.com/MetaCubeX/ClashMetaForAndroid) (pick the `arm64-v8a` APK from Releases for most modern phones).
2. Create a `config.yaml` that:
   - Pulls nodes from your provider's Clash subscription via `proxy-providers` (interval ~3600s).
   - Pulls every rule list from this repo via `rule-providers` with `behavior: classical` and `format: text` (interval ~86400s).
   - Mirrors the rule order from `shadowrocket.conf`: `reject` → `direct` → `proxy` → per-service domain lists, terminating in `MATCH,DIRECT`.
3. Import the yaml in CMFA: **配置 → + → 从文件导入** (or from URL if you host the yaml somewhere).
4. Activate it; allow the VPN permission on first run.

Minimal sketch:

```yaml
proxy-providers:
  airport:
    type: http
    url: "<your-clash-subscription-url>"
    interval: 3600
    path: ./providers/airport.yaml
    health-check: { enable: true, url: https://www.gstatic.com/generate_204, interval: 300 }

proxy-groups:
  - { name: PROXY, type: select, proxies: [自动选择, DIRECT], use: [airport] }
  - { name: 自动选择, type: url-test, url: https://www.gstatic.com/generate_204, interval: 300, use: [airport] }

rule-providers:
  google:
    type: http
    behavior: classical
    format: text
    url: https://raw.githubusercontent.com/nufnaf/shadowrocket-config/master/domains/google.list
    path: ./ruleset/google.list
    interval: 86400
  # ... one entry per file under domains/, plus reject/direct/proxy

rules:
  - RULE-SET,reject,REJECT
  - RULE-SET,direct,DIRECT
  - RULE-SET,proxy,PROXY
  - RULE-SET,google,PROXY
  # ... one RULE-SET line per provider, matching shadowrocket.conf order
  - MATCH,DIRECT
```

**Update behavior:**
- Nodes (proxy-provider) and rules (rule-provider) refresh on their own intervals while the VPN is running. Manual refresh: 主页 → 代理 / 规则提供者 → 刷新图标.
- The `config.yaml` itself is a local file — CMFA does not re-read it from disk on its own. If the yaml structure changes (new sections, different group logic), re-import it. Simple list edits inside this repo do not require re-importing because they propagate via `rule-providers`.

The same yaml works in any mihomo-based client (Mihomo Party desktop, FlClash, sing-box with Clash compatibility, etc.).

### v2rayNG (Android)
v2rayNG uses V2Ray/Xray's JSON routing format and cannot consume Surge `.list` files or Clash `rule-providers` directly. The repo ships a converter:

```
python3 scripts/convert_to_v2rayng.py
```

This regenerates `v2rayng-rules-array.json` — a flat array of V2Ray `field` rules grouped into `direct` / `proxy` / `block` outbound tags, derived from the same `.list` files Shadowrocket uses.

To import in v2rayNG: **设置 → 路由设置 → 自定义** mode, then **从剪贴板导入规则集** (or "Import rules from clipboard") with the file's contents pasted in. Make sure your subscription's outbound tag matches `proxy` (configure outbound tags in 配置 outbounds if needed).

Caveats vs CMFA:
- **Snapshot, not live.** v2rayNG does not refetch rules from URLs. Edits to `.list` files in this repo require re-running the script and re-importing.
- USER-AGENT, URL-REGEX, and other Surge directives without V2Ray equivalents are silently skipped.
- v2rayNG typically does not parse Clash YAML subscriptions — use a vmess/vless/ss/trojan subscription URL or single-node links from your provider.

## Periodic Sync

Domain lists should be periodically synced with the community rule repository [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script). This repo maintains up-to-date rules for many services (OpenAI, Discord, Telegram, YouTube, GitHub, etc.) and is the primary upstream source for domain/IP rules.

To sync:
1. Compare `domains/<service>.list` against the corresponding file in [`rule/Shadowrocket/`](https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/Shadowrocket)
2. Add any new domains, IP-CIDR, or IP-ASN entries
3. Remove stale entries that are no longer relevant

## Usefull Links:
 - [Description of the configuration file format](https://manual.nssurge.com) (originally written for [Surge](https://nssurge.com), but also suitable for [Shadowrocket](https://www.shadowrocketdownload.com))
