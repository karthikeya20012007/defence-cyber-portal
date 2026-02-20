/* ============================================================
   CERT-Army Cyber Portal — Main JavaScript
   Handles: form validation, sidebar toggle, toast alerts,
            file upload UI, clock
   ============================================================ */

/* ── 1. Run after page is fully loaded ─────────────────────── */
document.addEventListener('DOMContentLoaded', function () {

    initClock();          // live clock in topbar
    initSidebar();        // mobile hamburger toggle
    initLoginForm();      // login page validation
    initReportForm();     // report page validation
    initFileUpload();     // drag/click file upload area
    initAlertDismiss();   // close alert cards

});

/* ══════════════════════════════════════════════════════════════
   2. LIVE CLOCK
   Updates the element with id="live-clock" every second
══════════════════════════════════════════════════════════════ */
function initClock() {
    const clockEl = document.getElementById('live-clock');
    if (!clockEl) return; // not on this page

    function tick() {
        const now = new Date();
        const hh = String(now.getHours()).padStart(2, '0');
        const mm = String(now.getMinutes()).padStart(2, '0');
        const ss = String(now.getSeconds()).padStart(2, '0');
        clockEl.textContent = hh + ':' + mm + ':' + ss + ' IST';
    }

    tick();                      // run immediately
    setInterval(tick, 1000);     // then every second
}

/* ══════════════════════════════════════════════════════════════
   3. SIDEBAR TOGGLE (mobile hamburger)
   Clicking the hamburger button opens/closes the sidebar
══════════════════════════════════════════════════════════════ */
function initSidebar() {
    const hamburger = document.getElementById('hamburger-btn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    if (!hamburger || !sidebar) return;

    // Open sidebar
    hamburger.addEventListener('click', function () {
        sidebar.classList.add('open');
        if (overlay) overlay.classList.add('show');
    });

    // Close sidebar when clicking the overlay behind it
    if (overlay) {
        overlay.addEventListener('click', function () {
            sidebar.classList.remove('open');
            overlay.classList.remove('show');
        });
    }
}

/* ══════════════════════════════════════════════════════════════
   4. LOGIN FORM VALIDATION
   Checks username and password before submitting
══════════════════════════════════════════════════════════════ */
function initLoginForm() {
    const form = document.getElementById('login-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault(); // stop normal form submit

        let valid = true;

        // --- Validate Username ---
        const username = document.getElementById('username');
        const userErr = document.getElementById('username-error');

        if (username.value.trim() === '') {
            showFieldError(userErr, 'Username is required.');
            valid = false;
        } else {
            hideFieldError(userErr);
        }

        // --- Validate Password ---
        const password = document.getElementById('password');
        const passErr = document.getElementById('password-error');

        if (password.value.trim() === '') {
            showFieldError(passErr, 'Password is required.');
            valid = false;
        } else if (password.value.length < 6) {
            showFieldError(passErr, 'Password must be at least 6 characters.');
            valid = false;
        } else {
            hideFieldError(passErr);
        }

        // --- If all valid, submit (or redirect in Django) ---
        if (valid) {
            showToast('success', '🔐 Authenticating…', 'Redirecting to dashboard.');
            // In real Django this would be: form.submit()
            setTimeout(() => {
                window.location.href = '/dashboard/'; // Django URL
            }, 1500);
        }
    });
}

/* ══════════════════════════════════════════════════════════════
   5. REPORT INCIDENT FORM VALIDATION
   Validates title, description, and incident type
══════════════════════════════════════════════════════════════ */
function initReportForm() {
    const form = document.getElementById('report-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        let valid = true;

        // Title
        const title = document.getElementById('inc-title');
        const titleErr = document.getElementById('title-error');
        if (title.value.trim() === '') {
            showFieldError(titleErr, 'Incident title is required.');
            valid = false;
        } else if (title.value.trim().length < 5) {
            showFieldError(titleErr, 'Title must be at least 5 characters.');
            valid = false;
        } else {
            hideFieldError(titleErr);
        }

        // Description
        const desc = document.getElementById('inc-desc');
        const descErr = document.getElementById('desc-error');
        if (desc.value.trim() === '') {
            showFieldError(descErr, 'Description is required.');
            valid = false;
        } else if (desc.value.trim().split(' ').length < 5) {
            showFieldError(descErr, 'Please provide at least 5 words.');
            valid = false;
        } else {
            hideFieldError(descErr);
        }

        // Incident Type
        const type = document.getElementById('inc-type');
        const typeErr = document.getElementById('type-error');
        if (!type.value) {
            showFieldError(typeErr, 'Please select an incident type.');
            valid = false;
        } else {
            hideFieldError(typeErr);
        }

        if (valid) {
            showToast('success', '✅ Report Submitted', 'Your incident has been logged.');
            // In Django: form.submit();
            setTimeout(() => form.reset(), 2000);
        }
    });
}

/* ══════════════════════════════════════════════════════════════
   6. FILE UPLOAD — click area or drag
══════════════════════════════════════════════════════════════ */
function initFileUpload() {
    const area = document.getElementById('upload-area');
    const fileInput = document.getElementById('evidence-file');
    const fileLabel = document.getElementById('file-label');

    if (!area || !fileInput) return;

    // Clicking the area opens the file picker
    area.addEventListener('click', () => fileInput.click());

    // When user picks a file, show its name
    fileInput.addEventListener('change', function () {
        if (this.files.length > 0) {
            const names = Array.from(this.files).map(f => f.name).join(', ');
            if (fileLabel) fileLabel.textContent = '📎 ' + names;
            area.style.borderColor = 'var(--green)';
        }
    });

    // Drag-over highlight
    area.addEventListener('dragover', function (e) {
        e.preventDefault();
        area.style.borderColor = 'var(--accent)';
        area.style.background = 'rgba(0,170,255,0.07)';
    });

    area.addEventListener('dragleave', function () {
        area.style.borderColor = '';
        area.style.background = '';
    });

    // Drop a file
    area.addEventListener('drop', function (e) {
        e.preventDefault();
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            const names = Array.from(files).map(f => f.name).join(', ');
            if (fileLabel) fileLabel.textContent = '📎 ' + names;
            area.style.borderColor = 'var(--green)';
            area.style.background = '';
        }
    });
}

/* ══════════════════════════════════════════════════════════════
   7. ALERT CARD DISMISS
   Clicking × on an alert card fades it out
══════════════════════════════════════════════════════════════ */
function initAlertDismiss() {
    // Use event delegation so dynamically added cards also work
    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('dismiss-btn')) {
            const card = e.target.closest('.alert-card');
            if (card) {
                card.style.transition = 'opacity 0.3s, transform 0.3s';
                card.style.opacity = '0';
                card.style.transform = 'translateX(20px)';
                setTimeout(() => card.remove(), 350);
            }
        }
    });
}

/* ══════════════════════════════════════════════════════════════
   8. TOAST NOTIFICATION HELPER
   Call: showToast('success'|'error'|'info', title, subtitle)
══════════════════════════════════════════════════════════════ */
function showToast(type, title, subtitle) {
    // Remove any existing toast first
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const icons = { success: '✅', error: '❌', info: 'ℹ️' };

    const toast = document.createElement('div');
    toast.className = 'toast ' + type;
    toast.innerHTML = `
    <span class="toast-icon">${icons[type] || 'ℹ️'}</span>
    <div class="toast-msg">
      ${title}
      <small>${subtitle || ''}</small>
    </div>
  `;

    document.body.appendChild(toast);

    // Trigger animation on next frame
    requestAnimationFrame(() => {
        requestAnimationFrame(() => toast.classList.add('show'));
    });

    // Auto-remove after 3.5 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 350);
    }, 3500);
}

/* ══════════════════════════════════════════════════════════════
   9. HELPER: Show / Hide inline field errors
══════════════════════════════════════════════════════════════ */
function showFieldError(el, msg) {
    if (!el) return;
    el.textContent = msg;
    el.style.display = 'block';
}

function hideFieldError(el) {
    if (!el) return;
    el.textContent = '';
    el.style.display = 'none';
}

/* ══════════════════════════════════════════════════════════════
   10. PUBLIC helper — pages can call showToast() from buttons
   e.g. onclick="showToast('info','Title','Sub')"
══════════════════════════════════════════════════════════════ */
window.showToast = showToast;
