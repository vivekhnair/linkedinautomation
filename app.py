"""Azilen LinkedIn Growth OS – Full Web Application"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, render_template_string, request, stream_with_context

load_dotenv()

import sys
sys.path.insert(0, str(Path(__file__).parent))

from engines.data_analyzer import analyze_performance, format_analysis_report
from engines.trend_monitor import get_current_trends
from engines.competitor_analyzer import get_competitor_insights
from engines.visual_prompter import generate_visual_prompts
from engines.scheduler import generate_content_calendar
from engines.lead_engine import get_lead_recommendations

app = Flask(__name__)

with open(Path(__file__).parent / 'templates' / 'index.html', 'r') as f:
    HTML = f.read()


@app.route('/')
def index():
    return render_template_string(HTML)


@app.route('/set-key', methods=['POST'])
def set_key():
    data = request.json
    os.environ['OPENAI_API_KEY'] = data.get('key', '')
    return jsonify({'status': 'ok'})


@app.route('/api/analyze')
def api_analyze():
    data = analyze_performance()
    summary = {k: (float(v) if hasattr(v, 'item') else v) for k, v in data['summary'].items()}
    types = [{k: (float(v) if hasattr(v, 'item') else v) for k, v in t.items()} for t in data['performance_by_type']]
    top_posts = []
    for p in data.get('top_performing_posts', []):
        top_posts.append({k: (float(v) if hasattr(v, 'item') else str(v) if not isinstance(v, (str, int, float, bool, type(None))) else v) for k, v in p.items()})
    return jsonify({'summary': summary, 'insights': data['insights'], 'performance_by_type': types, 'top_posts': top_posts})


@app.route('/api/calendar')
def api_calendar():
    performance_data = analyze_performance()
    return jsonify(generate_content_calendar(performance_data))


@app.route('/api/leads')
def api_leads():
    performance_data = analyze_performance()
    return jsonify(get_lead_recommendations(performance_data))


@app.route('/api/generate-post', methods=['POST'])
def api_generate_post():
    from engines.content_generator import generate_post_only
    data = request.json
    try:
        content = generate_post_only(topic=data['topic'], pillar=data.get('pillar', 'Agentic AI'),
            post_format=data.get('format', 'TEXT'), buyer_persona=data.get('buyer', 'CTO'))
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}\n\nMake sure your OpenAI API key is saved.'})


@app.route('/api/generate-report-stream', methods=['POST'])
def api_generate_report_stream():
    from config import AZILEN_SYSTEM_PROMPT
    from openai import OpenAI
    from datetime import date

    data = request.json
    topic = data.get('topic')
    api_key = os.environ.get('OPENAI_API_KEY', '')
    if not api_key:
        def no_key():
            yield 'ERROR: OpenAI API key not set.\n\nPaste your key in the field at the top and click Save Key.'
        return Response(stream_with_context(no_key()), mimetype='text/plain')

    performance_data = analyze_performance()
    trend_data = get_current_trends()
    competitor_insights = get_competitor_insights()
    lead_data = get_lead_recommendations(performance_data)
    calendar_data = generate_content_calendar(performance_data)

    perf_summary = performance_data.get('summary', {})
    insights = performance_data.get('insights', [])
    opportunities = competitor_insights.get('azilen_opportunities', [])[:3]
    trend_signals = []
    for cat in list(trend_data.get('all_trends', {}).values())[:3]:
        trend_signals.extend(cat['signals'][:2])

    today = date.today()
    topic_context = f'Focus topic: {topic}' if topic else 'Auto-select the highest-potential topic for today.'

    prompt = f"""Today: {today.strftime('%A, %B %d, %Y')}
{topic_context}
PERFORMANCE: {perf_summary.get('latest_followers',0):,} followers | {perf_summary.get('total_posts_90d',0)} posts ({perf_summary.get('posting_frequency_per_week',0)}x/week) | Engagement: {perf_summary.get('avg_engagement_rate_pct','0%')} | Trend: {perf_summary.get('impression_trend_30d_pct',0):+.1f}%
INSIGHTS: {chr(10).join(insights[:3])}
TRENDS: {chr(10).join(f'- {s}' for s in trend_signals)}
COMPETITOR GAPS: {chr(10).join(f'- {o["opportunity"]}' for o in opportunities)}
Generate complete 17-Section LinkedIn Marketing Report. Brutally specific, data-driven, enterprise-focused.
SECTION 1: EXECUTIVE SUMMARY
SECTION 2: COMPETITOR ANALYSIS
SECTION 3: INDUSTRY TREND ANALYSIS
SECTION 4: CONTENT OPPORTUNITIES (5 ideas)
SECTION 5: 7-DAY CONTENT CALENDAR (Mon-Fri, IST times)
SECTION 6: TODAY'S HIGHEST POTENTIAL POST (800+ chars, publish-ready)
SECTION 7: POST CAPTION VARIATIONS (Long/Medium/Short + 5 headlines + 5 hooks + 5 CTAs)
SECTION 8: HASHTAG STRATEGY (Primary 5, Secondary 10, Niche 5)
SECTION 9: IMAGE GENERATION PROMPTS (DALL-E, Midjourney, Adobe Express)
SECTION 10: CAROUSEL OUTLINE (8-10 slides)
SECTION 11: VIDEO CONCEPT (30-60 sec)
SECTION 12: EMPLOYEE ADVOCACY (CEO, CTO, VP Marketing, Sales Leader)
SECTION 13: PUBLISHING RECOMMENDATION
SECTION 14: EXPECTED PERFORMANCE
SECTION 15: LEAD GENERATION RECOMMENDATIONS
SECTION 16: OPTIMIZATION RECOMMENDATIONS (5 data-backed)
SECTION 17: ACTIONS BEFORE NEXT POST"""

    client = OpenAI(api_key=api_key)

    def generate():
        stream = client.chat.completions.create(model='gpt-4o', max_tokens=8000, stream=True,
            messages=[{'role': 'system', 'content': AZILEN_SYSTEM_PROMPT}, {'role': 'user', 'content': prompt}])
        for chunk in stream:
            text = chunk.choices[0].delta.content or ''
            if text:
                yield text

    return Response(stream_with_context(generate()), mimetype='text/plain')


@app.route('/api/generate-monthly', methods=['POST'])
def api_generate_monthly():
    from engines.content_generator import generate_monthly_analysis
    try:
        return jsonify({'content': generate_monthly_analysis(analyze_performance())})
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'})


@app.route('/api/analyze-mention', methods=['POST'])
def api_analyze_mention():
    from engines.content_generator import generate_mention_response
    data = request.json
    try:
        context = f"Person: {data.get('name','')} | Title: {data.get('title','')} | Type: {data.get('type','')}"
        return jsonify({'content': generate_mention_response(data['text'], context)})
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}\n\nMake sure your OpenAI API key is saved.'})


@app.route('/api/generate-comment-reply', methods=['POST'])
def api_generate_comment_reply():
    from engines.content_generator import generate_comment_response
    data = request.json
    try:
        return jsonify({'content': generate_comment_response(data.get('post', ''), data['comment'], data.get('title', ''))})
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'})


@app.route('/api/generate-growth-plan', methods=['POST'])
def api_generate_growth_plan():
    from engines.content_generator import generate_audience_growth_plan
    try:
        return jsonify({'content': generate_audience_growth_plan(analyze_performance())})
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
