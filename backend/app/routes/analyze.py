from fastapi import APIRouter
from app.schemas import ListingRequest, AnalysisResponse
from app.services.evaluator import evaluate_listing
from app.errors import InternalServiceError

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
