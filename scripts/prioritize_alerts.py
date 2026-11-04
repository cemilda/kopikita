#!/usr/bin/env python3
"""Mengurutkan alert Dependabot: KEV dulu, lalu severity, lalu EPSS (Lab L1.4).

Ekspor alert:
  gh api "repos/OWNER/REPO/dependabot/alerts?state=open&per_page=100" > dependabot.json

Jalankan (online: ambil KEV dari CISA dan EPSS dari FIRST):
  python scripts/prioritize_alerts.py --alerts dependabot.json --online

Jalankan offline dengan berkas yang sudah diunduh:
  python scripts/prioritize_alerts.py --alerts dependabot.json --kev kev.json --epss epss.json
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
EPSS_URL = "https://api.first.org/data/v1/epss?cve="
SEVERITY_RANK = {"critical": 4, "high": 3, "medium": 2, "moderate": 2, "low": 1}


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def fetch_json(url):
    with urllib.request.urlopen(url, timeout=30) as resp:  # noqa: S310 - URL tetap
        return json.load(resp)


def kev_set(kev_doc):
    return {v["cveID"] for v in kev_doc.get("vulnerabilities", [])}


def epss_map(epss_doc):
    return {row["cve"]: float(row["epss"]) for row in epss_doc.get("data", [])}


def summarize(alert):
    adv = alert.get("security_advisory", {})
    vuln = alert.get("security_vulnerability", {})
    patched = (vuln.get("first_patched_version") or {}).get("identifier", "-")
    return {
        "number": alert.get("number"),
        "package": alert.get("dependency", {}).get("package", {}).get("name", "?"),
        "cve": adv.get("cve_id") or adv.get("ghsa_id", "-"),
        "severity": (adv.get("severity") or "low").lower(),
        "patched": patched,
    }


def prioritize(alerts, kev, epss):
    rows = []
    for alert in alerts:
        row = summarize(alert)
        row["kev"] = row["cve"] in kev
        row["epss"] = epss.get(row["cve"], 0.0)
        rows.append(row)
    rows.sort(key=lambda r: (not r["kev"], -SEVERITY_RANK.get(r["severity"], 0), -r["epss"]))
    return rows


def to_markdown(rows):
    lines = [
        "| Urutan | Alert | Paket | CVE | KEV | Severity | EPSS | Versi aman |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for i, r in enumerate(rows, 1):
        lines.append(
            f"| {i} | #{r['number']} | {r['package']} | {r['cve']} | {'YA' if r['kev'] else '-'} "
            f"| {r['severity']} | {r['epss']:.3f} | {r['patched']} |"
        )
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--alerts", required=True, help="JSON hasil gh api .../dependabot/alerts")
    ap.add_argument("--kev", help="berkas JSON katalog CISA KEV")
    ap.add_argument("--epss", help="berkas JSON respons API EPSS FIRST")
    ap.add_argument("--online", action="store_true", help="unduh KEV dan EPSS terbaru")
    args = ap.parse_args(argv)

    alerts = load_json(args.alerts)
    cves = sorted({summarize(a)["cve"] for a in alerts if summarize(a)["cve"].startswith("CVE-")})

    if args.online:
        kev = kev_set(fetch_json(KEV_URL))
        epss = epss_map(fetch_json(EPSS_URL + urllib.parse.quote(",".join(cves)))) if cves else {}
    else:
        kev = kev_set(load_json(args.kev)) if args.kev else set()
        epss = epss_map(load_json(args.epss)) if args.epss else {}

    print(to_markdown(prioritize(alerts, kev, epss)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
