"""Content calendar and publishing recommendation engine."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from config import CONTENT_PILLARS, CONTENT_DISTRIBUTION, PUBLISHING


# Optimal IST posting times based on LinkedIn algorithm patterns for enterprise audience
OPTIMAL_TIMES = {
    "Monday":    ["10:00", "17:30"],
    "Tuesday":   ["09:30", "17:00"],
    "Wednesday": ["10:00", "12:00"],
    "Thursday":  ["09:30", "17:30"],
    "Friday":    ["10:00", "15:00"],
}

WEEKLY_PILLAR_ROTATION = [
    # (pillar, content_type, format, goal)
    ("Agentic AI", "Thought Leadership", "TEXT", "Brand Authority + Leads"),
    ("Enterprise AI", "Educational", "CAROUSEL", "Website Traffic + Leads"),
    ("Product Engineering", "Case Study", "IMAGE", "Leads"),
    ("Data Engineering", "Industry Insights", "TEXT", "Brand Authority"),
    ("HRTech", "Thought Leadership", "IMAGE", "HRTech Leads"),
    ("Cloud Modernization", "Educational", "CAROUSEL", "Cloud Leads"),
    ("Digital Transformation", "Case Study", "TEXT", "Pipeline"),
    ("Manufacturing Technology", "Industry Insights", "IMAGE", "Mfg Leads"),
    ("Generative AI", "Thought Leadership", "VIDEO", "Brand Authority"),
    ("Leadership & Innovation", "Thought Leadership", "TEXT", "Followers"),
]


def generate_content_calendar(
    performance_data: dict[str, Any],
    current_date: date | None = None,
) -> dict[str, Any]:
    if current_date is None:
        current_date = date.today()

    # Find next Monday
    days_until_monday = (7 - current_date.weekday()) % 7
    if days_until_monday == 0:
        week_start = current_date
    else:
        week_start = current_date + timedelta(days=days_until_monday)

    # Use performance data to inform content mix
    best_format = _get_best_format(performance_data)
    best_day = _get_best_day(performance_data)

    calendar = []
    pillar_index = (current_date.isocalendar()[1] * 2) % len(WEEKLY_PILLAR_ROTATION)

    for i in range(5):  # Monday to Friday
        post_date = week_start + timedelta(days=i)
        day_name = post_date.strftime("%A")
        times = OPTIMAL_TIMES.get(day_name, ["10:00", "17:00"])

        # Morning post
        pillar_data = WEEKLY_PILLAR_ROTATION[(pillar_index + i * 2) % len(WEEKLY_PILLAR_ROTATION)]
        morning_post = {
            "day": day_name,
            "date": post_date.isoformat(),
            "time_ist": times[0],
            "content_pillar": pillar_data[0],
            "content_type": pillar_data[1],
            "format": pillar_data[2] if best_format is None else best_format,
            "goal": pillar_data[3],
            "priority": "HIGH" if day_name == best_day else "MEDIUM",
            "cta_type": _get_cta_for_goal(pillar_data[3]),
            "notes": _get_day_notes(day_name, i == 0),
        }
        calendar.append(morning_post)

        # Afternoon post (only Tuesday, Wednesday, Thursday for sustainable pace)
        if day_name in ["Tuesday", "Wednesday", "Thursday"]:
            afternoon_pillar = WEEKLY_PILLAR_ROTATION[(pillar_index + i * 2 + 1) % len(WEEKLY_PILLAR_ROTATION)]
            afternoon_post = {
                "day": day_name,
                "date": post_date.isoformat(),
                "time_ist": times[1],
                "content_pillar": afternoon_pillar[0],
                "content_type": afternoon_pillar[1],
                "format": afternoon_pillar[2],
                "goal": afternoon_pillar[3],
                "priority": "MEDIUM",
                "cta_type": _get_cta_for_goal(afternoon_pillar[3]),
                "notes": "Afternoon slot: engagement-focused, repurpose morning insight",
            }
            calendar.append(afternoon_post)

    return {
        "week_of": week_start.isoformat(),
        "total_posts_planned": len(calendar),
        "calendar": calendar,
        "performance_insights_applied": {
            "best_format_used": best_format or "data-driven per slot",
            "best_day_highlighted": best_day,
        },
        "zoho_social_instructions": _get_zoho_instructions(),
    }


def _get_best_format(performance_data: dict[str, Any]) -> str | None:
    types = performance_data.get("performance_by_type", [])
    if not types:
        return None
    best = max(types, key=lambda x: x.get("avg_engagement", 0))
    return best.get("Post Type")


def _get_best_day(performance_data: dict[str, Any]) -> str:
    days = performance_data.get("best_days", [])
    if days:
        return days[0].get("day_of_week", "Tuesday")
    return "Tuesday"


def _get_cta_for_goal(goal: str) -> str:
    mapping = {
        "Brand Authority + Leads": "Comment with your challenge → DM for consultation",
        "Website Traffic + Leads": "Full guide link in comments → azilen.com",
        "Leads": "Book a 30-min strategy call → [Calendly link]",
        "Brand Authority": "Follow for weekly AI insights → Share if valuable",
        "HRTech Leads": "HRTech assessment → Book discovery call",
        "Cloud Leads": "Cloud readiness assessment → Free consultation",
        "Pipeline": "Case study PDF → link in comments",
        "Mfg Leads": "Manufacturing AI blueprint → Download",
        "Followers": "Follow Azilen for weekly insights",
    }
    for key, cta in mapping.items():
        if key in goal:
            return cta
    return "Follow for more → Share with your network"


def _get_day_notes(day_name: str, is_week_start: bool) -> str:
    notes = {
        "Monday": "Week-setter post: bold prediction or data point. Executives check LinkedIn Monday morning.",
        "Tuesday": "Deep-dive day: best day for carousels and educational content.",
        "Wednesday": "Mid-week: industry insight or case study. High engagement window.",
        "Thursday": "Thought leadership: opinion or hot take. Pre-weekend sharing peak.",
        "Friday": "Lighter content: frameworks, lists, or team culture. Engagement drops Friday PM.",
    }
    return notes.get(day_name, "")


def _get_zoho_instructions() -> list[str]:
    return [
        "Schedule all posts in Zoho Social under Azilen Technologies LinkedIn page",
        "Set timezone to IST (Asia/Kolkata) for all scheduled times",
        "Add UTM parameters to all links: utm_source=linkedin&utm_medium=social&utm_campaign=organic",
        "Enable 'Best Time to Publish' override if Zoho Social suggests a better slot",
        "Tag each post with the appropriate content pillar label for tracking",
        "After publishing: monitor comments for first 60 minutes and respond within 2 hours",
        "Screenshot top-performing posts weekly for monthly performance report",
    ]
