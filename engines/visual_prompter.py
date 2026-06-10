"""Generates image, carousel, and video production prompts for every post."""

from __future__ import annotations

from typing import Any


AZILEN_BRAND = {
    "primary_colors": ["#0A2558 (deep navy)", "#00A3E0 (electric blue)", "#FFFFFF (white)"],
    "accent_colors": ["#FF6B35 (energy orange)", "#00D4AA (innovation teal)"],
    "typography": "Inter or IBM Plex Sans – clean, modern, technical",
    "style": "Enterprise-modern: clean, data-forward, minimal, premium",
    "avoid": "Stock photo clichés, handshake images, generic tech backgrounds, clip art",
    "feel": "McKinsey meets Stripe – authoritative but modern",
}


def generate_visual_prompts(topic: str, post_type: str = "thought_leadership") -> dict[str, Any]:
    brand_context = (
        f"Brand: Deep navy (#0A2558) and electric blue (#00A3E0) color palette. "
        f"Clean, enterprise-modern aesthetic. IBM Plex Sans or Inter typography. "
        f"Premium, data-forward, minimal design. No stock photo clichés."
    )

    dalle_prompt = _build_dalle_prompt(topic, brand_context)
    midjourney_prompt = _build_midjourney_prompt(topic)
    adobe_concept = _build_adobe_concept(topic, post_type)
    carousel_visual = _build_carousel_visual_flow(topic)

    return {
        "topic": topic,
        "post_type": post_type,
        "brand_guidelines": AZILEN_BRAND,
        "dalle_chatgpt_prompt": dalle_prompt,
        "midjourney_prompt": midjourney_prompt,
        "adobe_express_concept": adobe_concept,
        "carousel_visual_flow": carousel_visual,
        "linkedin_image_specs": {
            "single_image": "1200 x 627 px (1.91:1 ratio)",
            "carousel_slide": "1080 x 1080 px (1:1 square)",
            "cover_image": "1128 x 376 px",
            "profile_banner": "1584 x 396 px",
        },
        "production_notes": [
            "Add Azilen logo (bottom right corner, white or navy version based on background)",
            "Include website URL: azilen.com in small text at bottom",
            "Ensure minimum 4.5:1 contrast ratio for accessibility",
            "Use data visualizations (charts, stats, percentages) over abstract imagery",
            "Every visual must have a clear headline visible without reading the caption",
        ],
    }


def _build_dalle_prompt(topic: str, brand_context: str) -> str:
    return (
        f"Create a professional LinkedIn post image for an enterprise technology company. "
        f"Topic: {topic}. "
        f"{brand_context} "
        f"Style: Clean infographic-style layout with bold headline text overlay. "
        f"Use abstract data visualization elements (network nodes, flowing data streams, minimal geometric shapes). "
        f"Background: Deep navy gradient (#0A2558 to #0D3275). "
        f"Foreground elements: Electric blue accent lines and data nodes. "
        f"Include a bold white headline text area at top third. "
        f"Bottom strip: slight lighter navy with space for company name. "
        f"NO humans, NO stock photography, NO handshakes. "
        f"Resolution: 1200x627px. Ultra-clean, minimal, Fortune 500 quality."
    )


def _build_midjourney_prompt(topic: str) -> str:
    return (
        f"LinkedIn enterprise tech post graphic, topic: {topic}, "
        f"deep navy and electric blue color palette, clean modern minimal design, "
        f"data visualization elements, abstract network topology, "
        f"bold sans-serif typography overlay, enterprise premium aesthetic, "
        f"white space, geometric grid layout, "
        f"--ar 1.91:1 --style raw --v 6 --q 2 "
        f"--no photorealistic humans, stock photos, handshakes, generic office"
    )


def _build_adobe_concept(topic: str, post_type: str) -> dict[str, str]:
    concepts = {
        "thought_leadership": {
            "template_style": "Bold Statement",
            "layout": "Split layout: left 40% solid navy with large quote/stat, right 60% with supporting visual",
            "headline_treatment": "Large bold white text (48-64px), 2-3 words per line maximum",
            "data_element": "One key statistic displayed at 120px+ font size in electric blue",
            "cta_placement": "Bottom strip with website URL and subtle CTA",
        },
        "educational": {
            "template_style": "Numbered Framework",
            "layout": "Clean white background with numbered list items, navy headers",
            "headline_treatment": "Navy header text, numbered steps in electric blue circles",
            "data_element": "Supporting stat in a pull-quote box",
            "cta_placement": "Bottom: 'Read the full guide at azilen.com'",
        },
        "case_study": {
            "template_style": "Before/After Results",
            "layout": "Two-column: Challenge (left, problem framing) → Results (right, metrics)",
            "headline_treatment": "Client industry label + outcome metric as hero",
            "data_element": "3-4 outcome metrics in large navy boxes (% improvement, time saved, ROI)",
            "cta_placement": "CTA button: 'See how we did it →'",
        },
    }
    concept = concepts.get(post_type, concepts["thought_leadership"])
    concept["topic"] = topic
    return concept


def _build_carousel_visual_flow(topic: str) -> dict[str, Any]:
    return {
        "format": "LinkedIn Carousel (PDF/Document post)",
        "slide_count": "8-10 slides",
        "dimensions": "1080 x 1080 px per slide",
        "slide_flow": [
            {
                "slide": 1,
                "type": "Cover / Hook",
                "content": f"Bold provocative headline about {topic}. Subtitle teaser. Azilen logo.",
                "design": "Full navy background, large white headline, electric blue accent line",
            },
            {
                "slide": 2,
                "type": "Problem Statement",
                "content": "The pain/challenge. Relevant statistic. Why this matters now.",
                "design": "White background, navy text, red/orange warning accent",
            },
            {
                "slide": 3,
                "type": "Market Context",
                "content": "Industry data point. What's changing. The stakes.",
                "design": "Light navy background, data visualization chart",
            },
            {
                "slide": "4-6",
                "type": "Framework / Solution Slides",
                "content": "Core insight #1, #2, #3. Each with supporting detail and visual.",
                "design": "Alternating navy/white, numbered elements, icon per point",
            },
            {
                "slide": 7,
                "type": "Evidence / Proof",
                "content": "Case study snippet or benchmark data. Credibility builder.",
                "design": "Full-bleed data visualization or quote treatment",
            },
            {
                "slide": 8,
                "type": "Key Takeaway",
                "content": "Single most important insight. What to do next.",
                "design": "Bold single statement, electric blue accent, high contrast",
            },
            {
                "slide": 9,
                "type": "CTA",
                "content": "Clear next action. Link to resource. How to reach Azilen.",
                "design": "Navy background, white CTA button treatment, contact info",
            },
        ],
        "font_hierarchy": "Headline: 40-48px Bold | Subhead: 24-28px Medium | Body: 16-18px Regular",
        "production_tool": "Canva Pro, Adobe Express, or Figma",
    }
