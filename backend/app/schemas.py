from pydantic import BaseModel, Field
from typing import Optional


class ListingRequest(BaseModel):
    """
    Incoming listing data scraped from Facebook Marketplace
    """
    title: str = Field(..., description="Product title")
    price: float = Field(..., gt=0, description="Listing price")
    location: Optional[str] = Field(None, description="Listing location")
    url: str = Field(..., description="Marketplace listing URL")


class AnalysisResponse(BaseModel):
    """
    Result of flip analysis
    """
    estimated_resale_price: float
    estimated_profit: float
    roi_percent: float
    recommendation: str
    confidence: str
    notes: str
