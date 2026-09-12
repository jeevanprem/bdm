/* ==========================================================================
   BDM End-Term Masterclass Application Logic
   ========================================================================== */

(function () {
  'use strict';

  // Master Data Pointer
  const courseData = window.BDM_DATA || { questions: [], course: {} };
  const allQuestions = courseData.questions || [];
  const modulesInfo = (courseData.course && courseData.course.modules) || {};
  const conceptsData = window.BDM_CONCEPTS || {};

  // Application State
  const state = {
    currentView: 'syllabus',
    activeConceptWeek: 1,
    activeModuleFilter: 'all',
    activeSourceFilter: 'all',
    onlyCases: false,
    onlyBookmarked: false,
    onlyMistakes: false,
    searchQuery: '',
    userAnswers: JSON.parse(localStorage.getItem('bdm_user_answers') || '{}'),
    bookmarks: JSON.parse(localStorage.getItem('bdm_bookmarks') || '[]'),
    mockExam: {
      active: false,
      questions: [],
      currentIndex: 0,
      answers: {},
      markedForReview: new Set(),
      timeRemaining: 45 * 60, // 45 minutes
      timerInterval: null
    }
  };

  // DOM Elements Cache
  const views = {
    syllabus: document.getElementById('view-syllabus'),
    concepts: document.getElementById('view-concepts'),
    cases: document.getElementById('view-cases'),
    mnemonics: document.getElementById('view-mnemonics'),
    formulas: document.getElementById('view-formulas'),
    practice: document.getElementById('view-practice'),
    mock_exam: document.getElementById('view-mock-exam'),
    cram_sheet: document.getElementById('view-cram-sheet')
  };

  const navBtns = document.querySelectorAll('.nav-tab-btn');
  const questionsListEl = document.getElementById('practice-questions-list');
  const searchInputEl = document.getElementById('filter-search');
  const questionCountBadge = document.getElementById('practice-count-badge');
  const userScoreStat = document.getElementById('user-accuracy-stat');
  const userAttemptedStat = document.getElementById('user-attempted-stat');

  // Initialization
  function init() {
    setupNavigation();
    setupFilters();
    renderSyllabusView();
    renderConceptsView();
    renderMnemonicsView();
    renderCaseStudiesView();
    renderFormulaVault();
    renderPracticeQuestions();
    updateUserStats();
    startCountdown();
  }

  // Navigation Logic
  function setupNavigation() {
    navBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetView = btn.dataset.view;
        switchView(targetView);
      });
    });

    // Delegated jump links
    document.addEventListener('click', (e) => {
      const jumpBtn = e.target.closest('[data-jump-view]');
      if (jumpBtn) {
        const view = jumpBtn.dataset.jumpView;
        const filter = jumpBtn.dataset.jumpFilter;
        if (filter) {
          state.activeModuleFilter = filter;
          syncFilterButtons();
        }
        switchView(view);
      }
    });
  }

  function switchView(viewName) {
    if (!views[viewName]) return;
    state.currentView = viewName;

    navBtns.forEach(b => {
      b.classList.toggle('active', b.dataset.view === viewName);
    });

    Object.keys(views).forEach(key => {
      if (views[key]) {
        views[key].classList.toggle('active', key === viewName);
      }
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });

    if (viewName === 'practice') {
      renderPracticeQuestions();
    }
  }

  // Exam Countdown (Exam Tomorrow Morning 9:00 AM)
  function startCountdown() {
    const countdownEl = document.getElementById('countdown-timer');
    if (!countdownEl) return;

    function update() {
      // Simulate 14 hours countdown
      const targetTime = new Date().getTime() + (14 * 3600 * 1000);
      const now = new Date().getTime();
      const diff = Math.max(0, targetTime - now);

      const hours = Math.floor(diff / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((diff % (1000 * 60)) / 1000);

      countdownEl.textContent = `${String(hours).padStart(2, '0')}h ${String(minutes).padStart(2, '0')}m ${String(seconds).padStart(2, '0')}s`;
    }
    update();
    setInterval(update, 1000);
  }

  
  // ==========================================================================
  // CONCEPT BOOSTER & HINGLISH EXPLANATIONS MODULE
  // ==========================================================================
  function renderConceptsView() {
    const sidebarEl = document.getElementById('concept-week-sidebar');
    const showcaseEl = document.getElementById('concept-main-showcase');
    const jumpBtn = document.getElementById('concept-practice-jump-btn');
    if (!sidebarEl || !showcaseEl) return;

    const weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12];

    // Render Left Week Navigation Sidebar
    sidebarEl.innerHTML = weeks.map(w => {
      const c = conceptsData[w] || { title: `Week ${w}` };
      const qCount = allQuestions.filter(q => q.week === w).length;
      const isActive = w === state.activeConceptWeek;
      return `
        <button class="concept-week-btn ${isActive ? 'active' : ''}" onclick="window.selectConceptWeek(${w})">
          <div>
            <div style="font-weight: 700;">Week ${w}</div>
            <div style="font-size: 0.72rem; color: ${isActive ? '#e0e7ff' : 'var(--text-faint)'}; max-width: 140px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
              ${c.title}
            </div>
          </div>
          <span class="card-tag ${isActive ? 'tag-purple' : 'tag-blue'}" style="font-size: 0.68rem;">
            ${qCount} Qs
          </span>
        </button>
      `;
    }).join('');

    // Active Week Data
    const data = conceptsData[state.activeConceptWeek] || {
      week: state.activeConceptWeek,
      title: `Week ${state.activeConceptWeek}`,
      tagline: '',
      mnemonic: '',
      hinglish_summary: 'Concepts loading...',
      core_terms: [],
      formulas: [],
      key_exam_points: [],
      traps: ''
    };

    const weekQCount = allQuestions.filter(q => q.week === state.activeConceptWeek).length;

    if (jumpBtn) {
      jumpBtn.textContent = `🎯 Practice Week ${state.activeConceptWeek} Questions (${weekQCount}) →`;
      jumpBtn.onclick = () => window.jumpToPracticeWeek(state.activeConceptWeek);
    }

    showcaseEl.innerHTML = `
      <!-- Hero Card -->
      <div class="concept-hero-card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
          <div>
            <span class="hinglish-tag">🇮🇳 Hinglish Concept Master</span>
            <span class="card-tag tag-purple" style="margin-left: 8px;">Week ${data.week}</span>
          </div>
          <div style="font-family: var(--font-mono); font-size: 0.8rem; color: #a7f3d0; background: rgba(16, 185, 129, 0.15); padding: 4px 12px; border-radius: 4px; border: 1px solid rgba(16, 185, 129, 0.3);">
            ${data.mnemonic}
          </div>
        </div>

        <h2 style="font-size: 1.6rem; color: #fff; margin-bottom: 6px;">${data.title}</h2>
        <div style="font-size: 0.95rem; color: #38bdf8; font-weight: 600;">${data.tagline}</div>

        <!-- Hinglish Story & Intuition Box -->
        <div class="hinglish-story-box">
          <div style="font-size: 0.78rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
            🗣️ Hinglish me Samjho (Core Story & Intuition):
          </div>
          ${data.hinglish_summary}
        </div>
      </div>

      <!-- Core Terms Decoded (Kya matlab hai?) -->
      <div class="card">
        <div class="card-header">
          <h3 style="font-size: 1.15rem; color: #fff; display: flex; align-items: center; gap: 8px;">
            <span>📖</span> Technical Terms Decoded (Hinglish Understanding)
          </h3>
          <span class="card-tag tag-blue">${data.core_terms ? data.core_terms.length : 0} Essential Terms</span>
        </div>
        <div class="terms-grid">
          ${(data.core_terms || []).map(t => `
            <div class="term-card">
              <div>
                <div class="term-title">
                  <span>🔹</span> ${escapeHtml(t.term)}
                </div>
                <div class="term-hinglish-body">
                  ${escapeHtml(t.hinglish)}
                </div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>

      <!-- Problem Solving Formulas -->
      <div class="card">
        <div class="card-header">
          <h3 style="font-size: 1.15rem; color: #fff; display: flex; align-items: center; gap: 8px;">
            <span>📐</span> Problem-Solving Formulas (Numericals Kaise Solve Karein?)
          </h3>
          <span class="card-tag tag-green">Formula Sheet</span>
        </div>

        ${(data.formulas && data.formulas.length > 0) ? data.formulas.map(f => `
          <div style="margin-bottom: 16px; background: rgba(0,0,0,0.3); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 16px;">
            <div style="font-size: 1rem; font-weight: 700; color: #93c5fd; margin-bottom: 6px;">${escapeHtml(f.name)}</div>
            <div class="formula-display" style="text-align: left; font-size: 0.92rem; white-space: pre-line;">${escapeHtml(f.formula)}</div>
            <div class="formula-how-to-use">
              <strong>💡 Hinglish me Kaise Apply Karein:</strong><br>
              ${escapeHtml(f.how_to_use)}
            </div>
          </div>
        `).join('') : '<p style="color: var(--text-muted); font-size: 0.88rem;">Is module me theoretical / qualitative concepts zyada hain, formula-based calculations nahi hain.</p>'}
      </div>

      <!-- High-Yield Exam Points & Examiner Traps -->
      <div class="grid-2col">
        <div class="card" style="border-left: 4px solid var(--accent-emerald);">
          <div class="card-header">
            <h3 style="font-size: 1.05rem; color: var(--accent-emerald); display: flex; align-items: center; gap: 6px;">
              <span>💡</span> High-Yield Exam Points
            </h3>
            <span class="card-tag tag-green">Direct Exam Facts</span>
          </div>
          <ul style="padding-left: 18px; font-size: 0.88rem; color: #cbd5e1; line-height: 1.6;">
            ${(data.key_exam_points || []).map(pt => `<li style="margin-bottom: 8px;">${escapeHtml(pt)}</li>`).join('')}
          </ul>
        </div>

        <div class="card" style="border-left: 4px solid var(--accent-amber);">
          <div class="card-header">
            <h3 style="font-size: 1.05rem; color: var(--accent-amber); display: flex; align-items: center; gap: 6px;">
              <span>⚠️</span> Examiner ke Favorite Traps
            </h3>
            <span class="card-tag tag-amber">Danger Zone</span>
          </div>
          <p style="font-size: 0.88rem; color: #fde68a; line-height: 1.6;">
            ${escapeHtml(data.traps || '')}
          </p>
        </div>
      </div>

      <!-- Bottom Jump to Practice Banner -->
      <div class="concept-jump-practice-banner">
        <div>
          <h4 style="font-size: 1.15rem; color: #fff; margin-bottom: 4px;">Concept Samajh Aa Gaya? Ab Exam Questions Solve Karo!</h4>
          <p style="font-size: 0.85rem; color: #d1fae5; margin: 0;">
            All ${weekQCount} authentic graded assignment and quiz questions for Week ${data.week} with verified solutions and instant feedback.
          </p>
        </div>
        <button class="btn btn-primary" style="background: #fff; color: #065f46; font-weight: 700; padding: 10px 20px;" onclick="window.jumpToPracticeWeek(${data.week})">
          Practice Week ${data.week} Questions (${weekQCount}) →
        </button>
      </div>
    `;
  }

  // 1. SYLLABUS & MODULES MATRIX
  function renderSyllabusView() {
    const container = document.getElementById('syllabus-grid');
    if (!container) return;

    const weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12];
    container.innerHTML = weeks.map(w => {
      const info = modulesInfo[w] || { name: `Week ${w}`, desc: '', mnemonic: '', key_points: [] };
      const qCount = allQuestions.filter(q => q.week === w).length;
      return `
        <div class="card syllabus-module-card">
          <div class="card-header">
            <span class="card-tag tag-blue">Week ${w}</span>
            <span class="card-tag tag-purple">${qCount} Questions</span>
          </div>
          <h3 style="font-size: 1.15rem; margin-bottom: 8px;">${info.name}</h3>
          <p style="font-size: 0.85rem; color: var(--text-muted); min-height: 40px;">${info.desc}</p>
          
          <div style="margin: 12px 0; padding: 8px 12px; background: rgba(139, 92, 246, 0.1); border-left: 3px solid var(--accent-purple); border-radius: 4px;">
            <div style="font-size: 0.72rem; color: #c084fc; font-weight: 700; text-transform: uppercase;">Memory Trick</div>
            <div style="font-size: 0.84rem; font-weight: 600; color: #e0e7ff;">${info.mnemonic}</div>
          </div>

          <ul style="font-size: 0.82rem; color: #cbd5e1; padding-left: 18px; margin-bottom: 16px;">
            ${(info.key_points || []).slice(0, 3).map(pt => `<li style="margin-bottom: 4px;">${pt}</li>`).join('')}
          </ul>

          <div style="display: flex; gap: 8px; margin-top: auto;">
            <button class="btn btn-secondary btn-sm" style="flex: 1;" onclick="window.selectConceptWeek(${w}); window.switchViewDirect('concepts');">
              📖 Learn Concept
            </button>
            <button class="btn btn-primary btn-sm" style="flex: 1;" data-jump-view="practice" data-jump-filter="week_${w}">
              🎯 Practice (${qCount})
            </button>
          </div>
        </div>
      `;
    }).join('');
  }

  // 2. MNEMONICS & MEMORY PALACE
  function renderMnemonicsView() {
    const container = document.getElementById('mnemonics-grid');
    if (!container) return;

    const mnemonicsList = [
      {
        code: 'S - O - U - P',
        title: 'Core Economics Foundations',
        week: 'Week 1',
        context: 'Use this whenever an exam question asks about the fundamental economic problem or why choices must be made.',
        items: [
          { letter: 'S', label: 'Scarcity', desc: 'Resources are strictly limited (money, time, capacity, inputs).' },
          { letter: 'O', label: 'Opportunity Cost', desc: 'Value of the next best alternative forgone (NOT the sum of all alternatives).' },
          { letter: 'U', label: 'Unlimited Wants', desc: 'Human desires are insatiable; you can never fulfill everything.' },
          { letter: 'P', label: 'Prioritization (Marginal Rule)', desc: 'Choose where Marginal Benefit (MB) >= Marginal Cost (MC).' }
        ]
      },
      {
        code: 'B - I - O - S',
        title: 'Production Possibility Frontier (PPF)',
        week: 'Week 2',
        context: 'Visual curve of trade-offs between two outputs under fixed resources and technology.',
        items: [
          { letter: 'B', label: 'Bowed-out Shape', desc: 'Concave to origin due to the Law of Increasing Opportunity Cost (resources are specialized).' },
          { letter: 'I', label: 'Inside Points', desc: 'Feasible but Inefficient (underutilized capital or unemployment of labor).' },
          { letter: 'O', label: 'On Curve Points', desc: 'Optimal / Productively Efficient (cannot produce more of X without giving up Y).' },
          { letter: 'S', label: 'Shift Outward', desc: 'Economic growth caused by technological advancement or resource expansion.' }
        ]
      },
      {
        code: 'S - E - C',
        title: 'Goods Evaluation Spectrum',
        week: 'Week 3',
        context: 'How consumers assess quality relative to purchase time.',
        items: [
          { letter: 'S', label: 'Search Goods', desc: 'Evaluated BEFORE purchase (specs, RAM, clothing size, books).' },
          { letter: 'E', label: 'Experience Goods', desc: 'Evaluated AFTER/DURING consumption (restaurants, movie tickets, vacations).' },
          { letter: 'C', label: 'Credence Goods', desc: 'Difficult to evaluate even AFTER consumption (medical surgery, legal counsel, brake repair).' }
        ]
      },
      {
        code: 'P - E - R - K',
        title: 'Price Elasticity of Demand (Ep) & Total Revenue',
        week: 'Week 4',
        context: 'Predicting how revenue changes when a firm raises or lowers prices.',
        items: [
          { letter: 'P', label: 'Price Change', desc: 'Does the firm increase or decrease price?' },
          { letter: 'E', label: 'Elastic (|Ep| > 1)', desc: 'Price & Total Revenue move in OPPOSITE directions! (Cut price -> TR rises).' },
          { letter: 'R', label: 'Rigid / Inelastic (|Ep| < 1)', desc: 'Price & Total Revenue move in the SAME direction! (Raise price -> TR rises).' },
          { letter: 'K', label: 'Key Maximum (|Ep| = 1)', desc: 'Unitary elasticity is where Total Revenue is mathematically MAXIMIZED.' }
        ]
      },
      {
        code: 'A - L - O - E',
        title: 'The Fundamental Accounting Equation',
        week: 'Weeks 5 & 6',
        context: 'The foundation of the Balance Sheet. Must balance after every single transaction.',
        items: [
          { letter: 'A', label: 'Assets', desc: 'Economic resources owned (Cash, Debtors, Inventory, Equipment).' },
          { letter: 'L', label: 'Liabilities', desc: 'Obligations owed to external creditors (Payables, Bank Loans, Bonds).' },
          { letter: 'O-E', label: 'Owner\'s Equity', desc: 'Residual claim = Capital Contributed + Retained Earnings - Drawings.' }
        ]
      },
      {
        code: 'D-E-A-L  vs  C-L-I-P',
        title: 'Golden Rules of Debit & Credit',
        week: 'Week 6',
        context: 'Never get confused on what increases with Debit or Credit.',
        items: [
          { letter: 'DEAL', label: 'Debit Increases:', desc: 'Drawings, Expenses, Assets (When these go up -> DEBIT).' },
          { letter: 'CLIP', label: 'Credit Increases:', desc: 'Liabilities, Income/Revenue, Capital/Equity (When these go up -> CREDIT).' }
        ]
      },
      {
        code: 'O - I - F',
        title: 'Cash Flow Statement Classification',
        week: 'Week 7',
        context: 'Classification of cash inflows and outflows.',
        items: [
          { letter: 'O', label: 'Operating Activities', desc: 'Core daily business: Cash from customers, payments to vendors, salaries, taxes.' },
          { letter: 'I', label: 'Investing Activities', desc: 'Buying/selling long-term assets (Buying factory for cash = Outflow).' },
          { letter: 'F', label: 'Financing Activities', desc: 'Capital structure: Issuing shares, borrowing debt, repaying principal, dividends.' }
        ]
      },
      {
        code: 'DuPont Pyramid',
        title: '3-Step ROE Decomposition',
        week: 'Week 8',
        context: 'Deconstructing Return on Equity into Profitability, Operating Efficiency, and Leverage.',
        items: [
          { letter: '1', label: 'Net Profit Margin', desc: 'PAT / Revenue (How much profit per rupee of sales) - XYZ Ltd = 8.44%.' },
          { letter: '2', label: 'Asset Turnover', desc: 'Revenue / Total Assets (How efficiently assets generate sales) - XYZ Ltd = 1.33x.' },
          { letter: '3', label: 'Equity Multiplier', desc: 'Total Assets / Total Equity (Financial Leverage) - XYZ Ltd = 2.40x. ROE = 27.0%!' }
        ]
      },
      {
        code: 'C - R - P - I',
        title: 'Responsibility Centers Escalator',
        week: 'Week 9',
        context: 'Hierarchy of managerial accountability in decentralized organizations.',
        items: [
          { letter: 'C', label: 'Cost Center', desc: 'Manager is accountable ONLY for costs (Maintenance, IT support, Assembly).' },
          { letter: 'R', label: 'Revenue Center', desc: 'Manager is accountable ONLY for generating sales (Regional sales office).' },
          { letter: 'P', label: 'Profit Center', desc: 'Accountable for BOTH Revenues and Costs (e.g. Individual retail branch).' },
          { letter: 'I', label: 'Investment Center', desc: 'Accountable for Revenue, Costs, AND Capital Invested (evaluated on ROI / EVA).' }
        ]
      },
      {
        code: 'P-P-A-P-H-C-F',
        title: 'The 7 Steps of Personal Selling',
        week: 'Week 11',
        context: 'The exact chronological sequence of B2B sales cycles.',
        items: [
          { letter: 'P', label: 'Prospecting', desc: 'Finding leads & qualifying via M-A-N (Money, Authority, Need).' },
          { letter: 'P', label: 'Pre-approach', desc: 'Researching the prospect background before meeting.' },
          { letter: 'A', label: 'Approach', desc: 'First contact, rapport building, PSP technique.' },
          { letter: 'P', label: 'Presentation', desc: 'FAB pitch (Features, Advantages, Benefits).' },
          { letter: 'H', label: 'Handling Objections', desc: 'Reframing doubts into buying triggers.' },
          { letter: 'C', label: 'Closing the Sale', desc: 'Asking for the order (Assumptive / Urgency close).' },
          { letter: 'F', label: 'Follow-Up', desc: 'Ensuring delivery, satisfaction, and repeat orders.' }
        ]
      },
      {
        code: 'I - H - I - P',
        title: '4 Unique Characteristics of Services',
        week: 'Week 12',
        context: 'How services differ fundamentally from manufactured goods.',
        items: [
          { letter: 'I', label: 'Intangibility', desc: 'Cannot be touched, tasted, or seen prior to consumption.' },
          { letter: 'H', label: 'Heterogeneity (Variability)', desc: 'Service quality varies depending on who delivers it, when, and where.' },
          { letter: 'I', label: 'Inseparability', desc: 'Production and consumption occur simultaneously.' },
          { letter: 'P', label: 'Perishability', desc: 'Unused capacity cannot be stored in inventory (empty flight seats).' }
        ]
      },
      {
        code: 'R - A - T - E - R',
        title: 'SERVQUAL 5 Dimensions of Service Quality',
        week: 'Week 12',
        context: 'The 5 dimensions evaluated by customers when measuring service quality gaps.',
        items: [
          { letter: 'R', label: 'Reliability', desc: 'Delivering the promised service dependably and accurately.' },
          { letter: 'A', label: 'Assurance', desc: 'Employee knowledge, courtesy, and ability to inspire trust.' },
          { letter: 'T', label: 'Tangibles', desc: 'Physical facilities, equipment, decor, and staff appearance.' },
          { letter: 'E', label: 'Empathy', desc: 'Caring, personalized individual attention given to customer.' },
          { letter: 'R', label: 'Responsiveness', desc: 'Willingness to help promptly and handle requests quickly.' }
        ]
      }
    ];

    container.innerHTML = mnemonicsList.map(m => `
      <div class="mnemonic-card">
        <div class="card-header">
          <span class="card-tag tag-purple">${m.week}</span>
          <span style="font-size: 0.75rem; color: var(--accent-cyan); font-weight: 700;">Visual Trick</span>
        </div>
        <div class="mnemonic-code">${m.code}</div>
        <div style="font-size: 0.95rem; font-weight: 700; color: #fff; margin-bottom: 4px;">${m.title}</div>
        
        <ul class="mnemonic-expansion">
          ${m.items.map(it => `
            <li>
              <span class="mnemonic-letter">${it.letter}</span>
              <span><strong>${it.label}:</strong> <span style="color: #94a3b8;">${it.desc}</span></span>
            </li>
          `).join('')}
        </ul>

        <div class="mnemonic-context">
          <strong>Exam Trigger:</strong> ${m.context}
        </div>
      </div>
    `).join('');
  }

  // 3. CASE STUDIES MASTERCLASS
  function renderCaseStudiesView() {
    const container = document.getElementById('cases-list');
    if (!container) return;

    const cases = [
      {
        id: 'case-xyz',
        title: 'Case 1: XYZ Limited Commercial Vehicles (The Mega Financial Statement Case)',
        source: 'Graded Assignment Week 8 (12 Comprehensive Questions)',
        overview: `Company: XYZ Limited (Commercial Vehicle Manufacturer)
Financials (in ₹ Crores):
• Revenue from Operations: ₹40,000 Cr
• Cost of Materials Consumed: ₹28,000 Cr
• Employee Benefits: ₹2,500 Cr | Other Expenses: ₹4,000 Cr
• Depreciation: ₹800 Cr | Finance Costs (Interest): ₹200 Cr
• Profit Before Tax (PBT): ₹4,500 Cr | Tax: ₹1,125 Cr | Net Profit (PAT): ₹3,375 Cr

Balance Sheet:
• Share Capital (Face value ₹1): ₹500 Cr (500 Cr shares)
• Reserves & Surplus: ₹12,000 Cr => Total Equity = ₹12,500 Cr
• Total Debt: ₹2,500 Cr | Other Liabilities: ₹15,000 Cr
• Fixed Assets: ₹6,000 Cr | Inventory: ₹3,500 Cr | Debtors: ₹4,000 Cr | Cash & Others: ₹16,500 Cr
• Total Assets: ₹30,000 Cr | Market Price per share: ₹150 | Dividend per share: ₹2`,
        metrics: [
          { name: 'Net Profit Margin', formula: '(PAT / Revenue) × 100', calc: '(3,375 / 40,000) × 100', result: '8.44%' },
          { name: 'Operating Margin', formula: '(EBIT / Revenue) × 100', calc: '(4,500 / 40,000) × 100', result: '11.25%' },
          { name: 'Current Ratio', formula: 'Current Assets / Current Liabilities', calc: '24,000 / 15,000', result: '1.60' },
          { name: 'Quick Ratio', formula: '(Current Assets - Inventory) / CL', calc: '(24,000 - 3,500) / 15,000', result: '1.37' },
          { name: 'Debt-to-Equity Ratio', formula: 'Total Debt / Shareholders Equity', calc: '2,500 / 12,500', result: '0.20' },
          { name: 'Return on Equity (ROE)', formula: '(PAT / Total Equity) × 100', calc: '(3,375 / 12,500) × 100', result: '27.0%' },
          { name: 'Earnings Per Share (EPS)', formula: 'PAT / Outstanding Shares', calc: '₹3,375 Cr / 500 Cr shares', result: '₹6.75' },
          { name: 'Price-to-Earnings (P/E)', formula: 'Market Price / EPS', calc: '150 / 6.75', result: '22.22' },
          { name: 'Dividend Yield', formula: '(DPS / Market Price) × 100', calc: '(2 / 150) × 100', result: '1.33%' },
          { name: 'Market Capitalization', formula: 'Shares × Market Price', calc: '500 Cr × ₹150', result: '₹75,000 Cr' },
          { name: 'Inventory Turnover', formula: 'COGS (Materials) / Inventory', calc: '28,000 / 3,500', result: '8.00 times' },
          { name: 'Total Operating Expenses', formula: 'Total Expenses - Depreciation - Interest', calc: '35,500 - 800 - 200', result: '₹34,500 Cr' }
        ],
        trap: 'Common Exam Trap: Confusing Operating Margin with Net Profit Margin, or using Face Value (₹1) instead of Market Price (₹150) when computing P/E and Dividend Yield!'
      },
      {
        id: 'case-mumbai',
        title: 'Case 2: Sunk Cost vs Opportunity Cost (Mumbai Flight vs IPL Pavilion Tickets)',
        source: 'Graded Assignment Week 2 (Question 1)',
        overview: `Scenario:
You bought a non-refundable plane ticket to Mumbai for ₹5,500. You estimate this trip provides ₹10,000 worth of enjoyment/value.
Your friend calls: He won 2 free pavilion tickets to the IPL final (cost ₹8,000 each) and invites you to join him.
Question: What is the effective value one must gain from the IPL final to justify missing the scheduled flight to Mumbai?`,
        metrics: [
          { name: 'Sunk Cost', formula: 'Past non-refundable expense', calc: '₹5,500 plane ticket', result: 'IRRELEVANT' },
          { name: 'Alternative Value Lost', formula: 'Value of forgone Mumbai trip', calc: 'Estimated enjoyment', result: '₹10,000' },
          { name: 'Justification Rule', formula: 'IPL Enjoyment >= Next Best Forgone', calc: 'IPL Benefit >= ₹10,000', result: '₹10,000' }
        ],
        trap: 'Common Exam Trap: Students mistakenly add or subtract the ₹5,500 ticket cost! The ₹5,500 is already spent and non-refundable (Sunk Cost). Economic decision-making looks ONLY at the future benefit forgone (₹10,000)!'
      },
      {
        id: 'case-data001',
        title: 'Case 3: Startup Resource Allocation (Data001 Tech Bandwidth)',
        source: 'Graded Assignment Week 2 (Questions 9 & 10)',
        overview: `Scenario:
Data001 has limited team bandwidth and can commit to only ONE option over 6 months:
• Option A (External Client): Immediate revenue ₹5.0 Lakh. But delays internal software upgrade and incurs vendor extension penalty of ₹1.5 Lakh.
• Option B (Internal Upgrade): Saves ₹10,000/month operational costs immediately. But forfeits ₹5.0L external revenue.
Question: If Data001 chooses Option A, what is the Opportunity Cost of this decision over 6 months?`,
        metrics: [
          { name: 'Internal Savings Forgone', formula: 'Monthly Savings × 6 months', calc: '₹10,000 × 6', result: '₹60,000 (₹60K)' },
          { name: 'Penalty Status', formula: 'Vendor penalty', calc: 'Out-of-pocket explicit cost', result: 'Not Opp Cost of internal benefit' }
        ],
        trap: 'Common Exam Trap: Picking ₹1.5 Lakh (the vendor penalty) or ₹2.10 Lakh. Opportunity cost is strictly the value of the forgone internal operational savings: ₹10K/mo × 6 = ₹60K!'
      },
      {
        id: 'case-rgoura',
        title: 'Case 4: R-Goura\'s Student Canteen Market Equilibrium & Price Ceiling',
        source: 'Quiz 1 (Actual TCS iON Paper, Questions 19, 20, 21)',
        overview: `Scenario:
A university campus operates R-Goura's student mess.
• Demand: High demand for nutritious subsidized meal subscriptions.
• Equilibrium Price (P*) & Quantity (Q*) where Demand curve intersects Supply curve.
• The student administration imposes an artificial price cap (price ceiling) below market equilibrium to make food affordable.
• Consequences: Quantity demanded increases while quantity supplied decreases, creating an immediate persistent SHORTAGE.`,
        metrics: [
          { name: 'Price Ceiling Effect', formula: 'Price Cap < Equilibrium Price', calc: 'Qd > Qs at low price', result: 'Shortage & Queues' },
          { name: 'Welfare Impact', formula: 'Loss in total economic surplus', calc: 'Unrealized mutual trades', result: 'Deadweight Loss (DWL)' }
        ],
        trap: 'Common Exam Trap: Forgetting that a price ceiling below equilibrium always creates a shortage, whereas a price floor above equilibrium creates a surplus!'
      },
      {
        id: 'case-real-estate',
        title: 'Case 5: Asset Classification & Intent (Real Estate vs Manufacturer)',
        source: 'Graded Assignment Week 5 (Question 2)',
        overview: `Scenario:
How are buildings categorized in a real estate firm that intends to sell them to customers, as opposed to a manufacturing firm that uses them as factories?
Core Principle: "Intent of Ownership Determines Accounting Treatment".`,
        metrics: [
          { name: 'Real Estate Developer', formula: 'Held for sale in ordinary course', calc: 'Sold to buyers', result: 'INVENTORY (Current Asset)' },
          { name: 'Manufacturing Firm', formula: 'Held for operational production > 1 yr', calc: 'Factory use', result: 'FIXED ASSET (PP&E)' }
        ],
        trap: 'Common Exam Trap: Assuming all physical buildings are automatically Fixed Assets! For a builder, buildings are trading stock (inventory)!'
      }
    ];

    container.innerHTML = cases.map(cs => `
      <div class="case-card highlight" id="${cs.id}">
        <div class="case-header-row">
          <div>
            <span class="case-badge">High-Yield Case Study</span>
            <h3 style="font-size: 1.25rem; margin-top: 6px; color: #fff;">${cs.title}</h3>
            <div style="font-size: 0.8rem; color: #38bdf8; margin-top: 2px;">${cs.source}</div>
          </div>
        </div>

        <div class="case-body">${cs.overview}</div>

        <div style="margin: 16px 0;">
          <h4 style="font-size: 0.95rem; color: #93c5fd; margin-bottom: 8px;">Key Metric Calculations & Steps:</h4>
          <table class="cram-table">
            <thead>
              <tr>
                <th>Metric / Concept</th>
                <th>Standard Formula</th>
                <th>Case Working</th>
                <th>Exact Value</th>
              </tr>
            </thead>
            <tbody>
              ${cs.metrics.map(m => `
                <tr>
                  <td><strong>${m.name}</strong></td>
                  <td style="font-family: var(--font-mono); font-size: 0.82rem;">${m.formula}</td>
                  <td style="font-family: var(--font-mono); font-size: 0.82rem; color: #94a3b8;">${m.calc}</td>
                  <td style="font-weight: 700; color: var(--accent-emerald); font-family: var(--font-mono);">${m.result}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>

        <div class="exam-trap-box">
          <strong>⚠️ Exam Pitfall & Trap:</strong> ${cs.trap}
        </div>
      </div>
    `).join('');
  }

  // 4. FORMULA VAULT & LIVE CALCULATORS
  function renderFormulaVault() {
    const container = document.getElementById('formulas-grid');
    if (!container) return;

    container.innerHTML = `
      <!-- Calculator 1: DuPont ROE -->
      <div class="formula-card">
        <div>
          <span class="card-tag tag-purple">Week 8 • Valuation</span>
          <h3 style="font-size: 1.1rem; margin: 8px 0 4px;">DuPont 3-Step ROE Calculator</h3>
          <p style="font-size: 0.8rem; color: var(--text-muted);">ROE = Net Margin × Asset Turnover × Equity Multiplier</p>
          <div class="formula-display">ROE = (PAT / Rev) × (Rev / Assets) × (Assets / Equity)</div>
          
          <div class="calc-inputs">
            <div class="calc-input-group">
              <label>PAT (₹ Cr)</label>
              <input type="number" id="calc-dupont-pat" value="3375">
            </div>
            <div class="calc-input-group">
              <label>Revenue (₹ Cr)</label>
              <input type="number" id="calc-dupont-rev" value="40000">
            </div>
            <div class="calc-input-group">
              <label>Total Assets (₹ Cr)</label>
              <input type="number" id="calc-dupont-assets" value="30000">
            </div>
            <div class="calc-input-group">
              <label>Shareholders Equity (₹ Cr)</label>
              <input type="number" id="calc-dupont-equity" value="12500">
            </div>
          </div>
        </div>
        <div class="calc-result-box">
          <span>Calculated ROE:</span>
          <span class="calc-result-val" id="calc-dupont-res">27.00%</span>
        </div>
      </div>

      <!-- Calculator 2: Liquidity Ratios -->
      <div class="formula-card">
        <div>
          <span class="card-tag tag-blue">Week 7 & 8 • Liquidity</span>
          <h3 style="font-size: 1.1rem; margin: 8px 0 4px;">Current & Quick (Acid-Test) Ratio</h3>
          <p style="font-size: 0.8rem; color: var(--text-muted);">Current Ratio = CA / CL | Quick Ratio = (CA - Inventory) / CL</p>
          <div class="formula-display">CR = CA / CL &nbsp;|&nbsp; QR = (CA - Inv - Prepaid) / CL</div>
          
          <div class="calc-inputs">
            <div class="calc-input-group">
              <label>Current Assets (CA)</label>
              <input type="number" id="calc-liq-ca" value="24000">
            </div>
            <div class="calc-input-group">
              <label>Current Liabilities (CL)</label>
              <input type="number" id="calc-liq-cl" value="15000">
            </div>
            <div class="calc-input-group" style="grid-column: span 2;">
              <label>Inventory & Prepaids</label>
              <input type="number" id="calc-liq-inv" value="3500">
            </div>
          </div>
        </div>
        <div class="calc-result-box">
          <span>CR: <strong id="calc-liq-cr-res" style="color: #38bdf8;">1.60</strong></span>
          <span>Quick Ratio: <strong class="calc-result-val" id="calc-liq-qr-res">1.37</strong></span>
        </div>
      </div>

      <!-- Calculator 3: Price Elasticity of Demand -->
      <div class="formula-card">
        <div>
          <span class="card-tag tag-green">Week 4 • Microeconomics</span>
          <h3 style="font-size: 1.1rem; margin: 8px 0 4px;">Price Elasticity of Demand (Ep)</h3>
          <p style="font-size: 0.8rem; color: var(--text-muted);">Ep = % Change in Quantity Demanded / % Change in Price</p>
          <div class="formula-display">Ep = (%ΔQd) / (%ΔP)</div>
          
          <div class="calc-inputs">
            <div class="calc-input-group">
              <label>% Δ in Quantity Demanded</label>
              <input type="number" id="calc-ep-qd" value="-20">
            </div>
            <div class="calc-input-group">
              <label>% Δ in Price</label>
              <input type="number" id="calc-ep-p" value="10">
            </div>
          </div>
        </div>
        <div class="calc-result-box">
          <span id="calc-ep-label">Elasticity: <strong>-2.00</strong></span>
          <span class="calc-result-val" id="calc-ep-res">Elastic (|Ep| > 1)</span>
        </div>
      </div>

      <!-- Calculator 4: Valuation & Market Ratios -->
      <div class="formula-card">
        <div>
          <span class="card-tag tag-amber">Week 8 • Valuation</span>
          <h3 style="font-size: 1.1rem; margin: 8px 0 4px;">EPS, P/E Ratio & Dividend Yield</h3>
          <p style="font-size: 0.8rem; color: var(--text-muted);">EPS = PAT / Shares | P/E = Price / EPS | Div Yield = DPS / Price</p>
          <div class="formula-display">P/E = Market Price / EPS &nbsp;|&nbsp; Div Yield = (DPS / P) × 100</div>
          
          <div class="calc-inputs">
            <div class="calc-input-group">
              <label>Net Profit PAT (Cr)</label>
              <input type="number" id="calc-val-pat" value="3375">
            </div>
            <div class="calc-input-group">
              <label>Outstanding Shares (Cr)</label>
              <input type="number" id="calc-val-shares" value="500">
            </div>
            <div class="calc-input-group">
              <label>Market Price (₹)</label>
              <input type="number" id="calc-val-price" value="150">
            </div>
            <div class="calc-input-group">
              <label>Dividend per Share (₹)</label>
              <input type="number" id="calc-val-dps" value="2">
            </div>
          </div>
        </div>
        <div class="calc-result-box">
          <span>EPS: <strong id="calc-val-eps-res" style="color: #38bdf8;">₹6.75</strong></span>
          <span>P/E: <strong id="calc-val-pe-res" style="color: #c084fc;">22.22</strong></span>
          <span>Yield: <strong class="calc-result-val" id="calc-val-yield-res">1.33%</strong></span>
        </div>
      </div>
    `;

    // Bind Live Calculator Event Listeners
    setupCalculatorsLogic();
  }

  function setupCalculatorsLogic() {
    // 1. DuPont
    function updateDuPont() {
      const pat = parseFloat(document.getElementById('calc-dupont-pat')?.value) || 0;
      const rev = parseFloat(document.getElementById('calc-dupont-rev')?.value) || 1;
      const assets = parseFloat(document.getElementById('calc-dupont-assets')?.value) || 1;
      const equity = parseFloat(document.getElementById('calc-dupont-equity')?.value) || 1;

      const margin = pat / rev;
      const turnover = rev / assets;
      const leverage = assets / equity;
      const roe = (margin * turnover * leverage) * 100;

      const resEl = document.getElementById('calc-dupont-res');
      if (resEl) resEl.textContent = roe.toFixed(2) + '%';
    }
    ['calc-dupont-pat', 'calc-dupont-rev', 'calc-dupont-assets', 'calc-dupont-equity'].forEach(id => {
      document.getElementById(id)?.addEventListener('input', updateDuPont);
    });

    // 2. Liquidity
    function updateLiquidity() {
      const ca = parseFloat(document.getElementById('calc-liq-ca')?.value) || 0;
      const cl = parseFloat(document.getElementById('calc-liq-cl')?.value) || 1;
      const inv = parseFloat(document.getElementById('calc-liq-inv')?.value) || 0;

      const cr = ca / cl;
      const qr = (ca - inv) / cl;

      const crEl = document.getElementById('calc-liq-cr-res');
      const qrEl = document.getElementById('calc-liq-qr-res');
      if (crEl) crEl.textContent = cr.toFixed(2);
      if (qrEl) qrEl.textContent = qr.toFixed(2);
    }
    ['calc-liq-ca', 'calc-liq-cl', 'calc-liq-inv'].forEach(id => {
      document.getElementById(id)?.addEventListener('input', updateLiquidity);
    });

    // 3. Elasticity
    function updateElasticity() {
      const qd = parseFloat(document.getElementById('calc-ep-qd')?.value) || 0;
      const p = parseFloat(document.getElementById('calc-ep-p')?.value) || 1;
      const ep = qd / p;
      const absEp = Math.abs(ep);

      const labelEl = document.getElementById('calc-ep-label');
      const resEl = document.getElementById('calc-ep-res');
      if (labelEl) labelEl.innerHTML = `Elasticity: <strong>${ep.toFixed(2)}</strong>`;
      if (resEl) {
        if (absEp > 1) {
          resEl.textContent = 'Elastic (|Ep| > 1)';
          resEl.style.color = 'var(--accent-emerald)';
        } else if (absEp < 1) {
          resEl.textContent = 'Inelastic (|Ep| < 1)';
          resEl.style.color = 'var(--accent-amber)';
        } else {
          resEl.textContent = 'Unitary (|Ep| = 1)';
          resEl.style.color = 'var(--accent-cyan)';
        }
      }
    }
    ['calc-ep-qd', 'calc-ep-p'].forEach(id => {
      document.getElementById(id)?.addEventListener('input', updateElasticity);
    });

    // 4. Valuation
    function updateValuation() {
      const pat = parseFloat(document.getElementById('calc-val-pat')?.value) || 0;
      const shares = parseFloat(document.getElementById('calc-val-shares')?.value) || 1;
      const price = parseFloat(document.getElementById('calc-val-price')?.value) || 1;
      const dps = parseFloat(document.getElementById('calc-val-dps')?.value) || 0;

      const eps = pat / shares;
      const pe = eps > 0 ? (price / eps) : 0;
      const yieldPct = (dps / price) * 100;

      const epsEl = document.getElementById('calc-val-eps-res');
      const peEl = document.getElementById('calc-val-pe-res');
      const yieldEl = document.getElementById('calc-val-yield-res');
      if (epsEl) epsEl.textContent = '₹' + eps.toFixed(2);
      if (peEl) peEl.textContent = pe.toFixed(2);
      if (yieldEl) yieldEl.textContent = yieldPct.toFixed(2) + '%';
    }
    ['calc-val-pat', 'calc-val-shares', 'calc-val-price', 'calc-val-dps'].forEach(id => {
      document.getElementById(id)?.addEventListener('input', updateValuation);
    });
  }

  // 5. PRACTICE QUESTION BANK & FILTERS
  function setupFilters() {
    if (searchInputEl) {
      searchInputEl.addEventListener('input', (e) => {
        state.searchQuery = e.target.value.toLowerCase().trim();
        renderPracticeQuestions();
      });
    }

    // Filter chips
    document.querySelectorAll('.filter-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const filterType = chip.dataset.filterType;
        const val = chip.dataset.filterVal;

        if (filterType === 'module') {
          state.activeModuleFilter = val;
        } else if (filterType === 'source') {
          state.activeSourceFilter = val;
        } else if (filterType === 'cases') {
          state.onlyCases = !state.onlyCases;
          chip.classList.toggle('active', state.onlyCases);
          renderPracticeQuestions();
          return;
        } else if (filterType === 'bookmarks') {
          state.onlyBookmarked = !state.onlyBookmarked;
          chip.classList.toggle('active', state.onlyBookmarked);
          renderPracticeQuestions();
          return;
        } else if (filterType === 'mistakes') {
          state.onlyMistakes = !state.onlyMistakes;
          chip.classList.toggle('active', state.onlyMistakes);
          renderPracticeQuestions();
          return;
        }

        syncFilterButtons();
        renderPracticeQuestions();
      });
    });
  }

  function syncFilterButtons() {
    document.querySelectorAll('.filter-chip[data-filter-type="module"]').forEach(c => {
      c.classList.toggle('active', c.dataset.filterVal === state.activeModuleFilter);
    });
    document.querySelectorAll('.filter-chip[data-filter-type="source"]').forEach(c => {
      c.classList.toggle('active', c.dataset.filterVal === state.activeSourceFilter);
    });
  }

  function getFilteredQuestions() {
    return allQuestions.filter(q => {
      // Module filter
      if (state.activeModuleFilter !== 'all') {
        if (state.activeModuleFilter.startsWith('week_')) {
          const w = parseInt(state.activeModuleFilter.replace('week_', ''), 10);
          if (q.week !== w) return false;
        }
      }

      // Source filter
      if (state.activeSourceFilter !== 'all') {
        if (state.activeSourceFilter === 'quiz1' && !q.source.includes('Quiz 1')) return false;
        if (state.activeSourceFilter === 'quiz2' && !q.source.includes('Quiz 2')) return false;
        if (state.activeSourceFilter === 'ga' && !q.source.startsWith('GA')) return false;
      }

      // Case studies only
      if (state.onlyCases && !q.is_case_based) {
        return false;
      }

      // Bookmarked only
      if (state.onlyBookmarked && !state.bookmarks.includes(q.id)) {
        return false;
      }

      // Mistakes only
      if (state.onlyMistakes) {
        const ans = state.userAnswers[q.id];
        if (!ans || ans.isCorrect) return false;
      }

      // Text search
      if (state.searchQuery) {
        const combined = (q.question + ' ' + (q.options || []).map(o => o.text).join(' ') + ' ' + (q.feedback || '')).toLowerCase();
        if (!combined.includes(state.searchQuery)) return false;
      }

      return true;
    });
  }

  function renderPracticeQuestions() {
    if (!questionsListEl) return;
    const filtered = getFilteredQuestions();

    if (questionCountBadge) {
      questionCountBadge.textContent = `${filtered.length} of ${allQuestions.length} Questions`;
    }

    // Update quick concept banner in practice view
    const bannerTextEl = document.getElementById('practice-banner-text');
    const bannerBtnEl = document.getElementById('practice-banner-btn');
    if (bannerTextEl && bannerBtnEl) {
      if (state.activeModuleFilter.startsWith('week_')) {
        const w = state.activeModuleFilter.replace('week_', '');
        const c = conceptsData[w];
        const title = c ? c.title : `Week ${w}`;
        bannerTextEl.innerHTML = `Currently viewing <strong>Week ${w}: ${title}</strong>. Pehle concept & formulas samjho!`;
        bannerBtnEl.textContent = `📖 Open Week ${w} Concepts & Hinglish Guide →`;
      } else {
        bannerTextEl.textContent = `Stuck on any question? Open the full Hinglish concept guide for all 12 weeks.`;
        bannerBtnEl.textContent = `📖 Browse All Concepts & Hinglish Guide →`;
      }
    }


    if (filtered.length === 0) {
      questionsListEl.innerHTML = `
        <div class="card" style="text-align: center; padding: 40px 20px;">
          <h3 style="color: var(--text-muted);">No questions match your current filters</h3>
          <p style="font-size: 0.85rem; color: var(--text-faint); margin-top: 6px;">Try resetting search keywords or turning off specific filter chips.</p>
          <button class="btn btn-secondary btn-sm" style="margin-top: 12px;" onclick="window.resetPracticeFilters()">
            Reset All Filters
          </button>
        </div>
      `;
      return;
    }

    // Render questions (limit initial DOM render to 50 for speed, with load more if needed)
    const displayList = filtered.slice(0, 60);

    questionsListEl.innerHTML = displayList.map(q => {
      const isBookmarked = state.bookmarks.includes(q.id);
      const userAns = state.userAnswers[q.id];
      const hasAnswered = !!userAns;

      return `
        <div class="question-item-card" id="qcard-${q.id}">
          <div class="question-meta-bar">
            <div class="q-badge-group">
              <span class="q-source-tag">${q.source} • Q${q.q_num}</span>
              <span class="q-topic-tag">${q.module}</span>
              ${q.is_case_based ? '<span class="card-tag tag-amber">Case-Based</span>' : ''}
            </div>
            <button class="q-bookmark-btn ${isBookmarked ? 'bookmarked' : ''}" 
                    title="${isBookmarked ? 'Remove Bookmark' : 'Bookmark Question'}" 
                    onclick="window.toggleBookmark('${q.id}')">
              ${isBookmarked ? '★' : '☆'}
            </button>
          </div>

          <div class="question-text">${escapeHtml(q.question)}</div>

          <div class="options-container">
            ${(q.options || []).map((opt, idx) => {
              let optClass = 'option-choice-btn';
              if (hasAnswered) {
                optClass += ' disabled';
                if (opt.label === userAns.chosenLabel) {
                  optClass += userAns.isCorrect ? ' selected-correct' : ' selected-wrong';
                }
                if (opt.is_correct && !userAns.isCorrect) {
                  optClass += ' show-as-correct';
                }
              }
              return `
                <button class="${optClass}" 
                        onclick="window.selectOption('${q.id}', '${opt.label}', ${opt.is_correct})">
                  <span class="option-label">${opt.label}</span>
                  <span>${escapeHtml(opt.text)}</span>
                </button>
              `;
            }).join('')}
          </div>

          <div class="solution-drawer ${hasAnswered ? 'open' : ''}" id="sol-${q.id}">
            <div class="solution-badge" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-subtle); padding-bottom: 8px; margin-bottom: 10px;">
              <span style="color: var(--accent-emerald); font-weight: 700; font-size: 0.88rem;">
                🎯 AI Solution: <strong>${escapeHtml((q.ai_solution && q.ai_solution.direct_answer) || ('Option ' + ((q.options.find(o=>o.is_correct)||{}).label || 'A')))}</strong>
              </span>
              <span class="card-tag tag-green" style="font-size: 0.68rem;">Verified Key</span>
            </div>

            <!-- Core Conceptual Reason -->
            <div style="margin-bottom: 10px;">
              <div style="font-size: 0.78rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; margin-bottom: 2px;">
                💡 Conceptual Reason:
              </div>
              <div style="font-size: 0.9rem; color: #f1f5f9; line-height: 1.55;">
                ${escapeHtml((q.ai_solution && q.ai_solution.core_reason) || q.feedback || 'Identified based on fundamental BDM course principles.')}
              </div>
            </div>

            <!-- Numerical Calculation (if applicable) -->
            ${(q.ai_solution && q.ai_solution.calculation) ? `
              <div style="margin-bottom: 10px; background: rgba(0,0,0,0.35); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 4px; padding: 10px 14px;">
                <div style="font-size: 0.78rem; font-weight: 700; color: #38bdf8; text-transform: uppercase; margin-bottom: 4px;">
                  🔢 Step-by-Step Working:
                </div>
                <div style="font-family: var(--font-mono); font-size: 0.84rem; color: #a5f3fc; line-height: 1.6; white-space: pre-line;">
                  ${escapeHtml(q.ai_solution.calculation)}
                </div>
              </div>
            ` : ''}

            <!-- Trap Alert -->
            ${(q.ai_solution && q.ai_solution.distractor_trap) ? `
              <div style="margin-bottom: 8px; background: rgba(245, 158, 11, 0.08); border-left: 3px solid var(--accent-amber); padding: 8px 12px; border-radius: 4px;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #fbbf24; text-transform: uppercase;">
                  ⚠️ Trap Alert (Why others are wrong):
                </div>
                <div style="font-size: 0.82rem; color: #fef3c7; line-height: 1.5; margin-top: 2px;">
                  ${escapeHtml(q.ai_solution.distractor_trap)}
                </div>
              </div>
            ` : ''}

            <!-- 1-Second Hinglish Takeaway -->
            ${(q.ai_solution && q.ai_solution.hinglish_shortcut) ? `
              <div style="margin-top: 8px; font-size: 0.82rem; color: #c084fc; background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.25); padding: 6px 12px; border-radius: 4px;">
                <strong>⚡ Hinglish Takeaway:</strong> ${escapeHtml(q.ai_solution.hinglish_shortcut)}
              </div>
            ` : ''}
          </div>
        </div>
      `;
    }).join('');

    if (filtered.length > 60) {
      questionsListEl.innerHTML += `
        <div style="text-align: center; padding: 20px;">
          <p style="color: var(--text-muted); font-size: 0.85rem;">Showing 60 of ${filtered.length} questions. Use filters to narrow down.</p>
        </div>
      `;
    }
  }

  // Answer selection handler
  window.selectOption = function (qid, chosenLabel, isCorrect) {
    if (state.userAnswers[qid]) return; // already answered

    state.userAnswers[qid] = {
      chosenLabel,
      isCorrect,
      timestamp: Date.now()
    };

    localStorage.setItem('bdm_user_answers', JSON.stringify(state.userAnswers));
    updateUserStats();

    // Update DOM in-place without re-rendering entire list
    const card = document.getElementById(`qcard-${qid}`);
    if (!card) return;

    const btns = card.querySelectorAll('.option-choice-btn');
    const qObj = allQuestions.find(q => q.id === qid);
    if (!qObj) return;

    btns.forEach((btn, idx) => {
      btn.classList.add('disabled');
      const opt = qObj.options[idx];
      if (opt.label === chosenLabel) {
        btn.classList.add(isCorrect ? 'selected-correct' : 'selected-wrong');
      }
      if (opt.is_correct && !isCorrect) {
        btn.classList.add('show-as-correct');
      }
    });

    const solDrawer = document.getElementById(`sol-${qid}`);
    if (solDrawer) {
      solDrawer.classList.add('open');
    }
  };

  // Bookmark toggle
  window.toggleBookmark = function (qid) {
    const idx = state.bookmarks.indexOf(qid);
    if (idx > -1) {
      state.bookmarks.splice(idx, 1);
    } else {
      state.bookmarks.push(qid);
    }
    localStorage.setItem('bdm_bookmarks', JSON.stringify(state.bookmarks));
    renderPracticeQuestions();
  };

  // Reset filters helper
  window.resetPracticeFilters = function () {
    state.activeModuleFilter = 'all';
    state.activeSourceFilter = 'all';
    state.onlyCases = false;
    state.onlyBookmarked = false;
    state.onlyMistakes = false;
    state.searchQuery = '';
    if (searchInputEl) searchInputEl.value = '';
    syncFilterButtons();
    document.querySelectorAll('.filter-chip[data-filter-type="cases"], .filter-chip[data-filter-type="bookmarks"], .filter-chip[data-filter-type="mistakes"]').forEach(c => {
      c.classList.remove('active');
    });
    renderPracticeQuestions();
  };

  // Stats updater
  function updateUserStats() {
    const answers = Object.values(state.userAnswers);
    const totalAttempted = answers.length;
    const correctCount = answers.filter(a => a.isCorrect).length;
    const accuracy = totalAttempted > 0 ? Math.round((correctCount / totalAttempted) * 100) : 0;

    if (userAttemptedStat) userAttemptedStat.textContent = `${totalAttempted} / ${allQuestions.length}`;
    if (userScoreStat) userScoreStat.textContent = `${accuracy}%`;
  }

  // 6. TCS iON MOCK EXAM SIMULATOR
  window.startMockExam = function () {
    // Pick 22 questions randomly across modules
    const shuffled = [...allQuestions].sort(() => 0.5 - Math.random());
    state.mockExam.questions = shuffled.slice(0, 22);
    state.mockExam.currentIndex = 0;
    state.mockExam.answers = {};
    state.mockExam.markedForReview = new Set();
    state.mockExam.timeRemaining = 45 * 60;
    state.mockExam.active = true;

    // Switch view
    switchView('mock_exam');
    renderMockExamInterface();

    // Start timer
    if (state.mockExam.timerInterval) clearInterval(state.mockExam.timerInterval);
    state.mockExam.timerInterval = setInterval(() => {
      state.mockExam.timeRemaining--;
      updateMockTimerDisplay();
      if (state.mockExam.timeRemaining <= 0) {
        clearInterval(state.mockExam.timerInterval);
        window.submitMockExam();
      }
    }, 1000);
  };

  function updateMockTimerDisplay() {
    const timerEl = document.getElementById('mock-timer-display');
    if (!timerEl) return;
    const m = Math.floor(state.mockExam.timeRemaining / 60);
    const s = state.mockExam.timeRemaining % 60;
    timerEl.textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  }

  function renderMockExamInterface() {
    const container = document.getElementById('mock-exam-workspace');
    if (!container) return;

    const me = state.mockExam;
    const q = me.questions[me.currentIndex];
    if (!q) return;

    const chosen = me.answers[q.id];
    const isMarked = me.markedForReview.has(q.id);

    container.innerHTML = `
      <div class="mock-exam-container">
        <!-- Question Pane -->
        <div class="mock-left-pane">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 12px;">
              <div>
                <span class="card-tag tag-blue">Question ${me.currentIndex + 1} of 22</span>
                <span style="font-size: 0.78rem; color: var(--text-muted); margin-left: 8px;">Marks: +2.27 | Negative: 0</span>
              </div>
              <div style="font-family: var(--font-mono); color: #38bdf8; font-weight: 700;" id="mock-timer-display">
                --:--
              </div>
            </div>

            <div class="question-text" style="font-size: 1.05rem; margin-bottom: 20px;">
              ${escapeHtml(q.question)}
            </div>

            <div class="options-container">
              ${(q.options || []).map(opt => `
                <button class="option-choice-btn ${chosen === opt.label ? 'selected-correct' : ''}" 
                        onclick="window.selectMockOption('${q.id}', '${opt.label}')">
                  <span class="option-label">${opt.label}</span>
                  <span>${escapeHtml(opt.text)}</span>
                </button>
              `).join('')}
            </div>
          </div>

          <!-- Bottom Action Buttons -->
          <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-subtle); padding-top: 16px; margin-top: 24px;">
            <div style="display: flex; gap: 8px;">
              <button class="btn btn-secondary btn-sm" onclick="window.navMockQuestion(-1)" ${me.currentIndex === 0 ? 'disabled' : ''}>
                ← Previous
              </button>
              <button class="btn btn-secondary btn-sm" onclick="window.navMockQuestion(1)" ${me.currentIndex === 21 ? 'disabled' : ''}>
                Next →
              </button>
            </div>
            
            <div style="display: flex; gap: 8px;">
              <button class="btn btn-sm ${isMarked ? 'btn-accent' : 'btn-secondary'}" onclick="window.toggleMockReview('${q.id}')">
                ${isMarked ? '✓ Marked for Review' : 'Mark for Review'}
              </button>
              <button class="btn btn-primary btn-sm" style="background: var(--color-success);" onclick="window.submitMockExam()">
                Submit Exam
              </button>
            </div>
          </div>
        </div>

        <!-- Right Side Question Palette (TCS iON Style) -->
        <div class="mock-right-palette">
          <h4 style="font-size: 0.92rem; color: #fff; margin-bottom: 8px;">Question Palette</h4>
          <div class="palette-grid">
            ${me.questions.map((item, idx) => {
              let statusClass = '';
              if (idx === me.currentIndex) statusClass += ' current';
              if (me.answers[item.id]) {
                statusClass += ' answered';
              } else if (me.markedForReview.has(item.id)) {
                statusClass += ' marked';
              }
              return `
                <button class="palette-btn ${statusClass}" onclick="window.jumpMockQuestion(${idx})">
                  ${idx + 1}
                </button>
              `;
            }).join('')}
          </div>

          <div class="palette-legend">
            <div class="legend-item">
              <div class="legend-dot" style="background: var(--accent-emerald);"></div>
              <span>Answered (${Object.keys(me.answers).length})</span>
            </div>
            <div class="legend-item">
              <div class="legend-dot" style="background: var(--accent-purple);"></div>
              <span>Marked for Review (${me.markedForReview.size})</span>
            </div>
            <div class="legend-item">
              <div class="legend-dot" style="background: rgba(255, 255, 255, 0.1);"></div>
              <span>Not Visited (${22 - Object.keys(me.answers).length})</span>
            </div>
          </div>
        </div>
      </div>
    `;

    updateMockTimerDisplay();
  }

  window.selectMockOption = function (qid, optLabel) {
    state.mockExam.answers[qid] = optLabel;
    renderMockExamInterface();
  };

  window.toggleMockReview = function (qid) {
    if (state.mockExam.markedForReview.has(qid)) {
      state.mockExam.markedForReview.delete(qid);
    } else {
      state.mockExam.markedForReview.add(qid);
    }
    renderMockExamInterface();
  };

  window.navMockQuestion = function (step) {
    const nextIdx = state.mockExam.currentIndex + step;
    if (nextIdx >= 0 && nextIdx < state.mockExam.questions.length) {
      state.mockExam.currentIndex = nextIdx;
      renderMockExamInterface();
    }
  };

  window.jumpMockQuestion = function (idx) {
    if (idx >= 0 && idx < state.mockExam.questions.length) {
      state.mockExam.currentIndex = idx;
      renderMockExamInterface();
    }
  };

  window.submitMockExam = function () {
    if (state.mockExam.timerInterval) clearInterval(state.mockExam.timerInterval);

    const me = state.mockExam;
    let correctCount = 0;
    const reviewData = me.questions.map(q => {
      const chosen = me.answers[q.id];
      const correctOpt = (q.options || []).find(o => o.is_correct);
      const isCorrect = correctOpt && chosen === correctOpt.label;
      if (isCorrect) correctCount++;
      return { q, chosen, correctOpt, isCorrect };
    });

    const score = (correctCount / 22) * 50;
    const percentage = Math.round((correctCount / 22) * 100);

    const container = document.getElementById('mock-exam-workspace');
    if (!container) return;

    container.innerHTML = `
      <div class="card" style="padding: 32px; text-align: center; max-width: 800px; margin: 0 auto;">
        <span class="card-tag tag-green" style="font-size: 0.9rem; padding: 4px 14px;">Exam Completed</span>
        <h2 style="font-size: 2rem; margin: 16px 0 8px;">Score: ${score.toFixed(1)} / 50 Marks</h2>
        <div style="font-size: 1.1rem; color: #38bdf8; font-weight: 700; margin-bottom: 20px;">
          ${percentage}% (${correctCount} of 22 Correct)
        </div>

        <div style="display: flex; gap: 12px; justify-content: center; margin-bottom: 30px;">
          <button class="btn btn-primary" onclick="window.startMockExam()">Take Another Mock Exam</button>
          <button class="btn btn-secondary" onclick="window.switchViewDirect('practice')">Review in Question Bank</button>
        </div>

        <h3 style="font-size: 1.2rem; text-align: left; margin-bottom: 16px; border-bottom: 1px solid var(--border-subtle); padding-bottom: 8px;">
          Question-by-Question Diagnostic Review:
        </h3>

        <div style="text-align: left; display: flex; flex-direction: column; gap: 14px;">
          ${reviewData.map((item, idx) => `
            <div style="background: rgba(0,0,0,0.3); padding: 14px; border-radius: var(--radius-sm); border-left: 4px solid ${item.isCorrect ? 'var(--accent-emerald)' : 'var(--accent-rose)'};">
              <div style="display: flex; justify-content: space-between; font-size: 0.78rem; color: var(--text-faint); margin-bottom: 4px;">
                <span>Q${idx + 1} • ${item.q.source}</span>
                <span style="font-weight: 700; color: ${item.isCorrect ? 'var(--accent-emerald)' : 'var(--accent-rose)'};">
                  ${item.isCorrect ? '✓ Correct (+2.27)' : '✗ Incorrect (0.00)'}
                </span>
              </div>
              <div style="font-size: 0.9rem; color: #fff; margin-bottom: 6px;">${escapeHtml(item.q.question)}</div>
              <div style="font-size: 0.82rem; color: #cbd5e1;">
                Your Choice: <strong>${item.chosen || 'Not Attempted'}</strong> | Correct Answer: <strong style="color: var(--accent-emerald);">${item.correctOpt ? item.correctOpt.label + '. ' + item.correctOpt.text : 'N/A'}</strong>
              </div>
              ${item.q.feedback ? `<div style="font-size: 0.78rem; color: #94a3b8; margin-top: 4px;">${escapeHtml(item.q.feedback)}</div>` : ''}
            </div>
          `).join('')}
        </div>
      </div>
    `;
  };

  
  window.selectConceptWeek = function(w) {
    state.activeConceptWeek = w;
    renderConceptsView();
  };

  window.jumpToPracticeWeek = function(w) {
    state.activeModuleFilter = 'week_' + w;
    syncFilterButtons();
    switchView('practice');
  };

  window.jumpToActiveWeekConcept = function() {
    let targetWeek = 1;
    if (state.activeModuleFilter && state.activeModuleFilter.startsWith('week_')) {
      targetWeek = parseInt(state.activeModuleFilter.replace('week_', ''), 10);
    }
    state.activeConceptWeek = targetWeek;
    renderConceptsView();
    switchView('concepts');
  };

  window.switchViewDirect = function (viewName) {
    switchView(viewName);
  };

  // Helper: HTML Escaper
  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Start app on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
