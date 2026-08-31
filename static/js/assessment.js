/**
 * Lionix — Assessment Engine JavaScript
 * Timer · Navigation · Auto-Save · Anti-Cheat · Monaco Live Coding Sandbox
 */

'use strict';

// ── State ────────────────────────────────────────────────────
let currentQuestion = 0;
let answers = {};          // { questionId: 'A'/'B'/'C'/'D'/null }
let violations = INITIAL_VIOLATIONS;
let timerInterval = null;
let secondsRemaining = 0;
let saveDebounceTimers = {};
let isSubmitting = false;

// Coding State
let currentMainSection = 'mcq';
let currentProblemIndex = 0;
let monacoEditorInstance = null;

// Anti-Cheat Proctoring State
let antiCheatActive = false;
let lastViolationTimestamp = 0;

const LS_KEY_TIMER   = `eq_timer_${SUBMISSION_ID}`;
const LS_KEY_ANSWERS = `eq_answers_${SUBMISSION_ID}`;

// ── Monaco Config ──
if (window.require) {
  require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' }});
}

// ── Initialization ───────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  if (!QUESTIONS || QUESTIONS.length === 0) {
    const qContent = document.getElementById('questionContent');
    if (qContent) qContent.innerHTML = '<p style="color:var(--danger);text-align:center;padding:40px">No questions available.</p>';
  }

  // Restore saved answers from localStorage, then merge with server-saved
  const lsAnswers = JSON.parse(localStorage.getItem(LS_KEY_ANSWERS) || '{}');
  answers = { ...lsAnswers };

  // Merge server-side saved answers (server is authoritative)
  Object.entries(SAVED_ANSWERS).forEach(([qid, opt]) => {
    if (opt) answers[parseInt(qid)] = opt;
  });

  // Initialize violation counter UI
  updateViolationUI(violations);

  // Restore timer
  const savedSecondsStr = localStorage.getItem(LS_KEY_TIMER);
  const savedSeconds    = savedSecondsStr ? parseInt(savedSecondsStr) : null;
  secondsRemaining = (savedSeconds && savedSeconds > 0 && savedSeconds <= TOTAL_DURATION_SECONDS)
    ? savedSeconds
    : TOTAL_DURATION_SECONDS;

  // Setup Coding Problems UI
  if (typeof CODING_PROBLEMS !== 'undefined' && CODING_PROBLEMS && CODING_PROBLEMS.length > 0) {
    renderCodingProblemTabs();
    initMonacoEditor();
  }

  // If this assessment is Round 2 (Coding) or has no MCQs, switch to Coding Section immediately
  if (typeof IS_CODING_ROUND !== 'undefined' && (IS_CODING_ROUND === true || !QUESTIONS || QUESTIONS.length === 0)) {
    switchMainSection('coding');
  }

  // Check if screensharing is supported
  const isScreenshareSupported = !!(navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia);
  if (!isScreenshareSupported) {
    const overlay = document.getElementById('screenshareOverlay');
    if (overlay) {
      const titleEl = overlay.querySelector('.vio-title');
      const msgEl = overlay.querySelector('.vio-msg');
      const btnEl = document.getElementById('startScreenshareBtn');
      if (titleEl) titleEl.textContent = 'Proctoring Offline (HTTP/LAN)';
      if (msgEl) msgEl.innerHTML = 'Screenshare monitoring requires HTTPS or localhost. Since this is an unencrypted connection, proctoring is offline. Click below to continue.';
      if (btnEl) btnEl.textContent = 'Acknowledge & Start Test';
    }
  }

  // Setup tab switch detection
  setupAntiCheatListeners();
});

// ── Screenshare Proctoring Setup ─────────────────────────────
async function requestScreenshare() {
  const isScreenshareSupported = !!(navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia);
  if (!isScreenshareSupported) {
    document.getElementById('screenshareOverlay').style.display = 'none';
    const videoEl = document.getElementById('proctorVideo');
    const fallbackEl = document.getElementById('proctorVideoFallback');
    if (videoEl && fallbackEl) {
      videoEl.style.display = 'none';
      fallbackEl.style.display = 'flex';
    }
    startTimer();
    renderQuestion(currentQuestion);
    updateNavGrid();
    
    setTimeout(() => {
      antiCheatActive = true;
    }, 3000);
    return;
  }

  const btn = document.getElementById('startScreenshareBtn');
  btn.disabled = true;
  btn.textContent = 'Requesting Permission...';
  try {
    const stream = await navigator.mediaDevices.getDisplayMedia({
      video: { displaySurface: "monitor" },
      audio: false
    });
    
    const track = stream.getVideoTracks()[0];
    const settings = track.getSettings();
    if (settings.displaySurface && settings.displaySurface !== 'monitor') {
      track.stop();
      alert('Proctoring Violation: You must share your ENTIRE screen, not a window or tab. Please try again.');
      btn.disabled = false;
      btn.textContent = 'Enable Screenshare & Start Test';
      return;
    }
    
    track.addEventListener('ended', () => {
      if (!isSubmitting) autoSubmit('Screenshare terminated by user');
    });

    try {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const webcamStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        const videoEl = document.getElementById('proctorVideo');
        if (videoEl) videoEl.srcObject = webcamStream;
      }
    } catch (camErr) {
      console.warn('Webcam unavailable:', camErr);
    }
    
    document.getElementById('screenshareOverlay').style.display = 'none';
    startTimer();
    renderQuestion(currentQuestion);
    updateNavGrid();
    
    // Activate anti-cheat after a 3-second grace period for focus stabilization
    setTimeout(() => {
      antiCheatActive = true;
    }, 3000);
  } catch (err) {
    alert('Screenshare permission is mandatory to attempt this assessment.');
    btn.disabled = false;
    btn.textContent = 'Enable Screenshare & Start Test';
  }
}

// ── Anti-Cheat & Anti-Extension Shield ───────────────────────
function setupAntiCheatListeners() {
  // 1. Tab switches & minimizing
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && antiCheatActive && !isSubmitting) {
      recordViolation('tab_switch');
    }
  });

  window.addEventListener('blur', () => {
    if (antiCheatActive && !isSubmitting) {
      recordViolation('window_blur');
    }
  });

  // 2. Prevent right-click context menu
  document.addEventListener('contextmenu', e => {
    e.preventDefault();
    return false;
  });

  // 3. Block copy, cut, paste, drag & drop
  ['copy', 'cut', 'paste', 'dragstart', 'drop'].forEach(evt => {
    document.addEventListener(evt, e => {
      e.preventDefault();
      return false;
    });
  });

  // 4. Block Developer Tools & Common Extension Shortcuts
  document.addEventListener('keydown', e => {
    if (e.key === 'F12' || e.keyCode === 123 || e.key === 'F5' || (e.ctrlKey && e.key === 'r')) {
      e.preventDefault();
      return false;
    }
    if (e.ctrlKey || e.metaKey) {
      const key = (e.key || '').toLowerCase();
      if (['c', 'v', 'x', 'a', 'u', 's', 'p', 'j'].includes(key) || (e.shiftKey && ['i', 'j', 'c', 'k', 'm'].includes(key))) {
        e.preventDefault();
        return false;
      }
    }
    if (e.altKey || e.key === 'Meta') {
      recordViolation('system_key_switch');
    }
  });

  // 5. Anti-AI Extension DOM Scanner
  setInterval(() => {
    if (!antiCheatActive) return;
    const suspiciousSelectors = [
      '[id*="chatgpt" i]', '[class*="chatgpt" i]',
      '[id*="copilot" i]', '[class*="copilot" i]',
      '[id*="merlin" i]', '[class*="merlin" i]',
      '[id*="sider" i]', '[class*="sider" i]',
      '[id*="monica" i]', '[class*="monica" i]',
      '[id*="harpa" i]', '[class*="harpa" i]',
      '[id*="grammarly" i]', '[class*="grammarly" i]',
      '[id*="ai-assistant" i]', '[class*="ai-assistant" i]'
    ];
    suspiciousSelectors.forEach(sel => {
      try {
        const found = document.querySelectorAll(sel);
        found.forEach(el => {
          if (!el.closest('.exam-layout') && !el.closest('.violation-overlay')) {
            el.style.display = 'none';
            el.remove();
          }
        });
      } catch (err) {}
    });
  }, 1500);
}

async function recordViolation(reason) {
  if (!antiCheatActive || isSubmitting) return;

  const now = Date.now();
  // De-duplicate rapid triggers within 3.5 seconds
  if (now - lastViolationTimestamp < 3500) {
    return;
  }
  lastViolationTimestamp = now;

  violations++;
  updateViolationUI(violations);

  try {
    const res = await fetch(VIOLATION_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify({ reason: reason })
    });
    const data = await res.json();
    if (data && data.auto_submitted) {
      autoSubmit('Maximum violations exceeded');
      return;
    }
  } catch (err) {}

  if (violations >= 1) {
    autoSubmit('Tab switch or external window switch detected');
  } else {
    showViolationModal(violations);
  }
}

function showViolationModal(count) {
  const modal = document.getElementById('violationOverlay');
  const countEl = document.getElementById('vioCount');
  if (countEl) countEl.textContent = count;
  if (modal) modal.style.display = 'flex';
}

function dismissViolation() {
  const modal = document.getElementById('violationOverlay');
  if (modal) modal.style.display = 'none';
}

function updateViolationUI(count) {
  const header = document.getElementById('vioHeader');
  const ind = document.getElementById('vioIndicator');
  if (header) header.textContent = count;
  if (ind) {
    if (count > 0) ind.classList.remove('vio-clear');
    else ind.classList.add('vio-clear');
  }
}

// ── Timer ────────────────────────────────────────────────────
function startTimer() {
  updateTimerDisplay(secondsRemaining);
  if (timerInterval) clearInterval(timerInterval);
  timerInterval = setInterval(() => {
    secondsRemaining--;
    localStorage.setItem(LS_KEY_TIMER, secondsRemaining);
    updateTimerDisplay(secondsRemaining);

    if (secondsRemaining <= 0) {
      clearInterval(timerInterval);
      autoSubmit('Time limit reached');
    }
  }, 1000);
}

function updateTimerDisplay(sec) {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  const el = document.getElementById('timerDisplay');
  const wrap = document.getElementById('timerWrapper');
  if (el) el.textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  if (wrap) {
    if (sec <= 120) wrap.className = 'timer-wrapper timer-danger';
    else if (sec <= 300) wrap.className = 'timer-wrapper timer-warning';
    else wrap.className = 'timer-wrapper';
  }
}

function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function formatQuestionText(text) {
  if (!text) return '';
  let formatted = escapeHtml(text)
    .replace(/_____+/g, '<span class="fib-blank-box">&nbsp;&nbsp;_____&nbsp;&nbsp;</span>')
    .replace(/\n\n/g, '<br/><br/>')
    .replace(/\n/g, '<br/>');
  return formatted;
}

// ── QUESTION NAVIGATION & RENDERING (MCQ & FIB) ───────────────
function renderQuestion(idx) {
  if (!QUESTIONS || idx < 0 || idx >= QUESTIONS.length) return;
  currentQuestion = idx;

  const q = QUESTIONS[idx];
  const isFIB = (q.question_type === 'fib' || (!q.options || q.options.length === 0));
  const qProgress = document.getElementById('currentQNum');
  const progressFill = document.getElementById('progressFill');
  if (qProgress) qProgress.textContent = idx + 1;
  if (progressFill) progressFill.style.width = `${((idx + 1) / QUESTIONS.length) * 100}%`;

  const container = document.getElementById('questionContent');
  if (!container) return;

  const savedOpt = answers[q.id] || '';

  let bodyHtml = '';
  if (isFIB) {
    bodyHtml = `
      <div class="fib-question-box">
        <div class="fib-tag">✍️ Fill In The Blank (Technical Question ${idx + 1})</div>
        <div class="fib-prompt-text">${formatQuestionText(q.question)}</div>
        <div class="fib-input-container">
          <label class="fib-input-label">Type your answer:</label>
          <div class="fib-input-wrapper">
            <input type="text"
                   class="fib-field-input"
                   id="fibInput_${q.id}"
                   value="${escapeHtml(savedOpt)}"
                   placeholder="Type exact keyword, syntax, command, or value..."
                   autocomplete="off"
                   autocorrect="off"
                   autocapitalize="off"
                   spellcheck="false"
                   data-gramm="false"
                   oninput="onFibInput(${q.id}, this.value)"
            />
          </div>
          <div class="fib-guidance">
            <span>⚡ Note: Type only the missing keyword or value. Matching is verified accurately.</span>
          </div>
        </div>
      </div>
    `;
  } else {
    let optsHtml = '';
    (q.options || []).forEach(opt => {
      const isSelected = (savedOpt === opt.key);
      optsHtml += `
        <div class="opt-item ${isSelected ? 'opt-selected' : ''}" onclick="selectOption(${q.id}, '${opt.key}')">
          <div class="opt-key-circle">${opt.key}</div>
          <div class="opt-text">${opt.text}</div>
        </div>
      `;
    });
    bodyHtml = `
      <div class="q-card-wrapper">
        <div class="q-title-text">${formatQuestionText(q.question)}</div>
        <div class="options-list">${optsHtml}</div>
      </div>
    `;
  }

  container.innerHTML = bodyHtml;

  if (isFIB) {
    const inputEl = document.getElementById(`fibInput_${q.id}`);
    if (inputEl) {
      setTimeout(() => inputEl.focus(), 50);
    }
  }

  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  if (prevBtn) prevBtn.disabled = (idx === 0);
  if (nextBtn) {
    if (idx === QUESTIONS.length - 1) {
      nextBtn.innerHTML = 'Submit Assessment <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>';
      nextBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
      nextBtn.onclick = () => confirmSubmit();
    } else {
      nextBtn.innerHTML = 'Next <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>';
      nextBtn.style.background = '';
      nextBtn.onclick = () => navigateTo(idx + 1);
    }
  }

  updateNavGrid();
}

function selectOption(qId, key) {
  answers[qId] = key;
  localStorage.setItem(LS_KEY_ANSWERS, JSON.stringify(answers));
  renderQuestion(currentQuestion);
  saveAnswerDebounced(qId, key);
}

function onFibInput(qId, val) {
  answers[qId] = val.trim();
  localStorage.setItem(LS_KEY_ANSWERS, JSON.stringify(answers));
  updateNavGrid();
  saveAnswerDebounced(qId, val.trim());
}

function saveAnswerDebounced(qId, key) {
  if (saveDebounceTimers[qId]) clearTimeout(saveDebounceTimers[qId]);
  saveDebounceTimers[qId] = setTimeout(async () => {
    try {
      await fetch(SAVE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({ question_id: qId, selected_option: key })
      });
    } catch (e) {}
  }, 300);
}

function navigateTo(idx) {
  if (idx >= 0 && idx < QUESTIONS.length) {
    renderQuestion(idx);
  }
}

function updateNavGrid() {
  const answeredCountEl = document.getElementById('answeredCount');
  const unansweredCountEl = document.getElementById('unansweredCount');
  let ansCount = 0;

  QUESTIONS.forEach((q, idx) => {
    const btn = document.getElementById(`nav-${idx}`);
    if (!btn) return;
    const isAnswered = !!answers[q.id];
    if (isAnswered) ansCount++;

    btn.className = 'nav-btn';
    if (idx === currentQuestion) btn.classList.add('nav-current');
    if (isAnswered) btn.classList.add('nav-answered');
  });

  if (answeredCountEl) answeredCountEl.textContent = ansCount;
  if (unansweredCountEl) unansweredCountEl.textContent = QUESTIONS.length - ansCount;
}

// ── MONACO LIVE CODING SANDBOX ────────────────────────────────
function initMonacoEditor() {
  if (!window.require) return;
  require(['vs/editor/editor.main'], function() {
    const container = document.getElementById('monacoEditorBox');
    if (!container) return;

    const prob = CODING_PROBLEMS[currentProblemIndex];
    const initialCode = getProblemCode(prob, 'python');

    monacoEditorInstance = monaco.editor.create(container, {
      value: initialCode,
      language: 'python',
      theme: 'vs-dark',
      automaticLayout: true,
      fontSize: 14,
      fontFamily: "'Fira Code', Consolas, monospace",
      minimap: { enabled: false },
      scrollBeyondLastLine: false,
      tabSize: 4,
      bracketPairColorization: { enabled: true }
    });

    monacoEditorInstance.onDidChangeModelContent(() => {
      const code = monacoEditorInstance.getValue();
      const lang = document.getElementById('codeLangSelect').value;
      localStorage.setItem(`eq_code_${prob.id}_${lang}`, code);
    });
  });
}

function renderCodingProblemTabs() {
  const bar = document.getElementById('codingProblemTabs');
  if (!bar) return;
  bar.innerHTML = '';
  CODING_PROBLEMS.forEach((p, idx) => {
    const btn = document.createElement('button');
    btn.className = `prob-tab-btn ${idx === currentProblemIndex ? 'active' : ''}`;
    btn.textContent = `Problem ${idx + 1}: ${p.title}`;
    btn.onclick = () => selectCodingProblem(idx);
    bar.appendChild(btn);
  });
  renderCurrentCodingProblem();
}

function selectCodingProblem(idx) {
  currentProblemIndex = idx;
  renderCodingProblemTabs();
  renderCurrentCodingProblem();
  if (monacoEditorInstance) {
    const lang = document.getElementById('codeLangSelect').value;
    const prob = CODING_PROBLEMS[currentProblemIndex];
    monacoEditorInstance.setValue(getProblemCode(prob, lang));
  }
}

function renderCurrentCodingProblem() {
  const p = CODING_PROBLEMS[currentProblemIndex];
  if (!p) return;

  const titleEl = document.getElementById('probTitleText');
  const diffEl = document.getElementById('probDiffBadge');
  const bodyEl = document.getElementById('codingProblemBody');

  if (titleEl) titleEl.textContent = p.title;
  if (diffEl) {
    diffEl.textContent = p.difficulty || 'Medium';
  }

  let sampleCasesHtml = '';
  if (p.sample_testcases && p.sample_testcases.length) {
    p.sample_testcases.forEach((tc, idx) => {
      sampleCasesHtml += `
        <div class="prob-sec-header">Example ${idx + 1}</div>
        <div style="font-size:12px;color:#94a3b8">Input:</div>
        <div class="code-snippet-box">${tc.input_data}</div>
        <div style="font-size:12px;color:#94a3b8">Expected Output:</div>
        <div class="code-snippet-box">${tc.expected_output}</div>
      `;
    });
  }

  if (bodyEl) {
    bodyEl.innerHTML = `
      <div style="margin-bottom:16px">${p.problem_statement.replace(/\n/g, '<br>')}</div>
      ${p.input_format ? `<div class="prob-sec-header">Input Format</div><div style="color:#cbd5e1;font-size:13px">${p.input_format}</div>` : ''}
      ${p.output_format ? `<div class="prob-sec-header">Output Format</div><div style="color:#cbd5e1;font-size:13px">${p.output_format}</div>` : ''}
      ${p.constraints ? `<div class="prob-sec-header">Constraints</div><div class="code-snippet-box">${p.constraints}</div>` : ''}
      ${sampleCasesHtml}
    `;
  }
}

function getProblemCode(prob, lang) {
  const saved = localStorage.getItem(`eq_code_${prob.id}_${lang}`);
  if (saved) return saved;
  if (prob.saved_submission && prob.saved_submission.language === lang) {
    return prob.saved_submission.source_code;
  }
  if (prob.starter_code_json && prob.starter_code_json[lang]) {
    return prob.starter_code_json[lang];
  }
  return '# Write your solution here\n';
}

function onCodeLangChange() {
  if (!monacoEditorInstance || !CODING_PROBLEMS) return;
  const lang = document.getElementById('codeLangSelect').value;
  const prob = CODING_PROBLEMS[currentProblemIndex];
  const monacoLang = lang === 'cpp' ? 'cpp' : (lang === 'javascript' ? 'javascript' : (lang === 'java' ? 'java' : 'python'));
  monaco.editor.setModelLanguage(monacoEditorInstance.getModel(), monacoLang);
  monacoEditorInstance.setValue(getProblemCode(prob, lang));
}

function resetCodingTemplate() {
  if (!monacoEditorInstance || !CODING_PROBLEMS) return;
  if (!confirm('Reset code to template? Current changes for this language will be cleared.')) return;
  const lang = document.getElementById('codeLangSelect').value;
  const prob = CODING_PROBLEMS[currentProblemIndex];
  localStorage.removeItem(`eq_code_${prob.id}_${lang}`);
  const defaultCode = (prob.starter_code_json && prob.starter_code_json[lang]) || '';
  monacoEditorInstance.setValue(defaultCode);
}

// ── CODE EXECUTION (RUN & SUBMIT) ─────────────────────────────
async function executeSampleCode() {
  if (!monacoEditorInstance || !CODING_PROBLEMS) return;
  const btn = document.getElementById('btnRunSample');
  const consoleBox = document.getElementById('consoleOutputBox');
  btn.disabled = true;
  btn.textContent = '⏳ Running...';
  consoleBox.innerHTML = '<div style="color:#94a3b8">Executing against sample test cases...</div>';

  const prob = CODING_PROBLEMS[currentProblemIndex];
  const payload = {
    problem_id: prob.id,
    language: document.getElementById('codeLangSelect').value,
    source_code: monacoEditorInstance.getValue()
  };

  try {
    const res = await fetch(CODE_RUN_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Execution failed.');

    renderConsoleExecution(data);
  } catch (err) {
    consoleBox.innerHTML = `<div style="color:#ef4444">❌ Execution Error: ${err.message}</div>`;
  } finally {
    btn.disabled = false;
    btn.textContent = '▶ Run Sample Cases';
  }
}

async function submitProblemSolution() {
  if (!monacoEditorInstance || !CODING_PROBLEMS) return;
  const btn = document.getElementById('btnSubmitCodeProb');
  const consoleBox = document.getElementById('consoleOutputBox');
  btn.disabled = true;
  btn.textContent = '⏳ Evaluating...';
  consoleBox.innerHTML = '<div style="color:#94a3b8">Evaluating code against hidden test suite...</div>';

  const prob = CODING_PROBLEMS[currentProblemIndex];
  const payload = {
    problem_id: prob.id,
    language: document.getElementById('codeLangSelect').value,
    source_code: monacoEditorInstance.getValue()
  };

  try {
    const res = await fetch(CODE_SUBMIT_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken()
      },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Submission failed.');

    renderSubmissionScore(data);
  } catch (err) {
    consoleBox.innerHTML = `<div style="color:#ef4444">❌ Submission Error: ${err.message}</div>`;
  } finally {
    btn.disabled = false;
    btn.textContent = '⚡ Submit Code';
  }
}

function renderConsoleExecution(data) {
  const box = document.getElementById('consoleOutputBox');
  if (data.results && data.results.length) {
    let html = `<div style="font-weight:700;margin-bottom:8px;color:${data.all_passed ? '#10b981' : '#ef4444'}">
      Status: ${data.overall_status} (${data.passed_count}/${data.total_count} Sample Cases Passed)
    </div>`;

    data.results.forEach((r, idx) => {
      html += `
        <div class="tc-res-card ${r.passed ? 'tc-passed-border' : 'tc-failed-border'}">
          <div style="display:flex;justify-content:space-between;font-size:11px;font-weight:700;color:#94a3b8;margin-bottom:4px;">
            <span>Case ${idx + 1}: ${r.status}</span>
            <span>${r.execution_time_ms} ms</span>
          </div>
          <div style="font-size:11px;color:#94a3b8">Input: <span style="color:#fff">${r.input_data || ''}</span></div>
          <div style="font-size:11px;color:#94a3b8">Expected: <span style="color:#fff">${r.expected_output || ''}</span></div>
          <div style="font-size:11px;color:#94a3b8">Your Output: <span style="color:${r.passed ? '#10b981' : '#ef4444'}">${r.actual_output || ''}</span></div>
          ${r.stderr ? `<div style="font-size:11px;color:#ef4444;margin-top:4px">Stderr: ${r.stderr}</div>` : ''}
        </div>
      `;
    });
    box.innerHTML = html;
  } else {
    box.innerHTML = `<pre style="color:#fff">${data.actual_output || data.stderr || 'No output.'}</pre>`;
  }
}

function renderSubmissionScore(data) {
  const box = document.getElementById('consoleOutputBox');
  box.innerHTML = `
    <div style="padding:6px;">
      <div style="font-size:15px;font-weight:800;color:${data.all_passed ? '#10b981' : '#f59e0b'}">
        ${data.overall_status} • Score: ${data.score}/${data.max_score} Points
      </div>
      <div style="color:#94a3b8;font-size:12px;margin-top:4px;">
        Passed <strong>${data.passed_count}</strong> of <strong>${data.total_count}</strong> testcases.
      </div>
    </div>
  `;
}

// ── SUBMISSION ───────────────────────────────────────────────
function confirmSubmit() {
  const answered = Object.values(answers).filter(Boolean).length;
  const total = QUESTIONS.length;
  const unans = total - answered;
  const msg = unans > 0
    ? `You have ${unans} unanswered question(s).\n\nAre you sure you want to submit?`
    : 'Are you sure you want to submit your assessment?';

  if (confirm(msg)) {
    submitAssessment();
  }
}

function autoSubmit(reason) {
  if (isSubmitting) return;
  isSubmitting = true;
  clearInterval(timerInterval);

  const overlay = document.getElementById('submittingOverlay');
  const titleEl = document.getElementById('submittingTitle');
  const msgEl = document.getElementById('submittingMsg');
  if (titleEl) titleEl.textContent = 'Auto-Submitting Assessment…';
  if (msgEl) msgEl.textContent = `Reason: ${reason}. Please wait.`;
  if (overlay) overlay.style.display = 'flex';

  submitAssessment();
}

function submitAssessment() {
  isSubmitting = true;
  clearInterval(timerInterval);
  localStorage.removeItem(LS_KEY_TIMER);
  localStorage.removeItem(LS_KEY_ANSWERS);

  const overlay = document.getElementById('submittingOverlay');
  if (overlay) overlay.style.display = 'flex';

  const form = document.getElementById('submitForm');
  if (form) form.submit();
}

function getCsrfToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta) return meta.getAttribute('content');
  const inp = document.querySelector('input[name="csrf_token"]');
  return inp ? inp.value : '';
}
