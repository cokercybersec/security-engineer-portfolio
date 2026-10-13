# Vendor Security Questionnaire

30 questions across the six NIST CSF 2.0 functions. Weight 3 is critical, 2 is important, 1 is good practice. A gating question forces a High rating if the answer scores 3 (see the rubric in the README). Ask the vendor for evidence with every answer: a report, a policy, a screenshot or a scan result.

## Govern

| ID | Question | Weight | Gating | CSF 2.0 | NIST 800-53 |
| --- | --- | --- | --- | --- | --- |
| Q01 | Do you maintain a written information security policy that management approves and reviews at least once a year? | 2 | No | GV.PO | PL-1 |
| Q02 | Is one named person accountable for security, with a direct line to executive leadership? | 2 | No | GV.RR | PM-2 |
| Q03 | Do you assess the security of your own critical suppliers and subprocessors, and give customers a current list of them? | 3 | No | GV.SC | SR-6 |
| Q04 | Do you hold an independent assurance report for this service (SOC 2 Type II or ISO 27001) issued in the last 12 months? | 3 | No | GV.OV | CA-2 |
| Q05 | Do you run a formal risk assessment at least once a year and track the risks until they are closed? | 2 | No | GV.RM | RA-3 |

## Identify

| ID | Question | Weight | Gating | CSF 2.0 | NIST 800-53 |
| --- | --- | --- | --- | --- | --- |
| Q06 | Do you keep an inventory of the systems and data stores that hold customer data? | 2 | No | ID.AM | CM-8 |
| Q07 | Will you store and process our data only in the regions we agree on, and tell us where it is? | 2 | No | ID.AM | SA-9 |
| Q08 | Do you scan for vulnerabilities at least monthly and fix critical findings within a set time? | 3 | No | ID.RA | RA-5 |
| Q09 | Do you run an independent penetration test at least once a year and share a summary with customers? | 2 | No | ID.IM | CA-8 |

## Protect

| ID | Question | Weight | Gating | CSF 2.0 | NIST 800-53 |
| --- | --- | --- | --- | --- | --- |
| Q10 | Is multi factor authentication required for all administrator and privileged access to production? | 3 | Yes | PR.AA | IA-2(1) |
| Q11 | Does the service support multi factor authentication and single sign on for our users? | 2 | No | PR.AA | IA-2 |
| Q12 | Is staff access to customer data limited by role, reviewed at least quarterly, and removed within 24 hours when someone leaves? | 3 | No | PR.AA | AC-2 |
| Q13 | Is customer data encrypted at rest with strong, managed keys? | 3 | Yes | PR.DS | SC-28 |
| Q14 | Is customer data encrypted in transit using TLS 1.2 or higher? | 3 | Yes | PR.DS | SC-8 |
| Q15 | Is each customer's data logically separated from other customers? | 2 | No | PR.DS | SC-4 |
| Q16 | Are systems built from hardened baselines and patched on a defined schedule? | 2 | No | PR.PS | CM-6 |
| Q17 | Do all staff complete security awareness training when hired and every year? | 1 | No | PR.AT | AT-2 |
| Q18 | Do you back up customer data and protect the backups with encryption and access control? | 2 | No | PR.DS | CP-9 |
| Q19 | Are production and development environments separated, with no real customer data used in development? | 2 | No | PR.IR | SA-3 |
| Q20 | Will you return our data in a usable format and certify its deletion within 30 days after the contract ends? | 2 | No | PR.DS | MP-6 |

## Detect

| ID | Question | Weight | Gating | CSF 2.0 | NIST 800-53 |
| --- | --- | --- | --- | --- | --- |
| Q21 | Do you log sign ins, administrator actions and data access, and keep the logs for at least 90 days? | 3 | No | DE.CM | AU-11 |
| Q22 | Is the environment monitored for unauthorized access or unusual activity around the clock? | 2 | No | DE.CM | SI-4 |
| Q23 | Are alerts triaged and investigated against a documented procedure? | 2 | No | DE.AE | AU-6 |

## Respond

| ID | Question | Weight | Gating | CSF 2.0 | NIST 800-53 |
| --- | --- | --- | --- | --- | --- |
| Q24 | Do you have a written incident response plan that you test at least once a year? | 3 | No | RS.MA | IR-8 |
| Q25 | Will you tell us within 72 hours of confirming an incident that affects our data? | 3 | Yes | RS.CO | IR-6 |
| Q26 | Do you have a security contact who is reachable around the clock for incidents? | 2 | No | RS.CO | IR-6 |
| Q27 | Do you do a root cause analysis after incidents that affect customers and share a written summary? | 2 | No | RS.AN | IR-4 |

## Recover

| ID | Question | Weight | Gating | CSF 2.0 | NIST 800-53 |
| --- | --- | --- | --- | --- | --- |
| Q28 | Do you have a disaster recovery plan with stated recovery time and recovery point targets? | 2 | No | RC.RP | CP-2 |
| Q29 | Have you tested restoring from backup or failing over in the last 12 months, with results written down? | 3 | No | RC.RP | CP-4 |
| Q30 | Do you tell customers about outages and recovery progress through a status page and direct updates? | 1 | No | RC.CO | IR-6 |
