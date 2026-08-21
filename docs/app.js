/* DeployerX Pages — live progress + atlas + Path A */

const DATA_URL = "./data/progress.json";

const state = {
  data: null,
  lang: "en",
  l2Filter: null,
  statusFilter: "all",
  hasL3Only: false,
  sort: "complete",
  query: "",
  path: { use: null, lang: null },
};

function $(id) {
  return document.getElementById(id);
}

function esc(s) {
  return String(s ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function fmtTime(iso) {
  try {
    return new Date(iso).toLocaleString(undefined, {
      dateStyle: "medium",
      timeStyle: "short",
    });
  } catch {
    return iso || "unknown";
  }
}

function pct(num, den) {
  if (!den) return 0;
  return Math.min(100, Math.round((num / den) * 100));
}

function applyCopy() {
  const copy = state.data?.copy?.[state.lang] || state.data?.copy?.en;
  if (!copy) return;
  $("mission").textContent = copy.mission;
  $("lede").textContent = copy.lede;
  $("promise").textContent = copy.promise;
  document.documentElement.lang = state.lang === "hi" ? "hi" : "en";
  const btn = $("lang-toggle");
  btn.textContent = state.lang === "en" ? "हिं" : "EN";
  btn.setAttribute("aria-pressed", state.lang === "hi" ? "true" : "false");
}

function renderStats(stats) {
  const items = [
    [stats.india_l2_seeded, "L2 seeded"],
    [stats.india_l3_seeded ?? 0, "L3 seeded"],
    [stats.india_l3_draft ?? stats.india_l3, "L3 draft"],
    [stats.playbooks, "Playbooks"],
    [stats.glossaries, "Glossaries"],
    [stats.field_notes, "Field notes"],
  ];
  $("stat-grid").innerHTML = items
    .map(
      ([n, label]) => `
      <div class="stat">
        <span class="num">${esc(n)}</span>
        <span class="label">${esc(label)}</span>
      </div>`
    )
    .join("");
}

function renderIndiaProgress(india) {
  const l2Pct = pct(india.l2_seeded_count, india.l2_index_count || india.l2_meta_count || 36);
  const goal = india.l3_goal || 780;
  const seeded = india.l3_seeded_count ?? 0;
  const draft = india.l3_draft_count ?? 0;
  const l3Pct = pct(seeded, goal);
  $("india-progress").innerHTML = `
    <div class="bar-block">
      <div class="row"><span>India L2 seeded (not stubs)</span><span>${india.l2_seeded_count}/${india.l2_index_count || india.l2_meta_count}</span></div>
      <div class="bar-track"><div class="bar-fill" style="width:${l2Pct}%"></div></div>
    </div>
    <div class="bar-block">
      <div class="row"><span>India L3 seeded</span><span>${seeded} seeded · ${draft} draft · ~${goal} goal</span></div>
      <div class="bar-track"><div class="bar-fill" style="width:${l3Pct}%"></div></div>
    </div>`;
}

function renderStory() {
  const notes = state.data.field_notes || [];
  const featured = notes.find((n) => n.featured) || notes[0];
  const claim = state.data.links?.claim_l3 || "#";
  if (featured) {
    $("featured-note").innerHTML = `
      <p class="eyebrow">Field note</p>
      <h2>${esc(featured.title)}</h2>
      <p class="section-lede">${esc(featured.excerpt || "Deployment receipt from the field.")}</p>
      <p class="fine">${esc(featured.locale || "")} · ${esc(featured.playbook || "")}</p>
      <a class="btn ghost" href="${esc(featured.url)}" rel="noopener">Read note</a>`;
  } else {
    $("featured-note").innerHTML = `
      <p class="eyebrow">Field notes</p>
      <h2>None published yet</h2>
      <p class="section-lede">Stats stay at zero until a real Path A note lands with Results filled in.</p>
      <a class="btn ghost" href="https://github.com/Anshul9t6/DeployerX/blob/main/field-notes/FIRST_DEPLOYMENT.md" rel="noopener">First deployment checklist</a>`;
  }

  const recent = state.data.india?.recent_l3 || [];
  $("recent-activity").innerHTML = recent.length
    ? recent
        .map(
          (r) => `<li><a href="${esc(r.url)}" rel="noopener"><strong>${esc(r.name)}</strong> · ${esc(r.l2_name)} · ${esc(r.status)}</a></li>`
        )
        .join("")
    : `<li class="empty">No L3 packs yet. <a href="${esc(claim)}">Open an L3 issue</a></li>`;
}

function renderCountries(countries) {
  $("countries").innerHTML = (countries || [])
    .map((c) => {
      const status = (c.status || "draft").replaceAll('"', "");
      return `
      <a class="country-card" href="${esc(c.url)}" rel="noopener">
        <div class="code">${esc(c.code)}</div>
        <h3>${esc(c.name || c.code)}</h3>
        <p>${esc(c.notes || "Locale pack in progress")}</p>
        <div class="meta">
          <span class="chip hot">${esc(status)}</span>
          <span class="chip">L2 ${esc(c.l2_meta_count ?? 0)}</span>
          <span class="chip">L3 ${esc(c.l3_count ?? 0)}</span>
        </div>
      </a>`;
    })
    .join("");
}

function l3Hay(item) {
  return `${item.name} ${item.slug} ${item.l2} ${item.l2_name} ${item.languages} ${item.status} ${item.blurb || ""}`.toLowerCase();
}

function filteredL3() {
  let items = [...(state.data.india?.l3 || [])];
  if (state.l2Filter) items = items.filter((i) => i.l2 === state.l2Filter);
  if (state.statusFilter !== "all") {
    items = items.filter((i) => (i.status || "").includes(state.statusFilter));
  }
  if (state.query.trim()) {
    const q = state.query.trim().toLowerCase();
    items = items.filter((i) => l3Hay(i).includes(q));
  }
  if (state.sort === "name") items.sort((a, b) => a.name.localeCompare(b.name));
  else if (state.sort === "state") items.sort((a, b) => a.l2.localeCompare(b.l2) || a.name.localeCompare(b.name));
  else items.sort((a, b) => (b.status === "seeded") - (a.status === "seeded") || a.name.localeCompare(b.name));
  return items;
}

function renderL3() {
  const claim = state.data.links?.claim_l3 || "#";
  const items = filteredL3();
  const hint = state.l2Filter
    ? `Focused on <strong>${esc(state.l2Filter)}</strong> — ${items.length} pack(s).`
    : "Showing all India L3 packs. Click an L2 pill to focus.";
  $("drill-hint").innerHTML = hint;
  $("clear-l2").hidden = !state.l2Filter;
  $("l3-count-label").textContent = `${items.length} district pack${items.length === 1 ? "" : "s"}`;

  if (!items.length) {
    $("l3-grid").innerHTML = `
      <div class="empty-state">
        <p>No matches in this view.</p>
        <a class="btn primary" href="${esc(claim)}" rel="noopener">Open L3 issue</a>
        <button type="button" class="btn ghost" id="reset-filters">Reset filters</button>
      </div>`;
    $("reset-filters")?.addEventListener("click", () => {
      state.l2Filter = null;
      state.statusFilter = "all";
      state.query = "";
      $("l3-filter").value = "";
      document.querySelectorAll(".chip-btn[data-status]").forEach((b) => {
        b.classList.toggle("active", b.dataset.status === "all");
      });
      renderL2();
      renderL3();
    });
    return;
  }

  $("l3-grid").innerHTML = items
    .map(
      (i) => `
    <a class="l3-card" href="${esc(i.url)}" rel="noopener">
      <strong>${esc(i.name)}</strong>
      <span>${esc(i.l2_name)} · ${esc(i.status)} · ${esc(i.languages)}</span>
    </a>`
    )
    .join("");
}

function renderL2() {
  const items = state.data.india?.l2 || [];
  let list = items;
  if (state.hasL3Only) list = items.filter((i) => i.l3_count > 0);
  $("l2-strip").innerHTML = list
    .map((i) => {
      const cls = [
        "l2-pill",
        i.status !== "listed" ? "seeded" : "",
        i.l3_count > 0 ? "has-l3" : "",
        state.l2Filter === i.slug ? "active" : "",
      ]
        .filter(Boolean)
        .join(" ");
      return `<button type="button" class="${cls}" data-l2="${esc(i.slug)}" title="${esc(i.name)} · ${i.l3_count} L3">${esc(i.slug)}</button>`;
    })
    .join("");

  $("l2-strip").querySelectorAll("[data-l2]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const slug = btn.getAttribute("data-l2");
      state.l2Filter = state.l2Filter === slug ? null : slug;
      renderL2();
      renderL3();
      document.getElementById("explore")?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
}

function renderPlaybooks(playbooks) {
  $("playbook-grid").innerHTML = (playbooks || [])
    .map(
      (p) => `
    <a class="playbook-card" href="${esc(p.url)}" rel="noopener">
      <div class="id">${esc(p.id)} · ${esc(p.status)}</div>
      <h3>${esc(p.title)}</h3>
      <p>${esc(p.blurb || "Open the playbook on GitHub.")}</p>
      <div class="meta">
        <span class="chip hot">${esc(p.budget_label || "₹0")}</span>
        <span class="chip">${esc(p.time_to_first_win || "~30 min")}</span>
      </div>
    </a>`
    )
    .join("");
}

function playbookForUse(use) {
  const list = state.data.playbooks || [];
  if (use === "clinic") return list.find((p) => p.id.includes("clinic")) || list[0];
  return list.find((p) => p.id.includes("shop")) || list[0];
}

function updatePathUI() {
  const steps = document.querySelectorAll(".path-step");
  const done0 = !!state.path.use;
  const done1 = !!state.path.lang;
  steps.forEach((el) => {
    const n = Number(el.dataset.step);
    el.classList.toggle("active", n === 0 || (n === 1 && done0) || (n === 2 && done0) || (n === 3 && done0 && done1));
    el.classList.toggle("done", (n === 0 && done0) || (n === 1 && done1));
  });

  const pb = playbookForUse(state.path.use);
  if (pb && state.path.use) {
    $("path-playbook-label").textContent = pb.title;
    $("path-playbook-link").href = pb.deploy_url || pb.url;
    $("path-playbook-link").textContent = "Open deploy.md";
  }
  if (pb && state.path.lang) {
    const prompts = { hi: pb.prompt_hi, en: pb.prompt_en, pt: pb.prompt_pt };
    const prompt = prompts[state.path.lang] || pb.prompt_en;
    $("path-prompt-label").textContent = `Language: ${state.path.lang} · paste FAQ under <<<FAQ>>>`;
    $("path-prompt-link").href = prompt || pb.url;
    $("path-prompt-link").textContent = "Open system prompt";
  }
}

function wirePath() {
  document.querySelectorAll("#choice-use .choice").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.path.use = btn.dataset.use;
      document.querySelectorAll("#choice-use .choice").forEach((b) => b.classList.toggle("selected", b === btn));
      updatePathUI();
    });
  });
  document.querySelectorAll("#choice-lang .choice").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.path.lang = btn.dataset.lang;
      document.querySelectorAll("#choice-lang .choice").forEach((b) => b.classList.toggle("selected", b === btn));
      updatePathUI();
    });
  });
}

function wireExplore() {
  $("l3-filter").addEventListener("input", (e) => {
    state.query = e.target.value;
    renderL3();
  });
  $("l3-sort").addEventListener("change", (e) => {
    state.sort = e.target.value;
    renderL3();
  });
  $("clear-l2").addEventListener("click", () => {
    state.l2Filter = null;
    renderL2();
    renderL3();
  });
  document.querySelectorAll(".chip-btn[data-status]").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.statusFilter = btn.dataset.status;
      document.querySelectorAll(".chip-btn[data-status]").forEach((b) => b.classList.toggle("active", b === btn));
      renderL3();
    });
  });
  document.querySelectorAll(".chip-btn[data-l2-only]").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.hasL3Only = !state.hasL3Only;
      btn.classList.toggle("active", state.hasL3Only);
      renderL2();
    });
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && !e.metaKey && !e.ctrlKey && !e.altKey) {
      const tag = (e.target && e.target.tagName) || "";
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      e.preventDefault();
      $("l3-filter").focus();
    }
  });
}

async function main() {
  wirePath();
  wireExplore();
  $("lang-toggle").addEventListener("click", () => {
    state.lang = state.lang === "en" ? "hi" : "en";
    applyCopy();
  });

  const res = await fetch(DATA_URL, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to load ${DATA_URL}`);
  state.data = await res.json();

  applyCopy();
  $("generated-at").textContent = fmtTime(state.data.generated_at);
  $("generated-at").setAttribute("datetime", state.data.generated_at);
  if (state.data.links?.contribute) $("claim-link").href = state.data.links.contribute;
  if (state.data.links?.claim_l3) $("issue-l3").href = state.data.links.claim_l3;
  if (state.data.links?.receipt_plan && $("receipt-link")) {
    $("receipt-link").href = state.data.links.receipt_plan;
  }

  renderStats(state.data.stats);
  renderIndiaProgress(state.data.india);
  renderStory();
  renderCountries(state.data.countries);
  renderPlaybooks(state.data.playbooks);
  renderL2();
  renderL3();
  updatePathUI();
}

main().catch((err) => {
  console.error(err);
  $("stat-grid").innerHTML = `<p class="empty">Could not load live progress. Run <code>python3 scripts/generate_site_data.py</code> or open <a href="./data/progress.json">progress.json</a>.</p>`;
});
