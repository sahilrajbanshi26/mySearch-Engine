/**
 * app.js — LaptopSearchEngine frontend
 *
 * All communication with Flask uses the Fetch API:
 *   fetch("/api/route", { method, headers, body })
 *   → the Flask route runs scanner.py → returns JSON
 *   → we build HTML from the JSON and inject it into the page
 */

"use strict";

// ─────────────────────────────────────────────────────
//  BOOT — load header info when page opens
// ─────────────────────────────────────────────────────

window.addEventListener("DOMContentLoaded", () => {
  loadHeaderInfo();
  loadSysInfoTab();
  initTabs();
});

async function loadHeaderInfo() {
  try {
    // 1. current working directory
    const locRes  = await fetch("/api/location");
    const locData = await locRes.json();
    if (locData.success) {
      document.getElementById("pill-cwd").textContent = "📁 " + locData.path;
    }

    // 2. OS + user from sysinfo
    const sysRes  = await fetch("/api/sysinfo");
    const sysData = await sysRes.json();
    if (sysData.success) {
      document.getElementById("pill-os").textContent   = "💻 " + sysData.info["OS type"];
      document.getElementById("pill-user").textContent = "👤 " + sysData.info["Username"];
    }
  } catch (_) { /* header pills fail silently */ }
}

async function loadSysInfoTab() {
  try {
    const res  = await fetch("/api/sysinfo");
    const data = await res.json();
    const el   = document.getElementById("sysinfo-result");

    if (!data.success) { el.innerHTML = errorHTML(data.error); el.classList.remove("hidden"); return; }

    const rows = Object.entries(data.info)
      .map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`)
      .join("");

    el.innerHTML = `
      <div class="info-wrapper">
        <table class="info-table"><tbody>${rows}</tbody></table>
      </div>`;
    el.classList.remove("hidden");
  } catch (e) {
    showError("sysinfo-result", e.message);
  }
}


// ─────────────────────────────────────────────────────
//  TAB SWITCHING
// ─────────────────────────────────────────────────────

function initTabs() {
  document.querySelectorAll(".tab-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById("tab-" + btn.dataset.tab).classList.add("active");
    });
  });
}


// ─────────────────────────────────────────────────────
//  ACTION — Browse Folder  →  POST /api/list
// ─────────────────────────────────────────────────────

async function doList() {
  const path = document.getElementById("list-path").value.trim();
  if (!path) { alert("Please enter a folder path."); return; }

  showLoading(true);

  try {
    /* ── FETCH — send path to Flask ── */
    const res  = await fetch("/api/list", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ path })
    });
    const data = await res.json();
    showLoading(false);

    const el = document.getElementById("list-result");

    if (!data.success) { el.innerHTML = errorHTML(data.error); el.classList.remove("hidden"); return; }

    const total = data.files.length + data.folders.length;

    if (total === 0) {
      el.innerHTML = emptyHTML("Folder is empty.");
      el.classList.remove("hidden");
      return;
    }

    /* ── BUILD HTML from the JSON response ── */
    let html = `<div class="result-stat">
      <span class="count-badge">${total}</span>
      <span>items found in <code>${path}</code></span>
    </div>`;

    if (data.folders.length) {
      html += `<p class="result-section-title">📁 Folders (${data.folders.length})</p>`;
      html += `<div class="cards-grid">`;
      data.folders.forEach(f => {
        html += card("📁", f.name, f.full, "");
      });
      html += `</div>`;
    }

    if (data.files.length) {
      html += `<p class="result-section-title">📄 Files (${data.files.length})</p>`;
      html += `<div class="cards-grid">`;
      data.files.forEach(f => {
        html += card(fileIcon(f.name), f.name, f.full, "");
      });
      html += `</div>`;
    }

    el.innerHTML = html;
    el.classList.remove("hidden");

  } catch (e) {
    showLoading(false);
    showError("list-result", e.message);
  }
}


// ─────────────────────────────────────────────────────
//  ACTION — Search by Name  →  POST /api/search/name
// ─────────────────────────────────────────────────────

async function doSearchName() {
  const path    = document.getElementById("name-path").value.trim();
  const keyword = document.getElementById("name-keyword").value.trim();
  if (!path || !keyword) { alert("Please fill in both the folder path and keyword."); return; }

  showLoading(true);

  try {
    const res  = await fetch("/api/search/name", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ path, keyword })
    });
    const data = await res.json();
    showLoading(false);

    const el = document.getElementById("name-result");

    if (!data.success) { el.innerHTML = errorHTML(data.error); el.classList.remove("hidden"); return; }

    el.innerHTML = buildFileResults(data.results, `"${keyword}"`, path);
    el.classList.remove("hidden");

  } catch (e) {
    showLoading(false);
    showError("name-result", e.message);
  }
}


// ─────────────────────────────────────────────────────
//  ACTION — Search by Extension  →  POST /api/search/extension
// ─────────────────────────────────────────────────────

async function doSearchExt() {
  const path = document.getElementById("ext-path").value.trim();
  const ext  = document.getElementById("ext-keyword").value.trim();
  if (!path || !ext) { alert("Please fill in both the folder path and extension."); return; }

  showLoading(true);

  try {
    const res  = await fetch("/api/search/extension", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ path, extension: ext })
    });
    const data = await res.json();
    showLoading(false);

    const el = document.getElementById("ext-result");

    if (!data.success) { el.innerHTML = errorHTML(data.error); el.classList.remove("hidden"); return; }

    el.innerHTML = buildFileResults(data.results, `.${ext.replace(".", "")}`, path);
    el.classList.remove("hidden");

  } catch (e) {
    showLoading(false);
    showError("ext-result", e.message);
  }
}


// ─────────────────────────────────────────────────────
//  HELPERS — HTML builders
// ─────────────────────────────────────────────────────

function buildFileResults(results, label, path) {
  if (!results.length) return emptyHTML(`No files matching ${label} were found.`);

  let html = `<div class="result-stat">
    <span class="count-badge">${results.length}</span>
    <span>files matching <code>${label}</code> inside <code>${path}</code></span>
  </div>
  <div class="cards-grid">`;

  results.forEach(r => {
    html += card(fileIcon(r.name), r.name, r.path, r.size);
  });

  html += `</div>`;
  return html;
}

function card(icon, name, path, size) {
  return `
  <div class="card">
    <span class="card-icon">${icon}</span>
    <div class="card-body">
      <div class="card-name" title="${name}">${name}</div>
      <div class="card-path" title="${path}">${path}</div>
      ${size ? `<div class="card-size">${size}</div>` : ""}
    </div>
  </div>`;
}

function errorHTML(msg) {
  return `<div class="state-error"><span>⚠</span><span>${msg}</span></div>`;
}

function emptyHTML(msg) {
  return `<div class="state-empty"><span class="empty-icon">🔍</span>${msg}</div>`;
}

function showError(id, msg) {
  const el = document.getElementById(id);
  el.innerHTML = errorHTML(msg);
  el.classList.remove("hidden");
}

function showLoading(on) {
  document.getElementById("loading").classList.toggle("hidden", !on);
}

/** Pick a fitting emoji icon based on file extension */
function fileIcon(name) {
  const ext = name.split(".").pop().toLowerCase();
  const map = {
    pdf: "📕", doc: "📝", docx: "📝", txt: "📃", md: "📃",
    jpg: "🖼", jpeg: "🖼", png: "🖼", gif: "🖼", svg: "🖼",
    mp3: "🎵", wav: "🎵", mp4: "🎬", mkv: "🎬",
    zip: "🗜", tar: "🗜", gz: "🗜",
    py:  "🐍", js: "📜", html: "🌐", css: "🎨",
    json: "🔧", xml: "🔧", csv: "📊", xlsx: "📊",
  };
  return map[ext] || "📄";
}

// ── Allow pressing Enter in input fields ──────────────
document.addEventListener("keydown", e => {
  if (e.key !== "Enter") return;
  const tab = document.querySelector(".tab-panel.active");
  if (!tab) return;
  if (tab.id === "tab-list")      doList();
  if (tab.id === "tab-name")      doSearchName();
  if (tab.id === "tab-extension") doSearchExt();
});