const knowledgeBase = [
  {
    keywords: ["ospf", "adjacency", "neighbor", "lsa", "spf"],
    title: "OSPF Fundamentals and Troubleshooting Reference",
    content:
      "A healthy OSPF neighbor relationship is typically FULL. High CPU, packet loss, topology churn, frequent LSA updates, and route redistribution problems can trigger SPF recalculation and adjacency resets."
  },
  {
    keywords: ["bgp", "peer", "neighbor", "asn", "route"],
    title: "BGP Neighbor Failure Troubleshooting Guide",
    content:
      "BGP session instability is commonly caused by peer reachability loss, authentication mismatch, ASN mismatch, route filtering, WAN latency, or hold timer expiry."
  },
  {
    keywords: ["packet loss", "loss", "crc", "input errors", "transceiver", "interface"],
    title: "Packet Loss Investigation Guide",
    content:
      "Packet loss indicators include CRC errors, input errors, congestion, failing optics, poor signal quality, routing loops, and interface carrier transitions."
  },
  {
    keywords: ["cpu", "process", "utilization", "memory"],
    title: "Device Resource Diagnostic Guide",
    content:
      "Sustained high CPU can delay routing protocol hello processing, increase convergence time, and amplify packet loss during control-plane instability."
  },
  {
    keywords: ["port security", "mac", "violation", "errdisable"],
    title: "Port Security Troubleshooting Guide",
    content:
      "Port-security violations can err-disable access ports, cause host outages, and require validation of learned MAC addresses and switchport policy."
  }
];

function selectKnowledge(alert) {
  const normalizedAlert = alert.toLowerCase();
  const matches = knowledgeBase.filter((entry) =>
    entry.keywords.some((keyword) => normalizedAlert.includes(keyword))
  );

  const selected = matches.length ? matches : knowledgeBase.slice(0, 3);
  return selected.map((entry) => `${entry.title}: ${entry.content}`);
}

function extractMetric(alert, pattern, fallback) {
  const match = alert.match(pattern);
  return match ? Number.parseFloat(match[1]) : fallback;
}

function buildDeterministicRca(alert) {
  const normalizedAlert = alert.toLowerCase();
  const hasOspf = normalizedAlert.includes("ospf");
  const hasBgp = normalizedAlert.includes("bgp");
  const hasCpu = normalizedAlert.includes("cpu");
  const hasLoss = normalizedAlert.includes("loss") || normalizedAlert.includes("packet");
  const hasInterface =
    normalizedAlert.includes("interface") ||
    normalizedAlert.includes("crc") ||
    normalizedAlert.includes("flap") ||
    normalizedAlert.includes("carrier");

  const knowledge = selectKnowledge(alert);
  const plan = [
    "Classify severity, impacted network domain, and customer-facing blast radius from the alert text.",
    "Retrieve matching operational knowledge for routing, transport, interface, and resource symptoms.",
    "Correlate symptoms across control-plane state, interface health, packet loss, and device resource pressure.",
    "Rank likely root causes by evidence strength and produce remediation plus validation steps."
  ];

  const diagnostics = [
    hasCpu
      ? "CPU-related symptom detected; prioritize routing-process load, control-plane queueing, and recent topology churn."
      : "No explicit CPU symptom detected; keep device resource pressure as a secondary validation check.",
    hasInterface
      ? "Interface instability indicators detected; inspect CRC/input errors, carrier transitions, optics, cabling, and WAN handoff."
      : "No explicit interface error term detected; validate physical counters if routing symptoms continue.",
    hasOspf || hasBgp
      ? `Routing protocol symptom detected for ${hasOspf ? "OSPF" : "BGP"}; verify neighbor state, timers, reachability, and recent config changes.`
      : "No named routing protocol detected; validate forwarding path, default gateway reachability, and telemetry scope.",
    hasLoss
      ? "Packet-loss symptom detected; compare loss timeline against interface counters, CPU spikes, and routing adjacency events."
      : "No packet-loss term detected; use latency and reachability checks to confirm user impact."
  ];

  let rootCause =
    "The alert indicates a network service degradation that requires correlation across routing state, interface health, and device telemetry.";

  if ((hasOspf || hasBgp) && hasInterface && hasLoss) {
    rootCause =
      "The strongest root cause is transport or uplink interface instability causing packet loss and routing adjacency disruption. Interface errors or carrier transitions should be treated as the primary evidence, with routing resets as a downstream symptom.";
  } else if ((hasOspf || hasBgp) && hasCpu) {
    rootCause =
      "The strongest root cause is control-plane resource pressure affecting routing protocol stability. Sustained CPU load can delay hello or keepalive processing and trigger neighbor resets.";
  } else if (hasInterface) {
    rootCause =
      "The strongest root cause is a degraded interface path, likely cabling, optic, handoff, or congestion related, based on the interface-oriented symptoms in the alert.";
  } else if (hasLoss) {
    rootCause =
      "The strongest root cause is packet-loss in the forwarding path. The next evidence to collect is interface counters, WAN provider telemetry, queue drops, and routing stability around the incident window.";
  }

  const recommendation =
    "Validate the suspected fault domain, shift traffic to a redundant path if impact is high, collect before-and-after counters, remediate the identified interface/routing/resource issue, and monitor stability for at least 15 minutes before closing the incident.";

  const cpu = extractMetric(alert, /cpu(?:\D+)(\d+(?:\.\d+)?)%?/i, hasCpu ? 92 : 37);
  const loss = extractMetric(alert, /(?:loss|packet loss)(?:\D+)(\d+(?:\.\d+)?)%?/i, hasLoss ? 7.8 : 0.8);
  const resets = extractMetric(alert, /(?:reset|flap|down)(?:\D+)(\d+)/i, hasOspf || hasBgp ? 3 : 1);
  const confidence = Math.min(95, 68 + [hasOspf || hasBgp, hasCpu, hasLoss, hasInterface].filter(Boolean).length * 6);

  return {
    plan,
    knowledge,
    diagnostics,
    rootCause,
    recommendation,
    metrics: [
      { label: "Alert Confidence", value: confidence, unit: "%", level: "good" },
      { label: "Packet Loss", value: loss, unit: "%", level: loss > 5 ? "critical" : "warn" },
      { label: "CPU Utilization", value: cpu, unit: "%", level: cpu > 85 ? "critical" : "good" },
      { label: "Correlated Signals", value: [hasOspf || hasBgp, hasCpu, hasLoss, hasInterface].filter(Boolean).length, unit: "hits", level: "warn" }
    ],
    source: "rules_engine"
  };
}

function extractJson(text) {
  try {
    return JSON.parse(text);
  } catch (error) {
    const match = text.match(/\{[\s\S]*\}/);
    return match ? JSON.parse(match[0]) : null;
  }
}

async function runOpenAiRca(alert) {
  if (!process.env.OPENAI_API_KEY) {
    return null;
  }

  const fallback = buildDeterministicRca(alert);
  const prompt = `
You are NetOps AI, a senior cybersecurity and network operations RCA analyst.

Analyze this alert:
${alert}

Use this retrieved knowledge:
${fallback.knowledge.map((item) => `- ${item}`).join("\n")}

Return only valid JSON with this exact shape:
{
  "plan": ["string"],
  "knowledge": ["string"],
  "diagnostics": ["string"],
  "rootCause": "string",
  "recommendation": "string",
  "metrics": [
    {"label": "Alert Confidence", "value": number, "unit": "%", "level": "good|warn|critical"},
    {"label": "Packet Loss", "value": number, "unit": "%", "level": "good|warn|critical"},
    {"label": "CPU Utilization", "value": number, "unit": "%", "level": "good|warn|critical"},
    {"label": "Correlated Signals", "value": number, "unit": "hits", "level": "good|warn|critical"}
  ]
}

Keep each list to 4 concise items. Base the RCA on the alert and retrieved knowledge. Do not invent device names unless present in the alert.
`;

  const openAiResponse = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: process.env.OPENAI_MODEL || "gpt-4o-mini",
      input: prompt,
      temperature: 0.2,
      max_output_tokens: 1200
    })
  });

  if (!openAiResponse.ok) {
    throw new Error(`OpenAI request failed with ${openAiResponse.status}`);
  }

  const payload = await openAiResponse.json();
  const outputText =
    payload.output_text ||
    payload.output?.flatMap((item) => item.content || []).find((content) => content.type === "output_text")?.text;
  const parsed = extractJson(outputText || "");

  if (!parsed) {
    throw new Error("OpenAI response did not contain valid RCA JSON");
  }

  return {
    ...fallback,
    ...parsed,
    source: "live_openai"
  };
}

export default async function handler(request, response) {
  response.setHeader("Access-Control-Allow-Origin", "*");
  response.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  response.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (request.method === "OPTIONS") {
    return response.status(200).json({ ok: true });
  }

  if (request.method !== "POST") {
    return response.status(405).json({ error: "Method not allowed" });
  }

  const alert = request.body?.alert || "";

  try {
    const liveAnalysis = await runOpenAiRca(alert);

    return response.status(200).json({
      ...(liveAnalysis || buildDeterministicRca(alert)),
      alert
    });
  } catch (error) {
    return response.status(200).json({
      ...buildDeterministicRca(alert),
      alert,
      source: "rules_engine_openai_error",
      warning: error.message
    });
  }
}
