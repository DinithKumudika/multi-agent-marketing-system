import questionary
from ..config.logger import logger

# --- Helper Functions for Different Question Types ---
def _ask_required(question: str) -> str:
    """Asks a required text question."""
    return questionary.text(
        f"{question} (Required)",
        validate=lambda text: len(text) > 0 or "This field is required."
    ).unsafe_ask()

def _ask_required_multiline(question: str) -> str:
    """Asks a required multi-line text question."""
    logger.info(f"{question} (Required): (Press 'Enter' for a new line, 'Esc' then 'Enter' to finish)")
    return questionary.text(
        f"{question} (Required, 'Esc' + 'Enter' to finish)",
        multiline=True,
        validate=lambda text: len(text) > 0 or "This field is required."
    ).unsafe_ask()

def _ask_optional(question: str, default: str = "") -> str | None:
    """Asks an optional text question."""
    answer = questionary.text(f"{question} (Optional, press Enter to skip)", default=default).unsafe_ask()
    return answer if answer else None

def _ask_optional_list(question: str) -> list[str] | None:
    """Asks for an optional, comma-separated list."""
    answer = questionary.text(f"{question} (Optional, comma-separated list)", default="").unsafe_ask()
    if not answer:
        return None
    return [item.strip() for item in answer.split(',') if item.strip()]


# --- Main Collector Function ---
def collect_brief() -> dict:
    """
    Guides the user through an interactive CLI session to collect all
    marketing brief information.
    """
    brief_data = {}

    questionary.print("--- Starting New Marketing Brief ---", style="bold fg:green")
    questionary.print("Please provide the following information. Optional fields can be skipped.")

    # --- 1. Basic Information ---
    questionary.print("\n--- 1. Basic Information ---", style="bold fg:cyan")
    brief_data["product_name"] = _ask_required("Product Idea/Name")
    brief_data["category"] = _ask_required("Category/Industry")
    brief_data["one_line_summary"] = _ask_optional("One-line Summary")
    brief_data["detailed_description"] = _ask_required_multiline("Detailed Description")

    # --- 2. Problem & Solution Definition ---
    questionary.print("\n--- 2. Problem & Solution Definition ---", style="bold fg:cyan")
    brief_data["problem_statement"] = _ask_required_multiline("Problem Statement")
    brief_data["target_pain_points"] = _ask_optional_list("Target Pain Points")

    # --- 3. Target Audience ---
    questionary.print("\n--- 3. Target Audience ---", style="bold fg:cyan")
    brief_data["primary_audience"] = _ask_required("Primary Audience")
    brief_data["demographics"] = _ask_optional("Demographics (e.g., Age, Gender)")
    brief_data["psychographics"] = _ask_optional("Psychographics (e.g., Lifestyle, Values)")
    brief_data["geographic_market"] = _ask_optional("Geographic Market")

    # --- 4. Product Features & Benefits ---
    questionary.print("\n--- 4. Product Features & Benefits ---", style="bold fg:cyan")
    brief_data["key_features"] = _ask_optional_list("Key Features")
    brief_data["main_benefits"] = _ask_optional_list("Main Benefits")
    brief_data["usp"] = _ask_required("Unique Selling Proposition (USP)")

    # --- 5. Business & Market Details (Optional) ---
    questionary.print("\n--- 5. Business & Market Details (Optional) ---", style="bold fg:cyan")
    brief_data["price_point"] = _ask_optional("Estimated Price Point")
    brief_data["known_competitors"] = _ask_optional_list("Known Competitors")
    brief_data["distribution_channels"] = _ask_optional_list("Distribution Channels")

    # --- 6. Branding Preferences (Optional) ---
    questionary.print("\n--- 6. Branding Preferences (Optional) ---", style="bold fg:cyan")
    brief_data["brand_name_ideas"] = _ask_optional_list("Preferred Brand Name Ideas")
    # This one is required, but we give a default
    brief_data["tone_and_personality"] = questionary.text(
        "Tone & Personality (Required)",
        default="Professional and helpful"
    ).unsafe_ask()
    brief_data["color_preferences"] = _ask_optional_list("Color Preferences")
    brief_data["logo_tagline_ideas"] = _ask_optional_list("Logo/Tagline Ideas")

    # --- 7. Goals & Success Criteria ---
    questionary.print("\n--- 7. Goals & Success Criteria ---", style="bold fg:cyan")
    brief_data["main_goal"] = _ask_optional("Main Goal (e.g., 'Get signups')")
    brief_data["target_launch_date"] = _ask_optional("Target Launch Date")
    brief_data["budget_range"] = _ask_required("Budget Range (e.g., '$1,000')")
    brief_data["preferred_channels"] = _ask_optional_list("Preferred Channels")

    questionary.print("\n--- Brief Collection Complete! ---", style="bold fg:green")

    # Return the raw dictionary. Pydantic will validate it in main.py
    return brief_data