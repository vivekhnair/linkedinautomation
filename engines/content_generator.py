"""Content generation engine powered by Claude API."""

from __future__ import annotations

import json
import os
from datetime import date
from typing import Any

import anthropic

from config import AZILEN_SYSTEM_PROMPT, CONTENT_PILLARS, COMPETITORS


def _get_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY environment variable not set. "
            "Copy .env.example to .env and add your key."
        )
    return anthropic.Anthropic(api_key=api_key)


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
    top_posts = performance_data.get("top_performing_posts", [])[:3]
    insights = performance_data.get("insights", [])
    opportunities = competitor_insights.get("azilen_opportunities", [])[:3]
    trend_signals = []
    for cat in list(trend_data.get("all_trends", {}).values())[:3]:
        trend_signals.extend(cat["signals"][:2])

    today = date.today()
    topic_context = f"Focus topic for today: {topic}" if topic else "Generate the highest-potential topic for today based on trends and data."

    prompt = f"""
Today's date: {today.strftime("%A, %B %d, %Y")}

{topic_context}

=== PERFORMANCE DATA (Last 90 Days) ===
- Followers: {perf_summary.get('latest_followers', 0):,}
- Follower Growth 90d: +{perf_summary.get('follower_growth_90d', 0):,}
- Total Impressions: {perf_summary.get('total_impressions_90d', 0):,}
- Avg Daily Impressions: {perf_summary.get('avg_daily_impressions', 0):,}
- Total Posts: {perf_summary.get('total_posts_90d', 0)} ({perf_summary.get('posting_frequency_per_week', 0)}x/week)
- Avg Engagement Rate: {perf_summary.get('avg_engagement_rate_pct', '0%')} (Benchmark: {perf_summary.get('linkedin_benchmark_pct', '0.054%')}) → {perf_summary.get('vs_benchmark', 'BELOW')}
- Impression Trend 30d: {perf_summary.get('impression_trend_30d_pct', 0):+.1f}%

Key Performance Insights:
{chr(10).join(f'- {i}' for i in insights[:4])}

Top Performing Post Types: {json.dumps([t.get('Post Type') for t in performance_data.get('performance_by_type', [])[:2]], indent=2)}

=== TRENDING SIGNALS ===
{chr(10).join(f'- {s}' for s in trend_signals)}

=== COMPETITOR GAPS ===
{chr(10).join(f'- {o["opportunity"]}: {o["rationale"]}' for o in opportunities)}

=== LEAD GENERATION CONTEXT ===
{json.dumps(lead_data.get('immediate_actions', [])[:3], indent=2) if lead_data else "Focus on driving discovery calls and website visits."}

=== THIS WEEK'S CALENDAR ===
{_summarize_calendar(calendar_data) if calendar_data else "Generate optimal 7-day posting schedule."}

=== VISUAL PROMPTS CONTEXT ===
Topic: {visual_prompts.get('topic', topic or 'Enterprise AI') if visual_prompts else topic or 'Enterprise AI'}

---

Generate a complete LinkedIn Marketing Operating Report with ALL 17 SECTIONS below. Be specific, data-driven, and enterprise-focused. Never be generic.

SECTION 1: EXECUTIVE SUMMARY
(3-4 sentences: current state, biggest opportunity, this week's strategy, expected business impact)

SECTION 2: COMPETITOR ANALYSIS
(What competitors are doing this week, specific content gaps, exact positioning opportunities for Azilen. Name specific competitors.)

SECTION 3: INDUSTRY TREND ANALYSIS
(3-5 high-signal trends with specific data points. What CTOs/CHROs are actually discussing right now. What's becoming urgent.)

SECTION 4: CONTENT OPPORTUNITIES
(5 specific content ideas with: Title, Pillar, Why Now, Target Buyer, Format, Expected Reach/Impact)

SECTION 5: 7-DAY CONTENT CALENDAR (Monday–Friday)
Format each entry as:
DAY | DATE | TIME IST | TOPIC | PILLAR | FORMAT | GOAL | CTA TYPE
(Include 1-2 posts per day. Vary formats. Avoid repetition.)

SECTION 6: TODAY'S HIGHEST POTENTIAL POST
(Full complete LinkedIn post ready to publish. Must include: strong opening hook, curiosity trigger, industry-relevant insight with data, storytelling element, clear business takeaway, CTA. Minimum 800 characters.)

SECTION 7: POST CAPTION VARIATIONS
LONG VERSION (1200-1500 chars):
[full long post]

MEDIUM VERSION (700-900 chars):
[medium post]

SHORT VERSION (250-350 chars):
[short post]

5 HEADLINE OPTIONS:
1.
2.
3.
4.
5.

5 HOOK OPTIONS (opening line only):
1.
2.
3.
4.
5.

5 CTA VARIATIONS:
1.
2.
3.
4.
5.

SECTION 8: HASHTAG STRATEGY
PRIMARY (5 high-volume, brand-aligned):
SECONDARY (10 mid-volume, topic-specific):
NICHE (5 low-volume, high-conversion):
AVOID: [hashtags that look spammy or misaligned]

SECTION 9: IMAGE GENERATION PROMPTS
DALL-E / ChatGPT IMAGE PROMPT:
[detailed prompt]

MIDJOURNEY PROMPT:
[detailed prompt with flags]

ADOBE EXPRESS CONCEPT:
[layout description, colors, typography, elements]

SECTION 10: CAROUSEL OUTLINE (LinkedIn Document Post)
TITLE:
SLIDE 1 (Cover):
SLIDE 2 (Problem):
SLIDE 3 (Context):
SLIDES 4-6 (Framework):
SLIDE 7 (Proof):
SLIDE 8 (Takeaway):
SLIDE 9 (CTA):

SECTION 11: VIDEO CONCEPT (30-60 seconds)
HOOK (0-5 sec):
SETUP (5-15 sec):
CONTENT (15-45 sec):
CTA (45-60 sec):
PRODUCTION NOTES:

SECTION 12: EMPLOYEE ADVOCACY VERSIONS
CEO VERSION:
[post from CEO perspective – strategic, visionary]

CTO VERSION:
[post from CTO perspective – technical depth, architecture]

VP MARKETING VERSION:
[post from VP Marketing perspective – market insights, brand]

SALES LEADER VERSION:
[post from Sales Leader perspective – ROI, client challenges]

RECOMMENDED EMPLOYEE COMMENTS:
[3 specific comments employees can leave on the main post]

SECTION 13: PUBLISHING RECOMMENDATION
Best Publishing Time: [day, time IST, reason]
Format Priority: [1st choice, 2nd choice, why]
Audience Targeting: [specific targeting notes for Zoho Social]
A/B Test Opportunity: [what to test this week]

SECTION 14: EXPECTED PERFORMANCE
Predicted Impressions: [range]
Predicted Engagement Rate: [%]
Predicted Reach: [range]
Predicted Clicks: [range]
Predicted Profile Visits: [range]
Lead Generation Potential: [#]
Confidence Level: [HIGH/MEDIUM/LOW with reason]

SECTION 15: LEAD GENERATION RECOMMENDATIONS
Immediate CTA Action: [specific action]
Lead Magnet Recommendation: [which one, why]
Landing Page: [URL suggestion, what to change]
Follow-up Sequence: [what to do 24-48 hours after post]

SECTION 16: OPTIMIZATION RECOMMENDATIONS
(5 specific, data-backed improvements based on the 90-day performance data above)
1.
2.
3.
4.
5.

SECTION 17: ACTIONS TO IMPLEMENT BEFORE NEXT POST
(Ordered checklist of 5-7 specific actions with owner/tool)
□
□
□
□
□
□
□
"""

    print("  Generating report via Claude API (streaming)...\n")
    full_response = ""

    with client.messages.stream(
        model="claude-opus-4-8",
        max_tokens=8000,
        system=AZILEN_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_response += text

    print("\n")
    return full_response


def generate_post_only(
    topic: str,
    pillar: str,
    post_format: str = "TEXT",
    buyer_persona: str = "CTO",
    funnel_stage: str = "Awareness",
) -> str:
    client = _get_client()

    prompt = f"""
Generate a high-converting LinkedIn post for Azilen Technologies.

TOPIC: {topic}
CONTENT PILLAR: {pillar}
FORMAT: {post_format}
TARGET BUYER: {buyer_persona}
FUNNEL STAGE: {funnel_stage}

Deliver:
1. LONG POST (1200-1500 chars) – ready to publish
2. MEDIUM POST (700-900 chars)
3. SHORT POST (250-350 chars)
4. 5 headline options
5. 3 CTA variations
6. 10 hashtags (mix of volume levels)

Rules:
- Strong opening hook (no "In today's world" or "I'm excited to share")
- Data point or specific insight in first 3 lines
- Build credibility with specifics (not "many companies" but "67% of Fortune 500 CTOs")
- Clear business takeaway
- Enterprise buyer relevance throughout
- End with ONE clear CTA
"""

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=3000,
        system=AZILEN_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def generate_monthly_analysis(
    performance_data: dict[str, Any],
    prev_month_data: dict[str, Any] | None = None,
) -> str:
    client = _get_client()

    perf_summary = performance_data.get("summary", {})
    insights = performance_data.get("insights", [])

    prompt = f"""
Generate a comprehensive Monthly LinkedIn Performance Analysis for Azilen Technologies.

PERFORMANCE DATA:
{json.dumps(perf_summary, indent=2)}

KEY INSIGHTS FROM DATA:
{chr(10).join(insights)}

TOP PERFORMING POSTS:
{json.dumps(performance_data.get('top_performing_posts', [])[:5], indent=2, default=str)}

WORST PERFORMING POSTS:
{json.dumps(performance_data.get('worst_performing_posts', [])[:3], indent=2, default=str)}

PERFORMANCE BY TYPE:
{json.dumps(performance_data.get('performance_by_type', []), indent=2)}

Deliver a complete Monthly Analysis Report with:
1. Executive Dashboard (KPIs vs targets vs LinkedIn benchmarks)
2. Top Performing Posts Analysis (WHY they worked)
3. Worst Performing Posts Analysis (WHY they failed)
4. Content Gap Analysis (what wasn't published that should have been)
5. Competitor Opportunity Analysis (what competitors did that Azilen didn't)
6. Follower Growth Analysis (quality vs quantity, growth trajectory)
7. Engagement Quality Analysis (are the right people engaging?)
8. Lead Generation Results (estimated leads, meetings, pipeline influenced)
9. Next Month Strategy (themes, formats, frequency, KPI targets)
10. Predicted Impact of Recommendations (with specific numbers)

Be brutally honest about what's not working. Think like a CMO reporting to a board.
"""

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=5000,
        system=AZILEN_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def _summarize_calendar(calendar_data: dict[str, Any]) -> str:
    if not calendar_data:
        return ""
    cal = calendar_data.get("calendar", [])
    lines = []
    for entry in cal[:8]:
        lines.append(
            f"{entry['day']} {entry['date']} {entry['time_ist']} IST – "
            f"{entry['content_pillar']} ({entry['format']})"
        )
    return "\n".join(lines)
