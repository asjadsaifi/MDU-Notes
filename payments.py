from __future__ import annotations

import hashlib
import hmac
import uuid

import requests
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

from study_store import PHYSICS_BUNDLE


RAZORPAY_API = "https://api.razorpay.com/v1"


class PaymentConfigurationError(RuntimeError):
    pass


class PaymentError(RuntimeError):
    pass


def _payment_credentials() -> tuple[str, str]:
    try:
        credentials = st.secrets["razorpay"]
    except (StreamlitSecretNotFoundError, KeyError):
        raise PaymentConfigurationError("Razorpay credentials are missing.")
    key_id = credentials.get("key_id")
    key_secret = credentials.get("key_secret")
    if not key_id or not key_secret:
        raise PaymentConfigurationError("Razorpay credentials are incomplete.")
    return key_id, key_secret


def create_payment_link(email: str) -> str:
    key_id, key_secret = _payment_credentials()
    try:
        app_url = st.secrets["APP_URL"]
    except (StreamlitSecretNotFoundError, KeyError) as error:
        raise PaymentConfigurationError("The public app URL is missing.") from error
    if not app_url:
        raise PaymentConfigurationError("The public app URL is missing.")

    reference_id = uuid.uuid4().hex
    payload = {
        "amount": PHYSICS_BUNDLE["amount_minor"],
        "currency": PHYSICS_BUNDLE["currency"],
        "accept_partial": False,
        "reference_id": reference_id,
        "description": PHYSICS_BUNDLE["title"],
        "customer": {"email": email},
        "notify": {"sms": False, "email": False},
        "reminder_enable": False,
        "callback_url": app_url,
        "callback_method": "get",
        "notes": {"product_id": PHYSICS_BUNDLE["id"]},
    }
    try:
        response = requests.post(
            f"{RAZORPAY_API}/payment_links",
            auth=(key_id, key_secret),
            json=payload,
            timeout=20,
        )
    except requests.RequestException as error:
        raise PaymentError("Razorpay could not be reached. Please try again.") from error
    if not response.ok:
        raise PaymentError(f"Razorpay could not create checkout (HTTP {response.status_code}).")
    payment_link = response.json().get("short_url")
    if not isinstance(payment_link, str) or not payment_link.startswith("https://"):
        raise PaymentError("Razorpay returned an invalid checkout link.")
    return payment_link


def verify_payment(
    payment_id: str,
    payment_link_id: str,
    reference_id: str,
    status: str,
    signature: str,
) -> bool:
    key_id, key_secret = _payment_credentials()
    if status != "paid":
        return False

    payload = f"{payment_link_id}|{reference_id}|{status}|{payment_id}".encode("utf-8")
    expected_signature = hmac.new(
        key_secret.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(expected_signature, signature):
        return False

    try:
        response = requests.get(
            f"{RAZORPAY_API}/payment_links/{payment_link_id}",
            auth=(key_id, key_secret),
            timeout=20,
        )
    except requests.RequestException as error:
        raise PaymentError("Razorpay could not be reached to verify payment.") from error
    if not response.ok:
        raise PaymentError(f"Razorpay payment verification failed (HTTP {response.status_code}).")

    link = response.json()
    return (
        link.get("id") == payment_link_id
        and link.get("reference_id") == reference_id
        and link.get("status") == "paid"
        and link.get("amount") == PHYSICS_BUNDLE["amount_minor"]
        and link.get("currency") == PHYSICS_BUNDLE["currency"]
        and link.get("notes", {}).get("product_id") == PHYSICS_BUNDLE["id"]
    )
