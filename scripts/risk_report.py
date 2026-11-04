#!/usr/bin/env python3
"""Hitung metrik risiko dari alert code scanning (Lab L4.2).

Angka dihitung oleh skrip ini; Claude hanya menulis narasinya. Verifikasi dua angka
secara manual terhadap Security Overview sebelum mengirim laporan.

Ekspor data:
  gh api "repos/OWNER/REPO/code-scanning/alerts?per_page=100&state=all" > alerts.json

Jalankan:
  python scripts/risk_report.py --alerts alerts.json
"""
import argparse
import datetime
import json
import sys

SEV = {"critical": 4, "high": 3, "error": 3, "medium": 2, "warning": 2, "low": 1, "note": 1}


def parse_ts(value):
    if not value:
        return None
    return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))


def backlog(alerts):
    out = {}
    for a in alerts:
        if a.get("state") == "open":
            sev = (a.get("rule", {}).get("security_severity_level")
                   or a.get("rule", {}).get("severity") or "low").lower()
            out[sev] = out.get(sev, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: -SEV.get(kv[0], 0)))


def mttr_days(alerts):
    durations = []
    for a in alerts:
        created, fixed = parse_ts(a.get("created_at")), parse_ts(a.get("fixed_at"))
        if created and fixed:
            durations.append((fixed - created).total_seconds() / 86400)
    if not durations:
        return None
    return round(sum(durations) / len(durations), 1)


def dismissed_without_reason(alerts):
    return sum(1 for a in alerts if a.get("state") == "dismissed" and not a.get("dismissed_reason"))


def _sev(a):
    r = a.get("rule", {})
    return (r.get("security_severity_level") or r.get("severity") or "low").lower()


def top_risks(alerts, n=3):
    """Tiga alert terbuka teratas: severity tertinggi dulu, lalu yang paling lama terbuka."""
    terbuka = [a for a in alerts if a.get("state") == "open"]
    terbuka.sort(key=lambda a: (-SEV.get(_sev(a), 0), a.get("created_at") or ""))
    return [{"number": a.get("number"), "rule": a.get("rule", {}).get("id"), "severity": _sev(a),
             "path": a.get("most_recent_instance", {}).get("location", {}).get("path"),
             "created_at": a.get("created_at")} for a in terbuka[:n]]


def build(alerts):
    return {
        "total": len(alerts),
        "backlog_per_severity": backlog(alerts),
        "mttr_hari": mttr_days(alerts),
        "dismissed_tanpa_alasan": dismissed_without_reason(alerts),
        "top_risiko": top_risks(alerts),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--alerts", required=True)
    args = ap.parse_args(argv)
    with open(args.alerts, encoding="utf-8") as fh:
        print(json.dumps(build(json.load(fh)), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
