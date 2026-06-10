"""Monitors industry trends and surfaces high-signal content opportunities."""

from __future__ import annotations

from datetime import date
from typing import Any


TREND_CATEGORIES = {
    "agentic_ai": {
        "label": "Agentic AI",
        "signals": [
            "Multi-agent orchestration replacing single-model pipelines",
            "OpenAI Agents SDK and Anthropic's Claude for autonomous workflows",
            "Enterprises deploying AI agents for end-to-end business process automation",
            "Agentic RAG replacing static retrieval systems",
            "Tool-use and function-calling becoming table stakes for enterprise AI",
            "LLM-as-judge evaluation patterns gaining traction",
            "Agent memory architectures (episodic, semantic, procedural) in production",
        ],
        "buyer_relevance": "CTO, Head of AI, VP Engineering",
        "urgency": "HIGH",
        "search_queries": [
            "agentic AI enterprise 2026",
            "multi-agent systems production deployment",
            "OpenAI agents enterprise adoption",
        ],
    },
    "enterprise_ai_adoption": {
        "label": "Enterprise AI Adoption",
        "signals": [
            "Gartner: 40% of enterprises will use AI agents in production by end of 2026",
            "CIOs shifting from AI experimentation to AI portfolio management",
            "AI ROI measurement becoming board-level agenda item",
            "AI governance frameworks becoming mandatory in regulated industries",
            "Shadow AI becoming enterprise risk management priority",
            "RAG + fine-tuning hybrid approaches dominating enterprise deployments",
            "AI integration with ERP (SAP, Oracle) accelerating",
        ],
        "buyer_relevance": "CIO, CTO, CDO, Transformation Leaders",
        "urgency": "HIGH",
        "search_queries": [
            "enterprise AI adoption 2026 statistics",
            "CIO AI investment priorities 2026",
            "AI ROI enterprise case studies",
        ],
    },
    "product_engineering": {
        "label": "Product Engineering",
        "signals": [
            "Platform engineering teams replacing siloed DevOps",
            "AI-assisted code generation reducing development cycles by 40-60%",
            "Internal Developer Platforms (IDPs) becoming standard",
            "SaaS platform engineering for multi-tenancy and scale",
            "Shift from feature factories to outcome-driven product teams",
            "FinOps integration with platform engineering",
        ],
        "buyer_relevance": "VP Engineering, VP Product, Head of Engineering",
        "urgency": "MEDIUM",
        "search_queries": [
            "platform engineering trends 2026",
            "AI-assisted development productivity",
            "internal developer platform adoption",
        ],
    },
    "data_engineering": {
        "label": "Data Engineering",
        "signals": [
            "Data mesh architecture implementations scaling beyond early adopters",
            "Real-time data pipelines replacing batch for AI inference",
            "Data lakehouse replacing pure data warehouse architectures",
            "Vector databases becoming core enterprise data infrastructure",
            "Streaming analytics with Apache Kafka + Flink in production",
            "Data contracts becoming engineering standard for data quality",
        ],
        "buyer_relevance": "Head of Data, CTO, VP Engineering",
        "urgency": "MEDIUM",
        "search_queries": [
            "data engineering trends 2026",
            "vector database enterprise adoption",
            "data mesh implementation challenges",
        ],
    },
    "hrtech": {
        "label": "HRTech",
        "signals": [
            "AI-powered talent intelligence replacing traditional ATS",
            "Skills-based hiring frameworks replacing degree-based hiring",
            "Agentic AI for employee onboarding automation",
            "Background verification automation with AI reducing time-to-hire",
            "HR analytics predicting attrition with 80%+ accuracy",
            "Workforce planning AI becoming strategic CHRO tool",
        ],
        "buyer_relevance": "CHRO, HR Technology Leaders",
        "urgency": "MEDIUM",
        "search_queries": [
            "HRTech AI trends 2026",
            "AI talent intelligence platforms",
            "background verification automation",
        ],
    },
    "cloud_modernization": {
        "label": "Cloud & Infrastructure",
        "signals": [
            "Cloud repatriation trend: 30% of workloads moving back to private cloud",
            "FinOps becoming mandatory as cloud costs exceed projections",
            "Kubernetes 2.0 patterns: GitOps, service mesh, eBPF networking",
            "Multi-cloud orchestration replacing single-cloud lock-in",
            "Serverless AI inference reducing infrastructure costs by 60%",
            "Edge AI deployments in manufacturing and retail scaling fast",
        ],
        "buyer_relevance": "CTO, VP Engineering, Infrastructure Leaders",
        "urgency": "MEDIUM",
        "search_queries": [
            "cloud modernization trends 2026",
            "FinOps cloud cost optimization",
            "Kubernetes enterprise patterns",
        ],
    },
    "manufacturing_ai": {
        "label": "Manufacturing & Industrial AI",
        "signals": [
            "Predictive maintenance AI reducing downtime by 30-50% in discrete manufacturing",
            "Computer vision quality control replacing manual inspection",
            "Digital twin adoption accelerating in automotive and aerospace",
            "AI-powered supply chain optimization responding to tariff volatility",
            "IIoT data platforms enabling real-time production intelligence",
        ],
        "buyer_relevance": "CTO, VP Technology, Innovation Leaders",
        "urgency": "MEDIUM",
        "search_queries": [
            "manufacturing AI automation 2026",
            "predictive maintenance AI ROI",
            "digital twin enterprise adoption",
        ],
    },
}

CONTENT_OPPORTUNITIES = [
    {
        "title": "Why 73% of Enterprise AI Projects Fail Before Production",
        "pillar": "Enterprise AI",
        "angle": "Azilen's engineering-first approach vs consulting-first competitors",
        "buyer": "CTO, VP Engineering",
        "funnel_stage": "Awareness",
        "format": "TEXT",
        "why_now": "AI project failure rates dominating CTO conversations",
    },
    {
        "title": "The Agentic AI Architecture That Actually Scales to Enterprise",
        "pillar": "Agentic AI",
        "angle": "Technical deep-dive: multi-agent orchestration patterns Azilen deploys",
        "buyer": "Head of AI, CTO",
        "funnel_stage": "Consideration",
        "format": "CAROUSEL",
        "why_now": "Every competitor is talking about agents; few are showing architecture",
    },
    {
        "title": "HRTech's Dirty Secret: Why Your ATS Is Costing You $2.3M/Year",
        "pillar": "HRTech",
        "angle": "Cost of manual background verification + outdated ATS quantified",
        "buyer": "CHRO, HR Technology Leaders",
        "funnel_stage": "Problem Aware",
        "format": "IMAGE",
        "why_now": "Economic pressure on HR budgets; CFO scrutiny of headcount costs",
    },
    {
        "title": "From 18 Months to 4 Months: How We Rebuilt a Core Banking Platform",
        "pillar": "Product Engineering",
        "angle": "Case study angle on accelerated platform engineering",
        "buyer": "CTO, VP Product, FinTech Leaders",
        "funnel_stage": "Consideration",
        "format": "DOCUMENT",
        "why_now": "FinTech modernization budgets accelerating in 2026",
    },
    {
        "title": "The Data Infrastructure Every Enterprise AI Stack Needs (But Doesn't Have)",
        "pillar": "Data Engineering",
        "angle": "Real-time data pipelines as AI enablement infrastructure",
        "buyer": "Head of Data, CTO",
        "funnel_stage": "Education",
        "format": "CAROUSEL",
        "why_now": "Data readiness becoming the #1 AI blocker cited by CIOs",
    },
]


def get_current_trends() -> dict[str, Any]:
    today = date.today()
    week_number = today.isocalendar()[1]

    # Rotate focus areas by week to ensure content variety
    priority_order = list(TREND_CATEGORIES.keys())
    week_priorities = priority_order[week_number % len(priority_order) :] + priority_order[: week_number % len(priority_order)]

    return {
        "as_of_date": today.isoformat(),
        "week_number": week_number,
        "primary_trend_focus": week_priorities[0],
        "secondary_trend_focus": week_priorities[1],
        "all_trends": TREND_CATEGORIES,
        "top_content_opportunities": CONTENT_OPPORTUNITIES,
        "high_urgency_trends": [
            k for k, v in TREND_CATEGORIES.items() if v["urgency"] == "HIGH"
        ],
        "recommended_topics_this_week": [
            TREND_CATEGORIES[week_priorities[0]]["label"],
            TREND_CATEGORIES[week_priorities[1]]["label"],
            TREND_CATEGORIES[week_priorities[2]]["label"],
        ],
        "viral_content_signals": [
            "LinkedIn algorithm favoring posts with 5+ comments in first 60 minutes",
            "Carousel posts getting 3x more dwell time than single images",
            "Text posts with data points outperforming images among C-suite",
            "Posts mentioning specific companies/products getting 2x more engagement",
            "Controversial 'hot take' openings driving 40% more comments",
        ],
    }
