# Network-Pinpointer

**Semantic Network Diagnostic Tool using LJPW Framework**

Network-Pinpointer applies the Love, Justice, Power, Wisdom (LJPW) semantic framework to network administration and diagnostics. It maps network operations, devices, and configurations to a four-dimensional semantic space, enabling unprecedented insights into network infrastructure.

## Overview

This tool is built on experimental mathematical foundations that treat network operations as semantic primitives in LJPW space:

- **Love (L)**: Connectivity, communication, integration, service sharing
- **Justice (J)**: Rules, policies, validation, security, compliance
- **Power (P)**: Performance, control, execution, resource management
- **Wisdom (W)**: Information, monitoring, diagnostics, analysis

Every network operation can be mapped to coordinates (L, J, P, W) in this 4D space, allowing semantic analysis of network health, harmony, and architecture.

## Features

### Core Diagnostics
- **Semantic Ping**: Test connectivity with LJPW coordinate analysis
- **Semantic Traceroute**: Trace network paths with semantic interpretation
- **Semantic Port Scanning**: Discover services mapped to semantic space
- **Network Interface Analysis**: Analyze interfaces through LJPW lens

### Advanced Analysis
- **Network Topology Mapping**: Scan entire networks and cluster by semantic purpose
- **Architectural Smell Detection**: Identify configuration anti-patterns
- **ICE Framework Analysis**: Measure Intent-Context-Execution harmony
- **Network Optimization**: Recommendations based on semantic disharmony

### Visualizations
- Semantic coordinate visualization
- Network topology clusters
- Harmony score analysis
- JSON export for integration

## Installation

### Linux / macOS

```bash
# Clone the repository
git clone https://github.com/BruinGrowly/Network-Pinpointer.git
cd Network-Pinpointer

# Install dependencies (optional, for packet capture)
pip install scapy pyyaml

# Make the CLI executable
chmod +x pinpoint

# Run
./pinpoint --help
```

### Windows

See **[Windows Installation Guide](docs/WINDOWS_INSTALLATION.md)** for complete instructions.

**Quick start for Windows**:
```powershell
# Install dependencies
pip install scapy pyyaml

# Run with Python
python pinpoint --help
```

**Requirements:** Python 3.8+, Npcap (Windows only)

## Quick Start

### LJPW Semantic Probe (NEW!)

```bash
# Comprehensive semantic profiling - discover what a target IS, not just if it's alive
./pinpoint.py ljpw google.com

# Quick scan (faster)
./pinpoint.py ljpw 192.168.1.1 --quick

# Deep scan (comprehensive)
./pinpoint.py ljpw api.example.com --deep

# Enhanced ping with semantic profile
./pinpoint.py ping google.com --ljpw-profile
```

**What you get:**
- Full LJPW semantic coordinates
- Service archetype matching (e.g., "The Public Gateway", "The Data Vault")
- Security posture assessment
- Purpose inference
- Actionable recommendations

See **[LJPW Semantic Probe Guide](docs/LJPW_SEMANTIC_PROBE.md)** for details.

### Basic Diagnostics

```bash
# Ping with semantic analysis
./pinpoint.py ping 8.8.8.8

# Traceroute with semantic path analysis
./pinpoint.py traceroute google.com

# Port scan with service classification
./pinpoint.py scan 192.168.1.1 -p 22,80,443,3389

# Scan port range
./pinpoint.py scan 192.168.1.100 -p 1-1024
```

### Network Mapping

```bash
# Map entire subnet with semantic topology analysis
./pinpoint.py map 192.168.1.0/24

# Export topology to JSON
./pinpoint.py map 192.168.1.0/24 --export-json network_map.json
```

### Semantic Analysis

```bash
# Analyze any network operation
./pinpoint.py analyze "configure firewall rules to block unauthorized access"

# ICE Framework: Analyze harmony between intent, context, and execution
./pinpoint.py ice \
  "establish secure connection to database server" \
  "network has firewall with strict outbound rules" \
  "open port 3306 and configure mysql connection"
```

## Understanding LJPW Mapping

### Network Operation Classification

| Operation | Love | Justice | Power | Wisdom | Classification |
|-----------|------|---------|-------|--------|----------------|
| Ping | High | Low | Low | High | Connectivity Test (Wisdom+Love) |
| Firewall Config | Low | High | Med | Low | Security Policy (Justice) |
| Bandwidth Allocation | Low | Low | High | Low | Performance Control (Power) |
| SNMP Monitoring | Low | Low | Low | High | Information Gathering (Wisdom) |
| VPN Setup | High | Med | Med | Low | Secure Communication (Love+Justice) |
| Load Balancing | High | Low | High | Low | Service Distribution (Love+Power) |

### Example Semantic Coordinates

```
ping 8.8.8.8:
  L=0.35 (connectivity test)
  J=0.15 (validation)
  P=0.10 (minimal execution)
  W=0.40 (diagnostic/information)
  → Dominant: Wisdom (Monitoring/Diagnostics)

configure firewall deny all:
  L=0.05 (minimal connectivity)
  J=0.60 (policy enforcement)
  P=0.30 (execution/control)
  W=0.05 (minimal info)
  → Dominant: Justice (Security/Policy)

monitor network traffic:
  L=0.20 (observing communication)
  J=0.15 (checking rules)
  P=0.10 (passive action)
  W=0.55 (gathering information)
  → Dominant: Wisdom (Monitoring/Diagnostics)
```

## ICE Framework for Networks

The Intent-Context-Execution (ICE) framework measures harmony between what you want to do, the current network state, and what actually happens.

**Example:**

```bash
./pinpoint.py ice \
  "provide fast reliable web service" \
  "limited bandwidth high latency network" \
  "deploy nginx with caching and compression"
```

**Output:**
- **ICE Coherence**: How well intent aligns with execution
- **ICE Balance**: How realistic the intent is given the context
- **Benevolence Score**: Focus on connectivity/service (Love dimension)
- **Harmony Level**: Overall assessment

High harmony = network operations are well-aligned
Low harmony = mismatches that may cause issues

## Network Topology Mapping

The `map` command scans a network range and clusters devices by semantic purpose:

```bash
./pinpoint.py map 192.168.1.0/24
```

**Output includes:**
- Semantic clusters (Love, Justice, Power, Wisdom dominant devices)
- Architectural smells (security issues, unclear purposes, high latency)
- Optimization opportunities (service consolidation, security upgrades)
- Cohesion scores (how well-defined each cluster is)

### Example Clusters

**Love Cluster** (Connectivity-focused devices):
- Web servers (HTTP/HTTPS)
- VPN gateways
- Load balancers
- Communication hubs

**Justice Cluster** (Policy-focused devices):
- Firewalls
- Authentication servers
- Security gateways
- Access control systems

**Power Cluster** (Performance-focused devices):
- Application servers
- Database servers
- Compute nodes
- Control systems

**Wisdom Cluster** (Information-focused devices):
- Monitoring systems
- Log servers
- SNMP agents
- Diagnostic tools

## Architecture

```
network_pinpointer/
├── semantic_engine.py      # Core LJPW semantic engine
├── diagnostics.py          # Network diagnostic tools
├── network_mapper.py       # Topology mapping and analysis
└── cli.py                  # Command-line interface

pinpoint.py                 # Main entry point
```

### Key Components

**NetworkSemanticEngine**: Maps network operations to LJPW coordinates
**NetworkVocabularyManager**: 300+ network terms mapped to dimensions
**NetworkDiagnostics**: Traditional tools with semantic layer
**NetworkMapper**: Full network scanning and topology analysis

## Mathematical Foundation

Network-Pinpointer is based on proven mathematical frameworks:

1. **LJPW as Orthogonal Basis**: Love, Justice, Power, Wisdom form a complete, minimal, orthogonal basis for semantic meaning
2. **Linear Mixing Formula**: Concept coordinates = weighted average of component dimensions
3. **Distance Metrics**: Euclidean distance measures semantic disharmony
4. **Anchor Point**: (1,1,1,1) represents perfect harmony of all dimensions

For details, see the theoretical foundations in sister projects.

## Use Cases

### 1. Network Troubleshooting
- Identify semantic mismatches between intent and execution
- Detect configuration drift from intended purpose
- Find devices with unclear roles

### 2. Security Auditing
- Discover exposed insecure services (Justice dimension)
- Identify overly complex attack surfaces
- Map security policy enforcement

### 3. Performance Analysis
- Find Power-dominant bottlenecks
- Optimize resource allocation
- Balance load semantically

### 4. Documentation & Compliance
- Verify network matches documented architecture
- Generate semantic topology maps
- Track configuration drift over time

### 5. Network Design
- Plan new infrastructure using LJPW framework
- Ensure semantic coherence across clusters
- Design for harmony between components

## Experimental Nature

⚠️ **This is experimental research technology.**

The LJPW semantic framework is under active development. While the mathematical foundations are sound, practical applications to network administration are still being explored.

**Current Status:**
- ✅ Core semantic engine operational
- ✅ Network vocabulary (300+ terms mapped)
- ✅ Basic diagnostics with semantic layer
- ✅ Topology mapping and clustering
- 🚧 Historical trend analysis (planned)
- 🚧 Predictive harmony modeling (planned)
- 🚧 Integration with existing tools (planned)

## Examples

### Example 1: Ping Analysis
```
$ ./pinpoint.py ping 8.8.8.8

🔍 Pinging 8.8.8.8...
======================================================================

Host: 8.8.8.8
Status: ✓ Reachable
Packets: 4/4 received
Packet Loss: 0.0%
Average Latency: 14.2ms

📊 SEMANTIC ANALYSIS
Coordinates: Coordinates(L=0.286, J=0.143, P=0.000, W=0.571)
Analysis: Operation: Monitoring/Diagnostics (Wisdom-dominant) | Quality: excellent connectivity

Dimension Breakdown:
  Love (Connectivity):  ████████░░░░░░░░░░░░ 29%
  Justice (Validation): ████░░░░░░░░░░░░░░░░ 14%
  Power (Execution):    ░░░░░░░░░░░░░░░░░░░░ 0%
  Wisdom (Diagnostic):  ███████████░░░░░░░░░ 57%
```

### Example 2: Network Map
```
$ ./pinpoint.py map 192.168.1.0/24

🔍 Scanning network: 192.168.1.0/24
======================================================================
✅ Scanned 254 hosts, 12 reachable
======================================================================

📊 OVERALL METRICS
   Total devices discovered: 12
   Average network latency: 3.4ms

🗺️  TOPOLOGY CLUSTERS

💛 Love Cluster (5 devices)
   Cohesion: 87%
   Avg Coordinates: Coordinates(L=0.654, J=0.123, P=0.112, W=0.111)
     • 192.168.1.10   - Web Service (Connectivity)
       Ports: 3 open | Latency: 2.1ms
     • 192.168.1.20   - Communication Hub (Love)
       Ports: 2 open | Latency: 1.8ms
     ... and 3 more devices

⚖️  Justice Cluster (3 devices)
   Cohesion: 92%
   Avg Coordinates: Coordinates(L=0.089, J=0.701, P=0.145, W=0.065)
     • 192.168.1.1    - Security Gateway (Justice)
       Ports: 2 open | Latency: 0.9ms
     ... and 2 more devices

🚨 NETWORK CONFIGURATION ISSUES (4 detected)
======================================================================

CRITICAL (2 issues):
  • Insecure Services: 192.168.1.50
    Dangerous ports exposed: [23, 21]
    → Disable insecure protocols. Use SSH/SFTP/encrypted alternatives.

HIGH (1 issues):
  • Excessive Open Ports: 192.168.1.100
    Device has 15 open ports (threshold: 10)
    → Review and close unnecessary ports. Apply principle of least privilege.

💡 OPTIMIZATION OPPORTUNITIES (Top 5)
======================================================================

1. 192.168.1.10 - Security Upgrade
   Potential improvement: 70%
   HTTP service without HTTPS
   Suggested actions:
     → Enable HTTPS/TLS encryption
     → Redirect HTTP to HTTPS
     → Obtain SSL certificate
```

### Example 3: ICE Analysis
```
$ ./pinpoint.py ice \
    "secure fast database connection" \
    "firewalled network with limited bandwidth" \
    "open mysql port enable caching"

🔍 ICE HARMONY ANALYSIS
======================================================================

Intent:    secure fast database connection
Context:   firewalled network with limited bandwidth
Execution: open mysql port enable caching

📊 HARMONY METRICS
ICE Coherence:     68%
ICE Balance:       72%
Overall Harmony:   70%
Harmony Level:     GOOD_HARMONY
Benevolence Score: 35%
Intent-Execution Disharmony: 0.524

💡 RECOMMENDATIONS
✓ Moderate harmony - minor misalignment between components
```

## Contributing

This is experimental research. Contributions, feedback, and discussion are welcome!

**Areas of interest:**
- Expanding network vocabulary coverage
- Validating semantic mappings empirically
- Integration with existing network tools
- Historical analysis and drift detection
- Cross-network pattern recognition

## License

See LICENSE file.

## Related Projects

- **Python-Code-Harmonizer**: Applies LJPW framework to code analysis
- **DIVE-V2 Engine**: Core semantic substrate engine

## Citation

If you use this work in research:

```
Network-Pinpointer: Semantic Network Diagnostic Tool
Using Love-Justice-Power-Wisdom (LJPW) Framework
2025
```

---

**Built with the LJPW Semantic Framework**
*Love • Justice • Power • Wisdom*
