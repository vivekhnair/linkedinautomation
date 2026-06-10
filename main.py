#!/usr/bin/env python3
"""
Azilen Technologies – LinkedIn Autonomous Growth Operating System

Usage:
    python main.py daily              # Full 17-section daily report
    python main.py weekly             # 7-day content calendar
    python main.py analyze            # Performance analysis only
    python main.py monthly            # Monthly analysis report
    python main.py post --topic "..."  # Generate post for specific topic
    python main.py post --topic "..." --pillar "Agentic AI" --buyer "CTO"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from engines.data_analyzer import analyze_performance, format_analysis_report
from engines.trend_monitor import get_current_trends
from engines.competitor_analyzer import get_competitor_insights
from engines.visual_prompter import generate_visual_prompts
from engines.scheduler import generate_content_calendar
from engines.lead_engine import get_lead_recommendations
from engines.content_generator import (
    generate_full_report,
    generate_post_only,
    generate_monthly_analysis,
)


OUTPUTS_DIR = Path(__file__).parent / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)


def _save_output(content: str, prefix: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUTS_DIR / f"{prefix}_{timestamp}.md"
    filename.write_text(content, encoding="utf-8")
    return filename


def _print_header(title: str) -> None:
    print("\n" + "═" * 70)
    print(f"  {title}")
    print("═" * 70 + "\n")


def cmd_analyze(_args: argparse.Namespace) -> None:
    _print_header("AZILEN TECHNOLOGIES – LINKEDIN PERFORMANCE ANALYSIS")
    print("  Loading and analyzing 90-day Zoho Social data...\n")

    data = analyze_performance()
    report = format_analysis_report(data)
    print(report)

    saved = _save_output(report, "analysis")
    print(f"\n  Report saved → {saved}")


def cmd_daily(args: argparse.Namespace) -> None:
    _print_header("AZILEN LINKEDIN GROWTH OS – DAILY EXECUTION")
    print("  Initializing all engines...\n")

    print("  [1/6] Loading performance data...")
    performance_data = analyze_performance()

    print("  [2/6] Scanning industry trends...")
    trend_data = get_current_trends()

    print("  [3/6] Running competitor intelligence...")
    competitor_insights = get_competitor_insights()

    topic = getattr(args, "topic", None)
    primary_trend = trend_data["all_trends"][trend_data["primary_trend_focus"]]
    effective_topic = topic or primary_trend["signals"][0].split(":")[0].strip()

    print(f"  [4/6] Generating visual prompts for: {effective_topic}")
    visual_prompts = generate_visual_prompts(effective_topic)

    print("  [5/6] Building content calendar...")
    calendar_data = generate_content_calendar(performance_data)

    print("  [6/6] Generating lead recommendations...")
    lead_data = get_lead_recommendations(performance_data)

    print("\n" + "─" * 70)
    print("  GENERATING 17-SECTION LINKEDIN MARKETING REPORT")
    print("─" * 70 + "\n")

    report = generate_full_report(
        trend_data=trend_data,
        performance_data=performance_data,
        competitor_insights=competitor_insights,
        topic=topic,
        visual_prompts=visual_prompts,
        lead_data=lead_data,
        calendar_data=calendar_data,
    )

    saved = _save_output(report, "daily_report")
    print(f"\n{'─'*70}")
    print(f"  Full report saved → {saved}")
    print("─" * 70)

    # Print calendar separately for quick reference
    print("\n  QUICK REFERENCE: THIS WEEK'S CALENDAR")
    print("  " + "─" * 60)
    for entry in calendar_data["calendar"]:
        priority_marker = "★" if entry["priority"] == "HIGH" else " "
        print(
            f"  {priority_marker} {entry['day'][:3]} {entry['date']} {entry['time_ist']} IST | "
            f"{entry['content_pillar']:<25} | {entry['format']:<8} | {entry['goal']}"
        )
    print()


def cmd_weekly(args: argparse.Namespace) -> None:
    _print_header("AZILEN – 7-DAY CONTENT CALENDAR")

    print("  Loading performance data...")
    performance_data = analyze_performance()

    print("  Building calendar...\n")
    calendar_data = generate_content_calendar(performance_data)

    output_lines = [
        "# AZILEN TECHNOLOGIES – 7-DAY LINKEDIN CONTENT CALENDAR",
        f"**Week of:** {calendar_data['week_of']}",
        f"**Total Posts Planned:** {calendar_data['total_posts_planned']}",
        "",
        "| Day | Date | Time IST | Content Pillar | Format | Goal | CTA Type |",
        "|-----|------|----------|----------------|--------|------|----------|",
    ]

    for entry in calendar_data["calendar"]:
        output_lines.append(
            f"| {entry['day'][:3]} | {entry['date']} | {entry['time_ist']} | "
            f"{entry['content_pillar']} | {entry['format']} | {entry['goal']} | {entry['cta_type'][:40]}... |"
        )

    output_lines += [
        "",
        "## ZOHO SOCIAL PUBLISHING INSTRUCTIONS",
    ]
    for instruction in calendar_data["zoho_social_instructions"]:
        output_lines.append(f"- {instruction}")

    output_lines += [
        "",
        "## PERFORMANCE INSIGHTS APPLIED",
        f"- Best performing format prioritized: **{calendar_data['performance_insights_applied']['best_format_used']}**",
        f"- Highest engagement day: **{calendar_data['performance_insights_applied']['best_day_highlighted']}**",
    ]

    output = "\n".join(output_lines)
    print(output)

    saved = _save_output(output, "weekly_calendar")
    print(f"\n  Calendar saved → {saved}")


def cmd_monthly(args: argparse.Namespace) -> None:
    _print_header("AZILEN – MONTHLY LINKEDIN PERFORMANCE REPORT")

    print("  Loading performance data...")
    performance_data = analyze_performance()

    print("  Generating monthly analysis via Claude API...\n")
    report = generate_monthly_analysis(performance_data)

    print(report)
    saved = _save_output(report, "monthly_report")
    print(f"\n  Monthly report saved → {saved}")


def cmd_post(args: argparse.Namespace) -> None:
    topic = args.topic
    pillar = getattr(args, "pillar", "Agentic AI")
    buyer = getattr(args, "buyer", "CTO")
    funnel = getattr(args, "funnel", "Awareness")
    fmt = getattr(args, "format", "TEXT")

    _print_header(f"GENERATING POST: {topic}")
    print(f"  Pillar: {pillar} | Buyer: {buyer} | Funnel: {funnel} | Format: {fmt}\n")

    content = generate_post_only(
        topic=topic,
        pillar=pillar,
        post_format=fmt,
        buyer_persona=buyer,
        funnel_stage=funnel,
    )

    print(content)
    saved = _save_output(content, f"post_{topic[:30].replace(' ', '_')}")
    print(f"\n  Post saved → {saved}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Azilen LinkedIn Autonomous Growth Operating System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("analyze", help="Analyze 90-day performance data")
    subparsers.add_parser("monthly", help="Generate monthly analysis report")
    subparsers.add_parser("weekly", help="Generate 7-day content calendar")

    daily_parser = subparsers.add_parser("daily", help="Generate full 17-section daily report")
    daily_parser.add_argument("--topic", type=str, help="Override topic for today's post")

    post_parser = subparsers.add_parser("post", help="Generate content for a specific topic")
    post_parser.add_argument("--topic", type=str, required=True, help="Post topic")
    post_parser.add_argument("--pillar", type=str, default="Agentic AI", help="Content pillar")
    post_parser.add_argument("--buyer", type=str, default="CTO", help="Target buyer persona")
    post_parser.add_argument("--funnel", type=str, default="Awareness", help="Funnel stage")
    post_parser.add_argument("--format", type=str, default="TEXT", help="Post format (TEXT/IMAGE/CAROUSEL/VIDEO)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "analyze": cmd_analyze,
        "daily": cmd_daily,
        "weekly": cmd_weekly,
        "monthly": cmd_monthly,
        "post": cmd_post,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
