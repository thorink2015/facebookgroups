/* Tank Mix Campaign Dashboard — frontend logic (vanilla JS, no build step) */

// ---- tiny helpers --------------------------------------------------------
const $ = (sel, root = document) => root.querySelector(sel);
const view = $("#view");

async function api(path, opts = {}) {
  const res = await fetch(path, opts);
  let data = null;
  try { data = await res.json(); } catch (e) {}
  if (!res.ok) throw new Error((data && data.error) || res.statusText);
  return data;
}
const getJSON = (p) => api(p);
const postJSON = (p, body) => api(p, {
  method: "POST", headers: { "Content-Type": "application/json" },
  body: JSON.stringify(body || {}),
});
const patchJSON = (p, body) => api(p, {
  method: "PATCH", headers: { "Content-Type": "application/json" },
  body: JSON.stringify(body || {}),
});
const del = (p) => api(p, { method: "DELETE" });

function esc(s) {
  return (s == null ? "" : String(s)).replace(/[&<>"']/g, c =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function fmtDate(s) {
  if (!s) return "—";
  return String(s).replace("T", " ").slice(0, 16);
}
function toast(msg, isErr = false) {
  const t = $("#toast");
  t.textContent = msg;
  t.className = "toast show" + (isErr ? " err" : "");
  setTimeout(() => (t.className = "toast"), 2600);
}
async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    toast("Copied to clipboard");
  } catch (e) {
    const ta = document.createElement("textarea");
    ta.value = text; document.body.appendChild(ta); ta.select();
    document.execCommand("copy"); ta.remove();
    toast("Copied to clipboard");
  }
}
function openModal(title, html) {
  $("#modal-title").textContent = title;
  $("#modal-body").innerHTML = html;
  $("#modal-backdrop").classList.remove("hidden");
}
function closeModal() { $("#modal-backdrop").classList.add("hidden"); }
window.closeModal = closeModal;

const TITLES = {
  overview: ["Overview", "Your campaign at a glance"],
  queue: ["Daily Queue", "Generate non-duplicate posts, then post them by hand"],
  groups: ["Groups", "Your Facebook groups and where you've posted"],
  templates: ["Templates", "Your post copy — 8 templates, rotated hook variants"],
  images: ["Images", "Upload and tag the images you rotate through"],
  history: ["History", "Every post you've logged"],
  settings: ["Settings", "Cadence guardrails and your newsletter link"],
  logs: ["Activity Log", "What the dashboard recorded, plus your own notes"],
};

// ---- router --------------------------------------------------------------
const RENDER = {
  overview: renderOverview, queue: renderQueue, groups: renderGroups,
  templates: renderTemplates, images: renderImages, history: renderHistory,
  settings: renderSettings, logs: renderLogs,
};
function go(name) {
  document.querySelectorAll(".nav-item").forEach(b =>
    b.classList.toggle("active", b.dataset.view === name));
  $("#view-title").textContent = TITLES[name][0];
  $("#view-sub").textContent = TITLES[name][1];
  view.innerHTML = '<div class="empty">Loading…</div>';
  RENDER[name]().catch(e => {
    view.innerHTML = `<div class="callout warn">Error: ${esc(e.message)}</div>`;
  });
}
document.querySelectorAll(".nav-item").forEach(b =>
  b.addEventListener("click", () => go(b.dataset.view)));

// ---- OVERVIEW ------------------------------------------------------------
async function renderOverview() {
  const o = await getJSON("/api/overview");
  // status pill
  const pill = $("#status-pill");
  if (o.cadence === "high") { pill.className = "pill pill-warn"; pill.textContent = "high volume"; }
  else if (o.planned > 0) { pill.className = "pill pill-ready"; pill.textContent = `${o.planned} queued`; }
  else { pill.className = "pill pill-idle"; pill.textContent = "idle"; }

  let nextStep = "";
  if (o.groups_total === 0) nextStep = `Start by importing your groups CSV in the <b>Groups</b> tab.`;
  else if (o.variants === 0) nextStep = `Add some copy in the <b>Templates</b> tab.`;
  else if (o.images === 0) nextStep = `Upload at least one image in the <b>Images</b> tab.`;
  else if (o.planned === 0) nextStep = `Go to <b>Daily Queue</b> and click <b>Generate</b> to build tonight's posts.`;
  else nextStep = `You have <b>${o.planned}</b> posts queued. Open <b>Daily Queue</b> and start posting.`;

  let cadenceNote = "";
  if (o.cadence === "high")
    cadenceNote = `<div class="callout warn">⚠️ You've logged <b>${o.posts_today}</b> posts today — above your high-volume line (${o.high_volume_warn}). Your playbook favors slow and varied. Consider stopping for today.</div>`;
  else if (o.cadence === "at_cap")
    cadenceNote = `<div class="callout warn">You're at your daily cap (${o.daily_cap}). You can keep going, but this is the gentle nudge to wrap up.</div>`;

  const cards = [
    ["Posted today", o.posts_today, `cap ${o.daily_cap}`],
    ["This week", o.posts_week, "last 7 days"],
    ["In queue", o.planned, "ready to post"],
    ["Groups covered", `${o.groups_covered}/${o.groups_total}`, `${o.groups_remaining} to go`],
    ["Active images", o.images, "rotation pool"],
    ["Copy variants", o.variants, `${o.templates} templates`],
  ].map(([l, v, h]) => `<div class="card stat"><div class="label">${l}</div><div class="value">${v}</div><div class="hint">${h}</div></div>`).join("");

  const recent = o.recent.length ? o.recent.map(r => `
    <tr>
      <td>${fmtDate(r.posted_at)}</td>
      <td>${esc(r.group_name || r.group_url || "—")}</td>
      <td><span class="badge cat">${esc(r.category || "—")}</span></td>
      <td>${esc(r.template_code || "—")}</td>
      <td><span class="badge ${r.status}">${r.status}</span></td>
      <td>${r.post_url ? `<a href="${esc(r.post_url)}" target="_blank">view</a>` : "—"}</td>
    </tr>`).join("") : `<tr><td colspan="6" class="muted">No activity yet.</td></tr>`;

  const cats = o.by_category.length ? o.by_category.map(c => `
    <tr><td><span class="badge cat">${esc(c.category)}</span></td>
        <td>${c.covered || 0}/${c.total}</td>
        <td><div class="progress"><div style="width:${Math.round(100*(c.covered||0)/Math.max(1,c.total))}%"></div></div></td>
    </tr>`).join("") : `<tr><td colspan="3" class="muted">No groups yet.</td></tr>`;

  view.innerHTML = `
    <div class="callout info">👉 <b>Next:</b> ${nextStep}</div>
    ${cadenceNote}
    <div class="grid cards">${cards}</div>
    <div class="section">
      <h2>Recent activity</h2>
      <table><thead><tr><th>When</th><th>Group</th><th>Category</th><th>Template</th><th>Status</th><th>Link</th></tr></thead>
      <tbody>${recent}</tbody></table>
    </div>
    <div class="section">
      <h2>Coverage by category</h2>
      <p class="sec-sub">How many groups in each category you've posted to at least once.</p>
      <table><thead><tr><th>Category</th><th>Covered</th><th></th></tr></thead><tbody>${cats}</tbody></table>
    </div>`;
}

// ---- DAILY QUEUE ---------------------------------------------------------
let SETTINGS_CACHE = {};
async function renderQueue() {
  const [items, settings] = await Promise.all([getJSON("/api/queue"), getJSON("/api/settings")]);
  SETTINGS_CACHE = settings;
  const target = settings.session_target || "5";
  const link = settings.newsletter_link || "";
  const fcTemplate = settings.first_comment_text || "{link}";

  const controls = `
    <div class="section">
      <div class="row between">
        <div class="row">
          <label class="field" style="margin:0;"><span>How many to generate</span>
            <input type="number" id="gen-count" value="${esc(target)}" min="1" style="width:90px;"></label>
          <button class="btn primary" onclick="doGenerate()">⚡ Generate queue</button>
          <button class="btn ghost" onclick="clearQueue()">Clear queue</button>
        </div>
        <div class="muted">${items.length} planned</div>
      </div>
      ${link ? "" : `<div class="callout warn" style="margin-top:12px;margin-bottom:0;">No newsletter link set yet. Add it in <b>Settings</b> so the "first comment" text fills in automatically.</div>`}
    </div>`;

  if (!items.length) {
    view.innerHTML = controls + `<div class="empty"><div class="big">🌱</div>
      <p>No posts queued. Click <b>Generate queue</b> to build a fresh, non-duplicate batch.</p></div>`;
    return;
  }

  // Same for every item (one template + one link), so compute once and copy via a
  // function — never inline the raw string into an onclick attribute.
  const firstComment = fcTemplate.replace("{link}", link || "[set your link in Settings]");
  window.__firstComment = firstComment;

  const cards = items.map(it => {
    const img = it.image_filename
      ? `<img class="qimg" src="/images/${encodeURIComponent(it.image_filename)}" title="${esc(it.image_type||"")}">`
      : `<div class="qimg placeholder">no image<br>matched</div>`;
    const flag = it.red_flag
      ? `<div class="callout warn" style="margin:0 0 12px;">⚠️ Pre-flight: ${esc(it.red_flag)}</div>` : "";
    const pitch = it.pitch_angle
      ? `<div class="muted" style="font-size:12.5px;margin-top:3px;">🎯 ${esc(it.pitch_angle)}</div>` : "";
    const tierBadge = it.tier ? `<span class="badge gray">tier ${esc(it.tier)}</span>` : "";
    const kw = it.group_keyword || it.template_keyword || "";
    return `
    <div class="qcard" id="q-${it.id}">
      ${flag}
      <div class="qhead">
        <div>
          <b>${esc(it.group_name || it.group_url)}</b>
          <span class="badge cat">${esc(it.category || "—")}</span>
          <span class="badge gray">${esc(it.template_code || "—")}</span>
          ${tierBadge}
          ${pitch}
        </div>
        <a class="btn sm" href="${esc(it.group_url)}" target="_blank">Open group ↗</a>
      </div>
      <div class="qbody">
        <div>
          ${img}
          ${it.image_filename ? `<a class="btn sm ghost" style="margin-top:8px;width:100%;justify-content:center;" href="/images/${encodeURIComponent(it.image_filename)}" download>⬇ Save image</a>` : ""}
        </div>
        <div>
          <textarea id="copy-${it.id}" onblur="saveCopy(${it.id})">${esc(it.copy_text || "")}</textarea>
          <div class="first-comment">💬 <b>Link drop</b> — keep it out of the post body.${kw ? ` When someone comments <b>"${esc(kw)}"</b>, reply + DM them:` : " Reply / DM commenters with:"} ${esc(firstComment)}</div>
          <div class="qactions">
            <button class="btn sm primary" onclick="copyOnly(${it.id})">📋 Copy post text</button>
            <button class="btn sm" onclick="copyFirstComment()">📋 Copy first comment</button>
            <button class="btn sm" onclick="markPosted(${it.id})">✅ Mark posted</button>
            <button class="btn sm ghost" onclick="regen(${it.id})">🔄 Regenerate</button>
            <button class="btn sm ghost" onclick="skipItem(${it.id})">Skip</button>
            <button class="btn sm danger" onclick="dropItem(${it.id})">Delete</button>
          </div>
        </div>
      </div>
    </div>`;
  }).join("");

  view.innerHTML = controls + `<div style="margin-top:18px;">${cards}</div>`;
}
window.copyOnly = (id) => copyText($(`#copy-${id}`).value);
window.copyFirstComment = () => copyText(window.__firstComment || "");
window.saveCopy = (id) => patchJSON(`/api/posts/${id}`, { copy_text: $(`#copy-${id}`).value });
window.doGenerate = async () => {
  const n = parseInt($("#gen-count").value, 10) || 5;
  try {
    const r = await postJSON("/api/queue/generate", { count: n });
    if (r.created) toast(`Generated ${r.created} post${r.created > 1 ? "s" : ""}`);
    (r.warnings || []).forEach(w => toast(w, true));
    renderQueue();
  } catch (e) { toast(e.message, true); }
};
window.clearQueue = async () => {
  if (!confirm("Clear all planned posts in the queue?")) return;
  await postJSON("/api/queue/clear"); toast("Queue cleared"); renderQueue();
};
window.regen = async (id) => { await postJSON(`/api/posts/${id}/regenerate`); toast("Regenerated"); renderQueue(); };
window.skipItem = async (id) => { await postJSON(`/api/posts/${id}/status`, { status: "skipped" }); toast("Skipped"); renderQueue(); };
window.dropItem = async (id) => { await del(`/api/posts/${id}`); renderQueue(); };
window.markPosted = (id) => {
  openModal("Mark as posted", `
    <label class="field"><span>Post URL (optional but handy)</span>
      <input type="url" id="mp-url" placeholder="https://www.facebook.com/groups/.../posts/..."></label>
    <label class="field"><span><input type="checkbox" id="mp-comment"> I added the newsletter link as the first comment</span></label>
    <label class="field"><span>Notes (optional)</span><textarea id="mp-notes"></textarea></label>
    <div class="row"><button class="btn primary" onclick="confirmPosted(${id})">Save</button>
    <button class="btn ghost" onclick="closeModal()">Cancel</button></div>`);
};
window.confirmPosted = async (id) => {
  await postJSON(`/api/posts/${id}/status`, {
    status: "posted",
    post_url: $("#mp-url").value,
    link_in_comment: $("#mp-comment").checked,
    notes: $("#mp-notes").value,
  });
  closeModal(); toast("Logged as posted ✅"); renderQueue();
};

// ---- GROUPS --------------------------------------------------------------
async function renderGroups() {
  const groups = await getJSON("/api/groups");
  const cats = [...new Set(groups.map(g => g.category))].sort();
  const catOpts = cats.map(c => `<option value="${esc(c)}">${esc(c)}</option>`).join("");

  const controls = `
    <div class="section">
      <div class="row between">
        <div class="row">
          <input type="text" id="grp-search" placeholder="Search groups…" style="width:220px;" oninput="filterGroups()">
          <select id="grp-cat" onchange="filterGroups()" style="width:170px;"><option value="">All categories</option>${catOpts}</select>
        </div>
        <div class="row">
          <button class="btn" onclick="addGroupModal()">+ Add group</button>
          <label class="btn primary" style="cursor:pointer;">⬆ Import CSV
            <input type="file" accept=".csv" style="display:none;" onchange="importCsv(this)"></label>
        </div>
      </div>
      <p class="sec-sub" style="margin:12px 0 0;">CSV columns (any order): <code class="inline">url</code>, <code class="inline">name</code>, <code class="inline">category</code>, <code class="inline">notes</code>. Importing never deletes — it only adds new groups.</p>
    </div>`;

  if (!groups.length) {
    view.innerHTML = controls + `<div class="empty"><div class="big">👥</div>
      <p>No groups yet. Import your CSV (drop it on the <b>Import CSV</b> button) or add one manually.</p></div>`;
    return;
  }
  view.innerHTML = controls + `<div class="section"><table id="grp-table">
    <thead><tr><th>Name</th><th>Category</th><th>Last posted</th><th>Posts</th><th>Link</th><th></th></tr></thead>
    <tbody>${groupRows(groups)}</tbody></table></div>`;
  window._groups = groups;
}
function groupRows(groups) {
  return groups.map(g => `
    <tr data-name="${esc((g.name||"").toLowerCase())} ${esc((g.url||"").toLowerCase())} ${esc((g.category||"").toLowerCase())}" data-cat="${esc(g.category||"")}">
      <td>${esc(g.name || "(unnamed)")}</td>
      <td><span class="badge cat">${esc(g.category||"—")}</span>${g.tier?` <span class="badge gray">${esc(g.tier)}</span>`:""}${g.active?"":' <span class="badge gray">off</span>'}</td>
      <td>${fmtDate(g.last_posted)}</td>
      <td>${g.post_count || 0}</td>
      <td><a href="${esc(g.url)}" target="_blank">open ↗</a></td>
      <td><button class="icon-btn" title="Edit" onclick="editGroupModal(${g.id})">✏️</button>
          <button class="icon-btn" title="Delete" onclick="deleteGroup(${g.id})">🗑️</button></td>
    </tr>`).join("");
}
window.filterGroups = () => {
  const q = $("#grp-search").value.toLowerCase();
  const cat = $("#grp-cat").value;
  document.querySelectorAll("#grp-table tbody tr").forEach(tr => {
    const okQ = !q || tr.dataset.name.includes(q);
    const okC = !cat || tr.dataset.cat === cat;
    tr.style.display = (okQ && okC) ? "" : "none";
  });
};
window.importCsv = async (input) => {
  if (!input.files.length) return;
  const fd = new FormData(); fd.append("file", input.files[0]);
  try {
    const r = await api("/api/groups/import", { method: "POST", body: fd });
    toast(`Imported ${r.added} groups · ${r.active_added} active · ${r.skipped} skipped`);
    renderGroups();
  } catch (e) { toast(e.message, true); }
  input.value = "";
};
window.addGroupModal = () => openModal("Add group", `
  <label class="field"><span>Group URL *</span><input type="url" id="g-url" placeholder="https://www.facebook.com/groups/..."></label>
  <label class="field"><span>Name</span><input type="text" id="g-name"></label>
  <label class="field"><span>Category</span><input type="text" id="g-cat" placeholder="operators / farmer_operators / drone_curious / specialty"></label>
  <label class="field"><span>Notes</span><textarea id="g-notes"></textarea></label>
  <div class="row"><button class="btn primary" onclick="saveNewGroup()">Add</button><button class="btn ghost" onclick="closeModal()">Cancel</button></div>`);
window.saveNewGroup = async () => {
  try {
    await postJSON("/api/groups", { url: $("#g-url").value, name: $("#g-name").value, category: $("#g-cat").value, notes: $("#g-notes").value });
    closeModal(); toast("Group added"); renderGroups();
  } catch (e) { toast(e.message, true); }
};
window.editGroupModal = (id) => {
  const g = (window._groups || []).find(x => x.id === id); if (!g) return;
  openModal("Edit group", `
    <label class="field"><span>Group URL</span><input type="url" id="g-url" value="${esc(g.url)}"></label>
    <label class="field"><span>Name</span><input type="text" id="g-name" value="${esc(g.name||"")}"></label>
    <label class="field"><span>Category</span><input type="text" id="g-cat" value="${esc(g.category||"")}"></label>
    <label class="field"><span>Notes</span><textarea id="g-notes">${esc(g.notes||"")}</textarea></label>
    <div class="row"><button class="btn primary" onclick="saveEditGroup(${id})">Save</button><button class="btn ghost" onclick="closeModal()">Cancel</button></div>`);
};
window.saveEditGroup = async (id) => {
  await patchJSON(`/api/groups/${id}`, { url: $("#g-url").value, name: $("#g-name").value, category: $("#g-cat").value, notes: $("#g-notes").value });
  closeModal(); toast("Saved"); renderGroups();
};
window.deleteGroup = async (id) => { if (!confirm("Delete this group?")) return; await del(`/api/groups/${id}`); renderGroups(); };

// ---- TEMPLATES -----------------------------------------------------------
async function renderTemplates() {
  const ts = await getJSON("/api/templates");
  const blocks = ts.map(t => `
    <div class="section">
      <div class="row between">
        <div><h2 style="display:inline;">${esc(t.code)} · ${esc(t.name||"")}</h2>
          ${t.active ? "" : '<span class="badge gray">inactive</span>'}</div>
        <div class="row">
          <button class="btn sm" onclick="editTemplateModal(${t.id})">Edit</button>
          <button class="btn sm danger" onclick="deleteTemplate(${t.id})">Delete</button>
        </div>
      </div>
      <p class="sec-sub">Audiences: <b>${esc(t.audiences||"any")}</b> · Image types: <b>${esc(t.image_types||"any")}</b> · Keyword: <b>${esc(t.keyword||"—")}</b></p>
      <table><tbody>
        ${t.variants.map(v => `<tr>
          <td style="width:100%;">${esc(v.text)}</td>
          <td class="muted" style="white-space:nowrap;">used ${v.times_used||0}×</td>
          <td style="white-space:nowrap;">
            <button class="icon-btn" title="Edit" onclick="editVariant(${v.id}, ${JSON.stringify(esc(v.text)).replace(/"/g,'&quot;')})">✏️</button>
            <button class="icon-btn" title="${v.active?'Disable':'Enable'}" onclick="toggleVariant(${v.id}, ${v.active?0:1})">${v.active?'🟢':'⚪'}</button>
            <button class="icon-btn" title="Delete" onclick="deleteVariant(${v.id})">🗑️</button>
          </td></tr>`).join("") || `<tr><td class="muted">No variants yet.</td></tr>`}
      </tbody></table>
      <div style="margin-top:10px;"><button class="btn sm" onclick="addVariantModal(${t.id})">+ Add variant</button></div>
    </div>`).join("");

  view.innerHTML = `
    <div class="callout info">Each template is one post idea. <b>Variants</b> are different wordings of it — the queue rotates them so no two posts are identical. Replace the starter text with your real playbook copy. Keep your newsletter link OUT of the body (it goes in the first comment).</div>
    <div class="row" style="margin-bottom:6px;"><button class="btn" onclick="addTemplateModal()">+ New template</button></div>
    ${blocks || '<div class="empty">No templates yet.</div>'}`;
}
window.addTemplateModal = () => openModal("New template", templateForm());
function templateForm(t) {
  t = t || {};
  return `
    <label class="field"><span>Code * (e.g. T9)</span><input type="text" id="t-code" value="${esc(t.code||"")}"></label>
    <label class="field"><span>Name</span><input type="text" id="t-name" value="${esc(t.name||"")}"></label>
    <label class="field"><span>Audiences (comma separated)</span><input type="text" id="t-aud" value="${esc(t.audiences||"")}" placeholder="operators,farmer_operators"></label>
    <label class="field"><span>Image types (comma separated)</span><input type="text" id="t-img" value="${esc(t.image_types||"")}" placeholder="hero,rate_card"></label>
    <label class="field"><span>Keyword (comment CTA for the link)</span><input type="text" id="t-kw" value="${esc(t.keyword||"")}" placeholder="rates"></label>
    <div class="row"><button class="btn primary" onclick="${t.id?`saveEditTemplate(${t.id})`:'saveNewTemplate()'}">Save</button><button class="btn ghost" onclick="closeModal()">Cancel</button></div>`;
}
window.saveNewTemplate = async () => {
  try {
    await postJSON("/api/templates", { code: $("#t-code").value, name: $("#t-name").value, audiences: $("#t-aud").value, image_types: $("#t-img").value, keyword: $("#t-kw").value });
    closeModal(); toast("Template added"); renderTemplates();
  } catch (e) { toast(e.message, true); }
};
window.editTemplateModal = async (id) => {
  const ts = await getJSON("/api/templates"); const t = ts.find(x => x.id === id);
  openModal("Edit template", templateForm(t));
};
window.saveEditTemplate = async (id) => {
  await patchJSON(`/api/templates/${id}`, { code: $("#t-code").value, name: $("#t-name").value, audiences: $("#t-aud").value, image_types: $("#t-img").value, keyword: $("#t-kw").value });
  closeModal(); toast("Saved"); renderTemplates();
};
window.deleteTemplate = async (id) => { if (!confirm("Delete this template and all its variants?")) return; await del(`/api/templates/${id}`); renderTemplates(); };
window.addVariantModal = (tid) => openModal("Add variant", `
  <label class="field"><span>Variant text</span><textarea id="v-text" style="min-height:120px;"></textarea></label>
  <div class="row"><button class="btn primary" onclick="saveVariant(${tid})">Add</button><button class="btn ghost" onclick="closeModal()">Cancel</button></div>`);
window.saveVariant = async (tid) => {
  try { await postJSON(`/api/templates/${tid}/variants`, { text: $("#v-text").value }); closeModal(); toast("Variant added"); renderTemplates(); }
  catch (e) { toast(e.message, true); }
};
window.editVariant = (id, text) => openModal("Edit variant", `
  <label class="field"><span>Variant text</span><textarea id="v-text" style="min-height:120px;">${text}</textarea></label>
  <div class="row"><button class="btn primary" onclick="saveVariantEdit(${id})">Save</button><button class="btn ghost" onclick="closeModal()">Cancel</button></div>`);
window.saveVariantEdit = async (id) => { await patchJSON(`/api/variants/${id}`, { text: $("#v-text").value }); closeModal(); toast("Saved"); renderTemplates(); };
window.toggleVariant = async (id, active) => { await patchJSON(`/api/variants/${id}`, { active }); renderTemplates(); };
window.deleteVariant = async (id) => { if (!confirm("Delete this variant?")) return; await del(`/api/variants/${id}`); renderTemplates(); };

// ---- IMAGES --------------------------------------------------------------
async function renderImages() {
  const imgs = await getJSON("/api/images");
  const upload = `
    <div class="section">
      <h2>Upload image</h2>
      <p class="sec-sub">Tag each image by type so it gets matched to the right templates.</p>
      <div class="row">
        <label class="btn primary" style="cursor:pointer;">Choose file
          <input type="file" id="img-file" accept="image/*" style="display:none;" onchange="$('#img-name').textContent=this.files[0]?this.files[0].name:''"></label>
        <span id="img-name" class="muted"></span>
        <select id="img-type" style="width:160px;">
          <option value="hero">hero</option><option value="rate_card">rate_card</option>
          <option value="quote_card">quote_card</option><option value="screenshot">screenshot</option>
        </select>
        <input type="text" id="img-cap" placeholder="caption (optional)" style="width:220px;">
        <button class="btn" onclick="doUpload()">Upload</button>
      </div>
    </div>`;
  const gallery = imgs.length ? `<div class="gallery">${imgs.map(im => `
    <div class="imgcard">
      <img src="/images/${encodeURIComponent(im.filename)}" alt="">
      <div class="meta">
        <span class="badge cat">${esc(im.image_type)}</span> ${im.active ? "" : '<span class="badge gray">off</span>'}<br>
        <span class="muted">used ${im.times_used||0}×</span>
        <div class="row" style="margin-top:6px;gap:6px;">
          <button class="btn sm ghost" onclick="toggleImage(${im.id}, ${im.active?0:1})">${im.active?"Disable":"Enable"}</button>
          <button class="btn sm danger" onclick="deleteImage(${im.id})">Delete</button>
        </div>
      </div></div>`).join("")}</div>`
    : `<div class="empty"><div class="big">🖼️</div><p>No images yet. Upload the images you want rotated across your posts.</p></div>`;
  view.innerHTML = upload + `<div style="margin-top:18px;">${gallery}</div>`;
}
window.doUpload = async () => {
  const f = $("#img-file").files[0];
  if (!f) { toast("Choose a file first", true); return; }
  const fd = new FormData();
  fd.append("file", f); fd.append("image_type", $("#img-type").value); fd.append("caption", $("#img-cap").value);
  try { await api("/api/images", { method: "POST", body: fd }); toast("Uploaded"); renderImages(); }
  catch (e) { toast(e.message, true); }
};
window.toggleImage = async (id, active) => { await patchJSON(`/api/images/${id}`, { active }); renderImages(); };
window.deleteImage = async (id) => { if (!confirm("Delete this image?")) return; await del(`/api/images/${id}`); renderImages(); };

// ---- HISTORY -------------------------------------------------------------
async function renderHistory() {
  const h = await getJSON("/api/history");
  const rows = h.slice().reverse().map(p => `
    <tr>
      <td>${fmtDate(p.posted_at || p.generated_at)}</td>
      <td>${esc(p.group_name || p.group_url || "—")}</td>
      <td><span class="badge cat">${esc(p.category||"—")}</span></td>
      <td>${esc(p.template_code||"—")}</td>
      <td>${esc(p.image_filename||"—")}</td>
      <td><span class="badge ${p.status}">${p.status}</span></td>
      <td>${p.link_in_comment ? "✅" : "—"}</td>
      <td>${p.post_url ? `<a href="${esc(p.post_url)}" target="_blank">view</a>` : "—"}</td>
    </tr>`).join("");
  view.innerHTML = `
    <div class="row between" style="margin-bottom:14px;">
      <div class="muted">${h.length} logged post${h.length===1?"":"s"}</div>
      <a class="btn" href="/api/history/export.csv">⬇ Export CSV</a>
    </div>
    <div class="section">
      <table><thead><tr><th>When</th><th>Group</th><th>Category</th><th>Template</th><th>Image</th><th>Status</th><th>Link in comment</th><th>Post</th></tr></thead>
      <tbody>${rows || '<tr><td colspan="8" class="muted">Nothing logged yet.</td></tr>'}</tbody></table>
    </div>`;
}

// ---- SETTINGS ------------------------------------------------------------
const SETTING_FIELDS = [
  ["newsletter_link", "Newsletter link (goes in first comment)", "url"],
  ["first_comment_text", "First-comment text  ({link} is replaced)", "text"],
  ["session_target", "Default queue size when you click Generate", "number"],
  ["daily_cap", "Soft daily cap (advisory warning only)", "number"],
  ["min_gap_minutes", "Reminder: minutes to space posts apart", "number"],
  ["dup_window_days", "Don't reuse same copy/image within (days)", "number"],
  ["group_cooldown_days", "Don't re-post to same group within (days)", "number"],
  ["high_volume_warn", "Show 'high volume' caution above (posts/day)", "number"],
];
async function renderSettings() {
  const s = await getJSON("/api/settings");
  const fields = SETTING_FIELDS.map(([k, label, type]) => `
    <label class="field"><span>${esc(label)}</span>
      <input type="${type}" id="s-${k}" value="${esc(s[k]||"")}"></label>`).join("");
  view.innerHTML = `
    <div class="callout info">These are <b>guardrails for you</b>, not the platform. This dashboard never posts automatically — it only plans and tracks what you post by hand.</div>
    <div class="section" style="max-width:640px;">
      ${fields}
      <button class="btn primary" onclick="saveSettings()">Save settings</button>
    </div>`;
}
window.saveSettings = async () => {
  const body = {};
  SETTING_FIELDS.forEach(([k]) => body[k] = $(`#s-${k}`).value);
  await postJSON("/api/settings", body); toast("Settings saved");
};

// ---- LOGS ----------------------------------------------------------------
async function renderLogs() {
  const logs = await getJSON("/api/logs");
  const rows = logs.map(l => `<tr>
    <td class="mono">${fmtDate(l.ts)}</td>
    <td><span class="badge ${l.level==='error'?'failed':l.level==='warn'?'skipped':'planned'}">${l.level}</span></td>
    <td>${esc(l.message)}</td></tr>`).join("");
  view.innerHTML = `
    <div class="section">
      <h2>Add a note</h2>
      <p class="sec-sub">Log anything worth remembering — an error you hit, a group that blocked you, an idea. Keeps a running record so we don't repeat mistakes.</p>
      <div class="row">
        <select id="log-level" style="width:120px;"><option value="info">info</option><option value="warn">warn</option><option value="error">error</option></select>
        <input type="text" id="log-msg" placeholder="What happened?" style="flex:1;min-width:240px;">
        <button class="btn" onclick="addLog()">Add</button>
      </div>
    </div>
    <div class="section">
      <table><thead><tr><th>When</th><th>Level</th><th>Message</th></tr></thead>
      <tbody>${rows || '<tr><td colspan="3" class="muted">No log entries yet.</td></tr>'}</tbody></table>
    </div>`;
}
window.addLog = async () => {
  const msg = $("#log-msg").value.trim(); if (!msg) return;
  await postJSON("/api/logs", { message: msg, level: $("#log-level").value });
  toast("Logged"); renderLogs();
};

// ---- boot ----------------------------------------------------------------
(async function boot() {
  try { await getJSON("/api/health"); $("#health-dot").className = "dot ok"; $("#health-text").textContent = "connected"; }
  catch (e) { $("#health-dot").className = "dot bad"; $("#health-text").textContent = "offline"; }
  go("overview");
})();
