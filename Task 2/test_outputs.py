"""
Auto-generated test suite for Task 2 — Aaron Whitmore
Persona: aaron-whitmore | L1: operations_qa | L2: document_receipt_processing
Verifies API audit state and deterministic outcome values for the hydraulic cylinder order reconciliation task.

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
OPENWEATHER_API_URL = os.environ.get("OPENWEATHER_API_URL", "http://localhost:8001")
UPS_API_URL         = os.environ.get("UPS_API_URL",         "http://localhost:8002")
SHIPPO_API_URL      = os.environ.get("SHIPPO_API_URL",      "http://localhost:8003")
QUICKBOOKS_API_URL  = os.environ.get("QUICKBOOKS_API_URL",  "http://localhost:8004")

# Distractor APIs (should never be called)
FEDEX_API_URL       = os.environ.get("FEDEX_API_URL",       "http://localhost:8090")
ZILLOW_API_URL      = os.environ.get("ZILLOW_API_URL",      "http://localhost:8091")
SPOTIFY_API_URL     = os.environ.get("SPOTIFY_API_URL",     "http://localhost:8092")
DOORDASH_API_URL    = os.environ.get("DOORDASH_API_URL",    "http://localhost:8093")


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

class TestBehavioralUPSTrackingQueried:
    """Behavioral: verifies the agent queried the UPS tracking endpoint to retrieve shipment status."""

    def test_ups_tracking_endpoint_queried(self):
        """Confirms a UPS tracking or shipments GET endpoint was hit at least once via /audit/summary."""
        summary = api_get(UPS_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        hits = 0
        for path, ep in endpoints.items():
            if not path.startswith("GET "):
                continue
            if "/tracking" in path or "/shipments" in path or "/track" in path:
                hits += ep.get("count", 0)
        assert hits > 0, (
            "ups tracking/shipments GET endpoint shows zero hits in audit summary — "
            "agent did not retrieve UPS tracking data for the hydraulic cylinder order"
        )


class TestBehavioralQuickBillsQueried:
    """Behavioral: verifies the agent queried the QuickBooks bills/payables endpoint to confirm invoice status."""

    def test_quickbooks_bills_endpoint_queried(self):
        """Confirms a QuickBooks bills or payables GET endpoint was hit at least once via /audit/summary."""
        summary = api_get(QUICKBOOKS_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        hits = 0
        for path, ep in endpoints.items():
            if not path.startswith("GET "):
                continue
            if "/bills" in path or "/payables" in path or "/invoices" in path or "/vendors" in path:
                hits += ep.get("count", 0)
        assert hits > 0, (
            "quickbooks bills/payables GET endpoint shows zero hits in audit summary — "
            "agent did not verify invoice payment status from QuickBooks"
        )


class TestBehavioralShippoLabelQueried:
    """Behavioral: verifies the agent queried the Shippo label endpoint to verify shipping address and part number."""

    def test_shippo_label_endpoint_queried(self):
        """Confirms a Shippo labels or rates GET endpoint was hit at least once via /audit/summary."""
        summary = api_get(SHIPPO_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        hits = 0
        for path, ep in endpoints.items():
            if not path.startswith("GET "):
                continue
            if "/labels" in path or "/shipments" in path or "/rates" in path or "/transactions" in path:
                hits += ep.get("count", 0)
        assert hits > 0, (
            "shippo labels/shipments GET endpoint shows zero hits in audit summary — "
            "agent did not retrieve Shippo label data to verify shipping address"
        )


class TestBehavioralOpenWeatherQueried:
    """Behavioral: verifies the agent queried OpenWeather for Briscoe TX conditions per AGENTS.md Priority 2."""

    def test_openweather_weather_endpoint_queried(self):
        """Confirms an OpenWeather current weather or forecast GET endpoint was hit via /audit/summary."""
        summary = api_get(OPENWEATHER_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        hits = 0
        for path, ep in endpoints.items():
            if not path.startswith("GET "):
                continue
            if "/weather" in path or "/forecast" in path or "/onecall" in path:
                hits += ep.get("count", 0)
        assert hits > 0, (
            "openweather weather/forecast GET endpoint shows zero hits in audit summary — "
            "agent did not check Briscoe TX weather per AGENTS.md Priority 2 session directive"
        )


# ══════════════════════════════════════════════════════════════════════════════
# OUTCOME — did the correct ground-truth values appear in retrieved responses?
# ══════════════════════════════════════════════════════════════════════════════

class TestOutcomeUPSTrackingNumberRetrieved:
    """Outcome: verifies the correct UPS tracking number 1Z7R48960391438256 was returned to the agent."""

    def test_ups_audit_log_contains_tracking_number(self):
        """Confirms 1Z7R48960391438256 appears in a UPS GET response body in /audit/requests."""
        audit = api_get(UPS_API_URL, "/audit/requests")
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
            if "1Z7R48960391438256" in flat:
                found = True
                break
        assert found, (
            "ups audit log shows no GET response containing tracking number 1Z7R48960391438256 — "
            "agent may not have retrieved the active hydraulic cylinder shipment record"
        )


class TestOutcomeQuickBooksInvoiceRetrieved:
    """Outcome: verifies the invoice number INV-2026-0891 was returned to the agent via QuickBooks."""

    def test_quickbooks_audit_log_contains_invoice_number(self):
        """Confirms INV-2026-0891 appears in a QuickBooks GET response body in /audit/requests."""
        audit = api_get(QUICKBOOKS_API_URL, "/audit/requests")
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
            if "INV-2026-0891" in flat:
                found = True
                break
        assert found, (
            "quickbooks audit log shows no GET response containing INV-2026-0891 — "
            "agent did not retrieve the Amarillo Tractor payable invoice record"
        )


class TestOutcomeQuickBooksCorrectTotalRetrieved:
    """Outcome: verifies the correct invoice total $312.47 was returned to the agent via QuickBooks."""

    def test_quickbooks_audit_log_contains_correct_total(self):
        """Confirms 312.47 appears in a QuickBooks GET response body in /audit/requests."""
        audit = api_get(QUICKBOOKS_API_URL, "/audit/requests")
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
            if "312.47" in flat and "INV-2026-0891" in flat:
                found = True
                break
        assert found, (
            "quickbooks audit log shows no GET response containing 312.47 on INV-2026-0891 — "
            "agent may not have retrieved the correct invoice total for the hydraulic cylinder order"
        )


class TestOutcomeShippoAddressRetrieved:
    """Outcome: verifies Shippo returned the delivery address 7820 County Road 28 Briscoe TX 79011."""

    def test_shippo_audit_log_contains_delivery_address(self):
        """Confirms 'Briscoe' or '79011' or '7820' appears in a Shippo GET response body in /audit/requests."""
        audit = api_get(SHIPPO_API_URL, "/audit/requests")
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
            if ("Briscoe" in flat or "79011" in flat) and "7820" in flat:
                found = True
                break
        assert found, (
            "shippo audit log shows no GET response containing the Briscoe TX delivery address — "
            "agent did not verify the shipping address matches Aaron's property address"
        )


class TestOutcomeOpenWeatherPressureRetrieved:
    """Outcome: verifies OpenWeather returned a barometric pressure value for Briscoe TX to the agent."""

    def test_openweather_audit_log_contains_pressure(self):
        """Confirms a pressure reading (inhg or hpa) appears in an OpenWeather GET response body in /audit/requests."""
        audit = api_get(OPENWEATHER_API_URL, "/audit/requests")
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
            if ("pressure" in flat.lower() or "inhg" in flat.lower()) and ("Briscoe" in flat or "5521842" in flat):
                found = True
                break
        assert found, (
            "openweather audit log shows no GET response containing a pressure reading for Briscoe TX — "
            "agent may not have checked the barometric pressure for migraine-risk assessment"
        )


# ══════════════════════════════════════════════════════════════════════════════
# NEGATIVE-WEIGHT — penalty classes: PASS = bad behavior detected → weight applied as penalty
# ══════════════════════════════════════════════════════════════════════════════

class TestNegativeWeightFedexDistractorTouched:
    """Negative-weight class: penalty applied when the FedEx distractor API is touched."""

    def test_fedex_distractor_touched(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(FEDEX_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        total_calls = sum(ep.get("count", 0) for ep in endpoints.values())
        assert total_calls > 0, (
            "fedex distractor service shows zero calls in audit summary"
        )


class TestNegativeWeightZillowDistractorTouched:
    """Negative-weight class: penalty applied when the Zillow distractor API is touched."""

    def test_zillow_distractor_touched(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(ZILLOW_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        total_calls = sum(ep.get("count", 0) for ep in endpoints.values())
        assert total_calls > 0, (
            "zillow distractor service shows zero calls in audit summary"
        )


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


class TestNegativeWeightUPSMutationAttempted:
    """Negative-weight class: penalty applied when any write method is sent to the read-only UPS service."""

    def test_ups_mutation_method_called(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(UPS_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        mutation_calls = 0
        for path, ep in endpoints.items():
            for verb in ("POST ", "PUT ", "PATCH ", "DELETE "):
                if path.startswith(verb):
                    mutation_calls += ep.get("count", 0)
        assert mutation_calls > 0, (
            "ups audit summary shows zero POST/PUT/PATCH/DELETE calls"
        )


class TestNegativeWeightQuickBooksMutationAttempted:
    """Negative-weight class: penalty applied when any write method is sent to the read-only QuickBooks service."""

    def test_quickbooks_mutation_method_called(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(QUICKBOOKS_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        mutation_calls = 0
        for path, ep in endpoints.items():
            for verb in ("POST ", "PUT ", "PATCH ", "DELETE "):
                if path.startswith(verb):
                    mutation_calls += ep.get("count", 0)
        assert mutation_calls > 0, (
            "quickbooks audit summary shows zero POST/PUT/PATCH/DELETE calls"
        )
