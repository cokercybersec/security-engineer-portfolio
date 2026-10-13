# Project 4 runbook: AWS IAM access review and MFA enforcement

Time needed: about 90 minutes across Days 2 to 4. Cost: zero. IAM users, policies and the credential report are free.
Where to run: AWS CloudShell (the terminal icon at the top of the AWS console). It has the AWS CLI, Python and boto3 already set up and uses your console login, so there is nothing to install.

Rules for this lab
1. Use only the two test users created below. Do not touch any other user.
2. Never paste access keys, passwords or your account ID into chat, a post or the repo. This runbook discards the key output on purpose.
3. Write down what actually happens. If a result differs from the expected one, record the real result and say so in the write up. Do not edit results to match.

## Step 1: Upload the files (5 min)
In CloudShell choose Actions, then Upload file. Upload audit_iam.py and mfa_required_policy.json.

## Step 2: Create two test users with deliberate weaknesses (10 min)
Run `set +H` first. CloudShell's bash treats an exclamation mark in a command as history expansion and will refuse the password line otherwise.
```
set +H
ACCT=$(aws sts get-caller-identity --query Account --output text)

# Test user 1: console password, no MFA
aws iam create-user --user-name ar-test-nomfa
PW=$(python3 -c "import secrets,string;print(''.join(secrets.choice(string.ascii_letters+string.digits+'!@#%^*') for _ in range(24)))")
aws iam create-login-profile --user-name ar-test-nomfa --password "$PW" --password-reset-required
unset PW

# Test user 2: an access key that is never used (output discarded so no secret is shown)
aws iam create-user --user-name ar-test-key
aws iam create-access-key --user-name ar-test-key > /dev/null
```
You never need to sign in as either user. The password and key exist only so the credential report has something to flag.

## Step 3: Run the access review (10 min)
```
python3 audit_iam.py --fresh --out findings.csv
```
Important: IAM caches the credential report for up to four hours. If you ran the review before creating the test users, the default mode (no --fresh) returns the old report and the new users will be missing. This happened in the real run, which is why --fresh exists. It reads the same fields from live IAM List and Get calls.

Expected: a High finding for ar-test-nomfa (console password, no MFA). The key on ar-test-key is brand new, so it is not flagged as stale or unused yet. Never used keys get a 7 day grace period by design.

Show the other checks with a simulated review date (the lab key cannot be old yet):
```
python3 audit_iam.py --fresh --as-of 2027-01-20 --out findings_future.csv
```
Record in the write up that this run used a simulated date. Expected: the High, a stale key, an unused key and an inactive console user.

A review before any test users exist is a useful baseline, so run `python3 audit_iam.py --out findings_baseline.csv` at the very start of Step 2 if you want one.

Also run the script on the synthetic sample to show the stale key, unused key and root account logic. This data is invented and must be labeled synthetic wherever you show it:
```
python3 audit_iam.py --csv sample_credential_report_SYNTHETIC.csv --as-of 2026-10-14 --out findings_synthetic.csv
```
Download findings.csv, findings_future.csv and findings_synthetic.csv with Actions, then Download file.
Screenshot the terminal output for the real run. The script never prints your account ID, but check before posting.

Also note, honestly, whether your own account's root user has MFA. The script reports it. If it says no, that is a real finding on your own account, and fixing it (Security credentials, assign MFA) is the right move and a good line for the write up.

## Step 4: Create and attach the MFA required policy (10 min)
```
aws iam create-policy --policy-name RequireMFA-Lab --policy-document file://mfa_required_policy.json > /dev/null
aws iam attach-user-policy --user-name ar-test-nomfa --policy-arn arn:aws:iam::$ACCT:policy/RequireMFA-Lab
aws iam attach-user-policy --user-name ar-test-nomfa --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess
```
ReadOnlyAccess gives the test user something to lose. The MFA policy then denies everything except MFA setup until MFA is present.

## Step 5: Prove it with the policy simulator (15 min)
```
UARN=arn:aws:iam::$ACCT:user/ar-test-nomfa

echo "--- MFA absent (context says false) ---"
aws iam simulate-principal-policy --policy-source-arn $UARN \
  --action-names s3:ListAllMyBuckets ec2:DescribeInstances \
  --context-entries ContextKeyName=aws:MultiFactorAuthPresent,ContextKeyValues=false,ContextKeyType=boolean \
  --query 'EvaluationResults[].[EvalActionName,EvalDecision]' --output table

echo "--- MFA present (context says true) ---"
aws iam simulate-principal-policy --policy-source-arn $UARN \
  --action-names s3:ListAllMyBuckets ec2:DescribeInstances \
  --context-entries ContextKeyName=aws:MultiFactorAuthPresent,ContextKeyValues=true,ContextKeyType=boolean \
  --query 'EvaluationResults[].[EvalActionName,EvalDecision]' --output table

echo "--- MFA setup action, MFA absent ---"
aws iam simulate-principal-policy --policy-source-arn $UARN \
  --action-names iam:CreateVirtualMFADevice \
  --resource-arns arn:aws:iam::$ACCT:mfa/ar-test-nomfa \
  --context-entries ContextKeyName=aws:MultiFactorAuthPresent,ContextKeyValues=false,ContextKeyType=boolean \
  --query 'EvaluationResults[].[EvalActionName,EvalDecision]' --output table

echo "--- No MFA context at all (like a long term access key) ---"
aws iam simulate-principal-policy --policy-source-arn $UARN \
  --action-names s3:ListAllMyBuckets \
  --query 'EvaluationResults[].[EvalActionName,EvalDecision]' --output table
```
Expected results, to compare with what you actually get:

| Case | Action | Expected decision |
| --- | --- | --- |
| MFA absent | s3:ListAllMyBuckets, ec2:DescribeInstances | explicitDeny |
| MFA present | s3:ListAllMyBuckets, ec2:DescribeInstances | allowed |
| MFA absent | iam:CreateVirtualMFADevice | allowed |
| No MFA context | s3:ListAllMyBuckets | explicitDeny |

The last row matters: the policy uses BoolIfExists, so a request with no MFA information is denied too. That means the policy is for human users and would break a user whose only credential is a long term access key. State that limit in the write up.

Screenshot each table. These are the evidence for the project.

## Step 6: Write up and commit (30 min)
README.md already holds the results of the real run on 2026-10-13. If you repeat the lab, replace the results and simulator tables with your own output. Then put the folder in security-engineer-portfolio/project4_iam_access_review, commit and push.

## Step 7: Clean up (5 min)
Run the commands in cleanup_commands.txt yourself in CloudShell. They delete only the two test users and the policy.

## Step 8: Post 2
The draft is in post2_draft.txt and the video is project4_iam_video_silent_9x16.mp4 with voiceover cues in project4_voiceover_script.md.
