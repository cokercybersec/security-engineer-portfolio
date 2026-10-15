# Data Classification Standard

Version 1.0. Date 2026-10-13. Owner: Information Security Officer. Review: every year.

This is a template written for a portfolio. It has not been reviewed by a lawyer and no organization has adopted it. Adapt it to your own business, laws and tools before using it.

## Purpose

This standard tells everyone how to label data and how to handle it. The higher the level, the stricter the rules. The goal is simple: protect data in proportion to the harm its exposure would cause.

## Scope

All data the company creates, receives or stores, in any form: files, email, chat, databases, paper and verbal. It applies to employees, contractors and vendors who handle company data.

## The four levels

| Level | Meaning | Examples | Harm if disclosed |
| --- | --- | --- | --- |
| Public | Approved for release to anyone. | Published web pages, press releases, job postings, marketing brochures. | None. The information is meant to be seen. |
| Internal | For employees and approved contractors only. | Internal memos, org charts, meeting notes, general procedures, project plans. | Minor. Some embarrassment or a small competitive disadvantage. |
| Confidential | Sensitive business or personal data for people with a need to know. | Customer lists, contracts, unreleased financial results, employee records, security assessments, vendor questionnaires. | Serious. Financial loss, legal exposure or loss of customer trust. |
| Restricted | The most sensitive data. Named individuals only. | Passwords, keys and tokens, payment card data, health records, government ID numbers, forensic data from an incident. | Severe. Major harm to people or the business and likely regulatory penalties. |

## Handling rules

| Topic | Public | Internal | Confidential | Restricted |
| --- | --- | --- | --- | --- |
| Labeling | Optional. | Label as Internal in the footer or file name where practical. | Label every page or file as Confidential. | Label every page or file as Restricted and list it in the data inventory. |
| Who may access | Anyone. | Employees and approved contractors. | Named people or roles with a business need, approved by the data owner. | Named individuals only, approved by the data owner and reviewed every quarter. |
| Storage | Any approved system. | Company approved systems only. | Company approved systems with access controls and encryption at rest. | Approved systems with encryption at rest and access logging. Never on personal devices or removable media. |
| Sharing inside the company | No limit. | No limit. | Only with people who need it, using links restricted to named people. | Only with named people approved by the owner. No forwarding and no group sharing. |
| Sharing outside the company | Allowed. | Only with a business reason and never in bulk. | Only with a signed agreement and the data owner's approval. | Only with data owner and security approval, a signed agreement and encryption. |
| Email and chat | Allowed. | Allowed on company accounts. | Company accounts only. Send links instead of copies where possible. | Do not send. Use the approved secure sharing tool. |
| Encryption in transit | Not required. | Required. TLS 1.2 or higher. | Required. TLS 1.2 or higher. No public networks without a VPN. | Required. TLS 1.2 or higher, and end to end encryption where available. |
| Printing | Allowed. | Allowed. | Avoid. Collect at once and shred when done. | Only with owner approval. Shred at once and log it. |
| Devices | Any device. | Approved apps with MFA on any device. | Company managed devices only. | Company managed devices only. No local copies. |
| Backups | Standard backups. | Standard backups. | Encrypted backups. | Encrypted backups with restricted access and a restore test every year. |
| AI tools and outside cloud services | Allowed. | Company approved tools only. | Company approved tools with a signed data agreement only. | Never. |
| Retention and disposal | Follow the records schedule. | Delete when no longer needed. | Delete on the retention schedule. Wipe or shred. | Delete as soon as the purpose ends. Certified wipe or destruction, recorded. |

## Classification rules

1. Every data set has an owner. The owner decides its level using the table above.
2. Data with no label is treated as Internal until the owner decides. Anything that looks like Restricted data is treated as Restricted at once.
3. A document that mixes levels takes the highest level in it.
4. Combining data can raise its level. A list of names is Internal. The same list with home addresses and ID numbers may be Restricted.
5. Owners review their levels every year and whenever the use of the data changes.
6. Lowering a level needs the owner's written approval.
7. If you lose Confidential or Restricted data, or see it exposed, report it the same day.

## Roles

| Role | Responsibility |
| --- | --- |
| Data owner | A manager accountable for a data set. Assigns the level, approves access and reviews both every year. |
| Data custodian | IT and security staff who apply the controls for each level, such as encryption, backups and logging. |
| Everyone | Handles data according to its level and reports mistakes and incidents the same day. |
| Information Security Officer | Owns this standard, approves exceptions with the data owner, and reports on compliance. |

## Exceptions and enforcement

Exceptions follow the process in the Acceptable Use Policy. Violations are handled as described there.
