"""Simple web UI for Azilen LinkedIn Growth OS."""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, Response, jsonify, render_template_string, request, stream_with_context

load_dotenv()

# Add parent to path so engines can be imported
import sys
sys.path.insert(0, str(Path(__file__).parent))

from engines.data_analyzer import analyze_performance, format_analysis_report
from engines.trend_monitor import get_current_trends
from engines.competitor_analyzer import get_competitor_insights
from engines.visual_prompter import generate_visual_prompts
from engines.scheduler import generate_content_calendar
from engines.lead_engine import get_lead_recommendations

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Azilen LinkedIn Growth OS</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', system-ui, sans-serif; background: #0a0f1e; color: #e8eaf0; min-height: 100vh; }

  .header { background: linear-gradient(135deg, #0A2558 0%, #0d3275 100%); padding: 24px 40px; border-bottom: 2px solid #00A3E0; display: flex; align-items: center; gap: 16px; }
  .header h1 { font-size: 22px; font-weight: 700; color: #fff; }
  .header p { font-size: 13px; color: #8badd4; margin-top: 3px; }
  .badge { background: #00A3E0; color: #fff; font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 20px; }

  .container { max-width: 1200px; margin: 0 auto; padding: 32px 24px; }

  .api-banner { background: #1a1f35; border: 1px solid #2a3550; border-left: 4px solid #FF6B35; border-radius: 8px; padding: 16px 20px; margin-bottom: 28px; display: flex; align-items: center; gap: 16px; }
  .api-banner input { background: #0a0f1e; border: 1px solid #2a3550; color: #e8eaf0; padding: 8px 14px; border-radius: 6px; font-size: 14px; flex: 1; outline: none; }
  .api-banner input:focus { border-color: #00A3E0; }
  .api-banner label { font-size: 13px; color: #8badd4; white-space: nowrap; }
  .api-banner button { background: #00A3E0; color: #fff; border: none; padding: 9px 20px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 13px; white-space: nowrap; }
  .api-banner button:hover { background: #0091c9; }
  .api-status { font-size: 12px; color: #8badd4; white-space: nowrap; }
  .api-status.ok { color: #00D4AA; }

  .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 32px; }
  .stat-card { background: #131929; border: 1px solid #1e2d4a; border-radius: 10px; padding: 20px; text-align: center; }
  .stat-card .value { font-size: 28px; font-weight: 800; color: #00A3E0; }
  .stat-card .label { font-size: 12px; color: #8badd4; margin-top: 4px; }
  .stat-card .sub { font-size: 11px; color: #5a7a9a; margin-top: 2px; }
  .stat-card.warn .value { color: #FF6B35; }
  .stat-card.good .value { color: #00D4AA; }

  .section-title { font-size: 13px; font-weight: 700; color: #8badd4; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px; }

  .actions-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-bottom: 32px; }
  .action-card { background: #131929; border: 1px solid #1e2d4a; border-radius: 10px; padding: 24px; cursor: pointer; transition: all 0.2s; position: relative; }
  .action-card:hover { border-color: #00A3E0; transform: translateY(-2px); }
  .action-card h3 { font-size: 16px; font-weight: 700; margin-bottom: 6px; }
  .action-card p { font-size: 13px; color: #8badd4; line-height: 1.5; }
  .action-card .icon { font-size: 28px; margin-bottom: 12px; }
  .action-card .requires-key { position: absolute; top: 12px; right: 12px; font-size: 10px; background: #1a2540; color: #8badd4; padding: 2px 8px; border-radius: 10px; }
  .action-card button { margin-top: 16px; width: 100%; background: #0A2558; color: #00A3E0; border: 1px solid #00A3E0; padding: 10px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 14px; transition: all 0.2s; }
  .action-card button:hover { background: #00A3E0; color: #fff; }
  .action-card button:disabled { opacity: 0.4; cursor: not-allowed; }

  .post-generator { background: #131929; border: 1px solid #1e2d4a; border-radius: 10px; padding: 24px; margin-bottom: 32px; }
  .post-generator h3 { font-size: 16px; font-weight: 700; margin-bottom: 16px; }
  .form-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 12px; }
  .form-group { display: flex; flex-direction: column; gap: 6px; }
  .form-group label { font-size: 12px; color: #8badd4; }
  .form-group input, .form-group select { background: #0a0f1e; border: 1px solid #2a3550; color: #e8eaf0; padding: 9px 12px; border-radius: 6px; font-size: 14px; outline: none; }
  .form-group input:focus, .form-group select:focus { border-color: #00A3E0; }
  .form-group input.wide { width: 100%; }
  .generate-btn { background: linear-gradient(135deg, #0A2558, #0d3a8e); color: #00A3E0; border: 1px solid #00A3E0; padding: 11px 28px; border-radius: 6px; cursor: pointer; font-weight: 700; font-size: 15px; margin-top: 8px; transition: all 0.2s; }
  .generate-btn:hover { background: #00A3E0; color: #fff; }
  .generate-btn:disabled { opacity: 0.4; cursor: not-allowed; }

  .output-panel { background: #0d1220; border: 1px solid #1e2d4a; border-radius: 10px; padding: 24px; margin-bottom: 32px; display: none; }
  .output-panel.visible { display: block; }
  .output-panel h3 { font-size: 14px; font-weight: 700; color: #8badd4; margin-bottom: 16px; display: flex; align-items: center; gap: 10px; }
  .output-content { white-space: pre-wrap; font-family: 'Cascadia Code', 'Fira Code', monospace; font-size: 13px; line-height: 1.7; color: #d0d8f0; max-height: 600px; overflow-y: auto; }
  .output-content::-webkit-scrollbar { width: 6px; }
  .output-content::-webkit-scrollbar-track { background: #0a0f1e; }
  .output-content::-webkit-scrollbar-thumb { background: #2a3550; border-radius: 3px; }

  .spinner { display: inline-block; width: 14px; height: 14px; border: 2px solid #2a3550; border-top-color: #00A3E0; border-radius: 50%; animation: spin 0.8s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }

  .insights-list { background: #131929; border: 1px solid #1e2d4a; border-radius: 10px; padding: 24px; margin-bottom: 32px; }
  .insight-item { display: flex; gap: 12px; padding: 12px 0; border-bottom: 1px solid #1a2540; }
  .insight-item:last-child { border-bottom: none; }
  .insight-num { background: #00A3E0; color: #fff; width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex-shrink: 0; margin-top: 1px; }
  .insight-text { font-size: 13px; color: #c0cce0; line-height: 1.6; }

  .calendar-table { width: 100%; border-collapse: collapse; font-size: 13px; }
  .calendar-table th { background: #0A2558; color: #8badd4; padding: 10px 14px; text-align: left; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
  .calendar-table td { padding: 10px 14px; border-bottom: 1px solid #1a2540; vertical-align: top; }
  .calendar-table tr:hover td { background: #131929; }
  .format-badge { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }
  .format-IMAGE { background: #0d3a1a; color: #00D4AA; }
  .format-TEXT { background: #1a2d0a; color: #7ed957; }
  .format-CAROUSEL { background: #0a1f3a; color: #00A3E0; }
  .format-VIDEO { background: #2d1a0a; color: #FF6B35; }

  .copy-btn { background: transparent; border: 1px solid #2a3550; color: #8badd4; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 11px; margin-left: 8px; }
  .copy-btn:hover { border-color: #00A3E0; color: #00A3E0; }

  .tab-bar { display: flex; gap: 4px; margin-bottom: 20px; border-bottom: 1px solid #1e2d4a; padding-bottom: 0; }
  .tab { padding: 10px 20px; cursor: pointer; font-size: 13px; font-weight: 600; color: #8badd4; border-bottom: 2px solid transparent; margin-bottom: -1px; }
  .tab.active { color: #00A3E0; border-bottom-color: #00A3E0; }
  .tab-content { display: none; }
  .tab-content.active { display: block; }
</style>
</head>
<body>

<div class="header">
  <div>
    <h1>⚡ Azilen LinkedIn Growth OS</h1>
    <p>Autonomous LinkedIn Marketing • Enterprise AI & Product Engineering</p>
  </div>
  <span class="badge">LIVE</span>
</div>

<div class="container">

  <!-- API Key Banner -->
  <div class="api-banner">
    <label>🔑 Anthropic API Key</label>
    <input type="password" id="apiKeyInput" placeholder="sk-ant-..." />
    <button onclick="saveApiKey()">Save Key</button>
    <span class="api-status" id="apiStatus">Not set – analysis works without key</span>
  </div>

  <!-- Stats Grid (loaded on page load) -->
  <div class="section-title">📊 90-Day Performance Dashboard</div>
  <div class="stats-grid" id="statsGrid">
    <div class="stat-card"><div class="value">—</div><div class="label">Loading...</div></div>
  </div>

  <!-- Tab Bar -->
  <div class="tab-bar">
    <div class="tab active" onclick="switchTab('insights')">Key Insights</div>
    <div class="tab" onclick="switchTab('calendar')">Content Calendar</div>
    <div class="tab" onclick="switchTab('generate')">Generate Content</div>
    <div class="tab" onclick="switchTab('report')">Full Daily Report</div>
  </div>

  <!-- Tab: Insights -->
  <div class="tab-content active" id="tab-insights">
    <div class="insights-list" id="insightsList">
      <div style="color:#8badd4;font-size:13px;">Loading insights...</div>
    </div>
  </div>

  <!-- Tab: Calendar -->
  <div class="tab-content" id="tab-calendar">
    <div style="background:#131929;border:1px solid #1e2d4a;border-radius:10px;padding:24px;overflow-x:auto;">
      <table class="calendar-table" id="calendarTable">
        <tr><td style="color:#8badd4;font-size:13px;">Loading calendar...</td></tr>
      </table>
    </div>
  </div>

  <!-- Tab: Generate Content -->
  <div class="tab-content" id="tab-generate">
    <div class="post-generator">
      <h3>✍️ Generate LinkedIn Post</h3>
      <div class="form-group" style="margin-bottom:12px;">
        <label>Topic / Idea *</label>
        <input type="text" id="postTopic" class="wide" placeholder="e.g. Why 73% of Enterprise AI Projects Fail Before Production" />
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Content Pillar</label>
          <select id="postPillar">
            <option>Agentic AI</option>
            <option>Generative AI</option>
            <option>Enterprise AI</option>
            <option>Product Engineering</option>
            <option>Digital Transformation</option>
            <option>Data Engineering</option>
            <option>Cloud Modernization</option>
            <option>HRTech</option>
            <option>Manufacturing Technology</option>
            <option>FinTech Technology</option>
            <option>Software Product Development</option>
            <option>Leadership & Innovation</option>
          </select>
        </div>
        <div class="form-group">
          <label>Target Buyer</label>
          <select id="postBuyer">
            <option>CTO</option>
            <option>CIO</option>
            <option>Chief Digital Officer</option>
            <option>VP Engineering</option>
            <option>VP Product</option>
            <option>Head of AI</option>
            <option>Head of Data</option>
            <option>CHRO</option>
            <option>Startup Founders</option>
            <option>SaaS Founders</option>
          </select>
        </div>
        <div class="form-group">
          <label>Format</label>
          <select id="postFormat">
            <option>TEXT</option>
            <option>IMAGE</option>
            <option>CAROUSEL</option>
            <option>VIDEO</option>
          </select>
        </div>
      </div>
      <button class="generate-btn" id="genPostBtn" onclick="generatePost()">Generate Post Variations →</button>
    </div>
    <div class="output-panel" id="postOutput">
      <h3><span class="spinner" id="postSpinner" style="display:none"></span> Generated Content <button class="copy-btn" onclick="copyOutput('postOutputContent')">Copy All</button></h3>
      <div class="output-content" id="postOutputContent"></div>
    </div>
  </div>

  <!-- Tab: Full Daily Report -->
  <div class="tab-content" id="tab-report">
    <div style="background:#131929;border:1px solid #1e2d4a;border-radius:10px;padding:28px;margin-bottom:24px;">
      <div class="icon" style="font-size:32px;margin-bottom:12px;">🚀</div>
      <h3 style="font-size:18px;margin-bottom:8px;">Full 17-Section LinkedIn Marketing Report</h3>
      <p style="font-size:13px;color:#8badd4;line-height:1.6;margin-bottom:16px;">
        Generates your complete daily marketing operating report: competitor analysis, trend analysis, content calendar, post variations, image prompts, carousel outline, video concept, employee advocacy versions, lead generation recommendations, and more. Takes ~60-90 seconds.
      </p>
      <div class="form-group" style="margin-bottom:16px;max-width:500px;">
        <label>Topic Override (optional – leave blank to auto-select best topic)</label>
        <input type="text" id="reportTopic" class="wide" placeholder="Leave blank for AI to pick best topic today..." />
      </div>
      <button class="generate-btn" id="genReportBtn" onclick="generateReport()">Generate Full Report →</button>
    </div>
    <div class="output-panel" id="reportOutput">
      <h3><span class="spinner" id="reportSpinner" style="display:none"></span> Full Marketing Report <button class="copy-btn" onclick="copyOutput('reportOutputContent')">Copy All</button></h3>
      <div class="output-content" id="reportOutputContent"></div>
    </div>
  </div>

</div>

<script>
let apiKey = '';

function saveApiKey() {
  apiKey = document.getElementById('apiKeyInput').value.trim();
  if (apiKey) {
    fetch('/set-key', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({key: apiKey})})
      .then(r => r.json())
      .then(d => {
        document.getElementById('apiStatus').textContent = '✓ Key saved for this session';
        document.getElementById('apiStatus').className = 'api-status ok';
      });
  }
}

function switchTab(name) {
  document.querySelectorAll('.tab').forEach((t,i) => t.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  event.target.classList.add('active');
  document.getElementById('tab-' + name).classList.add('active');
}

async function loadStats() {
  const r = await fetch('/api/analyze');
  const data = await r.json();
  const s = data.summary;

  document.getElementById('statsGrid').innerHTML = `
    <div class="stat-card good"><div class="value">${s.latest_followers.toLocaleString()}</div><div class="label">Total Followers</div><div class="sub">+${s.follower_growth_90d.toLocaleString()} in 90 days</div></div>
    <div class="stat-card ${s.vs_benchmark === 'BELOW' ? 'warn' : 'good'}"><div class="value">${s.avg_engagement_rate_pct}</div><div class="label">Avg Engagement Rate</div><div class="sub">Benchmark: ${s.linkedin_benchmark_pct}</div></div>
    <div class="stat-card"><div class="value">${s.total_impressions_90d.toLocaleString()}</div><div class="label">Total Impressions 90d</div><div class="sub">${s.avg_daily_impressions.toLocaleString()} avg/day</div></div>
    <div class="stat-card ${s.posting_frequency_per_week < 5 ? 'warn' : 'good'}"><div class="value">${s.posting_frequency_per_week}x</div><div class="label">Posts / Week</div><div class="sub">Target: 7-10x/week</div></div>
    <div class="stat-card ${s.impression_trend_30d_pct < 0 ? 'warn' : 'good'}"><div class="value">${s.impression_trend_30d_pct > 0 ? '+' : ''}${s.impression_trend_30d_pct}%</div><div class="label">Impression Trend (30d)</div><div class="sub">${s.impression_trend_30d_pct < 0 ? 'Declining ↓' : 'Growing ↑'}</div></div>
    <div class="stat-card"><div class="value">${s.total_posts_90d}</div><div class="label">Posts Published (90d)</div><div class="sub">${s.date_range_days} day period</div></div>
  `;

  // Insights
  const insights = data.insights;
  document.getElementById('insightsList').innerHTML = insights.map((ins, i) =>
    `<div class="insight-item"><div class="insight-num">${i+1}</div><div class="insight-text">${ins}</div></div>`
  ).join('');

  // Calendar
  const calR = await fetch('/api/calendar');
  const calData = await calR.json();
  const formatClass = f => `format-badge format-${f}`;
  document.getElementById('calendarTable').innerHTML = `
    <thead><tr>
      <th>Day</th><th>Date</th><th>Time IST</th><th>Content Pillar</th><th>Format</th><th>Goal</th><th>CTA Type</th>
    </tr></thead>
    <tbody>
      ${calData.calendar.map(e => `<tr>
        <td><strong>${e.day}</strong></td>
        <td>${e.date}</td>
        <td>${e.time_ist}</td>
        <td>${e.content_pillar}</td>
        <td><span class="${formatClass(e.format)}">${e.format}</span></td>
        <td>${e.goal}</td>
        <td style="font-size:12px;color:#8badd4;max-width:200px;">${e.cta_type}</td>
      </tr>`).join('')}
    </tbody>
  `;
}

async function generatePost() {
  const topic = document.getElementById('postTopic').value.trim();
  if (!topic) { alert('Please enter a topic'); return; }

  const btn = document.getElementById('genPostBtn');
  const panel = document.getElementById('postOutput');
  const content = document.getElementById('postOutputContent');
  const spinner = document.getElementById('postSpinner');

  btn.disabled = true;
  btn.textContent = 'Generating...';
  spinner.style.display = 'inline-block';
  panel.classList.add('visible');
  content.textContent = 'Generating post variations via Claude API...\\n\\nThis takes 15-20 seconds...';

  const resp = await fetch('/api/generate-post', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      topic,
      pillar: document.getElementById('postPillar').value,
      buyer: document.getElementById('postBuyer').value,
      format: document.getElementById('postFormat').value,
    })
  });
  const data = await resp.json();
  content.textContent = data.content || data.error;
  btn.disabled = false;
  btn.textContent = 'Generate Post Variations →';
  spinner.style.display = 'none';
}

async function generateReport() {
  const btn = document.getElementById('genReportBtn');
  const panel = document.getElementById('reportOutput');
  const content = document.getElementById('reportOutputContent');
  const spinner = document.getElementById('reportSpinner');
  const topic = document.getElementById('reportTopic').value.trim();

  btn.disabled = true;
  btn.textContent = 'Generating report...';
  spinner.style.display = 'inline-block';
  panel.classList.add('visible');
  content.textContent = '';

  const response = await fetch('/api/generate-report-stream', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({topic: topic || null})
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const {done, value} = await reader.read();
    if (done) break;
    content.textContent += decoder.decode(value);
    content.scrollTop = content.scrollHeight;
  }

  btn.disabled = false;
  btn.textContent = 'Generate Full Report →';
  spinner.style.display = 'none';
}

function copyOutput(id) {
  const text = document.getElementById(id).textContent;
  navigator.clipboard.writeText(text).then(() => alert('Copied to clipboard!'));
}

loadStats();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/set-key", methods=["POST"])
def set_key():
    data = request.json
    os.environ["ANTHROPIC_API_KEY"] = data.get("key", "")
    return jsonify({"status": "ok"})


@app.route("/api/analyze")
def api_analyze():
    data = analyze_performance()
    # Convert any non-serializable types
    summary = {}
    for k, v in data["summary"].items():
        try:
            json.dumps(v)
            summary[k] = v
        except Exception:
            summary[k] = str(v)
    return jsonify({
        "summary": summary,
        "insights": data["insights"],
        "performance_by_type": [
            {k: (float(v) if hasattr(v, 'item') else v) for k, v in t.items()}
            for t in data["performance_by_type"]
        ],
    })


@app.route("/api/calendar")
def api_calendar():
    performance_data = analyze_performance()
    calendar_data = generate_content_calendar(performance_data)
    return jsonify(calendar_data)


@app.route("/api/generate-post", methods=["POST"])
def api_generate_post():
    from engines.content_generator import generate_post_only
    data = request.json
    try:
        content = generate_post_only(
            topic=data["topic"],
            pillar=data.get("pillar", "Agentic AI"),
            post_format=data.get("format", "TEXT"),
            buyer_persona=data.get("buyer", "CTO"),
        )
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}\n\nMake sure your Anthropic API key is saved above."})


@app.route("/api/generate-report-stream", methods=["POST"])
def api_generate_report_stream():
    import anthropic as ant_module

    data = request.json
    topic = data.get("topic")

    performance_data = analyze_performance()
    trend_data = get_current_trends()
    competitor_insights = get_competitor_insights()
    lead_data = get_lead_recommendations(performance_data)
    calendar_data = generate_content_calendar(performance_data)
    visual_prompts = generate_visual_prompts(topic or "Enterprise AI")

    from config import AZILEN_SYSTEM_PROMPT, CONTENT_PILLARS
    from engines.content_generator import _summarize_calendar
    import json as _json
    from datetime import date

    perf_summary = performance_data.get("summary", {})
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

PERFORMANCE DATA (Last 90 Days):
- Followers: {perf_summary.get('latest_followers', 0):,}
- Total Posts: {perf_summary.get('total_posts_90d', 0)} ({perf_summary.get('posting_frequency_per_week', 0)}x/week – CRITICAL: far below 7-10x target)
- Avg Engagement Rate: {perf_summary.get('avg_engagement_rate_pct', '0%')} vs Benchmark {perf_summary.get('linkedin_benchmark_pct', '')} → {perf_summary.get('vs_benchmark', 'BELOW')}
- Impression Trend 30d: {perf_summary.get('impression_trend_30d_pct', 0):+.1f}%
- 100% of posts have zero link clicks – CTA strategy broken
- 88% of posts have zero comments

Key Insights: {chr(10).join(insights[:3])}

TRENDING NOW: {chr(10).join(f'- {s}' for s in trend_signals)}

COMPETITOR GAPS: {chr(10).join(f'- {o["opportunity"]}' for o in opportunities)}

Generate the complete 17-Section LinkedIn Marketing Operating Report. Be brutally specific, data-driven, and enterprise-focused.

SECTION 1: EXECUTIVE SUMMARY
SECTION 2: COMPETITOR ANALYSIS
SECTION 3: INDUSTRY TREND ANALYSIS
SECTION 4: CONTENT OPPORTUNITIES (5 specific ideas)
SECTION 5: 7-DAY CONTENT CALENDAR (Mon-Fri, specific topics, times in IST)
SECTION 6: TODAY'S HIGHEST POTENTIAL POST (complete, publish-ready post, 800+ chars)
SECTION 7: POST CAPTION VARIATIONS (Long/Medium/Short + 5 headlines + 5 hooks + 5 CTAs)
SECTION 8: HASHTAG STRATEGY (Primary 5, Secondary 10, Niche 5)
SECTION 9: IMAGE GENERATION PROMPTS (DALL-E, Midjourney, Adobe Express)
SECTION 10: CAROUSEL OUTLINE (8-10 slides)
SECTION 11: VIDEO CONCEPT (30-60 second script)
SECTION 12: EMPLOYEE ADVOCACY VERSIONS (CEO, CTO, VP Marketing, Sales Leader)
SECTION 13: PUBLISHING RECOMMENDATION (exact time, format, targeting)
SECTION 14: EXPECTED PERFORMANCE (impressions, engagement, reach, leads)
SECTION 15: LEAD GENERATION RECOMMENDATIONS
SECTION 16: OPTIMIZATION RECOMMENDATIONS (5 data-backed improvements)
SECTION 17: ACTIONS TO IMPLEMENT BEFORE NEXT POST
"""

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        def no_key():
            yield "ERROR: Anthropic API key not set.\n\nPlease enter your API key in the field at the top of the page and click Save Key."
        return Response(stream_with_context(no_key()), mimetype="text/plain")

    client = ant_module.Anthropic(api_key=api_key)

    def generate():
        with client.messages.stream(
            model="claude-opus-4-8",
            max_tokens=8000,
            system=AZILEN_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            for text in stream.text_stream:
                yield text

    return Response(stream_with_context(generate()), mimetype="text/plain")


if __name__ == "__main__":
    print("\n" + "═"*60)
    print("  Azilen LinkedIn Growth OS – Web Interface")
    print("═"*60)
    print("  Open in browser: http://localhost:5000")
    print("═"*60 + "\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
