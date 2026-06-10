"""Competitor intelligence engine for LinkedIn content strategy."""

from __future__ import annotations

from typing import Any


COMPETITOR_PROFILES = {
    "EPAM": {
        "strengths": [
            "Heavy engineering talent content (developer stories)",
            "Strong thought leadership from named engineers/architects",
            "Regular case studies with named enterprise clients",
            "Active employee advocacy program (1000+ employee posts/week)",
        ],
        "weaknesses": [
            "Rarely takes provocative industry positions",
            "Content is achievement-focused, not insight-focused",
            "Weak AI-specific thought leadership despite strong AI practice",
        ],
        "content_gaps": [
            "No agentic AI architecture content",
            "No enterprise AI failure analysis",
            "Weak HRTech content despite large CHRO audience",
        ],
        "posting_frequency": "10-15x/week",
        "top_formats": ["Employee stories", "Case studies", "Award announcements"],
    },
    "Thoughtworks": {
        "strengths": [
            "Technology Radar is industry-defining content",
            "Strong POV content on emerging technologies",
            "Consistent brand voice: opinionated, progressive",
            "Martin Fowler and named thought leaders driving personal brand",
        ],
        "weaknesses": [
            "Expensive positioning creates barrier for mid-market",
            "Weak ROI-focused content",
            "Limited vertical industry content",
        ],
        "content_gaps": [
            "No manufacturing AI content",
            "Weak HRTech angle",
            "Rarely quantifies business outcomes",
        ],
        "posting_frequency": "5-8x/week",
        "top_formats": ["Opinion pieces", "Research publications", "Event content"],
    },
    "Nagarro": {
        "strengths": [
            "High volume posting: 15-20x/week",
            "Strong technical talent content",
            "Active in AI/ML content",
        ],
        "weaknesses": [
            "Content often lacks specific business outcomes",
            "Generic AI content without differentiated positioning",
            "Weak enterprise buyer targeting",
        ],
        "content_gaps": [
            "No agentic AI positioning",
            "Weak C-suite targeting",
            "No data engineering thought leadership",
        ],
        "posting_frequency": "15-20x/week",
        "top_formats": ["Tech posts", "Award wins", "Job postings"],
    },
    "Persistent Systems": {
        "strengths": [
            "Strong financial services and healthcare vertical content",
            "Regular earnings-linked content builds investor confidence",
            "Growing AI practice marketing",
        ],
        "weaknesses": [
            "Content feels corporate/IR-focused, not buyer-focused",
            "Weak engineering thought leadership",
        ],
        "content_gaps": [
            "No agentic AI differentiation",
            "Weak startup/SaaS founder targeting",
            "Limited HRTech content",
        ],
        "posting_frequency": "8-12x/week",
        "top_formats": ["Earnings news", "Partnership announcements", "AI case studies"],
    },
    "GlobalLogic": {
        "strengths": [
            "Strong digital product engineering positioning",
            "Good use of customer logos/case studies",
            "Hitachi ownership gives enterprise credibility",
        ],
        "weaknesses": [
            "Posting frequency dropped post-acquisition",
            "Content becoming more corporate/conservative",
        ],
        "content_gaps": [
            "No Agentic AI content strategy",
            "Weak manufacturing AI content",
            "Limited thought leadership from internal experts",
        ],
        "posting_frequency": "5-8x/week",
        "top_formats": ["Product engineering", "Digital transformation", "Awards"],
    },
    "LTIMindtree": {
        "strengths": [
            "Scale: large follower base drives algorithmic amplification",
            "Strong enterprise client case studies",
            "SAP and Salesforce ecosystem content",
        ],
        "weaknesses": [
            "Content is volume-focused, not quality-focused",
            "Generic AI content lacking technical depth",
            "Weak startup/founder targeting",
        ],
        "content_gaps": [
            "No agentic AI differentiation",
            "Weak product engineering positioning vs pure IT services framing",
            "Limited HRTech vertical content",
        ],
        "posting_frequency": "20-30x/week",
        "top_formats": ["Press releases", "Awards", "Generic AI posts"],
    },
}

AZILEN_OPPORTUNITIES = [
    {
        "opportunity": "Own the Agentic AI for Enterprise positioning",
        "rationale": "No mid-market IT services firm has claimed this space. EPAM and Thoughtworks talk about AI broadly. Azilen can own 'Agentic AI that ships to production.'",
        "content_action": "Publish a 10-part series: 'The Enterprise Agentic AI Playbook'",
        "effort": "HIGH",
        "potential_impact": "VERY HIGH",
    },
    {
        "opportunity": "HRTech AI thought leadership gap",
        "rationale": "CHRO and HR Technology buyer has almost no technical vendor serving their LinkedIn feed. Competitors ignore this buyer. Azilen has a background verification platform.",
        "content_action": "Bi-weekly HRTech AI post targeting CHRO persona",
        "effort": "LOW",
        "potential_impact": "HIGH",
    },
    {
        "opportunity": "AI failure analysis content",
        "rationale": "Everyone publishes success stories. No competitor is analyzing WHY enterprise AI projects fail. This is the #1 fear of every CTO spending on AI.",
        "content_action": "'AI Project Post-Mortems' content series – what failed, why, how to avoid",
        "effort": "MEDIUM",
        "potential_impact": "VERY HIGH",
    },
    {
        "opportunity": "Manufacturing AI content vacuum",
        "rationale": "Manufacturing sector is massively underserved on LinkedIn. Competitors focus on financial services and healthcare. Azilen can own manufacturing AI positioning.",
        "content_action": "Monthly 'Manufacturing AI Benchmark' report or data post",
        "effort": "MEDIUM",
        "potential_impact": "HIGH",
    },
    {
        "opportunity": "Startup/SaaS founder targeting",
        "rationale": "Large competitors (Accenture, Deloitte) cannot credibly speak to Series B startups. Azilen's agility and engineering depth is a perfect fit. No competitor is creating content for this buyer.",
        "content_action": "Bi-weekly 'Engineering for Founders' post targeting startup CTOs",
        "effort": "LOW",
        "potential_impact": "MEDIUM",
    },
    {
        "opportunity": "Data-backed benchmark content",
        "rationale": "Original research and benchmarks generate 3x more shares and backlinks than opinion pieces. No mid-market competitor is publishing original LinkedIn research.",
        "content_action": "Quarterly 'Enterprise AI Benchmark Report' published as LinkedIn Document",
        "effort": "HIGH",
        "potential_impact": "VERY HIGH",
    },
]


def get_competitor_insights() -> dict[str, Any]:
    return {
        "profiles": COMPETITOR_PROFILES,
        "azilen_opportunities": AZILEN_OPPORTUNITIES,
        "competitive_summary": {
            "highest_frequency_competitor": "LTIMindtree (20-30x/week)",
            "strongest_thought_leadership": "Thoughtworks",
            "biggest_content_gap_across_all": "Agentic AI production architecture",
            "underserved_buyer_persona": "CHRO / HR Technology Leaders",
            "underserved_vertical": "Manufacturing AI",
            "azilen_unique_positioning": (
                "The only mid-market engineering firm that combines Agentic AI production deployment "
                "expertise with deep vertical specialization in HRTech, FinTech, and Manufacturing"
            ),
        },
        "weekly_recommendation": (
            "This week: Focus on Agentic AI content. "
            "EPAM, Nagarro and GlobalLogic are all silent on agentic AI architecture. "
            "One well-structured technical post this week will face zero competition."
        ),
    }
