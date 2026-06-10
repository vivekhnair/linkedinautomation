"""Lead generation recommendations engine."""

from __future__ import annotations

from typing import Any


LEAD_MAGNETS = [
    {
        "title": "The Enterprise Agentic AI Readiness Assessment",
        "format": "Interactive scorecard (10 questions)",
        "target_buyer": "CTO, Head of AI",
        "funnel_stage": "Top of Funnel",
        "estimated_conversion": "8-12% of LinkedIn profile visitors",
        "production_effort": "MEDIUM",
        "cta_text": "Take the 2-minute assessment → azilen.com/ai-readiness",
    },
    {
        "title": "2026 Enterprise AI Implementation Playbook",
        "format": "15-page PDF guide",
        "target_buyer": "CTO, VP Engineering, CDO",
        "funnel_stage": "Middle of Funnel",
        "estimated_conversion": "5-8% of post engagers",
        "production_effort": "HIGH",
        "cta_text": "Download the playbook → azilen.com/ai-playbook",
    },
    {
        "title": "HRTech AI Transformation Checklist",
        "format": "1-page checklist PDF",
        "target_buyer": "CHRO, HR Technology Leaders",
        "funnel_stage": "Top of Funnel",
        "estimated_conversion": "10-15% of HR-focused post engagers",
        "production_effort": "LOW",
        "cta_text": "Get the checklist → azilen.com/hrtech-checklist",
    },
    {
        "title": "Product Engineering Cost Calculator",
        "format": "Interactive web tool",
        "target_buyer": "CTO, VP Product, Startup Founders",
        "funnel_stage": "Middle of Funnel",
        "estimated_conversion": "12-18% of product engineering post engagers",
        "production_effort": "HIGH",
        "cta_text": "Calculate your build cost → azilen.com/cost-calculator",
    },
    {
        "title": "Manufacturing AI ROI Benchmark Report",
        "format": "8-page research report",
        "target_buyer": "CTO, VP Technology (Manufacturing)",
        "funnel_stage": "Top of Funnel",
        "estimated_conversion": "6-10% of manufacturing post engagers",
        "production_effort": "HIGH",
        "cta_text": "Download the benchmark → azilen.com/manufacturing-ai-report",
    },
]

LANDING_PAGE_RECOMMENDATIONS = [
    {
        "page": "AI Services Landing Page",
        "url_suggestion": "azilen.com/enterprise-ai",
        "critical_elements": [
            "Above-fold: Specific outcome statement (not 'We build AI solutions')",
            "Social proof: 3 client logos + outcome metrics",
            "Single CTA: 'Book a 30-minute AI strategy call' with Calendly embed",
            "Case study thumbnails below fold",
            "No form longer than 3 fields",
        ],
        "current_gap": "Generic service pages don't convert LinkedIn traffic",
        "expected_improvement": "2-4x conversion rate improvement",
    },
    {
        "page": "LinkedIn Traffic Landing Page",
        "url_suggestion": "azilen.com/linkedin",
        "critical_elements": [
            "Personal welcome: 'Welcome from LinkedIn →'",
            "Latest thought leadership content",
            "Direct meeting booking (no contact form)",
            "3 specific outcome case studies",
        ],
        "current_gap": "No dedicated LinkedIn traffic page = lost conversion",
        "expected_improvement": "Creates trackable LinkedIn → pipeline attribution",
    },
]

CTA_IMPROVEMENTS = [
    {
        "current_pattern": "Visit our website",
        "improved_version": "I break down our 6-step Agentic AI deployment framework on our site. Link in comments.",
        "why": "Specific value proposition + indicates where link is (comments get more reach than links in posts)",
    },
    {
        "current_pattern": "Contact us for more information",
        "improved_version": "If you're evaluating AI vendors this quarter, I'd suggest a 20-minute architecture review. No pitch. DM me 'AI REVIEW'.",
        "why": "Specific time commitment, specific value, specific action word",
    },
    {
        "current_pattern": "Learn more about our services",
        "improved_version": "Which of these 3 AI challenges is blocking your team this quarter? Comment below – I'll respond with specific frameworks.",
        "why": "Creates engagement + qualifies intent + stays in feed algorithm",
    },
    {
        "current_pattern": "Follow us for updates",
        "improved_version": "I publish one enterprise AI insight every Tuesday. Follow so you don't miss it.",
        "why": "Gives specific reason + sets expectation + feels personal",
    },
]


def get_lead_recommendations(performance_data: dict[str, Any]) -> dict[str, Any]:
    summary = performance_data.get("summary", {})
    click_rate = 0
    posts_data = performance_data.get("performance_by_type", [])

    zero_click_issue = summary.get("total_impressions_90d", 0) > 0

    priority_magnets = sorted(LEAD_MAGNETS, key=lambda x: x["production_effort"] == "LOW", reverse=True)[:3]

    return {
        "immediate_actions": [
            "Add 'Link in first comment' to every post instead of post body links",
            "Create dedicated LinkedIn landing page at azilen.com/linkedin",
            "Add UTM tracking to all LinkedIn post links immediately",
            "Install LinkedIn Insight Tag on azilen.com for retargeting",
            "Set up Calendly for 'Book AI Strategy Call' and pin to LinkedIn profile",
        ],
        "quick_win_lead_magnets": priority_magnets,
        "all_lead_magnets": LEAD_MAGNETS,
        "landing_page_recommendations": LANDING_PAGE_RECOMMENDATIONS,
        "cta_upgrade_examples": CTA_IMPROVEMENTS,
        "pipeline_attribution_setup": {
            "utm_parameters": "utm_source=linkedin&utm_medium=social&utm_campaign=organic&utm_content={post_topic}",
            "crm_integration": "Connect LinkedIn Lead Gen Forms to Zoho CRM for direct lead capture",
            "tracking_dashboard": "Create Zoho Analytics report: LinkedIn impressions → profile visits → website clicks → form fills → meetings booked",
        },
        "monthly_lead_target": {
            "impressions_needed": 50000,
            "ctr_target_pct": 0.5,
            "website_visits_target": 250,
            "lead_conversion_rate_pct": 3,
            "monthly_leads_target": 7,
            "monthly_meetings_target": 3,
            "note": "Based on current follower base of ~99K. Achievable with 7 posts/week + lead magnets.",
        },
    }
