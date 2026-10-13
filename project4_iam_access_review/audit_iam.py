#!/usr/bin/env python3
"""
audit_iam.py : AWS IAM access review from the credential report.

What it does
    Reads the IAM credential report (live from AWS, or from a saved CSV) and flags:
      1. Console users with no MFA                        (NIST 800-53 IA-2, AC-2)
      2. Active access keys older than the rotation limit (NIST 800-53 IA-5, AC-2)
      3. Active access keys that are unused or never used (NIST 800-53 AC-2, AC-2(3))
      4. Console passwords unused beyond the inactivity limit (NIST 800-53 AC-2(3))
      5. Root account without MFA, or with active access keys (NIST 800-53 IA-2, AC-6)

Safety
    Read only. By default it calls iam:GenerateCredentialReport and
    iam:GetCredentialReport. With --fresh it calls only IAM List and Get APIs.
    It never prints access key IDs or secrets (the report does
    not contain them). Redact your AWS account ID before sharing any output.

Usage
    Live:     python audit_iam.py --out findings.csv
    Fresh:    python audit_iam.py --fresh --out findings.csv   (skips the cached report)
    Offline:  python audit_iam.py --csv sample_credential_report.csv --as-of 2026-10-14 --out findings.csv

Exit code: 2 if any Critical or High finding exists, otherwise 0.
"""
import argparse
import csv
import io
import sys
import time
from datetime import datetime, timezone, timedelta

SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}

CONTROLS = {
    "ROOT_NO_MFA": "IA-2(1), AC-6",
    "ROOT_ACCESS_KEY": "AC-6, IA-5",
    "NO_MFA_CONSOLE": "IA-2(1), IA-2(2), AC-2",
    "STALE_ACCESS_KEY": "IA-5, AC-2",
    "UNUSED_ACCESS_KEY": "AC-2, AC-2(3)",
    "INACTIVE_CONSOLE_USER": "AC-2(3)",
}

RECOMMENDATIONS = {
    "ROOT_NO_MFA": "Enable MFA on the root user and store the device securely.",
    "ROOT_ACCESS_KEY": "Delete root access keys. Use IAM roles or users instead.",
    "NO_MFA_CONSOLE": "Register an MFA device and attach the MFA required policy.",
    "STALE_ACCESS_KEY": "Rotate the key: create a new one, update the application, deactivate then delete the old one.",
    "UNUSED_ACCESS_KEY": "Confirm the key is not needed, then deactivate and delete it.",
    "INACTIVE_CONSOLE_USER": "Confirm the user still needs access. Disable the console password if not.",
}


def parse_time(value):
    """Credential report timestamps are ISO 8601, or N/A, no_information, not_supported."""
    if value is None:
        return None
    value = value.strip()
    if value in ("", "N/A", "no_information", "not_supported"):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def is_true(value):
    return str(value).strip().lower() == "true"


def load_live_report():
    import boto3  # imported here so offline mode works without boto3 installed

    iam = boto3.client("iam")
    for _ in range(30):
        state = iam.generate_credential_report()["State"]
        if state == "COMPLETE":
            break
        time.sleep(2)
    else:
        sys.exit("Credential report did not complete in time. Try again.")
    content = iam.get_credential_report()["Content"].decode("utf-8")
    return list(csv.DictReader(io.StringIO(content)))


def load_fresh_report():
    """Build rows from live IAM List and Get calls. IAM caches the credential report
    for up to four hours, so use this when users changed recently."""
    import boto3

    iam = boto3.client("iam")

    def fmt(value):
        return value.isoformat() if value else "N/A"

    summary = iam.get_account_summary()["SummaryMap"]
    rows = [{
        "user": "<root_account>",
        "mfa_active": str(summary.get("AccountMFAEnabled", 0) == 1).lower(),
        "access_key_1_active": str(summary.get("AccountAccessKeysPresent", 0) > 0).lower(),
        "access_key_2_active": "false",
    }]
    for page in iam.get_paginator("list_users").paginate():
        for u in page["Users"]:
            name = u["UserName"]
            row = {
                "user": name,
                "user_creation_time": fmt(u["CreateDate"]),
                "password_last_used": fmt(u.get("PasswordLastUsed")),
            }
            try:
                iam.get_login_profile(UserName=name)
                row["password_enabled"] = "true"
            except iam.exceptions.NoSuchEntityException:
                row["password_enabled"] = "false"
            row["mfa_active"] = str(bool(iam.list_mfa_devices(UserName=name)["MFADevices"])).lower()
            keys = iam.list_access_keys(UserName=name)["AccessKeyMetadata"]
            for n in (1, 2):
                if n <= len(keys):
                    key = keys[n - 1]
                    used = iam.get_access_key_last_used(AccessKeyId=key["AccessKeyId"])["AccessKeyLastUsed"]
                    row[f"access_key_{n}_active"] = str(key["Status"] == "Active").lower()
                    row[f"access_key_{n}_last_rotated"] = fmt(key["CreateDate"])
                    row[f"access_key_{n}_last_used_date"] = fmt(used.get("LastUsedDate"))
                else:
                    row[f"access_key_{n}_active"] = "false"
            rows.append(row)
    return rows


def load_csv_report(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def days_between(later, earlier):
    return (later - earlier).days


def audit(rows, now, max_key_age, unused_days, inactive_days):
    findings = []

    def add(severity, user, kind, detail):
        findings.append({
            "severity": severity,
            "user": user,
            "finding": kind,
            "detail": detail,
            "nist_800_53": CONTROLS[kind],
            "recommendation": RECOMMENDATIONS[kind],
        })

    for row in rows:
        user = row["user"]
        if user == "<root_account>":
            if not is_true(row.get("mfa_active")):
                add("Critical", "root", "ROOT_NO_MFA", "Root account has no MFA device.")
            for n in ("1", "2"):
                if is_true(row.get(f"access_key_{n}_active")):
                    add("Critical", "root", "ROOT_ACCESS_KEY", f"Root access key {n} is active.")
            continue

        # 1. Console user without MFA
        if is_true(row.get("password_enabled")) and not is_true(row.get("mfa_active")):
            add("High", user, "NO_MFA_CONSOLE", "Console password is enabled and no MFA device is active.")

        # 4. Inactive console user
        if is_true(row.get("password_enabled")):
            last_used = parse_time(row.get("password_last_used"))
            created = parse_time(row.get("user_creation_time"))
            reference = last_used or created
            if reference and days_between(now, reference) > inactive_days:
                what = "last sign in" if last_used else "creation (never signed in)"
                add("Low", user, "INACTIVE_CONSOLE_USER",
                    f"Console password enabled, {days_between(now, reference)} days since {what}.")

        # 2 and 3. Access keys
        for n in ("1", "2"):
            if not is_true(row.get(f"access_key_{n}_active")):
                continue
            rotated = parse_time(row.get(f"access_key_{n}_last_rotated"))
            key_used = parse_time(row.get(f"access_key_{n}_last_used_date"))
            if rotated:
                age = days_between(now, rotated)
                if age > max_key_age:
                    add("Medium", user, "STALE_ACCESS_KEY",
                        f"Access key {n} is {age} days old (limit {max_key_age}).")
            if key_used is None:
                if rotated and days_between(now, rotated) > 7:
                    add("Medium", user, "UNUSED_ACCESS_KEY",
                        f"Access key {n} is active and has never been used.")
            else:
                idle = days_between(now, key_used)
                if idle > unused_days:
                    add("Medium", user, "UNUSED_ACCESS_KEY",
                        f"Access key {n} last used {idle} days ago (limit {unused_days}).")

    findings.sort(key=lambda f: (SEVERITY_ORDER[f["severity"]], f["user"], f["finding"]))
    return findings


def print_summary(rows, findings, now):
    users = [r for r in rows if r["user"] != "<root_account>"]
    print(f"IAM access review as of {now.date()}")
    print(f"Users reviewed: {len(users)} (plus the root account)")
    counts = {}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    if not findings:
        print("No findings.")
        return
    print("Findings: " + ", ".join(f"{counts[s]} {s}" for s in SEVERITY_ORDER if s in counts))
    print()
    width = max(len(f["user"]) for f in findings)
    for f in findings:
        print(f'[{f["severity"]:<8}] {f["user"]:<{width}}  {f["finding"]:<22} {f["detail"]}')


def write_csv(path, findings):
    fields = ["severity", "user", "finding", "detail", "nist_800_53", "recommendation"]
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(findings)


def main():
    parser = argparse.ArgumentParser(description="AWS IAM access review from the credential report")
    parser.add_argument("--csv", help="Use a saved credential report CSV instead of calling AWS")
    parser.add_argument("--fresh", action="store_true", help="Read live IAM data instead of the cached credential report")
    parser.add_argument("--out", help="Write findings to this CSV file")
    parser.add_argument("--max-key-age", type=int, default=90, help="Days before an access key counts as stale")
    parser.add_argument("--unused-days", type=int, default=45, help="Days of key inactivity before flagging")
    parser.add_argument("--inactive-days", type=int, default=90, help="Days of console inactivity before flagging")
    parser.add_argument("--as-of", help="Review date as YYYY-MM-DD (default: now). Useful for repeatable tests.")
    args = parser.parse_args()

    if args.as_of:
        now = datetime.strptime(args.as_of, "%Y-%m-%d").replace(tzinfo=timezone.utc) + timedelta(hours=23)
    else:
        now = datetime.now(timezone.utc)

    if args.csv:
        rows = load_csv_report(args.csv)
    elif args.fresh:
        rows = load_fresh_report()
    else:
        rows = load_live_report()
    findings = audit(rows, now, args.max_key_age, args.unused_days, args.inactive_days)
    print_summary(rows, findings, now)
    if args.out:
        write_csv(args.out, findings)
        print(f"\nWrote {len(findings)} findings to {args.out}")
    sys.exit(2 if any(f["severity"] in ("Critical", "High") for f in findings) else 0)


if __name__ == "__main__":
    main()
