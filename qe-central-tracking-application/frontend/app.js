const CATEGORIES = ["api", "web", "mobile", "database", "performance", "ai"];

const state = {
  category: "",
  buildId: "",
};

function qs(params) {
  const entries = Object.entries(params).filter(([, v]) => v !== "" && v !== undefined && v !== null);
  if (!entries.length) return "";
  return "?" + entries.map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`).join("&");
}

async function getJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Request failed: ${url} (${res.status})`);
  return res.json();
}

function fmtPct(value) {
  return value === null || value === undefined ? "n/a" : `${value}%`;
}

function barClass(value, goodAbove = true, threshold = 80) {
  if (value === null || value === undefined) return "warn";
  if (goodAbove) return value >= threshold ? "good" : value >= threshold - 20 ? "warn" : "bad";
  return value <= threshold ? "good" : value <= threshold + 20 ? "warn" : "bad";
}

function setupTabs() {
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(`tab-${btn.dataset.tab}`).classList.add("active");
      loadTab(btn.dataset.tab);
    });
  });
}

async function loadOverview() {
  const data = await getJSON(`/api/metrics/dashboard${qs({ build_id: state.buildId })}`);
  const container = document.getElementById("overviewCards");
  container.innerHTML = "";

  const categories = state.category ? [state.category] : CATEGORIES;
  for (const category of categories) {
    const metrics = data.categories[category];
    if (!metrics) continue;
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <h3>${category}</h3>
      ${renderMetricBar("Gate pass rate", metrics.gate_pass_rate_percent, true, 80)}
      ${renderMetricBar("DDE", metrics.dde_percent, true, 70)}
      ${renderMetricBar("Automation DDE", metrics.automation_dde_percent, true, 60)}
      ${renderMetricBar("Production leakage", metrics.production_leakage_percent, false, 20)}
      ${renderMetricBar("Flaky rate", metrics.flaky_rate_percent, false, 5)}
      <div class="metric-row"><span>Defects (total)</span><span class="value">${metrics.defects.total}</span></div>
      <div class="metric-row"><span>Executions</span><span class="value">${metrics.executions.total}</span></div>
    `;
    container.appendChild(card);
  }

  const dep = data.deployments;
  document.getElementById("deploymentSummary").innerHTML = `
    <h3>Deployments</h3>
    <div class="metric-row"><span>Count</span><span class="value">${dep.count}</span></div>
    <div class="metric-row"><span>Avg duration (s)</span><span class="value">${dep.avg_duration_seconds ?? "n/a"}</span></div>
    <div class="metric-row"><span>Success rate</span><span class="value">${fmtPct(dep.success_rate_percent)}</span></div>
  `;
}

function renderMetricBar(label, value, goodAbove, threshold) {
  const pct = value === null || value === undefined ? 0 : Math.min(Math.abs(value), 100);
  const cls = barClass(value, goodAbove, threshold);
  return `
    <div class="metric-row"><span>${label}</span><span class="value">${fmtPct(value)}</span></div>
    <div class="bar-track"><div class="bar-fill ${cls}" style="width:${pct}%"></div></div>
  `;
}

async function loadExecutions() {
  const rows = await getJSON(`/api/executions${qs({ category: state.category, build_id: state.buildId })}`);
  const tbody = document.querySelector("#executionsTable tbody");
  tbody.innerHTML = rows
    .map(
      (r) => `<tr>
        <td>${r.category}</td><td>${r.suite_name}</td><td>${r.environment}</td><td>${r.build_id ?? ""}</td>
        <td>${r.status}</td><td>${r.passed_tests}/${r.total_tests}</td><td>${new Date(r.started_at).toLocaleString()}</td>
      </tr>`
    )
    .join("");
}

async function loadDeployments() {
  const rows = await getJSON(`/api/deployments${qs({ build_id: state.buildId })}`);
  const tbody = document.querySelector("#deploymentsTable tbody");
  tbody.innerHTML = rows
    .map(
      (r) => `<tr>
        <td>${r.service_name}</td><td>${r.environment}</td><td>${r.category ?? ""}</td><td>${r.status}</td>
        <td>${Math.round(r.duration_seconds ?? 0)}</td><td>${new Date(r.started_at).toLocaleString()}</td>
      </tr>`
    )
    .join("");
}

async function loadDefects() {
  const rows = await getJSON(`/api/defects${qs({ category: state.category, build_id: state.buildId })}`);
  const tbody = document.querySelector("#defectsTable tbody");
  tbody.innerHTML = rows
    .map(
      (r) => `<tr>
        <td>${r.category}</td><td>${r.title}</td><td>${r.priority}</td><td>${r.status}</td>
        <td>${r.detected_by}</td><td>${r.detection_phase}</td><td>${new Date(r.detected_at).toLocaleString()}</td>
      </tr>`
    )
    .join("");
}

async function loadFlakiness() {
  const rows = await getJSON(`/api/flakiness${qs({ category: state.category })}`);
  const tbody = document.querySelector("#flakinessTable tbody");
  tbody.innerHTML = rows
    .map(
      (r) => `<tr>
        <td>${r.name}</td><td>${r.category}</td><td>${r.total_runs}</td><td>${r.flaky_runs}</td>
        <td>${fmtPct(r.flaky_rate_percent)}</td>
      </tr>`
    )
    .join("");
}

async function loadGates() {
  const rows = await getJSON(`/api/quality-gates${qs({ category: state.category, build_id: state.buildId })}`);
  const tbody = document.querySelector("#gatesTable tbody");
  tbody.innerHTML = rows
    .map(
      (r) => `<tr>
        <td>${r.category}</td><td>${r.name}</td><td>${r.gate_type}</td><td>${r.stage ?? ""}</td>
        <td>${r.status}</td><td>${r.owner ?? ""}</td>
      </tr>`
    )
    .join("");
}

async function loadCoverage() {
  const rows = await getJSON(`/api/coverage/summary${qs({ build_id: state.buildId })}`);
  const filtered = state.category ? rows.filter((r) => r.category === state.category) : rows;
  const tbody = document.querySelector("#coverageTable tbody");
  tbody.innerHTML = filtered
    .map(
      (r) => `<tr>
        <td>${r.category}</td><td>${r.metric_name}</td><td>${r.numerator}</td><td>${r.denominator}</td>
        <td>${fmtPct(r.coverage_percent)}</td>
      </tr>`
    )
    .join("");
}

async function generateAIInsights() {
  const button = document.getElementById("generateInsights");
  button.disabled = true;
  button.textContent = "Generating...";
  try {
    const data = await getJSON(`/api/ai/insights${qs({ build_id: state.buildId })}`);
    document.getElementById("aiProviderBadge").textContent = `provider: ${data.provider}`;
    document.getElementById("aiSummary").textContent = data.summary;
    document.getElementById("aiRecommendations").innerHTML = data.recommendations
      .map((rec) => `<li>${rec}</li>`)
      .join("");
  } finally {
    button.disabled = false;
    button.textContent = "Generate AI Insights";
  }
}

function loadTab(tab) {
  const loaders = {
    overview: loadOverview,
    executions: loadExecutions,
    deployments: loadDeployments,
    defects: loadDefects,
    flakiness: loadFlakiness,
    gates: loadGates,
    coverage: loadCoverage,
    ai: () => Promise.resolve(),
  };
  (loaders[tab] || (() => Promise.resolve()))().catch((err) => console.error(err));
}

function currentActiveTab() {
  const active = document.querySelector(".tab-btn.active");
  return active ? active.dataset.tab : "overview";
}

document.addEventListener("DOMContentLoaded", () => {
  setupTabs();
  document.getElementById("applyFilters").addEventListener("click", () => {
    state.category = document.getElementById("categoryFilter").value;
    state.buildId = document.getElementById("buildFilter").value.trim();
    loadTab(currentActiveTab());
  });
  document.getElementById("generateInsights").addEventListener("click", generateAIInsights);
  loadOverview().catch((err) => console.error(err));
});
