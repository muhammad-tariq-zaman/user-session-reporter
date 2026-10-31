# user-session-reporter

Summarise login sessions from a CSV: who is still active, session lengths, longest session and per-user totals — useful for shared-machine audits.

## How to run

```sh
python3 main.py sessions.csv
```

## Example output

```
alice@pc1: closed (120 min)
bob@pc2: ACTIVE (120 min)
1 active session(s), 2 total.
Longest: alice (120 min).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
