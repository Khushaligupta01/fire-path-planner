# ============================================================
#  app.py  —  FIRE Planner  |  Polished Streamlit UI
#  v2.1 — Plotly removed, Matplotlib used (Python 3.14 safe)
# ============================================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import google.generativeai as genai
from calculator import (
    calculate_fire_plan,
    calculate_goal_plan,
    calculate_insurance,
    calculate_money_health_score,
)

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="FIRE Planner — AI Financial Advisor",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Sora', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

[data-testid="metric-container"] {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border: 1px solid rgba(99,179,237,0.2);
  border-radius: 16px;
  padding: 20px 24px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.3);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="metric-container"]:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(99,179,237,0.15);
}
[data-testid="metric-container"] label {
  font-size: 12px !important;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #63b3ed !important;
  font-weight: 600;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 26px !important;
  font-weight: 600;
  color: #f0f4f8 !important;
}
.section-header {
  font-size: 22px;
  font-weight: 700;
  color: #e2e8f0;
  margin: 32px 0 16px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid rgba(99,179,237,0.3);
  letter-spacing: -0.02em;
}
.info-card {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border: 1px solid rgba(99,179,237,0.15);
  border-radius: 14px;
  padding: 20px 24px;
  margin-bottom: 16px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.2);
  height: 100%;
}
.info-card h4 {
  color: #63b3ed;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 12px;
  font-weight: 600;
}
.info-card p { color: #e2e8f0; font-size: 15px; margin: 6px 0; }
.tip-bullet {
  background: rgba(99,179,237,0.07);
  border-left: 3px solid #63b3ed;
  border-radius: 0 8px 8px 0;
  padding: 10px 16px;
  margin-bottom: 10px;
  color: #cbd5e0;
  font-size: 14px;
  line-height: 1.6;
}
.ai-box {
  background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
  border: 1px solid rgba(99,179,237,0.25);
  border-radius: 16px;
  padding: 24px 28px;
  color: #e2e8f0;
  font-size: 15px;
  line-height: 1.8;
  box-shadow: 0 4px 32px rgba(0,0,0,0.3);
}
.score-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 56px;
  font-weight: 700;
  background: linear-gradient(135deg, #63b3ed, #0ea5e9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 8px;
}
.custom-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(99,179,237,0.3), transparent);
  margin: 32px 0;
}
.disclaimer-box {
  background: rgba(245,158,11,0.06);
  border: 1px solid rgba(245,158,11,0.2);
  border-radius: 10px;
  padding: 10px 16px;
  color: #92400e;
  font-size: 12px;
  text-align: center;
  margin-top: 8px;
  line-height: 1.5;
}
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
  border-right: 1px solid rgba(99,179,237,0.1);
}
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stTextInput label {
  color: #8b949e;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
}
.stButton > button {
  background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 12px;
  padding: 14px 20px;
  font-family: 'Sora', sans-serif;
  font-size: 15px;
  font-weight: 600;
  width: 100%;
  box-shadow: 0 4px 16px rgba(14,165,233,0.3);
}
.stButton > button:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 24px rgba(14,165,233,0.45);
}
</style>
""", unsafe_allow_html=True)

# ── Chart colour palette ──────────────────────────────────────
BG      = "#0d1117"
BG2     = "#161b22"
BLUE    = "#0ea5e9"
BLUE2   = "#38bdf8"
GREEN   = "#10b981"
RED     = "#ef4444"
MUTED   = "#4a5568"
TEXT    = "#e2e8f0"
SUBTEXT = "#718096"

def set_dark_style(fig, ax):
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG2)
    ax.tick_params(colors=SUBTEXT, labelsize=10)
    ax.xaxis.label.set_color(SUBTEXT)
    ax.yaxis.label.set_color(SUBTEXT)
    for spine in ax.spines.values():
        spine.set_edgecolor(MUTED)
        spine.set_linewidth(0.4)
    ax.grid(color=MUTED, linewidth=0.3, alpha=0.4)

# ── Gemini Setup ─────────────────────────────────────────────
def get_gemini_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.environ.get("GEMINI_API_KEY", "")

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📝 Your Profile")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    age          = st.number_input("Age",                       18, 70,  22, 1)
    retire_age   = st.number_input("Retirement Age",            25, 75,  60, 1)
    income       = st.number_input("Monthly Income (₹)",         0, 10_000_000, 30_000, 1_000)
    expenses     = st.number_input("Monthly Expenses (₹)",      0, 10_000_000, 15_000, 500)
    savings      = st.number_input("Current Savings (₹)",       0, 100_000_000, 50_000, 1_000)
    existing_sip = st.number_input("Existing Monthly SIP (₹)",  0, 1_000_000, 0, 500,
                                   help="Any SIP you already run every month")
    st.markdown("---")
    st.markdown("## 🎯 Optional Goal")
    goal_name   = st.text_input("Goal Name", "")
    goal_amount = st.number_input("Goal Amount (₹)",  0, 100_000_000, 0, 10_000)
    goal_years  = st.number_input("Years to Goal",    0, 50, 0, 1)
    st.markdown("---")
    st.markdown("## 🔑 Gemini API Key")
    gemini_key_input = st.text_input(
        "API Key (optional — or set in secrets)",
        value="", type="password",
        help="Get a free key at aistudio.google.com"
    )
    st.markdown("""
    <div class="disclaimer-box">
      ⚠️ For educational purposes only.<br>Not financial advice.
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    generate = st.button("Generate Plan 🚀", use_container_width=True)


# ── Hero ─────────────────────────────────────────────────────
st.markdown("""
<div style="padding:8px 0 24px 0;">
  <h1 style="font-family:'Sora',sans-serif;font-size:36px;font-weight:700;
     background:linear-gradient(135deg,#63b3ed,#0ea5e9,#38bdf8);
     -webkit-background-clip:text;-webkit-text-fill-color:transparent;
     background-clip:text;margin:0;letter-spacing:-0.03em;">
    🔥 AI Financial Independence Advisor
  </h1>
  <p style="color:#4a5568;font-size:15px;margin:8px 0 0 0;">
    Inflation-adjusted FIRE planning · 6-dimension health score · Gemini AI insights
  </p>
</div>
""", unsafe_allow_html=True)

if not generate:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);
      border:1px solid rgba(99,179,237,0.15);border-radius:20px;
      padding:48px;text-align:center;margin-top:16px;">
      <div style="font-size:56px;margin-bottom:16px;">🏦</div>
      <h3 style="color:#e2e8f0;font-family:'Sora',sans-serif;font-weight:600;
        font-size:22px;margin-bottom:12px;">Ready to plan your financial independence?</h3>
      <p style="color:#718096;font-size:15px;max-width:480px;margin:0 auto;line-height:1.7;">
        Fill in your profile in the sidebar and click
        <strong style="color:#63b3ed">Generate Plan</strong> to get your complete FIRE roadmap,
        money health score, tax-saving tips, and personalised Gemini AI insights.
      </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ── Validation ───────────────────────────────────────────────
errors = []
if retire_age <= age:
    errors.append("Retirement age must be greater than your current age.")
if income <= 0:
    errors.append("Monthly income must be greater than ₹0.")
for e in errors:
    st.error(e)
if errors:
    st.stop()
if expenses >= income:
    st.warning("⚠️ Expenses ≥ Income — savings rate is 0% or negative. Plan may be unrealistic.")


# ── Compute ──────────────────────────────────────────────────
with st.spinner("Crunching your numbers..."):
    plan      = calculate_fire_plan(age, retire_age, income, expenses, savings, existing_sip)
    insurance = calculate_insurance(income, age)
    score, breakdown = calculate_money_health_score(
        income, expenses, savings, age,
        plan["Monthly Investment (SIP)"],
        insurance
    )

sip      = plan["Monthly Investment (SIP)"]
fire_tgt = plan["FIRE Target"]
em_fund  = plan["Emergency Fund"]
roadmap  = plan["Roadmap"]

fire_achieved_year    = plan.get("FIRE Achieved Year")
years_to_fire_display = (
    f"{fire_achieved_year} yrs 🎯" if fire_achieved_year
    else f"{retire_age - age} yrs"
)
fire_early = fire_achieved_year and fire_achieved_year < (retire_age - age)

MAX_SCORES = {"Emergency":20,"Investment":15,"Debt":15,"Tax":15,"Retirement":20,"Insurance":15}
DIM_COLORS = {
    "Emergency":"#0ea5e9","Investment":"#10b981","Debt":"#8b5cf6",
    "Tax":"#f59e0b","Retirement":"#ef4444","Insurance":"#ec4899"
}


# ═══ SECTION 1: Key Metrics ══════════════════════════════════
st.markdown('<div class="section-header">📊 Key Metrics</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("🎯 FIRE Target",    f"₹{int(fire_tgt):,}")
c2.metric("💰 Additional SIP", f"₹{int(sip):,}")
c3.metric("🛡 Emergency Fund", f"₹{int(em_fund):,}")
c4.metric("⏳ Years to FIRE",  years_to_fire_display)
c5.metric("💹 Health Score",   f"{score}/100")
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

if existing_sip > 0:
    st.info(f"✅ Your existing SIP of ₹{int(existing_sip):,}/month is factored in. "
            f"You need ₹{int(sip):,}/month **additional** on top of that.")
if fire_early:
    st.success(
        f"🎉 You can reach FIRE in just **{fire_achieved_year} years** — "
        f"{retire_age - age - fire_achieved_year} years ahead of your retirement age!"
    )


# ═══ SECTION 2: Plan Details ═════════════════════════════════
st.markdown('<div class="section-header">📋 Plan Details</div>', unsafe_allow_html=True)
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown(f"""
    <div class="info-card">
      <h4>Financial Overview</h4>
      <p>{plan['Savings Analysis']}</p>
      <p>{plan['Retirement Feasibility']}</p>
      <p style="margin-top:10px;color:#718096;font-size:13px;">
        Equity at retirement: <strong style="color:#63b3ed">{plan['Equity Allocation']}</strong>
        &nbsp;|&nbsp; Debt: <strong style="color:#63b3ed">{plan['Debt Allocation']}</strong>
      </p>
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown(f"""
    <div class="info-card">
      <h4>💸 Tax-Saving (80C / NPS)</h4>
      <p>ELSS SIP: <strong style="color:#48bb78">₹{int(plan['ELSS SIP (80C)']):,}</strong> / month</p>
      <p>Est. Tax Saved: <strong style="color:#48bb78">₹{int(plan['Est. Tax Saved (₹/yr)']):,}</strong> / year</p>
      <p style="color:#718096;font-size:12px;margin-top:10px;line-height:1.5;">
        ELSS qualifies for Section 80C (₹1.5L/year limit).
        Add NPS for extra ₹50,000 deduction (80CCD 1B).
      </p>
    </div>""", unsafe_allow_html=True)

with col_c:
    st.markdown(f"""
    <div class="info-card">
      <h4>🛡 Insurance Recommendations</h4>
      <p>Life Cover: <strong style="color:#f6ad55">₹{int(insurance['Life Insurance Needed']):,}</strong></p>
      <p>Health Cover: <strong style="color:#f6ad55">₹{int(insurance['Health Insurance Suggested']):,}</strong></p>
      <p style="color:#718096;font-size:12px;margin-top:10px;line-height:1.5;">
        Life cover = 10× annual income.
        Health cover scales with age (₹5L → ₹10L → ₹20L).
      </p>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


# ═══ SECTION 3: Roadmap Chart (Matplotlib) ═══════════════════
st.markdown('<div class="section-header">📈 Portfolio Growth Roadmap</div>', unsafe_allow_html=True)
st.caption("Real return ~5.66% p.a. (inflation-adjusted) · Glide-path equity allocation shifts yearly")

if roadmap:
    df = pd.DataFrame(roadmap)
    tab1, tab2 = st.tabs(["📈 Chart", "📋 Data Table"])

    with tab1:
        fig, ax = plt.subplots(figsize=(12, 4.5))
        set_dark_style(fig, ax)

        years  = df["Year"].values
        values = df["Total Value"].values

        # Smooth interpolation
        x_smooth = np.linspace(years.min(), years.max(), 300)
        y_smooth  = np.interp(x_smooth, years, values)

        ax.fill_between(x_smooth, y_smooth, alpha=0.12, color=BLUE)
        ax.plot(x_smooth, y_smooth, color=BLUE, linewidth=2.5, label="Portfolio Value")

        # FIRE target line
        ax.axhline(y=fire_tgt, color=RED, linewidth=1.2, linestyle="--", alpha=0.7)
        ax.text(years.max() * 0.02, fire_tgt * 1.03,
                f"FIRE Target ₹{int(fire_tgt):,}", color=RED, fontsize=9, alpha=0.85)

        # 5-year milestones
        milestones = df[df["Year"] % 5 == 0]
        if not milestones.empty:
            ax.scatter(milestones["Year"], milestones["Total Value"],
                       color=BLUE2, s=60, zorder=5, label="5-yr milestone")

        # FIRE star marker
        if fire_achieved_year and fire_achieved_year in df["Year"].values:
            fire_val = df[df["Year"] == fire_achieved_year]["Total Value"].values[0]
            ax.scatter([fire_achieved_year], [fire_val],
                       color=GREEN, s=200, marker="*", zorder=6, label="FIRE Achieved")
            ax.annotate("FIRE! 🎯", xy=(fire_achieved_year, fire_val),
                        xytext=(fire_achieved_year + 0.5, fire_val * 1.06),
                        color=GREEN, fontsize=9, fontweight="bold")

        # Y-axis formatter: ₹L / ₹Cr
        def rupee_fmt(x, _):
            if x >= 1e7:   return f"₹{x/1e7:.1f}Cr"
            elif x >= 1e5: return f"₹{x/1e5:.0f}L"
            else:          return f"₹{int(x):,}"

        ax.yaxis.set_major_formatter(plt.FuncFormatter(rupee_fmt))
        ax.set_xlabel("Year", fontsize=11)
        ax.set_ylabel("Portfolio Value", fontsize=11)
        ax.legend(facecolor=BG2, edgecolor=MUTED, labelcolor=TEXT, fontsize=10)
        ax.set_xlim(1, years.max())
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close()

        if fire_early:
            st.success(
                f"🎯 Chart ends at Year {fire_achieved_year} — FIRE target hit "
                f"{retire_age - age - fire_achieved_year} years ahead of schedule!"
            )

    with tab2:
        df_show = df.copy()
        df_show["Total Value"] = df_show["Total Value"].apply(lambda x: f"₹{int(x):,}")
        df_show["Equity %"]    = df_show["Equity %"].apply(lambda x: f"{x}%")
        df_show["Debt %"]      = df_show["Debt %"].apply(lambda x: f"{x}%")
        st.dataframe(df_show, use_container_width=True, hide_index=True)
else:
    st.warning("No roadmap data — please check your inputs.")

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


# ═══ SECTION 4: Goal Planning ════════════════════════════════
if goal_amount > 0 and goal_years > 0:
    st.markdown('<div class="section-header">🎯 Goal Planning</div>', unsafe_allow_html=True)
    sip_goal  = calculate_goal_plan(goal_amount, goal_years)
    total_sip = sip_goal + sip + existing_sip
    label     = goal_name.strip() or "Your Goal"
    g1, g2, g3, g4 = st.columns(4)
    g1.metric(f"Goal: {label}",    f"₹{int(goal_amount):,}")
    g2.metric("Goal SIP / month",  f"₹{int(sip_goal):,}")
    g3.metric("FIRE SIP / month",  f"₹{int(sip):,}")
    g4.metric("Total Monthly SIP", f"₹{int(total_sip):,}",
              delta=f"incl. ₹{int(existing_sip):,} existing" if existing_sip else None)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


# ═══ SECTION 5: Money Health Score ═══════════════════════════
st.markdown('<div class="section-header">💯 Money Health Score</div>', unsafe_allow_html=True)

sc_left, sc_right = st.columns([1, 2])

with sc_left:
    if score >= 80:
        rating, rating_color, rating_icon = "Excellent", "#10b981", "🟢"
    elif score >= 60:
        rating, rating_color, rating_icon = "Good", "#f59e0b", "🟡"
    else:
        rating, rating_color, rating_icon = "Needs Work", "#ef4444", "🔴"

    st.markdown(f"""
    <div class="info-card" style="text-align:center;padding:32px 24px;">
      <div class="score-badge">{score}</div>
      <div style="color:#718096;font-size:14px;margin-bottom:16px;">out of 100</div>
      <div style="background:rgba(255,255,255,0.06);border-radius:100px;
                  height:8px;width:100%;overflow:hidden;margin-bottom:16px;">
        <div style="height:100%;width:{score}%;
                    background:linear-gradient(90deg,#0ea5e9,#38bdf8);
                    border-radius:100px;"></div>
      </div>
      <div style="color:{rating_color};font-size:18px;font-weight:600;">
        {rating_icon} {rating}
      </div>
    </div>""", unsafe_allow_html=True)

with sc_right:
    dims   = list(breakdown.keys())
    vals   = [breakdown[d] for d in dims]
    maxes  = [MAX_SCORES[d] for d in dims]
    pcts   = [v / m * 100 for v, m in zip(vals, maxes)]
    colors = [DIM_COLORS.get(d, BLUE) for d in dims]

    fig2, ax2 = plt.subplots(figsize=(8, 3.2))
    set_dark_style(fig2, ax2)

    y_pos = list(range(len(dims)))
    ax2.barh(y_pos, [100]*len(dims), color="white", alpha=0.05, height=0.5)
    bars = ax2.barh(y_pos, pcts, color=colors, alpha=0.85, height=0.5)

    for i, (v, m, pct) in enumerate(zip(vals, maxes, pcts)):
        ax2.text(min(pct + 2, 108), i, f"{v}/{m}", va="center", color=TEXT, fontsize=10)

    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(dims, fontsize=11, color=TEXT)
    ax2.set_xlim(0, 130)
    ax2.invert_yaxis()
    ax2.xaxis.set_visible(False)
    for spine in ax2.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    st.pyplot(fig2, use_container_width=True)
    plt.close()

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


# ═══ SECTION 6: Personalised Suggestions ═════════════════════
st.markdown('<div class="section-header">💡 Personalised Suggestions</div>', unsafe_allow_html=True)

weakest       = min(breakdown, key=breakdown.get)
expense_ratio = int(expenses / income * 100) if income > 0 else 0

st.markdown(f"""
<div style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.3);
  border-radius:12px;padding:14px 20px;margin-bottom:20px;display:flex;
  align-items:center;gap:12px;">
  <span style="font-size:20px;">⚠️</span>
  <span style="color:#fbbf24;font-weight:600;font-size:15px;">
    Weakest area: {weakest}
    <span style="font-weight:400;color:#d97706;">
      ({breakdown[weakest]}/{MAX_SCORES[weakest]} pts)
    </span>
  </span>
</div>""", unsafe_allow_html=True)

SUGGESTIONS = {
    "Emergency": [
        f"Build an emergency fund of ₹{int(expenses*6):,} (6 months of expenses).",
        "Keep it in a liquid mutual fund or high-yield savings account — not your regular account.",
        "Automate a monthly transfer until you hit the target.",
    ],
    "Investment": [
        "Increase your SIP to at least 20% of income — your current rate is below this threshold.",
        "Start with a Nifty 50 index fund for low-cost, broad market exposure.",
        "Even ₹500/month more today makes a significant corpus difference over 20 years.",
    ],
    "Debt": [
        f"Your expense-to-income ratio is {expense_ratio}% — aim for below 40%.",
        "List all discretionary expenses and cut the bottom 20% ruthlessly.",
        "Every ₹1,000/month saved and redirected to SIP = ₹1L+ extra in 10 years.",
    ],
    "Tax": [
        f"Invest ₹{int(plan['ELSS SIP (80C)']):,}/month in ELSS to fully use Section 80C (₹1.5L/year limit).",
        "Add NPS for an extra ₹50,000 deduction under 80CCD(1B) — saves ₹5,000–₹15,000/year in tax.",
        "Health insurance premium (₹25,000) also qualifies under Section 80D.",
    ],
    "Retirement": [
        "Your SIP is below the 20% income threshold needed for strong retirement readiness.",
        "Use SIP step-up (increase by 10% each year) to grow contributions painlessly.",
        "Open a PPF account (₹500/year minimum) for tax-free retirement income on maturity.",
    ],
    "Insurance": [
        f"Get a term life cover of ₹{int(insurance['Life Insurance Needed']):,} — premiums are lowest now.",
        f"Target health insurance of ₹{int(insurance['Health Insurance Suggested']):,} — medical inflation runs 12%+ p.a.",
        "Avoid ULIPs and endowment plans — buy pure term + invest the rest separately.",
        "Use PolicyBazaar or Ditto to compare term plans and buy online (lowest premiums).",
    ],
}

for tip in SUGGESTIONS.get(weakest, []):
    st.markdown(f'<div class="tip-bullet">{tip}</div>', unsafe_allow_html=True)

with st.expander("View tips for all dimensions"):
    for dim, tips in SUGGESTIONS.items():
        color = DIM_COLORS.get(dim, BLUE)
        st.markdown(f"""
        <div style="margin-bottom:16px;">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
            <span style="width:10px;height:10px;border-radius:50%;
                         background:{color};display:inline-block;"></span>
            <strong style="color:#e2e8f0;font-size:14px;">{dim}</strong>
            <span style="color:#718096;font-size:12px;">
              {breakdown[dim]}/{MAX_SCORES[dim]}
            </span>
          </div>""", unsafe_allow_html=True)
        for tip in tips:
            st.markdown(f'<div class="tip-bullet" style="margin-left:20px;">{tip}</div>',
                        unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)


# ═══ SECTION 7: Gemini AI Insights ═══════════════════════════
st.markdown('<div class="section-header">🤖 AI Insights — Powered by Gemini</div>',
            unsafe_allow_html=True)

def build_gemini_prompt():
    return f"""You are an expert Indian personal finance advisor. Analyse this user's FIRE plan and give sharp,
personalised, actionable advice. Be direct, specific, and use Indian financial context (₹, SIP, ELSS, NPS, 80C, PPF).

USER PROFILE:
- Age: {age} | Target Retirement Age: {retire_age}
- Monthly Income: ₹{int(income):,} | Monthly Expenses: ₹{int(expenses):,}
- Current Savings: ₹{int(savings):,} | Existing SIP: ₹{int(existing_sip):,}/month

FIRE PLAN RESULTS:
- FIRE Target: ₹{int(fire_tgt):,}
- Additional SIP Needed: ₹{int(sip):,}/month
- Emergency Fund Target: ₹{int(em_fund):,}
- FIRE Achieved in: {fire_achieved_year if fire_achieved_year else retire_age - age} years
- Equity/Debt at Retirement: {plan['Equity Allocation']} / {plan['Debt Allocation']}
- ELSS SIP (80C): ₹{int(plan['ELSS SIP (80C)']):,}/month
- Est. Tax Saved: ₹{int(plan['Est. Tax Saved (₹/yr)']):,}/year
- Savings Analysis: {plan['Savings Analysis']}
- Retirement Feasibility: {plan['Retirement Feasibility']}

MONEY HEALTH SCORE: {score}/100
Dimension Breakdown: {breakdown}
Weakest Dimension: {weakest}

INSURANCE NEEDS:
- Life Cover: ₹{int(insurance['Life Insurance Needed']):,}
- Health Cover: ₹{int(insurance['Health Insurance Suggested']):,}

Please provide:
1. **Overall Assessment** — 2-3 sentences on where this person stands
2. **Top 3 Immediate Actions** — specific, numbered, with rupee amounts where relevant
3. **Hidden Risk** — one thing they might be overlooking
4. **One Motivating Insight** — something encouraging based on their numbers

Keep total response under 350 words. Use markdown formatting. Be honest but encouraging."""


def get_gemini_insights(api_key: str) -> str:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(build_gemini_prompt())
        return response.text
    except Exception as e:
        return f"⚠️ Gemini error: {str(e)}"


api_key = gemini_key_input.strip() or get_gemini_key()

if api_key:
    if st.button("✨ Generate AI Insights", use_container_width=True):
        with st.spinner("Gemini is analysing your financial profile..."):
            insight_text = get_gemini_insights(api_key)
        st.markdown(f'<div class="ai-box">{insight_text}</div>', unsafe_allow_html=True)
        st.caption("🤖 Generated by Google Gemini 1.5 Flash · For educational purposes only")
    else:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);
          border:1px solid rgba(99,179,237,0.15);border-radius:16px;
          padding:28px;text-align:center;">
          <div style="font-size:36px;margin-bottom:10px;">✨</div>
          <p style="color:#e2e8f0;font-size:16px;font-weight:600;margin-bottom:6px;">
            Gemini AI is ready
          </p>
          <p style="color:#718096;font-size:14px;max-width:400px;margin:0 auto;">
            Click the button above to get personalised analysis of your FIRE plan,
            hidden risks, and top action items — powered by Google Gemini.
          </p>
        </div>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);
      border:1px solid rgba(245,158,11,0.2);border-radius:16px;
      padding:28px;text-align:center;">
      <div style="font-size:36px;margin-bottom:10px;">🔑</div>
      <p style="color:#e2e8f0;font-size:16px;font-weight:600;margin-bottom:6px;">
        Add your Gemini API key to unlock AI Insights
      </p>
      <p style="color:#718096;font-size:14px;max-width:440px;margin:0 auto;line-height:1.7;">
        Get a <strong style="color:#fbbf24">free key</strong> at
        <a href="https://aistudio.google.com" target="_blank"
           style="color:#63b3ed;">aistudio.google.com</a>
        and paste it in the sidebar, or set
        <code style="color:#a78bfa;">GEMINI_API_KEY</code> in
        <code style="color:#a78bfa;">.streamlit/secrets.toml</code>.
      </p>
    </div>""", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:40px 0 20px 0;color:#2d3748;font-size:12px;letter-spacing:0.05em;">
  🔥 FIRE Planner · For educational purposes only · Not financial advice · Built with Streamlit + Gemini AI
</div>""", unsafe_allow_html=True)