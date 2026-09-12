# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update master data pointers and state
content = content.replace(
    "const modulesInfo = (courseData.course && courseData.course.modules) || {};",
    """const modulesInfo = (courseData.course && courseData.course.modules) || {};
  const conceptsData = window.BDM_CONCEPTS || {};"""
)

content = content.replace(
    "currentView: 'syllabus',",
    """currentView: 'syllabus',
    activeConceptWeek: 1,"""
)

content = content.replace(
    "syllabus: document.getElementById('view-syllabus'),",
    """syllabus: document.getElementById('view-syllabus'),
    concepts: document.getElementById('view-concepts'),"""
)

# 2. Add renderConceptsView to init()
content = content.replace(
    "renderSyllabusView();\n    renderMnemonicsView();",
    "renderSyllabusView();\n    renderConceptsView();\n    renderMnemonicsView();"
)

# 3. Add renderConceptsView function
concepts_func = """
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
"""

content = content.replace("// 1. SYLLABUS & MODULES MATRIX", concepts_func + "\n  // 1. SYLLABUS & MODULES MATRIX")

# 4. Update renderSyllabusView buttons to add Learn Concepts (Hinglish)
old_syllabus_btn = """          <div style="display: flex; gap: 8px; margin-top: auto;">
            <button class="btn btn-primary btn-sm" style="flex: 1;" data-jump-view="practice" data-jump-filter="week_${w}">
              Practice Week ${w} (${qCount})
            </button>
          </div>"""

new_syllabus_btn = """          <div style="display: flex; gap: 8px; margin-top: auto;">
            <button class="btn btn-secondary btn-sm" style="flex: 1;" onclick="window.selectConceptWeek(${w}); window.switchViewDirect('concepts');">
              📖 Learn Concept
            </button>
            <button class="btn btn-primary btn-sm" style="flex: 1;" data-jump-view="practice" data-jump-filter="week_${w}">
              🎯 Practice (${qCount})
            </button>
          </div>"""

content = content.replace(old_syllabus_btn, new_syllabus_btn)

# 5. Add global window helpers
global_helpers = """
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
"""

content = content.replace("window.switchViewDirect = function (viewName) {", global_helpers + "\n  window.switchViewDirect = function (viewName) {")

# 6. Update practice banner text in renderPracticeQuestions
practice_banner_update = """
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
"""

content = content.replace("if (questionCountBadge) {\n      questionCountBadge.textContent = `${filtered.length} of ${allQuestions.length} Questions`;\n    }", "if (questionCountBadge) {\n      questionCountBadge.textContent = `${filtered.length} of ${allQuestions.length} Questions`;\n    }\n" + practice_banner_update)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated app.js with Concept Booster & Hinglish Learning Module!")
