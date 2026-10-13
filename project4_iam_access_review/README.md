# AWS IAM Access Review and MFA Enforcement

A read only access review of an AWS account, followed by an MFA required policy that I tested with the IAM policy simulator. Built and run in my own AWS lab account on 2026-10-13.

## Objective
Show how a periodic access review finds common identity weaknesses (missing MFA, old or unused access keys, inactive users) and how a policy can enforce MFA, with each finding tied to NIST SP 800-53 controls.

## Scope
1. One personal AWS lab account. No production systems and no employer data.
2. Two test users created for this lab: ar-test-nomfa (console password, no MFA) and ar-test-key (an access key that has never been used).
3. Two existing lab users in the account were not touched.

## Method
1. Ran audit_iam.py against the clean account for a baseline.
2. Created the two test users and ran the review again.
3. Attached an MFA required deny policy (mfa_required_policy.json) plus ReadOnlyAccess to ar-test-nomfa.
4. Tested the policy with the IAM policy simulator: MFA context false, true, and absent.
5. Re-ran the review with a simulated review date to exercise the key and inactivity checks.

audit_iam.py is read only. Its default mode uses the IAM credential report. The --fresh mode uses IAM List and Get calls and does not need the report.

## Results from my real run

Baseline (clean account): 2 users reviewed, 0 findings, including the root account checks.

After creating the test users (--fresh): 4 users reviewed, 1 High finding.

| Severity | User | Finding | NIST 800-53 |
| --- | --- | --- | --- |
| High | ar-test-nomfa | NO_MFA_CONSOLE: console password enabled, no MFA device active | IA-2(1), IA-2(2), AC-2 |

Simulated review date of 2027-01-20 (99 days later): 1 High, 2 Medium, 1 Low.

| Severity | User | Finding | NIST 800-53 |
| --- | --- | --- | --- |
| High | ar-test-nomfa | NO_MFA_CONSOLE | IA-2(1), IA-2(2), AC-2 |
| Medium | ar-test-key | STALE_ACCESS_KEY: key is 99 days old (limit 90) | IA-5, AC-2 |
| Medium | ar-test-key | UNUSED_ACCESS_KEY: active and never used | AC-2, AC-2(3) |
| Low | ar-test-nomfa | INACTIVE_CONSOLE_USER: 99 days since creation, never signed in | AC-2(3) |

## Policy simulator results

| Case | Action | Expected | Actual |
| --- | --- | --- | --- |
| MFA absent | s3:ListAllMyBuckets, ec2:DescribeInstances | explicitDeny | explicitDeny |
| MFA present | s3:ListAllMyBuckets, ec2:DescribeInstances | allowed | allowed |
| MFA absent | iam:CreateVirtualMFADevice | allowed | allowed |
| No MFA context | s3:ListAllMyBuckets | explicitDeny | explicitDeny |

## What I learned
1. IAM caches the credential report for up to four hours. My first re-run after creating the test users still showed the old two users. I added a --fresh mode that reads live IAM data instead.
2. My first attempt to demonstrate key checks with tightened thresholds did not flag the new key. Never used keys get a 7 day grace period in the script. I demonstrated those checks with a simulated review date instead and labeled it as simulated.
3. The password generation command failed once because bash treated an exclamation mark as history expansion. Nothing was created on that attempt.

## NIST SP 800-53 mapping
1. AC-2 Account Management: reviewing accounts and removing unused ones.
2. AC-2(3) Disable Accounts: disabling inactive accounts and credentials.
3. IA-2(1) and IA-2(2) Multi-Factor Authentication: MFA for privileged and non privileged accounts.
4. IA-5 Authenticator Management: rotating access keys.
5. AC-6 Least Privilege: no root access keys, root used only when required.

## Limits
1. A lab account with two test users shows the method, not the state of any real organization.
2. The review covers IAM users. It does not cover IAM roles, federated identities or IAM Identity Center users.
3. The simulator evaluates policy. I did not sign in as the test users, so this does not prove a real sign in was blocked.
4. The policy uses BoolIfExists, so requests with no MFA information are denied. It suits human users and would break a user whose only credential is a long term access key.
5. The 99 day results use a simulated review date because a new lab key cannot be that old yet.
6. A real review also needs business context, such as who owns each account and whether the access is still needed.

## Files
1. audit_iam.py: the review script.
2. mfa_required_policy.json: the MFA required policy.
3. sample_credential_report_SYNTHETIC.csv: invented data for offline testing only.
4. RUNBOOK.md: steps to reproduce.
5. cleanup_commands.txt: removes the two test users and the lab policy.
