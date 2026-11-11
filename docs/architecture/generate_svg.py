#!/usr/bin/env python3
"""Generate a comprehensive, beautiful SVG architecture diagram for the Highly Available QE Platform."""

import xml.etree.ElementTree as ET

def create_svg():
    width = 1600
    height = 1040

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background:#090d16; font-family:-apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif;">')

    # Definitions
    svg.append('''
  <defs>
    <!-- Background Blueprint Grid Pattern -->
    <pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="0.8" fill="#1e293b" opacity="0.6"/>
    </pattern>

    <!-- Drop Shadows -->
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.6"/>
    </filter>
    <filter id="card-shadow" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000000" flood-opacity="0.45"/>
    </filter>
    <filter id="glow-cyan" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>

    <!-- Gradients -->
    <linearGradient id="header-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="50%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e1b4b"/>
    </linearGradient>

    <linearGradient id="card-grad-infra" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#0b1120"/>
    </linearGradient>

    <linearGradient id="card-grad-k8s" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0f1e36"/>
      <stop offset="100%" stop-color="#091322"/>
    </linearGradient>

    <linearGradient id="card-grad-obs" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#181329"/>
      <stop offset="100%" stop-color="#0e0a1c"/>
    </linearGradient>

    <linearGradient id="card-grad-agent" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#08202d"/>
      <stop offset="100%" stop-color="#05131b"/>
    </linearGradient>

    <linearGradient id="card-grad-dr" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1b122c"/>
      <stop offset="100%" stop-color="#0f0a1c"/>
    </linearGradient>

    <!-- Badges -->
    <linearGradient id="badge-blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>
    <linearGradient id="badge-green" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#059669"/>
      <stop offset="100%" stop-color="#047857"/>
    </linearGradient>
    <linearGradient id="badge-orange" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ea580c"/>
      <stop offset="100%" stop-color="#c2410c"/>
    </linearGradient>
    <linearGradient id="badge-purple" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#7c3aed"/>
      <stop offset="100%" stop-color="#6d28d9"/>
    </linearGradient>

    <!-- Arrow Markers -->
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#38bdf8"/>
    </marker>
    <marker id="arrow-orange" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#fb923c"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#34d399"/>
    </marker>
    <marker id="arrow-purple" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#c084fc"/>
    </marker>
    <marker id="arrow-rose" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#fb7185"/>
    </marker>
  </defs>
''')

    # Background
    svg.append(f'<rect width="{width}" height="{height}" fill="#090d16"/>')
    svg.append(f'<rect width="{width}" height="{height}" fill="url(#grid)"/>')

    # Header Bar
    svg.append('''
  <!-- ======================== HEADER BAR ======================== -->
  <g transform="translate(30, 20)">
    <rect width="1540" height="74" rx="10" fill="url(#header-grad)" stroke="#334155" stroke-width="1.2" filter="url(#shadow)"/>
    
    <!-- Title & Subtitle with K8s Wheel Icon -->
    <g transform="translate(25, 18)">
      <!-- Hex Shield Icon -->
      <path d="M 18 4 L 32 11 L 32 27 L 18 34 L 4 27 L 4 11 Z" fill="#0284c7" opacity="0.25" stroke="#38bdf8" stroke-width="1.5"/>
      <circle cx="18" cy="19" r="5" fill="#38bdf8"/>
      <path d="M 18 9 L 18 14 M 18 24 L 18 29 M 9 14 L 13 16 M 23 22 L 27 24 M 9 24 L 13 22 M 23 16 L 27 14" stroke="#38bdf8" stroke-width="1.8"/>

      <text x="48" y="18" fill="#f8fafc" font-size="20" font-weight="700" letter-spacing="0.4">HIGHLY AVAILABLE QUALITY ENGINEERING PLATFORM</text>
      <text x="48" y="36" fill="#94a3b8" font-size="11.5" font-weight="500">Enterprise Blueprint • Multi-Cloud (AWS/Azure) &amp; Local HA • GitOps Continuous Reconciliation • Dynamic Agent Cloud • Full Observability &amp; DR</text>
    </g>

    <!-- HA Pillars / Badges -->
    <g transform="translate(930, 23)">
      <!-- Badge 1: 3-CP Quorum -->
      <g transform="translate(0, 0)">
        <rect width="140" height="28" rx="6" fill="url(#badge-blue)" stroke="#0284c7" stroke-width="0.8"/>
        <text x="70" y="18" fill="#ffffff" font-size="10.5" font-weight="700" text-anchor="middle">⚡ 3-CP ETCD QUORUM</text>
      </g>
      <!-- Badge 2: JCasC RTO -->
      <g transform="translate(150, 0)">
        <rect width="140" height="28" rx="6" fill="url(#badge-green)" stroke="#059669" stroke-width="0.8"/>
        <text x="70" y="18" fill="#ffffff" font-size="10.5" font-weight="700" text-anchor="middle">⏱️ JCasC RTO &lt; 45s</text>
      </g>
      <!-- Badge 3: GitOps Self-Heal -->
      <g transform="translate(300, 0)">
        <rect width="150" height="28" rx="6" fill="url(#badge-orange)" stroke="#ea580c" stroke-width="0.8"/>
        <text x="75" y="18" fill="#ffffff" font-size="10.5" font-weight="700" text-anchor="middle">🔄 ARGOCD SELF-HEAL</text>
      </g>
      <!-- Badge 4: PDB Protected -->
      <g transform="translate(460, 0)">
        <rect width="135" height="28" rx="6" fill="url(#badge-purple)" stroke="#7c3aed" stroke-width="0.8"/>
        <text x="67" y="18" fill="#ffffff" font-size="10.5" font-weight="700" text-anchor="middle">🛡️ PDB PROTECTED</text>
      </g>
    </g>
  </g>
''')

    # ROW 1: (Y: 108 to 408)
    # Box 1: Infrastructure & Cloud Runtimes (Terraform)
    svg.append('''
  <!-- ======================== ROW 1: PLATFORM FOUNDATION ======================== -->
  <!-- BOX 1: Infrastructure & Cloud Environments (Terraform) -->
  <g transform="translate(30, 108)">
    <rect width="460" height="300" rx="10" fill="url(#card-grad-infra)" stroke="#1e3a5f" stroke-width="1.4" filter="url(#card-shadow)"/>
    <!-- Title Strip -->
    <path d="M 0 10 Q 0 0 10 0 L 450 0 Q 460 0 460 10 L 460 38 L 0 38 Z" fill="#0b1e38"/>
    <text x="18" y="24" fill="#38bdf8" font-size="12.5" font-weight="700" letter-spacing="0.5">☁️ INFRASTRUCTURE &amp; CLOUD RUNTIMES (TERRAFORM)</text>
    
    <!-- AWS Multi-AZ -->
    <g transform="translate(15, 48)">
      <rect width="430" height="72" rx="7" fill="#0b1728" stroke="#1d4ed8" stroke-width="1"/>
      <!-- AWS Icon Pill -->
      <rect x="12" y="12" width="28" height="28" rx="6" fill="#f59e0b" opacity="0.15"/>
      <path d="M 18 29 C 23 32 29 32 34 29" stroke="#f59e0b" stroke-width="2" fill="none" stroke-linecap="round"/>
      <text x="26" y="24" fill="#f59e0b" font-size="13" font-weight="bold" text-anchor="middle">a</text>
      
      <text x="50" y="23" fill="#f8fafc" font-size="12.5" font-weight="700">Amazon Web Services (Multi-AZ VPC)</text>
      <text x="50" y="39" fill="#94a3b8" font-size="10.5">Subnets: us-east-1a, 1b, 1c • Dedicated NAT Gateways • IAM IRSA</text>
      <text x="50" y="55" fill="#38bdf8" font-size="10" font-weight="600">EKS v1.30 HA Managed Nodes • Multi-AZ EFS • S3 Versioned Buckets</text>
    </g>

    <!-- Azure Multi-AZ -->
    <g transform="translate(15, 128)">
      <rect width="430" height="72" rx="7" fill="#0b1728" stroke="#0284c7" stroke-width="1"/>
      <rect x="12" y="12" width="28" height="28" rx="6" fill="#0284c7" opacity="0.15"/>
      <text x="26" y="30" fill="#38bdf8" font-size="14" font-weight="bold" text-anchor="middle">Az</text>
      
      <text x="50" y="23" fill="#f8fafc" font-size="12.5" font-weight="700">Microsoft Azure (Multi-Zone VNet)</text>
      <text x="50" y="39" fill="#94a3b8" font-size="10.5">Availability Zones: ["1", "2", "3"] • Auto-Scaling • 33% Max Surge</text>
      <text x="50" y="55" fill="#60a5fa" font-size="10" font-weight="600">AKS v1.30 HA Cluster • GRS Geo-Redundant Storage • Azure Monitor</text>
    </g>

    <!-- Local Docker / Kind / LocalStack -->
    <g transform="translate(15, 208)">
      <rect width="430" height="76" rx="7" fill="#0b1728" stroke="#0d9488" stroke-width="1"/>
      <rect x="12" y="14" width="28" height="28" rx="6" fill="#0d9488" opacity="0.15"/>
      <text x="26" y="32" fill="#2dd4bf" font-size="13" font-weight="bold" text-anchor="middle">🐳</text>
      
      <text x="50" y="24" fill="#f8fafc" font-size="12.5" font-weight="700">Local Development (Multi-Node Kind &amp; Emulators)</text>
      <text x="50" y="40" fill="#94a3b8" font-size="10.5">6-Node HA Kind: 3 Control-Planes (etcd HA) + 3 Zone Worker Nodes</text>
      <text x="50" y="56" fill="#2dd4bf" font-size="10" font-weight="600">LocalStack 3.7.2 (S3, IAM, STS, CloudWatch) • Azurite Storage (Port 10000)</text>
    </g>
  </g>
''')

    # Box 2: Kubernetes Core Platform & GitOps (Namespaced)
    svg.append('''
  <!-- BOX 2: Kubernetes HA Workloads & GitOps Engine -->
  <g transform="translate(510, 108)">
    <rect width="550" height="300" rx="10" fill="url(#card-grad-k8s)" stroke="#2563eb" stroke-width="1.4" filter="url(#card-shadow)"/>
    <!-- Title Strip -->
    <path d="M 0 10 Q 0 0 10 0 L 540 0 Q 550 0 550 10 L 550 38 L 0 38 Z" fill="#0c203f"/>
    <text x="18" y="24" fill="#60a5fa" font-size="12.5" font-weight="700" letter-spacing="0.5">☸️ KUBERNETES HA PLATFORM CORE &amp; GITOPS (NAMESPACED)</text>
    
    <!-- Sub-box: ArgoCD GitOps Engine -->
    <g transform="translate(15, 48)">
      <rect width="250" height="120" rx="7" fill="#0a1424" stroke="#ea580c" stroke-width="1.2"/>
      <rect x="10" y="10" width="24" height="24" rx="4" fill="#ea580c" opacity="0.2"/>
      <text x="22" y="27" fill="#fb923c" font-size="13" font-weight="bold" text-anchor="middle">🐙</text>
      <text x="40" y="26" fill="#fdba74" font-size="12.5" font-weight="700">ArgoCD GitOps</text>
      <rect x="165" y="10" width="75" height="18" rx="4" fill="#9a3412"/>
      <text x="202" y="23" fill="#ffedd5" font-size="9" font-weight="700" text-anchor="middle">ns: argocd</text>
      
      <text x="12" y="52" fill="#e2e8f0" font-size="10.5" font-weight="600">• Continuous Sync &amp; Self-Healing</text>
      <text x="12" y="68" fill="#94a3b8" font-size="10">• Auto-reverts manual out-of-band drifts</text>
      <text x="12" y="84" fill="#94a3b8" font-size="10">• AppSets: Jenkins, Tracker, Monitoring</text>
      <text x="12" y="102" fill="#38bdf8" font-size="9.5" font-weight="600">PDB Guardrail: minAvailable 1</text>
    </g>

    <!-- Sub-box: Jenkins HA Controller + JCasC -->
    <g transform="translate(280, 48)">
      <rect width="255" height="120" rx="7" fill="#0a1424" stroke="#f59e0b" stroke-width="1.2"/>
      <rect x="10" y="10" width="24" height="24" rx="4" fill="#f59e0b" opacity="0.2"/>
      <text x="22" y="27" fill="#fbbf24" font-size="13" font-weight="bold" text-anchor="middle">⚙️</text>
      <text x="40" y="26" fill="#fde68a" font-size="12.5" font-weight="700">Jenkins HA Controller</text>
      <rect x="175" y="10" width="70" height="18" rx="4" fill="#854d0e"/>
      <text x="210" y="23" fill="#fef9c3" font-size="9" font-weight="700" text-anchor="middle">ns: jenkins</text>
      
      <text x="12" y="52" fill="#e2e8f0" font-size="10.5" font-weight="600">• NumExecutors = 0 (Zero Master Builds)</text>
      <text x="12" y="68" fill="#94a3b8" font-size="10">• JCasC 100% Deterministic Rebuild</text>
      <text x="12" y="84" fill="#94a3b8" font-size="10">• Dynamic K8s Cloud Provider (Port 50000)</text>
      <text x="12" y="102" fill="#34d399" font-size="9.5" font-weight="600">Controller Reboot RTO &lt; 45s • PDB: 1</text>
    </g>

    <!-- Sub-box: Central Automation Tracker -->
    <g transform="translate(15, 178)">
      <rect width="520" height="106" rx="7" fill="#0a1424" stroke="#10b981" stroke-width="1.2"/>
      <rect x="10" y="10" width="24" height="24" rx="4" fill="#10b981" opacity="0.2"/>
      <text x="22" y="27" fill="#34d399" font-size="13" font-weight="bold" text-anchor="middle">📊</text>
      <text x="42" y="25" fill="#a7f3d0" font-size="12.5" font-weight="700">Central Automation Tracker (Backend &amp; Frontend)</text>
      <rect x="385" y="10" width="125" height="18" rx="4" fill="#065f46"/>
      <text x="447" y="23" fill="#d1fae5" font-size="9" font-weight="700" text-anchor="middle">ns: automation-tracker</text>

      <!-- Sub-elements: Backend & Frontend -->
      <g transform="translate(12, 40)">
        <rect width="240" height="54" rx="5" fill="#064e3b" opacity="0.25" stroke="#059669" stroke-width="0.8"/>
        <text x="10" y="18" fill="#6ee7b7" font-size="11" font-weight="700">FastAPI Telemetry API (Port 8000)</text>
        <text x="10" y="32" fill="#cbd5e1" font-size="9.5">2+ Replicas • PDB minAvailable: 2</text>
        <text x="10" y="46" fill="#38bdf8" font-size="9.5">POST /api/v1/runs • /health probe</text>
      </g>
      <g transform="translate(265, 40)">
        <rect width="245" height="54" rx="5" fill="#064e3b" opacity="0.25" stroke="#059669" stroke-width="0.8"/>
        <text x="10" y="18" fill="#6ee7b7" font-size="11" font-weight="700">Real-Time UI Dashboard (Port 3000)</text>
        <text x="10" y="32" fill="#cbd5e1" font-size="9.5">PDB: 1 • SQLite / EFS Persistent Volume</text>
        <text x="10" y="46" fill="#34d399" font-size="9.5">Prometheus Metrics Export: /metrics</text>
      </g>
    </g>
  </g>
''')

    # Box 3: Full Observability & Alerting Stack (Namespace: monitoring)
    svg.append('''
  <!-- BOX 3: Observability & Alerting Stack -->
  <g transform="translate(1080, 108)">
    <rect width="490" height="300" rx="10" fill="url(#card-grad-obs)" stroke="#9333ea" stroke-width="1.4" filter="url(#card-shadow)"/>
    <!-- Title Strip -->
    <path d="M 0 10 Q 0 0 10 0 L 480 0 Q 490 0 490 10 L 490 38 L 0 38 Z" fill="#200d3b"/>
    <text x="18" y="24" fill="#c084fc" font-size="12.5" font-weight="700" letter-spacing="0.5">📈 OBSERVABILITY &amp; INCIDENT ALERTING (MONITORING)</text>
    
    <!-- Prometheus -->
    <g transform="translate(15, 48)">
      <rect width="220" height="110" rx="7" fill="#110d24" stroke="#e11d48" stroke-width="1.1"/>
      <text x="12" y="22" fill="#fda4af" font-size="12" font-weight="700">🔥 Prometheus (Port 9090)</text>
      <text x="12" y="40" fill="#94a3b8" font-size="10">• 15s Scrapes across K8s, JCasC, Tracker</text>
      <text x="12" y="56" fill="#94a3b8" font-size="10">• Rule: JenkinsControllerDown</text>
      <text x="12" y="72" fill="#94a3b8" font-size="10">• Rule: KubernetesNodeNotReady</text>
      <text x="12" y="94" fill="#f43f5e" font-size="9.5" font-weight="600">PDB: minAvailable 1</text>
    </g>

    <!-- Alertmanager -->
    <g transform="translate(250, 48)">
      <rect width="225" height="110" rx="7" fill="#110d24" stroke="#ea580c" stroke-width="1.1"/>
      <text x="12" y="22" fill="#fdba74" font-size="12" font-weight="700">🚨 Alertmanager (Port 9093)</text>
      <text x="12" y="40" fill="#94a3b8" font-size="10">• HA Alert Deduplication &amp; Grouping</text>
      <text x="12" y="56" fill="#94a3b8" font-size="10">• Multi-Route Dispatcher</text>
      <text x="12" y="72" fill="#94a3b8" font-size="10">• SNS, Slack, Webhook &amp; Email</text>
      <text x="12" y="94" fill="#fb923c" font-size="9.5" font-weight="600">Repeat: 1h • Group Wait: 30s</text>
    </g>

    <!-- Grafana -->
    <g transform="translate(15, 168)">
      <rect width="220" height="116" rx="7" fill="#110d24" stroke="#f59e0b" stroke-width="1.1"/>
      <text x="12" y="22" fill="#fde68a" font-size="12" font-weight="700">📊 Grafana (Port 3001)</text>
      <text x="12" y="40" fill="#94a3b8" font-size="10">• Provisioned Datasources &amp; Dashboards</text>
      <text x="12" y="56" fill="#94a3b8" font-size="10">• HA Cluster Health &amp; Node Capacity</text>
      <text x="12" y="72" fill="#94a3b8" font-size="10">• QE Test Execution Pass/Fail Rates</text>
      <text x="12" y="96" fill="#fbbf24" font-size="9.5" font-weight="600">Credentials: admin / admin</text>
    </g>

    <!-- Loki & OpenTelemetry -->
    <g transform="translate(250, 168)">
      <rect width="225" height="116" rx="7" fill="#110d24" stroke="#06b6d4" stroke-width="1.1"/>
      <text x="12" y="22" fill="#a5f3fc" font-size="12" font-weight="700">📑 Loki + OpenTelemetry</text>
      <text x="12" y="40" fill="#94a3b8" font-size="10">• Promtail DaemonSet (Container logs)</text>
      <text x="12" y="56" fill="#94a3b8" font-size="10">• Loki Log Storage (Port 3100)</text>
      <text x="12" y="72" fill="#94a3b8" font-size="10">• OTel Collector: 4317 gRPC / 4318 HTTP</text>
      <text x="12" y="96" fill="#22d3ee" font-size="9.5" font-weight="600">Centralized QE Trace Ingestion</text>
    </g>
  </g>
''')

    # ROW 2: (Y: 428 to 718)
    # Box 4: Ephemeral Dynamic Kubernetes Agent Execution Grid (Multi-AZ)
    svg.append('''
  <!-- ======================== ROW 2: EXECUTION & DISASTER RECOVERY ======================== -->
  <!-- BOX 4: Dynamic Agent Execution Grid (Workers) -->
  <g transform="translate(30, 428)">
    <rect width="1030" height="290" rx="10" fill="url(#card-grad-agent)" stroke="#0e7490" stroke-width="1.4" filter="url(#card-shadow)"/>
    <!-- Title Strip -->
    <path d="M 0 10 Q 0 0 10 0 L 1020 0 Q 1030 0 1030 10 L 1030 38 L 0 38 Z" fill="#062836"/>
    <text x="18" y="24" fill="#38bdf8" font-size="12.5" font-weight="700" letter-spacing="0.5">⚡ DYNAMIC KUBERNETES AGENT EXECUTION GRID (MULTI-AZ RESILIENT WORKERS)</text>
    <rect x="730" y="8" width="285" height="22" rx="4" fill="#155e75"/>
    <text x="872" y="23" fill="#e0f2fe" font-size="10" font-weight="600" text-anchor="middle">Zero Permanent Agents • On-Demand Pod Spawning</text>

    <!-- Worker Zone A -->
    <g transform="translate(18, 48)">
      <rect width="315" height="185" rx="7" fill="#061922" stroke="#0284c7" stroke-width="1.1"/>
      <rect x="10" y="8" width="295" height="26" rx="5" fill="#075985" opacity="0.6"/>
      <text x="157" y="25" fill="#e0f2fe" font-size="11" font-weight="700" text-anchor="middle">Worker Node - Zone A (topology.kubernetes.io)</text>

      <!-- Pod Box -->
      <g transform="translate(12, 42)">
        <rect width="291" height="130" rx="6" fill="#092430" stroke="#38bdf8" stroke-dasharray="3,3" stroke-width="1"/>
        <text x="10" y="18" fill="#7dd3fc" font-size="11" font-weight="bold">Pod: qe-dynamic-agent-zone-a</text>
        
        <rect x="10" y="26" width="271" height="42" rx="4" fill="#04141c" stroke="#0369a1" stroke-width="0.8"/>
        <text x="16" y="42" fill="#bae6fd" font-size="10" font-weight="600">Container 1: jnlp (jenkins/inbound-agent)</text>
        <text x="16" y="58" fill="#94a3b8" font-size="9">Connects to Port 50000 • 500m CPU / 1Gi RAM</text>

        <rect x="10" y="74" width="271" height="44" rx="4" fill="#04141c" stroke="#0369a1" stroke-width="0.8"/>
        <text x="16" y="90" fill="#bae6fd" font-size="10" font-weight="600">Container 2: tools (alpine/k8s:1.30.2)</text>
        <text x="16" y="106" fill="#94a3b8" font-size="9">kubectl, helm, curl, git • 1-2 Core / 2-4Gi RAM</text>
      </g>
    </g>

    <!-- Worker Zone B -->
    <g transform="translate(355, 48)">
      <rect width="315" height="185" rx="7" fill="#061922" stroke="#0284c7" stroke-width="1.1"/>
      <rect x="10" y="8" width="295" height="26" rx="5" fill="#075985" opacity="0.6"/>
      <text x="157" y="25" fill="#e0f2fe" font-size="11" font-weight="700" text-anchor="middle">Worker Node - Zone B (topology.kubernetes.io)</text>

      <!-- Pod Box -->
      <g transform="translate(12, 42)">
        <rect width="291" height="130" rx="6" fill="#092430" stroke="#38bdf8" stroke-dasharray="3,3" stroke-width="1"/>
        <text x="10" y="18" fill="#7dd3fc" font-size="11" font-weight="bold">Pod: qe-dynamic-agent-zone-b</text>
        
        <rect x="10" y="26" width="271" height="42" rx="4" fill="#04141c" stroke="#0369a1" stroke-width="0.8"/>
        <text x="16" y="42" fill="#bae6fd" font-size="10" font-weight="600">Container 1: jnlp (jenkins/inbound-agent)</text>
        <text x="16" y="58" fill="#94a3b8" font-size="9">Connects to Port 50000 • 500m CPU / 1Gi RAM</text>

        <rect x="10" y="74" width="271" height="44" rx="4" fill="#04141c" stroke="#0369a1" stroke-width="0.8"/>
        <text x="16" y="90" fill="#bae6fd" font-size="10" font-weight="600">Container 2: tools (alpine/k8s:1.30.2)</text>
        <text x="16" y="106" fill="#94a3b8" font-size="9">kubectl, helm, curl, git • 1-2 Core / 2-4Gi RAM</text>
      </g>
    </g>

    <!-- Worker Zone C -->
    <g transform="translate(695, 48)">
      <rect width="315" height="185" rx="7" fill="#061922" stroke="#0284c7" stroke-width="1.1"/>
      <rect x="10" y="8" width="295" height="26" rx="5" fill="#075985" opacity="0.6"/>
      <text x="157" y="25" fill="#e0f2fe" font-size="11" font-weight="700" text-anchor="middle">Worker Node - Zone C (topology.kubernetes.io)</text>

      <!-- Pod Box -->
      <g transform="translate(12, 42)">
        <rect width="291" height="130" rx="6" fill="#092430" stroke="#38bdf8" stroke-dasharray="3,3" stroke-width="1"/>
        <text x="10" y="18" fill="#7dd3fc" font-size="11" font-weight="bold">Pod: qe-dynamic-agent-zone-c</text>
        
        <rect x="10" y="26" width="271" height="42" rx="4" fill="#04141c" stroke="#0369a1" stroke-width="0.8"/>
        <text x="16" y="42" fill="#bae6fd" font-size="10" font-weight="600">Container 1: jnlp (jenkins/inbound-agent)</text>
        <text x="16" y="58" fill="#94a3b8" font-size="9">Connects to Port 50000 • 500m CPU / 1Gi RAM</text>

        <rect x="10" y="74" width="271" height="44" rx="4" fill="#04141c" stroke="#0369a1" stroke-width="0.8"/>
        <text x="16" y="90" fill="#bae6fd" font-size="10" font-weight="600">Container 2: tools (alpine/k8s:1.30.2)</text>
        <text x="16" y="106" fill="#94a3b8" font-size="9">kubectl, helm, curl, git • 1-2 Core / 2-4Gi RAM</text>
      </g>
    </g>

    <!-- Bottom strip for HA Agent Grid -->
    <g transform="translate(18, 245)">
      <rect width="992" height="32" rx="6" fill="#05212c" stroke="#0e7490" stroke-width="1"/>
      <text x="20" y="20" fill="#67e8f9" font-size="11" font-weight="700">🛡️ HA Dynamic Agent Guarantees:</text>
      <text x="210" y="20" fill="#cbd5e1" font-size="10.5">TopologySpreadConstraints across 3 AZs</text>
      <text x="520" y="20" fill="#cbd5e1" font-size="10.5">• Ephemeral emptyDir (Zero residual state leak)</text>
      <text x="820" y="20" fill="#38bdf8" font-size="10.5" font-weight="600">• Auto-terminates upon completion</text>
    </g>
  </g>
''')

    # Box 5: Disaster Recovery & Storage Persistence
    svg.append('''
  <!-- BOX 5: Disaster Recovery, Storage & Resilience -->
  <g transform="translate(1080, 428)">
    <rect width="490" height="290" rx="10" fill="url(#card-grad-dr)" stroke="#7e22ce" stroke-width="1.4" filter="url(#card-shadow)"/>
    <!-- Title Strip -->
    <path d="M 0 10 Q 0 0 10 0 L 480 0 Q 490 0 490 10 L 490 38 L 0 38 Z" fill="#240c50"/>
    <text x="18" y="24" fill="#d8b4fe" font-size="12.5" font-weight="700" letter-spacing="0.5">💾 DISASTER RECOVERY &amp; STORAGE PERSISTENCE</text>
    
    <!-- Velero Backup Operator -->
    <g transform="translate(15, 48)">
      <rect width="460" height="106" rx="7" fill="#130b24" stroke="#a855f7" stroke-width="1.1"/>
      <text x="14" y="24" fill="#e9d5ff" font-size="12.5" font-weight="700">🔄 Velero Automated Backup Operator</text>
      <rect x="345" y="10" width="100" height="18" rx="4" fill="#6b21a8"/>
      <text x="395" y="23" fill="#f3e8ff" font-size="9" font-weight="700" text-anchor="middle">ns: velero-backup</text>
      
      <text x="14" y="46" fill="#cbd5e1" font-size="10.5">• Hourly Schedule Policy: "0 * * * *" • 7-Day Retention (168h)</text>
      <text x="14" y="64" fill="#94a3b8" font-size="10">• Namespaces: jenkins, argocd, automation-tracker, monitoring</text>
      <text x="14" y="82" fill="#94a3b8" font-size="10">• Automated DR Drills (dr-drill.sh) &amp; Restore Verification Tests</text>
      <text x="14" y="99" fill="#34d399" font-size="9.5" font-weight="600">Disaster Recovery RTO &lt; 45s Guaranteed</text>
    </g>

    <!-- Storage Targets -->
    <g transform="translate(15, 166)">
      <rect width="460" height="110" rx="7" fill="#130b24" stroke="#3b82f6" stroke-width="1.1"/>
      <text x="14" y="24" fill="#93c5fd" font-size="12.5" font-weight="700">🗄️ Multi-Cloud &amp; Local Storage Targets</text>
      
      <g transform="translate(12, 34)">
        <rect width="210" height="66" rx="5" fill="#0b1120" stroke="#1d4ed8" stroke-width="0.8"/>
        <text x="10" y="18" fill="#60a5fa" font-size="11" font-weight="600">AWS S3 &amp; Multi-AZ EFS</text>
        <text x="10" y="34" fill="#94a3b8" font-size="9.5">Artifacts &amp; Velero PV Snapshots</text>
        <text x="10" y="48" fill="#94a3b8" font-size="9.5">Server-Side Encryption + Versioning</text>
        <text x="10" y="60" fill="#38bdf8" font-size="9">EFS Mount across 3 Subnets</text>
      </g>

      <g transform="translate(235, 34)">
        <rect width="213" height="66" rx="5" fill="#0b1120" stroke="#0284c7" stroke-width="0.8"/>
        <text x="10" y="18" fill="#38bdf8" font-size="11" font-weight="600">Azure Blob &amp; LocalStack</text>
        <text x="10" y="34" fill="#94a3b8" font-size="9.5">GRS Geo-Redundant Storage</text>
        <text x="10" y="48" fill="#94a3b8" font-size="9.5">LocalStack S3 Bucket: qe-artifacts</text>
        <text x="10" y="60" fill="#2dd4bf" font-size="9">Azurite Storage Emulator</text>
      </g>
    </g>
  </g>
''')

    # ROW 3: (Y: 732 to 942)
    # Box 6: Downstream QE Clients & Telemetry Pipeline
    svg.append('''
  <!-- ======================== ROW 3: INGESTION & HA STANDARDS ======================== -->
  <!-- BOX 6: Downstream QE Frameworks & Telemetry Pipeline -->
  <g transform="translate(30, 732)">
    <rect width="750" height="210" rx="10" fill="#0f172a" stroke="#e11d48" stroke-width="1.4" filter="url(#card-shadow)"/>
    <!-- Title Strip -->
    <path d="M 0 10 Q 0 0 10 0 L 740 0 Q 750 0 750 10 L 750 36 L 0 36 Z" fill="#3b0714"/>
    <text x="18" y="23" fill="#fb7185" font-size="12.5" font-weight="700" letter-spacing="0.5">🧪 DOWNSTREAM QE CLIENTS &amp; TELEMETRY INGESTION PIPELINE</text>
    
    <!-- Test Frameworks -->
    <g transform="translate(18, 48)">
      <text x="0" y="13" fill="#cbd5e1" font-size="11" font-weight="600">Supported QE Test Frameworks:</text>
      <!-- Pills -->
      <g transform="translate(0, 22)">
        <rect width="130" height="26" rx="5" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
        <text x="65" y="17" fill="#7dd3fc" font-size="10" font-weight="600" text-anchor="middle">🎭 Playwright UI/API</text>

        <rect x="140" width="135" height="26" rx="5" fill="#1e293b" stroke="#f59e0b" stroke-width="1"/>
        <text x="207" y="17" fill="#fde68a" font-size="10" font-weight="600" text-anchor="middle">☕ Java TestNG / BOM</text>

        <rect x="285" width="120" height="26" rx="5" fill="#1e293b" stroke="#10b981" stroke-width="1"/>
        <text x="345" y="17" fill="#a7f3d0" font-size="10" font-weight="600" text-anchor="middle">🐍 Pytest Suites</text>

        <rect x="415" width="130" height="26" rx="5" fill="#1e293b" stroke="#a855f7" stroke-width="1"/>
        <text x="480" y="17" fill="#d8b4fe" font-size="10" font-weight="600" text-anchor="middle">🥒 Cucumber BDD</text>

        <rect x="555" width="155" height="26" rx="5" fill="#1e293b" stroke="#ec4899" stroke-width="1"/>
        <text x="632" y="17" fill="#fbcfe8" font-size="10" font-weight="600" text-anchor="middle">💥 Chaos &amp; DR Drills</text>
      </g>
    </g>

    <!-- CI Execution Triggers & Exporter -->
    <g transform="translate(18, 112)">
      <rect width="714" height="82" rx="7" fill="#14142b" stroke="#334155" stroke-width="1"/>
      <!-- Left side: scripts -->
      <g transform="translate(14, 12)">
        <text x="0" y="14" fill="#f8fafc" font-size="11" font-weight="700">Pipeline Execution Runners:</text>
        <text x="0" y="32" fill="#38bdf8" font-size="10" font-family="monospace">ci/scripts/jenkins-agent-run.sh &lt;suite&gt;</text>
        <text x="0" y="48" fill="#94a3b8" font-size="10" font-family="monospace">ci/scripts/github-actions-run.sh</text>
        <text x="0" y="64" fill="#94a3b8" font-size="10" font-family="monospace">ci/scripts/local-run.sh</text>
      </g>
      <!-- Middle Arrow -->
      <g transform="translate(370, 24)">
        <path d="M 0 16 L 35 16" stroke="#fb7185" stroke-width="2" marker-end="url(#arrow-rose)"/>
        <text x="18" y="8" fill="#fda4af" font-size="8.5" text-anchor="middle">Push Telemetry</text>
      </g>
      <!-- Right side: Exporter -->
      <g transform="translate(425, 12)">
        <text x="0" y="14" fill="#f8fafc" font-size="11" font-weight="700">qe-telemetry-exporter.py</text>
        <text x="0" y="30" fill="#cbd5e1" font-size="10">• Auto-parses test execution results</text>
        <text x="0" y="46" fill="#cbd5e1" font-size="10">• Dispatches HTTP JSON payload to Tracker</text>
        <text x="0" y="62" fill="#34d399" font-size="9.5" font-weight="600">POST /api/v1/runs (Status, Counts, Latency)</text>
      </g>
    </g>
  </g>
''')

    # Box 7: HA Principles & Architecture Flow Legend
    svg.append('''
  <!-- BOX 7: HA Principles & Architecture Flow Legend -->
  <g transform="translate(800, 732)">
    <rect width="770" height="210" rx="10" fill="#0f172a" stroke="#059669" stroke-width="1.4" filter="url(#card-shadow)"/>
    <!-- Title Strip -->
    <path d="M 0 10 Q 0 0 10 0 L 760 0 Q 770 0 770 10 L 770 36 L 0 36 Z" fill="#043a2c"/>
    <text x="18" y="23" fill="#6ee7b7" font-size="12.5" font-weight="700" letter-spacing="0.5">🛡️ ARCHITECTURAL FLOW LEGEND &amp; HA RESILIENCE GUARANTEES</text>

    <!-- Flow Legend -->
    <g transform="translate(20, 50)">
      <text x="0" y="10" fill="#cbd5e1" font-size="11" font-weight="700">Platform Interaction Flows:</text>

      <g transform="translate(0, 22)">
        <!-- Flow 1 -->
        <line x1="0" y1="8" x2="35" y2="8" stroke="#fb923c" stroke-width="2.2" stroke-dasharray="4,3"/>
        <text x="45" y="12" fill="#fdba74" font-size="10.5" font-weight="600">GitOps Auto-Sync &amp; Drift Self-Heal</text>
        <text x="245" y="12" fill="#94a3b8" font-size="10">(ArgoCD ➔ Jenkins / Tracker / Monitoring)</text>
        
        <!-- Flow 2 -->
        <g transform="translate(0, 24)">
          <line x1="0" y1="8" x2="35" y2="8" stroke="#38bdf8" stroke-width="2.2"/>
          <text x="45" y="12" fill="#7dd3fc" font-size="10.5" font-weight="600">Dynamic Pod Execution Grid</text>
          <text x="245" y="12" fill="#94a3b8" font-size="10">(Jenkins Controller ➔ Multi-Zone Dynamic Pods)</text>
        </g>

        <!-- Flow 3 -->
        <g transform="translate(0, 48)">
          <line x1="0" y1="8" x2="35" y2="8" stroke="#34d399" stroke-width="2.2"/>
          <text x="45" y="12" fill="#6ee7b7" font-size="10.5" font-weight="600">Telemetry &amp; Metrics Export</text>
          <text x="245" y="12" fill="#94a3b8" font-size="10">(Agents / Downstream ➔ Tracker API ➔ Prometheus)</text>
        </g>

        <!-- Flow 4 -->
        <g transform="translate(0, 72)">
          <line x1="0" y1="8" x2="35" y2="8" stroke="#a855f7" stroke-width="2.2" stroke-dasharray="4,3"/>
          <text x="45" y="12" fill="#d8b4fe" font-size="10.5" font-weight="600">Hourly Velero State Snapshots</text>
          <text x="245" y="12" fill="#94a3b8" font-size="10">(K8s Namespaces &amp; PVs ➔ S3 / Azure Blob GRS)</text>
        </g>
      </g>
    </g>

    <!-- HA Pillars Box -->
    <g transform="translate(520, 45)">
      <rect width="230" height="152" rx="7" fill="#03201e" stroke="#10b981" stroke-width="1"/>
      <text x="115" y="22" fill="#34d399" font-size="11" font-weight="700" text-anchor="middle">KEY HA METRICS &amp; SLA</text>
      
      <g transform="translate(14, 36)">
        <text x="0" y="12" fill="#f8fafc" font-size="10" font-weight="600">⏱️ RTO: &lt; 45 Seconds</text>
        <text x="0" y="26" fill="#94a3b8" font-size="9">JCasC + Velero fast reboot</text>

        <text x="0" y="44" fill="#f8fafc" font-size="10" font-weight="600">🏛️ etcd HA Quorum</text>
        <text x="0" y="58" fill="#94a3b8" font-size="9">3 Control-Planes withstand node loss</text>

        <text x="0" y="76" fill="#f8fafc" font-size="10" font-weight="600">🔒 100% Workload Isolation</text>
        <text x="0" y="90" fill="#94a3b8" font-size="9">Zero builds execute on Jenkins master</text>

        <text x="0" y="108" fill="#38bdf8" font-size="9.5" font-weight="600">🔄 Auto-Drift Correction</text>
      </g>
    </g>
  </g>
''')

    # Visual Flow Connectors
    svg.append('''
  <!-- ======================== ARCHITECTURAL CONNECTORS ======================== -->
  <g>
    <!-- Flow 1: ArgoCD -> Jenkins Controller (GitOps Sync & Drift Reconciliation) -->
    <path d="M 760 190 L 790 190" fill="none" stroke="#fb923c" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrow-orange)"/>
    <rect x="762" y="176" width="26" height="12" rx="2" fill="#7c2d12"/>
    <text x="775" y="185" fill="#ffedd5" font-size="7" font-weight="700" text-anchor="middle">SYNC</text>

    <!-- Flow 2: Jenkins HA Controller -> Dynamic Agent Grid (Multi-Node Spawning) -->
    <path d="M 915 278 L 915 350 L 545 350 L 545 428" fill="none" stroke="#38bdf8" stroke-width="2.4" marker-end="url(#arrow-blue)"/>
    <rect x="670" y="340" width="190" height="20" rx="4" fill="#0c4a6e" stroke="#0284c7" stroke-width="0.8"/>
    <text x="765" y="354" fill="#e0f2fe" font-size="9.5" font-weight="600" text-anchor="middle">Spawns Ephemeral Agent Pods (JCasC)</text>

    <!-- Flow 3: Dynamic Agents -> Central Automation Tracker (Telemetry Ingestion) -->
    <path d="M 370 428 L 370 380 L 525 380" fill="none" stroke="#34d399" stroke-width="2" marker-end="url(#arrow-green)"/>
    <rect x="385" y="370" width="130" height="18" rx="4" fill="#064e3b" stroke="#059669" stroke-width="0.8"/>
    <text x="450" y="383" fill="#d1fae5" font-size="9" font-weight="600" text-anchor="middle">HTTP POST Telemetry</text>

    <!-- Flow 4: Prometheus -> Jenkins & Tracker (Scrapes Health & Metrics) -->
    <path d="M 1095 210 L 1050 210" fill="none" stroke="#f43f5e" stroke-width="2" marker-end="url(#arrow-purple)"/>
    <path d="M 1095 330 L 1045 330" fill="none" stroke="#f43f5e" stroke-width="2" marker-end="url(#arrow-purple)"/>

    <!-- Flow 5: Velero -> Storage Targets (Hourly Snapshots) -->
    <path d="M 1320 584 L 1320 594" fill="none" stroke="#a855f7" stroke-width="2" stroke-dasharray="4,3" marker-end="url(#arrow-purple)"/>

    <!-- Flow 6: Downstream Pipelines -> Dynamic Agents (Test Trigger) -->
    <path d="M 380 732 L 380 718" fill="none" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow-blue)"/>
  </g>
''')

    # Footer Strip
    svg.append('''
  <!-- ======================== FOOTER STRIP ======================== -->
  <g transform="translate(30, 960)">
    <rect width="1540" height="58" rx="8" fill="#111827" stroke="#1f2937" stroke-width="1"/>
    <text x="25" y="25" fill="#94a3b8" font-size="11" font-weight="600">HIGHLY AVAILABLE QUALITY ENGINEERING PLATFORM BLUEPRINT</text>
    <text x="25" y="42" fill="#64748b" font-size="10">Repository: github.com/adarshashetty/highly-available-qe-setup • Verified Multi-Cloud, GitOps, Kubernetes HA, and Resilience Standards</text>
    <text x="1515" y="34" fill="#38bdf8" font-size="10.5" font-weight="600" text-anchor="end">Status: Active &amp; Production Verified • Multi-AZ / Multi-Cloud Ready</text>
  </g>
''')

    svg.append('</svg>')
    return '\n'.join(svg)

if __name__ == '__main__':
    content = create_svg()
    with open('docs/architecture/ha-qe-architecture.svg', 'w') as f:
        f.write(content)
    with open('ha-qe-architecture.svg', 'w') as f:
        f.write(content)
    print("SVG generated successfully at docs/architecture/ha-qe-architecture.svg and ha-qe-architecture.svg")
