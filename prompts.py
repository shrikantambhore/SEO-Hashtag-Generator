"""
prompts.py
Contains all prompt-building logic for SEO and Hashtag generation.
Prompts are assembled from structured project inputs — never generic.
"""

from grok_client import call_grok


# ──────────────────────────────────────────────
# SYSTEM PROMPTS
# ──────────────────────────────────────────────

SEO_SYSTEM_PROMPT = """
You are an expert real estate SEO strategist for the Indian property market.
You write search-intent-driven SEO copy for residential and commercial project launches.
Your output is always grounded in the specific project details provided — no filler phrases
unless the input clearly warrants them.

You MUST respond with a single valid JSON object and nothing else.
Do not include any explanation, markdown, or text outside the JSON.
""".strip()

HASHTAG_SYSTEM_PROMPT = """
You are a real estate social media strategist who creates high-performing hashtag sets
for Instagram, LinkedIn, and X (formerly Twitter).
Your hashtags are location-aware, audience-specific, and campaign-ready.
You never use generic lifestyle hashtags unless they directly relate to the project's USP.

You MUST respond with a single valid JSON object and nothing else.
Do not include any explanation, markdown, or text outside the JSON.
""".strip()


# ──────────────────────────────────────────────
# PROMPT BUILDERS
# ──────────────────────────────────────────────

def _build_project_brief(inputs: dict) -> str:
    """Formats project inputs into a compact brief string for prompt injection."""
    landmarks_line = (
        f"Nearby landmarks: {inputs['landmarks']}"
        if inputs.get("landmarks")
        else "No specific landmarks mentioned."
    )
    configs_line = ", ".join(inputs["configurations"]) if inputs.get("configurations") else "Not specified"

    return f"""
Project Name     : {inputs['project_name']}
City             : {inputs['city']}
Micro Market     : {inputs['micro_market']}
Project Type     : {inputs['project_type']}
Configurations   : {configs_line}
{landmarks_line}
Brand Positioning: {inputs['brand_positioning']}
USP              : {inputs['usp']}
""".strip()


# ──────────────────────────────────────────────
# SEO GENERATION
# ──────────────────────────────────────────────

def generate_seo(inputs: dict) -> dict:
    """
    Builds the SEO prompt and calls Grok.
    Returns a dict with titles, meta descriptions, and keyword groups.

    Expected output schema:
    {
        "seo_titles": ["...", "...", "..."],
        "meta_descriptions": ["...", "...", "..."],
        "primary_keywords": ["...", ...],
        "secondary_keywords": ["...", ...],
        "long_tail_keywords": ["...", ...]
    }
    """
    brief = _build_project_brief(inputs)

    user_prompt = f"""
Generate SEO content for the following real estate project launch:

{brief}

Return a JSON object with exactly these keys:

{{
    "seo_titles": [
        "Title 1 (50-60 chars, location + config + project name)",
        "Title 2 (search-intent focused, includes city + project type)",
        "Title 3 (USP-driven, differentiator first)"
    ],
    "meta_descriptions": [
        "Description 1 (150-160 chars, includes CTA, city, key config)",
        "Description 2 (benefits-first, micro market, nearby landmark if available)",
        "Description 3 (brand positioning angle, includes USP)"
    ],
    "primary_keywords": [
        "5-7 high-intent keywords combining project type + city + config"
    ],
    "secondary_keywords": [
        "6-8 supporting keywords: micro market, landmarks, price bracket signals"
    ],
    "long_tail_keywords": [
        "5-7 long-tail phrases buyers actually search: e.g. '3BHK flats near <landmark> in <city>'"
    ]
}}

Rules:
- Every keyword and title must reference the actual project details above.
- Do not use filler phrases like "luxury living" unless the brand_positioning explicitly says so.
- Titles must be unique in angle — do not repeat the same structure.
- Long-tail keywords must match real buyer search intent for this specific project.
""".strip()

    return call_grok(SEO_SYSTEM_PROMPT, user_prompt)


# ──────────────────────────────────────────────
# HASHTAG GENERATION
# ──────────────────────────────────────────────

def generate_hashtags(inputs: dict) -> dict:
    """
    Builds the hashtag prompt and calls Grok.
    Returns platform-specific hashtag sets and social keywords.

    Expected output schema:
    {
        "instagram_hashtags": ["#...", ...],
        "linkedin_hashtags": ["#...", ...],
        "x_hashtags": ["#...", ...],
        "social_keywords": ["...", ...]
    }
    """
    brief = _build_project_brief(inputs)

    user_prompt = f"""
Generate social media hashtags for this real estate project launch:

{brief}

Return a JSON object with exactly these keys:

{{
    "instagram_hashtags": [
        "20-25 hashtags: mix of project-specific, city, micro market, project type,
         configuration, landmark-based, USP-based, and discovery tags.
         Example format: #ProjectName, #CityRealEstate, #MicroMarketHomes"
    ],
    "linkedin_hashtags": [
        "10-12 professional hashtags for B2B, investment, and developer audience.
         Focus on: city + real estate, project type, investment angle, developer brand"
    ],
    "x_hashtags": [
        "8-10 concise, trending-style hashtags for X.
         Short, punchy, relevant to Indian real estate audience"
    ],
    "social_keywords": [
        "10-12 non-hashtag keywords/phrases suitable for caption copy,
         alt text, and social bios. Location-aware and USP-driven."
    ]
}}

Rules:
- All hashtags must be CamelCase with # prefix.
- Instagram set should be discovery-optimised (mix of niche and broad).
- LinkedIn set should appeal to investors and property professionals.
- X set should be concise and campaign-launch ready.
- Do not include generic hashtags like #Home or #Property unless combined with location.
- Social keywords must be plain phrases (no #), useful for caption writing.
""".strip()

    return call_grok(HASHTAG_SYSTEM_PROMPT, user_prompt)
