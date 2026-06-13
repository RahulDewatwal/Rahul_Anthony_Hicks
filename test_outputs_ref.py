"""
Auto-generated test suite for verifying API state changes and task completion.
"""

import json
import os
import subprocess
import sqlite3
from urllib.request import Request, urlopen

try:
    import pytest
except ImportError:
    pytest = None

ETSY_API_URL = os.environ.get("ETSY_API_URL", "http://localhost:8001")
AMAZON_SELLER_API_URL = os.environ.get("AMAZON_SELLER_API_URL", "http://localhost:8000")
BIGCOMMERCE_API_URL = os.environ.get("BIGCOMMERCE_API_URL", "http://localhost:8084")
WOOCOMMERCE_API_URL = os.environ.get("WOOCOMMERCE_API_URL", "http://localhost:8085")
INSTACART_API_URL = os.environ.get("INSTACART_API_URL", "http://localhost:8012")
DOORDASH_API_URL = os.environ.get("DOORDASH_API_URL", "http://localhost:8037")


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


class TestBehavioralEtsyQueried:
    """Behavioral: verifies the agent queried the etsy listings catalog for vintage Western boot comparables."""

    def test_etsy_listings_endpoint_queried(self):
        """Confirms the etsy listings or single-listing GET endpoint was hit at least once via /audit/summary."""
        summary = api_get(ETSY_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        listing_hits = 0
        for path, ep in endpoints.items():
            if not path.startswith("GET "):
                continue
            if "/listings" in path:
                listing_hits += ep.get("count", 0)
        assert listing_hits > 0, "etsy listings GET endpoints show zero hits in audit summary"


class TestBehavioralAmazonSellerQueried:
    """Behavioral: verifies the agent queried amazon-seller catalog for the reissue cross-confirmation."""

    def test_amazon_seller_catalog_items_endpoint_queried(self):
        """Confirms an amazon-seller catalog or listings GET endpoint was hit via /audit/summary."""
        summary = api_get(AMAZON_SELLER_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        catalog_hits = 0
        for path, ep in endpoints.items():
            if not path.startswith("GET "):
                continue
            if "/catalog/" in path or "/listings/" in path:
                catalog_hits += ep.get("count", 0)
        assert catalog_hits > 0, "amazon-seller catalog/listings GET endpoints show zero hits in audit summary"


class TestOutcomeEtsyAuthenticitySoleCodeRetrieved:
    """Outcome: verifies the L-704 sole-code marker on the authentic Tony Lama 1970s listing was returned to the agent."""

    def test_etsy_audit_log_contains_l_704_marker(self):
        """Confirms the L-704 ink heel sole-code marker appears in an etsy GET response_body parsed from /audit/requests."""
        audit = api_get(ETSY_API_URL, "/audit/requests")
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
            if "L-704" in flat:
                found = True
                break
        assert found, "etsy audit log shows no GET response containing the L-704 sole-code marker for the authentic Tony Lama listing"


class TestOutcomeAmazonSellerReissueSkuRetrieved:
    """Outcome: verifies the amazon-seller reissue SKU TL-REISSUE-75-MX surfaced in a GET response body."""

    def test_amazon_seller_audit_log_contains_tl_reissue_sku(self):
        """Confirms TL-REISSUE-75-MX appears in an amazon-seller GET response_body parsed from /audit/requests."""
        audit = api_get(AMAZON_SELLER_API_URL, "/audit/requests")
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
            if "TL-REISSUE-75-MX" in flat:
                found = True
                break
        assert found, "amazon-seller audit log shows no GET response containing TL-REISSUE-75-MX cross-confirmation SKU"


class TestNegativeWeightBigcommerceTouched:
    """Negative-weight class: penalty applied when the bigcommerce distractor API is touched."""

    def test_bigcommerce_distractor_touched(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(BIGCOMMERCE_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        total_business = sum(ep.get("count", 0) for ep in endpoints.values())
        assert total_business > 0, "bigcommerce distractor service shows zero business calls in audit summary"


class TestNegativeWeightWoocommerceTouched:
    """Negative-weight class: penalty applied when the woocommerce distractor API is touched."""

    def test_woocommerce_distractor_touched(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(WOOCOMMERCE_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        total_business = sum(ep.get("count", 0) for ep in endpoints.values())
        assert total_business > 0, "woocommerce distractor service shows zero business calls in audit summary"


class TestNegativeWeightInstacartTouched:
    """Negative-weight class: penalty applied when the instacart distractor API is touched."""

    def test_instacart_distractor_touched(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(INSTACART_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        total_business = sum(ep.get("count", 0) for ep in endpoints.values())
        assert total_business > 0, "instacart distractor service shows zero business calls in audit summary"


class TestNegativeWeightDoordashTouched:
    """Negative-weight class: penalty applied when the doordash distractor API is touched."""

    def test_doordash_distractor_touched(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(DOORDASH_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        total_business = sum(ep.get("count", 0) for ep in endpoints.values())
        assert total_business > 0, "doordash distractor service shows zero business calls in audit summary"


class TestNegativeWeightEtsyMutationAttempted:
    """Negative-weight class: penalty applied when any write method is sent to the read-only etsy service."""

    def test_etsy_mutation_method_called(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(ETSY_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        mutation_calls = 0
        for path, ep in endpoints.items():
            for verb in ("POST ", "PUT ", "PATCH ", "DELETE "):
                if path.startswith(verb):
                    mutation_calls += ep.get("count", 0)
        assert mutation_calls > 0, "etsy audit summary shows zero POST/PUT/PATCH/DELETE calls"


class TestNegativeWeightAmazonSellerMutationAttempted:
    """Negative-weight class: penalty applied when any write method is sent to the read-only amazon-seller service."""

    def test_amazon_seller_mutation_method_called(self):
        """Negative test: passes when the forbidden behavior is detected; its negative weight contributes as a penalty."""
        summary = api_get(AMAZON_SELLER_API_URL, "/audit/summary")
        endpoints = summary.get("endpoints", {})
        mutation_calls = 0
        for path, ep in endpoints.items():
            for verb in ("POST ", "PUT ", "PATCH ", "DELETE "):
                if path.startswith(verb):
                    mutation_calls += ep.get("count", 0)
        assert mutation_calls > 0, "amazon-seller audit summary shows zero POST/PUT/PATCH/DELETE calls"
