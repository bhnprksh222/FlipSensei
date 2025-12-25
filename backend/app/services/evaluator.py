from app.schemas import ListingRequest, AnalysisResponse
from app.errors import EvaluationError


def evaluate_listing(listing: ListingRequest) -> AnalysisResponse:
    """
    Evaluates a listing using a simple heuristic.
    Raises EvaluationError for expected evaluation issues.
    """
    try:
        # Defensive checks (even though Pydantic validates)
        if not listing.title.strip():
            raise EvaluationError("Title is empty after trimming.")

        price = float(listing.price)
        if price <= 0:
            raise EvaluationError("Price must be positive.")

        # Heuristic placeholder: resale ~ 1.4x
        estimated_resale = price * 1.4
        profit = estimated_resale - price
        roi = (profit / price) * 100.0

        recommendation = "GOOD_FLIP" if roi >= 30 else (
            "MAYBE" if roi >= 15 else "PASS"
        )

        return AnalysisResponse(
            estimated_resale_price=round(estimated_resale, 2),
            estimated_profit=round(profit, 2),
            roi_percent=round(roi, 2),
            recommendation=recommendation,
            confidence="LOW",
            notes="Heuristic-based estimate (market + AI integrations pending)"
        )

    except EvaluationError:
        # Re-raise expected errors untouched
        raise
    except Exception as e:
        # Convert unexpected evaluation errors into a safe, typed error
        raise EvaluationError(f"Evaluation failed: {e}")
