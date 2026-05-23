# Shadowrocket Config

## How to use
Open [Shadowrocket](https://www.shadowrocketdownload.com) and add configuration from url: 
`https://raw.githubusercontent.com/nufnaf/shadowrocket-config/master/shadowrocket.conf`

## Periodic Sync

Domain lists should be periodically synced with the community rule repository [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script). This repo maintains up-to-date rules for many services (OpenAI, Discord, Telegram, YouTube, GitHub, etc.) and is the primary upstream source for domain/IP rules.

To sync:
1. Compare `domains/<service>.list` against the corresponding file in [`rule/Shadowrocket/`](https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/Shadowrocket)
2. Add any new domains, IP-CIDR, or IP-ASN entries
3. Remove stale entries that are no longer relevant

## Usefull Links:
 - [Description of the configuration file format](https://manual.nssurge.com) (originally written for [Surge](https://nssurge.com), but also suitable for [Shadowrocket](https://www.shadowrocketdownload.com))
