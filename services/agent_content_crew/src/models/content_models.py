from pydantic import BaseModel, Field
from typing import List, Optional


class LandingPageContent(BaseModel):
    """
    Structured content for a product landing page.
    """
    
    headline: str = Field(..., description="The main headline for the landing page (max 10 words).")
    sub_headline: str = Field(..., description="A brief sub-headline (max 20 words).")
    
    feature_blurbs: List[str] = Field(...,description="A list of 3 short feature blurbs, each under 25 words.")
    
class MarketingContent(BaseModel):
    """
    The complete, structured marketing content output.
    """
    blog_post_markdown: str = Field(
        description="The full, 500-word SEO-friendly blog post, formatted in markdown."
    )
    landing_page: LandingPageContent = Field(
        description="Structured content for the landing page."
    )

class MarketingBrief(BaseModel):
    """
    A comprehensive marketing brief detailing all aspects of the product
    and campaign goals.
    """
    # 1. Basic Information
    product_name: str = Field(..., description="A short working title for the idea.")
    category: str = Field(..., description="Broad category for classification.")
    one_line_summary: Optional[str] = Field(None, description="Short description (max 20 words).")
    detailed_description: str = Field(..., description="Paragraph describing the idea, features, and use case.")

    # 2. Problem & Solution Definition
    problem_statement: str = Field(..., description="What problem does the product solve?")
    target_pain_points: Optional[List[str]] = Field(None, description="Key frustrations of customers.")

    # 3. Target Audience
    primary_audience: str = Field(..., description="Who is most likely to use/buy it?")
    demographics: Optional[str] = Field(None, description="Age, gender, income level.")
    psychographics: Optional[str] = Field(None, description="Lifestyle, values, interests.")
    geographic_market: Optional[str] = Field(None, description="Country or region focus.")

    # 4. Product Features & Benefits
    key_features: Optional[List[str]] = Field(None, description="Main characteristics of the product.")
    main_benefits: Optional[List[str]] = Field(None, description="What the user gains.")
    usp: str = Field(..., alias="unique_selling_proposition", description="What makes it stand out.")

    # 5. Business & Market Details (Optional)
    price_point: Optional[str] = Field(None, alias="estimated_price_point", description="Target selling price.")
    known_competitors: Optional[List[str]] = Field(None, description="List of existing competitors.")
    distribution_channels: Optional[List[str]] = Field(None, description="Online store, Amazon, etc.")

    # 6. Branding Preferences (Optional)
    brand_name_ideas: Optional[List[str]] = Field(None, description="Any name ideas.")
    tone_and_personality: str = Field(..., description="Brand voice (e.g., 'Professional and helpful').")
    color_preferences: Optional[List[str]] = Field(None, description="Colors associated with the product.")
    logo_tagline_ideas: Optional[List[str]] = Field(None, description="Optional starter ideas.")

    # 7. Goals & Success Criteria
    main_goal: Optional[str] = Field(None, description="What to achieve first (e.g., 'Get signups').")
    target_launch_date: Optional[str] = Field(None, description="Helps time campaign.")
    budget_range: str = Field(..., description="For ads or initial marketing spend.")
    preferred_channels: Optional[List[str]] = Field(None, description="Channels to prioritize.")

    class Config:
        allow_population_by_field_name = True

class ResearchReport(BaseModel):
    """
    A structured research report containing validated market insights.
    """
    audience_insights: str = Field(
        ...,
        description="A 2-3 sentence summary of the target audience's demographics and psychographics."
    )
    market_trends: List[str] = Field(
        ...,
        description="A list of 2-3 key market trends for the product's category.",
        min_items=2,
        max_items=3
    )
    key_pain_points: List[str] = Field(
        ...,
        description="A list of the top 3-5 pain points the product addresses.",
        min_items=3,
        max_items=5
    )
    competitor_analysis: str = Field(
        ...,
        description="A 3-5 sentence paragraph analyzing 3-5 competitors and their strengths/weaknesses."
    )
    seo_keywords: List[str] = Field(
        ...,
        description="A list of 10 primary SEO keywords.",
        min_items=10,
        max_items=10
    )