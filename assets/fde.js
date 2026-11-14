// fde.js — small activity helpers for the Forward Deployed Engineering course.
// Load after common.js (it uses addReset). Each helper builds one activity from data in the lesson.

const $ = (sel, root = document) => root.querySelector(sel);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
function shuffle(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }

// ---------- Sort items into boxes: tap an item, then tap its box ----------
// sorter(rootId, { items: [{ t, bin, why }], bins: [{ id, label }], done })
function sorter(rootId, cfg) {
  const root = document.getElementById(rootId);
  const pool = document.createElement("div"); pool.className = "chips";
  const msg = document.createElement("div"); msg.className = "picked";
  const binsEl = document.createElement("div"); binsEl.className = "bins";
  root.append(pool, binsEl, msg);
  let picked = null, placed = 0, order = [];
  function build() {
    pool.innerHTML = ""; binsEl.innerHTML = ""; picked = null; placed = 0;
    msg.textContent = "Tap an item, then tap the box it belongs in.";
    order = shuffle(cfg.items);
    order.forEach((it, i) => {
      const b = document.createElement("button"); b.type = "button"; b.className = "chip"; b.textContent = it.t; b.dataset.i = i; b.dataset.bin = it.bin;
      b.onclick = () => { if (b.classList.contains("used")) return; pool.querySelectorAll(".chip").forEach(x => x.classList.remove("on")); b.classList.add("on"); picked = b; msg.textContent = "Now tap its box."; };
      pool.appendChild(b);
    });
    cfg.bins.forEach(bn => {
      const box = document.createElement("button"); box.type = "button"; box.className = "bin"; box.innerHTML = `<h4>${bn.label}</h4>`; box.dataset.bin = bn.id;
      box.onclick = () => {
        if (!picked) { msg.textContent = "First tap an item above."; return; }
        const it = order[picked.dataset.i];
        if (it.bin === bn.id) {
          const c = document.createElement("span"); c.className = "chip ok"; c.textContent = it.t; box.appendChild(c);
          picked.classList.remove("on"); picked.classList.add("used"); picked.disabled = true; picked.hidden = true; picked = null; placed++;
          msg.innerHTML = placed === order.length ? (cfg.done || "All sorted.") : `Yes. ${it.why ? esc(it.why) : ""} <span class="muted-note">(${placed} of ${order.length})</span>`;
        } else {
          picked.classList.add("no"); const p = picked; setTimeout(() => p.classList.remove("no"), 700);
          msg.innerHTML = `Not quite: ${esc(it.why || "try the other box.")}`;
        }
      };
      binsEl.appendChild(box);
    });
  }
  build(); addReset(root, build);
}

// ---------- Reveal a list one step at a time ----------
// stepper(listId, { after(i) }) — every <li> but the first starts hidden (keeps its space)
function stepper(listId, cfg = {}) {
  const list = document.getElementById(listId);
  const items = [...list.children];
  const row = document.createElement("div"); row.className = "btnrow";
  const back = document.createElement("button"); back.type = "button"; back.textContent = "← Back";
  const next = document.createElement("button"); next.type = "button"; next.className = "primary"; next.textContent = "Next step →";
  const note = document.createElement("span"); note.className = "muted-note";
  row.append(back, next, note); list.after(row);
  let i = 0;
  function show() {
    items.forEach((li, k) => { li.classList.toggle("off", k > i); li.classList.toggle("now", k === i); });
    back.hidden = i === 0; next.hidden = i === items.length - 1;
    note.innerHTML = cfg.after ? cfg.after(i, items.length) : "";
  }
  back.onclick = () => { if (i > 0) { i--; show(); } };
  next.onclick = () => { if (i < items.length - 1) { i++; show(); } };
  show(); addReset(list, () => { i = 0; show(); });
}

// ---------- Practice problems: type an answer, Check, a hint when wrong, Show working ----------
// <div class="prob" data-answer="2" data-hint="…" data-work="…" data-tol="0"> <div class="ask">…</div> </div>
function practice(rootId) {
  const root = document.getElementById(rootId);
  const probs = [...root.querySelectorAll(".prob")];
  probs.forEach(p => {
    const row = document.createElement("div"); row.className = "btnrow";
    const inp = document.createElement("input"); inp.type = "text"; inp.setAttribute("aria-label", "Your answer"); inp.placeholder = "your answer";
    const check = document.createElement("button"); check.type = "button"; check.className = "primary"; check.textContent = "Check";
    const show = document.createElement("button"); show.type = "button"; show.textContent = "Show working"; show.hidden = true;
    const res = document.createElement("div"); res.className = "res";
    const work = document.createElement("div"); work.className = "work"; work.innerHTML = p.dataset.work; work.hidden = true;
    row.append(inp, check, show); p.append(row, res, work);
    const norm = s => s.trim().toLowerCase().replace(/[₹,%\s]/g, "");
    const answers = p.dataset.answer.split("|").map(norm);
    const tol = parseFloat(p.dataset.tol || "0");
    function test() {
      const v = norm(inp.value); if (!v) return;
      const num = parseFloat(v);
      const ok = answers.some(a => a === v || (!isNaN(num) && !isNaN(parseFloat(a)) && Math.abs(num - parseFloat(a)) <= tol));
      res.className = "res " + (ok ? "good" : "bad");
      res.innerHTML = ok ? (p.dataset.right || "Yes, that's it.") : "Not yet. " + (p.dataset.hint || "");
      show.hidden = false;
    }
    check.onclick = test; inp.onkeydown = e => { if (e.key === "Enter") test(); };
    show.onclick = () => { work.hidden = !work.hidden; show.textContent = work.hidden ? "Show working" : "Hide working"; };
    p._reset = () => { inp.value = ""; res.textContent = ""; res.className = "res"; work.hidden = true; show.hidden = true; show.textContent = "Show working"; };
  });
  addReset(root, () => probs.forEach(p => p._reset()));
}

// ---------- Pick one of several cards; each card says why ----------
// picker(rootId, msgId) — buttons with data-right or data-why inside root
function picker(rootId, msgId) {
  const root = document.getElementById(rootId), msg = document.getElementById(msgId);
  const btns = [...root.querySelectorAll("button[data-why], button[data-right]")];
  const start = msg.innerHTML;
  btns.forEach(b => b.onclick = () => {
    btns.forEach(x => x.classList.remove("ok", "no"));
    const right = b.hasAttribute("data-right");
    b.classList.add(right ? "ok" : "no");
    msg.className = "say-why " + (right ? "good" : "bad");
    msg.innerHTML = right ? b.dataset.right : b.dataset.why;
  });
  addReset(root, () => { btns.forEach(x => x.classList.remove("ok", "no")); msg.className = "say-why"; msg.innerHTML = start; });
}

// ---------- A short conversation: pick the best reply to each message ----------
// chatPick(rootId, sayId, { who, turns: [{ q, a: [[text, whyBadOrNull], …] }], end })
function chatPick(rootId, sayId, cfg) {
  const chat = document.getElementById(rootId), say = document.getElementById(sayId);
  const who = cfg.who || "Client";
  let t = 0;
  function bub(cls, html) { const d = document.createElement("div"); d.className = "bub " + cls; d.innerHTML = html; chat.appendChild(d); }
  function ask() {
    if (t >= cfg.turns.length) { if (cfg.endLine) bub("them", `<small>${who}</small>${esc(cfg.endLine)}`); say.className = "say-why good"; say.textContent = cfg.end || "Done."; return; }
    bub("them", `<small>${who}</small>${esc(cfg.turns[t].q)}`);
    const box = document.createElement("div"); box.className = "replies";
    cfg.turns[t].a.forEach(([text, bad]) => {
      const b = document.createElement("button"); b.type = "button"; b.textContent = text; b.dataset.good = bad ? "0" : "1";
      b.onclick = () => {
        if (bad) { say.className = "say-why bad"; say.textContent = bad + " Try another reply."; b.classList.add("no"); b.disabled = true; return; }
        box.remove(); bub("you", `<small>You</small>${esc(text)}`); say.className = "say-why"; say.textContent = ""; t++; ask();
      };
      box.appendChild(b);
    });
    chat.appendChild(box);
  }
  function reset() { chat.innerHTML = ""; say.textContent = ""; say.className = "say-why"; t = 0; ask(); }
  reset(); addReset(chat, reset);
}

// ---------- Choose the best line for each part, then check ----------
// lineBuilder(rootId, btnId, sayId, { lines: [{ k, opts: [], right, why }], done })
function lineBuilder(rootId, btnId, sayId, cfg) {
  const root = document.getElementById(rootId), check = document.getElementById(btnId), say = document.getElementById(sayId);
  const lines = cfg.lines;
  root.classList.add("scope");
  root.innerHTML = lines.map((l, i) => `<label class="line"><b>${l.k}</b><select data-i="${i}" data-right="${l.right}"><option value="">Choose…</option>${l.opts.map((o, j) => `<option value="${j}">${esc(o)}</option>`).join("")}</select></label>`).join("");
  const sels = [...root.querySelectorAll("select")];
  sels.forEach(s => s.onchange = () => { s.className = ""; });
  check.onclick = () => {
    let ok = 0, first = null;
    sels.forEach((s, i) => {
      if (s.value === "") { s.className = ""; if (first === null) first = { i, empty: true }; return; }
      const right = +s.value === lines[i].right; s.className = right ? "ok" : "no";
      if (right) ok++; else if (first === null) first = { i };
    });
    if (ok === lines.length) { say.className = "say-why good"; say.textContent = cfg.done || "All right."; }
    else if (first && first.empty) { say.className = "say-why"; say.textContent = `${ok} of ${lines.length} right so far. Choose a line for "${lines[first.i].k}" too.`; }
    else { say.className = "say-why bad"; say.textContent = `${ok} of ${lines.length} right. ${lines[first.i].k}: ${lines[first.i].why}`; }
  };
  addReset(root, () => { sels.forEach(s => { s.value = ""; s.className = ""; }); say.textContent = ""; say.className = "say-why"; });
}

// ---------- Put steps in order: tap them first to last ----------
// orderer(rootId, { steps: [in the right order], done })
function orderer(rootId, cfg) {
  const root = document.getElementById(rootId);
  const pool = document.createElement("div"); pool.className = "chips";
  const list = document.createElement("ol"); list.className = "ordered";
  const msg = document.createElement("div"); msg.className = "picked";
  root.append(pool, list, msg);
  let next = 0;
  function build() {
    pool.innerHTML = ""; list.innerHTML = ""; next = 0;
    msg.textContent = "Tap the steps in order, first to last.";
    shuffle(cfg.steps.map((s, i) => ({ s, i }))).forEach(({ s, i }) => {
      const b = document.createElement("button"); b.type = "button"; b.className = "chip"; b.textContent = s; b.dataset.order = i;
      b.onclick = () => {
        if (i === next) { const li = document.createElement("li"); li.textContent = s; list.appendChild(li); b.hidden = true; next++;
          msg.textContent = next === cfg.steps.length ? (cfg.done || "In order.") : "Yes. What comes next?"; }
        else { b.classList.add("no"); setTimeout(() => b.classList.remove("no"), 700); msg.textContent = cfg.hints && cfg.hints[i] ? "Not yet: " + cfg.hints[i] : "Not yet. Something else comes first."; }
      };
      pool.appendChild(b);
    });
  }
  build(); addReset(root, build);
}

// ---------- Show/hide content with switches ----------
// toggles(rootId, { keys: [{ id, label, on }], render(state) → html }, outId)
function toggles(rootId, outId, cfg) {
  const root = document.getElementById(rootId), out = document.getElementById(outId);
  let state;
  function draw() { out.innerHTML = cfg.render(state); }
  function build() {
    state = {}; root.innerHTML = "";
    cfg.keys.forEach(k => {
      state[k.id] = !!k.on;
      const lab = document.createElement("label"); lab.className = "switch";
      lab.innerHTML = `<input type="checkbox"${k.on ? " checked" : ""}> <span>${k.label}</span>`;
      lab.querySelector("input").onchange = e => { state[k.id] = e.target.checked; draw(); };
      root.appendChild(lab);
    });
    draw();
  }
  build(); addReset(root, build);
}
