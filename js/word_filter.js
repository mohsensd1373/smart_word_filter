import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

const NODE_NAME = "SmartWordFilter";
const SPLIT_RE = /[,\u060c\n]+/;

const norm = (s) => s.toLowerCase().split(/\s+/).filter(Boolean).join(" ");
const canon = (s) => norm(s).replace(/_/g, " ");

function tagKey(seg) {
  let s = seg.trim(), prev = null;
  while (s !== prev) {
    prev = s;
    s = s.replace(/^[(\[{<]+|[)\]}>]+$/g, "").trim();
    s = s.replace(/:\s*-?[\d.]+$/, "").trim();
  }
  return norm(s);
}

function extractWords(text) {
  const out = [], seen = new Set();
  for (const seg of (text || "").split(SPLIT_RE)) {
    const k = tagKey(seg);
    if (k && !seen.has(canon(k))) { seen.add(canon(k)); out.push(k); }
  }
  return out;
}

const has = (list, w) => list.some((x) => canon(x) === canon(w));
const without = (list, w) => list.filter((x) => canon(x) !== canon(w));

const CSS = `
.swf-board{display:flex;flex-direction:column;gap:6px;width:100%;height:100%;box-sizing:border-box;
  padding:6px;font:13px/1.4 Tahoma,"Segoe UI",sans-serif;color:var(--input-text,#ddd);overflow:hidden}
.swf-row{display:flex;gap:4px;align-items:center;flex-wrap:wrap}
.swf-row input,.swf-row select{flex:1;min-width:0;padding:4px 6px;border-radius:4px;border:1px solid #555;
  background:var(--comfy-input-bg,#222);color:inherit}
.swf-btn{padding:3px 8px;border-radius:4px;border:1px solid #555;background:#333;color:inherit;cursor:pointer;white-space:nowrap}
.swf-btn:hover{filter:brightness(1.3)}
.swf-sec{display:flex;flex-direction:column;gap:4px;min-height:0;border:1px solid #444;border-radius:8px;
  padding:5px;background:rgba(0,0,0,.14)}
.swf-sec.grow{flex:1.2}.swf-sec.half{flex:1}
.swf-sec.pos{border-color:#2f7a4d}.swf-sec.neg{border-color:#9b403d}
.swf-title{font-weight:bold;display:flex;align-items:center;gap:6px}
.swf-title .sp{flex:1}
.swf-sec.pos .swf-title{color:#5fd68e}.swf-sec.neg .swf-title{color:#ff8582}
.swf-sec.pos .add{border-color:#3f9b5f;background:#1f4d33}
.swf-sec.neg .add{border-color:#c0504d;background:#5a2523}
.swf-chips{flex:1;min-height:34px;overflow-y:auto;display:flex;flex-wrap:wrap;gap:5px;align-content:flex-start;padding:2px}
.swf-chip{display:inline-flex;direction:ltr;align-items:stretch;border-radius:6px;border:1px solid #555;
  background:#2c2c2c;overflow:hidden;user-select:none}
.swf-chip .t{padding:2px 8px;display:flex;align-items:center}
.swf-chip button{border:0;background:rgba(255,255,255,.07);color:#aaa;cursor:pointer;padding:0 7px;
  font-weight:bold;font-size:14px;line-height:1}
.swf-chip button:hover{background:rgba(255,255,255,.2);color:#fff}
.swf-chip.pos{border-color:#3f9b5f;background:#1f4d33;color:#c9f2d6}
.swf-chip.neg{border-color:#c0504d;background:#5a2523;color:#f6d0cf}
.swf-chip.pos .p{background:#2fae6a;color:#fff}
.swf-chip.neg .m{background:#d9534f;color:#fff}
.swf-chip.ro{cursor:default}
.swf-hint{font-size:11px;opacity:.65}
.swf-empty{opacity:.55;padding:4px}
`;

function injectCss() {
  if (document.getElementById("swf-css")) return;
  const st = document.createElement("style");
  st.id = "swf-css";
  st.textContent = CSS;
  document.head.appendChild(st);
}

function hideWidget(w) {
  w.type = "converted-widget";
  w.hidden = true;
  w.computeSize = () => [0, -4];
  if (w.element) w.element.style.display = "none";
}

async function copyText(text) {
  try { await navigator.clipboard.writeText(text); return true; } catch { /* fallback */ }
  const ta = document.createElement("textarea");
  ta.value = text; document.body.appendChild(ta); ta.select();
  let ok = false;
  try { ok = document.execCommand("copy"); } catch { /* ignore */ }
  ta.remove();
  return ok;
}

// refresh the profile lists of the other nodes
function refreshCombos() {
  try { app.refreshComboInNodes?.(); } catch { /* ignore */ }
}

async function postJson(url, body) {
  const r = await api.fetchApi(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error("HTTP " + r.status);
  return r.json();
}

const el = (tag, cls, text) => {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  return e;
};

app.registerExtension({
  name: "SmartWordFilter.WordBoard",

  async beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.name !== NODE_NAME) return;
    injectCss();

    const onCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
      onCreated?.apply(this, arguments);
      const node = this;
      const W = (n) => node.widgets?.find((w) => w.name === n);
      const rulesW = W("rules");
      const textW = W("text");
      hideWidget(rulesW);

      // ---------- state (stored in the hidden "rules" widget)
      const load = () => {
        try {
          const d = JSON.parse(rulesW.value || "{}");
          return { pos: d.pos || [], neg: d.neg || [], seen: d.seen || [], pp: d.pp || "", np: d.np || "" };
        } catch { return { pos: [], neg: [], seen: [], pp: "", np: "" }; }
      };
      let state = load();
      const save = () => {
        const v = JSON.stringify(state);
        if (v !== rulesW.value) rulesW.value = v;
        app.graph?.setDirtyCanvas(true, true);
      };
      const stateOf = (w) => (has(state.neg, w) ? "neg" : has(state.pos, w) ? "pos" : "neu");

      // a tag can only be in one of the two lists
      const put = (w, s) => {
        state.pos = without(state.pos, w);
        state.neg = without(state.neg, w);
        if (s === "pos") state.pos.push(w);
        if (s === "neg") state.neg.push(w);
      };
      const setState = (w, s) => { put(w, s); save(); renderAll(); };

      // ---------- profiles (on disk)
      let profiles = { pos: {}, neg: {} };
      const refreshProfiles = async () => {
        try {
          const r = await api.fetchApi("/smart_word_filter/profiles");
          if (r.ok) profiles = await r.json();
        } catch { /* ignore */ }
        panels.pos.fillSelect(); panels.neg.fillSelect();
      };

      // ---------- DOM
      const board = el("div", "swf-board");
      board.dir = "auto";

      // 1) tags of the input text
      const secText = el("div", "swf-sec grow");
      const tRow = el("div", "swf-row");
      const tTitle = el("div", "swf-title", "Tags in input text");
      const sp = el("span", "sp");
      const btnExtract = el("button", "swf-btn", "Extract from text");
      btnExtract.onclick = () => refreshFromText(true);
      tTitle.append(sp, btnExtract);
      const textChips = el("div", "swf-chips");
      const hint = el("div", "swf-hint", "+ = positive   − = negative   click again = neutral");
      secText.append(tTitle, textChips, hint);

      // 2) positive / negative panels
      function makePanel(kind, title) {
        const pk = kind === "pos" ? "pp" : "np";
        const sec = el("div", "swf-sec half " + kind);

        const head = el("div", "swf-title");
        const count = el("span", "", "");
        const sp2 = el("span", "sp");
        const bCopy = el("button", "swf-btn", "Copy");
        bCopy.onclick = async () => {
          const ok = await copyText(state[kind].join(", "));
          bCopy.textContent = ok ? "Copied ✓" : "Failed";
          setTimeout(() => (bCopy.textContent = "Copy"), 1200);
        };
        const bClear = el("button", "swf-btn", "Clear");
        bClear.onclick = () => {
          if (state[kind].length && confirm("Clear this list?")) { state[kind] = []; save(); renderAll(); }
        };
        head.append(el("span", "", title), count, sp2, bCopy, bClear);

        const addRow = el("div", "swf-row");
        const input = el("input");
        input.placeholder = kind === "pos" ? "New positive tag(s), comma separated..." : "New negative tag(s), comma separated...";
        const bAdd = el("button", "swf-btn add", "Add");
        const add = () => {
          const ws = extractWords(input.value);
          if (!ws.length) return;
          input.value = "";
          ws.forEach((w) => put(w, kind));
          save(); renderAll();
        };
        bAdd.onclick = add;
        input.addEventListener("keydown", (e) => { e.stopPropagation(); if (e.key === "Enter") add(); });
        input.addEventListener("paste", (e) => e.stopPropagation());
        addRow.append(input, bAdd);

        const chips = el("div", "swf-chips");

        // profiles
        const pRow = el("div", "swf-row");
        const sel = el("select");
        const fillSelect = () => {
          const names = Object.keys(profiles[kind] || {}).sort((a, b) => a.localeCompare(b));
          const cur = state[pk];
          sel.textContent = "";
          const o0 = el("option", "", names.length ? "— select profile —" : "— no profile saved —");
          o0.value = "";
          sel.append(o0);
          names.forEach((n) => { const o = el("option", "", n); o.value = n; sel.append(o); });
          sel.value = names.includes(cur) ? cur : "";
        };
        const words = () => profiles[kind]?.[sel.value] || [];
        const bLoad = el("button", "swf-btn", "Load");
        bLoad.title = "Replaces the current list";
        bLoad.onclick = () => {
          if (!sel.value) return;
          state[kind] = [];
          words().forEach((w) => put(w, kind));
          state[pk] = sel.value; save(); renderAll();
        };
        const bMerge = el("button", "swf-btn", "Merge");
        bMerge.title = "Adds to the current list";
        bMerge.onclick = () => {
          if (!sel.value) return;
          words().forEach((w) => put(w, kind));
          save(); renderAll();
        };
        const saveAs = async (name) => {
          try {
            profiles = await postJson("/smart_word_filter/profiles/save", { kind, name, words: state[kind] });
            state[pk] = name; save(); panels.pos.fillSelect(); panels.neg.fillSelect(); refreshCombos();
          } catch (e) { alert("Save failed: " + e.message); }
        };
        const bSave = el("button", "swf-btn", "Save");
        bSave.title = "Saves into the selected profile";
        bSave.onclick = async () => {
          const name = sel.value;
          if (!name || name.startsWith("★")) { const n = prompt(name ? "Built-in profiles cannot be overwritten; new profile name:" : "Profile name:", name ? name.replace(/^★\s*/, "") : ""); if (n && n.trim()) await saveAs(n.trim()); return; }
          if (name !== state[pk] && !confirm(`Overwrite profile "${name}"?`)) return;
          await saveAs(name);
        };
        const bNew = el("button", "swf-btn", "Save as new");
        bNew.onclick = async () => {
          const n = prompt("New profile name:", state[pk] || "");
          if (n && n.trim()) await saveAs(n.trim());
        };
        const bDel = el("button", "swf-btn", "Delete");
        bDel.onclick = async () => {
          if (sel.value.startsWith("★")) { alert("Built-in (★) profiles cannot be deleted."); return; }
          if (!sel.value || !confirm(`Delete profile "${sel.value}"?`)) return;
          try {
            profiles = await postJson("/smart_word_filter/profiles/delete", { kind, name: sel.value });
            if (state[pk] === sel.value) state[pk] = "";
            save(); panels.pos.fillSelect(); panels.neg.fillSelect(); refreshCombos();
          } catch (e) { alert("Delete failed: " + e.message); }
        };
        pRow.append(sel, bLoad, bMerge, bSave, bNew, bDel);

        sec.append(head, addRow, chips, pRow);

        const render = () => {
          count.textContent = `(${state[kind].length})`;
          chips.textContent = "";
          if (!state[kind].length) { chips.append(el("div", "swf-empty", "List is empty")); return; }
          for (const w of state[kind]) {
            const c = el("span", "swf-chip ro " + kind);
            const t = el("span", "t", w);
            const x = el("button", kind === "pos" ? "p" : "m", "×");
            x.title = "Remove from list";
            x.onclick = () => { state[kind] = without(state[kind], w); save(); renderAll(); };
            c.append(t, x);
            chips.append(c);
          }
        };
        return { sec, render, fillSelect };
      }

      const panels = { pos: makePanel("pos", "Positive list"), neg: makePanel("neg", "Negative list") };
      board.append(secText, panels.pos.sec, panels.neg.sec);

      // ---------- render
      function renderText() {
        textChips.textContent = "";
        const list = [];
        for (const w of state.seen) if (!has(list, w)) list.push(w); // drop duplicates
        if (!list.length) {
          textChips.append(el("div", "swf-empty", "No text yet."));
          return;
        }
        for (const w of list) {
          const s = stateOf(w);
          const c = el("span", "swf-chip " + s);
          const bm = el("button", "m", "−"); bm.title = "Negative";
          bm.onclick = () => setState(w, s === "neg" ? "neu" : "neg");
          const bp = el("button", "p", "+"); bp.title = "Positive";
          bp.onclick = () => setState(w, s === "pos" ? "neu" : "pos");
          c.append(bm, bp, el("span", "t", w));
          textChips.append(c);
        }
      }
      function renderAll() { renderText(); panels.pos.render(); panels.neg.render(); }

      // ---------- extraction
      function setSeen(words) {
        const next = [];
        for (const w of words) if (!has(next, w)) next.push(w);
        if (JSON.stringify(next) === JSON.stringify(state.seen)) return;
        state.seen = next; save(); renderText();
      }
      const textIsLinked = () => node.inputs?.some((i) => i.name === "text" && i.link != null);
      function refreshFromText(force) {
        if (textIsLinked()) {
          if (force) alert("The text input is linked to another node; tags are extracted after the workflow runs.");
          return;
        }
        setSeen(extractWords(textW.value));
      }
      const origCb = textW.callback;
      textW.callback = function () { origCb?.apply(this, arguments); refreshFromText(false); };
      const bindLive = () => {
        const e = textW.element || textW.inputEl;
        if (e && !e.dataset.swf) { e.dataset.swf = "1"; e.addEventListener("input", () => refreshFromText(false)); }
      };
      bindLive(); setTimeout(bindLive, 300);

      node.addDOMWidget("word_board", "swf_board", board, {
        serialize: false,
        hideOnZoom: false,
        getMinHeight: () => 560,
      });

      node.swfSetSeen = setSeen;
      node.swfReload = () => { state = load(); renderAll(); panels.pos.fillSelect(); panels.neg.fillSelect(); };
      node.setSize([Math.max(node.size[0], 500), Math.max(node.size[1], 820)]);
      renderAll();
      refreshProfiles();
    };

    // after execution: tags of the input text (even when it comes from another node)
    const onExec = nodeType.prototype.onExecuted;
    nodeType.prototype.onExecuted = function (message) {
      onExec?.apply(this, arguments);
      if (message?.words) this.swfSetSeen?.(message.words);
    };

    // after a workflow is loaded
    const onCfg = nodeType.prototype.onConfigure;
    nodeType.prototype.onConfigure = function () {
      onCfg?.apply(this, arguments);
      setTimeout(() => this.swfReload?.(), 0);
    };
  },
});
