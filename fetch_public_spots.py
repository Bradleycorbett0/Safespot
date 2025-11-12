#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fetch public "safe spots" for a UK city from OpenStreetMap (Overpass API)
and upload to Firebase Realtime Database.

Covers:
- Libraries, police, hospitals/clinics
- Parks and outdoor green spaces
- Tourist attractions, museums, galleries, viewpoints
- Transport hubs (bus, train, airport)
- 24-hour venues detected via opening_hours=24/7

Usage:
  python3 fetch_public_spots.py "Liverpool"
  python3 fetch_public_spots.py "Manchester" --patch
"""

import argparse
import hashlib
import json
import time
import urllib.parse
from typing import Dict, Any, List, Tuple
import requests

# ---------------- CONFIG ----------------

# ✅ Your Firebase endpoint (with correct region)
FIREBASE_URL = "https://safespot-c5e02-default-rtdb.europe-west1.firebasedatabase.app"

# Optional: Firebase secret or ID token (if required by your database rules)
FIREBASE_AUTH = None  # e.g., "YOUR_FIREBASE_AUTH_TOKEN"

# Database node
ROOT_COLLECTION = "public_spots"

# Overpass API endpoint
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Connection settings
HTTP_TIMEOUT = 45
RETRY_COUNT = 3
RETRY_BACKOFF = 3.0  # seconds
# ----------------------------------------


# 🏷️ Categories and tag filters
OSM_FILTERS = [
    ('library', 'amenity=library'),
    ('police', 'amenity=police'),
    ('hospital', 'amenity=hospital'),
    ('clinic', 'amenity=clinic'),
    ('doctors', 'amenity=doctors'),
    ('pharmacy', 'amenity=pharmacy'),
    ('park', 'leisure=park'),
    ('garden', 'leisure=garden'),
    ('greenspace', 'landuse=meadow'),
    ('train_station', 'railway=station'),
    ('bus_station', 'amenity=bus_station'),
    ('airport', 'aeroway=aerodrome'),
    ('tourist_attraction', 'tourism=attraction'),
    ('museum', 'tourism=museum'),
    ('gallery', 'tourism=gallery'),
    ('viewpoint', 'tourism=viewpoint'),
    ('theme_park', 'tourism=theme_park'),
    ('zoo', 'tourism=zoo'),
]


def overpass_area_query(city: str, country: str = "United Kingdom") -> str:
    """Build Overpass QL query for a specific UK city."""
    parts = []
    for _, kv in OSM_FILTERS:
        k, v = kv.split("=")
        parts.append(f'  node["{k}"="{v}"](area.searchArea);')
        parts.append(f'  way["{k}"="{v}"](area.searchArea);')
        parts.append(f'  relation["{k}"="{v}"](area.searchArea);')

    body = "\n".join(parts)

    return f"""
[out:json][timeout:90];
area["name"="{country}"]["boundary"="administrative"]["admin_level"="2"]->.uk;
area(uk)["name"="{city}"]["boundary"="administrative"]->.searchArea;
(
{body}
);
out body center;
"""


def http_post(url: str, data: str) -> requests.Response:
    """Safe POST with retries."""
    for attempt in range(1, RETRY_COUNT + 1):
        try:
            resp = requests.post(url, data=data.encode("utf-8"),
                                 headers={"Content-Type": "application/x-www-form-urlencoded"},
                                 timeout=HTTP_TIMEOUT)
            if resp.status_code in (429, 500, 502, 503):
                time.sleep(RETRY_BACKOFF * attempt)
                continue
            return resp
        except requests.RequestException:
            time.sleep(RETRY_BACKOFF * attempt)
    raise RuntimeError(f"Failed to contact Overpass after {RETRY_COUNT} attempts.")


def normalize_text(s: str) -> str:
    return " ".join(s.strip().split()) if s else ""


def slugify(s: str) -> str:
    s = normalize_text(s).lower()
    out = []
    for ch in s:
        if ch.isalnum():
            out.append(ch)
        elif ch in [' ', '-', '_', '/', '&']:
            out.append('_')
    slug = "".join(out).strip("_")
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug or "spot"


def is_open_24h(tags: Dict[str, str], fallback_type: str) -> bool:
    oh = (tags.get("opening_hours") or "").strip().lower()
    if oh in ("24/7", "24-7", "24h"):
        return True
    if fallback_type in {"airport", "train_station"}:
        return True
    return False


def map_category(tags: Dict[str, str]) -> Tuple[str, str]:
    """Return (type, category) from tags."""
    for label, kv in OSM_FILTERS:
        k, v = kv.split("=")
        if tags.get(k) == v:
            if label in {"library"}:
                return (label, "education")
            if label in {"police"}:
                return (label, "public_service")
            if label in {"hospital", "clinic", "doctors", "pharmacy"}:
                return (label, "health")
            if label in {"park", "garden", "greenspace"}:
                return (label, "outdoor")
            if label in {"train_station", "bus_station", "airport"}:
                return (label, "transport")
            if label in {"tourist_attraction", "museum", "gallery", "viewpoint", "theme_park", "zoo"}:
                return (label, "tourist")
    return ("poi", "general")


def extract_address(tags: Dict[str, str]) -> str:
    parts = []
    for key in ["addr:housename", "addr:housenumber", "addr:street", "addr:suburb", "addr:city", "addr:postcode"]:
        if tags.get(key):
            parts.append(tags[key])
    return normalize_text(", ".join(parts))


def fetch_osm_data(city: str) -> List[Dict[str, Any]]:
    """Fetch & parse OSM Overpass data for the given city."""
    query = overpass_area_query(city)
    resp = http_post(OVERPASS_URL, data=f"data={urllib.parse.quote(query)}")

    if resp.status_code != 200:
        raise RuntimeError(f"Overpass returned {resp.status_code}: {resp.text[:200]}")

    elements = resp.json().get("elements", [])
    results = []

    for el in elements:
        tags = el.get("tags", {}) or {}
        name = tags.get("name") or tags.get("official_name") or ""
        if not name:
            continue

        lat = el.get("lat") or (el.get("center", {}).get("lat"))
        lon = el.get("lon") or (el.get("center", {}).get("lon"))
        if lat is None or lon is None:
            continue

        spot_type, category = map_category(tags)
        address = extract_address(tags)
        phone = tags.get("phone") or tags.get("contact:phone")
        website = tags.get("website") or tags.get("contact:website")
        email = tags.get("email") or tags.get("contact:email")

        result = {
            "name": normalize_text(name),
            "type": spot_type,
            "category": category,
            "address": address or None,
            "lat": float(lat),
            "lon": float(lon),
            "open_24h": is_open_24h(tags, spot_type),
            "tag": "public"
        }
        if phone: result["contact"] = phone
        if website: result["website"] = website
        if email: result["email"] = email

        results.append(result)

    # Deduplicate
    seen = set()
    final = []
    for r in results:
        key = f"{slugify(r['name'])}_{round(r['lat'], 4)}_{round(r['lon'], 4)}"
        if key not in seen:
            seen.add(key)
            final.append(r)
    return final


def firebase_key(rec: Dict[str, Any]) -> str:
    base = f"{rec['name']}|{rec['type']}|{rec['lat']}|{rec['lon']}"
    return slugify(rec["name"]) + "_" + hashlib.sha1(base.encode()).hexdigest()[:8]


def upload_to_firebase(city: str, spots: List[Dict[str, Any]], method: str = "PUT"):
    """Upload a batch of spots to Firebase under /public_spots/<city>/"""
    city_node = f"{ROOT_COLLECTION}/{city}"
    url = f"{FIREBASE_URL}/{city_node}.json"
    if FIREBASE_AUTH:
        url += f"?auth={FIREBASE_AUTH}"

    payload = {firebase_key(s): s for s in spots}
    print(f"Uploading {len(payload)} records to Firebase...")

    if method.upper() == "PATCH":
        resp = requests.patch(url, json=payload, timeout=HTTP_TIMEOUT)
    else:
        resp = requests.put(url, json=payload, timeout=HTTP_TIMEOUT)

    if resp.status_code not in (200, 204):
        print(f"Firebase upload failed: {resp.status_code} - {resp.text[:200]}")
    else:
        print(f"✅ Upload complete for {city} ({len(payload)} records)")


def main():
    parser = argparse.ArgumentParser(description="Fetch & upload UK public safe spots.")
    parser.add_argument("city", help="City name (e.g. Liverpool)")
    parser.add_argument("--patch", action="store_true", help="Append to existing data instead of overwrite.")
    args = parser.parse_args()

    city = args.city.strip()
    print(f"Fetching safe spots for: {city} 🇬🇧")
    spots = fetch_osm_data(city)
    print(f"Found {len(spots)} safe spots.")

    method = "PATCH" if args.patch else "PUT"
    upload_to_firebase(city, spots, method)


if __name__ == "__main__":
    main()