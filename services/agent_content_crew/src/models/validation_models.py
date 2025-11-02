from pydantic import BaseModel, Field, conint
from typing import Literal

class ValidationReport(BaseModel):
    """
    A structured market validation report with a final viability score.
    """
    market_demand: str = Field(
        ...,
        description="Analysis of search volume, trends, and user interest."
    )
    competitor_density: Literal["Low", "Medium", "High"] = Field(
        ...,
        description="The number and strength of existing competitors."
    )
    monetization_potential: str = Field(
        ...,
        description="Analysis of how similar products make money and the idea's potential."
    )
    viability_score: conint(ge=0, le=100) = Field(
        ...,
        description="The final market viability score from 0 (No-Go) to 100 (High Potential)."
    )
    recommendation: str = Field(
        ...,
        description="A final recommendation, e.g., 'Proceed with caution' or 'High potential, proceed.'"
    )