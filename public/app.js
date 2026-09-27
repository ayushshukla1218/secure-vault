// app.js — Frontend logic for SecureVault
const API = '/api';
let session = { userId: null, masterPassword: null, username: null };
let allEntries = [];
let viewEntries = [];
let exportPayload = null;
let viewUnlocked = false;

// --- Auth ---
function showTab(tab) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.form-panel').forEach(p => p.classList.add('hidden'));
  event.target.classList.add('active');
  document.getElementById(`${tab}-form`).classList.remove('hidden');
}

async function register() {
  const username = document.getElementById('reg-username').value.trim();
  const password = document.getElementById('reg-password').value;
  const confirm  = document.getElementById('reg-confirm').value;
  const errEl    = document.getElementById('reg-error');
  errEl.textContent = '';
  if (!username || !password) return (errEl.textContent = 'All fields required');
  if (password !== confirm)   return (errEl.textContent = 'Passwords do not match');
  if (password.length < 6)    return (errEl.textContent = 'Password too short (min 6 chars)');
  const res = await post('/register', { username, masterPassword: password });
  if (res.error) return (errEl.textContent = res.error);
  toast('Account created! Please login.', 'success');
  showTab({ target: document.querySelectorAll('.tab')[0] });
}

async function login() {
  const username = document.getElementById('login-username').value.trim();
  const password = document.getElementById('login-password').value;
  const errEl    = document.getElementById('login-error');
  errEl.textContent = '';
  const res = await post('/login', { username, masterPassword: password });
  if (res.error) return (errEl.textContent = res.error);
  session = { userId: res.userId, masterPassword: password, username };
  document.getElementById('nav-username').textContent = username;
  switchScreen('app-screen');
  loadVault();
}

function logout() {
  session = { userId: null, masterPassword: null, username: null };
  allEntries = []; viewEntries = []; exportPayload = null; viewUnlocked = false;
  document.getElementById('login-username').value = '';
  document.getElementById('login-password').value = '';
  document.getElementById('login-error').textContent = '';
  lockView();
  switchScreen('auth-screen');
}

// --- Vault section ---
async function loadVault() {
  const res = await get(`/vault/${session.userId}?masterPassword=${encodeURIComponent(session.masterPassword)}`);
  if (res.error) return toast(res.error, 'error');
  allEntries = res.entries || [];
  renderEntries(allEntries);
}

function renderEntries(entries) {
  const container = document.getElementById('vault-entries');
  if (!entries.length) {
    container.innerHTML = `<div class="empty-state"><div class="icon">🔒</div><p>No passwords saved yet. Add your first one!</p></div>`;
    return;
  }
  container.innerHTML = entries.map(e => `
    <div class="entry-card">
      <div class="entry-card-header">
        <div>
          <div class="entry-site">${esc(e.site)}</div>
          <div class="entry-username">${esc(e.username)}</div>
        </div>
        <span class="entry-badge">AES-256</span>
      </div>
      <div class="entry-password-row">
        <span class="entry-password">••••••••••</span>
      </div>
      <div class="entry-meta">Updated ${formatDate(e.updatedAt)}</div>
      <div class="entry-actions" style="margin-top:10px;display:flex;gap:6px;">
        <button class="btn-secondary" style="padding:6px 10px" onclick="openEditModal('${e.id}','${esc(e.site)}','${esc(e.username)}','${esc(e.password)}')">Edit</button>
        <button class="btn-icon" onclick="deleteEntry('${e.id}')" title="Delete">🗑</button>
      </div>
    </div>
  `).join('');
}

function filterEntries() {
  const q = document.getElementById('search-input').value.toLowerCase();
  renderEntries(allEntries.filter(e => e.site.toLowerCase().includes(q) || e.username.toLowerCase().includes(q)));
}

function togglePassword(id, pw) {
  const el = document.getElementById(`pw-${id}`);
  el.textContent = el.textContent === '••••••••••' ? pw : '••••••••••';
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => toast('Copied!', 'success'));
}

// --- Add / Edit ---
function openAddModal() {
  document.getElementById('modal-title').textContent = 'Add Password';
  ['edit-entry-id','m-site','m-username','m-password'].forEach(id => document.getElementById(id).value = '');
  document.getElementById('modal').classList.remove('hidden');
}

function openEditModal(id, site, username, password) {
  document.getElementById('modal-title').textContent = 'Edit Password';
  document.getElementById('edit-entry-id').value = id;
  document.getElementById('m-site').value = site;
  document.getElementById('m-username').value = username;
  document.getElementById('m-password').value = password;
  document.getElementById('modal').classList.remove('hidden');
}

function closeModal() { document.getElementById('modal').classList.add('hidden'); }

async function saveEntry() {
  const entryId  = document.getElementById('edit-entry-id').value;
  const site     = document.getElementById('m-site').value.trim();
  const username = document.getElementById('m-username').value.trim();
  const password = document.getElementById('m-password').value;
  if (!site || !username || !password) return toast('All fields required', 'error');
  const body = { userId: session.userId, masterPassword: session.masterPassword, site, username, password };
  let res;
  if (entryId) {
    res = await fetchJson(`${API}/vault/${session.userId}/${entryId}`, { method: 'PUT', body: JSON.stringify(body), headers: {'Content-Type':'application/json'} });
  } else {
    res = await post('/vault', body);
  }
  if (res.error) return toast(res.error, 'error');
  toast(entryId ? 'Password updated!' : 'Password saved!', 'success');
  closeModal();
  loadVault();
  if (viewUnlocked) loadViewTable(viewEntries);
}

async function deleteEntry(entryId) {
  if (!confirm('Delete this password?')) return;
  const res = await fetchJson(`${API}/vault/${session.userId}/${entryId}`, {
    method: 'DELETE',
    body: JSON.stringify({ masterPassword: session.masterPassword }),
    headers: {'Content-Type':'application/json'}
  });
  if (res.error) return toast(res.error, 'error');
  toast('Deleted', 'success');
  loadVault();
  if (viewUnlocked) {
    viewEntries = viewEntries.filter(e => e.id !== entryId);
    loadViewTable(viewEntries);
  }
}

function generatePassword() {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
  document.getElementById('m-password').value = Array.from({length:16}, () => chars[Math.floor(Math.random()*chars.length)]).join('');
  document.getElementById('m-password').type = 'text';
}

function toggleModalPass() {
  const el = document.getElementById('m-password');
  el.type = el.type === 'password' ? 'text' : 'password';
}

// --- VIEW SAVED PASSWORDS SECTION ---
async function unlockView() {
  const masterInput = document.getElementById('view-master-input').value;
  const errEl = document.getElementById('view-auth-error');
  errEl.textContent = '';
  if (!masterInput) return (errEl.textContent = 'Enter master password');

  const res = await get(`/vault/${session.userId}?masterPassword=${encodeURIComponent(masterInput)}`);
  if (res.error) return (errEl.textContent = 'Wrong master password');

  viewUnlocked = true;
  viewEntries = res.entries || [];
  document.getElementById('view-auth-gate').classList.add('hidden');
  document.getElementById('view-content').classList.remove('hidden');
  loadViewTable(viewEntries);
  document.getElementById('view-master-input').value = '';
}

function lockView() {
  viewUnlocked = false;
  viewEntries = [];
  document.getElementById('view-auth-gate').classList.remove('hidden');
  document.getElementById('view-content').classList.add('hidden');
  const tbody = document.getElementById('view-table-body');
  if (tbody) tbody.innerHTML = '';
}

function loadViewTable(entries) {
  const tbody = document.getElementById('view-table-body');
  if (!entries.length) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center;padding:30px;color:var(--text-muted);">No passwords saved yet.</td></tr>`;
    return;
  }
  tbody.innerHTML = entries.map((e, i) => `
    <tr>
      <td style="color:var(--text-muted);font-size:12px;">${i+1}</td>
      <td>
        <div style="font-weight:700;color:var(--text);">${esc(e.site)}</div>
      </td>
      <td style="color:var(--text-muted);font-size:13px;">${esc(e.username)}</td>
      <td>
        <div style="display:flex;align-items:center;gap:8px;">
          <span id="vpw-${e.id}" style="font-family:monospace;letter-spacing:3px;font-size:15px;">••••••••</span>
          <button class="btn-icon" onclick="toggleViewPw('${e.id}','${esc(e.password)}')" title="Reveal">👁</button>
          <button class="btn-icon" onclick="copyToClipboard('${esc(e.password)}')" title="Copy">📋</button>
        </div>
      </td>
      <td style="color:var(--text-muted);font-size:12px;">${formatDate(e.updatedAt)}</td>
      <td>
        <button class="btn-secondary" style="padding:4px 10px;font-size:12px;" onclick="openEditModal('${e.id}','${esc(e.site)}','${esc(e.username)}','${esc(e.password)}');showSection('vault')">Edit</button>
      </td>
    </tr>
  `).join('');
}

function toggleViewPw(id, pw) {
  const el = document.getElementById(`vpw-${id}`);
  el.textContent = el.textContent === '••••••••' ? pw : '••••••••';
  el.style.letterSpacing = el.textContent === '••••••••' ? '3px' : '0';
}

function filterView() {
  const q = document.getElementById('view-search').value.toLowerCase();
  loadViewTable(viewEntries.filter(e => e.site.toLowerCase().includes(q) || e.username.toLowerCase().includes(q)));
}

// --- Export — opens its own modal, completely separate from View section ---
async function exportPasswords() {
  const res = await post('/export', { userId: session.userId, masterPassword: session.masterPassword });
  if (res.error) return toast(res.error, 'error');
  exportPayload = res;

  const badge = document.getElementById('export-sig-badge');
  badge.textContent = res.verified ? '✓ Digitally Signed & Verified (RSA-2048)' : '⚠ Signature Unverified';
  badge.className = `export-status ${res.verified ? 'verified' : 'unverified'}`;

  const grid = document.getElementById('export-preview-grid');
  grid.innerHTML = res.data.map((d, i) => `
    <div class="epg-row">
      <span class="epg-num">${i+1}</span>
      <span class="epg-site">${esc(d.site)}</span>
      <span class="epg-user">${esc(d.username)}</span>
      <span class="epg-signed">${res.verified ? '✓ Digitally Signed' : '⚠ Unverified'}</span>
    </div>
  `).join('');

  document.getElementById('export-sig-short').textContent = res.signature.substring(0, 80) + '…';
  document.getElementById('export-modal').classList.remove('hidden');
}

function closeExportModal() {
  document.getElementById('export-modal').classList.add('hidden');
}

function downloadExport() {
  if (!exportPayload) return;
  const blob = new Blob([JSON.stringify(exportPayload, null, 2)], { type: 'application/json' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'vault-export.json'; a.click();
}

// --- Audit Log ---
async function loadAudit() {
  const res = await get(`/audit/${session.userId}?masterPassword=${encodeURIComponent(session.masterPassword)}`);
  if (res.error) return toast(res.error, 'error');
  const badge = document.getElementById('chain-status');
  badge.textContent = res.chainIntegrity ? '✓ Chain Intact' : '⚠ Chain Tampered!';
  badge.className = `chain-badge ${res.chainIntegrity ? 'valid' : 'invalid'}`;
  const container = document.getElementById('audit-entries');
  container.innerHTML = `
    <div class="audit-row header"><span>#</span><span>Timestamp</span><span>Event</span><span>Detail</span><span>Block Hash</span></div>
    ${res.logs.map(l => `
      <div class="audit-row">
        <span>${l.index}</span>
        <span>${formatDate(l.timestamp)}</span>
        <span class="audit-event">${l.event}</span>
        <span>${esc(l.detail)}</span>
        <span class="audit-hash">${l.hash.substring(0,12)}…</span>
      </div>
    `).join('')}
  `;
}

// --- Nav ---
function showSection(name) {
  document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(`${name}-section`).classList.remove('hidden');
  const navBtn = document.getElementById(`nav-${name}`);
  if (navBtn) navBtn.classList.add('active');
  if (name === 'audit') loadAudit();
  if (name === 'vault') loadVault();
}

function switchScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

// --- Helpers ---
async function post(path, data) {
  return fetchJson(`${API}${path}`, { method:'POST', body:JSON.stringify(data), headers:{'Content-Type':'application/json'} });
}
async function get(path) { return fetchJson(`${API}${path}`); }
async function fetchJson(url, opts = {}) {
  try { const r = await fetch(url, opts); return await r.json(); }
  catch (e) { return { error: e.message }; }
}
function esc(str) {
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}
function formatDate(iso) { return new Date(iso).toLocaleString(); }
function toast(msg, type = 'success') {
  const el = document.createElement('div');
  el.className = `toast ${type}`; el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 3000);
}
