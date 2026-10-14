import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

const NODE_NAME = "ProfileWordFilter";
const SLOTS = ["profile", "profile_2", "profile_3", "profile_4"];
const NO_VALUE = ["(none)", "(no profile saved)"];
const SPLIT_RE = /[,\u060c\n]+/;

// ---- tag helpers (same rules as the Python side)
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
.swfp{display:flex;flex-direction:column;gap:6px;width:100%;height:100%;box-sizing:border-box;padding:4px;
  font:12px/1.4 Tahoma,"Segoe UI",sans-serif;color:var(--input-text,#ddd)}
.swfp-row{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.swfp button{padding:3px 10px;border-radius:4px;border:1px solid #555;background:#333;color:inherit;cursor:pointer}
.swfp button:hover{filter:brightness(1.3)}
.swfp button.go{border-color:#3f9b5f;background:#1f4d33}
.swfp .st{flex:1;opacity:.7;font-size:11px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.swfp label{font-weight:bold;flex:1}
.swfp .box{display:flex;flex-direction:column;gap:3px;flex:1;min-height:0;border:1px solid #444;
  border-radius:8px;padding:5px;background:rgba(0,0,0,.14)}
.swfp .box.in{border-color:#2f7a4d}
.swfp .box.out{border-color:#9b403d}
.swfp .box.in label{color:#5fd68e}
.swfp .box.out label{color:#ff8582}
.swfp .chips{flex:1;min-height:40px;overflow-y:auto;display:flex;flex-wrap:wrap;gap:5px;
  align-content:flex-start;padding:2px}
.swfp .empty{opacity:.55;padding:4px}
.swfp-chip{display:inline-flex;direction:ltr;align-items:stretch;border-radius:6px;border:1px solid #555;
  background:#2c2c2c;overflow:hidden;user-select:none}
.swfp-chip .t{padding:2px 8px;display:flex;align-items:center}
.swfp-chip button{border:0;background:rgba(255,255,255,.07);color:#aaa;cursor:pointer;padding:0 7px;
  font-weight:bold;font-size:14px;line-height:1}
.swfp-chip button:hover{background:rgba(255,255,255,.2);color:#fff}
.swfp-chip.want{border-color:#3f9b5f;background:#1f4d33;color:#c9f2d6}
.swfp-chip.want .p{background:#2fae6a;color:#fff}
.swfp-chip.dont{border-color:#c0504d;background:#5a2523;color:#f6d0cf}
.swfp-chip.dont .m{background:#d9534f;color:#fff}
.swfp .help{border:1px solid #4a5a6a;border-radius:8px;background:rgba(70,110,150,.12);padding:5px 8px;font-size:11px}
.swfp .help .ttl{font-weight:bold;cursor:pointer;display:flex;gap:6px;align-items:center}
.swfp .help .body{margin-top:5px;opacity:.9;line-height:1.6;white-space:pre-wrap}
.swfp .hint{font-size:11px;opacity:.65}
`;

function injectCss() {
  if (document.getElementById("swfp-css")) return;
  const st = document.createElement("style");
  st.id = "swfp-css";
  st.textContent = CSS;
  document.head.appendChild(st);
}

const el = (tag, cls, text) => {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  return e;
};

async function copyText(text) {
  try { await navigator.clipboard.writeText(text); return true; } catch { /* fallback */ }
  const ta = document.createElement("textarea");
  ta.value = text; document.body.appendChild(ta); ta.select();
  let ok = false;
  try { ok = document.execCommand("copy"); } catch { /* ignore */ }
  ta.remove();
  return ok;
}

// brief, complete help text (English); collapsed by default
const HELP_TEXT =
  "Split or replace the input tags using saved profiles.\n" +
  "• split: output 1 = tags inside the profile(s), output 2 = the rest.\n" +
  "   On each tag: + = want (force-keep), - = don't want (force-remove). Click again to reset; don't want wins.\n" +
  "• replace: removes the profile tags and inserts your 'replacement' tags; output 1 = result, output 2 = removed.\n" +
  "mode: any_profile = in at least one selected profile; all_profiles = in every one.\n" +
  "The (★) profiles are built from the tag_lists folder and refresh live.";

app.registerExtension({
  name: "SmartWordFilter.ProfileTools",

  async beforeRegisterNodeDef(nodeType, nodeData) {
    if (nodeData.name !== NODE_NAME) return;
    injectCss();

    const onCreated = nodeType.prototype.onNodeCreated;
    nodeType.prototype.onNodeCreated = function () {
      onCreated?.apply(this, arguments);
      const node = this;
      const W = (n) => node.widgets?.find((w) => w.name === n);
      const linked = (n) => node.inputs?.some((i) => i.name === n && i.link != null);
      const isReplace = () => W("operation")?.value === "replace";

      // ---- backing widgets for the want / don't-want lists (split mode)
      const addW = () => W("add_tags");
      const remW = () => W("remove_tags");
      const listOf = (w) => extractWords(w?.value || "");
      const setWidget = (w, list) => {
        if (!w) return;
        const v = list.join(", ");
        if (v !== w.value) {
          w.value = v;
          w.callback?.call(w, v);
          const dom = w.element || w.inputEl;
          const field = dom?.querySelector?.("textarea, input") || dom;
          if (field && "value" in field) field.value = v;
        }
        app.graph?.setDirtyCanvas(true, true);
      };
      const stateOf = (tag) => {
        if (has(listOf(remW()), tag)) return "dont";
        if (has(listOf(addW()), tag)) return "want";
        return "neu";
      };
      const toggleWant = (tag) => {
        if (stateOf(tag) === "want") {
          setWidget(addW(), without(listOf(addW()), tag));
        } else {
          setWidget(remW(), without(listOf(remW()), tag));
          const a = listOf(addW()); if (!has(a, tag)) a.push(tag);
          setWidget(addW(), a);
        }
        schedule();
      };
      const toggleDont = (tag) => {
        if (stateOf(tag) === "dont") {
          setWidget(remW(), without(listOf(remW()), tag));
        } else {
          setWidget(addW(), without(listOf(addW()), tag));
          const r = listOf(remW()); if (!has(r, tag)) r.push(tag);
          setWidget(remW(), r);
        }
        schedule();
      };

      // ---- UI
      const root = el("div", "swfp");

      // description / help (collapsed by default)
      const help = el("div", "help");
      const htitle = el("div", "ttl");
      const arrow = el("span", "", "▶");
      htitle.append(arrow, el("span", "", "How this node works"));
      const hbody = el("div", "body", HELP_TEXT);
      hbody.style.display = "none";
      htitle.onclick = () => {
        const show = hbody.style.display === "none";
        hbody.style.display = show ? "block" : "none";
        arrow.textContent = show ? "▼" : "▶";
      };
      help.append(htitle, hbody);

      const bar = el("div", "swfp-row");
      const btn = el("button", "go", "Preview now");
      btn.title = "Apply instantly, without running the workflow";
      const status = el("span", "st", "Preview updates automatically on any change.");
      bar.append(btn, status);

      const mkBox = (cls) => {
        const box = el("div", "box " + cls);
        const head = el("div", "swfp-row");
        const lbl = el("label", "", "");
        const cp = el("button", "", "Copy");
        head.append(lbl, cp);
        const chips = el("div", "chips");
        box.append(head, chips);
        box._tags = [];
        cp.onclick = async () => {
          const ok = await copyText(box._tags.join(", "));
          cp.textContent = ok ? "Copied ✓" : "Failed";
          setTimeout(() => (cp.textContent = "Copy"), 1200);
        };
        return { box, chips, lbl };
      };
      const outIn = mkBox("in");
      const outRest = mkBox("out");
      const hint = el("div", "hint", "+ = want   - = don't want   click again = reset");
      root.append(help, bar, outIn.box, outRest.box, hint);

      // render chips; +/- buttons only in split mode
      const renderChips = (target, tags, editable) => {
        target.box._tags = tags.slice();
        target.chips.textContent = "";
        if (!tags.length) { target.chips.append(el("div", "empty", "—")); return; }
        for (const tag of tags) {
          const st = editable ? stateOf(tag) : "neu";
          const chip = el("span", "swfp-chip" + (st === "neu" ? "" : " " + st));
          if (editable) {
            const bm = el("button", "m", "-"); bm.title = "don't want (force-remove)";
            bm.onclick = () => toggleDont(tag);
            const bp = el("button", "p", "+"); bp.title = "want (force-keep)";
            bp.onclick = () => toggleWant(tag);
            chip.append(bm, bp);
          }
          chip.append(el("span", "t", tag));
          target.chips.append(chip);
        }
      };

      // ---- preview logic
      let busy = false, again = false;
      async function preview() {
        if (busy) { again = true; return; }
        busy = true;
        try {
          const replace = isReplace();
          outIn.lbl.textContent = replace ? "result (output 1)" : "kept / in_profile (output 1)";
          outRest.lbl.textContent = replace ? "removed_tags (output 2)" : "rest / not_in_profile (output 2)";
          hint.style.display = replace ? "none" : "";

          const textW = W("text");
          const text = linked("text") ? node.swfLastText : textW?.value;
          if (text == null) {
            status.textContent = "Text comes from another node: run the workflow once first.";
            return;
          }
          const profiles = SLOTS.map((n) => W(n)?.value).filter((v) => v && !NO_VALUE.includes(v));
          if (!profiles.length) { status.textContent = "Select a profile first."; return; }
          const r = await api.fetchApi("/smart_word_filter/preview", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              text, profiles,
              operation: W("operation")?.value,
              mode: W("mode")?.value,
              separator: W("separator")?.value ?? ", ",
              add_tags: addW()?.value ?? "",
              remove_tags: remW()?.value ?? "",
              replacement: W("replacement")?.value ?? "",
              insert_at: W("insert_at")?.value ?? "where_first_match",
              if_no_match: W("if_no_match")?.value ?? "append",
            }),
          });
          const j = await r.json();
          if (!r.ok) { status.textContent = j.error || "Preview failed."; return; }
          renderChips(outIn, extractWords(j.in), !replace);
          renderChips(outRest, extractWords(j.out), !replace);
          status.textContent = linked("text") ? "Updated (text of the last run)." : "Updated.";
        } catch (e) {
          status.textContent = "Preview failed: " + e.message;
        } finally {
          busy = false;
          if (again) { again = false; schedule(); }
        }
      }
      let timer = null;
      function schedule() {
        clearTimeout(timer);
        timer = setTimeout(preview, 250);
      }
      btn.onclick = preview;

      // ---- auto-update when any related widget changes
      const names = ["text", ...SLOTS, "operation", "mode", "separator", "add_tags",
                     "remove_tags", "replacement", "insert_at", "if_no_match"];
      for (const n of names) {
        const w = W(n);
        if (!w) continue;
        const cb = w.callback;
        w.callback = function () { cb?.apply(this, arguments); schedule(); };
      }
      const bindInputs = () => {
        for (const n of ["text", "add_tags", "remove_tags", "replacement"]) {
          const e = W(n)?.element || W(n)?.inputEl;
          if (e && !e.dataset.swfp) { e.dataset.swfp = "1"; e.addEventListener("input", schedule); }
        }
      };
      bindInputs(); setTimeout(bindInputs, 300);

      node.addDOMWidget("live_preview", "swfp_board", root, {
        serialize: false,
        hideOnZoom: false,
        getMinHeight: () => 280,
      });
      const sz = node.computeSize();
      node.setSize([Math.max(sz[0], 460), Math.max(sz[1], 620)]);
      setTimeout(schedule, 500);
      node.swfPreview = preview;
    };

    // remember the text of the last run (when it comes from another node) and refresh the preview
    const onExec = nodeType.prototype.onExecuted;
    nodeType.prototype.onExecuted = function (message) {
      onExec?.apply(this, arguments);
      if (message?.text) {
        this.swfLastText = Array.isArray(message.text) ? message.text[0] : message.text;
        this.swfPreview?.();
      }
    };
  },
});
