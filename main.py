# ============================================================
#  main.py  —  CLI version of the FIRE Planner
# ============================================================
from calculator import (
    calculate_fire_plan,
    calculate_goal_plan,
    calculate_insurance,
    calculate_money_health_score,
)


def separator(title=""):
    line = "─" * 45
    if title:
        print(f"\n{line}\n  {title}\n{line}")
    else:
        print(line)


def main():
    print("\n🔥  AI Financial Independence Advisor  🔥")
    separator()

    # ── Inputs ────────────────────────────────────────────────
    try:
        age        = int(input("Enter your age: "))
        retire_age = int(input("Target retirement age: "))
        income     = float(input("Monthly income (₹): "))
        expenses   = float(input("Monthly expenses (₹): "))
        savings    = float(input("Current savings (₹): "))
    except ValueError:
        print("❌ Invalid input — please enter numbers only.")
        return

    # ── Validation ────────────────────────────────────────────
    if retire_age <= age:
        print("❌ Retirement age must be greater than current age.")
        return
    if income <= 0:
        print("❌ Monthly income must be greater than ₹0.")
        return
    if expenses >= income:
        print("⚠️  Warning: Expenses ≥ income. Savings rate is 0% or negative.")

    # ── FIRE Plan ─────────────────────────────────────────────
    plan = calculate_fire_plan(age, retire_age, income, expenses, savings)

    separator("📊 FIRE PLAN")
    print(f"  FIRE Target         : ₹{int(plan['FIRE Target']):,}")
    print(f"  Monthly SIP         : ₹{int(plan['Monthly Investment (SIP)']):,}")
    print(f"  Emergency Fund      : ₹{int(plan['Emergency Fund']):,}")
    print(f"  Equity (at retire)  : {plan['Equity Allocation']}")
    print(f"  Debt (at retire)    : {plan['Debt Allocation']}")
    print(f"  Savings Analysis    : {plan['Savings Analysis']}")
    print(f"  Feasibility         : {plan['Retirement Feasibility']}")
    print(f"  ELSS SIP (80C)      : ₹{int(plan['ELSS SIP (80C)']):,} / month")
    print(f"  Est. Tax Saved      : ₹{int(plan['Est. Tax Saved (₹/yr)']):,} / year")

    # ── Insurance ─────────────────────────────────────────────
    insurance = calculate_insurance(income, age)
    separator("🛡  INSURANCE")
    print(f"  Life Cover Needed   : ₹{int(insurance['Life Insurance Needed']):,}")
    print(f"  Health Cover Needed : ₹{int(insurance['Health Insurance Suggested']):,}")

    # ── Roadmap ───────────────────────────────────────────────
    separator("📅 LONG-TERM ROADMAP (yearly)")
    roadmap = plan["Roadmap"]
    if roadmap:
        for m in roadmap:
            eq  = m.get("Equity %", "—")
            dbt = m.get("Debt %",   "—")
            print(f"  Year {m['Year']:>3}  →  ₹{int(m['Total Value']):>12,}  "
                  f"[Equity {eq}% | Debt {dbt}%]")
    else:
        print("  No roadmap data — check inputs.")

    # ── Goal Planning ─────────────────────────────────────────
    separator("🎯 GOAL PLANNING")
    goal_choice = input("Do you have a financial goal? (yes/no): ").strip().lower()

    if goal_choice == "yes":
        goal_name   = input("Goal name: ")
        try:
            goal_amount = float(input("Goal amount (₹): "))
            goal_years  = int(input("Years to achieve goal: "))
        except ValueError:
            print("❌ Invalid goal input.")
            goal_amount = goal_years = 0

        if goal_amount > 0 and goal_years > 0:
            sip_goal  = calculate_goal_plan(goal_amount, goal_years)
            total_sip = plan["Monthly Investment (SIP)"] + sip_goal
            print(f"\n  Goal: {goal_name}")
            print(f"  Goal SIP      : ₹{int(sip_goal):,} / month")
            print(f"  FIRE SIP      : ₹{int(plan['Monthly Investment (SIP)']):,} / month")
            print(f"  ─────────────────────────────────")
            print(f"  Total Monthly : ₹{int(total_sip):,} / month")

    # ── Health Score ──────────────────────────────────────────
    score, breakdown = calculate_money_health_score(
        income, expenses, savings, age, plan["Monthly Investment (SIP)"]
    )

    separator("💯 MONEY HEALTH SCORE")
    print(f"  Overall Score : {score} / 100")

    if score >= 80:
        print("  Rating        : Excellent 🚀")
    elif score >= 60:
        print("  Rating        : Good 👍")
    else:
        print("  Rating        : Needs Improvement ⚠️")

    max_scores = {
        "Emergency": 20, "Investment": 15, "Debt": 15,
        "Tax": 15, "Retirement": 20, "Insurance": 15,
    }
    print("\n  Dimension Breakdown:")
    for dim, val in breakdown.items():
        mx  = max_scores.get(dim, 20)
        bar = "█" * int((val / mx) * 10) + "░" * (10 - int((val / mx) * 10))
        print(f"    {dim:<12} {bar}  {val}/{mx}")

    # ── Suggestions ───────────────────────────────────────────
    separator("💡 SUGGESTIONS")
    weakest = min(breakdown, key=breakdown.get)
    print(f"  Focus on: {weakest}\n")

    suggestions = {
        "Emergency":  [
            "Build an emergency fund equal to 6 months of expenses.",
            f"Target ₹{int(expenses * 6):,}. Use a liquid fund or high-yield savings account.",
        ],
        "Investment": [
            "Increase your monthly SIP to at least 20% of income.",
            "Consider low-cost index funds (Nifty 50/Next 50 ETFs).",
        ],
        "Debt": [
            "Reduce your expense-to-income ratio below 40%.",
            "Identify non-essential expenses and redirect them to SIP.",
        ],
        "Tax": [
            "Invest ₹12,500/month in ELSS to fully use Section 80C (₹1.5L/year).",
            "Also consider NPS for extra ₹50,000 deduction under 80CCD(1B).",
        ],
        "Retirement": [
            "Increase SIP to at least 20% of income for retirement readiness.",
            "Small increases now have a huge impact over 20+ years due to compounding.",
        ],
        "Insurance": [
            f"Get a term life cover of ₹{int(insurance['Life Insurance Needed']):,}.",
            "Premiums are lowest when you're young — act now.",
        ],
    }

    for tip in suggestions.get(weakest, []):
        print(f"  • {tip}")

    print("\n✅  Analysis complete. Happy investing! 🚀")


if __name__ == "__main__":
    main()