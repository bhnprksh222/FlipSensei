from fastapi import APIRouter

from app.errors import InternalServiceError
from app.schemas import AnalysisResponse, ListingRequest
from app.services.evaluator import evaluate_listing

router = APIRouter()


@router.post("/", response_model=AnalysisResponse)
def analyze(listing: ListingRequest):
    """
    Analyze a single Marketplace listing.
    """
    try:
        return evaluate_listing(listing)
    except Exception as e:
        # If something slipped through unexpectedly, wrap it
        # (Expected AppError types are already handled globally)
        raise InternalServiceError(str(e))
