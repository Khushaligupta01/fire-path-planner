<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FIRE Path Planner — README</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --fire: #FF4500;
    --fire-light: #FF6B35;
    --gold: #F59E0B;
    --dark: #0A0A0F;
    --dark2: #12121A;
    --dark3: #1A1A28;
    --dark4: #22223A;
    --card: #16161F;
    --border: rgba(255,255,255,0.07);
    --text: #F0EEF8;
    --muted: #9490B0;
    --accent: #7C6EF8;
    --green: #22C55E;
    --teal: #14B8A6;
  }

  body {
    background: var(--dark);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    line-height: 1.75;
    min-height: 100vh;
  }

  /* ── HERO ── */
  .hero {
    position: relative;
    text-align: center;
    padding: 80px 40px 60px;
    overflow: hidden;
    background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(255,69,0,0.18) 0%, transparent 70%),
                radial-gradient(ellipse 50% 40% at 80% 80%, rgba(124,110,248,0.12) 0%, transparent 60%);
  }

  .hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: radial-gradient(rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 28px 28px;
    pointer-events: none;
  }

  .hero-emoji {
    font-size: 64px;
    display: block;
    margin-bottom: 20px;
    filter: drop-shadow(0 0 40px rgba(255,100,0,0.6));
    animation: pulse 3s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { filter: drop-shadow(0 0 30px rgba(255,100,0,0.5)); }
    50% { filter: drop-shadow(0 0 60px rgba(255,100,0,0.9)); }
  }

  .hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(36px, 6vw, 64px);
    font-weight: 800;
    letter-spacing: -1.5px;
    background: linear-gradient(135deg, #FF6B35 0%, #FF4500 40%, #F59E0B 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
  }

  .hero-sub {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 600;
    color: var(--muted);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 28px;
  }

  .hero-tagline {
    font-size: 18px;
    font-style: italic;
    font-weight: 300;
    color: rgba(240,238,248,0.7);
    margin-bottom: 20px;
  }

  .hero-desc {
    max-width: 680px;
    margin: 0 auto 36px;
    font-size: 15px;
    color: var(--muted);
    line-height: 1.8;
  }

  .badges {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-bottom: 36px;
  }

  .badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 500;
    border: 1px solid;
    font-family: 'DM Sans', sans-serif;
  }

  .badge-python { background: rgba(59,130,246,0.1); border-color: rgba(59,130,246,0.3); color: #93C5FD; }
  .badge-streamlit { background: rgba(255,75,75,0.1); border-color: rgba(255,75,75,0.3); color: #FCA5A5; }
  .badge-openai { background: rgba(124,110,248,0.1); border-color: rgba(124,110,248,0.3); color: #C4B5FD; }
  .badge-mit { background: rgba(34,197,94,0.1); border-color: rgba(34,197,94,0.3); color: #86EFAC; }

  .hero-links {
    display: flex;
    gap: 16px;
    justify-content: center;
    flex-wrap: wrap;
  }

  .btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 24px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    text-decoration: none;
    transition: all 0.2s;
    cursor: pointer;
  }

  .btn-primary {
    background: linear-gradient(135deg, #FF4500, #FF6B35);
    color: white;
    border: none;
    box-shadow: 0 4px 24px rgba(255,69,0,0.3);
  }

  .btn-primary:hover { box-shadow: 0 6px 32px rgba(255,69,0,0.5); transform: translateY(-1px); }

  .btn-outline {
    background: transparent;
    color: var(--text);
    border: 1px solid var(--border);
  }

  .btn-outline:hover { border-color: rgba(255,255,255,0.2); background: rgba(255,255,255,0.04); }

  /* ── DIVIDER ── */
  .divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,69,0,0.3), rgba(124,110,248,0.3), transparent);
    margin: 0;
  }

  /* ── CONTENT ── */
  .content {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 32px 80px;
  }

  /* ── SECTION ── */
  .section {
    margin-top: 60px;
  }

  .section-label {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--fire);
    margin-bottom: 12px;
  }

  .section-label::before {
    content: '';
    display: block;
    width: 24px;
    height: 1px;
    background: var(--fire);
  }

  h2 {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 20px;
    letter-spacing: -0.5px;
  }

  h3 {
    font-family: 'Syne', sans-serif;
    font-size: 17px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 12px;
  }

  p { color: var(--muted); margin-bottom: 14px; }

  /* ── PROBLEM CARDS ── */
  .problem-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px;
    margin-top: 20px;
  }

  .problem-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    position: relative;
    overflow: hidden;
  }

  .problem-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--fire), var(--gold));
  }

  .problem-card p {
    color: var(--text);
    font-size: 14px;
    margin: 0;
    line-height: 1.6;
  }

  /* ── FEATURE CARDS ── */
  .feature-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 16px;
    position: relative;
    transition: border-color 0.2s;
  }

  .feature-card:hover { border-color: rgba(255,69,0,0.2); }

  .feature-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 16px;
  }

  .feature-icon {
    width: 44px;
    height: 44px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
  }

  .icon-fire { background: rgba(255,69,0,0.15); }
  .icon-gold { background: rgba(245,158,11,0.15); }
  .icon-blue { background: rgba(59,130,246,0.15); }
  .icon-green { background: rgba(34,197,94,0.15); }
  .icon-teal { background: rgba(20,184,166,0.15); }
  .icon-purple { background: rgba(124,110,248,0.15); }
  .icon-pink { background: rgba(236,72,153,0.15); }
  .icon-star { background: rgba(245,158,11,0.15); }
  .icon-dash { background: rgba(99,102,241,0.15); }

  .feature-num {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: var(--fire);
    letter-spacing: 1px;
  }

  .feature-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
  }

  .feature-tag {
    margin-left: auto;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 100px;
    background: rgba(255,69,0,0.1);
    color: var(--fire);
    border: 1px solid rgba(255,69,0,0.2);
    white-space: nowrap;
  }

  .feature-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .feature-list li {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-size: 14px;
    color: var(--muted);
    line-height: 1.5;
  }

  .feature-list li::before {
    content: '→';
    color: var(--fire);
    flex-shrink: 0;
    font-size: 12px;
    margin-top: 2px;
  }

  /* ── SCORE TABLE ── */
  .score-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 14px;
    font-size: 14px;
  }

  .score-table th {
    text-align: left;
    padding: 10px 14px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    border-bottom: 1px solid var(--border);
  }

  .score-table td {
    padding: 12px 14px;
    border-bottom: 1px solid var(--border);
    color: var(--muted);
    vertical-align: top;
  }

  .score-table tr:last-child td { border-bottom: none; }

  .score-table td:first-child {
    color: var(--text);
    font-weight: 500;
    white-space: nowrap;
  }

  .score-table tr:hover td { background: rgba(255,255,255,0.02); }

  /* ── TECH STACK ── */
  .stack-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    margin-top: 20px;
  }

  .stack-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 16px;
    text-align: center;
  }

  .stack-layer {
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
  }

  .stack-tech {
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 700;
    color: var(--text);
  }

  /* ── CODE BLOCK ── */
  .code-block {
    background: var(--dark2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    overflow-x: auto;
    margin: 16px 0;
    position: relative;
  }

  .code-block .comment { color: #4CAF50; }
  .code-block .cmd { color: #FF9800; }
  .code-block .str { color: #81D4FA; }
  .code-label {
    position: absolute;
    top: 10px;
    right: 14px;
    font-size: 10px;
    font-weight: 600;
    color: var(--muted);
    letter-spacing: 1px;
    text-transform: uppercase;
    font-family: 'DM Sans', sans-serif;
  }

  .code-line { display: block; line-height: 1.9; color: #E0E0E0; }

  /* ── FILE TREE ── */
  .file-tree {
    background: var(--dark2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    font-family: 'Courier New', monospace;
    font-size: 13px;
    line-height: 2;
  }

  .tree-root { color: var(--fire); font-weight: 700; }
  .tree-dir { color: #81D4FA; }
  .tree-file { color: #E0E0E0; }
  .tree-comment { color: #5A5A7A; }

  /* ── IMPACT ── */
  .impact-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 14px;
    margin-top: 20px;
  }

  .impact-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px 18px;
    text-align: center;
  }

  .impact-value {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    background: linear-gradient(135deg, var(--fire), var(--gold));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 6px;
    line-height: 1.2;
  }

  .impact-label {
    font-size: 12px;
    color: var(--muted);
    line-height: 1.4;
  }

  /* ── TEAM ── */
  .team-grid {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin-top: 20px;
  }

  .team-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px 28px;
    display: flex;
    align-items: center;
    gap: 16px;
    min-width: 220px;
  }

  .avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--fire), var(--gold));
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 16px;
    color: white;
    flex-shrink: 0;
  }

  .team-name {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 15px;
    color: var(--text);
  }

  .team-role {
    font-size: 12px;
    color: var(--muted);
    margin-top: 2px;
  }

  /* ── ROADMAP ── */
  .roadmap-list {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 20px;
  }

  .roadmap-item {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    color: var(--muted);
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
  }

  .todo-box {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255,255,255,0.15);
    border-radius: 4px;
    flex-shrink: 0;
  }

  /* ── FOOTER ── */
  .footer {
    text-align: center;
    padding: 48px 32px;
    border-top: 1px solid var(--border);
    background: radial-gradient(ellipse 60% 40% at 50% 100%, rgba(255,69,0,0.06) 0%, transparent 70%);
  }

  .footer-heart {
    font-size: 22px;
    margin-bottom: 10px;
    display: block;
  }

  .footer-headline {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 16px;
    color: var(--text);
    margin-bottom: 8px;
  }

  .footer-quote {
    font-style: italic;
    font-size: 14px;
    color: var(--muted);
    max-width: 500px;
    margin: 0 auto;
  }

  /* ── prereqs ── */
  .prereq-list {
    list-style: none;
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-top: 10px;
  }
  .prereq-item {
    background: var(--dark3);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 13px;
    color: var(--muted);
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .prereq-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--fire); flex-shrink: 0; }
</style>
</head>
<body>

<!-- ═══════════════════ HERO ═══════════════════ -->
<div class="hero">
  <span class="hero-emoji">🔥</span>
  <h1>FIRE Path Planner</h1>
  <p class="hero-sub">Your AI-Powered Financial Independence Advisor</p>
  <p class="hero-tagline">Plan early. Retire free. Live fully.</p>
  <p class="hero-desc">
    FIRE Path Planner is an intelligent financial planning web app that helps you achieve
    <strong style="color:var(--text)">Financial Independence, Retire Early (FIRE)</strong> —
    with AI-driven insights, a personalized Money Health Score, and a year-by-year investment
    roadmap tailored to your life.
  </p>
  <div class="badges">
    <span class="badge badge-python">🐍 Python 3.9+</span>
    <span class="badge badge-streamlit">⚡ Streamlit</span>
    <span class="badge badge-openai">🤖 OpenAI GPT-4</span>
    <span class="badge badge-mit">📄 MIT License</span>
  </div>
  <div class="hero-links">
    <a href="#" class="btn btn-primary">🚀 Live Demo</a>
    <a href="#" class="btn btn-outline">📽️ Pitch Video</a>
    <a href="#" class="btn btn-outline">📄 Architecture</a>
  </div>
</div>

<div class="divider"></div>

<div class="content">

  <!-- ═══ PROBLEM ═══ -->
  <div class="section">
    <span class="section-label">The Problem</span>
    <h2>🎯 Most Indians don't know…</h2>
    <div class="problem-grid">
      <div class="problem-card"><p>How much they need to retire early</p></div>
      <div class="problem-card"><p>Whether their current finances are healthy</p></div>
      <div class="problem-card"><p>What to invest in, and how much per month</p></div>
    </div>
    <p style="margin-top:20px">Generic financial calculators give numbers — not guidance. We built an <strong style="color:var(--text)">AI advisor</strong> that gives both.</p>
  </div>

  <!-- ═══ SOLUTION ═══ -->
  <div class="section">
    <span class="section-label">Our Solution</span>
    <h2>💡 What We Built</h2>
    <p>FIRE Path Planner combines <strong style="color:var(--text)">rule-based financial intelligence</strong> with <strong style="color:var(--text)">OpenAI's LLM</strong> to give users a complete picture of their financial future — in minutes, not months.</p>
  </div>

  <!-- ═══ FEATURES ═══ -->
  <div class="section">
    <span class="section-label">Features</span>
    <h2>✨ What's Inside</h2>

    <div class="feature-card">
      <div class="feature-header">
        <div class="feature-icon icon-fire">🔥</div>
        <div>
          <div class="feature-num">01</div>
          <div class="feature-title">FIRE Path Planner</div>
        </div>
        <span class="feature-tag">Core Engine</span>
      </div>
      <ul class="feature-list">
        <li>Calculates your FIRE Target using the 25× rule</li>
        <li>Computes monthly SIP needed to retire early</li>
        <li>Estimates emergency fund (6 months expenses)</li>
        <li>Factors in inflation-adjusted returns (~5–6%)</li>
        <li>Generates a year-by-year investment roadmap</li>
      </ul>
    </div>

    <div class="feature-card">
      <div class="feature-header">
        <div class="feature-icon icon-gold">💰</div>
        <div>
          <div class="feature-num">02</div>
          <div class="feature-title">Goal-Based Planning</div>
        </div>
      </div>
      <ul class="feature-list">
        <li>Add life goals (house, car, education, travel)</li>
        <li>Calculates SIP required per goal</li>
        <li>Combines FIRE SIP + Goal SIP into one unified plan</li>
      </ul>
    </div>

    <div class="feature-card">
      <div class="feature-header">
        <div class="feature-icon icon-blue">🛡️</div>
        <div>
          <div class="feature-num">03</div>
          <div class="feature-title">Insurance Recommendation</div>
        </div>
      </div>
      <ul class="feature-list">
        <li>Life cover = 10× annual income</li>
        <li>Health cover tailored to age bracket</li>
        <li>Fills the most overlooked gap in personal finance</li>
      </ul>
    </div>

    <div class="feature-card" style="border-color: rgba(124,110,248,0.25);">
      <div class="feature-header">
        <div class="feature-icon icon-purple">💯</div>
        <div>
          <div class="feature-num">04</div>
          <div class="feature-title">Money Health Score</div>
        </div>
        <span class="feature-tag" style="background:rgba(124,110,248,0.1);color:#C4B5FD;border-color:rgba(124,110,248,0.3)">Key Differentiator</span>
      </div>
      <p style="margin-bottom:14px;font-size:14px">Scores your finances out of <strong style="color:var(--text)">100 across 6 dimensions:</strong></p>
      <table class="score-table">
        <thead><tr><th>Dimension</th><th>What It Measures</th></tr></thead>
        <tbody>
          <tr><td>🧰 Emergency Preparedness</td><td>Do you have a safety net?</td></tr>
          <tr><td>📈 Investment Discipline</td><td>Are you investing enough?</td></tr>
          <tr><td>💳 Debt Health</td><td>Is your debt load manageable?</td></tr>
          <tr><td>🧾 Tax Efficiency</td><td>Are you using tax-saving instruments?</td></tr>
          <tr><td>🏖️ Retirement Readiness</td><td>Are you on track to retire?</td></tr>
          <tr><td>🛡️ Insurance Coverage</td><td>Are you adequately protected?</td></tr>
        </tbody>
      </table>
    </div>

    <div class="feature-card">
      <div class="feature-header">
        <div class="feature-icon icon-teal">📊</div>
        <div>
          <div class="feature-num">05</div>
          <div class="feature-title">Investment Roadmap Visualization</div>
        </div>
      </div>
      <ul class="feature-list">
        <li>Interactive wealth growth chart over time</li>
        <li>Year-by-year data table for detailed tracking</li>
      </ul>
    </div>

    <div class="feature-card">
      <div class="feature-header">
        <div class="feature-icon icon-green">🎯</div>
        <div>
          <div class="feature-num">06</div>
          <div class="feature-title">Smart Suggestions Engine</div>
        </div>
      </div>
      <ul class="feature-list">
        <li>Detects your weakest financial area</li>
        <li>Gives targeted, actionable improvement tips</li>
        <li>Feels like AI — even without an API call</li>
      </ul>
    </div>

    <div class="feature-card">
      <div class="feature-header">
        <div class="feature-icon icon-purple">🤖</div>
        <div>
          <div class="feature-num">07</div>
          <div class="feature-title">AI Insights (OpenAI Integration)</div>
        </div>
      </div>
      <ul class="feature-list">
        <li>Explains your full plan in simple language</li>
        <li>Surfaces warnings and opportunities</li>
        <li>Personalizes advice based on your unique inputs</li>
      </ul>
    </div>

    <div class="feature-card">
      <div class="feature-header">
        <div class="feature-icon icon-star">🎉</div>
        <div>
          <div class="feature-num">08</div>
          <div class="feature-title">Life Event Advisor</div>
        </div>
        <span class="feature-tag">Bonus Feature</span>
      </div>
      <ul class="feature-list">
        <li>Handles events: Bonus received, Marriage, Inheritance</li>
        <li>Gives contextual financial advice for life changes</li>
      </ul>
    </div>
  </div>

  <!-- ═══ TECH STACK ═══ -->
  <div class="section">
    <span class="section-label">Technology</span>
    <h2>🖥️ Tech Stack</h2>
    <div class="stack-grid">
      <div class="stack-card"><div class="stack-layer">Frontend & App</div><div class="stack-tech">Streamlit</div></div>
      <div class="stack-card"><div class="stack-layer">Backend Logic</div><div class="stack-tech">Python 3.9+</div></div>
      <div class="stack-card"><div class="stack-layer">AI Layer</div><div class="stack-tech">OpenAI GPT-4</div></div>
      <div class="stack-card"><div class="stack-layer">Data & Math</div><div class="stack-tech">Pandas · NumPy</div></div>
      <div class="stack-card"><div class="stack-layer">Visualization</div><div class="stack-tech">Plotly</div></div>
    </div>
  </div>

  <!-- ═══ GETTING STARTED ═══ -->
  <div class="section">
    <span class="section-label">Setup</span>
    <h2>🚀 Getting Started</h2>
    <h3>Prerequisites</h3>
    <ul class="prereq-list">
      <li class="prereq-item"><span class="prereq-dot"></span>Python 3.9+</li>
      <li class="prereq-item"><span class="prereq-dot"></span>OpenAI API key</li>
    </ul>
    <h3 style="margin-top:24px">Installation</h3>
    <div class="code-block">
      <span class="code-label">bash</span>
      <span class="code-line"><span class="comment"># 1. Clone the repository</span></span>
      <span class="code-line"><span class="cmd">git clone</span> <span class="str">https://github.com/YOUR_USERNAME/fire-path-planner.git</span></span>
      <span class="code-line"><span class="cmd">cd</span> fire-path-planner</span>
      <span class="code-line">&nbsp;</span>
      <span class="code-line"><span class="comment"># 2. Install dependencies</span></span>
      <span class="code-line"><span class="cmd">pip install</span> -r requirements.txt</span>
      <span class="code-line">&nbsp;</span>
      <span class="code-line"><span class="comment"># 3. Set your OpenAI API key</span></span>
      <span class="code-line"><span class="cmd">export</span> OPENAI_API_KEY=<span class="str">"your-api-key-here"</span></span>
      <span class="code-line">&nbsp;</span>
      <span class="code-line"><span class="comment"># 4. Run the app</span></span>
      <span class="code-line"><span class="cmd">streamlit run</span> main.py</span>
    </div>
    <p>The app will open at <code style="background:var(--dark3);padding:2px 8px;border-radius:5px;font-size:13px;color:#81D4FA">http://localhost:8501</code> 🎉</p>
  </div>

  <!-- ═══ STRUCTURE ═══ -->
  <div class="section">
    <span class="section-label">Codebase</span>
    <h2>📁 Project Structure</h2>
    <div class="file-tree">
      <span class="code-line tree-root">fire-path-planner/</span>
      <span class="code-line">│</span>
      <span class="code-line">├── <span class="tree-file">main.py</span>                  <span class="tree-comment"># Streamlit app entry point & dashboard UI</span></span>
      <span class="code-line">├── <span class="tree-file">fire_calculator.py</span>       <span class="tree-comment"># FIRE target, SIP & roadmap engine</span></span>
      <span class="code-line">├── <span class="tree-file">health_score.py</span>          <span class="tree-comment"># Money Health Score (6-dimension scoring)</span></span>
      <span class="code-line">├── <span class="tree-file">goal_planner.py</span>          <span class="tree-comment"># Goal-based SIP calculator</span></span>
      <span class="code-line">├── <span class="tree-file">insurance.py</span>             <span class="tree-comment"># Insurance recommendation logic</span></span>
      <span class="code-line">├── <span class="tree-file">ai_insights.py</span>           <span class="tree-comment"># OpenAI API integration</span></span>
      <span class="code-line">├── <span class="tree-file">requirements.txt</span>         <span class="tree-comment"># Python dependencies</span></span>
      <span class="code-line">└── <span class="tree-file">README.md</span></span>
    </div>
  </div>

  <!-- ═══ IMPACT ═══ -->
  <div class="section">
    <span class="section-label">Business Value</span>
    <h2>📊 Impact Model</h2>
    <div class="impact-grid">
      <div class="impact-card">
        <div class="impact-value">10,000</div>
        <div class="impact-label">Target users in Year 1 (young professionals)</div>
      </div>
      <div class="impact-card">
        <div class="impact-value">₹5K–15K</div>
        <div class="impact-label">Financial advisor cost saved per user per year</div>
      </div>
      <div class="impact-card">
        <div class="impact-value">₹15 Cr</div>
        <div class="impact-label">Total value delivered annually</div>
      </div>
      <div class="impact-card">
        <div class="impact-value">&lt; 2 min</div>
        <div class="impact-label">To generate a full plan (vs hours with advisor)</div>
      </div>
    </div>
  </div>

  <!-- ═══ TEAM ═══ -->
  <div class="section">
    <span class="section-label">The Team</span>
    <h2>👥 Built By</h2>
    <div class="team-grid">
      <div class="team-card">
        <div class="avatar">K</div>
        <div>
          <div class="team-name">Khushali</div>
          <div class="team-role">Co-founder & Developer</div>
        </div>
      </div>
      <div class="team-card">
        <div class="avatar" style="background:linear-gradient(135deg,var(--accent),var(--teal))">T</div>
        <div>
          <div class="team-name">Teammate</div>
          <div class="team-role">Co-founder & Developer</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ═══ ROADMAP ═══ -->
  <div class="section">
    <span class="section-label">What's Next</span>
    <h2>🔮 Future Roadmap</h2>
    <ul class="roadmap-list">
      <li class="roadmap-item"><span class="todo-box"></span>NLP-based conversational input (spaCy)</li>
      <li class="roadmap-item"><span class="todo-box"></span>Asset allocation glide path visualization</li>
      <li class="roadmap-item"><span class="todo-box"></span>Tax-saving (80C/80D) recommendations</li>
      <li class="roadmap-item"><span class="todo-box"></span>Mobile app (React Native)</li>
      <li class="roadmap-item"><span class="todo-box"></span>Multi-language support (Hindi, Gujarati)</li>
    </ul>
  </div>

  <!-- ═══ LICENSE ═══ -->
  <div class="section">
    <span class="section-label">Legal</span>
    <h2>📄 License</h2>
    <p>This project is licensed under the MIT License — see the <a href="#" style="color:var(--fire)">LICENSE</a> file for details.</p>
  </div>

</div>

<!-- ═══════════════════ FOOTER ═══════════════════ -->
<div class="footer">
  <span class="footer-heart">❤️‍🔥</span>
  <div class="footer-headline">Built with love for financial freedom</div>
  <p class="footer-quote">"The best time to start planning for FIRE was yesterday. The second best time is now."</p>
</div>

</body>
</html>
