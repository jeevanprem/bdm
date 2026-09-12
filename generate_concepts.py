# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

CONCEPTS = {
    1: {
        "week": 1,
        "title": "Economics Foundations: Micro vs Macro, Scarcity & Choices",
        "tagline": "Duniya me resources limited hain, demands unlimited — Chunaav (Choice) kaise karein?",
        "mnemonic": "S - O - U - P (Scarcity, Opportunity cost, Unlimited wants, Prioritization)",
        "hinglish_summary": "Economics ka basic funda simple hai: Insaan ki chahatein (wants) kabhi khatam nahi hoti, lekin resources (paisa, samay, zameen, raw material) bohot limited hain. Isliye hume har pal 'CHOICE' karni padti hai. Pehle samjho Micro vs Macro: Microeconomics me hum INDIVIDUAL level par padhte hain (ek customer ka decision, ek firm ka pricing, ek market ka demand-supply). Jabki Macroeconomics me poore DESH ka aggregate dekha jata hai (GDP, Inflation, National Unemployment, RBI repo rate, Fiscal deficit). Sunk cost (jo paisa pehle kharch ho gaya aur wapas nahi mil sakta) ko economics me bilkul ignore kiya jata hai!",
        "core_terms": [
            {
                "term": "Microeconomics vs Macroeconomics",
                "hinglish": "Micro = Individual level (Ek household, ek firm, kisi ek cheez ki price aur demand-supply). Macro = Aggregate level (Desh ka GDP, Inflation, National Unemployment rate, RBI ki Monetary policy). Yaad rakhne ka trick: Micro me 'i' = Individual, Macro me 'a' = Aggregate!"
            },
            {
                "term": "Positive vs Normative Economics",
                "hinglish": "Positive Economics = Facts aur Science ('What is' — jo data se verify kiya ja sake, bina kisi emotion ke). Normative Economics = Value judgments aur Opinions ('What ought to be' — jaise 'Sarkar ko tax kam karna chahiye' ya 'Garibo ko free khana milna chahiye')."
            },
            {
                "term": "Free Goods vs Economic Goods",
                "hinglish": "Free Goods = Nature me unlimited hain, inki koi Opportunity Cost nahi hoti (Hawa, Dhoop). Economic Goods = Scarce hain, inko paane ke liye kuch aur chhodna padta hai aur inki positive opportunity cost aur price hoti hai."
            },
            {
                "term": "Scarcity (Kami)",
                "hinglish": "Resources limited hain par human desires unlimited hain. Har problem ki jad yahi hai. Agar sab kuch free aur unlimited hota, toh economics ki zaroorat hi nahi hoti!"
            },
            {
                "term": "Needs vs Wants vs Desires",
                "hinglish": "Needs = Zinda rehne ke liye zaroori (Roti, Kapda, Makaan, Paani). Wants = Needs ko satisfy karne ki specific chahat (Pyaas bujhane ke liye Bisleri ya Coke). Desires = Khwahish jisko khareedne ki aukat (purchasing power) na ho."
            },
            {
                "term": "Opportunity Cost (Chhoota Hua Mauka)",
                "hinglish": "Next Best Alternative ki value jo tumne kurbaan kar di! Dhyan rahe: Yeh saare options ka sum nahi hota, sirf AGLE SABSE BEST option ki value hoti hai."
            },
            {
                "term": "Sunk Cost (Dooba Hua Paisa)",
                "hinglish": "Wo kharcha jo ho chuka hai aur kisi bhi haal me wapas nahi aayega (jaise non-refundable flight ticket). Future decision lete waqt Sunk Cost ko ZERO maanna chahiye!"
            },
            {
                "term": "Rational Decision Making at Margin",
                "hinglish": "Insaan tabhi koi naya kadam uthayega jab aane wala fayda (Marginal Benefit MB) aane wale kharche (Marginal Cost MC) se bada ya barabar ho (MB >= MC)."
            },
            {
                "term": "Factors of Production & Factor Payments",
                "hinglish": "Char cheezein production me lagti hain: 1) Land (badle me milta hai Rent), 2) Labor (badle me milta hai Wages), 3) Capital (badle me milta hai Interest), 4) Entrepreneurship (badle me milta hai Profit)."
            }
        ],
        "formulas": [
            {
                "name": "Marginal Decision Rule",
                "formula": "Net Marginal Benefit = Marginal Benefit (MB) - Marginal Cost (MC) >= 0",
                "how_to_use": "Exam me numerical aaye ki 'Should the company produce 1 more unit?': Agar agla unit bechkar milne wala paisa (MB) usko banane ki cost (MC) se zyada hai, toh 'YES' karo, warna 'NO'."
            },
            {
                "name": "Opportunity Cost Calculation",
                "formula": "Opportunity Cost = Value of the Next Best Foregone Alternative",
                "how_to_use": "Agar ₹50 Lakh budget hai aur CS lab (₹50L) chuna, toh Sports stadium (₹50L) chhoot gaya. Opp cost = Sports stadium ka fayda. Saare departments ko jod mat dena!"
            }
        ],
        "key_exam_points": [
            "Microeconomics focuses on individual decision-making units (a consumer, a firm, price of tea). Macroeconomics focuses on aggregates (GDP, Inflation).",
            "Economics paiso ki padhai nahi hai, balki SCARCE RESOURCES ko allocate karne ki science hai.",
            "Free Goods have ZERO opportunity cost. Economic Goods have a POSITIVE opportunity cost.",
            "College ₹50 Lakh budget case: Student kehta hai 'yeh accounting problem hai kyunki paisa laga hai' — Galat! Yeh pure ECONOMICS problem hai kyunki competing alternatives me resource allocate karna hai.",
            "IPL Mega Auction ₹120 Crore cap: Franchise sabhi star players ko nahi khareed sakti kyunki financial capital SCARCE hai."
        ],
        "traps": "Trap 1: Sunk cost par question aayega (Mumbai flight ₹5,500 non-refundable). Sunk cost ko future decision me ZERO maano! Trap 2: 'Inflation in India is 6%' is a Positive statement (fact), while 'Inflation should be below 4%' is a Normative statement (opinion)!"
    },
    2: {
        "week": 2,
        "title": "Cost Behavior, Production & PPF Mechanics",
        "tagline": "Kharcha kitne type ka hota hai aur Factory ki maximum limit (PPF) kya hai?",
        "mnemonic": "B - I - O - S (Bowed-out=Increasing Opp Cost, Inside=Inefficient, On=Optimal, Shift=Growth)",
        "hinglish_summary": "Iss hafte do main cheezein hain: 1) Production Cost: Short-run me kam se kam ek factor fixed hota hai (jaise building). Isliye Fixed Cost (TFC) hamesha lagta hai, aur Variable Cost (TVC) units badhne par badhta hai. Explicit cost jeb se cash nikalna hota hai, jabki Implicit cost apna khud ka time ya capital lagane ki opportunity cost hoti hai! 2) PPF (Production Possibility Frontier): Yeh ek graph hai jo dikhata hai ki fixed resources me company do goods maximum kitne bana sakti hai. PPF concave (bowed-out) hota hai 'Law of Increasing Opportunity Cost' ki wajah se!",
        "core_terms": [
            {
                "term": "Fixed Cost (TFC) vs Variable Cost (TVC)",
                "hinglish": "TFC = Chahe factory band rahe, rent aur permanent manager salary lagegi. TVC = Production badhega toh raw material aur bijli ka kharcha badhega."
            },
            {
                "term": "Marginal Cost (MC)",
                "hinglish": "Sirf 1 extra unit banane me jeb se kitna extra paisa laga: MC = ΔTC / ΔQ. MC curve hamesha ATC aur AVC ke sabse lowest point (minimum) ko kaat-ti hai!"
            },
            {
                "term": "Explicit vs Implicit Cost",
                "hinglish": "Explicit Cost = Jeb se nikla actual cash (Rent, wages, raw material). Implicit Cost = Jo kamai chhod di (Maalik agar dukan na chala kar kahi naukri karta toh ₹50,000 kamata — yeh implicit cost hai)."
            },
            {
                "term": "Accounting Profit vs Economic Profit",
                "hinglish": "Accounting Profit = Revenue - Explicit Costs. Economic Profit = Revenue - Explicit Costs - Implicit Costs. Economic profit hamesha Accounting profit se CHHOTA ya barabar hota hai!"
            },
            {
                "term": "Law of Diminishing Marginal Returns",
                "hinglish": "Short-run me jab ek fixed machine par zyada se zyada workers lagate jaoge, toh shuru me output badhega, par ek point ke baad har naya worker pehle se KAM output dega (crowding ho jayegi)!"
            },
            {
                "term": "PPF Curve Points",
                "hinglish": "Curve ke UPAR (On curve) = Productively Efficient. Curve ke ANDAR (Inside) = Inefficient / Berozgari. Curve ke BAHAR (Outside) = Infeasible (aaj namumkin)."
            },
            {
                "term": "MRT (Slope of PPF)",
                "hinglish": "Marginal Rate of Transformation = |ΔY / ΔX|. Dikhata hai ki 1 unit Good X paane ke liye Good Y ke kitne units kurbaan karne padenge."
            }
        ],
        "formulas": [
            {
                "name": "Total Cost Formula",
                "formula": "TC = TFC + TVC  aur  ATC = TC / Q = AFC + AVC",
                "how_to_use": "AFC = TFC / Q. Jaise-jaise Quantity badhegi, AFC lagatar kam hoti jayegi (Spreading overheads)."
            },
            {
                "name": "Marginal Cost (MC)",
                "formula": "MC = ΔTC / ΔQ = ΔTVC / ΔQ",
                "how_to_use": "Dhyan do: MC nikalte waqt TFC ka koi role nahi hota kyunki TFC change nahi hota! Isliye MC sirf variable cost ke change se aati hai."
            },
            {
                "name": "Economic vs Accounting Profit",
                "formula": "Accounting Profit = Revenue - Explicit Cost\nEconomic Profit = Accounting Profit - Implicit Cost",
                "how_to_use": "Agar revenue ₹10L hai, explicit cost ₹6L hai, aur implicit cost ₹2L hai: Accounting Profit = ₹4L, Economic Profit = ₹2L."
            },
            {
                "name": "PPF Slope (Opportunity Cost)",
                "formula": "Slope of PPF = |ΔY / ΔX| = (Sacrificed Units of Y) / (Gained Units of X)",
                "how_to_use": "Agar 10 car se 8 car par aaye (loss = 2) aur trucks 0 se 5 ho gaye (gain = 5), toh 1 truck ki opportunity cost = 2/5 = 0.4 cars."
            }
        ],
        "key_exam_points": [
            "PPF 'bowed-out' (concave) kyun hota hai? Answer: 'Law of Increasing Opportunity Cost' — resources are specialized.",
            "Agar economy me recession ya berozgari hai, toh PPF shift nahi hota; economy PPF ke ANDAR kisi inefficient point par operate karti hai.",
            "Startup Data001 Case: 6 mahine ke liye client project lene par internal upgrade delay hui jisse ₹10K/month ki bachat ruk gayi. Opp cost = ₹10,000 × 6 = ₹60,000!"
        ],
        "traps": "Examiner puchega: 'Can Economic Profit be greater than Accounting Profit?' Kabhi nahi! Economic profit hamesha chhota ya barabar hoga kyunki usme implicit cost bhi ghatayi jati hai."
    },
    3: {
        "week": 3,
        "title": "Basics of Business, Business Models & Goods Classification",
        "tagline": "Dhandha kaise chalta hai: B2B vs B2C, Business Model Canvas, aur Goods classification!",
        "mnemonic": "S - E - C (Search=Seen before buying, Experience=Felt during/after, Credence=Trust even after consumption)",
        "hinglish_summary": "Business Model batata hai ki company paisa kaise banayegi (Value creation, delivery aur capture). B2B me customer company hoti hai (order size bada, lambi sales cycle, DMU decision team), jabki B2C me individual customer hota hai. Goods ko customer 3 tariko se judge karta hai: Search Goods (specs dekh kar pehle hi quality confirm), Experience Goods (khareed kar use karne ke baad pata chalta hai), aur Credence Goods (use karne ke baad bhi aam insaan judge nahi kar sakta, sirf brand trust par chalta hai).",
        "core_terms": [
            {
                "term": "B2B, B2C, C2C, B2G",
                "hinglish": "B2B: Intel selling to Dell. B2C: Amazon selling to consumer. C2C: OLX / eBay peer-to-peer. B2G: Defense supplier selling to Government."
            },
            {
                "term": "Search Goods (S)",
                "hinglish": "Dukan par ya online specs padhkar khareedne se PEHLE hi quality pata chal jati hai (Laptop RAM, Mobile processor, Kapde ka size, Kitaab)."
            },
            {
                "term": "Experience Goods (E)",
                "hinglish": "Khareedne aur use karne ke BAAD hi pata chalta hai ki kaisa tha (Restaurant ka khana, Cinema ticket, Vacation resort, Salon haircut)."
            },
            {
                "term": "Credence Goods (C)",
                "hinglish": "Consume karne ke baad bhi aam insaan judge nahi kar sakta ki sahi hua ya galat (Car ka brake repair, Dil ki surgery, Legal case advice). Yahan sirf Brand aur Trust bikta hai!"
            },
            {
                "term": "Business Model Canvas (9 Blocks)",
                "hinglish": "1) Value Proposition, 2) Customer Segments, 3) Channels, 4) Customer Relationships, 5) Revenue Streams, 6) Key Resources, 7) Key Activities, 8) Key Partners, 9) Cost Structure."
            },
            {
                "term": "Revenue Models",
                "hinglish": "Subscription (Netflix), Freemium (Spotify), Marketplace Commission (Uber/Amazon), Pay-per-use (Cloud AWS), Licensing (Microsoft Windows)."
            },
            {
                "term": "Unit Economics: CAC & CLV",
                "hinglish": "CAC = Customer Acquisition Cost (ek naya customer lane ka marketing kharcha). CLV = Customer Lifetime Value (wo customer zindagibhar me kitna munafa dega). Healthy rule: CLV / CAC >= 3 hona chahiye!"
            }
        ],
        "formulas": [
            {
                "name": "Customer Perceived Value",
                "formula": "Perceived Value = Total Perceived Benefits - Total Perceived Costs",
                "how_to_use": "Customer tabhi purchase karega jab Perceived Value > 0 ho."
            },
            {
                "name": "LTV to CAC Ratio",
                "formula": "Ratio = Customer Lifetime Value (CLV) / Customer Acquisition Cost (CAC)",
                "how_to_use": "Agar ratio < 1 hai toh company har naye customer par loss kar rahi hai!"
            }
        ],
        "key_exam_points": [
            "Services me sabse zyada Experience aur Credence qualities hoti hain, Search qualities bohot kam hoti hain.",
            "B2B sales me formal contracts aur agreements bohot zyada hote hain kyunki risk, paisa, aur legal liability bohot badi hoti hai.",
            "High price par bhi agar log baar-baar khareedte hain, toh product me strong BRAND EQUITY aur INELASTIC DEMAND hoti hai."
        ],
        "traps": "Direct question: 'A doctor recommends knee surgery. What kind of good is this?' Trap me log Experience good laga dete hain. Correct answer is CREDENCE GOOD kyunki surgery ke baad bhi patient ko medically pata nahi chalta ki procedure 100% zaroori tha ya perfect tha."
    },
    4: {
        "week": 4,
        "title": "Demand, Supply, Market Equilibrium & Elasticities",
        "tagline": "Price badhegi toh public kitna bhagegi? Elasticity ka poora khel!",
        "mnemonic": "P - E - R - K (Inelastic: Price aur Revenue SAME direction me chalte hain; Elastic: OPPOSITE direction)",
        "hinglish_summary": "Law of Demand: Price badhegi toh Demand ghategi (Inverse). Law of Supply: Price badhegi toh Supply badhegi (Direct). Jahan dono intersect karte hain wo Equilibrium (P*, Q*) hota hai. Elasticity (Ep) batata hai ki price badalne par demand kitni tezi se jhatka khati hai. Inelastic goods (namak, life-saving medicines) me price badhaoge toh revenue badhega. Elastic goods (luxury, restaurant dining) me price badhaoge toh public bhag jayegi aur revenue gir jayega! Cross elasticity substitutes me positive hoti hai aur complements me negative hoti hai.",
        "core_terms": [
            {
                "term": "Movement vs Shift",
                "hinglish": "Apni price badli toh sirf MOVEMENT along curve hoga (Change in Quantity Demanded). Income, substitutes, fashion badla toh poora curve SHIFT ho jayega (Change in Demand)."
            },
            {
                "term": "Price Elasticity of Demand (Ep)",
                "hinglish": "|Ep| > 1 = Elastic (Luxury). |Ep| < 1 = Inelastic (Necessities). |Ep| = 1 = Unitary Elastic (Total Revenue maximum hota hai!)."
            },
            {
                "term": "Cross-Price Elasticity (Exy)",
                "hinglish": "Exy > 0 (Positive) = Substitutes (Chai aur Coffee). Exy < 0 (Negative) = Complements (Car aur Petrol). Exy = 0 = Unrelated goods."
            },
            {
                "term": "Income Elasticity (Ey)",
                "hinglish": "Ey > 0 = Normal Good (Ey > 1 Luxury, 0 < Ey <= 1 Necessity). Ey < 0 = Inferior Good (income badhne par log saste chawal ya local bus chhod dete hain)."
            },
            {
                "term": "Consumer & Producer Surplus",
                "hinglish": "Consumer Surplus = Jo price customer dene ko taiyar tha minus jo usne actual di (Willingness to pay - Price). Producer Surplus = Actual price received - Minimum supply cost."
            },
            {
                "term": "Price Ceiling (Price Cap)",
                "hinglish": "Sarkar ne equilibrium se NEECHE maximum rate fix kar diya (jaise R-Goura's mess case). Result: Demand badhegi, supply ghategi, aur market me SHORTAGE aur lambi line lag jayegi!"
            }
        ],
        "formulas": [
            {
                "name": "Price Elasticity Formula",
                "formula": "Ep = (% Change in Quantity Demanded) / (% Change in Price) = (ΔQ / Q) / (ΔP / P)",
                "how_to_use": "Agar Petrol ki price 10% badhi (+10%) aur demand 5% ghati (-5%), toh Ep = -5 / +10 = -0.5. Absolute value |0.5| < 1, iska matlab demand INELASTIC hai!"
            },
            {
                "name": "Total Revenue (TR) Test",
                "formula": "TR = Price × Quantity",
                "how_to_use": "Agar demand Inelastic hai: Price badhao => Revenue BADHEGA! Agar demand Elastic hai: Price ghatao => Revenue BADHEGA! Max revenue tab milta hai jab |Ep| = 1."
            }
        ],
        "key_exam_points": [
            "Amazon Prime subscription price badhane par subscribers cancel karte hain — yeh ELASTIC demand ka demonstration hai.",
            "Bumper crop (zyada kheti) hone par farmers ko nuksan kyun hota hai? Kyunki food grains ki demand inelastic hoti hai, supply badhne se price bohot zyada gir jati hai aur total revenue kam ho jata hai!",
            "R-Goura's Canteen Case (Quiz 1): Price cap lagane se natural equilibrium disturb hota hai aur SHORTAGE create hoti hai."
        ],
        "traps": "Examiner puchega: 'Cross elasticity between Butter and Margarine is positive or negative?' Butter aur Margarine substitutes hain, isliye POSITIVE (+ve) hoga!"
    },
    5: {
        "week": 5,
        "title": "Introduction to Accounting & Asset Classification",
        "tagline": "Accounts ki teen shaakhayein, 10 GAAP Rules, aur Real Estate Builder ka Asset Trap!",
        "mnemonic": "12-Month Operating Intent Rule: Bechne ke liye rakha hai = Inventory (Current Asset); Kaam chalane ke liye >1 saal = Fixed Asset",
        "hinglish_summary": "Accounting 3 type ki hoti hai: Financial (external, historical, GAAP mandatory), Managerial (internal managers ke liye, budgets, no strict format), aur Cost accounting. 10 fundamental GAAP principles har exam me aate hain: Business Entity, Money Measurement, Going Concern, Historical Cost, Matching, Revenue Recognition, Conservatism, Materiality, Dual Aspect, aur Periodicity. Sabse bada asset trap: Koi cheez asset hai ya inventory, yeh company ke BUSINESS INTENT par depend karta hai!",
        "core_terms": [
            {
                "term": "The 10 Core GAAP Principles",
                "hinglish": "1) Business Entity: Owner aur company alag hain. 2) Money Measurement: Sirf paiso wali cheezein likhi jayengi (employee morale nahi). 3) Going Concern: Company hamesha chalti rahegi. 4) Historical Cost: Asset khareedne wale original rate par likha jata hai. 5) Revenue Recognition: Maal deliver hone par revenue record hoti hai, cash aane par nahi! 6) Matching: Revenue kamane ke kharche usi saal record honge. 7) Conservatism (Prudence): Aane wale har nuksan ka provision banao, par munafa tab tak mat gino jab tak hath me na aaye! 8) Materiality: Chhoti-moti cheez (jaise ₹50 ka stapler) direct expense maano, asset nahi. 9) Dual Aspect: Har debit ka equal credit. 10) Periodicity: Har 1 saal ka hisab."
            },
            {
                "term": "The Intent of Ownership Rule (The DLF Trap)",
                "hinglish": "Ek manufacturing factory ke liye Building = FIXED ASSET (PP&E) hai. Lekin ek Real Estate Developer (jaise DLF ya Godrej Properties) ke liye wahi Buildings aur Apartments = INVENTORY (Current Asset) hain kyunki unhe bechne ke liye banaya hai!"
            },
            {
                "term": "CapEx vs OpEx",
                "hinglish": "CapEx (Capital Expenditure) = Nayi machine ya factory khareedna jo >1 saal fayda dega (Balance sheet me asset banta hai). OpEx (Operating Expenditure) = Bijli ka bill, salary, daily maintenance (P&L me expense banta hai)."
            },
            {
                "term": "Current Assets vs Fixed Assets",
                "hinglish": "Current = 12 mahine ke andar cash ban jayega (Cash, Debtors, Inventory, Prepaid rent). Fixed = Long-term operations me kaam aayega."
            }
        ],
        "formulas": [
            {
                "name": "Balance Sheet Asset Total",
                "formula": "Total Assets = Current Assets (Cash + Debtors + Inventory) + Non-Current Fixed Assets (Net Block + CWIP + Intangibles)",
                "how_to_use": "XYZ Ltd case me: Fixed Assets (6,000) + Inventory (3,500) + Debtors (4,000) + Cash & Others (16,500) = ₹30,000 Cr."
            }
        ],
        "key_exam_points": [
            "Manager ko naye product development ke liye budget aur cost analysis chahiye — yeh data MANAGERIAL ACCOUNTING provide karegi.",
            "Real Estate firm ke liye buildings kya hain? Answer: INVENTORY (Current Asset).",
            "A product delivered in October but paid in November: Revenue is recognized in OCTOBER (Revenue Recognition Principle)."
        ],
        "traps": "Exam trap: 'An entrepreneur buys a ₹10,000 software license valid for 3 years. Is it an asset or expense?' It is an INTANGIBLE ASSET (CapEx) because benefit lasts for 3 years (> 12 months)!"
    },
    6: {
        "week": 6,
        "title": "Accounting Equation, Transactions & Income Statement",
        "tagline": "Assets = Liabilities + Equity ka balance aur Debit/Credit ka asan raaz!",
        "mnemonic": "A - L - O - E & DEAL (Debit: Drawings, Expenses, Assets) vs CLIP (Credit: Liabilities, Income, Capital)",
        "hinglish_summary": "Fundamental Equation hai: Assets = Liabilities + Owner's Equity. Har transaction do jagah asar daalta hai. Owner jab company se personal kharche ke liye paisa nikalta hai, usko 'DRAWINGS' kehte hain, aur yeh Equity ko kam karta hai. Inventory valuation me FIFO (First-In, First-Out: pehle aaya maal pehle bika) me inflation ke waqt ending inventory ki value zyada aati hai aur profit zyada dikhta hai. Depreciation ka Straight Line Method (SLM) har saal barabar kharcha kaatta hai!",
        "core_terms": [
            {
                "term": "Fundamental Accounting Equation",
                "hinglish": "Assets = Liabilities + Owner's Equity. Assets = Bahar walo se udhar (Liabilities) + Maalik ka apna paisa (Equity)."
            },
            {
                "term": "Drawings (Personal Nikaas)",
                "hinglish": "Maalik ne company ke account se apne ghar ka rent bhara — yeh company ka business expense nahi hai, yeh DRAWINGS hai jo Equity ko kam karega!"
            },
            {
                "term": "FIFO vs LIFO Inventory Valuation",
                "hinglish": "FIFO (First-In, First-Out): Pehle khareeda hua sasta maal pehle becha $\implies$ COGS kam, Reported Profit zyada, Ending inventory mehenga dikhega. LIFO (Last-In, First-Out): Aakhri me khareeda mehenga maal pehle becha $\implies$ COGS zyada, Tax bachega!"
            },
            {
                "term": "Depreciation: SLM vs WDV",
                "hinglish": "SLM (Straight Line): Har saal barabar depreciation kat-ta hai: (Cost - Salvage) / Life. WDV (Written Down Value): Shuru ke saalo me zyada depreciation kat-ta hai, baad me kam."
            },
            {
                "term": "Gross Profit vs EBIT vs PAT",
                "hinglish": "Revenue me se COGS ghatao = Gross Profit. Gross Profit me se OpEx ghatao = Operating Profit (EBIT). EBIT me se Interest ghatao = PBT. PBT me se Tax ghatao = Net Profit (PAT)!"
            }
        ],
        "formulas": [
            {
                "name": "Accounting Equation",
                "formula": "Assets = Liabilities + Equity (Capital + Retained Earnings - Drawings + Revenue - Expenses)",
                "how_to_use": "Har transaction ke baad check karo: Left side (Assets) = Right side (Liabilities + Equity) hona hi chahiye."
            },
            {
                "name": "Straight Line Depreciation (SLM)",
                "formula": "Annual Depreciation = (Original Cost - Salvage Value) / Useful Life in Years",
                "how_to_use": "Cost = ₹21,000, Salvage = ₹1,000, Life = 5 years: Depreciation = (21,000 - 1,000) / 5 = ₹4,000 per year."
            }
        ],
        "key_exam_points": [
            "Subtracting Cost of Goods Sold (COGS) from Sales Revenue gives: GROSS PROFIT.",
            "Paying off ₹3,000 accounts payable reduces Cash by ₹3,000 and reduces Payables by ₹3,000.",
            "Owner withdrawing cash for personal use is debited to DRAWINGS account."
        ],
        "traps": "Exam trap: 'Owner paid personal house rent from business bank account. Which account is debited?' Option me Rent Expense diya hota hai — DO NOT tick Rent Expense! Correct answer is DRAWINGS ACCOUNT!"
    },
    7: {
        "week": 7,
        "title": "Financial Ratios, Solvency & Cash Flow Classification",
        "tagline": "Company kitni tazi se karz chukayegi aur Cash kahan se aa raha hai (O-I-F)?",
        "mnemonic": "O - I - F (Operating=Daily Core, Investing=Long-term PP&E, Financing=Debt, Shares, Dividends)",
        "hinglish_summary": "Do type ke risk hote hain: Short-term risk (Liquidity — Current Ratio aur Quick Ratio) aur Long-term risk (Solvency — Debt-to-Equity aur Interest Coverage Ratio ICR). Debt-Equity 4:1 ka matlab company bohot zyada karz me doobi hai. Profitability aur Liquidity me zameen-aasmaan ka farq hai: Company paper par bohot bhaari Profit dikha sakti hai, lekin agar cash hath me nahi hai toh bijli ka bill na bhar pane se diwaliya (bankrupt) ho sakti hai! Cash flow ke 3 hisse hote hain: Operating, Investing, Financing.",
        "core_terms": [
            {
                "term": "Current Ratio vs Quick Ratio",
                "hinglish": "Current Ratio = Current Assets / Current Liabilities (Ideal ~ 2:1). Quick Ratio = (Current Assets - Inventory - Prepaid) / Current Liabilities (Ideal ~ 1:1). Quick ratio me se Inventory isliye nikalte hain kyunki inventory ko turant bechkar cash banana mushkil hota hai!"
            },
            {
                "term": "Debt-to-Equity Ratio (D/E)",
                "hinglish": "Total Debt / Shareholders' Equity. Agar D/E = 4:1 hai, iska matlab maalik ke ₹1 ke badle company ne market se ₹4 ka karz le rakha hai — high risk of bankruptcy!"
            },
            {
                "term": "Interest Coverage Ratio (ICR)",
                "hinglish": "ICR = EBIT / Interest Expense. Dikhata hai ki company apne munafay se kitni baar karz ka byaj (interest) chuka sakti hai. ICR < 1.5 hone par bank loan dene se mana kar dete hain."
            },
            {
                "term": "Cash Flow Activities (O-I-F)",
                "hinglish": "Operating = Core dhandha (Customer se mila cash, supplier ko diya cash). Investing = Plant, machinery, factory khareedna ya bechna. Financing = Share issue karna, bank loan lena ya wapas karna, dividend dena."
            }
        ],
        "formulas": [
            {
                "name": "Current Ratio & Quick Ratio",
                "formula": "CR = CA / CL  |  Quick Ratio = (CA - Inventory - Prepaid) / CL",
                "how_to_use": "Agar CA = 24,000, CL = 15,000, Inv = 3,500: CR = 24,000/15,000 = 1.60 | QR = (24,000 - 3,500)/15,000 = 1.37."
            },
            {
                "name": "Interest Coverage Ratio (ICR)",
                "formula": "ICR = Operating Profit (EBIT) / Finance Costs (Interest)",
                "how_to_use": "XYZ Ltd case me: EBIT = 4,500 Cr, Interest = 200 Cr. ICR = 4,500 / 200 = 22.5 times!"
            },
            {
                "name": "Working Capital",
                "formula": "Net Working Capital = Current Assets - Current Liabilities",
                "how_to_use": "Agar NWC positive hai toh short-term liquidity acchi hai."
            }
        ],
        "key_exam_points": [
            "Company buys a new factory building for cash — classified as: CASH OUTFLOW FROM INVESTING ACTIVITIES.",
            "Firm reports significant Net Profit but cannot pay electricity bill — this highlights the difference between PROFITABILITY and LIQUIDITY (Cash Flow).",
            "High Debt-Equity ratio (4:1) signals to potential lenders that the company is HIGHLY LEVERAGED with higher default risk."
        ],
        "traps": "Exam trap: 'Payment of dividend to shareholders is which activity?' Option me Operating laga dete hain. Bilkul galat! Dividend dena maalik ko capital return karna hai, so it is FINANCING ACTIVITY!"
    },
    8: {
        "week": 8,
        "title": "Corporate Financial Statements Case Study (XYZ Limited)",
        "tagline": "End-term exam ka sabse bada case study — P&L, Balance Sheet aur 12 Ratios ka complete formula master!",
        "mnemonic": "DuPont Pyramid: ROE = Net Margin (Profitability) × Asset Turnover (Efficiency) × Equity Multiplier (Leverage)",
        "hinglish_summary": "Week 8 me IIT Madras ne XYZ Limited (Commercial vehicle manufacturer) ka complete simplified P&L aur Balance Sheet diya hai aur 12 consecutive questions puche hain. Yeh numbers seedhe exam me aate hain! Yahan revenue ₹40,000 Cr hai, PAT ₹3,375 Cr hai, Assets ₹30,000 Cr hain, aur Equity ₹12,500 Cr hai. Har ratio ko dhyan se samjho: Net Margin = 8.44%, Operating Margin = 11.25%, ROE = 27.0%, EPS = ₹6.75, P/E = 22.22, Dividend Yield = 1.33%, aur Market Cap = ₹75,000 Cr.",
        "core_terms": [
            {
                "term": "XYZ Ltd Base Data",
                "hinglish": "Revenue: ₹40,000 Cr | Expenses: Materials 28,000 + Employees 2,500 + Other 4,000 + Depr 800 + Finance 200 = 35,500 Cr | PBT: 4,500 Cr | Tax: 1,125 Cr | PAT: 3,375 Cr."
            },
            {
                "term": "XYZ Ltd Balance Sheet Data",
                "hinglish": "Equity Share Capital (Face value ₹1): ₹500 Cr (500 Cr shares) | Reserves: ₹12,000 Cr => Total Equity = ₹12,500 Cr | Debt: ₹2,500 Cr | Current Liabilities: ₹15,000 Cr | Total Assets: ₹30,000 Cr (Current Assets = ₹24,000 Cr, Fixed Assets = ₹6,000 Cr)."
            },
            {
                "term": "Market Info",
                "hinglish": "Current Market Price (CMP) per share = ₹150 | Dividend Declared per share = ₹2.00."
            }
        ],
        "formulas": [
            {
                "name": "1. Net Profit Margin",
                "formula": "(PAT / Revenue) × 100 = (3,375 / 40,000) × 100",
                "how_to_use": "Exact value: 8.4375% => Rounds to 8.44%."
            },
            {
                "name": "2. Operating Margin (EBIT Margin)",
                "formula": "(Operating Profit EBIT / Revenue) × 100",
                "how_to_use": "EBIT = Revenue (40,000) - Operating Costs (35,500 - 200 interest) = ₹4,500 Cr. Operating Margin = (4,500 / 40,000) × 100 = 11.25%."
            },
            {
                "name": "3. Total Operating Expenses (Excluding Depr & Interest)",
                "formula": "Total Expenses (35,500) - Depreciation (800) - Finance Costs (200)",
                "how_to_use": "35,500 - 800 - 200 = ₹34,500 Crores."
            },
            {
                "name": "4. Current Ratio & Quick Ratio",
                "formula": "CR = CA / CL = 24,000 / 15,000 = 1.60 | QR = (24,000 - 3,500) / 15,000 = 1.37",
                "how_to_use": "Current Assets me Inventory 3,500 + Debtors 4,000 + Cash 16,500 = 24,000 Cr."
            },
            {
                "name": "5. Return on Equity (ROE)",
                "formula": "ROE = (Net Profit / Total Shareholder's Equity) × 100",
                "how_to_use": "(3,375 / 12,500) × 100 = 27.00%."
            },
            {
                "name": "6. DuPont 3-Step ROE",
                "formula": "ROE = Net Margin × Asset Turnover × Equity Multiplier",
                "how_to_use": "(3,375/40,000) × (40,000/30,000) × (30,000/12,500) = 8.4375% × 1.3333 × 2.400 = 27.0%."
            },
            {
                "name": "7. EPS, P/E Ratio & Dividend Yield",
                "formula": "EPS = PAT / Shares = 3,375 / 500 = ₹6.75 | P/E = Market Price / EPS = 150 / 6.75 = 22.22 | Div Yield = (DPS / Market Price) × 100 = (2 / 150) × 100 = 1.33%",
                "how_to_use": "Face value ₹1 hai, isliye Share Capital ₹500 Cr ka matlab exactly 500 Crore shares hain!"
            },
            {
                "name": "8. Market Capitalization",
                "formula": "Total Shares × Market Price per Share",
                "how_to_use": "500 Crore shares × ₹150 = ₹75,000 Crores."
            },
            {
                "name": "9. Inventory Turnover Ratio",
                "formula": "Cost of Materials Consumed (COGS) / Inventory",
                "how_to_use": "28,000 / 3,500 = 8.00 times."
            }
        ],
        "key_exam_points": [
            "All 12 values from XYZ Limited case must be on your fingertips — they are frequently repeated in Quiz 2 and Endsem!",
            "Number of shares = Equity Share Capital / Face Value = 500 Cr / ₹1 = 500 Cr shares.",
            "Equity Multiplier = Total Assets / Total Equity = 30,000 / 12,500 = 2.40."
        ],
        "traps": "Trap 1: P/E nikalte waqt Face Value (₹1) mat le lena! Market Price (₹150) lena hota hai: 150 / 6.75 = 22.22! Trap 2: Operating expenses me log depreciation include kar lete hain — question me saaf likha hota hai 'excluding depreciation and finance costs' (₹34,500 Cr)!"
    },
    9: {
        "week": 9,
        "title": "Management Accounting, CVP & Responsibility Centers",
        "tagline": "Company ke departments ka evaluation (C-R-P-I) aur Break-Even Point ka formula!",
        "mnemonic": "C - R - P - I (Cost -> Revenue -> Profit -> Investment Centers)",
        "hinglish_summary": "Badi companies me departments ko 'Responsibility Centers' me baant diya jata hai: Cost Center (kharcha kam karna), Revenue Center (sales badhana), Profit Center (munafa dikhana), aur Investment Center (capital par return ROI/EVA nikalna). Iske alawa Cost-Volume-Profit (CVP) analysis batata hai ki kitne units bechne par 'No Profit No Loss' hoga (Break-Even Point BEP). Break-even ke upar ki har sale par company 'Margin of Safety' me hoti hai!",
        "core_terms": [
            {
                "term": "Cost Center (Expense Center)",
                "hinglish": "Manager ki performance check hoti hai ki usne budget ke andar reh kar kaam kiya ya nahi (Maintenance, Legal, HR, IT helpdesk)."
            },
            {
                "term": "Revenue Center",
                "hinglish": "Manager sirf revenue target achieve karne ke liye responsible hai (Regional sales team)."
            },
            {
                "term": "Profit Center",
                "hinglish": "Manager ke paas pricing aur cost dono ka control hota hai (McDonald's ka individual franchise restaurant)."
            },
            {
                "term": "Investment Center",
                "hinglish": "Manager capital asset lagane/bechne ka faisla le sakta hai. Performance metric: Return on Investment (ROI) ya Economic Value Added (EVA)."
            },
            {
                "term": "Contribution Margin & P/V Ratio",
                "hinglish": "Contribution = Selling Price - Variable Cost per unit. P/V Ratio (Profit-Volume) = (Contribution / Sales) × 100."
            },
            {
                "term": "Break-Even Point (BEP)",
                "hinglish": "Wo point jahan Total Revenue = Total Cost hota hai (Zero Profit, Zero Loss). BEP ke baad banne wala har unit seedhe profit deta hai!"
            },
            {
                "term": "Margin of Safety (MoS)",
                "hinglish": "Actual Sales minus Break-Even Sales. Yeh dikhata hai ki kitni sale girne par bhi company loss me nahi jayegi."
            }
        ],
        "formulas": [
            {
                "name": "Break-Even Point (in Units)",
                "formula": "BEP (Units) = Total Fixed Cost / (Selling Price - Variable Cost per unit) = TFC / Contribution per unit",
                "how_to_use": "Agar Fixed Cost ₹1,00,000 hai, Price ₹50 hai, VC ₹30 hai: Contribution = 20. BEP = 1,00,000 / 20 = 5,000 units."
            },
            {
                "name": "Break-Even Point (in ₹ Value)",
                "formula": "BEP (Value) = Total Fixed Cost / P/V Ratio",
                "how_to_use": "P/V Ratio = 20/50 = 40%. BEP (Value) = 1,00,000 / 0.40 = ₹2,50,000."
            },
            {
                "name": "Return on Investment (ROI)",
                "formula": "ROI = Net Operating Income / Average Operating Assets",
                "how_to_use": "Investment Center managers ko evaluate karne ka primary formula."
            }
        ],
        "key_exam_points": [
            "Financial accounting aggregated and historical data deta hai, jo internal managerial decision making ke liye insufficient hai.",
            "Responsibility accounting decentralization ko support karta hai aur har manager ko uske span of control ke hisab se evaluate karta hai.",
            "Maintenance department ek COST CENTER hai."
        ],
        "traps": "Trap question: 'Is a regional sales branch a profit center?' Nahi! Agar unhe price aur product cost control karne ka haq nahi hai, toh wo sirf REVENUE CENTER hain!"
    },
    11: {
        "week": 11,
        "title": "Personal Selling, Sales Process & Prospecting Funnel",
        "tagline": "Maal bechne ke 7 chronological kadam — Lead dhoondhne se lekar Deal close karne tak!",
        "mnemonic": "P - P - A - P - H - C - F (Prospecting, Pre-approach, Approach, Presentation, Handling objections, Closing, Follow-up)",
        "hinglish_summary": "B2B Sales me koi tukka nahi chalta, ek scientific 7-step process hoti hai: 1) Prospecting: Potential customer (lead) dhoondhna aur check karna ki kya uske paas M-A-N (Money, Authority, Need) hai. 2) Pre-approach: Meeting se pehle customer ke baare me homework aur research karna. 3) Approach: Pehli meeting me accha impression banana aur rapport create karna (PSP technique). 4) Presentation: FAB framework (Features, Advantages, Benefits) aur SPIN Model se pitch karna. 5) Handling Objections: Customer ke shaq aur doubts ko door karna. 6) Closing: Order sign karwana. 7) Follow-up: Delivery ensure karna aur long-term relation banana.",
        "core_terms": [
            {
                "term": "1. Prospecting & Qualifying (MAN Rule)",
                "hinglish": "Naye potential buyers dhoondhna. Har contact 'Prospect' nahi hota; qualify tabhi hota hai jab uske paas Money (budget), Authority (faisla lene ka haq), aur Need (zaroorat) ho!"
            },
            {
                "term": "2. Pre-approach (Homework Phase)",
                "hinglish": "Client se milne se pehle uski company, industry, pain points aur background research karna."
            },
            {
                "term": "3. Approach & PSP Technique",
                "hinglish": "First impression phase! PSP = Personal Selling Principles / Problem-Solution-Presentation. Client ka dhyaan kheench kar meeting set karna."
            },
            {
                "term": "4. Presentation & FAB Analysis",
                "hinglish": "F = Feature (product me kya hai: 128GB storage), A = Advantage (yeh kya karta hai: bohot saari videos save kar sakta hai), B = Benefit (customer ko kya fayda: tumhe travel karte waqt internet ki zaroorat nahi padegi!). Customer hamesha BENEFITS khareedta hai!"
            },
            {
                "term": "SPIN Selling Model",
                "hinglish": "S = Situation questions (current halat), P = Problem questions (dikkat kahan aa rahi hai), I = Implication questions (agar theek nahi kiya toh kitna nuksan hoga), N = Need-payoff questions (agar hum solve kar dein toh kitna munafa hoga)."
            },
            {
                "term": "5. Handling Objections",
                "hinglish": "Customer jab bolta hai 'tumhara rate bohot mehanga hai' — toh usse behas mat karo! Usko Value aur ROI dikha kar objection ko selling opportunity me badlo."
            },
            {
                "term": "6. Closing & 7. Follow-up",
                "hinglish": "Closing = Order maangna (Assumptive close, urgency close). Follow-up = Maal bechne ke baad phone karke puchna ki koi dikkat toh nahi aayi — yeh repeat business deta hai."
            }
        ],
        "formulas": [
            {
                "name": "Sales Conversion Rate",
                "formula": "Conversion Rate = (Deals Closed / Total Qualified Prospects) × 100",
                "how_to_use": "Sales Funnel efficiency napne ka formula."
            }
        ],
        "key_exam_points": [
            "Process of identifying potential customers is called: PROSPECTING.",
            "Pre-approach phase includes: Background research, setting call objectives, and choosing the right approach strategy.",
            "FAB technique: Features describe the product, Benefits describe the customer value."
        ],
        "traps": "Exam order trap: Examiner puchega 'Which step comes immediately after Approach?' Sequence yaad rakho PPAPHCF — Approach ke turant baad PRESENTATION aati hai!"
    },
    12: {
        "week": 12,
        "title": "Services Marketing, Service Quality & Service Recovery",
        "tagline": "Service bechna physical product se alag kyun hai? 5 Gaps Model aur Service Recovery Paradox!",
        "mnemonic": "R - A - T - E - R (SERVQUAL) & I - H - I - P (Service Characteristics)",
        "hinglish_summary": "Services physical goods se bilkul alag hoti hain (IHIP): Intangible (chhoo nahi sakte), Heterogeneous (har baar deliver karne wale ke hisab se quality thodi alag ho sakti hai), Inseparable (production aur consumption ek sath hota hai jaise haircut ya doctor checkup), aur Perishable (khali bachi plane ki seat ya hotel room ko kal ke liye store nahi kar sakte). Service quality napne ke liye SERVQUAL ke 5 dimensions hote hain: RATER (Reliability, Assurance, Tangibles, Empathy, Responsiveness). Sabse mazedaar concept hai 'Service Recovery Paradox': Agar service me galti ho jaye aur company turant sorry bolkar zabardast solution de de, toh wo customer us customer se bhi zyada loyal ban jata hai jiske sath kabhi koi dikkat hi nahi aayi thi!",
        "core_terms": [
            {
                "term": "IHIP Characteristics of Services",
                "hinglish": "Intangibility (No physical touch), Heterogeneity/Variability (Human factor), Inseparability (Simultaneous creation and use), Perishability (Cannot be stored in warehouse)."
            },
            {
                "term": "7Ps of Services",
                "hinglish": "Traditional 4Ps (Product, Price, Place, Promotion) + 3 Extra Ps: People (employees), Process (service delivery steps), Physical Evidence (office interior, dress code, ambience)."
            },
            {
                "term": "RATER (SERVQUAL Dimensions)",
                "hinglish": "R = Reliability (jo promise kiya wo deliver kiya), A = Assurance (employees ka gyaan aur trust), T = Tangibles (cleanliness, equipment, uniform), E = Empathy (personal dhyan dena), R = Responsiveness (jaldi reply aur prompt service)."
            },
            {
                "term": "The 5 Gaps Model of Service Quality",
                "hinglish": "Gap 1: Management ko pata hi nahi customer kya chahta hai. Gap 2: Management ko pata hai par quality standard galat banaya. Gap 3: Employees standard deliver nahi kar paye. Gap 4: Advertisement me jo bola delivery me wo nahi mila. Gap 5: Customer Expectation aur Actual Experience ka final gap!"
            },
            {
                "term": "Service Recovery Paradox",
                "hinglish": "Galti hone ke baad agar company ne dil jeet liya, toh customer pehle se zyada bada fan ban jata hai! Lekin pehla kadam hamesha: Problem ko acknowledge karo aur dil se apology do."
            },
            {
                "term": "Zone of Tolerance",
                "hinglish": "Customer ki Desired Service (jo wo chahta hai) aur Adequate Service (jo minimum wo jhel sakta hai) ke beech ka gap."
            }
        ],
        "formulas": [
            {
                "name": "Service Quality Gap (Gap Model)",
                "formula": "Perceived Service Quality (Q) = Perceived Experience (P) - Expected Service (E)",
                "how_to_use": "Agar Experience > Expectations => Customer Delighted! Agar Experience < Expectations => Service Failure."
            }
        ],
        "key_exam_points": [
            "What is service recovery mainly about? Answer: RESTORING CUSTOMER SATISFACTION FOLLOWING A SERVICE FAILURE.",
            "First crucial step in service recovery: Acknowledge the failure promptly, listen attentively, and apologize sincerely.",
            "An empty flight seat that flies cannot be inventoried — this illustrates PERISHABILITY of services."
        ],
        "traps": "Exam trap: 'Can a company rely on the Service Recovery Paradox instead of providing good initial service?' Bilkul NAHI! Har baar galti karke sudharna bohot costly aur risky hota hai; yeh sirf failure management ka tool hai, initial strategy nahi!"
    }
}

# Export to concepts_data.js
js_content = "window.BDM_CONCEPTS = " + json.dumps(CONCEPTS, ensure_ascii=False, indent=2) + ";\n"

with open(r'd:\ai codings\bdm html\concepts_data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Successfully updated concepts_data.js ({len(js_content)} bytes, {len(CONCEPTS)} weeks enriched)")
