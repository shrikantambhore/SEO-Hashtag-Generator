"""
utils.py
Helper functions for input validation and output formatting.
Keeps app.py clean by isolating all non-UI logic here.
"""

from typing import Optional


# ──────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────

INDIAN_CITIES = [
    "Mumbai", "Pune", "Bengaluru", "Hyderabad", "Chennai",
    "Delhi NCR", "Gurgaon", "Noida", "Ahmedabad", "Kolkata",
    "Surat", "Jaipur", "Lucknow", "Kochi", "Chandigarh",
    "Coimbatore", "Nagpur", "Indore", "Bhopal", "Vadodara",
    "Thane", "Navi Mumbai", "Nashik", "Mysuru", "Visakhapatnam",
]

PROJECT_TYPES = ["Residential", "Commercial", "Mixed Use"]

CONFIGURATIONS = [
    "Studio", "1 BHK", "2 BHK", "3 BHK", "4 BHK",
    "4+ BHK / Penthouse", "Office Space", "Retail / Shop",
    "Plot / Villa", "Co-working",
]


# ──────────────────────────────────────────────
# VALIDATION
# ──────────────────────────────────────────────

def validate_inputs(inputs: dict) -> Optional[str]:
    """
    Validates required form fields.
    Returns an error message string if invalid, else None.
    """
    required = {
        "project_name":      "Project Name",
        "city":              "City",
        "micro_market":      "Micro Market",
        "project_type":      "Project Type",
        "configurations":    "Configuration(s)",
        "brand_positioning": "Brand Positioning",
        "usp":               "USP",
    }

    for field, label in required.items():
        value = inputs.get(field)
        if not value or (isinstance(value, list) and len(value) == 0):
            return f"'{label}' is required. Please fill in all required fields."

    if len(inputs.get("project_name", "").strip()) < 2:
        return "Project Name is too short."

    if len(inputs.get("usp", "").strip()) < 10:
        return "USP should be at least 10 characters for meaningful content generation."

    return None


# ──────────────────────────────────────────────
# OUTPUT FORMATTING
# ──────────────────────────────────────────────

def format_keyword_list(keywords: list) -> str:
    """Joins a list of keywords into a copy-paste-friendly comma-separated string."""
    return ", ".join(keywords) if keywords else "—"


def format_hashtag_block(hashtags: list) -> str:
    """Joins hashtags into a single spaced block for easy copy-paste."""
    return " ".join(hashtags) if hashtags else "—"


def safe_get_list(data: dict, key: str) -> list:
    """
    Safely retrieve a list from the parsed API response.
    Returns empty list if key is missing or value is not a list.
    """
    value = data.get(key, [])
    if isinstance(value, list):
        return value
    # Handle case where model returns a single string instead of a list
    if isinstance(value, str):
        return [value]
    return []
