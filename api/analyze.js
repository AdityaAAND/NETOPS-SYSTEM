const mockAnalysis = {
  plan: [
    "Classify the incident severity and identify impacted routers, peerings, VLANs, and customer services.",
    "Retrieve similar routing instability, interface error, packet-loss, and high CPU incidents from the knowledge base.",
    "Correlate Prometheus metrics with routing adjacency state, interface counters, and recent diagnostic evidence.",
    "Validate the strongest root cause hypothesis and produce an operator-ready remediation path."
  ],
  knowledge: [
    "Historical incident BGP_004: WAN packet loss caused repeated BGP hold timer expiry on branch edge routers.",
    "OSPF troubleshooting guide: high CPU and input drops can trigger missed hellos and adjacency resets.",
    "Interface flapping playbook recommends checking CRC errors, carrier transitions, optics, cabling, and upstream transport.",
    "Packet loss runbook recommends separating device resource pressure from physical transport degradation."
  ],
  diagnostics: [
    "Prometheus reports CPU utilization above 94% for 11 minutes on the affected network device.",
    "Interface Gi0/1 shows increasing CRC/input errors and intermittent carrier transitions.",
    "Routing adjacency changed from FULL to INIT multiple times during the alert window.",
    "Packet loss to branch VLAN gateways peaked near 8.7% during adjacency reset events."
  ],
  rootCause:
    "The most likely root cause is uplink interface instability compounded by elevated routing-process CPU. The timing of CRC errors, carrier transitions, packet loss, and adjacency resets strongly indicates a physical or transport-layer issue rather than a standalone routing policy failure.",
  recommendation:
    "Fail traffic to the redundant uplink, inspect or replace the affected cable or optic, clear interface counters, and monitor CRC/input errors for 15 minutes. If CPU remains high after link stabilization, capture routing process diagnostics and review recent configuration changes.",
  metrics: [
    { label: "Alert Confidence", value: 91, unit: "%", level: "good" },
    { label: "Packet Loss", value: 8.7, unit: "%", level: "critical" },
    { label: "CPU Utilization", value: 98, unit: "%", level: "critical" },
    { label: "Adjacency Resets", value: 3, unit: "events", level: "warn" }
  ]
};

export default function handler(request, response) {
  response.setHeader("Access-Control-Allow-Origin", "*");
  response.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  response.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (request.method === "OPTIONS") {
    return response.status(200).json({ ok: true });
  }

  if (request.method !== "POST") {
    return response.status(405).json({ error: "Method not allowed" });
  }

  return response.status(200).json({
    ...mockAnalysis,
    alert: request.body?.alert || "",
    source: "vercel_mock_api"
  });
}
