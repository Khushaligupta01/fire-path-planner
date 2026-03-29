# ============================================================
#  calculator.py  —  FIRE Planner + Money Health Score
# ============================================================

def calculate_fire_plan(age, retire_age, income, expenses, savings):
    """
    Returns a complete FIRE plan dict with:
      - FIRE Target, Emergency Fund, SIP
      - Glide-path equity/debt allocation (shifts yearly toward retirement)
      - Inflation-adjusted real return (~5.66%)
      - Full yearly roadmap until FIRE target is hit or retirement
      - Tax-saving headroom (80C / ELSS)
    """

    annual_expenses = expenses * 12
    fire_target = annual_expenses * 25          # 4% safe withdrawal rule
    emergency_fund = expenses * 6               # 6-month buffer

    years_left = max(retire_age - age, 0)
    months     = years_left * 12

    # ── Inflation-adjusted real return ──────────────────────
    nominal_rate = 0.12
    inflation    = 0.06
    real_rate    = ((1 + nominal_rate) / (1 + inflation)) - 1   # ≈ 5.66 %
    monthly_rate = real_rate / 12

    # ── SIP needed to reach FIRE target ─────────────────────
    future_value = max(fire_target - savings * ((1 + monthly_rate) ** months), 0)

    if months > 0 and monthly_rate > 0:
        denominator = ((1 + monthly_rate) ** months - 1)
        sip = (future_value * monthly_rate / denominator) if denominator else 0
    else:
        sip = 0

    sip = max(sip, income * 0.20)   # floor: at least 20 % of income

    # ── Tax-saving headroom (Section 80C cap = ₹1.5L/year) ──
    annual_sip      = sip * 12
    elss_limit      = 150000         # 80C ceiling
    elss_sip        = min(annual_sip * equity_at_age(age), elss_limit) / 12
    tax_saved_80c   = min(elss_sip * 12, elss_limit) * marginal_tax_rate(income * 12)

    # ── Savings-rate comment ─────────────────────────────────
    savings_rate = (income - expenses) / income if income > 0 else 0
    if savings_rate < 0.20:
        advice = "⚠️ Low savings rate — try to cut expenses"
    elif savings_rate < 0.40:
        advice = "👍 Decent savings rate"
    else:
        advice = "🚀 Excellent savings rate!"

    # ── Retirement feasibility ───────────────────────────────
    if years_left <= 0:
        retirement_msg = "❌ Invalid retirement age"
    elif years_left < 10:
        retirement_msg = "⚠️ Very aggressive — needs high SIP discipline"
    else:
        retirement_msg = "✅ Achievable with consistent investing"

    # ── Full yearly roadmap with glide-path allocation ───────
    balance = savings
    roadmap  = []

    for month in range(1, months + 1):
        current_age = age + (month - 1) / 12
        eq = equity_at_age(current_age)
        balance += balance * monthly_rate + sip

        if month % 12 == 0:
            year = month // 12
            roadmap.append({
                "Year":        year,
                "Total Value": round(balance, 2),
                "Equity %":    round(eq * 100, 1),
                "Debt %":      round((1 - eq) * 100, 1),
            })

        if balance >= fire_target:
            break

    # Edge-case: horizon < 1 year
    if not roadmap and months > 0:
        roadmap.append({
            "Year":        1,
            "Total Value": round(balance, 2),
            "Equity %":    round(equity_at_age(age) * 100, 1),
            "Debt %":      round((1 - equity_at_age(age)) * 100, 1),
        })

    # Final-year allocation (for display)
    final_eq = equity_at_age(retire_age)

    return {
        "FIRE Target":              round(fire_target, 2),
        "Emergency Fund":           round(emergency_fund, 2),
        "Monthly Investment (SIP)": round(sip, 2),
        "Equity Allocation":        f"{final_eq*100:.0f}%",
        "Debt Allocation":          f"{(1-final_eq)*100:.0f}%",
        "Savings Analysis":         advice,
        "Retirement Feasibility":   retirement_msg,
        "ELSS SIP (80C)":           round(elss_sip, 2),
        "Est. Tax Saved (₹/yr)":    round(tax_saved_80c, 2),
        "Roadmap":                  roadmap,
    }


# ── Helper: glide-path equity % ─────────────────────────────
def equity_at_age(age):
    """
    100-minus-age rule, clamped between 30% and 80%.
    Equity drops ~1% per year naturally as age increases.
    """
    equity = (100 - age) / 100
    return round(max(0.30, min(0.80, equity)), 4)


# ── Helper: marginal income-tax rate (India slabs, new regime) ──
def marginal_tax_rate(annual_income):
    if annual_income <= 300000:
        return 0.0
    elif annual_income <= 700000:
        return 0.05
    elif annual_income <= 1000000:
        return 0.10
    elif annual_income <= 1200000:
        return 0.15
    elif annual_income <= 1500000:
        return 0.20
    else:
        return 0.30


# ============================================================
def calculate_goal_plan(goal_amount, years):
    """SIP required to accumulate goal_amount in given years at 10% p.a."""
    if goal_amount <= 0 or years <= 0:
        return 0.0
    rate   = 0.10 / 12
    months = years * 12
    denom  = ((1 + rate) ** months - 1)
    sip    = goal_amount * rate / denom if denom else 0
    return round(sip, 2)


# ============================================================
def calculate_insurance(income, age):
    """
    Life cover: 10× annual income (thumb rule).
    Health cover: ₹5L under 40, ₹10L at 40+, ₹20L at 55+.
    """
    annual_income  = income * 12
    life_cover     = annual_income * 10

    if age < 40:
        health_cover = 500_000
    elif age < 55:
        health_cover = 1_000_000
    else:
        health_cover = 2_000_000

    return {
        "Life Insurance Needed":     round(life_cover, 2),
        "Health Insurance Suggested": round(health_cover, 2),
    }


# ============================================================
def calculate_money_health_score(income, expenses, savings, age, sip):
    """
    6-dimension score — max points per dimension:
      Emergency   20
      Investment  15
      Debt        15
      Tax         15
      Retirement  20
      Insurance   15
      ─────────────
      Total      100
    """
    score     = 0
    breakdown = {}

    annual_income = income * 12

    # 1. Emergency fund (20 pts) ─────────────────────────────
    needed = expenses * 6
    em_score = min((savings / needed) * 20, 20) if needed > 0 else 0
    breakdown["Emergency"] = round(em_score, 1)
    score += em_score

    # 2. Investment discipline (15 pts) ──────────────────────
    if income > 0:
        sip_ratio = sip / income
        if sip_ratio >= 0.20:
            inv_score = 15
        elif sip_ratio >= 0.10:
            inv_score = 10
        else:
            inv_score = 5
    else:
        inv_score = 0
    breakdown["Investment"] = inv_score
    score += inv_score

    # 3. Debt / expense health (15 pts) ──────────────────────
    ratio = expenses / income if income > 0 else 1
    if ratio < 0.40:
        debt_score = 15
    elif ratio < 0.60:
        debt_score = 10
    else:
        debt_score = 5
    breakdown["Debt"] = debt_score
    score += debt_score

    # 4. Tax efficiency — 80C usage (15 pts) ─────────────────
    # Reward: SIP ≥ ₹12,500/mo → fully utilising 80C (₹1.5L/yr)
    annual_sip = sip * 12
    if annual_sip >= 150_000:
        tax_score = 15          # fully using 80C
    elif annual_sip >= 75_000:
        tax_score = 10          # partially using 80C
    elif annual_sip >= 36_000:
        tax_score = 6           # some tax-saving investment
    else:
        tax_score = 3           # little to no tax planning
    # Bonus: no income tax if very low income
    if annual_income <= 300_000:
        tax_score = 15          # no tax liability anyway
    breakdown["Tax"] = tax_score
    score += tax_score

    # 5. Retirement readiness (20 pts) ───────────────────────
    if income > 0:
        if sip >= income * 0.20:
            ret_score = 20
        elif sip >= income * 0.10:
            ret_score = 12
        else:
            ret_score = 6
    else:
        ret_score = 0
    breakdown["Retirement"] = ret_score
    score += ret_score

    # 6. Insurance adequacy (15 pts) ─────────────────────────
    ideal_life_cover = annual_income * 10
    # Proxy: if savings cover at least 1 year of income → assumed insured
    if savings >= annual_income:
        ins_score = 15
    elif savings >= annual_income * 0.5:
        ins_score = 10
    else:
        ins_score = 5
    breakdown["Insurance"] = ins_score
    score += ins_score

    return round(score, 1), breakdown