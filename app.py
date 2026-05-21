"""
app.py
Main Streamlit application.
Handles all UI rendering — inputs, generation triggers, and output display.
All business logic is delegated to prompts.py and utils.py.
"""

import streamlit as st
from prompts import generate_seo, generate_hashtags
from utils import (
    INDIAN_CITIES, PROJECT_TYPES, CONFIGURATIONS,
    validate_inputs, format_keyword_list, format_hashtag_block, safe_get_list,
)

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────

st.set_page_config(
    page_title="RealLaunch – SEO & Social Generator",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ──────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────

st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&family=DM+Sans:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Sora', sans-serif;
    }

    /* Header band */
    .app-header {
        background: linear-gradient(135deg, #0f1b2d 0%, #1a3a5c 100%);
        border-radius: 12px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        color: white;
    }
    .app-header h1 { color: #ffffff; margin: 0 0 0.4rem 0; font-size: 2rem; }
    .app-header p  { color: #a8c4e0; margin: 0; font-size: 1rem; }

    /* Section cards */
    .output-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
    }
    .output-card h4 {
        font-family: 'Sora', sans-serif;
        color: #0f1b2d;
        margin: 0 0 0.75rem 0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Numbered items */
    .item-row {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        margin-bottom: 0.5rem;
        font-size: 0.92rem;
        color: #1e293b;
        line-height: 1.5;
    }
    .item-number {
        display: inline-block;
        background: #1a3a5c;
        color: white;
        border-radius: 50%;
        width: 22px;
        height: 22px;
        text-align: center;
        line-height: 22px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.6rem;
        font-family: 'Sora', sans-serif;
        vertical-align: middle;
    }

    /* Keyword pill block */
    .keyword-block {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        font-size: 0.9rem;
        color: #334155;
        line-height: 1.8;
    }

    /* Hashtag block */
    .hashtag-block {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.9rem 1rem;
        font-size: 0.88rem;
        color: #1a3a5c;
        font-weight: 500;
        line-height: 2;
        word-break: break-word;
    }

    /* Platform badge */
    .platform-badge {
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'Sora', sans-serif;
        margin-bottom: 0.6rem;
    }
    .badge-instagram { background: #fce7f3; color: #be185d; }
    .badge-linkedin  { background: #dbeafe; color: #1d4ed8; }
    .badge-x         { background: #f1f5f9; color: #0f172a; }
    .badge-social    { background: #dcfce7; color: #15803d; }

    /* Generate button styling override */
    div.stButton > button {
        background: linear-gradient(135deg, #1a3a5c, #2563eb);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-family: 'Sora', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: opacity 0.2s;
    }
    div.stButton > button:hover { opacity: 0.88; }

    /* Divider */
    hr { border-color: #e2e8f0; margin: 1.5rem 0; }

    /* Form section label */
    .form-section-label {
        font-family: 'Sora', sans-serif;
        font-size: 0.78rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 1.2rem 0 0.4rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────

st.markdown("""
<div class="app-header">
    <h1>🏢 RealLaunch Content Generator</h1>
    <p>AI-powered SEO copy and social hashtags for every real estate project launch — powered by Grok.</p>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# INPUT FORM
# ──────────────────────────────────────────────

with st.form("project_form"):
    st.markdown('<div class="form-section-label">Project Identity</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        project_name = st.text_input(
            "Project Name *",
            placeholder="e.g. Prestige Elysian Heights",
        )
    with col2:
        city = st.selectbox("City *", options=["— Select City —"] + INDIAN_CITIES)

    col3, col4 = st.columns(2)
    with col3:
        micro_market = st.text_input(
            "Micro Market *",
            placeholder="e.g. Sarjapur Road, Whitefield, BKC",
        )
    with col4:
        project_type = st.selectbox("Project Type *", options=["— Select Type —"] + PROJECT_TYPES)

    st.markdown('<div class="form-section-label">Unit & Location Details</div>', unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        configurations = st.multiselect(
            "Configuration(s) *",
            options=CONFIGURATIONS,
            placeholder="Select all that apply",
        )
    with col6:
        landmarks = st.text_input(
            "Nearby Landmarks (optional)",
            placeholder="e.g. ISRO, Infosys Campus, Phoenix Mall",
        )

    st.markdown('<div class="form-section-label">Brand & Positioning</div>', unsafe_allow_html=True)
    brand_positioning = st.text_input(
        "Brand Positioning *",
        placeholder="e.g. Mid-premium, aspirational homebuyer, tech-corridor families",
    )
    usp = st.text_area(
        "USP — Unique Selling Proposition *",
        placeholder="e.g. RERA-registered, rooftop infinity pool, 15 min from airport, zero GST on possession",
        height=90,
    )

    st.markdown("---")
    submitted = st.form_submit_button("✨ Generate SEO + Hashtags")


# ──────────────────────────────────────────────
# GENERATION LOGIC
# ──────────────────────────────────────────────

if submitted:
    # Normalise city / project_type placeholders
    inputs = {
        "project_name":      project_name.strip(),
        "city":              city if city != "— Select City —" else "",
        "micro_market":      micro_market.strip(),
        "project_type":      project_type if project_type != "— Select Type —" else "",
        "configurations":    configurations,
        "landmarks":         landmarks.strip(),
        "brand_positioning": brand_positioning.strip(),
        "usp":               usp.strip(),
    }

    # Validate
    error = validate_inputs(inputs)
    if error:
        st.error(f"⚠️ {error}")
        st.stop()

    # Call API with spinner
    seo_result = None
    hashtag_result = None

    with st.spinner("Generating content with Grok — this takes about 10–20 seconds…"):
        try:
            seo_result = generate_seo(inputs)
        except ValueError as e:
            st.error(f"**SEO generation failed — response parse error.**\n\n{e}")
        except Exception as e:
            st.error(f"**SEO generation failed — API error.**\n\n{e}")

        try:
            hashtag_result = generate_hashtags(inputs)
        except ValueError as e:
            st.error(f"**Hashtag generation failed — response parse error.**\n\n{e}")
        except Exception as e:
            st.error(f"**Hashtag generation failed — API error.**\n\n{e}")

    if not seo_result and not hashtag_result:
        st.stop()

    # ──────────────────────────────────────────
    # OUTPUT TABS
    # ──────────────────────────────────────────

    st.markdown(f"### Results for **{inputs['project_name']}** — {inputs['city']}")
    tab_seo, tab_hashtags = st.tabs(["🔍 SEO Content", "📣 Hashtags & Social"])

    # ── SEO TAB ──────────────────────────────
    with tab_seo:
        if not seo_result:
            st.warning("SEO content could not be generated. Check the error above.")
        else:
            # SEO Titles
            st.markdown('<div class="output-card">', unsafe_allow_html=True)
            st.markdown('<h4>SEO Titles (pick one for your page &lt;title&gt; tag)</h4>', unsafe_allow_html=True)
            for i, title in enumerate(safe_get_list(seo_result, "seo_titles"), 1):
                st.markdown(
                    f'<div class="item-row"><span class="item-number">{i}</span>{title}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

            # Meta Descriptions
            st.markdown('<div class="output-card">', unsafe_allow_html=True)
            st.markdown('<h4>Meta Descriptions (pick one for your &lt;meta description&gt;)</h4>', unsafe_allow_html=True)
            for i, desc in enumerate(safe_get_list(seo_result, "meta_descriptions"), 1):
                st.markdown(
                    f'<div class="item-row"><span class="item-number">{i}</span>{desc}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

            # Keywords
            col_kw1, col_kw2 = st.columns(2)

            with col_kw1:
                st.markdown('<div class="output-card">', unsafe_allow_html=True)
                st.markdown('<h4>Primary Keywords</h4>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="keyword-block">{format_keyword_list(safe_get_list(seo_result, "primary_keywords"))}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown('</div>', unsafe_allow_html=True)

            with col_kw2:
                st.markdown('<div class="output-card">', unsafe_allow_html=True)
                st.markdown('<h4>Secondary Keywords</h4>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="keyword-block">{format_keyword_list(safe_get_list(seo_result, "secondary_keywords"))}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown('</div>', unsafe_allow_html=True)

            # Long-tail Keywords
            st.markdown('<div class="output-card">', unsafe_allow_html=True)
            st.markdown('<h4>Long-Tail Keyword Ideas (great for blog posts & Google Ads)</h4>', unsafe_allow_html=True)
            for i, kw in enumerate(safe_get_list(seo_result, "long_tail_keywords"), 1):
                st.markdown(
                    f'<div class="item-row"><span class="item-number">{i}</span>{kw}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

            # Raw copy block for power users
            with st.expander("📋 Copy all SEO keywords as plain text"):
                all_kw = (
                    safe_get_list(seo_result, "primary_keywords")
                    + safe_get_list(seo_result, "secondary_keywords")
                    + safe_get_list(seo_result, "long_tail_keywords")
                )
                st.code(", ".join(all_kw), language=None)

    # ── HASHTAGS TAB ─────────────────────────
    with tab_hashtags:
        if not hashtag_result:
            st.warning("Hashtag content could not be generated. Check the error above.")
        else:
            ht_col1, ht_col2 = st.columns(2)

            with ht_col1:
                # Instagram
                st.markdown('<div class="output-card">', unsafe_allow_html=True)
                st.markdown(
                    '<h4><span class="platform-badge badge-instagram">📸 Instagram</span></h4>',
                    unsafe_allow_html=True,
                )
                insta = safe_get_list(hashtag_result, "instagram_hashtags")
                st.markdown(
                    f'<div class="hashtag-block">{format_hashtag_block(insta)}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown('</div>', unsafe_allow_html=True)

                # X / Twitter
                st.markdown('<div class="output-card">', unsafe_allow_html=True)
                st.markdown(
                    '<h4><span class="platform-badge badge-x">𝕏 X (Twitter)</span></h4>',
                    unsafe_allow_html=True,
                )
                x_tags = safe_get_list(hashtag_result, "x_hashtags")
                st.markdown(
                    f'<div class="hashtag-block">{format_hashtag_block(x_tags)}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown('</div>', unsafe_allow_html=True)

            with ht_col2:
                # LinkedIn
                st.markdown('<div class="output-card">', unsafe_allow_html=True)
                st.markdown(
                    '<h4><span class="platform-badge badge-linkedin">💼 LinkedIn</span></h4>',
                    unsafe_allow_html=True,
                )
                li_tags = safe_get_list(hashtag_result, "linkedin_hashtags")
                st.markdown(
                    f'<div class="hashtag-block">{format_hashtag_block(li_tags)}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown('</div>', unsafe_allow_html=True)

                # Social Keywords
                st.markdown('<div class="output-card">', unsafe_allow_html=True)
                st.markdown(
                    '<h4><span class="platform-badge badge-social">✏️ Caption Keywords</span></h4>',
                    unsafe_allow_html=True,
                )
                soc_kw = safe_get_list(hashtag_result, "social_keywords")
                st.markdown(
                    f'<div class="keyword-block">{format_keyword_list(soc_kw)}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown('</div>', unsafe_allow_html=True)

            # Copy blocks
            with st.expander("📋 Copy all hashtags as plain text (paste into caption)"):
                all_ht = insta + li_tags + x_tags
                # Deduplicate preserving order
                seen = set()
                deduped = [h for h in all_ht if not (h in seen or seen.add(h))]
                st.code(" ".join(deduped), language=None)

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────

st.markdown("---")
st.markdown(
    "<small style='color:#94a3b8;'>RealLaunch · Powered by Grok (xAI) · "
    "Built with Streamlit · Internal use only</small>",
    unsafe_allow_html=True,
)
