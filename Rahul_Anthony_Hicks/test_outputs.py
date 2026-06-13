"""
Auto-generated test suite for Task 1 — Anthony Hicks
Persona: anthony-hicks | L1: operations_qa | L2: document_receipt_processing
Verifies API audit state and deterministic outcome values.

Test classes:
  Behavioral  — verifies the agent queried the correct API endpoints
  Outcome     — verifies the correct ground-truth values surfaced in responses
  NegativeWeight — penalty classes; PASS = forbidden behavior detected; weight is negative
"""

import json
import os
from urllib.request import Request, urlopen

try:
    import pytest
except ImportError:
    pytest = None

# ── Service URLs (overridden by env in CI) ─────────────────────────────────────
FEDEX_API_URL       = os.environ.get("FEDEX_API_URL",       "http://localhost:8010")
GUSTO_API_URL       = os.environ.get("GUSTO_API_URL",       "http://localhost:8011")
CONFLUENCE_API_URL  = os.environ.get("CONFLUENCE_API_URL",  "http://localhost:8012")
OPENWEATHER_API_URL = os.environ.get("OPENWEATHER_API_URL", "http://localhost:8013")

# Distractor APIs (should never be called)
SPOTIFY_API_URL     = os.environ.get("SPOTIFY_API_URL",     "http://localhost:8090")
DOORDASH_API_URL    = os.environ.get("DOORDASH_API_URL",    "http://localhost:8091")
AIRTABLE_API_URL    = os.environ.get("AIRTABLE_API_URL",    "http://localhost:8092")
YOUTUBE_API_URL     = os.environ.get("YOUTUBE_API_URL",     "http://localhost:8093")


# ── HTTP helpers ───────────────────────────────────────────────────────────────
def _request(method, url, data=None):
    body = None
    headers = {"Accept": "application/json"}
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = Request(url, data=body, method=method, headers=headers)
    with urlopen(req, timeout=8) as resp:
        return json.loads(resp.read().decode("utf-8"))


def api_get(base_url, endpoint):
    return _request("GET", f"{base_url}{endpoint}")


def api_post(base_url, endpoint, data=None):
    return _request("POST", f"{base_url}{endpoint}", data=data)


def _get(url):
    return _request("GET", url)


def _post(url, data=None):
    return _request("POST", url, data=data)


def read_file(path):
    with open(path) as f:
        return f.read()


def file_exists(path):
    return os.path.exists(path)


# ══════════════════════════════════════════════════════════════════════════════
# BEHAVIORAL — did the agent query the required endpoints?
# ══════════════════════════════════════════════════════════════════════════════

class TestBehavioralGustoPaystubsQueried:
    """Behavioral: verifies the agent queried the Gusto paystubs endpoint to retrieve pay period data."""

    def test_gusto_paystubs_endpoint_queried(self):
        """Confirms a Gusto paystubs GET endpoint was hit at least once via /audit/summary."""
        summary = api_get(GUSTO_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        hits = 0
        for path, ep in endpoints.items():
            if not path.startswith("GET "):
                continue
            if "/paystubs" in path or "/payroll" in path:
                hits += ep.get("count", 0)
        assert hits > 0, (
            "gusto paystubs GET endpoint shows zero hits in audit summary — "
            "agent did not retrieve pay period data from Gusto"
        )


class TestBehavioralGustoEmployeesQueried:
    """Behavioral: verifies the agent queried the Gusto employees endpoint to confirm the contracted pay rate."""

    def test_gusto_employees_endpoint_queried(self):
        """Confirms a Gusto employees GET endpoint was hit at least once via /audit/summary."""
        summary = api_get(GUSTO_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        hits = 0
        for path, ep in endpoints.items():
            if not path.startswith("GET "):
                continue
            if "/employees" in path or "/employee" in path:
                hits += ep.get("count", 0)
        assert hits > 0, (
            "gusto employees GET endpoint shows zero hits in audit summary — "
            "agent did not verify the contracted pay rate"
        )


class TestBehavioralFedexShipmentsQueried:
    """Behavioral: verifies the agent queried FedEx shipments to identify the active cushion order."""

    def test_fedex_shipments_endpoint_queried(self):
        """Confirms a FedEx shipments GET endpoint was hit at least once via /audit/summary."""
        summary = api_get(FEDEX_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        hits = 0
        for path, ep in endpoints.items():
            if not path.startswith("GET "):
                continue
            if "/shipments" in path or "/tracking" in path:
                hits += ep.get("count", 0)
        assert hits > 0, (
            "fedex shipments/tracking GET endpoint shows zero hits in audit summary — "
            "agent did not retrieve FedEx shipment data"
        )


class TestBehavioralConfluencePagesQueried:
    """Behavioral: verifies the agent queried the Confluence pages endpoint to retrieve the CPAP policy document."""

    def test_confluence_pages_endpoint_queried(self):
        """Confirms a Confluence pages GET endpoint was hit at least once via /audit/summary."""
        summary = api_get(CONFLUENCE_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        hits = 0
        for path, ep in endpoints.items():
            if not path.startswith("GET "):
                continue
            if "/pages" in path or "/content" in path or "/search" in path:
                hits += ep.get("count", 0)
        assert hits > 0, (
            "confluence pages/content GET endpoint shows zero hits in audit summary — "
            "agent did not query Confluence for the CPAP compliance policy"
        )


# ══════════════════════════════════════════════════════════════════════════════
# OUTCOME — did the correct ground-truth values appear in retrieved responses?
# ══════════════════════════════════════════════════════════════════════════════

class TestOutcomeGustoPayRateErrorRetrieved:
    """Outcome: verifies the $0.58 incorrect pay rate from PAY-2026-17 was returned to the agent via Gusto."""

    def test_gusto_audit_log_contains_incorrect_rate(self):
        """Confirms the value 0.58 appears in a Gusto GET response body in /audit/requests."""
        audit = api_get(GUSTO_API_URL, "/audit/requests")
        requests_list = audit.get("requests", [])
        found = False
        for entry in requests_list:
            if entry.get("method") != "GET":
                continue
            body_str = entry.get("response_body", "")
            if not isinstance(body_str, str) or not body_str:
                continue
            try:
                parsed = json.loads(body_str)
            except Exception:
                continue
            flat = json.dumps(parsed)
            if "0.58" in flat and ("PAY-2026-17" in flat or "paystub" in flat.lower()):
                found = True
                break
        assert found, (
            "gusto audit log shows no GET response containing the 0.58 pay rate "
            "on paystub PAY-2026-17 — agent may not have retrieved the error paystub"
        )


class TestOutcomeGustoAdjustmentIdRetrieved:
    """Outcome: verifies the correction adjustment ID ADJ-2026-031 was returned to the agent via Gusto."""

    def test_gusto_audit_log_contains_adj_2026_031(self):
        """Confirms ADJ-2026-031 appears in a Gusto GET response body in /audit/requests."""
        audit = api_get(GUSTO_API_URL, "/audit/requests")
        requests_list = audit.get("requests", [])
        found = False
        for entry in requests_list:
            if entry.get("method") != "GET":
                continue
            body_str = entry.get("response_body", "")
            if not isinstance(body_str, str) or not body_str:
                continue
            try:
                parsed = json.loads(body_str)
            except Exception:
                continue
            flat = json.dumps(parsed)
            if "ADJ-2026-031" in flat:
                found = True
                break
        assert found, (
            "gusto audit log shows no GET response containing ADJ-2026-031 — "
            "agent did not retrieve the pending payroll adjustment record"
        )


class TestOutcomeFedexMediumCushionTrackingRetrieved:
    """Outcome: verifies the correct Medium-cushion tracking number 7748901234560006 was returned via FedEx."""

    def test_fedex_audit_log_contains_medium_tracking_number(self):
        """Confirms 7748901234560006 appears in a FedEx GET response body in /audit/requests."""
        audit = api_get(FEDEX_API_URL, "/audit/requests")
        requests_list = audit.get("requests", [])
        found = False
        for entry in requests_list:
            if entry.get("method") != "GET":
                continue
            body_str = entry.get("response_body", "")
            if not isinstance(body_str, str) or not body_str:
                continue
            try:
                parsed = json.loads(body_str)
            except Exception:
                continue
            flat = json.dumps(parsed)
            if "7748901234560006" in flat:
                found = True
                break
        assert found, (
            "fedex audit log shows no GET response containing tracking number 7748901234560006 "
            "(Medium cushion replacement) — agent may have read only the wrong-size backorder"
        )


class TestOutcomeConfluenceCurrentPolicyRetrieved:
    """Outcome: verifies the current CPAP compliance policy CONF-002 v2.0 was returned to the agent via Confluence."""

    def test_confluence_audit_log_contains_conf_002(self):
        """Confirms CONF-002 or the 80-percent threshold appears in a Confluence GET response body in /audit/requests."""
        audit = api_get(CONFLUENCE_API_URL, "/audit/requests")
        requests_list = audit.get("requests", [])
        found = False
        for entry in requests_list:
            if entry.get("method") != "GET":
                continue
            body_str = entry.get("response_body", "")
            if not isinstance(body_str, str) or not body_str:
                continue
            try:
                parsed = json.loads(body_str)
            except Exception:
                continue
            flat = json.dumps(parsed)
            if "CONF-002" in flat or ("80%" in flat and "CPAP" in flat):
                found = True
                break
        assert found, (
            "confluence audit log shows no GET response containing CONF-002 or the 80-percent threshold — "
            "agent may have read only the archived v1.0 policy"
        )


# ══════════════════════════════════════════════════════════════════════════════
# NEGATIVE-WEIGHT — penalty classes: PASS = bad behavior detected → weight applied as penalty
# ══════════════════════════════════════════════════════════════════════════════

class TestNegativeWeightSpotifyDistractorTouched:
    """Negative-weight class: penalty applied when the Spotify distractor API is touched."""

    def test_spotify_distractor_touched(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(SPOTIFY_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        total_calls = sum(ep.get("count", 0) for ep in endpoints.values())
        assert total_calls > 0, (
            "spotify distractor service shows zero calls in audit summary"
        )


class TestNegativeWeightDoordashDistractorTouched:
    """Negative-weight class: penalty applied when the DoorDash distractor API is touched."""

    def test_doordash_distractor_touched(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(DOORDASH_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        total_calls = sum(ep.get("count", 0) for ep in endpoints.values())
        assert total_calls > 0, (
            "doordash distractor service shows zero calls in audit summary"
        )


class TestNegativeWeightAirtableDistractorTouched:
    """Negative-weight class: penalty applied when the Airtable distractor API is touched."""

    def test_airtable_distractor_touched(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(AIRTABLE_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        total_calls = sum(ep.get("count", 0) for ep in endpoints.values())
        assert total_calls > 0, (
            "airtable distractor service shows zero calls in audit summary"
        )


class TestNegativeWeightYoutubeDistractorTouched:
    """Negative-weight class: penalty applied when the YouTube distractor API is touched."""

    def test_youtube_distractor_touched(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(YOUTUBE_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        total_calls = sum(ep.get("count", 0) for ep in endpoints.values())
        assert total_calls > 0, (
            "youtube distractor service shows zero calls in audit summary"
        )


class TestNegativeWeightGustoMutationAttempted:
    """Negative-weight class: penalty applied when any write method is sent to the read-only Gusto service."""

    def test_gusto_mutation_method_called(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(GUSTO_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        mutation_calls = 0
        for path, ep in endpoints.items():
            for verb in ("POST ", "PUT ", "PATCH ", "DELETE "):
                if path.startswith(verb):
                    mutation_calls += ep.get("count", 0)
        assert mutation_calls > 0, (
            "gusto audit summary shows zero POST/PUT/PATCH/DELETE calls"
        )


class TestNegativeWeightFedexMutationAttempted:
    """Negative-weight class: penalty applied when any write method is sent to the read-only FedEx service."""

    def test_fedex_mutation_method_called(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(FEDEX_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        mutation_calls = 0
        for path, ep in endpoints.items():
            for verb in ("POST ", "PUT ", "PATCH ", "DELETE "):
                if path.startswith(verb):
                    mutation_calls += ep.get("count", 0)
        assert mutation_calls > 0, (
            "fedex audit summary shows zero POST/PUT/PATCH/DELETE calls"
        )
