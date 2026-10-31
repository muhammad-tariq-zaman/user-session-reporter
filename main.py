"""Report user sessions from a CSV: active sessions, longest, per-user time.

Usage: python3 main.py sessions.csv
CSV columns: user,host,login,logout (logout empty means still active).
Times are ISO format, e.g. 2026-10-30T09:00:00.
"""
import argparse
import csv
import sys
from datetime import datetime


def parse_rows(rows, now):
    sessions = []
    for row in rows:
        login = datetime.fromisoformat(row["login"])
        logout = datetime.fromisoformat(row["logout"]) if row["logout"] else None
        end = logout or now
        sessions.append({"user": row["user"], "host": row["host"], "login": login,
                         "logout": logout, "active": logout is None,
                         "minutes": (end - login).total_seconds() / 60})
    return sessions


def summarise(sessions):
    active = [s for s in sessions if s["active"]]
    longest = max(sessions, key=lambda s: s["minutes"]) if sessions else None
    per_user = {}
    for session in sessions:
        per_user[session["user"]] = per_user.get(session["user"], 0) + session["minutes"]
    return {"active": len(active), "longest": longest, "per_user": per_user}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="CSV with user,host,login,logout columns")
    parser.add_argument("--now", default=None, help="Reference time ISO (default: now)")
    args = parser.parse_args(argv)
    now = datetime.fromisoformat(args.now) if args.now else datetime.now()
    with open(args.path, newline="", encoding="utf-8") as f:
        sessions = parse_rows(list(csv.DictReader(f)), now)
    summary = summarise(sessions)
    for session in sessions:
        state = "ACTIVE" if session["active"] else "closed"
        print(f"{session['user']}@{session['host']}: {state} ({session['minutes']:.0f} min)")
    print(f"{summary['active']} active session(s), {len(sessions)} total.")
    if summary["longest"]:
        print(f"Longest: {summary['longest']['user']} ({summary['longest']['minutes']:.0f} min).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
