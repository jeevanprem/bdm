# -*- coding: utf-8 -*-
import os
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('bdm_master_dataset.json', 'r', encoding='utf-8') as f:
    master_data = json.load(f)

questions = master_data['questions']
print(f"Loaded {len(questions)} questions.")

def clean_txt(t):
    return re.sub(r'\s+', ' ', (t or '')).strip()

def build_long_solution(q):
    qid = q['id']
    q_txt = clean_txt(q['question'])
    feedback = clean_txt(q.get('feedback', ''))
    week = q.get('week', 1)
    source = q.get('source', '')
    module = q.get('module', '')
    options = q.get('options', [])

    corr_opts = [o for o in options if o.get('is_correct')]
    corr = corr_opts[0] if corr_opts else options[0]
    c_lbl = corr['label']
    c_txt = clean_txt(corr['text'])

    q_lower = q_txt.lower()
    c_lower = c_txt.lower()
    fb_lower = feedback.lower()

    conceptual_exp = ""
    calc = None
    distractor_trap = ""
    hinglish_shortcut = ""

    # Specialized handlers for major cases and standard question patterns
    # 1. GreenFleet001 Optimization Questions (GA1 Q7 & Q8)
    if "greenfleet" in q_lower:
        if "maximum number of electric 2-wheelers" in q_lower or "e2" in q_lower and "deploy" in q_lower:
            conceptual_exp = (
                "In economics, constrained optimization under resource scarcity requires allocating the available budget "
                "after satisfying mandatory fixed commitments. Here, the startup faces a linear daily budget constraint: "
                "100E2 + 400E3 = 20,000. Since the contractual agreement obligates deploying exactly 10 units of Electric "
                "3-Wheelers (E3 = 10), the charging expenditure on E3 is fixed at 10 × ₹400 = ₹4,000. The remaining scarce "
                "financial resource (₹20,000 - ₹4,000 = ₹16,000) is then fully channeled into Electric 2-Wheelers (E2) at "
                "₹100 per vehicle, yielding exactly 160 vehicles."
            )
            calc = (
                "Step 1: Total Daily Charging Budget Cap = ₹20,000\n"
                "Step 2: Mandatory E3 Commitment = 10 vehicles\n"
                "Step 3: Budget consumed by E3 = 10 × ₹400 = ₹4,000\n"
                "Step 4: Remaining Budget for E2 = ₹20,000 - ₹4,000 = ₹16,000\n"
                "Step 5: Maximum E2 deployable = ₹16,000 / ₹100 = 160 vehicles"
            )
            distractor_trap = "Students frequently compute 20,000 / 100 = 200 (Option D), forgetting that 10 E3 vehicles MUST be deployed under contract, which ties up ₹4,000 of charging funds."
            hinglish_shortcut = "Pehle mandatory contract ka ₹4,000 alag karo (20,000 - 4,000 = 16,000), phir ₹100 se divide karo = 160 E2 vehicles!"
        elif "maximum daily profit" in q_lower:
            conceptual_exp = (
                "Total daily profit is the sum of profits generated from both vehicle types operating under the optimal "
                "fleet configuration (160 E2 and 10 E3). Each E2 generates ₹500 in daily net profit, producing ₹80,000. "
                "Each E3 generates ₹1,500 in daily net profit, producing ₹15,000. Summing both yields the maximum achievable "
                "profit of ₹95,000."
            )
            calc = (
                "Step 1: Optimal Fleet Configuration = 160 E2 and 10 E3\n"
                "Step 2: Profit from E2 = 160 × ₹500 = ₹80,000\n"
                "Step 3: Profit from E3 = 10 × ₹1,500 = ₹15,000\n"
                "Step 4: Total Daily Profit = ₹80,000 + ₹15,000 = ₹95,000"
            )
            distractor_trap = "A common mistake is only counting the E2 profit (₹80,000, Option A) and omitting the E3 profit (₹15,000), or assuming 200 E2 vehicles could be run (₹1,00,000, Option C)."
            hinglish_shortcut = "Dono vehicles ka munafa jodo: (160 × 500) + (10 × 1,500) = 80,000 + 15,000 = ₹95,000 total profit!"

    # 2. College Administration ₹50 Lakh Budget (GA1 Q1)
    elif "college administration" in q_lower or "budget of ₹50" in q_lower:
        conceptual_exp = (
            "Economics is fundamentally the study of allocating scarce resources among competing, unlimited alternatives. "
            "A college having ₹50 lakhs faces multiple departmental demands (CS AI Lab, Sports facility, Library, Hostel), "
            "where choosing one necessitates foregoing others. Accounting merely tracks the numerical monetary transactions, "
            "but the core problem of choosing optimal tradeoffs under scarcity is the textbook definition of Economics."
        )
        distractor_trap = "Do not think this is an accounting problem just because money is mentioned. Accounting records past cash flows, whereas economics decides the optimal forward-looking allocation of scarce resources."
        hinglish_shortcut = "Rule: Jab bhi budget limited ho aur maangne wale departments multiple hon, decision hamesha SCARCITY & RESOURCE ALLOCATION (Economics) ka hota hai!"

    # 3. IPL Mega Auction ₹120 Cr Cap (GA1 Q2)
    elif "ipl mega auction" in q_lower or ("120 crore" in q_lower and "cap" in q_lower):
        conceptual_exp = (
            "The IPL salary cap represents an artificial budget ceiling imposed on franchises. Despite wanting all top "
            "players (unlimited desires), franchises are constrained by a strict financial limit of ₹120 crore. This is a "
            "direct manifestation of the economic concept of Scarcity—limited resources preventing the satisfaction of all wants."
        )
        distractor_trap = "Do not confuse scarcity with inflation or macroeconomics. It is a microeconomic constraint of limited financial capital."
        hinglish_shortcut = "Rule: Fixed budget ceiling + unlimited player desires = Textbook SCARCITY!"

    # 4. Delivery Partners Nationwide Labour Law (GA1 Q3)
    elif "nationwide labour law" in q_lower or ("instant-" in q_lower and "macroeconomics" in c_lower):
        conceptual_exp = (
            "Microeconomics analyzes individual agents (a single consumer, firm, or specific market). Macroeconomics studies "
            "aggregate, economy-wide phenomena such as nationwide employment rates, aggregate consumption, GDP, and systemic price levels. "
            "Because this model evaluates the impact of a nationwide law across the entire country's worker unemployment and national retail spending, "
            "it is unequivocally Macroeconomics."
        )
        distractor_trap = "Seeing 'delivery platforms' might tempt you to select firm-level microeconomics. However, because the study evaluates country-wide unemployment and aggregate spending, it is Macroeconomics."
        hinglish_shortcut = "Micro me 'i' = Individual firm/buyer. Macro me 'a' = Aggregate country/economy-wide."

    # 5. Economic Systems: Country X vs Country Y (GA1 Q5)
    elif "country x" in q_lower and "country y" in q_lower:
        conceptual_exp = (
            "In Country X, market forces of demand and supply determine production, prices, and vehicle allocation with private ownership "
            "and minimal government interference, which defines a Capitalist (Market) Economy. In Country Y, private enterprise coexists with "
            "state subsidies, stringent public regulations, and government interventions, which defines a Mixed Economy."
        )
        distractor_trap = "Regulations alone do not make an economy socialist. Almost all modern capitalist nations have some basic regulations, but heavy welfare intervention and public-private co-existence indicates a Mixed Economy."
        hinglish_shortcut = "Country X (Free market pricing) = Capitalist; Country Y (Private + State subsidies/rules) = Mixed Economy."

    # 6. Sunk Cost in Traffic / Flight Cases (GA1 Q6, GA2 Q1)
    elif "sunk cost" in c_lower or "bumper-to-bumper traffic" in q_lower or ("mumbai" in q_lower and "flight" in q_lower):
        conceptual_exp = (
            "A Sunk Cost is an expenditure that has already been incurred and cannot be recovered or altered by any present or future decision. "
            "Rational economic decision-making dictates that sunk costs must be completely ignored because they remain identical regardless of "
            "the alternative selected. In forward-looking decisions, only marginal future costs and opportunity costs matter."
        )
        if "mumbai" in q_lower:
            calc = "Sunk Cost = ₹5,500 flight ticket (Irrelevant) | Opportunity Cost = ₹10,000 Mumbai enjoyment forgone | Rule: Accept IPL only if Enjoyment >= ₹10,000"
        distractor_trap = "Never factor past unrecoverable money or time into current choices. The ₹5,500 flight ticket or 45 minutes lost in traffic cannot be recovered."
        hinglish_shortcut = "Sunk cost = Dooba hua paisa/samay jo wapas nahi aayega. Future decision me iski value ZERO maano!"

    # 7. Data001 Startup Bandwidth & Opportunity Cost (GA2 Q9 & Q10)
    elif "data001" in q_lower or "internal software upgrade" in q_lower:
        conceptual_exp = (
            "Opportunity cost is the value of the next best alternative forgone as a consequence of choosing a specific course of action. "
            "When Data001 chooses Option A (the external client), it must postpone the internal upgrade by 6 months. By postponing the upgrade, "
            "the firm directly forfeits ₹10,000 per month in operational savings. Over 6 months, the forgone benefit is exactly ₹60,000."
        )
        calc = "Opportunity Cost = Monthly Operational Savings Forgone × Number of Months = ₹10,000 × 6 = ₹60,000 (₹60K)"
        distractor_trap = "Do not pick the ₹1.5 Lakh vendor penalty. The penalty is an explicit out-of-pocket accounting cost of choosing Option A, not the forgone benefit of the unchosen alternative."
        hinglish_shortcut = "Opportunity cost = Chhoote hue option ka fayda (₹10K/mo × 6 months = ₹60,000)."

    # 8. XYZ Limited Comprehensive Case (GA8 Q1 to Q12)
    elif "xyz limited" in q_lower or "xyz ltd" in q_lower or "fy 2025" in q_lower:
        if "net profit margin" in q_lower:
            conceptual_exp = "Net Profit Margin measures bottom-line profitability, indicating how much of each rupee of revenue remains as net earnings (PAT) after deducting all operating costs, depreciation, interest, and taxes."
            calc = "Net Profit Margin = (PAT / Revenue) × 100 = (₹3,375 Cr / ₹40,000 Cr) × 100 = 8.4375% ≈ 8.44%"
            distractor_trap = "Do not use Profit Before Tax (₹4,500 Cr) or EBIT. Net margin strictly uses PAT (₹3,375 Cr)."
            hinglish_shortcut = "XYZ Golden Number: Net Profit Margin = 8.44%."
        elif "operating margin" in q_lower:
            conceptual_exp = "Operating Margin (EBIT Margin) reflects core operational efficiency before financing costs and taxes. It evaluates how effectively the company turns revenue into operational profit."
            calc = "Operating Profit (EBIT) = PBT (₹4,500 Cr) + Finance Costs (₹200 Cr) = ₹4,700 Cr or Operating Profit = Revenue (40,000) - Total Operating Costs (35,500 - 200) = ₹4,500 Cr\nOperating Margin = (4,500 / 40,000) × 100 = 11.25%"
            hinglish_shortcut = "XYZ Golden Number: Operating Margin = 11.25%."
        elif "operating expenses" in q_lower:
            conceptual_exp = "Operating expenses include direct and indirect operational costs incurred to run day-to-day operations, explicitly excluding financing charges (interest) and non-cash amortization/depreciation."
            calc = "Total Expenses = ₹35,500 Cr\nLess Depreciation = ₹800 Cr\nLess Finance Costs = ₹200 Cr\nOperating Expenses = 35,500 - 800 - 200 = ₹34,500 Crores"
            distractor_trap = "The problem statement explicitly specifies 'excluding depreciation and finance costs'. Omitting these deductions yields an incorrect ₹35,500 Cr."
            hinglish_shortcut = "XYZ Golden Number: Operating Expenses = ₹34,500 Cr."
        elif "current ratio" in q_lower:
            conceptual_exp = "The Current Ratio evaluates short-term solvency and liquidity—the company's ability to cover obligations due within one year using assets convertible into cash within one year."
            calc = "Current Assets = Inventory (3,500) + Debtors (4,000) + Cash & Others (16,500) = ₹24,000 Cr\nCurrent Liabilities = Other Liabilities = ₹15,000 Cr\nCurrent Ratio = 24,000 / 15,000 = 1.60"
            distractor_trap = "Ensure you sum all current assets (3,500 + 4,000 + 16,500 = 24,000) and do not include Fixed Assets (₹6,000 Cr)."
            hinglish_shortcut = "XYZ Golden Number: Current Ratio = 1.60."
        elif "quick ratio" in q_lower:
            conceptual_exp = "The Quick Ratio (Acid-Test Ratio) is a more stringent test of liquidity than the Current Ratio because it excludes Inventory, which cannot be converted into cash immediately at full book value."
            calc = "Quick Assets = Current Assets (₹24,000 Cr) - Inventory (₹3,500 Cr) = ₹20,500 Cr\nQuick Ratio = Quick Assets / Current Liabilities = 20,500 / 15,000 = 1.3667 ≈ 1.37"
            distractor_trap = "Do not forget to subtract inventory from current assets. 24,000 / 15,000 = 1.60 is the current ratio, not quick ratio."
            hinglish_shortcut = "XYZ Golden Number: Quick Ratio = 1.37."
        elif "debt-equity" in q_lower or "debt to equity" in q_lower:
            conceptual_exp = "The Debt-to-Equity (D/E) ratio gauges financial leverage, showing the proportion of debt financing relative to shareholders' equity funds."
            calc = "Total Debt = ₹2,500 Cr\nShareholders' Equity = Share Capital (500) + Reserves & Surplus (12,000) = ₹12,500 Cr\nDebt-to-Equity = 2,500 / 12,500 = 0.20"
            distractor_trap = "Always include Reserves & Surplus in Equity. Dividing debt by share capital alone (2,500 / 500 = 5.0) is a catastrophic error."
            hinglish_shortcut = "XYZ Golden Number: Debt-to-Equity = 0.20."
        elif "return on equity" in q_lower or "roe" in q_lower:
            conceptual_exp = "Return on Equity (ROE) measures how effectively management deploys shareholders' invested equity capital to generate post-tax net income."
            calc = "ROE = (PAT / Total Shareholders' Equity) × 100 = (₹3,375 Cr / ₹12,500 Cr) × 100 = 27.00%"
            distractor_trap = "Do not divide PAT by Total Assets (₹30,000 Cr) which yields ROA (11.25%). ROE specifically divides by Total Equity (₹12,500 Cr)."
            hinglish_shortcut = "XYZ Golden Number: ROE = 27.0%."
        elif "earnings per share" in q_lower or "eps" in q_lower:
            conceptual_exp = "Earnings Per Share (EPS) allocates net earnings available to equity shareholders across each outstanding share."
            calc = "Number of Shares = Equity Share Capital (₹500 Cr) / Face Value (₹1) = 500 Cr shares\nEPS = PAT / Shares = ₹3,375 Cr / 500 Cr = ₹6.75 per share"
            hinglish_shortcut = "XYZ Golden Number: EPS = ₹6.75."
        elif "p/e" in q_lower or "price to earnings" in q_lower:
            conceptual_exp = "The Price-to-Earnings (P/E) multiple reveals how many times their annual earnings investors are willing to pay for a share at market valuation."
            calc = "P/E Ratio = Market Price per Share / EPS = ₹150 / ₹6.75 = 22.22"
            distractor_trap = "Never divide Face Value (₹1) by EPS. P/E strictly utilizes the Current Market Price (₹150)."
            hinglish_shortcut = "XYZ Golden Number: P/E Ratio = 22.22."
        elif "dividend yield" in q_lower:
            conceptual_exp = "Dividend Yield represents the annual percentage cash return a shareholder earns from declared dividends per share relative to the prevailing market stock price."
            calc = "Dividend Yield = (Dividend per Share / Current Market Price) × 100 = (₹2 / ₹150) × 100 = 1.333% ≈ 1.33%"
            distractor_trap = "Do not compute dividend yield on Face Value (2 / 1 = 200%). Dividend yield is strictly calculated against Market Price (₹150)."
            hinglish_shortcut = "XYZ Golden Number: Dividend Yield = 1.33%."
        elif "market cap" in q_lower:
            conceptual_exp = "Market Capitalization represents the aggregate market value of all outstanding common equity shares of the enterprise."
            calc = "Market Cap = Total Outstanding Shares × Market Price per Share = 500 Cr shares × ₹150 = ₹75,000 Crores"
            hinglish_shortcut = "XYZ Golden Number: Market Capitalization = ₹75,000 Cr."
        elif "inventory turnover" in q_lower:
            conceptual_exp = "Inventory Turnover ratio assesses how many times a company sells and replaces its inventory over a fiscal period, reflecting working capital efficiency."
            calc = "Inventory Turnover = Cost of Materials Consumed / Inventory = ₹28,000 Cr / ₹3,500 Cr = 8.00 times"
            hinglish_shortcut = "XYZ Golden Number: Inventory Turnover = 8.00 times."

    # 9. Real Estate Intent Test (GA5 Q2)
    elif "real estate" in q_lower and ("building" in q_lower or "inventory" in c_lower):
        conceptual_exp = (
            "Under accounting standards (GAAP/IFRS), the classification of an asset is dictated by the Intent of Ownership, "
            "not physical form. For a manufacturing firm, buildings house operations over many years and are classified as Fixed Assets (PP&E). "
            "However, for a real estate developer, buildings are constructed and held specifically for sale in the ordinary course of business, "
            "which defines them strictly as Current Assets (Inventory)."
        )
        distractor_trap = "Do not assume physical buildings are always fixed assets. For a property developer, unsold flats and buildings are trading inventory."
        hinglish_shortcut = "Held for Sale in ordinary business = Inventory (Current Asset); Held for operational use >1 yr = Fixed Asset."

    # 10. R-Goura's Canteen Price Ceiling (Quiz 1 Q19-21)
    elif "r-goura" in q_lower or ("price ceiling" in q_lower and "canteen" in q_lower):
        conceptual_exp = (
            "When the administration imposes a binding price ceiling below the market equilibrium price, it makes the good cheaper than "
            "what market forces dictate. At this artificially lowered price, quantity demanded exceeds quantity supplied (Qd > Qs). "
            "Suppliers reduce their output due to unprofitability while student demand surges, causing persistent shortages, long queues, "
            "and deadweight welfare loss."
        )
        calc = "Equilibrium: Qd = Qs. Price Ceiling < Equilibrium Price => Qd > Qs (Shortage = Qd - Qs)"
        distractor_trap = "A price ceiling set below equilibrium causes a Shortage, not a surplus. A price floor above equilibrium causes a surplus."
        hinglish_shortcut = "Price Ceiling below equilibrium = Sasti price par demand badhegi, supply ghategi => Market me SHORTAGE aayegi!"

    # 11. Generic/Fallback Comprehensive Generator
    if not conceptual_exp:
        # Generate context-rich explanation based on topic, feedback, and option texts
        if feedback and len(feedback) > 20:
            conceptual_exp = (
                f"Based on core {module} principles: {feedback} "
                f"The correct option '{c_lbl}' ({c_txt}) directly aligns with this foundational rule."
            )
        else:
            conceptual_exp = (
                f"In the study of {module}, Option '{c_lbl}' ({c_txt}) provides the conceptually accurate statement. "
                f"It accurately reflects the established principles of {module}, satisfying the specific conditions "
                f"stipulated in the scenario while remaining compliant with core business and economic theory."
            )
        if not distractor_trap:
            distractor_trap = f"Watch out for distractors that use superficially similar terminology but reverse the cause-and-effect relationship or violate the scope of {module}."
        if not hinglish_shortcut:
            hinglish_shortcut = f"Key Takeaway: {c_txt} — exam me is concept ko direct link karke identify karo."

    # Generate Option-by-Option Breakdown
    options_breakdown = []
    for opt in options:
        lbl = opt.get('label', '')
        txt = clean_txt(opt.get('text', ''))
        is_corr = opt.get('is_correct', False)

        if is_corr:
            analysis = (
                f"✅ [CORRECT] Option {lbl} is the verified correct answer. "
                f"It correctly establishes that '{txt}'. This adheres to the theoretical framework of {module} "
                f"and precisely addresses the problem requirements."
            )
        else:
            # Generate tailored distractor explanation
            analysis = (
                f"❌ [INCORRECT] Option {lbl} ('{txt}') is incorrect. "
                f"It does not satisfy the operational constraints or theoretical principles governing this problem. "
                f"Choosing this option represents a common conceptual confusion or miscalculation."
            )
            # Custom explanations for known options
            if "greenfleet" in q_lower:
                if "100" in txt and "vehicles" in txt:
                    analysis = "❌ [INCORRECT] 100 E2 vehicles would only spend ₹10,000 on charging. Combined with ₹4,000 for E3, total spend is ₹14,000, leaving ₹6,000 of the daily budget unutilized."
                elif "120" in txt and "vehicles" in txt:
                    analysis = "❌ [INCORRECT] 120 E2 vehicles would spend ₹12,000, totaling ₹16,000 with E3. This leaves ₹4,000 unutilized, failing to maximize fleet deployment."
                elif "200" in txt and "vehicles" in txt:
                    analysis = "❌ [INCORRECT] 200 E2 vehicles cost 200 × ₹100 = ₹20,000. This leaves zero budget for the mandatory 10 E3 vehicles (costing ₹4,000), violating the mandatory B2B contract."
                elif "80,000" in txt:
                    analysis = "❌ [INCORRECT] ₹80,000 only counts the profit from 160 E2 vehicles (160 × ₹500), mistakenly omitting the ₹15,000 profit generated by the 10 E3 vehicles."
                elif "1,00,000" in txt:
                    analysis = "❌ [INCORRECT] ₹1,00,000 is the profit if 200 E2 vehicles were deployed with zero E3 vehicles, which violates the mandatory B2B contract."
                elif "1,15,000" in txt:
                    analysis = "❌ [INCORRECT] ₹1,15,000 exceeds the maximum possible profit under the ₹20,000 charging constraint."
            elif "college administration" in q_lower or "budget of ₹50" in q_lower:
                if lbl == 'A':
                    analysis = "❌ [INCORRECT] Economics is not limited to money. It deals with allocating scarce resources in general (time, attention, energy, capital)."
                elif lbl == 'C':
                    analysis = "❌ [INCORRECT] Coordinating departments is management, but deciding how to ration scarce budget among mutually exclusive investments is pure Economics."
                elif lbl == 'D':
                    analysis = "❌ [INCORRECT] Resource allocation decisions exist prior to market transactions. Internal budget rationing is a fundamental economic problem."
            elif "ipl mega auction" in q_lower:
                if lbl == 'A':
                    analysis = "❌ [INCORRECT] Demand is the willingness and ability to purchase, not the constraint limiting total purchasing capacity."
                elif lbl == 'C':
                    analysis = "❌ [INCORRECT] Inflation refers to a sustained rise in the general price level across an economy, not a franchise's fixed salary cap."
                elif lbl == 'D':
                    analysis = "❌ [INCORRECT] An individual franchise managing its squad budget is a microeconomic decision unit, not aggregate macroeconomics."

        options_breakdown.append({
            "label": lbl,
            "text": txt,
            "is_correct": is_corr,
            "analysis": analysis
        })

    return {
        "direct_answer": f"Option {c_lbl}: {c_txt}",
        "correct_label": c_lbl,
        "correct_text": c_txt,
        "conceptual_explanation": conceptual_exp,
        "options_breakdown": options_breakdown,
        "calculation": calc,
        "distractor_trap": distractor_trap,
        "hinglish_shortcut": hinglish_shortcut
    }

# Process all questions
updated_count = 0
for q in questions:
    q['ai_solution'] = build_long_solution(q)
    updated_count += 1

print(f"Enriched all {updated_count} questions with long conceptual solutions and option breakdowns.")

# Save back to master JSON
with open('bdm_master_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(master_data, f, indent=2, ensure_ascii=False)

# Save to data.js
js_content = "window.BDM_DATA = " + json.dumps(master_data, indent=2, ensure_ascii=False) + ";\n"
with open('data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Successfully wrote updated bdm_master_dataset.json and data.js!")
