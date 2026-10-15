# Policy Pack: Data Classification Standard and Acceptable Use Policy

Two plain language policies written as templates, with a mapping of every policy element to NIST CSF 2.0 and NIST SP 800-53 Rev. 5. Built to show I can turn security requirements into rules people can actually follow. Completed 2026-10-13.

## These are templates
I wrote these documents for my portfolio. They have not been reviewed by a lawyer, no organization has adopted them, and they are not legal advice. Adapt them to your own business, laws and tools before using them.

## Objective
Show how to write policy that a new employee can read in a few minutes, that a manager can enforce, and that an auditor can trace back to a framework.

## Method
1. Defined four data levels (Public, Internal, Confidential, Restricted) with a meaning, examples and the harm if the data is exposed.
2. Wrote handling rules for 12 topics at each level, such as storage, sharing, email, printing, devices, backups, AI tools and disposal, so the rules get stricter as the level rises.
3. Added seven classification rules, for example that a document mixing levels takes the highest one and that combining data can raise its level.
4. Wrote a one page Acceptable Use Policy: what you may do, must do and must not do, plus monitoring, a four step exception process, enforcement and yearly acknowledgement.
5. Mapped 17 policy elements to a NIST CSF 2.0 subcategory and to NIST SP 800-53 Rev. 5 controls.
6. Generated the markdown files, the PDF and the quick reference card from one source file so they cannot drift apart.

## Design choices
1. Plain language first. Short sentences, no legal wording, one action per rule.
2. Rules in a table by level, so people find their answer in one lookup.
3. Unlabeled data is treated as Internal, and anything that looks like Restricted data is treated as Restricted at once.
4. AI tools and outside cloud services are covered explicitly: never for Restricted data, and only with a signed data agreement for Confidential data.
5. Exceptions expire after 12 months at most and are logged in the risk register, which connects this project to Project 5.

## Limits
1. Templates only. No organization has adopted them and no lawyer has reviewed them.
2. The rules assume a mid sized company with company managed devices and a password manager. A small team or a fully remote one would need changes.
3. Policy is not control. Nothing here shows the rules are followed. That needs training, technical enforcement and audits.
4. Retention periods are not set. They depend on the laws and contracts that apply to each business.
5. Mappings are my study mappings, not an official crosswalk. Check them against the current NIST publications before you rely on them.

## Files
1. data_classification_standard.md: the standard, readable on GitHub.
2. acceptable_use_policy.md: the acceptable use policy.
3. framework_mapping.md and framework_mapping.csv: the 17 mappings.
4. policy_pack.pdf: both policies and the mapping, formatted for reading and printing.
5. classification_card.png: a one page quick reference for the four levels.
