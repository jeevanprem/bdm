import os
import sys
import re
import json
import pymupdf

sys.stdout.reconfigure(encoding='utf-8')

EXTRACTED_DIR = r'd:\ai codings\bdm html\extracted_texts'
OUTPUT_JSON = r'd:\ai codings\bdm html\bdm_master_dataset.json'

MODULE_INFO = {
    1: {
        'name': 'Economics Foundations & Resource Scarcity',
        'desc': 'Core economic problems: Scarcity, Opportunity Cost, Needs vs Wants, Marginalism, and Resource Allocation.',
        'mnemonic': 'S-O-U-P (Scarcity, Opportunity cost, Unlimited wants, Prioritization)',
        'core_formula': 'Net Marginal Benefit = Marginal Benefit (MB) - Marginal Cost (MC) >= 0',
        'key_points': [
            'Economics is the study of how society allocates scarce resources among competing alternatives.',
            'Needs are basic survival essentials (food, water, shelter, clothing). Wants are desires beyond survival.',
            'Opportunity Cost is the value of the NEXT BEST alternative forgone (not the sum of all alternatives).',
            'Sunk costs are past unrecoverable expenses and should be IGNORED in forward-looking economic decisions.',
            'Rational individuals make decisions at the margin: do an action if and only if MB >= MC.'
        ]
    },
    2: {
        'name': 'Cost Concepts, PPF & Production Economics',
        'desc': 'Cost behaviors (TFC, TVC, TC, MC, ATC, AFC, AVC) and the Production Possibility Frontier.',
        'mnemonic': 'B-I-O-S (Bowed-out=Increasing Opp Cost, Inside=Inefficient, On=Optimal, Shift=Growth)',
        'core_formula': 'TC = TFC + TVC; MC = ΔTC/ΔQ; PPF Slope = MRT = |ΔY / ΔX|',
        'key_points': [
            'Fixed Costs (TFC) do not change with output in the short run. AFC = TFC / Q declines continuously.',
            'Variable Costs (TVC) increase with output (raw materials, wages). AVC = TVC / Q.',
            'Marginal Cost (MC) is the change in TC for 1 additional unit: MC = ΔTC/ΔQ. MC intersects ATC and AVC at their minimum points.',
            'PPF Points: ON the curve = Productively efficient; INSIDE = Inefficient/Unemployed; OUTSIDE = Infeasible.',
            'Concave (Bowed-out) PPF is caused by the Law of Increasing Opportunity Cost (resources are specialized).'
        ]
    },
    3: {
        'name': 'Basics of Business, Business Models & Goods Classification',
        'desc': 'Commercial structures (B2B, B2C, C2C), Value Proposition, and Search vs Experience vs Credence goods.',
        'mnemonic': 'S-E-C (Search=Seen before buying, Experience=Felt after consumption, Credence=Trust even after consumption)',
        'core_formula': 'Customer Value = Total Perceived Benefits - Total Perceived Costs',
        'key_points': [
            'B2B: End customer is another business (higher order value, longer sales cycle, multi-stakeholder DMU).',
            'B2C: End customer is an individual consumer (faster sales cycle, brand/emotional factors).',
            'Search Goods: Quality/attributes can be evaluated BEFORE purchase (clothing specs, laptop RAM, books).',
            'Experience Goods: Quality can only be assessed AFTER consumption (meals at restaurant, movies, vacation).',
            'Credence Goods: Quality cannot be evaluated easily even AFTER consumption (complex surgery, legal counsel).'
        ]
    },
    4: {
        'name': 'Demand, Supply, Market Equilibrium & Elasticities',
        'desc': 'Laws of Demand and Supply, Market Equilibrium, Price Elasticity, Cross-Price Elasticity, Income Elasticity.',
        'mnemonic': 'P-E-R-K (Inelastic Demand: P & TR move SAME direction; Elastic Demand: P & TR move OPPOSITE directions)',
        'core_formula': 'Ep = (%ΔQd)/(%ΔP); Exy = (%ΔQx)/(%ΔPy); Ey = (%ΔQd)/(%ΔIncome)',
        'key_points': [
            'Law of Demand: Price and Quantity Demanded are inversely related (P↑ => Qd↓), ceteris paribus.',
            'Movement along curve = caused ONLY by a change in the good\'s own price. Shift of curve = non-price factors.',
            'Price Elasticity: |Ep| > 1 is Elastic; |Ep| < 1 is Inelastic; |Ep| = 1 is Unit Elastic (Max TR).',
            'Cross Elasticity Exy: > 0 for Substitutes (Tea & Coffee); < 0 for Complements (Cars & Petrol).',
            'Income Elasticity Ey: > 0 for Normal Goods (Ey > 1 Luxury, 0 < Ey < 1 Necessity); < 0 for Inferior Goods.'
        ]
    },
    5: {
        'name': 'Introduction to Accounting & Asset Classification',
        'desc': 'Distinction between Financial, Managerial, and Cost Accounting; Asset and Liability classifications.',
        'mnemonic': '12-Month Operating Intent Test: Held for Sale = Inventory/Current Asset; Held to Operate > 1yr = Fixed Asset',
        'core_formula': 'Total Assets = Current Assets + Non-Current (Fixed) Assets',
        'key_points': [
            'Financial Accounting: Historical, external stakeholders (investors, creditors, tax), mandatory GAAP/IFRS.',
            'Managerial Accounting: Future-oriented, internal decision making (budgets, forecasts), flexible format.',
            'Cost Accounting: Cost of production, unit cost calculation, inventory cost tracking.',
            'Current Assets: Converted to cash or consumed within 12 months / 1 operating cycle (Cash, Debtors, Inventory).',
            'Crucial Context Trap: Buildings held by a Real Estate Builder for sale are INVENTORY (Current Asset), not Fixed Assets!'
        ]
    },
    6: {
        'name': 'Accounting Equation, Transactions & Income Statement',
        'desc': 'Dual-entry recording, Fundamental Accounting Equation, Gross Profit, Operating Profit, Net Income.',
        'mnemonic': 'ALOE (Assets = Liabilities + Owner Equity) & DEAL vs CLIP (Debit: Drawings, Expenses, Assets; Credit: Liabilities, Income, Capital)',
        'core_formula': 'Assets = Liabilities + Equity; Gross Profit = Revenue - COGS; EBIT = GP - OpEx; PAT = EBIT - Interest - Tax',
        'key_points': [
            'Accounting Equation: Assets = Liabilities + Owner\'s Equity. Must always balance after every transaction.',
            'Owner withdrawing cash for personal rent is recorded as DRAWINGS, reducing Owner\'s Equity and Cash (Asset).',
            'Paying off Accounts Payable with Cash reduces both Assets (Cash) and Liabilities (Payables) equally.',
            'COGS includes direct materials, direct labor, and direct manufacturing costs.',
            'Operating Profit (EBIT) excludes Finance Costs (Interest) and Income Taxes.'
        ]
    },
    7: {
        'name': 'Financial Ratios, Solvency & Cash Flow Classification',
        'desc': 'Liquidity, Solvency, Operating vs Investing vs Financing Cash Flows, and Insolvency analysis.',
        'mnemonic': 'O-I-F Cash Flows (Operating=Daily Core, Investing=Long-term PP&E, Financing=Debt, Equity, Dividends)',
        'core_formula': 'Current Ratio = CA / CL; Quick Ratio = (CA - Inventory - Prepaid) / CL; Debt/Equity = Total Debt / Equity',
        'key_points': [
            'Current Ratio (ideal ~2:1): Measures short-term liquidity. Quick Ratio excludes Inventory and Prepaid expenses.',
            'A high Debt-Equity ratio (e.g. 4:1) signals high financial leverage, higher risk, and vulnerability to bankruptcy.',
            'A firm can be highly profitable on an accrual basis and still face bankruptcy if operating cash flow is negative!',
            'Purchasing factory equipment for cash is a CASH OUTFLOW from INVESTING ACTIVITIES.',
            'Issuing equity shares or repaying bank loans is classified under FINANCING ACTIVITIES.'
        ]
    },
    8: {
        'name': 'Corporate Financial Statements Case Study (XYZ Ltd)',
        'desc': 'Comprehensive financial statement analysis of commercial vehicle manufacturer XYZ Limited.',
        'mnemonic': 'DuPont Pyramid: ROE = Net Profit Margin × Asset Turnover × Equity Multiplier',
        'core_formula': 'ROE = (3375/40000) × (40000/30000) × (30000/12500) = 8.44% × 1.33 × 2.4 = 27.0%',
        'key_points': [
            'Revenue = ₹40,000 Cr; PAT = ₹3,375 Cr; Total Assets = ₹30,000 Cr; Total Equity = ₹12,500 Cr; Debt = ₹2,500 Cr.',
            'Net Profit Margin = (PAT / Revenue) × 100 = (3,375 / 40,000) × 100 = 8.44%.',
            'Operating Margin (EBIT / Revenue) = (4,500 / 40,000) × 100 = 11.25%.',
            'Current Ratio = Current Assets / Current Liabilities = 24,000 / 15,000 = 1.60.',
            'Quick Ratio = (24,000 - 3,500) / 15,000 = 1.37.',
            'Debt-to-Equity Ratio = 2,500 / 12,500 = 0.20.',
            'EPS = PAT / Shares = 3,375 / 500 = ₹6.75 per share.',
            'P/E Ratio = Market Price / EPS = 150 / 6.75 = 22.22.',
            'Dividend Yield = Dividend per share / Market Price = 2 / 150 = 1.33%.',
            'Market Capitalization = 500 Cr shares × ₹150 = ₹75,000 Cr.'
        ]
    },
    9: {
        'name': 'Management Accounting & Responsibility Centers',
        'desc': 'Cost, Revenue, Profit, and Investment Centers; internal reporting and performance evaluation.',
        'mnemonic': 'C-R-P-I Escalator (Cost Center -> Revenue Center -> Profit Center -> Investment Center)',
        'core_formula': 'ROI = Operating Income / Operating Assets; EVA = NOPAT - (WACC × Capital)',
        'key_points': [
            'Cost Center: Manager is accountable ONLY for controlling costs (e.g. IT support, Maintenance, Plant assembly).',
            'Revenue Center: Manager is accountable ONLY for sales generation (e.g. Regional sales branch).',
            'Profit Center: Manager is evaluated on both Revenues AND Costs (e.g. Individual retail outlet, Product line).',
            'Investment Center: Evaluated on Revenue, Costs, and return on capital invested (ROI / EVA) (e.g. Subsidiary head).',
            'Financial accounting limitations: Aggregated, historical, lacks unit-level cost insight and operational flexibility.'
        ]
    },
    11: {
        'name': 'Personal Selling, Sales Process & Prospecting Funnel',
        'desc': 'The 7-step personal selling cycle, B2B sales techniques, objection handling, and sales funnel.',
        'mnemonic': 'P-P-A-P-H-C-F (Prospecting, Pre-approach, Approach, Presentation, Handling objections, Closing, Follow-up)',
        'core_formula': 'Qualified Lead = M-A-N (Money / Budget, Authority to buy, Need for product)',
        'key_points': [
            '1. Prospecting: Identifying potential customers (leads). Qualifying using MAN criteria.',
            '2. Pre-approach: Researching the prospect before the initial meeting.',
            '3. Approach: Initial contact, building rapport. PSP technique (Personal Selling Principles / Problem-Solution-Pitch).',
            '4. Presentation: FAB framework (Features: what it is; Advantages: what it does; Benefits: what it means to customer).',
            '5. Handling Objections: Answering customer hesitations and turning concerns into selling points.',
            '6. Closing: Asking for the order (Assumptive close, Summary close, Alternative choice).',
            '7. Follow-up: Ensuring satisfaction, post-sales service, nurturing long-term relationship.'
        ]
    },
    12: {
        'name': 'Services Marketing, Service Quality & Service Recovery',
        'desc': 'Unique service characteristics (IHIP), 7Ps of Services, SERVQUAL 5 dimensions, and Service Recovery Paradox.',
        'mnemonic': 'R-A-T-E-R (Reliability, Assurance, Tangibles, Empathy, Responsiveness) & I-H-I-P',
        'core_formula': 'Service Quality Gap = Perceived Service Experience (P) - Expected Service (E)',
        'key_points': [
            'IHIP Characteristics: Intangibility, Heterogeneity (Variability), Inseparability, Perishability.',
            '7Ps of Services Marketing: Product, Price, Place, Promotion + People, Process, Physical Evidence.',
            'SERVQUAL 5 Dimensions: Reliability (promised service), Assurance (trust/courtesy), Tangibles (facilities/appearance), Empathy (individualized caring), Responsiveness (prompt helpful service).',
            'Service Recovery Paradox: A customer who experienced a failure that was resolved brilliantly may be MORE loyal than one who never had a problem.',
            'First critical step in service recovery: Prompt acknowledgment, sincere apology, and active listening.'
        ]
    }
}

def clean_boilerplate_prompt(raw_text):
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    cleaned = []
    for l in lines:
        if any(b in l for b in [
            'BDM Theory Course:', 'Read the questions carefully', 'marks each',
            'Wish you all The Best', 'Answer is Correct', 'Answer is Wrong',
            'This assignment is for a total', 'All the questions are compulsory',
            'First 12 questions carry', '--- PAGE', 'Courses :: IITM Study',
            'https://seek.study.iitm.ac.in', 'Score:'
        ]):
            continue
        if l.strip() == 'class answer the following questions:':
            continue
        cleaned.append(l)
    return '\n'.join(cleaned).strip()

def parse_all_gas():
    ga_list = []
    ga_files = [
        (1, 'Graded Assignment week 1.txt'),
        (2, 'Graded Assignment week 2.txt'),
        (3, 'Graded Assignment week 3.txt'),
        (4, 'Graded Assignment week 4.txt'),
        (5, 'Graded Assignment week 5.txt'),
        (6, 'Graded Assignment week 6.txt'),
        (7, 'Graded Assignment week 7.txt'),
        (8, 'Graded Assignment week 8.txt'),
        (9, 'Graded Assignment week 9.txt'),
        (11, 'Graded Assignment week 11.txt'),
        (12, 'Graded Assignment week 12.txt'),
    ]

    for week_num, fname in ga_files:
        fpath = os.path.join(EXTRACTED_DIR, fname)
        if not os.path.exists(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()

        mod = MODULE_INFO.get(week_num, {
            'name': f'Week {week_num}', 'desc': '', 'mnemonic': '', 'core_formula': '', 'key_points': []
        })

        chunks = re.split(r'QUESTION\s+(\d+)', content)
        for i in range(1, len(chunks), 2):
            qnum = int(chunks[i])
            body = chunks[i+1]

            # extract feedback
            fb = ''
            m_fb = re.search(r'FEEDBACK\s*(.*?)(?=\n[A-D]\.|\n10/09|\n--- PAGE|$)', body, re.DOTALL)
            if m_fb:
                fb = ' '.join(m_fb.group(1).split())

            # prompt is before 'Options'
            parts = body.split('Options')
            prompt_raw = parts[0]
            opts_raw = parts[1] if len(parts) > 1 else ''

            q_prompt = clean_boilerplate_prompt(prompt_raw)

            # parse options from the entire body (to capture before & after feedback)
            lines = [l.strip() for l in body.splitlines() if l.strip()]
            options = []
            curr_opt = None

            for l in lines:
                m = re.match(r'^([A-D])\.\s*(.*)', l)
                if m:
                    if curr_opt:
                        options.append(curr_opt)
                    curr_opt = {'label': m.group(1), 'text': m.group(2).strip(), 'is_correct': False}
                elif l in ['Correct', 'Expected']:
                    if curr_opt:
                        curr_opt['is_correct'] = True
                elif curr_opt:
                    if not any(x in l for x in ['FEEDBACK', '10/09/2026', 'https://', 'Courses ::', 'Score:', '--- PAGE', 'QUESTION ']):
                        curr_opt['text'] += ' ' + l

            if curr_opt:
                options.append(curr_opt)

            # determine case-based
            is_case = any(cw in q_prompt.lower() for cw in ['case', 'xyz limited', 'college administration', 'ipl', 'startup', 'data001', 'proposal', 'scenario']) or (week_num == 8)

            ga_list.append({
                'id': f'GA{week_num}_Q{qnum}',
                'source': f'GA Week {week_num}',
                'week': week_num,
                'module': mod['name'],
                'q_num': qnum,
                'is_case_based': is_case,
                'question': q_prompt,
                'options': options,
                'feedback': fb,
                'mnemonic': mod['mnemonic'],
                'formula': mod['core_formula']
            })

    return ga_list

def parse_quizzes_crosspage():
    quizzes = []
    configs = [
        ('Quiz 1', r'd:\ai codings\bdm html\bdm\quiz1.pdf', 1928, 1, 6, 'Economics & Business Fundamentals (Quiz 1)'),
        ('Quiz 2', r'd:\ai codings\bdm html\bdm\quiz2.pdf', 1872, 7, 12, 'Accounting, Ratios, Sales & Services (Quiz 2)')
    ]

    for qname, pdf_path, green_xref, start_w, end_w, module_title in configs:
        doc = pymupdf.open(pdf_path)
        all_blocks = []
        for p_idx in range(1, len(doc)):
            page = doc[p_idx]
            green_ys = [ (img['bbox'][1] + img['bbox'][3])/2 for img in page.get_image_info(xrefs=True) if img['xref'] == green_xref ]
            for b in sorted(page.get_text('blocks'), key=lambda b: b[1]):
                if b[4].strip():
                    all_blocks.append({
                        'page': p_idx + 1,
                        'y0': b[1],
                        'y1': b[3],
                        'text': b[4].strip(),
                        'green_ys': green_ys
                    })

        q_indices = []
        for idx, b in enumerate(all_blocks):
            if 'Question Number :' in b['text'] and 'Question Type : MCQ' in b['text']:
                m = re.search(r'Question Number\s*:\s*(\d+)', b['text'])
                if m and int(m.group(1)) > 1:
                    q_indices.append((idx, int(m.group(1))))

        for k, (start_idx, q_num) in enumerate(q_indices):
            end_idx = q_indices[k+1][0] if k+1 < len(q_indices) else len(all_blocks)
            q_blocks = all_blocks[start_idx:end_idx]

            q_text_parts = []
            options = []
            in_opts = False
            labels = ['A', 'B', 'C', 'D', 'E']
            opt_idx = 0

            for b in q_blocks:
                t = b['text']
                if 'Options :' in t:
                    in_opts = True
                    bf = t.split('Options :')[0].strip()
                    if bf:
                        q_text_parts.append(bf)
                    continue
                if not in_opts:
                    if not any(h in t for h in ['Question Number :', 'Correct Marks :', 'Question Label :']):
                        q_text_parts.append(t)
                else:
                    m = re.match(r'^\d{10,}\.\s*(.*)', t, re.DOTALL)
                    if m:
                        by0, by1 = b['y0'], b['y1']
                        corr = any(by0 - 8 <= gy <= by1 + 8 for gy in b['green_ys'])
                        lbl = labels[opt_idx] if opt_idx < len(labels) else str(opt_idx+1)
                        opt_idx += 1
                        options.append({
                            'label': lbl,
                            'text': m.group(1).strip(),
                            'is_correct': corr,
                            'page': b['page'],
                            'y': (by0, by1),
                            'green_ys': b['green_ys']
                        })
                    else:
                        if options:
                            options[-1]['text'] += ' ' + t
                            by1 = max(options[-1]['y'][1], b['y1'])
                            options[-1]['y'] = (options[-1]['y'][0], by1)
                            if not options[-1]['is_correct'] and options[-1]['page'] == b['page']:
                                options[-1]['is_correct'] = any(options[-1]['y'][0] - 8 <= gy <= by1 + 8 for gy in b['green_ys'])

            q_prompt = ' '.join(q_text_parts).strip()
            is_case = any(w in q_prompt.lower() for w in ['case', 'r-goura', 'canteen', 'company', 'scenario', 'xyz', 'firm', 'saturn'])

            # Clean options dict
            cleaned_opts = [{'label': o['label'], 'text': o['text'], 'is_correct': o['is_correct']} for o in options]

            quizzes.append({
                'id': f'{qname.replace(" ", "")}_Q{q_num}',
                'source': qname,
                'week': start_w if qname == 'Quiz 1' else end_w,
                'module': module_title,
                'q_num': q_num,
                'is_case_based': is_case,
                'question': q_prompt,
                'options': cleaned_opts,
                'feedback': 'Official IIT Madras TCS iON Exam Question',
                'mnemonic': 'Exam High-Yield Real Question',
                'formula': ''
            })

    return quizzes

def build_master():
    gas = parse_all_gas()
    quizzes = parse_quizzes_crosspage()
    all_qs = gas + quizzes

    print(f'Parsed {len(gas)} GA questions and {len(quizzes)} Quiz questions. Total = {len(all_qs)}')

    dataset = {
        'course': {
            'code': 'MS2001',
            'title': 'Business Data Management (BDM)',
            'degree': 'IIT Madras BS in Data Science and Applications',
            'level': 'Diploma Level',
            'total_questions': len(all_qs),
            'modules': MODULE_INFO
        },
        'questions': all_qs
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as fp:
        json.dump(dataset, fp, indent=2, ensure_ascii=False)

    print(f'Exported full master dataset to {OUTPUT_JSON}')

if __name__ == '__main__':
    build_master()
