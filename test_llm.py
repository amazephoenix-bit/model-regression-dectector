from app.schemas import SupportResponse

def test_support_response():
    response = SupportResponse(
        category="Billing",
        summary="Customer requested a refund."
    )
    assert response.category == "Billing"
    assert response.summary == "Customer requested a refund."

def test_support_response_category():
    response = SupportResponse(
        category="Technical",
        summary="Customer has a software issue."
    )
    assert response.category in {
        "Billing", "Technical", "Account", "General"
    }