from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator


class ListingRequest(BaseModel):
    title: str = Field(..., min_length=1, description="Product title")
    price: float = Field(..., gt=0, description="Listing price (numeric)")
    location: str | None = Field(None, description="Listing location")
    url: HttpUrl = Field(..., description="Facebook Marketplace item URL")

    @field_validator("url")
    @classmethod
    def validate_marketplace_item_url(cls, value: HttpUrl):
        s = str(value)
        if "/marketplace/item/" not in s:
            raise ValueError(
                "url must be a Facebook Marketplace item link \
            (/marketplace/item/...)"
            )
        return value


Recommendation = Literal["GOOD_FLIP", "MAYBE", "PASS"]
Confidence = Literal["LOW", "MEDIUM", "HIGH"]


class AnalysisResponse(BaseModel):
    estimated_resale_price: float
    estimated_profit: float
    roi_percent: float
    recommendation: Recommendation
    confidence: Confidence
    notes: str
