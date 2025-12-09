# Network-Pinpointer

**Semantic Network Diagnostic Tool**

Network-Pinpointer maps network operations to a four-dimensional semantic space (Connectivity, Security, Performance, Visibility), enabling unprecedented insights into network infrastructure through semantic analysis.

## Table of Contents
- [Quick Start](#quick-start)
  - [For Network Experts](#for-network-experts)
  - [For Beginners](#for-beginners)
- [Core Concepts](#core-concepts)
- [Installation](#installation)
- [Features](#features)
- [Visualizations](#visualizations)
- [Usage Examples](#usage-examples)
- [Documentation](#documentation)

---

## Quick Start

### For Network Experts

**TL;DR**: Semantic network analysis tool. Maps operations to 4D LJPW space. Think: tcpdump + nmap + topology discovery + semantic clustering.

```bash
# Installation
git clone https://github.com/BruinGrowly/Network-Pinpointer.git
cd Network-Pinpointer
pip install pyyaml scapy  # Core + packet capture

# Quick diagnostics
./pinpoint ping 8.8.8.8              # Semantic ping analysis
./pinpoint scan 192.168.1.1 -p 1-1024  # Port scan with classification
./pinpoint map 192.168.1.0/24        # Full network topology + clustering

# Advanced analysis
./pinpoint ljpw api.example.com --deep   # Comprehensive semantic profiling
./pinpoint ice "intent" "context" "execution"  # Harmony analysis
```

**What makes it different:**
- Maps every network operation to semantic coordinates (L, J, P, W)
- Clusters devices by purpose (connectivity, security, performance, monitoring)
- Detects architectural smells and semantic mismatches
- Interactive HTML visualizations with pathfinding and analytics

### For Beginners

**What is this?** A network diagnostic tool that understands *what* devices and operations do, not just *if* they work.

**Why use it?**
- Automatically categorizes network devices by purpose
- Finds security issues and optimization opportunities
- Beautiful visualizations you can interact with
- Helps you understand your network's architecture

**Basic workflow:**
```bash
# 1. Install (minimal setup)
git clone https://github.com/BruinGrowly/Network-Pinpointer.git
cd Network-Pinpointer
pip install pyyaml

# 2. Learn the framework
./pinpoint explain ljpw

# 3. Test your first device
./pinpoint ping google.com

# 4. Scan your network (replace with your subnet)
./pinpoint map 192.168.1.0/24

# 5. Open the HTML visualization (found in output/)
# Browse to see interactive network topology!
```

**Need help?** Run `./pinpoint --help` or `./pinpoint explain <topic>`

---

## Core Concepts

### The Four Dimensions

Every network operation maps to four dimensions:

| Dimension | What It Measures | Examples |
|-----------|------------------|----------|
| **Connectivity (L)** | Reachability, communication, service sharing | Web servers, VPNs, load balancers |
| **Security (J)** | Access control, policies, rules, compliance | Firewalls, auth servers, ACLs |
| **Performance (P)** | Speed, capacity, execution | App servers, databases, compute nodes |
| **Visibility (W)** | Monitoring, diagnostics, observability | SNMP, log servers, monitoring tools |

**Example coordinates:**
- `ping 8.8.8.8` → `(L=0.29, J=0.14, P=0.00, W=0.57)` → **Visibility-dominant** (monitoring operation)
- `configure firewall deny all` → `(L=0.05, J=0.60, P=0.30, W=0.05)` → **Security-dominant** (access control)

### ICE Framework

Measures **Intent-Context-Execution** harmony to detect mismatches:

```
Intent:    "provide fast database access"
Context:   "high-latency network with limited bandwidth"
Execution: "deploy mysql over unoptimized tcp"
Result:    Low harmony → performance issues likely
```

---

## Installation

### Quick Install (Choose One)

| Option | Use Case | Install Command |
|--------|----------|----------------|
| **Core CLI** | Basic diagnostics | `pip install pyyaml` |
| **+ Packet Capture** | Deep analysis | `pip install pyyaml scapy` |
| **Full Stack** | Production + API + monitoring | `pip install -r requirements.txt` |

### Platform-Specific

**Linux/macOS:**
```bash
git clone https://github.com/BruinGrowly/Network-Pinpointer.git
cd Network-Pinpointer
pip install pyyaml scapy  # Recommended
chmod +x pinpoint
./pinpoint --help
```

**Windows:**
```powershell
git clone https://github.com/BruinGrowly/Network-Pinpointer.git
cd Network-Pinpointer
pip install pyyaml scapy
# Install Npcap: https://npcap.com/#download
python pinpoint --help
```

**Full guide:** [WINDOWS_INSTALLATION.md](docs/WINDOWS_INSTALLATION.md)

### Docker (Full Stack)

```bash
cp .env.example .env
docker-compose up -d

# Access:
# - API: http://localhost:8080
# - Grafana: http://localhost:3000 (admin/admin123)
# - Prometheus: http://localhost:9090
```

**Verify installation:**
```bash
./pinpoint version
./pinpoint explain ljpw
SKIP_FIRST_RUN=1 ./pinpoint health
```

---

## Features

### Core Diagnostics
- **Semantic Ping**: Connectivity tests with LJPW coordinate analysis
- **Semantic Traceroute**: Path tracing with semantic interpretation
- **Port Scanning**: Service discovery mapped to semantic space
- **Network Mapping**: Subnet scanning with clustering by purpose
- **LJPW Semantic Probe**: Comprehensive profiling (archetype matching, purpose inference)

### Analysis Tools
- **ICE Framework**: Intent-Context-Execution harmony measurement
- **Architectural Smell Detection**: Identify anti-patterns and misconfigurations
- **Network Optimization**: Recommendations based on semantic disharmony
- **Topology Clustering**: Automatic grouping by semantic purpose

### Integration & Export
- **REST API**: FastAPI server with full semantic analysis endpoints
- **Prometheus Metrics**: Real-time monitoring integration
- **JSON Export**: All analysis results exportable for integration
- **Interactive Visualizations**: Self-contained HTML with advanced features

---

## Visualizations

**All visualizations are self-contained HTML files with:**
- ✅ Dark/Light themes
- ✅ Interactive filtering and search
- ✅ Export capabilities (JSON/CSV/PNG)
- ✅ Keyboard shortcuts
- ✅ LocalStorage persistence
- ✅ No server required - works offline

---

### 1. **Cluster Map** - 3D Semantic Topology

**CLI Command:**
```bash
# Generate 3D cluster visualization
./pinpoint map 192.168.1.0/24

# Output includes HTML file
# ✓ Network mapped and visualized: output/cluster_map.html
```

**CLI Output:**
```
🔍 Scanning network: 192.168.1.0/24
======================================================================
✅ Scanned 254 hosts, 12 reachable

🔗 Connectivity Cluster (5 devices) - Cohesion: 87%
🔒 Security Cluster (3 devices) - Cohesion: 92%
⚡ Performance Cluster (2 devices) - Cohesion: 78%
👁 Visibility Cluster (2 devices) - Cohesion: 95%

📊 Visualization saved: output/cluster_map.html
```

**HTML Visualization Mockup:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ 🎯 Semantic Cluster Map                    [🌙 Theme] [💾 Export] │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Control Panel              │        3D Visualization              │
│  ┌──────────────┐          │                                       │
│  │ 🔍 Search    │          │         ●                             │
│  │ [          ] │          │    ●        ● (google.com)            │
│  ├──────────────┤          │              ↗ Connectivity: 0.65   │
│  │ 🎚️ Filters   │          │         ●        ● Security: 0.12    │
│  │ Connect:█▓░░ │          │                  ● Performance: 0.10 │
│  │ Security█░░░ │          │    ●                Visibility: 0.13 │
│  │ Perform:▓░░░ │          │         ●                             │
│  │ Visible:██▓░ │          │              ●                        │
│  │ Mass:   █▓▓░ │          │                   ● (firewall)       │
│  ├──────────────┤          │    ●         ●                        │
│  │ 📊 Stats     │          │         Color-coded by dimension:     │
│  │ Nodes:    12 │          │         Red=Connectivity Blue=Security│
│  │ Filtered: 12 │          │         Orange=Perform Purple=Visible │
│  │ Connect:   5 │          │                                       │
│  │ Security:  3 │          │         [Interactive 3D - Drag to    │
│  │ Perform:   2 │          │          rotate, scroll to zoom]     │
│  │ Visible:   2 │          │                                       │
│  └──────────────┘          │                                       │
│                             │                                       │
│  Keyboard: F=Fullscreen R=Reset H=Hide E=Export T=Theme           │
└─────────────────────────────────────────────────────────────────────┘
```

**Interactive Features:**
- Drag to rotate the 3D space
- Click nodes to see details
- Use sliders to filter dimensions in real-time
- Search for specific targets
- Export filtered data or screenshot

---

### 2. **Dashboard** - Unified Overview

**CLI Command:**
```bash
# Generate comprehensive dashboard
./pinpoint map 192.168.1.0/24

# Or analyze specific targets
./pinpoint ljpw google.com github.com api.example.com
./pinpoint visualize dashboard

# Output: output/dashboard.html
```

**CLI Output:**
```
✓ Dashboard created with 12 targets
✓ AI insights generated: 5 recommendations
📊 Visualization saved: output/dashboard.html
```

**HTML Visualization Mockup:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ 📊 Network Semantic Dashboard          [💡 Insights] [💾 Export]   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [🔍 Search: ____] [Posture: All ▼] [Dimension: All ▼] [⚙️ Config] │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │Target ▲    │ L   │ J   │ P   │ W   │ Mass │ Posture │Dimension││
│  ├─────────────┼─────┼─────┼─────┼─────┼──────┼─────────┼─────────┤│
│  │google.com  │0.65 │0.12 │0.10 │0.13 │ 842  │Proactive│Connect  ││
│  │firewall.lo │0.05 │0.75 │0.15 │0.05 │ 1205 │Defensive│Security ││
│  │db-server   │0.08 │0.10 │0.72 │0.10 │ 956  │Proactive│Perform  ││
│  │monitor.sys │0.10 │0.08 │0.05 │0.77 │ 634  │Reactive │Visible  ││
│  │web-lb      │0.68 │0.10 │0.18 │0.04 │ 789  │Proactive│Connect  ││
│  │auth-server │0.12 │0.70 │0.12 │0.06 │ 1050 │Defensive│Security ││
│  │...         │...  │...  │...  │...  │ ...  │...      │...      ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│  💡 AI Insights:                                                   │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ • Security Gap: firewall.lo has high Security but cluster lacks││
│  │   redundancy. Consider backup security gateway.                ││
│  │ • Performance: db-server shows high Performance, suggesting    ││
│  │   opportunity for load distribution.                           ││
│  │ • Balance: Network shows 42% Connectivity focus - well-linked  ││
│  │   but monitor security coverage.                               ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│  [Import Data] [Export JSON] [Export CSV] [Generate Report]       │
└─────────────────────────────────────────────────────────────────────┘
```

**Interactive Features:**
- Click column headers to sort (ascending/descending)
- Filter by posture or dominant dimension
- Generate AI-powered insights
- Import/export data for custom analysis
- Config auto-saves to localStorage

---

### 3. **Drift Timeline** - Temporal Analysis

**CLI Commands:**
```bash
# Establish baseline for a target
./pinpoint baseline google.com
# ✓ Baseline established for google.com

# Wait some time (hours/days), then check drift
./pinpoint drift google.com

# Generate timeline visualization
./pinpoint visualize drift google.com
# Output: output/drift_timeline_google.com.html
```

**CLI Output:**
```
🔍 Analyzing drift for: google.com
======================================================================
Baseline:  2025-12-01 10:00:00 | L=0.65 J=0.12 P=0.10 W=0.13
Current:   2025-12-03 14:30:00 | L=0.62 J=0.15 P=0.12 W=0.11

📊 DRIFT ANALYSIS
Total drift distance: 0.052
Drift velocity: 0.021/day
Severity: Low (Normal)

Dimension changes:
  Connectivity: -0.03 (↓ 4.6%)
  Security:     +0.03 (↑ 25.0%)
  Performance:  +0.02 (↑ 20.0%)
  Visibility:   -0.02 (↓ 15.4%)

📊 Timeline visualization: output/drift_timeline_google.com.html
```

**HTML Visualization Mockup:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ 📈 Drift Timeline: google.com              [📝 Annotate] [💾 Export]│
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [📅 From: 2025-12-01] [To: 2025-12-03] [View: All ▼] [Analysis ✓]│
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ 1.0│                                                            ││
│  │    │   ━━━ Connectivity ┄┄┄ Security                           ││
│  │0.8 │   ─ ─ Performance  ··· Visibility                         ││
│  │    │                                                            ││
│  │0.6 │━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ (Connectivity)   ││
│  │    │            ↘                                               ││
│  │0.4 │                                                            ││
│  │    │                                                            ││
│  │0.2 │       ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄↗┄┄┄┄ (Security)              ││
│  │    │    ···················· (Visibility)                       ││
│  │0.0 │─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ (Performance)         ││
│  │    └────────────────────────────────────────────────────────────││
│  │        12/01      12/02  📍  12/03                             ││
│  │                         Annotation: "Config change"            ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│  📊 Statistics:                    🎯 Analysis:                    │
│  Total Drift:  0.052               Trend: Increasing Security     │
│  Velocity:     0.021/day           Pattern: Security enhancement  │
│  Duration:     2.2 days            Severity: Low                  │
│  Data Points:  48                  Confidence: High               │
│                                                                     │
│  📝 Annotations:                                                   │
│  • 12/02 10:30 - "Firewall rules updated"                         │
│  • 12/03 09:15 - "Load balancer added"                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Interactive Features:**
- Select date range with interactive pickers
- Add custom annotations (saved to localStorage)
- Toggle different view modes (All/LJPW/Mass/Harmony)
- Enable trend lines and moving averages
- Export timeline with annotations

---

### 4. **Mass Distribution** - Statistical Analysis

**CLI Commands:**
```bash
# Analyze mass distribution across network
./pinpoint map 192.168.1.0/24
./pinpoint visualize mass

# Or for specific targets
./pinpoint ljpw google.com github.com api.example.com
./pinpoint visualize mass

# Output: output/mass_distribution.html
```

**CLI Output:**
```
📊 Mass Distribution Analysis
======================================================================
Targets analyzed: 12

Statistics:
  Mean:        856.3
  Median:      842.0
  Std Dev:     198.4
  Min:         634.0 (monitor.sys)
  Max:         1205.0 (firewall.lo)

Outliers detected: 2
  • firewall.lo (1205.0) - High outlier
  • monitor.sys (634.0) - Low outlier

Correlation (mass vs harmony): 0.34 (weak positive)

📊 Visualization saved: output/mass_distribution.html
```

**HTML Visualization Mockup:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ 📊 Mass Distribution Analysis         [📈 Chart Type ▼] [💾 Export]│
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [Mass: 0─────────█████─────1200] [Category: All ▼] [Harmony: ●]  │
│                                                                     │
│  Chart: [Histogram ▼] (Pie | Scatter | Box Plot)                  │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │     ┌───┐                                                       ││
│  │  6  │   │                                                       ││
│  │  5  │   │    ┌───┐                                             ││
│  │  4  │   │    │   │                                             ││
│  │  3  │   │    │   │    ┌───┐                                    ││
│  │  2  │   │    │   │    │   │    ┌───┐         ┌───┐            ││
│  │  1  │   │    │   │    │   │    │   │         │   │            ││
│  │  0  └───┴────┴───┴────┴───┴────┴───┴─────────┴───┴────────────││
│  │    600-700  700-800  800-900  900-1000  ...  1100-1200        ││
│  │    Low      Medium          High                Outliers       ││
│  └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│  📊 Statistics:                    🔍 Outliers (2):                │
│  Mean:      856.3                  • firewall.lo    1205  ⚠️ High │
│  Median:    842.0                  • monitor.sys    634   ⚠️ Low  │
│  Std Dev:   198.4                                                  │
│  Correlation: 0.34                 💡 Recommendations:             │
│                                    • High-mass targets may benefit │
│  Distribution: Normal                from load distribution        │
│  Skew: 0.12 (slight right)         • Consider consolidating low-  │
│  CV: 23.2%                           mass monitoring services      │
│                                                                     │
│  [1] Histogram [2] Pie Chart [3] Scatter [4] Box Plot             │
└─────────────────────────────────────────────────────────────────────┘
```

**Interactive Features:**
- Switch between 4 chart types (histogram, pie, scatter, box)
- Filter by mass range, category, or harmony level
- Automatic outlier detection with IQR method
- Get AI-powered recommendations
- Export statistics and visualizations

---

### 5. **Topology Graph** - Network Relationships

**CLI Commands:**
```bash
# Generate network topology graph
./pinpoint map 192.168.1.0/24
./pinpoint visualize topology

# Graph includes all discovered devices and their relationships
# Output: output/topology_graph.html
```

**CLI Output:**
```
🗺️  Generating network topology graph...
======================================================================
Nodes: 12 devices
Edges: 18 connections (similarity > 0.8)

Network Metrics:
  Density:         0.273
  Avg Degree:      3.00
  Clustering:      0.418

📊 Topology visualization: output/topology_graph.html
```

**HTML Visualization Mockup:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ 🌐 Network Topology                    [🔀 Layout ▼] [💾 Export]   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Control Panel         │         3D Network Graph                  │
│  ┌─────────────────┐  │                                            │
│  │ 🔍 Search       │  │         ● web-lb                           │
│  │ [           ]   │  │        ╱│╲                                 │
│  ├─────────────────┤  │       ╱ │ ╲                                │
│  │ 🎯 Filters      │  │      ●  │  ●  app-1                        │
│  │ Dimension: All▼ │  │     ╱   │   ╲                              │
│  │ Threshold: 0.80 │  │    ●────●────● db-server                   │
│  │ Min Mass: 0     │  │   ╱     │  firewall                        │
│  ├─────────────────┤  │  ●      │                                  │
│  │ 📐 Layout       │  │  │      ●  monitor                         │
│  │ [LJPW Space▼]   │  │  │     ╱│╲                                 │
│  │ • Force         │  │  │    ╱ │ ╲                                │
│  │ • Circular      │  │  │   ●  │  ●                               │
│  │ • Hierarchical  │  │  │      │                                  │
│  ├─────────────────┤  │  ●──────●  auth                            │
│  │ 🗺️  Path        │  │                                            │
│  │ Source: web-lb  │  │  [Interactive 3D - drag to rotate]        │
│  │ Target: db      │  │  Green edges = shortest path              │
│  │ [Find Path]     │  │  Node size = semantic mass                │
│  │ Path: 3 hops    │  │  Color = dominant dimension               │
│  │ 1. web-lb       │  │                                            │
│  │ 2. firewall     │  │  Legend: 🔴 Connect 🔵 Security           │
│  │ 3. db-server    │  │         🟠 Perform 🟣 Visible            │
│  ├─────────────────┤  │                                            │
│  │ 📊 Metrics      │  │                                            │
│  │ Nodes:      12  │  │                                            │
│  │ Edges:      18  │  │                                            │
│  │ Density:  0.273 │  │                                            │
│  │ Avg Deg:  3.00  │  │                                            │
│  │ Cluster:  0.418 │  │                                            │
│  └─────────────────┘  │                                            │
│                        │                                            │
│  Keyboard: F=Full R=Reset H=Hide E=Export T=Theme P=Path          │
└─────────────────────────────────────────────────────────────────────┘
```

**Interactive Features:**
- **Pathfinding**: Click two nodes to find shortest path (Dijkstra algorithm)
- **Multiple Layouts**: Switch between LJPW Space, Force-Directed, Circular, Hierarchical
- **Network Metrics**: Real-time calculation of density, degree, clustering
- **Filter by Dimension**: Show only Connectivity, Security, Performance, or Visibility nodes
- **Connection Threshold**: Adjust similarity threshold for edges
- **Path Highlighting**: Shortest paths shown with bright green edges

**Layout Examples:**

```
LJPW Space (3D):          Force-Directed:         Circular:
Nodes positioned by       Physics-based           Evenly distributed
semantic coordinates      organic layout          around circle

     W                         ●──●                    ●
     │                        ╱│  │╲                 ╱   ╲
   ● │ ●                     ●─┼──┼─●              ●       ●
L────●────J                   │╲│╱│              ●           ●
     │                        ● ● ●               │           │
     P                         ╲│╱                 ●         ●
                                ●                   ╲       ╱
                                                      ●───●
```

---

### CLI Examples for All Visualizations

**Complete Workflow Example:**
```bash
# 1. Scan your network
./pinpoint map 192.168.1.0/24

# Outputs:
# ✓ output/cluster_map.html      - 3D semantic clusters
# ✓ output/dashboard.html         - Comprehensive overview
# ✓ output/topology_graph.html    - Network relationships
# ✓ output/mass_distribution.html - Statistical analysis

# 2. Establish baselines for key targets
./pinpoint baseline 192.168.1.1    # Gateway
./pinpoint baseline 192.168.1.10   # Web server
./pinpoint baseline 192.168.1.50   # Database

# 3. Later, check for drift and visualize
./pinpoint drift 192.168.1.1
./pinpoint visualize drift 192.168.1.1
# ✓ output/drift_timeline_192.168.1.1.html

# 4. Analyze specific targets
./pinpoint ljpw google.com --deep
./pinpoint ljpw github.com --deep

# 5. Generate comprehensive report
./pinpoint map 192.168.1.0/24 --export-json network_report.json
```

**Quick Analysis Commands:**
```bash
# Single target analysis with all visualizations
./pinpoint ljpw api.example.com --deep --visualize

# Compare multiple targets
./pinpoint ljpw google.com github.com cloudflare.com
./pinpoint visualize dashboard

# Network health check
./pinpoint map 192.168.1.0/24 --health-check

# Export everything
./pinpoint map 192.168.1.0/24 --export-all
```

---

**Full visualization guide:** [VISUALIZATION_ENHANCEMENTS.md](VISUALIZATION_ENHANCEMENTS.md)

---

## Usage Examples

### Basic Network Operations

```bash
# Semantic ping with analysis
./pinpoint ping 8.8.8.8

# Traceroute with semantic path analysis
./pinpoint traceroute google.com

# Port scan with service classification
./pinpoint scan 192.168.1.1 -p 22,80,443,3389

# Comprehensive semantic profiling
./pinpoint ljpw api.example.com --deep
```

### Network Mapping & Analysis

```bash
# Map entire subnet with semantic clustering
./pinpoint map 192.168.1.0/24

# Export topology to JSON
./pinpoint map 192.168.1.0/24 --export-json network_map.json

# Analyze specific operation
./pinpoint analyze "configure firewall rules to block unauthorized access"
```

### ICE Harmony Analysis

```bash
# Measure intent-context-execution alignment
./pinpoint ice \
  "establish secure database connection" \
  "network has strict firewall with limited bandwidth" \
  "open port 3306 and configure mysql over tcp"

# High harmony = well-aligned operations
# Low harmony = potential mismatches/issues
```

### Baseline & Drift Tracking

```bash
# Establish baseline
./pinpoint baseline google.com

# Check drift over time
./pinpoint drift google.com

# Visualize drift timeline
./pinpoint visualize drift google.com
```

---

## Example Output

### Network Map with Semantic Clustering

```
$ ./pinpoint map 192.168.1.0/24

🔍 Scanning network: 192.168.1.0/24
======================================================================
✅ Scanned 254 hosts, 12 reachable

🗺️  TOPOLOGY CLUSTERS

🔗 Connectivity Cluster (5 devices) - Cohesion: 87%
   Communication-focused: Web servers, communication hubs
   • 192.168.1.10 - Web Service | Ports: 3 | Latency: 2.1ms

🔒 Security Cluster (3 devices) - Cohesion: 92%
   Access control-focused: Firewalls, authentication
   • 192.168.1.1 - Security Gateway | Ports: 2 | Latency: 0.9ms

⚡ Performance Cluster (2 devices) - Cohesion: 78%
   Speed/capacity-focused: Application servers, databases
   • 192.168.1.50 - Database Server | Ports: 1 | Latency: 1.5ms

👁 Visibility Cluster (2 devices) - Cohesion: 95%
   Monitoring-focused: SNMP agents, log servers
   • 192.168.1.100 - Monitoring System | Ports: 2 | Latency: 3.2ms

🚨 ISSUES DETECTED (3):
CRITICAL:
  • Insecure Services: 192.168.1.50
    Dangerous ports exposed: [23, 21]
    → Use SSH/SFTP instead of Telnet/FTP

💡 OPTIMIZATION OPPORTUNITIES:
1. 192.168.1.10 - Security Upgrade (70% improvement potential)
   HTTP without HTTPS - Enable TLS encryption
```

---

## Architecture

```
┌─────────────────────────────────────────┐
│       Network-Pinpointer Stack           │
└─────────────────────────────────────────┘

CLI / API / Web UI
        ↓
┌───────────────────┐
│ Semantic Engine   │  355+ keywords mapped
│ LJPW Framework    │  4D coordinate system
│ ICE Analysis      │  Harmony measurement
└────────┬──────────┘
         ↓
┌───────────────────┐
│ Diagnostics Layer │  Ping, trace, scan
│ Network Mapping   │  Topology discovery
│ Packet Analysis   │  Deep inspection
└────────┬──────────┘
         ↓
InfluxDB / PostgreSQL / Redis
```

**Components:**
- `semantic_engine.py` - Core LJPW mapping (300+ network terms)
- `diagnostics.py` - Network tools with semantic layer
- `network_mapper.py` - Topology scanning and clustering
- `visualization/` - Interactive HTML visualizations
- `api_server.py` - FastAPI REST endpoints

**Detailed architecture:** [ARCHITECTURE_DIAGRAMS.md](docs/ARCHITECTURE_DIAGRAMS.md)

---

## Documentation

### Getting Started
- **[USAGE_GUIDE.md](docs/USAGE_GUIDE.md)** - Complete usage guide with examples
- **[WINDOWS_INSTALLATION.md](docs/WINDOWS_INSTALLATION.md)** - Windows-specific setup

### Visualizations
- **[VISUALIZATION_ENHANCEMENTS.md](VISUALIZATION_ENHANCEMENTS.md)** - Interactive visualization features

### Production
- **[PRODUCTION_DEPLOYMENT.md](docs/PRODUCTION_DEPLOYMENT.md)** - Full production setup
- **[BACKUP_RESTORE.md](docs/BACKUP_RESTORE.md)** - Backup & disaster recovery
- **[.env.example](.env.example)** - Configuration template (250+ options)

### Technical
- **[ARCHITECTURE_DIAGRAMS.md](docs/ARCHITECTURE_DIAGRAMS.md)** - System architecture & data flows
- **[LJPW-MATHEMATICAL-BASELINES.md](docs/LJPW-MATHEMATICAL-BASELINES.md)** - Mathematical foundations
- **[LJPW_SEMANTIC_PROBE.md](docs/LJPW_SEMANTIC_PROBE.md)** - Semantic probe guide

### Reference
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[SECURITY.md](SECURITY.md)** - Security policy
- **[ISSUES_REPORT.md](ISSUES_REPORT.md)** - Repository analysis
- **[FIXES_APPLIED.md](FIXES_APPLIED.md)** - Fix documentation

---

## Use Cases

| Scenario | How Network-Pinpointer Helps |
|----------|----------------------------|
| **Troubleshooting** | Identify semantic mismatches between intent and execution |
| **Security Audits** | Find insecure services and overly complex attack surfaces |
| **Performance Analysis** | Locate performance bottlenecks, optimize resource allocation |
| **Documentation** | Generate semantic topology maps, verify architecture matches docs |
| **Network Design** | Plan infrastructure using LJPW framework for coherent design |
| **Compliance** | Track configuration drift, ensure policy enforcement |

---

## Contributing

This is experimental research. Contributions welcome!

**Areas of interest:**
- Expanding network vocabulary (300+ terms currently)
- Empirical validation of semantic mappings
- Integration with existing tools (Wireshark, Nagios, etc.)
- Historical analysis and drift detection improvements
- Cross-network pattern recognition

**Development:**
```bash
# Run tests
python3 tests/test_semantic_engine.py

# Offline mode testing
OFFLINE_MODE=1 python3 tests/test_real_packet_analysis.py
```

See [ARCHITECTURE_DIAGRAMS.md](docs/ARCHITECTURE_DIAGRAMS.md) for system design.

---

## Experimental Status

⚠️ **This is experimental research technology.**

The LJPW semantic framework is under active development. Mathematical foundations are sound, but practical applications are still being explored.

**Status:**
- ✅ Core semantic engine operational
- ✅ Network vocabulary (355+ terms mapped)
- ✅ Interactive visualizations (5 types)
- ✅ Topology mapping and clustering
- ✅ ICE harmony analysis
- 🚧 Historical trend analysis (in progress)
- 🚧 Predictive harmony modeling (planned)
- 🚧 ML-based pattern recognition (planned)

---

## License

See [LICENSE](LICENSE) file.

## Related Projects

- **Python-Code-Harmonizer** - LJPW framework for code analysis
- **DIVE-V2 Engine** - Core semantic substrate engine

## Citation

```
Network-Pinpointer: Semantic Network Diagnostic Tool
Using LJPW (Connectivity-Security-Performance-Visibility) Framework
2025
```

---

**Built with the LJPW Semantic Framework**
*Connectivity • Security • Performance • Visibility*
