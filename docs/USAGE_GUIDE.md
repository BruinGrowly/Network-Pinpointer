# Network Pinpointer Usage Guide

Complete guide to using Network Pinpointer for network diagnostics using the LJPW semantic framework.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Understanding LJPW](#understanding-ljpw)
3. [Basic Commands](#basic-commands)
4. [Diagnostic Recipes](#diagnostic-recipes)
5. [Advanced Features](#advanced-features)
6. [Real-World Examples](#real-world-examples)
7. [Interpreting Results](#interpreting-results)
8. [Best Practices](#best-practices)

---

## Quick Start

### Installation
```bash
git clone https://github.com/BruinGrowly/Network-Pinpointer.git
cd Network-Pinpointer
pip install -r requirements.txt  # If scapy needed: pip install scapy
```

### Your First Diagnostic
```bash
# Quick 30-second health check
./pinpoint quick-check google.com

# Interactive mode (recommended for beginners)
./pinpoint interactive

# Explain what Love means
./pinpoint explain love
```

---

## Understanding LJPW

Network Pinpointer analyzes networks through **four semantic dimensions**:

### 📡 Love (Connectivity & Responsiveness)
**What it measures**: How well the network connects and responds
- **High Love (0.7+)**: Fast responses, good connectivity, low latency
- **Low Love (<0.3)**: Slow responses, poor connectivity, timeouts
- **Affects**: User experience, application performance

**Example interpretation**:
```
Love: 0.85  ████████████████░░░░  EXCELLENT
→ Network is highly responsive, users happy
```

### ⚖️ Justice (Policy & Boundaries)
**What it measures**: Rules, restrictions, and policy enforcement
- **High Justice (0.7+)**: Heavy firewall rules, strict policies, route changes
- **Low Justice (<0.3)**: Open network, minimal restrictions
- **Affects**: Security posture, access control

**Example interpretation**:
```
Justice: 0.25  █████░░░░░░░░░░░░░░░  LOW
→ Network is open, may need more security
```

### ⚡ Power (Performance & Capacity)
**What it measures**: Network strength and throughput capability
- **High Power (0.7+)**: High bandwidth, low loss, strong signal
- **Low Power (<0.3)**: Packet loss, congestion, weak links
- **Affects**: Throughput, reliability

**Example interpretation**:
```
Power: 0.45  █████████░░░░░░░░░░░  FAIR
→ Some packet loss or congestion detected
```

### 🧠 Wisdom (Intelligence & Observability)
**What it measures**: Protocol intelligence and network visibility
- **High Wisdom (0.7+)**: Rich protocol info, good DNS, clear routing
- **Low Wisdom (<0.3)**: DNS issues, protocol problems, poor visibility
- **Affects**: Troubleshooting ability, monitoring

**Example interpretation**:
```
Wisdom: 0.30  ██████░░░░░░░░░░░░░░  POOR
→ DNS issues or monitoring gaps detected
```

---

## Basic Commands

### Health Check
Get overall network health snapshot:
```bash
./pinpoint health
```
**Output**:
```
Health Score: 78% (GOOD)
Love      0.85  ████████████████░░░░  EXCELLENT
Justice   0.35  ███████░░░░░░░░░░░░░  LOW
Power     0.75  ███████████████░░░░░  GOOD
Wisdom    0.80  ████████████████░░░░  EXCELLENT
```

### Quick Check
Fast 30-second assessment of a target:
```bash
./pinpoint quick-check api.prod.example.com
```

### Enhanced Ping
Semantic analysis of connectivity:
```bash
./pinpoint ping 8.8.8.8 --count 10
```

### Pattern Library
View known network issue patterns:
```bash
./pinpoint patterns
```
Shows 15+ documented patterns like:
- The Over-Secured Network
- The DNS Black Hole
- The Flaky Link
- Route Flapping
- And more...

### Explain Mode
Learn about LJPW dimensions:
```bash
./pinpoint explain love     # Learn about Love
./pinpoint explain justice  # Learn about Justice
./pinpoint explain power    # Learn about Power
./pinpoint explain wisdom   # Learn about Wisdom
./pinpoint explain ljpw     # Overview of framework
```

---

## Diagnostic Recipes

Pre-built workflows for common problems. View all recipes:
```bash
./pinpoint recipes
```

### Recipe: Slow Connection
**When to use**: "This connection is slower than expected"
```bash
./pinpoint run slow_connection api.example.com
```
**What it analyzes**:
- Power dimension (capacity/throughput)
- Love dimension (latency)
- Wisdom dimension (routing efficiency)

**Typical findings**:
- Low Power → Congestion or packet loss
- Low Love → High latency
- Low Wisdom → Suboptimal routing

### Recipe: Can't Connect
**When to use**: "I can't reach this service"
```bash
./pinpoint run cant_connect db.example.com
```
**What it analyzes**:
- Love dimension (basic connectivity)
- Justice dimension (firewall blocking?)
- Wisdom dimension (DNS resolution)

**Typical findings**:
- Low Love + High Justice → Firewall blocking
- Low Wisdom → DNS can't resolve
- All Low → Network unreachable

### Recipe: Intermittent Issues
**When to use**: "Sometimes it works, sometimes it doesn't"
```bash
./pinpoint run intermittent api.example.com
```
**What it analyzes**:
- All dimensions over time
- Variance and stability
- Pattern recognition

**Typical findings**:
- Varying Wisdom → "The Flaky Link" pattern
- Periodic drops → QoS policy or congestion
- Route instability → "Route Flapping" pattern

### Recipe: Security Audit
**When to use**: "Is my network properly secured?"
```bash
./pinpoint run security_audit myserver.com
```
**What it analyzes**:
- Justice dimension (policy enforcement)
- Love dimension (is security blocking legitimate traffic?)

**Typical findings**:
- High Justice + High Love → Well secured, not blocking
- High Justice + Low Love → Over-secured
- Low Justice → May need more security

### Recipe: Baseline
**When to use**: "What's normal for this network?"
```bash
./pinpoint run baseline production-cluster
```
**What it does**:
- Establishes healthy state
- Records all LJPW coordinates
- Creates reference for future comparisons

### Recipe: Quick Check
**When to use**: "Just tell me if it's healthy"
```bash
./pinpoint run quick_check 8.8.8.8
```
**What it does**:
- 30-second fast assessment
- Overall health score
- Critical issues only

---

## Advanced Features

### Configuration Management

Create configuration file:
```bash
./pinpoint config create-example
```

This creates `~/.network-pinpointer/config.yaml`:
```yaml
network_type: enterprise
monitoring_interval: 300
targets:
  production_api:
    host: api.prod.example.com
    baseline:
      love: 0.9
      justice: 0.3
      power: 0.85
      wisdom: 0.9
    alert_threshold: 0.15
```

View current config:
```bash
./pinpoint config show
```

### State Comparison (Diff Mode)

Compare network states before and after a change:

```bash
# Capture baseline
./pinpoint health > baseline.json

# Make network change (deploy firewall rule, etc.)

# Capture new state
./pinpoint health > after.json

# Compare
./pinpoint diff baseline.json after.json
```

**Output**:
```
Network State Comparison: baseline → after
Overall Assessment: SIGNIFICANT change

Dimension Changes:
  Love       0.85 → 0.50  (-41.2%)  ↓  [SIGNIFICANT]
  Justice    0.30 → 0.75  (+150%)   ↑  [MAJOR]
  Power      0.80 → 0.80  (0%)      →  [NONE]
  Wisdom     0.85 → 0.82  (-3.5%)   ↓  [MINOR]

Likely Causes:
  • Network over-secured (new firewall rules?)
  • Performance degraded (blocking legitimate traffic)
```

### Continuous Monitoring (Watch Mode)

Monitor targets continuously:
```bash
./pinpoint watch api.prod.com db.prod.com --interval 300
```

Features:
- Checks every 5 minutes (300s)
- Detects drift from baseline
- Generates alerts
- Records to history

Stop with Ctrl+C.

### Historical Tracking

Record network states over time:
```bash
# History is recorded automatically in watch mode

# View last 24 hours
./pinpoint history api.prod.com --hours 24

# View specific dimension trend
./pinpoint history api.prod.com --hours 48 --dimension love
```

**Output** (ASCII timeline):
```
Timeline: api.prod.com (Love dimension, last 24 hours)

0.90 ┤     ╭─╮
0.80 ┤   ╭─╯ ╰─╮
0.70 ┤  ╭╯     ╰╮
0.60 ┤╭─╯       ╰─╮
     └─────────────────────────→
     00:00      12:00      24:00

Statistics:
  Mean: 0.75
  Min: 0.58 (at 18:30)
  Max: 0.88 (at 08:15)
  Trend: ↓ Declining
```

### Export Results

Export diagnostics to share with team:

```bash
# Export as HTML (default)
./pinpoint health > results.json
./pinpoint export results.json -f html

# Export as Markdown
./pinpoint export results.json -f markdown

# Export as JSON
./pinpoint export results.json -f json
```

HTML export includes:
- Styled report with CSS
- All LJPW coordinates
- Visual charts
- Root cause analysis
- Shareable standalone file

### Alert Integration

Configure alerts in config file:
```yaml
alert_slack_webhook: https://hooks.slack.com/services/YOUR/WEBHOOK
alert_email: oncall@example.com

monitoring:
  alert_methods:
    - slack
    - email
```

Alerts trigger when:
- Health score drops significantly
- Any dimension drifts from baseline
- Patterns detected (flapping, DNS issues, etc.)

---

## Real-World Examples

### Example 1: API Slowdown Investigation

**Scenario**: Users report slow API responses

**Steps**:
```bash
# 1. Check current state
./pinpoint health

# Output shows:
# Love: 0.45 (POOR) - Low connectivity
# Power: 0.35 (POOR) - Low performance
# This suggests network congestion or capacity issue

# 2. Run slow connection recipe
./pinpoint run slow_connection api.prod.com

# 3. Check patterns
./pinpoint patterns

# Matches "The Congestion Point" pattern:
# Low Power + burst loss + time-dependent
```

**Diagnosis**: Network congestion during peak hours
**Action**: Scale bandwidth or implement traffic shaping

### Example 2: Can't Connect to Database

**Scenario**: Application can't reach database

**Steps**:
```bash
# 1. Quick diagnostic
./pinpoint run cant_connect db.prod.internal

# Output shows:
# Love: 0.15 (CRITICAL) - No connectivity
# Justice: 0.85 (HIGH) - Heavy policy enforcement
# Pattern: "Over-Secured Network"

# 2. Compare to baseline
./pinpoint diff db-baseline.json current-state.json

# Shows Justice increased 150%
# Likely cause: New firewall rule blocking traffic
```

**Diagnosis**: Firewall blocking legitimate database traffic
**Action**: Review and adjust firewall rules

### Example 3: Intermittent DNS Issues

**Scenario**: DNS resolution works sometimes but fails randomly

**Steps**:
```bash
# 1. Run intermittent recipe
./pinpoint run intermittent nameserver.internal

# Output shows:
# Wisdom: 0.25 (POOR) - DNS issues detected
# Variance: HIGH - Unstable
# Pattern: "The DNS Black Hole"

# 2. Watch over time
./pinpoint watch nameserver.internal --interval 60

# Shows periodic Wisdom drops every ~30 minutes

# 3. View history
./pinpoint history nameserver.internal --dimension wisdom
```

**Diagnosis**: DNS server intermittently failing
**Action**: Check DNS server health, add redundancy

### Example 4: Post-Deployment Validation

**Scenario**: Validate network state after firewall update

**Steps**:
```bash
# 1. Capture baseline BEFORE change
./pinpoint health > pre-deploy.json

# 2. Deploy firewall changes

# 3. Capture state AFTER change
./pinpoint health > post-deploy.json

# 4. Compare
./pinpoint diff pre-deploy.json post-deploy.json

# Output shows:
# Justice: 0.30 → 0.45 (+50%) - Expected (more rules)
# Love: 0.85 → 0.82 (-3.5%) - Acceptable (minimal impact)
# Power: 0.80 → 0.80 (0%) - Good (no performance impact)
```

**Result**: Deployment successful, security improved without degrading performance

### Example 5: Continuous Production Monitoring

**Scenario**: Monitor critical production services 24/7

**Setup**:
```bash
# 1. Create config
./pinpoint config create-example

# 2. Edit ~/.network-pinpointer/config.yaml
# Add production targets with baselines

# 3. Start monitoring
./pinpoint watch api.prod.com db.prod.com cdn.prod.com --interval 300
```

**What happens**:
- Checks every 5 minutes
- Compares to baseline
- Sends Slack alert if drift detected
- Records history for trending
- Detects known patterns automatically

---

## Interpreting Results

### Health Scores

| Score | Rating | Meaning |
|-------|--------|---------|
| 90-100% | EXCELLENT | Network in optimal condition |
| 75-89% | GOOD | Normal operation, minor issues |
| 60-74% | FAIR | Noticeable issues, investigate |
| 40-59% | POOR | Significant problems, action needed |
| 0-39% | CRITICAL | Severe issues, immediate action |

### LJPW Coordinate Ranges

| Range | Rating | Visual |
|-------|--------|--------|
| 0.8 - 1.0 | EXCELLENT | ████████████████████ |
| 0.6 - 0.79 | GOOD | ███████████████░░░░░ |
| 0.4 - 0.59 | FAIR | ███████████░░░░░░░░░ |
| 0.2 - 0.39 | POOR | ██████░░░░░░░░░░░░░░ |
| 0.0 - 0.19 | CRITICAL | ███░░░░░░░░░░░░░░░░░ |

### Common Patterns and What They Mean

**High Justice + Low Love**
- **Pattern**: "The Over-Secured Network"
- **Meaning**: Security rules blocking legitimate traffic
- **Action**: Audit firewall, relax overly strict rules

**Low Power + Good Love**
- **Pattern**: "The Long Haul"
- **Meaning**: Far distance, but connection working
- **Action**: Normal for geographically distant connections

**Varying Wisdom + Burst Loss**
- **Pattern**: "The Flaky Link"
- **Meaning**: Unreliable network hardware
- **Action**: Check cables, switches, NICs

**Low Wisdom (DNS)**
- **Pattern**: "The DNS Black Hole"
- **Meaning**: DNS resolution failing
- **Action**: Check DNS servers, configuration

**Justice Unstable + TTL Variance**
- **Pattern**: "Route Flapping"
- **Meaning**: Routes changing frequently
- **Action**: Check BGP, routing stability

### Root Cause Analysis

Network Pinpointer prioritizes issues by:

1. **Severity**: CRITICAL > HIGH > MEDIUM > LOW
2. **Impact**: How many dimensions affected
3. **Dependencies**: What's blocking what

**Example output**:
```
Root Causes (3 found):

  🔴 CRITICAL: DNS Resolution Failure
     Impact: Wisdom dimension (0.15)
     Affects: All dependent services
     Likely cause: DNS server unreachable
     Fix: Check DNS configuration

  🟠 HIGH: Packet Loss Detected
     Impact: Power dimension (0.35)
     Affects: Throughput, reliability
     Likely cause: Network congestion
     Fix: Scale bandwidth or QoS

  🟡 MEDIUM: High Latency
     Impact: Love dimension (0.45)
     Affects: User experience
     Likely cause: Geographic distance
     Fix: Use CDN or regional deployment
```

---

## Best Practices

### 1. Establish Baselines First
```bash
# For each critical service
./pinpoint run baseline api.prod.com
./pinpoint run baseline db.prod.com

# Save these for comparison
```

### 2. Use Recipes for Common Issues
Don't run raw diagnostics - use recipes that analyze the right dimensions:
- Slow? → `slow_connection`
- Can't connect? → `cant_connect`
- Flaky? → `intermittent`

### 3. Compare Before/After Changes
Always capture state before deploying changes:
```bash
./pinpoint health > before-firewall-update.json
# Deploy changes
./pinpoint health > after-firewall-update.json
./pinpoint diff before-firewall-update.json after-firewall-update.json
```

### 4. Monitor Continuously in Production
```bash
./pinpoint watch production-api production-db --interval 300
```

### 5. Export Results for Stakeholders
Technical teams can read LJPW, but managers need HTML:
```bash
./pinpoint health > report.json
./pinpoint export report.json -f html
# Send network-health-report.html to management
```

### 6. Learn the Patterns
Familiarize yourself with common patterns:
```bash
./pinpoint patterns
```
Recognizing patterns speeds up diagnosis.

### 7. Use Interactive Mode for Learning
```bash
./pinpoint interactive
```
Great for understanding LJPW framework interactively.

### 8. Combine Multiple Techniques
```bash
# 1. Quick check
./pinpoint quick-check api.prod.com

# 2. If issues found, run recipe
./pinpoint run slow_connection api.prod.com

# 3. Compare to history
./pinpoint history api.prod.com --hours 24

# 4. Check for known patterns
./pinpoint patterns

# 5. Export for team
./pinpoint export results.json -f html
```

---

## Troubleshooting

### "Scapy not available" Warning
```bash
pip install scapy
```
Scapy enables real packet capture. Without it, tool uses fallback mode.

### No History Found
History is only recorded when using watch mode:
```bash
./pinpoint watch targethost.com --interval 300
```

### Config File Not Loaded
Check config file locations:
1. `~/.network-pinpointer/config.yaml`
2. `./network-pinpointer.yaml`

Create example:
```bash
./pinpoint config create-example
```

### Permission Denied (Packet Capture)
Packet capture requires elevated privileges:
```bash
sudo ./pinpoint ping 8.8.8.8
```

---

## Summary

Network Pinpointer provides **semantic network diagnostics** through LJPW framework:

- **Love** = How well it connects
- **Justice** = What rules apply
- **Power** = How strong it is
- **Wisdom** = How smart/visible it is

**Quick commands**:
- `./pinpoint quick-check <host>` - Fast health check
- `./pinpoint recipes` - See diagnostic workflows
- `./pinpoint patterns` - Known issue patterns
- `./pinpoint explain <dimension>` - Learn LJPW
- `./pinpoint diff <before> <after>` - Compare states
- `./pinpoint watch <hosts>` - Monitor continuously

**Philosophy**: Networks aren't just pipes moving bits - they're **communication systems** with semantic meaning. LJPW reveals that meaning.

---

For more information: https://github.com/BruinGrowly/Network-Pinpointer
