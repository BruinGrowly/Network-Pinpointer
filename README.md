# Network-Pinpointer

**Semantic Network Diagnostic Tool using LJPW Framework**

Network-Pinpointer maps network operations to a four-dimensional semantic space (Love, Justice, Power, Wisdom), enabling unprecedented insights into network infrastructure through semantic analysis.

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

### LJPW Framework

Every network operation maps to four dimensions:

| Dimension | Network Meaning | Examples |
|-----------|----------------|----------|
| **Love (L)** | Connectivity, communication, service sharing | Web servers, VPNs, load balancers |
| **Justice (J)** | Security, policies, rules, compliance | Firewalls, auth servers, ACLs |
| **Power (P)** | Performance, control, execution | App servers, databases, compute nodes |
| **Wisdom (W)** | Monitoring, diagnostics, information | SNMP, log servers, monitoring tools |

**Example coordinates:**
- `ping 8.8.8.8` → `(L=0.29, J=0.14, P=0.00, W=0.57)` → **Wisdom-dominant** (monitoring)
- `configure firewall deny all` → `(L=0.05, J=0.60, P=0.30, W=0.05)` → **Justice-dominant** (security)

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

### Available Visualizations

#### 1. **Cluster Map** - 3D Semantic Topology
Interactive 3D visualization of network devices in LJPW space.

**Features:**
- Filter by all LJPW dimensions with sliders
- Search targets in real-time
- Multiple export formats
- Statistics panel with live updates

**Generate:** `./pinpoint visualize clusters`

---

#### 2. **Dashboard** - Unified Overview
Comprehensive table view with AI-powered insights.

**Features:**
- Import/export custom data
- Sortable columns (click headers)
- AI insights generation
- Filter by posture and dimension
- Config persistence across sessions

**Generate:** `./pinpoint visualize dashboard`

---

#### 3. **Drift Timeline** - Temporal Analysis
Track semantic changes over time with annotations.

**Features:**
- Date range selection
- Custom annotations with persistence
- Trend lines and drift velocity
- Statistical analysis (drift rate, severity)
- Multiple view modes (LJPW/Mass/Harmony)

**Generate:** `./pinpoint baseline <target>` then track drift

---

#### 4. **Mass Distribution** - Statistical Analysis
Analyze semantic mass distribution with outlier detection.

**Features:**
- Multiple chart types (histogram, pie, scatter, box plot)
- Comprehensive statistics (mean, median, std dev, correlation)
- IQR-based outlier detection
- Recommendations engine
- Distribution skew analysis

**Generate:** `./pinpoint visualize mass`

---

#### 5. **Topology Graph** - Network Relationships
3D network graph with pathfinding and metrics.

**Features:**
- **Dijkstra pathfinding**: Click nodes to find shortest paths
- **Multiple layouts**: LJPW Space, Force-Directed, Circular, Hierarchical
- **Network metrics**: Density, average degree, clustering coefficient
- **Interactive filtering**: By dimension, connection strength, mass
- **Path highlighting**: Visual shortest path display

**Generate:** `./pinpoint visualize topology`

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

💛 Love Cluster (5 devices) - Cohesion: 87%
   Connectivity-focused: Web servers, communication hubs
   • 192.168.1.10 - Web Service | Ports: 3 | Latency: 2.1ms

⚖️  Justice Cluster (3 devices) - Cohesion: 92%
   Security-focused: Firewalls, authentication
   • 192.168.1.1 - Security Gateway | Ports: 2 | Latency: 0.9ms

⚡ Power Cluster (2 devices) - Cohesion: 78%
   Performance-focused: Application servers, databases
   • 192.168.1.50 - Database Server | Ports: 1 | Latency: 1.5ms

🧠 Wisdom Cluster (2 devices) - Cohesion: 95%
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
| **Performance Analysis** | Locate Power-dominant bottlenecks, optimize resource allocation |
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
Using Love-Justice-Power-Wisdom (LJPW) Framework
2025
```

---

**Built with the LJPW Semantic Framework**
*Love • Justice • Power • Wisdom*
