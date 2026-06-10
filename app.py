"""Azilen LinkedIn Growth OS"""
from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, render_template_string, request, stream_with_context
load_dotenv()
import sys
sys.path.insert(0, str(Path(__file__).parent))
from engines.data_analyzer import analyze_performance
from engines.trend_monitor import get_current_trends
from engines.competitor_analyzer import get_competitor_insights
from engines.scheduler import generate_content_calendar
from engines.lead_engine import get_lead_recommendations
app = Flask(__name__)
HTML = open(Path(__file__).parent / 'ui.html').read()

@app.route('/')
def index(): return render_template_string(HTML)

@app.route('/set-key', methods=['POST'])
def set_key():
    os.environ['OPENAI_API_KEY'] = request.json.get('key', '')
    return jsonify({'status': 'ok'})

@app.route('/api/analyze')
def api_analyze():
    data = analyze_performance()
    summary = {k: (float(v) if hasattr(v, 'item') else v) for k, v in data['summary'].items()}
    types = [{k: (float(v) if hasattr(v, 'item') else v) for k, v in t.items()} for t in data['performance_by_type']]
    top_posts = [{k: (float(v) if hasattr(v, 'item') else str(v) if not isinstance(v, (str, int, float, bool, type(None))) else v) for k, v in p.items()} for p in data.get('top_performing_posts', [])]
    return jsonify({'summary': summary, 'insights': data['insights'], 'performance_by_type': types, 'top_posts': top_posts})

@app.route('/api/calendar')
def api_calendar(): return jsonify(generate_content_calendar(analyze_performance()))

@app.route('/api/leads')
def api_leads(): return jsonify(get_lead_recommendations(analyze_performance()))

@app.route('/api/generate-post', methods=['POST'])
def api_generate_post():
    from engines.content_generator import generate_post_only
    d = request.json
    try:
        return jsonify({'content': generate_post_only(topic=d['topic'], pillar=d.get('pillar','Agentic AI'), post_format=d.get('format','TEXT'), buyer_persona=d.get('buyer','CTO'))})
    except Exception as e:
        return jsonify({'error': f'Error: {e}\n\nMake sure your OpenAI API key is saved.'})

@app.route('/api/generate-report-stream', methods=['POST'])
def api_generate_report_stream():
    from config import AZILEN_SYSTEM_PROMPT
    from openai import OpenAI
    from datetime import date
    topic = request.json.get('topic')
    api_key = os.environ.get('OPENAI_API_KEY', '')
    if not api_key:
        return Response(stream_with_context(iter(['ERROR: OpenAI API key not set. Paste your key at the top and click Save Key.'])), mimetype='text/plain')
    perf = analyze_performance()
    trends = get_current_trends()
    comp = get_competitor_insights()
    s = perf.get('summary', {})
    insights = perf.get('insights', [])
    opps = comp.get('azilen_opportunities', [])[:3]
    signals = []
    for cat in list(trends.get('all_trends', {}).values())[:3]:
        signals.extend(cat['signals'][:2])
    prompt = f"""Today: {date.today().strftime('%A, %B %d, %Y')}
{'Focus topic: ' + topic if topic else 'Auto-select highest-potential topic for today.'}
PERFORMANCE: {s.get('latest_followers',0):,} followers | {s.get('total_posts_90d',0)} posts ({s.get('posting_frequency_per_week',0)}x/week) | Engagement: {s.get('avg_engagement_rate_pct','0%')} | 30d Trend: {s.get('impression_trend_30d_pct',0):+.1f}% | 100% posts zero clicks | 88% zero comments
INSIGHTS: {chr(10).join(insights[:3])}
TRENDS: {chr(10).join(f'- {s2}' for s2 in signals)}
COMPETITOR GAPS: {chr(10).join(f'- {o["opportunity"]}' for o in opps)}
Generate complete 17-Section LinkedIn Marketing Report. Brutally specific, data-driven.
SECTION 1: EXECUTIVE SUMMARY\nSECTION 2: COMPETITOR ANALYSIS\nSECTION 3: INDUSTRY TREND ANALYSIS\nSECTION 4: CONTENT OPPORTUNITIES (5 ideas)\nSECTION 5: 7-DAY CONTENT CALENDAR (Mon-Fri, IST times)\nSECTION 6: TODAY'S HIGHEST POTENTIAL POST (800+ chars, publish-ready)\nSECTION 7: POST CAPTION VARIATIONS (Long/Medium/Short + 5 headlines + 5 hooks + 5 CTAs)\nSECTION 8: HASHTAG STRATEGY\nSECTION 9: IMAGE GENERATION PROMPTS (DALL-E, Midjourney, Adobe Express)\nSECTION 10: CAROUSEL OUTLINE (8-10 slides)\nSECTION 11: VIDEO CONCEPT (30-60 sec)\nSECTION 12: EMPLOYEE ADVOCACY (CEO, CTO, VP Marketing, Sales Leader)\nSECTION 13: PUBLISHING RECOMMENDATION\nSECTION 14: EXPECTED PERFORMANCE\nSECTION 15: LEAD GENERATION RECOMMENDATIONS\nSECTION 16: OPTIMIZATION RECOMMENDATIONS (5 data-backed)\nSECTION 17: ACTIONS BEFORE NEXT POST"""
    client = OpenAI(api_key=api_key)
    def generate():
        stream = client.chat.completions.create(model='gpt-4o', max_tokens=8000, stream=True,
            messages=[{'role':'system','content':AZILEN_SYSTEM_PROMPT},{'role':'user','content':prompt}])
        for chunk in stream:
            text = chunk.choices[0].delta.content or ''
            if text: yield text
    return Response(stream_with_context(generate()), mimetype='text/plain')

@app.route('/api/generate-monthly', methods=['POST'])
def api_generate_monthly():
    from engines.content_generator import generate_monthly_analysis
    try: return jsonify({'content': generate_monthly_analysis(analyze_performance())})
    except Exception as e: return jsonify({'error': str(e)})

@app.route('/api/analyze-mention', methods=['POST'])
def api_analyze_mention():
    from engines.content_generator import generate_mention_response
    d = request.json
    try:
        ctx = f"Person: {d.get('name','')} | Title: {d.get('title','')} | Type: {d.get('type','')}"
        return jsonify({'content': generate_mention_response(d['text'], ctx)})
    except Exception as e: return jsonify({'error': f'Error: {e}'})

@app.route('/api/generate-comment-reply', methods=['POST'])
def api_generate_comment_reply():
    from engines.content_generator import generate_comment_response
    d = request.json
    try: return jsonify({'content': generate_comment_response(d.get('post',''), d['comment'], d.get('title',''))})
    except Exception as e: return jsonify({'error': str(e)})

@app.route('/api/generate-growth-plan', methods=['POST'])
def api_generate_growth_plan():
    from engines.content_generator import generate_audience_growth_plan
    try: return jsonify({'content': generate_audience_growth_plan(analyze_performance())})
    except Exception as e: return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
