"""Content generation engine powered by OpenAI API."""

from __future__ import annotations

import json
import os
from datetime import date
from typing import Any

from openai import OpenAI

from config import AZILEN_SYSTEM_PROMPT, CONTENT_PILLARS, COMPETITORS


def _get_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set.")
    return OpenAI(api_key=api_key)


def generate_full_report(
    trend_data: dict[str, Any],
    performance_data: dict[str, Any],
    competitor_insights: dict[str, Any],
    topic: str | None = None,
    visual_prompts: dict[str, Any] | None = None,
    lead_data: dict[str, Any] | None = None,
    calendar_data: dict[str, Any] | None = None,
) -> str:
    client = _get_client()
    perf_summary = performance_data.get("summary", {})
    insights = performance_data.get("insights", [])
    opportunities = competitor_insights.get("azilen_opportunities", [])[:3]
    trend_signals = []
    for cat in list(trend_data.get("all_trends", {}).values())[:3]:
        trend_signals.extend(cat["signals"][:2])
    today = date.today()
    topic_context = f"Focus topic for today: {topic}" if topic else "Generate the highest-potential topic for today based on trends and data."
    prompt = f"""
Today: {today.strftime('%A, %B %d, %Y')}
{topic_context}
PERFORMANCE: {perf_summary.get('latest_followers',0):,} followers | {perf_summary.get('total_posts_90d',0)} posts ({perf_summary.get('posting_frequency_per_week',0)}x/week) | Engagement: {perf_summary.get('avg_engagement_rate_pct','0%')} | Trend: {perf_summary.get('impression_trend_30d_pct',0):+.1f}%
INSIGHTS: {chr(10).join(insights[:3])}
TRENDS: {chr(10).join(f'- {s}' for s in trend_signals)}
COMPETITOR GAPS: {chr(10).join(f'- {o["opportunity"]}' for o in opportunities)}
Generate complete 17-Section LinkedIn Marketing Report.
SECTION 1: EXECUTIVE SUMMARY
SECTION 2: COMPETITOR ANALYSIS
SECTION 3: INDUSTRY TREND ANALYSIS
SECTION 4: CONTENT OPPORTUNITIES (5 ideas)
SECTION 5: 7-DAY CONTENT CALENDAR
SECTION 6: TODAY'S HIGHEST POTENTIAL POST (800+ chars)
SECTION 7: POST CAPTION VARIATIONS (Long/Medium/Short + 5 headlines + 5 hooks + 5 CTAs)
SECTION 8: HASHTAG STRATEGY
SECTION 9: IMAGE GENERATION PROMPTS
SECTION 10: CAROUSEL OUTLINE
SECTION 11: VIDEO CONCEPT
SECTION 12: EMPLOYEE ADVOCACY VERSIONS
SECTION 13: PUBLISHING RECOMMENDATION
SECTION 14: EXPECTED PERFORMANCE
SECTION 15: LEAD GENERATION RECOMMENDATIONS
SECTION 16: OPTIMIZATION RECOMMENDATIONS
SECTION 17: ACTIONS BEFORE NEXT POST"""
    stream = client.chat.completions.create(model="gpt-4o", max_tokens=8000,
        messages=[{"role":"system","content":AZILEN_SYSTEM_PROMPT},{"role":"user","content":prompt}], stream=True)
    full_response = ""
    for chunk in stream:
        full_response += chunk.choices[0].delta.content or ""
    return full_response


def generate_post_only(topic: str, pillar: str, post_format: str = "TEXT", buyer_persona: str = "CTO", funnel_stage: str = "Awareness") -> str:
    client = _get_client()
    prompt = f"""Generate a high-converting LinkedIn post for Azilen Technologies.
TOPIC: {topic}
CONTENT PILLAR: {pillar}
FORMAT: {post_format}
TARGET BUYER: {buyer_persona}
FUNNEL STAGE: {funnel_stage}
Deliver:
1. LONG POST (1200-1500 chars)
2. MEDIUM POST (700-900 chars)
3. SHORT POST (250-350 chars)
4. 5 headline options
5. 3 CTA variations
6. 10 hashtags
Rules: Strong hook, no cliches, data-backed, enterprise-focused, ONE clear CTA."""
    response = client.chat.completions.create(model="gpt-4o", max_tokens=3000,
        messages=[{"role":"system","content":AZILEN_SYSTEM_PROMPT},{"role":"user","content":prompt}])
    return response.choices[0].message.content


def generate_mention_response(mention_text: str, mention_context: str = "") -> str:
    client = _get_client()
    prompt = f"""Someone mentioned Azilen Technologies on LinkedIn. Generate the ideal strategic response.
MENTION: {mention_text}
CONTEXT: {mention_context}
Deliver:
1. RECOMMENDED RESPONSE (2-4 lines, professional, adds value)
2. REPOST CAPTION (if worth reposting)
3. FOLLOW-UP STRATEGY
4. LEAD POTENTIAL: HIGH/MEDIUM/LOW with reason
5. SUGGESTED NEXT ACTION (within 24 hours)"""
    response = client.chat.completions.create(model="gpt-4o", max_tokens=1000,
        messages=[{"role":"system","content":AZILEN_SYSTEM_PROMPT},{"role":"user","content":prompt}])
    return response.choices[0].message.content


def generate_comment_response(post_text: str, comment_text: str, commenter_title: str = "") -> str:
    client = _get_client()
    prompt = f"""Someone commented on an Azilen LinkedIn post. Generate the ideal reply.
ORIGINAL POST: {post_text}
COMMENT: {comment_text}
COMMENTER: {commenter_title or 'Unknown'}
Deliver:
1. BEST REPLY (2-3 lines, human, adds value)
2. FOLLOW-UP QUESTION (optional)
3. LEAD SCORE: HOT/WARM/COLD
4. RECOMMENDED ACTION"""
    response = client.chat.completions.create(model="gpt-4o", max_tokens=600,
        messages=[{"role":"system","content":AZILEN_SYSTEM_PROMPT},{"role":"user","content":prompt}])
    return response.choices[0].message.content


def generate_audience_growth_plan(performance_data: dict[str, Any]) -> str:
    client = _get_client()
    s = performance_data.get("summary", {})
    prompt = f"""Create a 30-day audience growth sprint plan for Azilen Technologies LinkedIn.
CURRENT: {s.get('latest_followers',0):,} followers | {s.get('posting_frequency_per_week',0)}x/week | {s.get('avg_engagement_rate_pct','0%')} engagement | {s.get('impression_trend_30d_pct',0):+.1f}% trend
TARGET: 110,000 followers in 30 days
Deliver:
WEEK 1: Foundation (daily actions, content types, engagement tactics, employee advocacy)
WEEK 2: Amplification (viral tactics, collaborations, hashtag campaigns, algorithm hacks)
WEEK 3: Conversion (lead magnets, CTA optimization, profile optimization)
WEEK 4: Compound Growth (repurposing, community, cross-promotion)
DAILY HABITS (15 min/day): 5 actions that compound
FOLLOWER GROWTH LEVERS: ranked by impact with expected gains
CONTENT THAT ATTRACTS FOLLOWERS: what makes people click Follow"""
    response = client.chat.completions.create(model="gpt-4o", max_tokens=3000,
        messages=[{"role":"system","content":AZILEN_SYSTEM_PROMPT},{"role":"user","content":prompt}])
    return response.choices[0].message.content


def generate_monthly_analysis(performance_data: dict[str, Any], prev_month_data: dict[str, Any] | None = None) -> str:
    client = _get_client()
    s = performance_data.get("summary", {})
    prompt = f"""Monthly LinkedIn Analysis for Azilen Technologies.
DATA: {json.dumps(s, indent=2)}
INSIGHTS: {chr(10).join(performance_data.get('insights',[]))}
TOP POSTS: {json.dumps(performance_data.get('top_performing_posts',[])[:5], indent=2, default=str)}
WORST: {json.dumps(performance_data.get('worst_performing_posts',[])[:3], indent=2, default=str)}
BY TYPE: {json.dumps(performance_data.get('performance_by_type',[]), indent=2)}
Deliver complete monthly report: KPI dashboard, top/worst post analysis, content gaps, competitor opportunities, follower growth, engagement quality, lead results, next month strategy, predicted impact. Brutally honest. CMO reporting to board."""
    response = client.chat.completions.create(model="gpt-4o", max_tokens=5000,
        messages=[{"role":"system","content":AZILEN_SYSTEM_PROMPT},{"role":"user","content":prompt}])
    return response.choices[0].message.content


def _summarize_calendar(calendar_data: dict[str, Any]) -> str:
    cal = calendar_data.get("calendar", [])
    return "\n".join(f"{e['day']} {e['date']} {e['time_ist']} IST – {e['content_pillar']} ({e['format']})" for e in cal[:8])
