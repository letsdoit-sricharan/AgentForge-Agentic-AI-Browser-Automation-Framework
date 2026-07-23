"""
Tests for Payment.

Run:
    python -m app.plugins.bookmyshow.tests.test_payment
"""

from app.plugins.bookmyshow.models.payment import (
    Payment,
    PaymentStatus,
)


def test_payment_creation() -> None:
    """
    Test creating a payment.
    """

    payment = Payment(
        amount=500.0,
        currency="INR",
        status=PaymentStatus.INITIATED,
        transaction_id="TXN12345",
        payment_url="https://payment.example.com/txn",
    )

    assert payment.amount == 500.0
    assert payment.currency == "INR"
    assert payment.status is PaymentStatus.INITIATED
    assert payment.transaction_id == "TXN12345"
    assert payment.payment_url == "https://payment.example.com/txn"

    print("✓ Payment creation test passed.")


def test_default_values() -> None:
    """
    Test default values.
    """

    payment = Payment(amount=250.0)

    assert payment.currency == "INR"
    assert payment.status is PaymentStatus.PENDING
    assert payment.transaction_id is None
    assert payment.payment_url is None

    print("✓ Payment default values test passed.")


def run_tests() -> None:

    print("\n" + "=" * 65)
    print("Payment Tests")
    print("=" * 65)

    test_payment_creation()
    test_default_values()

    print("-" * 65)
    print("✅ All Payment tests passed!")
    print("=" * 65)


if __name__ == "__main__":
    run_tests()
