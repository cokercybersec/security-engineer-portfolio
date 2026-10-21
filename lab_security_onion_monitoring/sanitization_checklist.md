# Sanitization checklist

Home network monitoring produces information that describes where a person lives and how their network is built. Before publishing anything from a lab like this, check every item.

| Item | Published? |
| --- | --- |
| Public or private IP addresses, subnets or ranges | No |
| MAC addresses | No |
| Hostnames, device names and device models | No |
| Router, switch and internet provider names or models | No |
| WiFi network names and passwords | No |
| Packet captures, logs, console screenshots and alert details | No |
| Names of family members or devices that identify them | No |
| Exact weakness that was found and fixed | No |
| The method, the design, the lessons and the limits | Yes |

## Rule of thumb

Publish the method, not the map. If a detail would help someone find or attack this specific network, it stays out. A diagram can show the shape of the design with generic labels. A result can be described at the level of the lesson it taught.

## Why it matters to a security team

The same discipline applies at work. Evidence from monitoring tools often contains personal data and system details, so a finding is shared in a form that proves the control works without exposing the environment.
