#!/usr/bin/env python3
"""
Aktualisiert data.js für das Cyber-Lagebild-Dashboard.

Quellen:
  - security-incidents.de  (Sicherheitsvorfall-Datenbank, JSON-Endpunkt der Tabelle)
  - wid.cert-bund.de       (BSI CERT-Bund WID, öffentliche Kurzinformationen)
  - ransomware.live        (Ransomware-Opfer mit DE-Bezug; PRO-API mit Token, sonst HTML)

Aufruf:  python update_data.py      (nur Python 3 Standardbibliothek nötig)
Danach index.html im Browser neu laden.

Hinweis: Fuer ransomware.live wird ein PRO-API-Token genutzt, falls vorhanden
(Datei ransomware_token.txt oder Umgebungsvariable RANSOMWARE_LIVE_TOKEN).
Ohne Token dient die HTML-Laenderseite als Fallback. Die Actor-Profile in
data_actors.js und data_knowledge.js werden bewusst NICHT ueberschrieben.
"""
import json, ssl, sys, gzip, io, urllib.request, urllib.error, datetime, collections, os

INC_URL = "https://www.security-incidents.de/sicherheitsvorfall-datenbank/?cmd=getIncidents"
ADV_URL = "https://wid.cert-bund.de/content/public/securityAdvisory?size=1000&sort=published%2Cdesc&aboFilter=false"
RL_API  = "https://api-pro.ransomware.live/victims/?country=DE"  # bevorzugt, wenn API-Token vorhanden
RL_HTML = "https://www.ransomware.live/map/DE"                    # Fallback ohne Token (freie v2-API ist tot)
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
# Echter Browser-User-Agent – manche Server (Bot-Schutz) liefern sonst HTML statt JSON.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data.js")
OUT_RL = os.path.join(HERE, "data_ransomware.js")
OUT_KEV = os.path.join(HERE, "data_kev.js")
COUNTRY = "DE"          # Land, dessen Einzelvorfälle in die Tabelle kommen
ADV_KEEP = 400          # Anzahl CERT-Bund-Meldungen für die Tabelle


def get_json(url, referer=None, extra_headers=None):
    """Holt JSON wie ein Browser (gzip + realistische Header). Wirft bei Nicht-JSON
    eine aussagekräftige Meldung mit Textauszug statt eines kryptischen Parsefehlers."""
    headers = {
        "User-Agent": UA,
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "close",
    }
    if referer:
        headers["Referer"] = referer
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
            raw = r.read()
            if (r.headers.get("Content-Encoding") or "").lower() == "gzip":
                raw = gzip.decompress(raw)
            text = raw.decode("utf-8", "replace").lstrip("﻿ \r\n\t")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} von {url}")
    if not text or text[0] not in "[{":
        snippet = " ".join(text[:160].split()) or "(leere Antwort)"
        raise RuntimeError(f"Kein JSON von {url} – Antwort beginnt mit: {snippet!r}")
    return json.loads(text)


def get_text(url, referer=None):
    """Holt eine HTML-/Textseite wie ein Browser (gzip + realistische Header)."""
    headers = {
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        "Accept-Language": "de-DE,de;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close",
    }
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=90, context=ssl.create_default_context()) as r:
            raw = r.read()
            if (r.headers.get("Content-Encoding") or "").lower() == "gzip":
                raw = gzip.decompress(raw)
            return raw.decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} von {url}")


def main():
    ok = 0
    try:
        update_incidents_and_advisories()
        ok += 1
    except Exception as e:
        print(f"  Vorfälle/Schwachstellen konnten nicht aktualisiert werden: {e}")
        print("  -> Der bestehende data.js-Schnappschuss bleibt erhalten.")
    try:
        update_ransomware()
        ok += 1
    except Exception as e:
        print(f"  Ransomware-Daten konnten nicht aktualisiert werden: {e}")
        print("  -> Der bestehende data_ransomware.js-Schnappschuss bleibt erhalten.")
    try:
        update_kev()
        ok += 1
    except Exception as e:
        print(f"  KEV-Daten konnten nicht aktualisiert werden: {e}")
        print("  -> Der bestehende data_kev.js-Schnappschuss bleibt erhalten.")
    if ok == 0:
        print("\nKeine Quelle war erreichbar. Das Dashboard zeigt weiter die mitgelieferten Daten.")
        print("Pruefe die Internetverbindung oder oeffne die Quell-Links aus dem Dashboard im Browser.")
    else:
        print(f"\n{ok}/3 Quellen aktualisiert. index.html im Browser neu laden (F5).")


def update_incidents_and_advisories():
    print("Lade Sicherheitsvorfälle …")
    raw = get_json(INC_URL, referer="https://www.security-incidents.de/sicherheitsvorfall-datenbank/")
    allinc = raw if isinstance(raw, list) else raw.get("rows") or raw.get("data") or []
    de = [x for x in allinc if x.get("country") == COUNTRY]
    de.sort(key=lambda x: x.get("orgPublishDate") or "", reverse=True)

    month, tags, types, countries = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    for x in allinc:
        countries[x.get("country") or "NN"] += 1
    for x in de:
        d = (x.get("orgPublishDate") or "")[:7]
        if d >= "2019":
            month[d] += 1
        for t in (x.get("tags") or "").split(","):
            if t.strip():
                tags[t.strip()] += 1
        t = x.get("affectedType") or ""
        types[t if t in ("Unternehmen", "Organisation") else "Sonstige"] += 1

    # Einzelpersonen werden aus Datenschutzgründen nicht namentlich übernommen
    rows = [[x.get("incidentID"), x.get("orgPublishDate"), x.get("affectedObj"), x.get("affectedType"),
             (x.get("incidentText") or "").strip(), x.get("tags") or "", x.get("href") or ""]
            for x in de if (x.get("affectedType") or "") not in ("Person", "Personen")]

    print(f"  {len(allinc)} Vorfälle gesamt, {len(de)} in {COUNTRY}")

    print("Lade CERT-Bund Kurzinformationen …")
    adv = get_json(ADV_URL, referer="https://wid.cert-bund.de/portal/wid/kurzinformationen")
    content = adv.get("content", [])
    cls, perday = collections.Counter(), collections.Counter()
    for a in content:
        cls[a.get("classification") or "?"] += 1
        perday[(a.get("published") or "")[:10]] += 1
    first = content[-1]["published"][:10] if content else ""
    last = content[0]["published"][:10] if content else ""
    fmt = lambda s: f"{s[8:10]}.{s[5:7]}." if s else ""
    advrows = [[a.get("name"), (a.get("published") or "")[:16], a.get("classification"), a.get("basescore"),
                a.get("title"), " ".join((a.get("cves") or [])[:3]), a.get("status")] for a in content[:ADV_KEEP]]
    print(f"  {len(content)} Meldungen geladen ({first} bis {last}), {adv.get('totalElements')} insgesamt")

    data = {
        "generated": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "snapshot": False,
        "history": {
            "totalWorld": len(allinc), "totalDE": len(de),
            "monthDE": dict(sorted(month.items())),
            "tagsDE": dict(tags.most_common(18)),
            "typesDE": dict(types),
            "countries": dict(countries.most_common(12)),
        },
        "incidents": rows,
        "advisoryStats": {
            "total": adv.get("totalElements"),
            "window": f"{fmt(first)}–{fmt(last)}{last[:4]}",
            "count": len(content), "cls": dict(cls), "perDay": dict(sorted(perday.items())),
        },
        "advisories": advrows,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("/* Automatisch erzeugt von update_data.py */\nwindow.SECDASH = ")
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    print(f"Fertig: {OUT}")


def parse_ransomware_html(html):
    """Zerlegt die ransomware.live-Länderseite in Opfer-Einträge.
    Jede Opferkarte beginnt mit class="victim-title; dadurch ist jeder Block eindeutig begrenzt."""
    import re
    victims = []
    parts = html.split('class="victim-title')
    for chunk in parts[1:]:
        c = chunk[:1600]
        m_name = re.search(r'^[^>]*>\s*([^<]+?)\s*</a>', c)
        m_grp = re.search(r'/group/([^"#/?]+)', c)
        m_disc = re.search(r'Discovered:</strong>\s*(\d{4}-\d{2}-\d{2})', c)
        m_att = re.search(r'Attack est\.:</strong>\s*(\d{4}-\d{2}-\d{2})', c)
        if not (m_name and m_grp and m_disc):
            continue
        victims.append({
            "victim": m_name.group(1).strip(),
            "group": m_grp.group(1).lower(),
            "discovered": m_disc.group(1),
            "attackdate": m_att.group(1) if m_att else None,
        })
    return victims


def read_rl_token():
    """API-Token aus Umgebungsvariable RANSOMWARE_LIVE_TOKEN oder Datei ransomware_token.txt.
    Der Token ist ein Geheimnis und wird NICHT ins Repository eingecheckt (.gitignore)."""
    tok = os.environ.get("RANSOMWARE_LIVE_TOKEN", "").strip()
    if tok:
        return tok
    f = os.path.join(HERE, "ransomware_token.txt")
    if os.path.exists(f):
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    return line
    return ""


def fetch_ransomware_api(token):
    """Offizielle PRO-API (schnell & zuverlässig). Liefert normalisierte Opfer-Dicts."""
    j = get_json(RL_API, referer="https://www.ransomware.live/", extra_headers={"X-Api-Key": token})
    vs = j.get("victims") or []
    out = []
    for v in vs:
        out.append({
            "victim": v.get("victim") or v.get("post_title") or "?",
            "group": (v.get("group") or "").lower(),
            "discovered": (v.get("discovered") or "")[:10],
            "attackdate": (v.get("attackdate") or "")[:10] or None,
        })
    return out


def update_ransomware():
    """Aktualisiert data_ransomware.js (Opferzahlen & Monatsverlauf).
    Nutzt die offizielle PRO-API, wenn ein Token vorliegt, sonst die HTML-Länderseite.
    Die Gruppenprofile (data_actors.js) bleiben unberührt – von Hand gepflegt."""
    token = read_rl_token()
    victims = None
    if token:
        print("Lade Ransomware-Opfer (ransomware.live PRO-API) …")
        try:
            victims = fetch_ransomware_api(token)
        except Exception as e:
            print(f"  PRO-API fehlgeschlagen ({e}) – versuche HTML-Seite …")
    if not victims:
        print("Lade Ransomware-Opfer (ransomware.live, HTML) …")
        victims = parse_ransomware_html(get_text(RL_HTML, referer="https://www.ransomware.live/"))
    if len(victims) < 50:
        raise RuntimeError(f"nur {len(victims)} Opfer erkannt – Quelle/Format evtl. geändert")

    def gkey(v):  # Datum: attackdate bevorzugt, sonst discovered
        return (v.get("attackdate") or v.get("discovered") or "")[:10]

    by_month, groups = collections.Counter(), {}
    rows = []
    cut12 = (datetime.date.today() - datetime.timedelta(days=365)).isoformat()
    for v in victims:
        g = (v.get("group") or "").lower()
        d = gkey(v)
        name = v.get("victim") or "?"
        if d:
            by_month[d[:7]] += 1
        gr = groups.setdefault(g, {"de": 0, "de12": 0, "months": collections.Counter(), "latest": []})
        gr["de"] += 1
        if d >= cut12:
            gr["de12"] += 1
        if d:
            gr["months"][d[:7]] += 1
        gr["latest"].append([name, d])
        rows.append([name[:60], g, d])

    rows.sort(key=lambda r: r[2], reverse=True)
    for g, gr in groups.items():
        gr["latest"].sort(key=lambda x: x[1], reverse=True)
        gr["latest"] = gr["latest"][:6]
        gr["months"] = dict(sorted(gr["months"].items()))
    # nur Gruppen mit nennenswerter DE-Aktivität behalten
    groups = {g: v for g, v in sorted(groups.items(), key=lambda kv: kv[1]["de"], reverse=True) if g}

    out = {
        "generated": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "snapshot": False,
        "totalDE": len(victims),
        "byMonth": dict(sorted(by_month.items())),
        "groups": groups,
        "victims": rows[:120],
    }
    with open(OUT_RL, "w", encoding="utf-8") as f:
        f.write("/* Automatisch erzeugt von update_data.py – Quelle: ransomware.live */\nwindow.RANSOM = ")
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    print(f"  {len(victims)} DE-Opfer, {len(groups)} Gruppen. Fertig: {OUT_RL}")


def update_kev():
    """Aktualisiert data_kev.js aus dem CISA-KEV-Katalog. Behält alle von Ransomware
    genutzten Lücken plus die 50 neuesten Einträge."""
    print("Lade CISA KEV (aktiv ausgenutzte Lücken) …")
    data = get_json(KEV_URL, referer="https://www.cisa.gov/known-exploited-vulnerabilities-catalog")
    vulns = data.get("vulnerabilities") or []
    if not vulns:
        raise RuntimeError("leere/ungültige Antwort von CISA KEV")

    clean = lambda s: " ".join((s or "").split())
    is_r = lambda x: x.get("knownRansomwareCampaignUse") == "Known"
    ransom = sorted([x for x in vulns if is_r(x)], key=lambda x: x.get("dateAdded", ""), reverse=True)
    recent = sorted(vulns, key=lambda x: x.get("dateAdded", ""), reverse=True)[:50]

    seen, rows = set(), []
    for x in ransom + recent:
        cve = x.get("cveID")
        if cve in seen:
            continue
        seen.add(cve)
        rows.append([cve, x.get("dateAdded"), x.get("vendorProject"), x.get("product"),
                     clean(x.get("vulnerabilityName"))[:90], clean(x.get("shortDescription"))[:150],
                     1 if is_r(x) else 0, x.get("dueDate") or ""])

    by_vendor_r, by_year, ransom_year = collections.Counter(), collections.Counter(), collections.Counter()
    for x in ransom:
        by_vendor_r[x.get("vendorProject")] += 1
        ransom_year[(x.get("dateAdded") or "")[:4]] += 1
    for x in vulns:
        by_year[(x.get("dateAdded") or "")[:4]] += 1

    out = {
        "generated": data.get("dateReleased"),
        "version": data.get("catalogVersion"),
        "total": len(vulns),
        "ransomTotal": len(ransom),
        "topVendorsR": by_vendor_r.most_common(10),
        "byYear": dict(sorted(by_year.items())),
        "ransomByYear": dict(sorted(ransom_year.items())),
        "rows": rows,
    }
    with open(OUT_KEV, "w", encoding="utf-8") as f:
        f.write("/* Automatisch erzeugt von update_data.py – Quelle: CISA KEV */\nwindow.KEV = ")
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    print(f"  {len(vulns)} KEV-Einträge, {len(ransom)} von Ransomware genutzt. Fertig: {OUT_KEV}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Fehler beim Aktualisieren:", e)
        sys.exit(1)
