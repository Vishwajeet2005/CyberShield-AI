<div align="center">

<img src="https://img.shields.io/badge/CyberShield_AI-v1.0.0-00d4ff?style=for-the-badge&logo=shield&logoColor=white"/>
<img src="https://img.shields.io/badge/ET_AI_Hackathon_2026-Problem_7-ff3366?style=for-the-badge"/>
<img src="https://img.shields.io/badge/India_CNI-Cyber_Resilience-00ff88?style=for-the-badge"/>

<br/>

```
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗██╗  ██╗██╗███████╗██╗     ██████╗      █████╗ ██╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗    ██╔══██╗██║
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗███████║██║█████╗  ██║     ██║  ██║    ███████║██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║    ██╔══██║██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║██║  ██║██║███████╗███████╗██████╔╝    ██║  ██║██║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝     ╚═╝  ╚═╝╚═╝
```

### 🛡️ AI-Powered Cyber Resilience Platform for India's Critical National Infrastructure

**ET AI Hackathon 2026 · Problem Statement 7 · Team Submission**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)](https://pytorch.org)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.x-008CC1?style=flat-square&logo=neo4j&logoColor=white)](https://neo4j.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## 🔥 New Live Prototype Features
*   **Fully Functional SOC-PRIME UI**: A cohesive, cyberpunk-styled interface across all modules with real-time React state management.
*   **Groq + Chroma DB RAG Pipeline**: The AAPA module dynamically attributes Threat Actors using a local STIX knowledge base and LLaMA 3 via Groq for high-speed AI reasoning.
*   **High-Volume Stress Testing**: A live stress-test generator that blasts 500+ asynchronous attacks at the FastAPI backend to prove robust state management.
*   **Automated CERT-In Reporting**: The AIRO module generates compliant, exportable `.txt` incident reports for the Indian government.

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution Overview](#-solution-overview)
- [Platform Architecture](#-platform-architecture)
- [Modules](#-modules)
  - [BADE — Behavioural Anomaly Detection Engine](#module-1-bade--behavioural-anomaly-detection-engine)
  - [AAPA — APT Attribution & Prediction Agent](#module-2-aapa--apt-attribution--prediction-agent)
  - [AIRO — Autonomous Incident Response Orchestrator](#module-3-airo--autonomous-incident-response-orchestrator)
  - [VPA — Vulnerability Prioritisation Agent](#module-4-vpa--vulnerability-prioritisation-agent)
  - [CRDT — Cyber Resilience Digital Twin](#module-5-crdt--cyber-resilience-digital-twin)
- [Key Metrics](#-key-metrics)
- [Datasets Used](#-datasets-used)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Demo Scenarios](#-demo-scenarios)
- [Security & Compliance](#-security--compliance)
- [Scalability](#-scalability)
- [Team](#-team)

---

## Problem Statement

India's Critical National Infrastructure (CNI) — hospitals, power grids, educational institutions, financial systems — is under **sustained, sophisticated cyberattack**.

| Statistic | Impact |
|-----------|--------|
| **1.59M+** incidents handled by CERT-In in 2023 | Unprecedented scale |
| **AIIMS Delhi** paralysed for 2 weeks (ransomware, Nov 2022) | Patient lives at risk |
| **CBSE** attacked ahead of board exams (2026) | Student data of millions compromised |
| **70%+** of govt entities run on end-of-life IT | Massive unpatched attack surface |
| **Weeks to months** average breach detection time | Attackers operate undetected |

**The core gap**: Signature-based tools cannot detect APTs (Advanced Persistent Threats) that operate at low-and-slow speeds, blend into normal traffic, and exploit legitimate credentials. By the time a breach is discovered, the damage is done.

---

## 💡 Solution Overview

**CyberShield AI** is a **multi-agent autonomous cybersecurity platform** that compresses Mean Time to Detect (MTTD) and Mean Time to Respond (MTTR) from **weeks to hours** through **behavioural intelligence**, not signatures.

```
Traditional SIEM:  Detection in weeks  →  Response in days   ❌
CyberShield AI:    Detection in minutes →  Containment in 30s ✅
```

### What makes it different

| Capability | Traditional SOC | CyberShield AI |
|-----------|-----------------|----------------|
| Detection Method | Signature/rule-based | Behavioural ML + Graph Analytics |
| APT Detection | Misses low-and-slow | Detects via deviation from 30-day baseline |
| Response Time | Human-driven (hours-days) | Autonomous playbook (< 30 seconds) |
| OT/SCADA Coverage | Rarely supported | Passive monitoring via data diode |
| Attribution | Manual threat intel lookup | Automated MITRE ATT&CK TTP matching |
| Audit Trail | Log files (mutable) | Immutable hash-chained evidence vault |
| India Compliance | Generic | CERT-In Directions 2022, DPDP Act 2023, IT Act 2000 |

---

## 🏗️ Platform Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              CYBERSHIELD AI — 5-LAYER ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  LAYER 5 │ PRESENTATION                                                             │
│          │  React SOC Dashboard  │  Digital Twin Viewer  │  Executive Dashboard    │
│          │  Investigation Workbench  │  Mobile Approval App (iOS/Android)           │
├──────────┼──────────────────────────────────────────────────────────────────────────┤
│  LAYER 4 │ RESPONSE ORCHESTRATION                                                   │
│          │  AIRO Playbook Engine  →  Approval Workflow  →  Action Adapters          │
│          │  Immutable Evidence Vault (Hash-Chained Audit Log)                       │
├──────────┼──────────────────────────────────────────────────────────────────────────┤
│  LAYER 3 │ INTELLIGENCE ENGINES                                                     │
│          │  BADE (Anomaly)  │  AAPA (Attribution)  │  VPA (Vulns)  │  CRDT (Twin)  │
│          │  ←────────── Kafka Event Bus (100K+ events/sec) ──────────→              │
├──────────┼──────────────────────────────────────────────────────────────────────────┤
│  LAYER 2 │ DATA PIPELINE                                                            │
│          │  Apache Kafka  →  Normalisation & Enrichment  →  ClickHouse + Neo4j     │
├──────────┼──────────────────────────────────────────────────────────────────────────┤
│  LAYER 1 │ DATA COLLECTION                                                          │
│          │  Endpoint Agents  │  Network TAP/SPAN  │  OT Data Diodes                │
│          │  SIEM Connectors  │  Cloud APIs (AWS/Azure/GCP)                          │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Multi-Agent Coordination

```
                    ┌─────────────────────┐
                    │  Coordinator Agent  │
                    │  (Kafka Event Bus)  │
                    └──────────┬──────────┘
          ┌───────────┬────────┴────────┬───────────┐
          ▼           ▼                 ▼           ▼
       ┌──────┐  ┌──────┐         ┌──────┐    ┌──────┐
       │ BADE │  │ AAPA │         │  VPA │    │ CRDT │
       └──┬───┘  └──┬───┘         └──────┘    └──────┘
          │         │
          └────┬────┘
               ▼
           ┌──────┐
           │ AIRO │  ← Playbook Engine
           └──────┘
```

---

## 📦 Modules

---

### Module 1: BADE — Behavioural Anomaly Detection Engine

> *Detects the undetectable — APT behaviour without signatures*

**Purpose**: Build multi-dimensional behavioural baselines for all monitored entities (users, devices, service accounts, network segments) and score deviations in real time without relying on known malware signatures.

#### How It Works

```
Entity Activity Logs
        │
        ▼
┌───────────────────┐     ┌──────────────────────┐
│  30-Day Rolling   │────▶│  Isolation Forest +  │
│  Baseline Builder │     │  LSTM Autoencoder    │
└───────────────────┘     └──────────┬───────────┘
                                     │
                          ┌──────────▼───────────┐
                          │  Deviation Score 0-100│
                          │  Updated every 60s    │
                          └──────────┬───────────┘
                                     │
                     ┌───────────────┼───────────────┐
                     ▼               ▼               ▼
                 Score < 30      30-70 range      Score > 70
                 (Normal)        (Monitor)        (ALERT)
```

#### Key Features

- **30-day rolling baseline** per entity using statistical + ML models
- **Real-time deviation scoring** (0–100) every 60 seconds
- **12-dimensional feature vector** per entity: login patterns, bytes transferred, unique destinations, privilege usage, off-hours activity, process creations, DNS queries, lateral connections, file operations, port scans, failed authentications, credential usage
- **OT/SCADA passive monitoring** (Modbus, DNP3, IEC 61850, OPC-UA) via data diode — no active probing
- **Lateral movement detection** via entity correlation graph (PyTorch Geometric)
- **Analyst feedback loop** (TP/FP) for continuous model refinement
- **Peer group comparison**: entities compared to similar entities, not global baseline (reduces FP)

#### ML Models

| Model | Purpose | Dataset |
|-------|---------|---------|
| Isolation Forest | Real-time outlier scoring | CICIDS 2017/2018, UNSW-NB15 |
| LSTM Autoencoder | Time-series reconstruction error | LANL Cyber Dataset |
| Graph Neural Network | Lateral movement path detection | DARPA OpTC |
| Statistical Baseline | Per-entity normal ranges | CERT Insider Threat Dataset |

#### Performance Targets

- **True Positive Rate**: > 80% on CICIDS 2017 benchmark
- **False Positive Rate**: < 5%
- **Detection Latency**: P99 < 5 seconds from event ingestion to SOC alert
- **Throughput**: 100,000+ events/second per node

---

### Module 2: AAPA — APT Attribution & Prediction Agent

> *Knows your adversary before they make their next move*

**Purpose**: Map observed attack patterns to MITRE ATT&CK threat actor profiles, generate ranked attribution hypotheses, and predict the attacker's next moves using Markov chain modelling.

#### How It Works

```
Observed TTPs (from BADE alerts)
        │
        ▼
┌───────────────────────────────────────────┐
│  MITRE ATT&CK Knowledge Graph (Neo4j)    │
│  700+ techniques, Enterprise+ICS+Mobile  │
└──────────────────────┬────────────────────┘
                       │
        ┌──────────────▼──────────────┐
        │  Cosine Similarity Matching │
        │  Observed TTP Vector vs     │
        │  Known Actor Profiles       │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │  Attribution Ranking        │
        │  APT41: 91% confidence      │
        │  Lazarus: 67% confidence    │
        │  SideWinder: 43% confidence │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │  Markov Chain Next-Move     │
        │  Prediction                 │
        │  Next: T1486 (Ransomware)   │
        │  Prob: 0.73                 │
        └─────────────────────────────┘
```

#### Key Features

- **Full MITRE ATT&CK v14+ knowledge graph** in Neo4j (Enterprise + ICS + Mobile, ~700 techniques)
- **Cosine similarity matching** of observed TTP vector against 4 known India-targeting actor profiles
- **Markov chain campaign modelling** for next-move prediction with probability scores
- **RAG-powered threat intelligence Q&A** over CERT-In advisories + CTI report corpus (Groq/Mistral + Qdrant)
- **India-specific threat actor focus**: APT41, Lazarus Group, SideWinder, Transparent Tribe

#### Tracked Threat Actors

| Actor | Origin | Targets in India | Known Campaigns |
|-------|--------|-----------------|-----------------|
| **APT41** | China | Telecom, Healthcare, Finance | Operation CuckooBees, ShadowPad India 2024 |
| **Lazarus Group** | DPRK | Banks, Crypto, Defence | AppleJeus India 2023, TraderTraitor Banking |
| **SideWinder** | — | Military, Government | Operation Sidewind 2023, CBSE Data Exfil 2026 |
| **Transparent Tribe** | Pakistan | Defence, Education | Operation Crimson 2024, Education Sector 2026 |

#### Performance Targets

- **Attribution Accuracy**: > 70% at MITRE ATT&CK technique level
- **Attribution Latency**: < 10 seconds from TTP submission

---

### Module 3: AIRO — Autonomous Incident Response Orchestrator

> *30-second containment. Zero blast radius surprises.*

**Purpose**: Execute pre-approved containment playbooks within 30 seconds of high-confidence threat confirmation. Human approval is always required for high-blast-radius actions. Every action is immutably logged.

#### Blast Radius Classification

```
┌─────────────────────────────────────────────────────────────┐
│                    BLAST RADIUS TIERS                        │
├──────────────┬──────────────────────────────────────────────┤
│  🟢 LOW      │  Auto-execute immediately                    │
│              │  Examples: block IP, revoke session token,   │
│              │  disable single account                      │
├──────────────┼──────────────────────────────────────────────┤
│  🟡 MEDIUM   │  Execute + notify SOC analyst                │
│              │  Examples: isolate endpoint, snapshot VM,    │
│              │  force password reset                        │
├──────────────┼──────────────────────────────────────────────┤
│  🔴 HIGH     │  Require human approval (NEVER auto-execute) │
│              │  Examples: segment isolation, OT shutdown,   │
│              │  full domain lockdown                        │
│              │  10-min primary timeout → secondary escalate │
└──────────────┴──────────────────────────────────────────────┘
```

#### Playbook Library (50+ templates)

| # | Playbook | Trigger | Auto Steps |
|---|----------|---------|-----------|
| 1 | Ransomware Response | Encryption activity + C2 beacon | Isolate endpoint, block C2, snapshot VMs |
| 2 | Lateral Movement Containment | Cross-segment auth + BADE alert | Block source IP, revoke sessions |
| 3 | Data Exfiltration Response | Large egress anomaly | Block egress IPs, capture packets |
| 4 | Credential Compromise | Failed logins + credential dump | Disable account, revoke all sessions |
| 5 | OT Sabotage Response | ICS command anomaly | OT isolation, switch to manual |
| 6 | Phishing Response | Malicious email + click detected | Quarantine email, block sender domain |
| 7 | Privilege Escalation | Unexpected privilege gain | Revoke elevated privileges |
| 8 | Supply Chain Compromise | Backdoored package detected | Block package, rollback deployments |

#### Key Features

- **30-second SLA** from trigger to Low blast-radius action execution
- **One-click rollback** for every automated action (stored in evidence vault)
- **Auto-generates CERT-In format incident report** within 10 minutes of confirmation
- **Immutable evidence vault**: append-only hash-chained audit log, court-admissible
- **SOAR adapters**: Palo Alto XSOAR, Splunk SOAR, CrowdStrike Falcon, SentinelOne

#### Audit Log — Hash Chain Design

```
Entry N:  { action, actor, target, result, timestamp }
          hash_N = SHA256(hash_{N-1} + serialize(Entry_N))
          
Entry N+1: hash_{N+1} = SHA256(hash_N + serialize(Entry_{N+1}))

Any tampering of Entry K invalidates all entries K..N → instantly detectable
```

---

### Module 4: VPA — Vulnerability Prioritisation Agent

> *Not all CVEs are equal. Know which ones will kill you first.*

**Purpose**: Continuously map asset inventory against live CVE feeds and compute context-aware exploitability scores — not raw CVSS — generating a dynamic risk-ranked remediation queue that accounts for actual threat actor targeting and compensating controls.

#### Context-Aware Scoring Formula

```
Context Score = CVSS_Base × 10
              + (network_exposed ? +15 : 0)
              + (actor_targeted  ? +20 : 0)
              + (CISA_KEV_flag   ? max priority : 0)
              - (compensating_control ? -10 to -20 : 0)

Clamped to [0, 100]

Priority:  CRITICAL (>85) | HIGH (70-85) | MEDIUM (50-70) | LOW (<50)
```

#### Live Data Sources

| Source | URL | Update Frequency | Data |
|--------|-----|-----------------|------|
| **NVD CVE API v2.0** | services.nvd.nist.gov | Every 6 hours | 220,000+ CVEs with CVSS |
| **CISA KEV Feed** | cisa.gov/known-exploited-vulnerabilities | Daily | 1,100+ actively exploited CVEs |
| **ExploitDB** | exploit-db.com | Continuous | Public exploit code |
| **MISP** | misp-project.org | Real-time | STIX 2.1 community threat feeds |

#### Key Features

- **Asset discovery**: passive network observation + agent inventory, detects new assets within 15 minutes
- **Emergency escalation**: any CVE hitting CISA KEV list triggers immediate SOC alert
- **Auto-creates remediation tickets** in ServiceNow/Jira with priority and patch guidance
- **Compensating control credit**: firewall rules, network segmentation, MFA reduce effective risk score

---

### Module 5: CRDT — Cyber Resilience Digital Twin

> *Attack your own network safely. Fix it before the adversary finds it.*

**Purpose**: Maintain a live logical model of the organisation's network topology, trust boundaries, and security control positions — enabling attack path modelling, red team simulation, and security investment impact assessment WITHOUT touching production systems.

#### Network Graph Model

```
Nodes = Assets (servers, workstations, OT devices, cloud resources)
        attributes: {ip, os, vulnerabilities[], controls[], criticality}

Edges = Network paths
        attributes: {protocol, port, encrypted, firewall_protected}

Attack Path = Sequence of nodes/edges an attacker traverses
              Risk Score = Σ(node_vulnerabilities) / Σ(edge_controls)
```

#### Key Features

- **Directed attack graph** with 30+ node CNI topology (hospital/government simulation)
- **Attack path enumeration**: all paths from entry point to crown jewel asset, ranked by attacker effort
- **Chokepoint identification**: nodes/controls whose removal breaks ALL attack paths (critical to protect)
- **20+ pre-built red team scenarios**: ransomware, supply chain, insider, OT pivot, APT campaign
- **Custom scenario builder** using ATT&CK TTP selection
- **Live sync** with VPA asset/vulnerability data every 4 hours
- **Interactive D3.js visualisation** with zoom, pan, click-to-inspect

#### Pre-Built Scenarios

| Scenario | Entry Point | Target (Crown Jewel) |
|----------|------------|---------------------|
| 🔴 Ransomware | DMZ Web Server | Backup Server |
| 🟠 Lateral Movement | HR Workstation | Domain Controller |
| 🔴 OT Pivot | Corporate Network | SCADA Server |
| 🟠 Supply Chain | Cloud Connector | Patient/Student DB |
| 🔴 Insider Threat | Finance Workstation | Database Server |

---

## 📊 Key Metrics

| Metric | Target | Method |
|--------|--------|--------|
| **MTTD** | < 1 hour (vs industry avg 21 days) | BADE continuous scoring |
| **MTTR** | < 2 hours (vs industry avg 76 days) | AIRO automated playbooks |
| **True Positive Rate** | > 80% | BADE on CICIDS 2017/UNSW-NB15 |
| **False Positive Rate** | < 5% | Peer grouping + analyst feedback |
| **Attribution Accuracy** | > 70% | AAPA at ATT&CK technique level |
| **Containment Time** | < 30 seconds | AIRO Low blast-radius actions |
| **Incident Report** | < 10 minutes | AIRO auto-generation |
| **Alert Throughput** | P99 < 5 seconds | Kafka + ClickHouse pipeline |
| **Audit Coverage** | 100% | Hash-chained immutable log |

---

## 🗂️ Datasets Used

### IT/Network Datasets

| Dataset | Source | Purpose | Size |
|---------|--------|---------|------|
| **CICIDS 2017/2018** | Canadian Institute for Cybersecurity | BADE training (labelled network attacks) | ~50GB |
| **UNSW-NB15** | UNSW Canberra | BADE training (9 modern attack categories) | ~100MB |
| **LANL Cyber Dataset** | Los Alamos National Lab | UEBA baseline (real Windows auth + process logs, 12K machines) | ~12GB |
| **CERT Insider Threat** | Carnegie Mellon CERT | BADE training (insider threat scenarios) | ~1GB |
| **DARPA OpTC** | DARPA / MITRE | Endpoint telemetry from red team exercise | ~1TB |
| **BETH Dataset** | Bosch / Cambridge | Honeypot logs for anomaly benchmarking | ~2GB |

### OT/SCADA Datasets

| Dataset | Source | Purpose |
|---------|--------|---------|
| **SWaT Dataset** | iTrust, Singapore | Real water treatment plant with planted attacks |
| **BATADAL** | Academic consortium | Water distribution system attacks |

### Threat Intelligence

| Dataset | Source | Purpose |
|---------|--------|---------|
| **MITRE ATT&CK STIX v14** | MITRE Corporation | ATT&CK knowledge graph (free) |
| **CERT-In Advisories** | CERT-In | India-specific threat data (public PDFs) |
| **MISP Feeds** | MISP Community | STIX 2.1 IOC feeds |
| **MalwareBazaar** | abuse.ch | Malware samples with actor attribution |
| **CISA KEV** | CISA | 1,100+ actively exploited CVEs (live feed) |
| **NVD CVE** | NIST | 220,000+ CVEs with CVSS (live API) |
| **CTI Reports** | Mandiant, CrowdStrike, Secureworks | RAG corpus for threat Q&A |

### Live API Integrations (No Download Required)

- 🔴 **CISA KEV**: `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`
- 🔵 **NVD API v2.0**: `https://services.nvd.nist.gov/rest/json/cves/2.0`
- 🟢 **MITRE ATT&CK**: `https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json`

---

## 🛠️ Tech Stack

### AI/ML Layer

| Technology | Version | Use |
|-----------|---------|-----|
| **PyTorch** | 2.x | LSTM Autoencoder, GNN models |
| **scikit-learn** | 1.4 | Isolation Forest, statistical models |
| **PyTorch Geometric** | 2.x | Graph-based lateral movement detection |
| **HuggingFace Transformers** | 4.x | NLP embeddings for AAPA |
| **NumPy / SciPy** | Latest | Cosine similarity, Markov chains |

### LLM / RAG Layer

| Technology | Use |
|-----------|-----|
| **Groq Llama 3 70B** | Threat Q&A generation, incident report writing |
| **Qdrant / Weaviate** | Vector store for CTI report corpus |
| **LangChain** | RAG pipeline orchestration |

### Graph & Storage

| Technology | Use |
|-----------|-----|
| **Neo4j 5.x** | ATT&CK knowledge graph, asset-CVE graph |
| **ClickHouse** | Time-series event storage (100K+ events/sec) |
| **PostgreSQL** | Relational data (incidents, users, config) |
| **Apache Kafka** | Event streaming bus between agents |
| **S3-compatible** | Evidence vault (WORM bucket) |
| **NetworkX** | CRDT attack path graph (Python) |

### Backend

| Technology | Use |
|-----------|-----|
| **FastAPI** | REST API gateway (Python) |
| **Temporal / Airflow** | Playbook workflow orchestration |
| **Redis** | Caching, session state |
| **HashiCorp Vault** | Secrets management (no credentials in config) |

### Frontend

| Technology | Use |
|-----------|-----|
| **React 18** | UI framework |
| **TypeScript 5** | Type safety |
| **Vite** | Build tool |
| **Tailwind CSS** | Styling |
| **D3.js** | Digital Twin attack graph visualisation |
| **Recharts** | Metric charts and trend graphs |
| **Lucide React** | Icon library |

### Infrastructure

| Technology | Use |
|-----------|-----|
| **Docker / Docker Compose** | Local development |
| **Kubernetes** | Production deployment (horizontal scaling) |
| **Prometheus + Grafana** | Observability |
| **mTLS** | Inter-service security |
| **AES-256 / TLS 1.3** | Data encryption |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (for Neo4j, ClickHouse)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Vishwajeet2005/cyber-resilience-.git
cd cyber-resilience-
```

### 2. Start Infrastructure Services

```bash
docker-compose up -d
# Starts: Neo4j, ClickHouse, PostgreSQL, Redis, Kafka
```

### 3. Set Up the Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:
```env
# Optional but highly recommended for AAPA RAG pipeline
GROQ_API_KEY=your_groq_key_here
# Optional: get free key at nvd.nist.gov/developers
NVD_API_KEY=           
CERT_IN_ORG=AIIMS Delhi
```

Start the backend:
```bash
uvicorn main:app --reload --port 8000
```

Backend API docs available at: `http://localhost:8000/docs`

### 4. Set Up the Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend available at: `http://localhost:5173`

### 5. Trigger the Demo Scenario

```bash
# In a separate terminal
python demo/trigger_lateral_movement.py
```

This simulates an APT41 lateral movement attack through the AIIMS network and demonstrates:
1. **BADE** detecting anomalous behaviour within 60 seconds
2. **AAPA** attributing to APT41 with 91% confidence
3. **AIRO** generating an automated containment playbook (High Blast Radius requiring Approval)
4. **Audit Log** immutably recording the event

### 6. Run the Ultimate Stress Test

To prove the prototype's resilience, open a new terminal and run:

```bash
python demo/stress_test.py
```
This floods the FastAPI backend with **500 concurrent, asynchronous attack incidents**, proving that the React UI and backend state manager will not crash under extreme load.

---

## 📁 Project Structure

```
cyber-resilience-/
│
├── backend/                        # FastAPI Python backend
│   ├── main.py                     # App entry point, CORS, lifespan
│   ├── config.py                   # Configuration settings
│   ├── models.py                   # Pydantic data models
│   ├── database.py                 # SQLite audit log (demo) / PostgreSQL (prod)
│   ├── requirements.txt            # Python dependencies
│   │
│   ├── routers/                    # API route handlers
│   │   ├── bade.py                 # /api/bade/* endpoints
│   │   ├── aapa.py                 # /api/aapa/* endpoints
│   │   ├── airo.py                 # /api/airo/* endpoints
│   │   ├── vpa.py                  # /api/vpa/* endpoints
│   │   ├── crdt.py                 # /api/crdt/* endpoints
│   │   └── system.py               # /api/system/* + SSE stream
│   │
│   ├── services/                   # Business logic layer
│   │   ├── bade_service.py         # Isolation Forest + anomaly scoring
│   │   ├── aapa_service.py         # TTP cosine similarity + Markov chain
│   │   ├── airo_service.py         # Playbook orchestration + approval gate
│   │   ├── vpa_service.py          # CVE scoring + CISA KEV integration
│   │   └── crdt_service.py         # NetworkX attack path graph
│   │
│   ├── data/                       # Embedded reference data
│   │   ├── mitre_attack.py         # ATT&CK techniques + actor profiles
│   │   ├── playbooks.py            # 50+ playbook definitions
│   │   ├── topology.py             # CNI network topology (30 nodes)
│   │   └── scenarios.py            # Pre-built demo attack scenarios
│   │
│   └── utils/                      # Utility modules
│       ├── audit_log.py            # Hash-chained immutable audit logger
│       ├── simulator.py            # Background event generator (demo)
│       └── nvd_client.py           # NVD API + CISA KEV client
│
├── frontend/                       # React + Vite + TypeScript frontend
│   ├── index.html                  # HTML entry point
│   ├── package.json                # Node dependencies
│   ├── vite.config.ts              # Vite configuration
│   ├── tailwind.config.js          # Tailwind CSS configuration
│   ├── tsconfig.json               # TypeScript configuration
│   │
│   └── src/
│       ├── main.tsx                # React entry point
│       ├── App.tsx                 # Router + layout
│       ├── index.css               # Global styles + utilities
│       │
│       ├── api/
│       │   └── client.ts           # Typed API client (Axios)
│       │
│       ├── types/
│       │   └── index.ts            # Shared TypeScript interfaces
│       │
│       ├── components/
│       │   ├── layout/             # Sidebar, Header, Layout wrapper
│       │   ├── soc/                # Alert feed, threat globe, metrics
│       │   ├── bade/               # Entity risk table, anomaly chart, lateral movement graph
│       │   ├── aapa/               # Attribution panel, TTP heatmap, next-move predictor
│       │   ├── airo/               # Incident panel, playbook runner, approval gate, audit log
│       │   ├── vpa/                # CVE table, asset risk matrix, KEV badges
│       │   ├── crdt/               # D3.js attack graph, scenario panel
│       │   └── shared/             # Risk badge, score gauge, metric card, timeline
│       │
│       └── pages/
│           ├── Dashboard.tsx       # SOC Dashboard (main page)
│           ├── AnomalyDetection.tsx # BADE view
│           ├── APTAttribution.tsx  # AAPA view
│           ├── IncidentResponse.tsx # AIRO view
│           ├── VulnerabilityManager.tsx # VPA view
│           ├── DigitalTwin.tsx     # CRDT view (D3.js graph)
│           ├── AuditLog.tsx        # Immutable audit log viewer
│           └── Executive.tsx       # Executive/CISO dashboard
│
├── docker-compose.yml              # Infrastructure services
├── demo/                           # Demo scenario scripts
│   ├── trigger_lateral_movement.py # Simulate APT41 lateral movement
│   ├── trigger_ransomware.py       # Simulate ransomware deployment
│   └── generate_report.py          # Generate CERT-In incident report
│
└── README.md                       # This file
```

---

## 📡 API Reference

Base URL: `http://localhost:8000`

Interactive API docs: `http://localhost:8000/docs` (Swagger UI)

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/system/status` | Platform health and module statuses |
| `GET` | `/api/system/metrics` | Live KPIs: MTTD, MTTR, TPR, FPR |
| `GET` | `/api/events/stream` | Server-Sent Events stream (real-time) |

### BADE — Anomaly Detection

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/bade/alerts` | Get active anomaly alerts |
| `GET` | `/api/bade/entities` | Entity list with deviation scores |
| `GET` | `/api/bade/timeline` | Event timeline (last 24h) |
| `POST` | `/api/bade/feedback` | Submit TP/FP analyst feedback |

### AAPA — APT Attribution

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/aapa/attribution` | Ranked attribution hypotheses |
| `GET` | `/api/aapa/actors` | Known threat actor profiles |
| `GET` | `/api/aapa/next-moves?actor_id=...` | Predicted next attacker moves |
| `POST` | `/api/aapa/analyze` | Analyze a custom TTP set |

### AIRO — Incident Response

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/airo/incidents` | Active incidents |
| `GET` | `/api/airo/playbooks` | Available playbook library |
| `POST` | `/api/airo/execute` | Execute a playbook action |
| `POST` | `/api/airo/approve` | Approve a HIGH blast-radius action |
| `GET` | `/api/airo/audit-log` | Immutable audit log |
| `GET` | `/api/airo/report/{id}` | CERT-In format incident report |

### VPA — Vulnerability Prioritisation

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/vpa/vulnerabilities` | Context-scored CVE list |
| `GET` | `/api/vpa/assets` | Asset inventory |
| `GET` | `/api/vpa/kev-status` | CISA KEV CVEs in your environment |
| `POST` | `/api/vpa/refresh` | Refresh NVD + CISA KEV feeds |

### CRDT — Digital Twin

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/crdt/topology` | Network topology graph |
| `GET` | `/api/crdt/attack-paths` | Attack paths (source → target) |
| `GET` | `/api/crdt/chokepoints` | Critical chokepoint nodes |
| `POST` | `/api/crdt/simulate` | Run a pre-built attack scenario |

---

## 🎬 Demo Scenarios

### Scenario 1: APT41 Lateral Movement (Primary Demo)

**Story**: APT41 operator gains initial access via spear-phishing an AIIMS HR employee. CyberShield AI detects anomalous behaviour within 60 seconds and autonomously contains the threat.

```
Timeline:
T+0:00  APT41 delivers spear-phish to HR employee → initial access
T+0:05  Malware executes → BADE detects PowerShell anomaly (score: 78/100)
T+0:12  Lateral movement: HR workstation → File Server
T+0:18  BADE scores File Server at 91/100 → HIGH ALERT
T+0:25  AAPA attributes to APT41 with 91% confidence
T+0:28  AIRO executes: isolate endpoint + block C2 IP (< 30 seconds ✅)
T+0:35  CRDT shows attack path blocked at chokepoint
T+10:00 CERT-In incident report auto-generated ✅
```

### Scenario 2: Ransomware at Power Grid OT

**Story**: Ransomware enters via corporate network and attempts to pivot into SCADA systems.

### Scenario 3: Data Exfiltration at Educational Institution

**Story**: Insider threat at CBSE exfiltrates student exam data before board exams.

---

## 🔒 Security & Compliance

### Security Controls

| Layer | Control | Implementation |
|-------|---------|---------------|
| Data at Rest | AES-256 encryption | All databases encrypted |
| Data in Transit | TLS 1.3 | All inter-service communication |
| Secrets | HashiCorp Vault | No credentials in config files or repos |
| Access | RBAC + MFA | Enforced for all platform users |
| Audit | Hash-chained log | Tamper-evident, court-admissible |
| Network | mTLS | Mutual authentication between microservices |
| OT | Data Diode | Unidirectional — no active probing into OT |

### Indian Regulatory Compliance

| Regulation | Requirement | CyberShield AI Implementation |
|-----------|------------|-------------------------------|
| **IT Act 2000** | Cybersecurity obligations | Full audit trail, incident documentation |
| **DPDP Act 2023** | Data protection | Data processed in Indian data centres, DPO notification in playbook |
| **CERT-In Directions 2022** | 6-hour mandatory reporting | Auto-generated CERT-In format reports within 10 minutes |
| **CERT-In Directions 2022** | Log retention (180 days) | Immutable audit vault with configurable retention |
| **CERT-In Directions 2022** | ICT incident designation | Automated classification + escalation |

---

## 📈 Scalability

### Horizontal Scaling Architecture

```
┌─────────────────────────────────────────────────────┐
│              Kubernetes Cluster                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │  BADE    │  │  BADE    │  │  BADE    │  (n pods)│
│  │  Pod 1   │  │  Pod 2   │  │  Pod 3   │          │
│  └──────────┘  └──────────┘  └──────────┘          │
│       ↑              ↑              ↑                │
│  ─────────────── Kafka Bus ─────────────────        │
│       ↓              ↓              ↓                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ClickHouse│  │ClickHouse│  │ClickHouse│ (sharded)│
│  │ Shard 1  │  │ Shard 2  │  │ Shard 3  │          │
│  └──────────┘  └──────────┘  └──────────┘          │
└─────────────────────────────────────────────────────┘
```

### Scale Targets

| Dimension | Minimum | Target | Maximum |
|-----------|---------|--------|---------|
| Monitored Endpoints | 10,000 | 100,000 | 500,000 |
| Events/Second | 10,000 | 100,000 | 1,000,000 |
| Kafka Partitions | 12 | 48 | 192 |
| ClickHouse Shards | 3 | 9 | 27 |
| BADE Pods | 3 | 12 | 48 |
| Multi-tenancy | — | MSSP-ready | ✅ |

---

## 👥 Team

**CyberShield AI** — Built for ET AI Hackathon 2026, Problem Statement 7

> *Protecting India's Critical National Infrastructure through the power of AI*

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **MITRE Corporation** for the ATT&CK framework and CALDERA red team tool
- **CERT-In** for India-specific cybersecurity advisories and guidance
- **Canadian Institute for Cybersecurity** for the CICIDS datasets
- **iTrust Singapore** for the SWaT dataset
- **CISA** for the Known Exploited Vulnerabilities catalogue
- **NIST** for the NVD CVE database and NIST SP 800-61

---

<div align="center">

**🛡️ CyberShield AI — Because India's Infrastructure Cannot Wait**

*Compressing breach detection from weeks to minutes. Containment in 30 seconds.*

[![ET AI Hackathon 2026](https://img.shields.io/badge/ET_AI_Hackathon_2026-Problem_Statement_7-ff3366?style=for-the-badge)](https://github.com/Vishwajeet2005/cyber-resilience-)

</div>
