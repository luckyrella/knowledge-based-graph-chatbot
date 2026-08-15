/* ═══════════════════════════════════════════════════
   ADVANCED CHATBOT  — Complete Override
   ═══════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
    /* ── DOM refs ─────────────────────────────────── */
    const chatToggle     = document.getElementById('chatToggle');
    const chatPanel      = document.getElementById('chatPanel');
    const closeChat      = document.getElementById('closeChat');
    const chatMessages   = document.getElementById('chatMessages');
    const userInput      = document.getElementById('userInput');
    const sendBtn        = document.getElementById('sendBtn');
    const suggestionsBar = document.getElementById('chatSuggestions');
    const clearBtn       = document.getElementById('clearChat');

    /* ── State ────────────────────────────────────── */
    let ctx = { lastIntent: null, lastDept: null, lastCourse: null };
    let isFirstOpen  = true;
    let isTyping     = false;
    let msgId        = 0;
    let typingSpeed  = 8; // ms per char for typewriter

    /* ── Quick-reply presets per intent ──────────── */
    const CHIPS = {
        default:         ['📚 Departments', '🎓 Admissions', '💰 Fee Structure', '💼 Placements', '🏫 Facilities', '📞 Contact'],
        fee_info:        ['💳 B.Tech Fees', '🎓 M.Tech Fees', '💼 MBA Fees', '🏠 Hostel Fees', '🎖️ Scholarships'],
        department_info: ['💻 CSE', '🤖 AI & ML', '📊 Data Science', '🔒 Cyber Security', '📡 ECE', '💼 Placements'],
        admission_info:  ['🎓 B.Tech Admission', '📘 M.Tech Admission', '📊 MBA Admission', '↩️ Lateral Entry', '💰 Fee Structure'],
        placement_info:  ['🏆 Top Recruiters', '📈 Highest Package', '🎯 Training Programs', '🏫 Facilities', '📚 Departments'],
        facility_info:   ['🏠 Hostel', '📚 Library', '🏋️ Gym', '🚌 Transport', '📞 Contact'],
        scholarship_info:['💰 Fee Structure', '🎓 Admissions', '📞 Contact'],
        management_info: ['👥 All Leaders', '📞 Contact', '🏛️ College Info'],
        club_info:       ['📚 Departments', '🏫 Facilities', '💼 Placements'],
        contact_info:    ['📍 Location', '📞 Phones', '📚 Departments', '🎓 Admissions'],
        college_info:    ['📚 Departments', '💼 Placements', '🎓 Admissions', '🏫 Facilities'],
        event_info:      ['🎉 Fests', '📚 Departments', '🏫 Facilities'],
        greeting:        ['📚 Departments', '🎓 Admissions', '💰 Fee Structure', '💼 Placements', '📞 Contact'],
    };

    /* ── Intent → follow-up quick replies in message ── */
    const QUICK_REPLIES = {
        department_info: ['View Fees', 'Admissions', 'Placements'],
        fee_info:        ['B.Tech Fees', 'M.Tech Fees', 'Scholarships'],
        placement_info:  ['Top Recruiters', 'Training Programs', 'Departments'],
        admission_info:  ['Fee Structure', 'Lateral Entry', 'Documents needed'],
        facility_info:   ['Hostel', 'Library', 'Sports'],
        college_info:    ['Departments', 'Placements', 'Admissions'],
    };

    /* ═══════════════ TOGGLE ═══════════════ */
    chatToggle.addEventListener('click', () => {
        const open = chatPanel.classList.toggle('active');
        chatToggle.innerHTML = open ? '<i class="fas fa-times"></i>' : '<i class="fas fa-comment-dots"></i>';
        document.body.style.overflow = open ? 'hidden' : '';
        if (open) {
            if (isFirstOpen) {
                isFirstOpen = false;
                setTimeout(() => showWelcome(), 500);
            }
            setTimeout(() => userInput.focus(), 150);
        }
    });

    closeChat.addEventListener('click', () => {
        chatPanel.classList.remove('active');
        chatToggle.innerHTML = '<i class="fas fa-comment-dots"></i>';
        document.body.style.overflow = '';
    });

    /* Clear chat */
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            chatMessages.innerHTML = '';
            ctx = { lastIntent: null, lastDept: null, lastCourse: null };
            msgId = 0;
            renderChips('default');
            setTimeout(() => showWelcome(), 300);
        });
    }

    /* ═══════════════ WELCOME ═══════════════ */
    function showWelcome() {
        const html = `
        <div class="welcome-card">
          <img src="/static/bot_avatar.png" class="wc-avatar" alt="Bot">
          <h4>Sphoorthy Assistant 🎓</h4>
          <p>Hi there! I'm your smart college guide. Ask me anything about admissions, departments, fees, placements, or campus life!</p>
          <div class="wc-chips">
            <span class="wc-chip" data-q="Tell me about CSE">💻 CSE Dept</span>
            <span class="wc-chip" data-q="What are the fees?">💰 Fees</span>
            <span class="wc-chip" data-q="Tell me about placements">💼 Placements</span>
            <span class="wc-chip" data-q="How to get admission?">🎓 Admissions</span>
            <span class="wc-chip" data-q="What facilities are there?">🏫 Facilities</span>
            <span class="wc-chip" data-q="Scholarship available?">🎖️ Scholarships</span>
          </div>
        </div>`;
        injectRaw(html);
        bindWelcomeChips();
    }

    function bindWelcomeChips() {
        document.querySelectorAll('.wc-chip').forEach(c => {
            c.addEventListener('click', () => handleSend(c.dataset.q));
        });
    }

    /* ═══════════════ INPUT ═══════════════ */
    userInput.addEventListener('keydown', e => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(userInput.value); }
    });
    userInput.addEventListener('input', () => {
        sendBtn.classList.toggle('has-text', userInput.value.trim().length > 0);
    });
    sendBtn.addEventListener('click', () => handleSend(userInput.value));

    /* ═══════════════ CORE SEND ═══════════════ */
    function handleSend(raw) {
        const text = raw.trim();
        if (!text || isTyping) return;

        addUserBubble(text);
        userInput.value = '';
        sendBtn.classList.remove('has-text');
        isTyping = true;

        const typingId = showTyping();

        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, context: ctx })
        })
        .then(r => r.json())
        .then(data => {
            removeTyping(typingId);
            isTyping = false;

            const intent  = data.intent  || 'general_query';
            const dept    = data.entities?.department || null;
            const course  = data.entities?.course     || null;

            if (intent  !== 'general_query') ctx.lastIntent = intent;
            if (dept)   ctx.lastDept   = dept;
            if (course) ctx.lastCourse = course;

            addBotBubble(data.response || "I'm sorry, I couldn't find that info.", intent);
            renderChips(intent);
        })
        .catch(() => {
            removeTyping(typingId);
            isTyping = false;
            addBotBubble('⚠️ Connection error. Please check the server and try again.', 'error');
        });
    }

    /* ═══════════════ USER BUBBLE ═══════════════ */
    function addUserBubble(text) {
        const row = el('div', 'msg-row user-row');
        const bubble = el('div', 'message user');
        bubble.textContent = text;
        const meta = el('div', 'msg-meta user-meta');
        meta.textContent = timeStr();
        row.append(bubble, meta);
        chatMessages.appendChild(row);
        animIn(row, 'right');
        scroll();
    }

    /* ═══════════════ BOT BUBBLE ═══════════════ */
    function addBotBubble(rawText, intent) {
        const id = ++msgId;
        const row = el('div', 'msg-row bot-row');
        row.dataset.id = id;

        /* Avatar */
        const avatar = el('div', 'bot-avatar');
        avatar.innerHTML = '<img src="/static/bot_avatar.png" alt="Bot"><span class="online-dot"></span>';

        const right = el('div', 'bot-right');

        /* Bubble */
        const bubble = el('div', 'message bot');

        /* Meta */
        const meta = el('div', 'msg-meta bot-meta');
        meta.innerHTML = `<i class="fas fa-robot" style="font-size:0.6rem;margin-right:3px"></i> Sphoorthy Assistant &middot; ${timeStr()}`;

        /* Feedback */
        const fb = el('div', 'msg-feedback');
        fb.innerHTML = `
          <button class="fb-btn" title="Helpful" data-id="${id}" data-v="up"><i class="fas fa-thumbs-up"></i></button>
          <button class="fb-btn" title="Not helpful" data-id="${id}" data-v="down"><i class="fas fa-thumbs-down"></i></button>`;

        right.append(bubble, meta, fb);
        row.append(avatar, right);
        chatMessages.appendChild(row);
        animIn(row, 'left');

        /* Typewriter */
        const html = formatResponse(rawText);
        typewrite(bubble, html, () => {
            /* After typing done, inject quick replies */
            const qr = QUICK_REPLIES[intent];
            if (qr) {
                const qrRow = el('div', 'quick-replies');
                qr.forEach(label => {
                    const b = el('button', 'qr-btn');
                    b.textContent = label;
                    b.addEventListener('click', () => handleSend(label));
                    qrRow.appendChild(b);
                });
                right.insertBefore(qrRow, meta);
            }
            scroll();
        });

        /* Feedback handler */
        fb.addEventListener('click', e => {
            const btn = e.target.closest('.fb-btn');
            if (!btn) return;
            fb.querySelectorAll('.fb-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });

        scroll();
    }

    /* ═══════════════ TYPEWRITER ═══════════════ */
    function typewrite(el, html, done) {
        /* Fast-path: just inject instantly for long messages */
        if (html.length > 600) {
            el.innerHTML = html;
            done && done();
            return;
        }

        /* Parse html into plain chars + tag boundaries */
        const temp = document.createElement('div');
        temp.innerHTML = html;
        const fullText = temp.innerHTML;
        let i = 0;
        el.innerHTML = '';

        function tick() {
            if (i < fullText.length) {
                /* Skip over HTML tags instantly */
                if (fullText[i] === '<') {
                    const end = fullText.indexOf('>', i);
                    i = end + 1;
                    el.innerHTML = fullText.slice(0, i);
                } else {
                    i++;
                    el.innerHTML = fullText.slice(0, i) + '<span class="cursor">|</span>';
                }
                scroll();
                setTimeout(tick, typingSpeed);
            } else {
                el.innerHTML = fullText;
                done && done();
            }
        }
        tick();
    }

    /* ═══════════════ TYPING INDICATOR ═══════════════ */
    function showTyping() {
        const id = 'ty-' + Date.now();
        const row = el('div', 'msg-row bot-row');
        row.id = id;

        const avatar = el('div', 'bot-avatar');
        avatar.innerHTML = '<img src="/static/bot_avatar.png" alt="Bot"><span class="online-dot"></span>';

        const ind = el('div', 'typing-indicator');
        ind.innerHTML = '<span></span><span></span><span></span>';

        const label = el('span', 'typing-label');
        label.textContent = 'Sphoorthy is typing…';

        const wrap = el('div', 'typing-wrap');
        wrap.append(ind, label);

        row.append(avatar, wrap);
        chatMessages.appendChild(row);
        animIn(row, 'left');
        scroll();
        return id;
    }

    function removeTyping(id) {
        const el = document.getElementById(id);
        if (el) { el.style.opacity = '0'; setTimeout(() => el.remove(), 200); }
    }

    /* ═══════════════ CHIPS ═══════════════ */
    function renderChips(intent) {
        const set = CHIPS[intent] || CHIPS.default;
        suggestionsBar.innerHTML = '';
        set.forEach(label => {
            const c = el('span', 'chip');
            c.textContent = label.replace(/^.\s/, '').replace(/^[^ ]* /, m => m); // keep emoji
            c.textContent = label;
            c.addEventListener('click', () => handleSend(label.replace(/^[^\w]*/, '')));
            suggestionsBar.appendChild(c);
        });
    }
    renderChips('default');

    /* ═══════════════ FORMAT RESPONSE ═══════════════ */
    function formatResponse(raw) {
        if (!raw) return '';
        let out = raw;

        /* Bold */
        out = out.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        /* Italic */
        out = out.replace(/(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)/g, '<em>$1</em>');

        /* Bullets → <ul> */
        const lines = out.split('\n');
        const result = [];
        let inList = false;
        for (const line of lines) {
            const isBullet = /^[•\-]\s+/.test(line.trim());
            if (isBullet) {
                if (!inList) { result.push('<ul class="bot-list">'); inList = true; }
                result.push(`<li>${line.trim().replace(/^[•\-]\s+/, '')}</li>`);
            } else {
                if (inList) { result.push('</ul>'); inList = false; }
                result.push(line.trim() === '' ? '<br>' : line);
            }
        }
        if (inList) result.push('</ul>');

        out = result.join('\n').replace(/\n/g, '<br>').replace(/(<br>\s*){3,}/g, '<br><br>');
        return out;
    }

    /* ═══════════════ RAW INJECT ═══════════════ */
    function injectRaw(html) {
        const wrapper = el('div', 'msg-row bot-row welcome-row');
        wrapper.innerHTML = html;
        chatMessages.appendChild(wrapper);
        animIn(wrapper, 'left');
        scroll();
    }

    /* ═══════════════ HELPERS ═══════════════ */
    function el(tag, cls) {
        const e = document.createElement(tag);
        if (cls) e.className = cls;
        return e;
    }

    function scroll() {
        chatMessages.scrollTo({ top: chatMessages.scrollHeight, behavior: 'smooth' });
    }

    function animIn(node, dir = 'left') {
        const x = dir === 'right' ? '20px' : '-20px';
        node.style.cssText += `opacity:0;transform:translateY(10px) translateX(${x})`;
        requestAnimationFrame(() => requestAnimationFrame(() => {
            node.style.transition = 'opacity 0.3s ease, transform 0.35s cubic-bezier(.22,1,.36,1)';
            node.style.opacity = '1';
            node.style.transform = 'translateY(0) translateX(0)';
        }));
    }

    function timeStr() {
        return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    /* ═══════════════ SCROLL-TO-BOTTOM BTN ═══════════════ */
    const scrollBtn = document.getElementById('scrollDownBtn');
    if (scrollBtn) {
        chatMessages.addEventListener('scroll', () => {
            const atBottom = chatMessages.scrollHeight - chatMessages.scrollTop - chatMessages.clientHeight < 60;
            scrollBtn.classList.toggle('visible', !atBottom);
        });
        scrollBtn.addEventListener('click', scroll);
    }

    /* ═══════════════ INPUT AUTO-RESIZE (textarea feel) ═══ */
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = Math.min(userInput.scrollHeight, 100) + 'px';
    });
});
