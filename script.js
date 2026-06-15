const sampleAlert =
  "BGP neighbor 10.20.0.2 is flapping on edge-router-02 after WAN latency spikes. Prometheus shows packet loss above 8%, interface errors rising on Gi0/1, and customer VPN tunnels intermittently dropping.";

const fallbackAnalysis = {
  plan: [
    "Classify the alert severity and identify impacted routers, peerings, and customer-facing services.",
    "Retrieve similar OSPF, BGP, interface error, and packet-loss incidents from the knowledge base.",
    "Correlate Prometheus telemetry with routing adjacency state, CPU load, and interface counters.",
    "Form a root cause hypothesis and validate it against recent configuration and diagnostic evidence."
  ],
  knowledge: [
    "Historical incident BGP_004: WAN packet loss caused repeated BGP hold timer expiry on branch edge routers.",
    "Playbook: verify physical errors, MTU mismatch, route policy changes, and upstream provider stability.",
    "OSPF guide: high CPU and interface drops can trigger missed hellos and adjacency resets.",
    "Packet loss runbook recommends isolating transport, device resource, and security policy causes."
  ],
  diagnostics: [
    "core-router-01 CPU remains above 94% for 11 minutes with routing process spikes.",
    "Gi0/1 reports rising CRC/input errors and intermittent carrier transitions.",
    "OSPF neighbor state changed FULL to INIT three times in the last 15 minutes.",
    "Packet loss to branch VLAN gateways peaked at 8.7% during adjacency resets."
  ],
  rootCause:
    "The most likely root cause is interface instability on the uplink path combined with sustained routing-process CPU pressure. Error counters and carrier transitions align with OSPF adjacency resets and observed packet loss, making a pure software or policy issue less likely.",
  recommendation:
    "Move traffic to the redundant uplink, inspect or replace the affected transceiver/cable, clear the interface counters, and monitor CRC errors for 15 minutes. If CPU remains elevated after link stabilization, capture routing process diagnostics and temporarily tune adjacency timers only as a controlled mitigation.",
  metrics: [
    { label: "Alert Confidence", value: 91, unit: "%", level: "good" },
    { label: "Packet Loss", value: 8.7, unit: "%", level: "critical" },
    { label: "CPU Utilization", value: 98, unit: "%", level: "critical" },
    { label: "Adjacency Resets", value: 3, unit: "events", level: "warn" }
  ]
};

const form = document.querySelector("#alertForm");
const alertInput = document.querySelector("#alertInput");
const sampleButton = document.querySelector("#sampleButton");
const loadingState = document.querySelector("#loadingState");
const apiBadge = document.querySelector("#apiBadge");
const workflowNodes = [...document.querySelectorAll(".agent-node")];

const planList = document.querySelector("#planList");
const knowledgeList = document.querySelector("#knowledgeList");
const diagnosticsList = document.querySelector("#diagnosticsList");
const rootCauseText = document.querySelector("#rootCauseText");
const recommendationText = document.querySelector("#recommendationText");
const metricsGrid = document.querySelector("#metricsGrid");
const timestamp = document.querySelector("#timestamp");

function setLoading(isLoading) {
  loadingState.classList.toggle("visible", isLoading);
  loadingState.setAttribute("aria-hidden", String(!isLoading));
  form.querySelector("button[type='submit']").disabled = isLoading;
}

function renderList(target, items) {
  target.innerHTML = "";
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    target.appendChild(li);
  });
}

function renderMetrics(metrics) {
  metricsGrid.innerHTML = "";
  metrics.forEach((metric) => {
    const card = document.createElement("article");
    card.className = "metric-card";

    const safeValue = Math.min(Number(metric.value) || 0, 100);
    card.innerHTML = `
      <small>${metric.label}</small>
      <div class="metric-value">
        <strong>${metric.value}</strong>
        <span>${metric.unit}</span>
      </div>
      <div class="metric-bar" aria-hidden="true">
        <span style="width: ${safeValue}%"></span>
      </div>
    `;
    metricsGrid.appendChild(card);
  });
}

function renderAnalysis(data) {
  renderList(planList, data.plan);
  renderList(knowledgeList, data.knowledge);
  renderList(diagnosticsList, data.diagnostics);
  rootCauseText.textContent = data.rootCause;
  recommendationText.textContent = data.recommendation;
  renderMetrics(data.metrics);
  timestamp.textContent = `Updated ${new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit"
  })}`;
}

function normalizeApiResponse(payload) {
  return {
    plan: payload.plan || payload.investigation_plan || fallbackAnalysis.plan,
    knowledge: payload.knowledge || payload.retrieved_knowledge || fallbackAnalysis.knowledge,
    diagnostics: payload.diagnostics || fallbackAnalysis.diagnostics,
    rootCause: payload.rootCause || payload.root_cause || payload.rca || fallbackAnalysis.rootCause,
    recommendation: payload.recommendation || payload.recommendations || fallbackAnalysis.recommendation,
    metrics: payload.metrics || fallbackAnalysis.metrics
  };
}

async function analyzeAlert(alertText) {
  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ alert: alertText })
    });

    if (!response.ok) {
      throw new Error("Analyze endpoint unavailable");
    }

    const payload = await response.json();
    apiBadge.textContent = "Live API response";
    apiBadge.classList.remove("mock");
    return normalizeApiResponse(payload);
  } catch (error) {
    await new Promise((resolve) => setTimeout(resolve, 900));
    apiBadge.textContent = "Mock API response";
    apiBadge.classList.add("mock");
    return fallbackAnalysis;
  }
}

function animateWorkflow() {
  workflowNodes.forEach((node) => node.classList.remove("active"));
  workflowNodes.forEach((node, index) => {
    setTimeout(() => {
      workflowNodes.forEach((item) => item.classList.remove("active"));
      node.classList.add("active");
    }, index * 220);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const alertText = alertInput.value.trim();

  if (!alertText) {
    alertInput.focus();
    return;
  }

  setLoading(true);
  animateWorkflow();
  const analysis = await analyzeAlert(alertText);
  renderAnalysis(analysis);
  setLoading(false);
});

sampleButton.addEventListener("click", () => {
  alertInput.value = sampleAlert;
  alertInput.focus();
});

renderAnalysis(fallbackAnalysis);
