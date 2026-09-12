import os
import sys
import re
import json
import pymupdf

sys.stdout.reconfigure(encoding='utf-8')

EXTRACTED_DIR = r'd:\ai codings\bdm html\extracted_texts'
BDM_DIR = r'd:\ai codings\bdm html\bdm'
OUTPUT_JSON = r'd:\ai codings\bdm html\bdm_master_dataset.json'

TOPIC_INFO = {
    1: {
        'name': 'Economics Foundations & Resource Scarcity',
        'key_concepts': ['Needs vs Wants', 'Scarcity', 'Opportunity Cost', 'Rational Decision Making', 'Marginal Benefit vs Marginal Cost'],
        'mnemonic': 'S-O-U-P (Scarcity, Opportunity cost, Unlimited wants, Prioritization)',
        'core_formula': 'Net Marginal Benefit = MB - MC >= 0'
    },
    2: {
        'name': 'Cost Concepts, PPF & Production Economics',
        'key_concepts': ['Fixed vs Variable Costs', 'Marginal Cost (MC)', 'Average Cost (ATC, AVC, AFC)', 'Production Possibility Frontier (PPF)', 'Increasing Opportunity Cost (Concave PPF)'],
        'mnemonic': 'B-I-O-S (Bowed-out PPF, Inside=Inefficient, On=Optimal, Shift=Growth)',
        'core_formula': 'TC = TFC + TVC; MC = ΔTC/ΔQ; PPF Slope = MRT = |ΔY / ΔX|'
    },
    3: {
        'name': 'Basics of Business, Business Models & Goods Classification',
        'key_concepts': ['B2B vs B2C vs C2C', 'Search Goods vs Experience Goods vs Credence Goods', 'Value Proposition', 'Revenue Models'],
        'mnemonic': 'S-E-C (Search=Seen before buying, Experience=Felt after consumption, Credence=Trust even after consumption)',
        'core_formula': 'Customer Lifetime Value (CLV) & Value = Perceived Benefit - Cost'
    },
    4: {
        'name': 'Demand, Supply, Market Equilibrium & Elasticities',
        'key_concepts': ['Law of Demand & Supply', 'Movement vs Shift', 'Price Elasticity of Demand (Ep)', 'Cross-Price Elasticity (Exy)', 'Income Elasticity (Ey)', 'Surplus & Deadweight Loss'],
        'mnemonic': 'P-E-R-K (Inelastic: Price & Revenue in SAME direction; Elastic: OPPOSITE direction)',
        'core_formula': 'Ep = (%ΔQd)/(%ΔP); Exy > 0 (Substitutes), Exy < 0 (Complements); Ey > 0 (Normal), Ey < 0 (Inferior)'
    },
    5: {
        'name': 'Introduction to Accounting & Asset Classification',
        'key_concepts': ['Financial vs Managerial vs Cost Accounting', 'Current Assets vs Fixed Assets (12-Month Rule)', 'Inventory Intent Test', 'Balance Sheet Structure'],
        'mnemonic': '12-Month Operating Intent Rule: Held for Sale = Inventory/Current Asset; Held to Produce > 1yr = Fixed Asset',
        'core_formula': 'Total Assets = Current Assets + Non-Current (Fixed) Assets'
    },
    6: {
        'name': 'Accounting Equation, Transactions & Income Statement',
        'key_concepts': ['The Fundamental Accounting Equation', 'Double-Entry Mechanism', 'Drawings/Owner Equity', 'Gross Profit vs Operating Profit vs Net Profit'],
        'mnemonic': 'ALOE (Assets = Liabilities + Owner Equity) & DEAL (Debit: Drawings, Expenses, Assets) vs CLIP (Credit: Liabilities, Income, Capital)',
        'core_formula': 'Assets = Liabilities + Equity; Gross Profit = Sales - COGS; Operating Profit (EBIT) = GP - OpEx'
    },
    7: {
        'name': 'Financial Ratios, Solvency & Cash Flow Classification',
        'key_concepts': ['Current Ratio & Quick Ratio', 'Debt-Equity Ratio & Solvency Risk', 'Profitability vs Liquidity (Insolvency trap)', 'Operating vs Investing vs Financing Cash Flows'],
        'mnemonic': 'O-I-F Cash Flows (Operating = Core operations, Investing = Long-term PP&E, Financing = Debt, Shares, Dividends)',
        'core_formula': 'Current Ratio = CA / CL; Quick Ratio = (CA - Inv - Prepaid) / CL; Debt/Equity = Total Debt / Shareholders Equity'
    },
    8: {
        'name': 'Corporate Financial Statements Case Study (XYZ Ltd)',
        'key_concepts': ['12 Financial Metrics Breakdown', 'DuPont Analysis', 'EPS & P/E Ratio Valuation', 'Operating vs Net Margin', 'Inventory Turnover'],
        'mnemonic': 'DuPont Pyramid: ROE = Net Margin (Profitability) × Asset Turnover (Efficiency) × Equity Multiplier (Leverage)',
        'core_formula': 'ROE = (PAT/Rev) × (Rev/Assets) × (Assets/Equity) = 8.44% × 1.33 × 2.4 = 27.0%'
    },
    9: {
        'name': 'Management Accounting & Responsibility Centers',
        'key_concepts': ['Cost Centers vs Revenue Centers vs Profit Centers vs Investment Centers', 'Managerial Decision Making', 'Limitations of Financial Accounting'],
        'mnemonic': 'C-R-P-I Escalator (Cost -> Revenue -> Profit -> Investment Capital Return)',
        'core_formula': 'ROI = Net Operating Income / Average Operating Assets'
    },
    11: {
        'name': 'Personal Selling, Sales Process & Prospecting Funnel',
        'key_concepts': ['7 Steps of Personal Selling', 'Prospecting & Qualifying (MAN: Money, Authority, Need)', 'PSP (Problem-Solution-Presentation)', 'FAB (Features, Advantages, Benefits)', 'Closing & Follow-up'],
        'mnemonic': 'P-P-A-P-H-C-F (Prospecting, Pre-approach, Approach, Presentation, Handling objections, Closing, Follow-up)',
        'core_formula': 'Sales Funnel Conversion = Deals Closed / Prospects Contacted'
    },
    12: {
        'name': 'Services Marketing, Service Quality & Service Recovery',
        'key_concepts': ['IHIP Characteristics of Services (Intangibility, Heterogeneity, Inseparability, Perishability)', '7Ps of Services (People, Process, Physical Evidence)', 'SERVQUAL 5 Dimensions (RATER)', 'Service Recovery Paradox'],
        'mnemonic': 'R-A-T-E-R (Reliability, Assurance, Tangibles, Empathy, Responsiveness) & I-H-I-P',
        'core_formula': 'Perceived Service Quality = Perceived Service - Expected Service'
    }
}

def clean_lines(text):
    lines = [l.strip() for l in text.splitlines()]
    filtered = []
    for l in lines:
        if not l:
            continue
        if 'Courses :: IITM Study' in l or 'seek.study.iitm.ac.in' in l or re.search(r'\d+/\d+\s*$', l):
            continue
        filtered.append(l)
    return '\n'.join(filtered).strip()

def parse_all_gas():
    ga_questions = []
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

        # Split into questions by 'QUESTION '
        chunks = re.split(r'QUESTION\s+(\d+)', content)
        topic = TOPIC_INFO.get(week_num, {'name': f'Week {week_num}', 'key_concepts': [], 'mnemonic': '', 'core_formula': ''})

        for i in range(1, len(chunks), 2):
            q_num = int(chunks[i])
            raw_body = chunks[i+1]

            feedback = ''
            if 'FEEDBACK' in raw_body:
                fb_parts = raw_body.split('FEEDBACK')
                feedback = clean_lines(fb_parts[1])
                raw_body = fb_parts[0]

            cleaned_body = clean_lines(raw_body)
            parts = cleaned_body.split('Options')
            prompt_raw = parts[0].strip()
            opts_raw = parts[1].strip() if len(parts) > 1 else ''

            # Clean prompt
            prompt_lines = []
            for l in prompt_raw.splitlines():
                if any(bp in l for bp in ['BDM Theory Course:', 'Read the questions carefully', 'marks each', 'Wish you all The Best', 'Answer is Correct', 'Answer is Wrong', 'This assignment is for a total', 'All the questions are compulsory', 'First 12 questions carry', 'Note:', '--- PAGE']):
                    continue
                if l.strip() == 'class answer the following questions:':
                    continue
                prompt_lines.append(l)
            q_text = '\n'.join(prompt_lines).strip()

            # Parse options
            opt_lines = opts_raw.splitlines()
            options = []
            curr_opt = None

            for l in opt_lines:
                m = re.match(r'^([A-D])\.\s*(.*)', l)
                if m:
                    if curr_opt:
                        options.append(curr_opt)
                    curr_opt = {'label': m.group(1), 'text': m.group(2).strip(), 'is_correct': False}
                elif l == 'Correct':
                    if curr_opt:
                        curr_opt['is_correct'] = True
                else:
                    if curr_opt:
                        curr_opt['text'] += ' ' + l.strip()

            if curr_opt:
                options.append(curr_opt)

            # If no options found with A-D, let's look for line-by-line options
            if not options and opts_raw:
                # sometimes options are listed without letters or differently
                lines = [l.strip() for l in opts_raw.splitlines() if l.strip()]
                labels = ['A', 'B', 'C', 'D', 'E', 'F']
                lbl_idx = 0
                for l in lines:
                    if l == 'Correct':
                        if options:
                            options[-1]['is_correct'] = True
                    elif not any(x in l for x in ['Score:', '10/09/2026', '--- PAGE']):
                        lbl = labels[lbl_idx] if lbl_idx < len(labels) else str(lbl_idx+1)
                        lbl_idx += 1
                        options.append({'label': lbl, 'text': l, 'is_correct': False})

            # Check if there is a case study
            is_case = ('Case' in q_text or 'XYZ Limited' in q_text or 'college administration' in q_text.lower() or 'ipl' in q_text.lower() or week_num == 8)
            
            ga_questions.append({
                'id': f'GA{week_num}_Q{q_num}',
                'source': f'GA Week {week_num}',
                'week': week_num,
                'module': topic['name'],
                'q_num': q_num,
                'is_case_based': is_case,
                'question': q_text,
                'options': options,
                'feedback': feedback,
                'mnemonic': topic['mnemonic'],
                'formula': topic['core_formula']
            })

    return ga_questions

def parse_tcs_quizzes():
    quizzes_parsed = []
    quiz_configs = [
        ('Quiz 1', r'd:\ai codings\bdm html\bdm\quiz1.pdf', 1928, 1, 6),
        ('Quiz 2', r'd:\ai codings\bdm html\bdm\quiz2.pdf', 1872, 7, 12)
    ]

    for q_name, pdf_path, green_xref, start_w, end_w in quiz_configs:
        doc = pymupdf.open(pdf_path)
        for page_idx in range(1, len(doc)):
            page = doc[page_idx]
            green_boxes = [img['bbox'] for img in page.get_image_info(xrefs=True) if img['xref'] == green_xref]
            blocks = [b for b in sorted(page.get_text('blocks'), key=lambda b: b[1]) if b[4].strip()]

            # Group blocks by question
            q_blocks_list = []
            current_group = []
            for b in blocks:
                txt = b[4].strip()
                if 'Question Number :' in txt and 'Question Type : MCQ' in txt:
                    if current_group:
                        q_blocks_list.append(current_group)
                    current_group = [b]
                elif current_group:
                    current_group.append(b)
            if current_group:
                q_blocks_list.append(current_group)

            for grp in q_blocks_list:
                first_txt = grp[0][4]
                m_qnum = re.search(r'Question Number\s*:\s*(\d+)', first_txt)
                if not m_qnum:
                    continue
                qnum = int(m_qnum.group(1))
                if qnum == 1:
                    continue # confirmation question

                # separate question text from options
                q_text_blocks = []
                opt_blocks = []
                in_opts = False

                for b in grp:
                    txt = b[4].strip()
                    if 'Options :' in txt:
                        in_opts = True
                        before = txt.split('Options :')[0].strip()
                        if before:
                            q_text_blocks.append(before)
                        continue
                    if not in_opts:
                        if not any(header in txt for header in ['Question Number :', 'Correct Marks :', 'Question Label :']):
                            q_text_blocks.append(txt)
                    else:
                        opt_blocks.append(b)

                # parse options
                options = []
                labels = ['A', 'B', 'C', 'D', 'E']
                opt_idx = 0

                for b in opt_blocks:
                    txt = b[4].strip()
                    m_opt = re.match(r'^\d{10,}\.\s*(.*)', txt, re.DOTALL)
                    if m_opt:
                        opt_text = m_opt.group(1).strip()
                        by0, by1 = b[1], b[3]
                        is_corr = any(by0 - 6 <= (gy[1]+gy[3])/2 <= by1 + 6 for gy in green_boxes)
                        lbl = labels[opt_idx] if opt_idx < len(labels) else str(opt_idx+1)
                        opt_idx += 1
                        options.append({
                            'label': lbl,
                            'text': opt_text,
                            'is_correct': is_corr
                        })
                    else:
                        if options:
                            options[-1]['text'] += ' ' + txt
                            # recheck bounding box
                            by1 = max(options[-1].get('y1', b[3]), b[3])
                            if not options[-1]['is_correct']:
                                options[-1]['is_correct'] = any(b[1] - 6 <= (gy[1]+gy[3])/2 <= by1 + 6 for gy in green_boxes)

                q_prompt = ' '.join(q_text_blocks).strip()
                is_case = any(w in q_prompt.lower() for w in ['case', 'r-goura', 'canteen', 'company', 'scenario', 'xyz', 'firm'])

                # assign topic
                topic_title = 'Economics & Business Fundamentals (Quiz 1)' if q_name == 'Quiz 1' else 'Financial Analysis, Sales & Services (Quiz 2)'
                
                quizzes_parsed.append({
                    'id': f'{q_name.replace(" ", "")}_Q{qnum}',
                    'source': q_name,
                    'week': start_w if q_name == 'Quiz 1' else end_w,
                    'module': topic_title,
                    'q_num': qnum,
                    'is_case_based': is_case,
                    'question': q_prompt,
                    'options': options,
                    'feedback': '',
                    'mnemonic': 'Quiz Authentic TCS iON Exam Question',
                    'formula': ''
                })

    return quizzes_parsed

def enrich_and_export():
    ga_data = parse_all_gas()
    quiz_data = parse_tcs_quizzes()
    all_questions = ga_data + quiz_data
    
    print(f'Total GA Questions: {len(ga_data)}')
    print(f'Total Quiz Questions: {len(quiz_data)}')
    print(f'Combined Total Questions: {len(all_questions)}')

    output = {
        'metadata': {
            'course': 'Business Data Management (BDM) - MS2001',
            'institution': 'Indian Institute of Technology, Madras',
            'degree': 'BS in Data Science and Applications',
            'total_questions': len(all_questions),
            'topics': TOPIC_INFO
        },
        'questions': all_questions
    }

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as fp:
        json.dump(output, fp, indent=2, ensure_ascii=False)

    print(f'Successfully exported master dataset to {OUTPUT_JSON}')

if __name__ == '__main__':
    enrich_and_export()
