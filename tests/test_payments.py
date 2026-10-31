import hashlib
import hmac
import unittest
from unittest.mock import Mock, patch

import payments
from study_store import PHYSICS_BUNDLE


class PaymentTests(unittest.TestCase):
    def setUp(self):
        self.secrets = {
            "razorpay": {"key_id": "test-key", "key_secret": "test-secret"},
            "APP_URL": "https://example.streamlit.app/",
        }

    def test_create_payment_link_requests_fixed_bundle_amount_and_usd(self):
        response = Mock(ok=True)
        response.json.return_value = {"short_url": "https://rzp.io/i/test"}
        with (
            patch.object(payments.st, "secrets", self.secrets),
            patch.object(payments.requests, "post", return_value=response) as post,
        ):
            link = payments.create_payment_link("buyer@example.com")

        self.assertEqual(link, "https://rzp.io/i/test")
        payload = post.call_args.kwargs["json"]
        self.assertEqual(payload["amount"], 100)
        self.assertEqual(payload["currency"], "USD")
        self.assertFalse(payload["accept_partial"])
        self.assertEqual(payload["customer"]["email"], "buyer@example.com")
        self.assertEqual(payload["notes"]["product_id"], PHYSICS_BUNDLE["id"])
        self.assertEqual(payload["callback_url"], self.secrets["APP_URL"])

    def test_payment_requires_valid_signature_and_provider_confirmation(self):
        payment_id = "pay_test"
        link_id = "plink_test"
        reference_id = "order_test"
        status = "paid"
        signed_payload = f"{link_id}|{reference_id}|{status}|{payment_id}".encode()
        signature = hmac.new(b"test-secret", signed_payload, hashlib.sha256).hexdigest()
        response = Mock(ok=True)
        response.json.return_value = {
            "id": link_id,
            "reference_id": reference_id,
            "status": "paid",
            "amount": 100,
            "currency": "USD",
            "notes": {"product_id": PHYSICS_BUNDLE["id"]},
        }

        with (
            patch.object(payments.st, "secrets", self.secrets),
            patch.object(payments.requests, "get", return_value=response) as get,
        ):
            self.assertTrue(payments.verify_payment(payment_id, link_id, reference_id, status, signature))
            self.assertFalse(payments.verify_payment(payment_id, link_id, reference_id, status, "bad-signature"))

        get.assert_called_once()

    def test_payment_is_rejected_if_link_amount_or_product_is_wrong(self):
        link_id = "plink_test"
        reference_id = "order_test"
        payment_id = "pay_test"
        status = "paid"
        payload = f"{link_id}|{reference_id}|{status}|{payment_id}".encode()
        signature = hmac.new(b"test-secret", payload, hashlib.sha256).hexdigest()
        response = Mock(ok=True)
        response.json.return_value = {
            "id": link_id,
            "reference_id": reference_id,
            "status": "paid",
            "amount": 200,
            "currency": "USD",
            "notes": {"product_id": PHYSICS_BUNDLE["id"]},
        }

        with (
            patch.object(payments.st, "secrets", self.secrets),
            patch.object(payments.requests, "get", return_value=response),
        ):
            self.assertFalse(payments.verify_payment(payment_id, link_id, reference_id, status, signature))

    def test_missing_secrets_are_reported_as_configuration_error(self):
        from streamlit.errors import StreamlitSecretNotFoundError

        class MissingSecrets:
            def __getitem__(self, key):
                raise StreamlitSecretNotFoundError("missing")

        with (
            patch.object(payments.st, "secrets", MissingSecrets()),
            self.assertRaises(payments.PaymentConfigurationError),
        ):
            payments.create_payment_link("buyer@example.com")


if __name__ == "__main__":
    unittest.main()
