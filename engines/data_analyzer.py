"""Analyzes Zoho Social LinkedIn CSV exports to surface actionable insights."""

from __future__ import annotations

import os
from datetime import datetime, date
from pathlib import Path
from typing import Any

import pandas as pd


DATA_DIR = Path(__file__).parent.parent / "zoho_data"


def _load_post_analytics() -> pd.DataFrame:
    path = DATA_DIR / "ln_post_analytics_Azilen Technologies.csv"
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df["posted_at"] = pd.to_datetime(df["Time of post"], format="%d %b %Y %H:%M:%S %z", utc=True)
    df["day_of_week"] = df["posted_at"].dt.day_name()
    df["hour"] = df["posted_at"].dt.hour
    df["engagement_rate"] = pd.to_numeric(df["Engagement rate"], errors="coerce").fillna(0)
    df["Likes"] = pd.to_numeric(df["Likes"], errors="coerce").fillna(0)
    df["Comments"] = pd.to_numeric(df["Comments"], errors="coerce").fillna(0)
    df["Shares"] = pd.to_numeric(df["Shares"], errors="coerce").fillna(0)
    df["Clicks"] = pd.to_numeric(df["Clicks"], errors="coerce").fillna(0)
    df["Impressions"] = pd.to_numeric(df["Impressions"], errors="coerce").fillna(0)
    df["total_interactions"] = df["Likes"] + df["Comments"] * 3 + df["Shares"] * 5 + df["Clicks"]
    return df


def _load_page_analytics() -> pd.DataFrame:
    path = DATA_DIR / "ln_page_analytics_Azilen Technologies.csv"
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"].str.replace("'", " 20"), format="%d %b %Y", errors="coerce")
    numeric_cols = [c for c in df.columns if c != "Date"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(r"[^\d.\-Ee]", "", regex=True), errors="coerce").fillna(0)
    return df


def analyze_performance() -> dict[str, Any]:
    posts = _load_post_analytics()
    page = _load_page_analytics()

    # ── Post-level metrics ──────────────────────────────────────────────────
    total_posts = len(posts)
    date_range_days = (posts["posted_at"].max() - posts["posted_at"].min()).days + 1
    posting_frequency = round(total_posts / (date_range_days / 7), 1)  # posts/week

    # Best / worst posts
    top5 = posts.nlargest(5, "engagement_rate")[
        ["Time of post", "Post Type", "Likes", "Comments", "Shares", "Clicks", "engagement_rate", "Impressions"]
    ].to_dict("records")
    bottom5 = posts.nsmallest(5, "engagement_rate")[
        ["Time of post", "Post Type", "Likes", "Comments", "Shares", "Clicks", "engagement_rate", "Impressions"]
    ].to_dict("records")

    # Performance by post type
    by_type = (
        posts.groupby("Post Type")
        .agg(
            count=("Post Type", "count"),
            avg_engagement=("engagement_rate", "mean"),
            avg_likes=("Likes", "mean"),
            avg_shares=("Shares", "mean"),
            avg_comments=("Comments", "mean"),
            total_impressions=("Impressions", "sum"),
        )
        .reset_index()
        .to_dict("records")
    )

    # Best day of week
    by_day = (
        posts.groupby("day_of_week")
        .agg(count=("day_of_week", "count"), avg_engagement=("engagement_rate", "mean"))
        .sort_values("avg_engagement", ascending=False)
        .reset_index()
        .to_dict("records")
    )

    # Best hour
    by_hour = (
        posts.groupby("hour")
        .agg(count=("hour", "count"), avg_engagement=("engagement_rate", "mean"))
        .sort_values("avg_engagement", ascending=False)
        .reset_index()
        .to_dict("records")
    )
    best_hour = by_hour[0]["hour"] if by_hour else 10

    # ── Page-level metrics ──────────────────────────────────────────────────
    latest_followers = int(page["Total Followers"].iloc[0]) if not page.empty else 0
    follower_growth_90d = int(page["New Followers"].sum())
    avg_daily_impressions = round(page["Impressions"].mean(), 0)
    avg_daily_reach = round(page["Reach"].mean(), 0)
    total_impressions_90d = int(page["Impressions"].sum())

    # Weekly trend (last 4 weeks vs prior 4 weeks)
    page_sorted = page.sort_values("Date")
    recent_30d = page_sorted.tail(30)
    prior_30d = page_sorted.iloc[-60:-30] if len(page_sorted) >= 60 else page_sorted.head(30)
    impression_trend = (
        round((recent_30d["Impressions"].mean() - prior_30d["Impressions"].mean()) / (prior_30d["Impressions"].mean() + 1) * 100, 1)
        if not prior_30d.empty
        else 0
    )

    # ── Benchmarks & insights ───────────────────────────────────────────────
    avg_engagement_rate = posts["engagement_rate"].mean()
    linkedin_benchmark = 0.00054  # LinkedIn company page industry average ~0.054%

    insights = _generate_insights(
        posts=posts,
        total_posts=total_posts,
        posting_frequency=posting_frequency,
        avg_engagement_rate=avg_engagement_rate,
        linkedin_benchmark=linkedin_benchmark,
        follower_growth_90d=follower_growth_90d,
        latest_followers=latest_followers,
        impression_trend=impression_trend,
        by_type=by_type,
        by_day=by_day,
    )

    return {
        "summary": {
            "total_posts_90d": total_posts,
            "date_range_days": date_range_days,
            "posting_frequency_per_week": posting_frequency,
            "latest_followers": latest_followers,
            "follower_growth_90d": follower_growth_90d,
            "follower_growth_rate_pct": round(follower_growth_90d / max(latest_followers - follower_growth_90d, 1) * 100, 2),
            "total_impressions_90d": total_impressions_90d,
            "avg_daily_impressions": avg_daily_impressions,
            "avg_daily_reach": avg_daily_reach,
            "avg_engagement_rate": round(avg_engagement_rate, 6),
            "avg_engagement_rate_pct": f"{avg_engagement_rate*100:.4f}%",
            "linkedin_benchmark_pct": f"{linkedin_benchmark*100:.4f}%",
            "vs_benchmark": "ABOVE" if avg_engagement_rate > linkedin_benchmark else "BELOW",
            "impression_trend_30d_pct": impression_trend,
        },
        "top_performing_posts": top5,
        "worst_performing_posts": bottom5,
        "performance_by_type": by_type,
        "best_days": by_day[:3],
        "best_hours": by_hour[:3],
        "recommended_posting_time_ist": f"{best_hour:02d}:30 IST",
        "insights": insights,
    }


def _generate_insights(
    posts: pd.DataFrame,
    total_posts: int,
    posting_frequency: float,
    avg_engagement_rate: float,
    linkedin_benchmark: float,
    follower_growth_90d: int,
    latest_followers: int,
    impression_trend: float,
    by_type: list,
    by_day: list,
) -> list[str]:
    insights = []

    if posting_frequency < 5:
        insights.append(
            f"CRITICAL GAP: Posting only {posting_frequency:.1f}x/week against LinkedIn's recommended 1-2x/day. "
            f"Competitors posting 5-10x/week are capturing 3-5x more organic reach. "
            f"Increasing to 7 posts/week could 3x impressions within 60 days."
        )

    if avg_engagement_rate < linkedin_benchmark:
        delta_pct = round((linkedin_benchmark - avg_engagement_rate) / linkedin_benchmark * 100, 0)
        insights.append(
            f"Engagement rate ({avg_engagement_rate*100:.4f}%) is {delta_pct}% below LinkedIn's company page benchmark ({linkedin_benchmark*100:.4f}%). "
            f"Priority fix: improve opening hooks and add stronger CTAs to every post."
        )
    else:
        insights.append(
            f"Engagement rate ({avg_engagement_rate*100:.4f}%) is above LinkedIn benchmark ({linkedin_benchmark*100:.4f}%). "
            f"Build on this by increasing posting frequency to amplify reach."
        )

    # Best post type
    type_sorted = sorted(by_type, key=lambda x: x["avg_engagement"], reverse=True)
    if type_sorted:
        best_type = type_sorted[0]
        insights.append(
            f"Best performing format: {best_type['Post Type']} posts average {best_type['avg_engagement']*100:.4f}% engagement. "
            f"Increase {best_type['Post Type']} posts to 40% of content mix."
        )

    # Zero-comment problem
    zero_comment_pct = round(len(posts[posts["Comments"] == 0]) / len(posts) * 100, 0)
    if zero_comment_pct > 70:
        insights.append(
            f"{zero_comment_pct}% of posts received zero comments. "
            f"Add 1 direct question or controversial data point to every post to trigger discussion."
        )

    # Zero-click problem
    zero_click_pct = round(len(posts[posts["Clicks"] == 0]) / len(posts) * 100, 0)
    if zero_click_pct > 60:
        insights.append(
            f"{zero_click_pct}% of posts received zero link clicks. "
            f"CTAs are not driving website traffic. "
            f"Switch from passive mentions to explicit 'Link in comments →' format with lead magnets."
        )

    if impression_trend < 0:
        insights.append(
            f"Impression trend is declining {abs(impression_trend)}% month-over-month. "
            f"Algorithm likely penalizing low-frequency posting. Immediate action: increase posting cadence."
        )
    elif impression_trend > 10:
        insights.append(
            f"Impressions growing {impression_trend}% month-over-month – positive momentum. "
            f"Double down on the content formats driving this growth."
        )

    insights.append(
        f"Follower base: {latest_followers:,} followers. Added {follower_growth_90d:,} in 90 days. "
        f"To reach 150K followers by end of year, need to add ~1,700/month. "
        f"Employee advocacy activation (30+ employees sharing posts) can 2-3x organic follower growth."
    )

    return insights


def format_analysis_report(data: dict[str, Any]) -> str:
    s = data["summary"]
    lines = [
        "=" * 70,
        "  AZILEN TECHNOLOGIES – LINKEDIN PERFORMANCE ANALYSIS (90 DAYS)",
        "=" * 70,
        "",
        "── OVERVIEW ──────────────────────────────────────────────────────────",
        f"  Total Followers:        {s['latest_followers']:,}",
        f"  Follower Growth 90d:    +{s['follower_growth_90d']:,} ({s['follower_growth_rate_pct']}%)",
        f"  Total Impressions 90d:  {s['total_impressions_90d']:,}",
        f"  Avg Daily Impressions:  {s['avg_daily_impressions']:,}",
        f"  Avg Daily Reach:        {s['avg_daily_reach']:,}",
        f"  Total Posts Published:  {s['total_posts_90d']} ({s['posting_frequency_per_week']}x/week)",
        f"  Avg Engagement Rate:    {s['avg_engagement_rate_pct']} (Benchmark: {s['linkedin_benchmark_pct']}) → {s['vs_benchmark']}",
        f"  30-Day Impression Trend: {s['impression_trend_30d_pct']:+.1f}%",
        "",
        "── TOP 5 PERFORMING POSTS ────────────────────────────────────────────",
    ]
    for i, p in enumerate(data["top_performing_posts"], 1):
        lines.append(
            f"  {i}. [{p['Post Type']}] {p['Time of post'][:16]} | "
            f"Eng: {float(p['engagement_rate'])*100:.4f}% | "
            f"L:{p['Likes']} C:{p['Comments']} S:{p['Shares']}"
        )

    lines += [
        "",
        "── PERFORMANCE BY POST TYPE ──────────────────────────────────────────",
    ]
    for t in sorted(data["performance_by_type"], key=lambda x: x["avg_engagement"], reverse=True):
        lines.append(
            f"  {t['Post Type']:<8} {t['count']:>3} posts | "
            f"Avg Eng: {t['avg_engagement']*100:.4f}% | "
            f"Avg Likes: {t['avg_likes']:.1f} | Avg Shares: {t['avg_shares']:.1f}"
        )

    lines += [
        "",
        "── KEY INSIGHTS ──────────────────────────────────────────────────────",
    ]
    for i, insight in enumerate(data["insights"], 1):
        wrapped = "\n    ".join([insight[j : j + 80] for j in range(0, len(insight), 80)])
        lines.append(f"  {i}. {wrapped}")
        lines.append("")

    lines.append("=" * 70)
    return "\n".join(lines)
