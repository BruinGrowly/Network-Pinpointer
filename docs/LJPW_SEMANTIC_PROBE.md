# LJPW Semantic Probe - User Guide

## Overview

The LJPW Semantic Probe is a powerful feature that performs comprehensive semantic discovery and profiling of network targets. Instead of just asking "Is it alive?", it asks "What IS this thing semantically?" - revealing the target's LJPW identity, purpose, and characteristics.

## Quick Start

### Basic Usage

```bash
# Full semantic probe (standard scan)
python pinpoint.py ljpw google.com

# Quick scan (faster, fewer ports)
python pinpoint.py ljpw 192.168.1.1 --quick

# Deep scan (all common ports + extended analysis)
python pinpoint.py ljpw api.example.com --deep

# Export profile to JSON
python pinpoint.py ljpw database.local --export profile.json
```

### Enhanced Existing Commands

```bash
# Ping with semantic profile
python pinpoint.py ping google.com --ljpw-profile

# Traceroute with deep semantic analysis
python pinpoint.py traceroute google.com --semantic-deep
```

---

## Command Reference

### `ljpw` Command

**Syntax:**
```bash
python pinpoint.py ljpw <target> [--quick] [--deep] [--export FILE]
```

**Arguments:**
- `target` - Target host (IP address or hostname)
- `--quick` - Quick scan (ping + DNS + 4 ports) ~5-10 seconds
- `--deep` - Deep scan (ping + DNS + 22 ports) ~20-30 seconds
- `--export FILE` - Export profile to JSON file

**Default Behavior:**
- Standard scan: ping + DNS + 12 common ports (~10-15 seconds)

### Enhanced `ping` Command

**Syntax:**
```bash
python pinpoint.py ping <host> [options] [--ljpw-profile]
```

**New Flag:**
- `--ljpw-profile` - Add quick semantic profile to ping results

### Enhanced `traceroute` Command

**Syntax:**
```bash
python pinpoint.py traceroute <target> [options] [--semantic-deep]
```

**New Flag:**
- `--semantic-deep` - Deep semantic analysis of each hop (planned)

---

## What Gets Discovered

### Multi-Dimensional Discovery

The semantic probe performs several discovery operations:

1. **ICMP Ping** - Connectivity and latency
2. **DNS Resolution** - Forward lookup (hostname → IP)
3. **Reverse DNS** - Reverse lookup (IP → hostname)
4. **Port Scanning** - Service detection on common ports
5. **TTL Analysis** - Distance estimation (future)
6. **Banner Grabbing** - Service identification (future)

### Port Scanning Profiles

**Quick Scan (4 ports):**
- 22 (SSH)
- 80 (HTTP)
- 443 (HTTPS)
- 3389 (RDP)

**Standard Scan (12 ports):**
- 21 (FTP), 22 (SSH), 23 (Telnet)
- 25 (SMTP), 53 (DNS), 80 (HTTP)
- 443 (HTTPS), 3306 (MySQL), 3389 (RDP)
- 5432 (PostgreSQL), 8080 (HTTP-Alt), 8443 (HTTPS-Alt)

**Deep Scan (22 ports):**
- All standard ports plus:
- 110 (POP3), 143 (IMAP), 445 (SMB)
- 993 (IMAPS), 995 (POP3S), 1433 (MSSQL)
- 5900 (VNC), 6379 (Redis), 9090 (Prometheus)
- 27017 (MongoDB)

---

## Understanding the Output

### Discovery Results Section

```
📡 DISCOVERY RESULTS
  ✓ Ping: 14.2ms avg latency, 0% loss
  ✓ DNS: google.com → 142.250.185.46
  ✓ Reverse DNS: syd15s12-in-f14.1e100.net
  ✓ Open Ports: 2/12 scanned
    • 80/tcp   - http
    • 443/tcp  - https
```

**Interpretation:**
- ✓ = Successful discovery
- ✗ = Failed or no response
- Port list shows service names when known

### Semantic Profile Section

```
📊 SEMANTIC PROFILE
  Coordinates: Coordinates(L=0.75, J=0.35, P=0.65, W=0.25)
  
  Dimension Breakdown:
    Love (Connectivity):  ███████████████░░░░░ 75%  EXCELLENT
    Justice (Security):   ███████░░░░░░░░░░░░░ 35%  MODERATE
    Power (Performance):  █████████████░░░░░░░ 65%  GOOD
    Wisdom (Monitoring):  █████░░░░░░░░░░░░░░░ 25%  LOW
  
  Dominant Dimension: Love
  Harmony Score: 82% (EXCELLENT)
  Semantic Clarity: 68%
```

**Key Metrics:**

- **Coordinates** - LJPW position in 4D semantic space
- **Dominant Dimension** - Primary characteristic
- **Harmony Score** - Overall balance (0-100%)
  - 90-100%: Perfect harmony
  - 70-89%: Excellent
  - 50-69%: Good
  - 30-49%: Moderate
  - 0-29%: Poor
- **Semantic Clarity** - How well-defined the profile is

### Classification Section

```
🎯 CLASSIFICATION
  Primary Archetype: The Public Gateway (confidence: 94%)
    • High availability focus
    • Optimized for public connectivity
    • Balanced security posture
    • Designed for scale and performance
  
  Secondary Archetype: The Performance Engine (confidence: 67%)
```

**Archetype Matching:**
- Shows best-matching predefined patterns
- Confidence score indicates match quality
- Multiple archetypes = hybrid system

### Security Posture

```
🔒 SECURITY POSTURE: BALANCED
  ✓ Balanced security and accessibility
```

**Posture Levels:**
- **VERY_SECURE** - Strict access controls (Justice > 0.7, Love < 0.3)
- **SECURE** - Good security (Justice > 0.6)
- **BALANCED** - Appropriate mix (Justice 0.3-0.6, Love 0.3-0.7)
- **MODERATE** - Review recommended
- **OPEN** - Very accessible (Love > 0.7, Justice < 0.3)
- **POTENTIALLY_VULNERABLE** - Low security (Justice < 0.2)

### Recommendations

```
⚡ RECOMMENDATIONS
  → Consider HTTPS-only (port 443) and redirect HTTP traffic
  → Monitor for service availability (high Love dependency)
```

**Types of Recommendations:**
- Security improvements
- Configuration suggestions
- Best practices
- Harmony optimization

---

## Service Archetypes

### 1. The Public Gateway

**LJPW Signature:** High Love (0.6-1.0), Moderate Justice (0.2-0.5)

**Characteristics:**
- High availability focus
- Optimized for public connectivity
- Balanced security posture
- Designed for scale

**Typical Services:** HTTP, HTTPS, CDN

**Examples:** google.com, cloudflare.com, public APIs

### 2. The Security Sentinel

**LJPW Signature:** Low Love (0.0-0.3), High Justice (0.7-1.0)

**Characteristics:**
- Strict access policies
- Minimal exposed services
- Authentication required
- Security-first design

**Typical Services:** SSH, VPN, Firewall

**Examples:** Firewalls, bastion hosts, VPN gateways

### 3. The Data Vault

**LJPW Signature:** Moderate Love (0.2-0.5), High Power (0.6-1.0)

**Characteristics:**
- Restricted access patterns
- High performance requirements
- Data integrity focus
- Backend service orientation

**Typical Services:** MySQL, PostgreSQL, MongoDB, Redis

**Examples:** Database servers, data stores

### 4. The Performance Engine

**LJPW Signature:** Moderate Love (0.4-0.7), High Power (0.7-1.0)

**Characteristics:**
- High computational capacity
- Optimized for throughput
- Resource-intensive operations
- Backend processing focus

**Typical Services:** Application servers, compute nodes, APIs

**Examples:** App servers, compute clusters

### 5. The Monitoring Hub

**LJPW Signature:** Moderate Love (0.3-0.6), High Wisdom (0.7-1.0)

**Characteristics:**
- Observability focused
- Metrics and logs collection
- Diagnostic capabilities
- Information aggregation

**Typical Services:** SNMP, Prometheus, Grafana, Syslog

**Examples:** Monitoring servers, log aggregators

### 6. The Hybrid Service

**LJPW Signature:** Balanced (0.4-0.6 all dimensions)

**Characteristics:**
- Balanced across all dimensions
- Multiple service types
- General-purpose orientation
- Flexible configuration

**Typical Services:** Multiple

**Examples:** All-in-one servers, dev boxes

### 7. The Stealth Node

**LJPW Signature:** Very Low (0.0-0.2 all dimensions)

**Characteristics:**
- Minimal network presence
- Few or no open ports
- Possibly offline or dormant
- Intentionally hidden

**Typical Services:** Minimal or none

**Examples:** Honeypots, offline systems, air-gapped

### 8. The Over-Secured Fortress

**LJPW Signature:** Very Low Love (0.0-0.2), Very High Justice (0.8-1.0)

**Characteristics:**
- Extremely restrictive policies
- Minimal attack surface
- Hardened configuration
- Security over accessibility

**Typical Services:** Minimal secure services

**Examples:** Secure vaults, hardened bastions

---

## Use Cases

### 1. Network Discovery

**Scenario:** You've discovered a new IP on your network and want to know what it is.

```bash
python pinpoint.py ljpw 192.168.1.50
```

**Result:** Identifies the service type, purpose, and security posture.

### 2. Security Auditing

**Scenario:** Verify that public services have appropriate security.

```bash
python pinpoint.py ljpw api.example.com --deep
```

**Result:** Checks for insecure services, assesses security posture, provides recommendations.

### 3. Service Classification

**Scenario:** Classify multiple servers in your infrastructure.

```bash
for ip in 192.168.1.{10..20}; do
  python pinpoint.py ljpw $ip --quick --export "profile_$ip.json"
done
```

**Result:** Creates semantic profiles for batch analysis.

### 4. Quick Health Check

**Scenario:** Fast check if a service is up and properly configured.

```bash
python pinpoint.py ping database.local --ljpw-profile
```

**Result:** Ping + quick semantic assessment in one command.

### 5. Architecture Validation

**Scenario:** Verify that servers match their intended purpose.

```bash
python pinpoint.py ljpw web-server-01
# Should match "The Public Gateway" archetype

python pinpoint.py ljpw db-server-01
# Should match "The Data Vault" archetype
```

**Result:** Confirms semantic alignment with architecture.

---

## Interpreting Results

### High Love (Connectivity)

**What it means:**
- Service is designed for accessibility
- Many open ports or public services
- Focus on communication and integration

**Good for:** Web servers, APIs, public services

**Warning if:** Internal database or security system

### High Justice (Security)

**What it means:**
- Strong access controls
- Security policies enforced
- Restricted access patterns

**Good for:** Firewalls, secure systems, compliance servers

**Warning if:** Public service with very high Justice (may be over-secured)

### High Power (Performance)

**What it means:**
- Computational capabilities
- Resource-intensive operations
- Execution and control focus

**Good for:** Application servers, databases, compute nodes

**Warning if:** Simple monitoring system

### High Wisdom (Monitoring)

**What it means:**
- Information gathering focus
- Monitoring and diagnostics
- Observability orientation

**Good for:** Monitoring systems, log servers, SNMP agents

**Warning if:** Production application server

### Harmony Score Interpretation

**High Harmony (>70%):**
- Well-balanced system
- Clear purpose
- Good configuration

**Low Harmony (<50%):**
- Potential misconfiguration
- Unclear purpose
- Review recommended

---

## JSON Export Format

```json
{
  "target": "google.com",
  "ip_address": "142.250.185.46",
  "timestamp": "2025-11-28T18:46:03",
  "scan_duration": 13.0,
  "ljpw_coordinates": {
    "love": 0.75,
    "justice": 0.35,
    "power": 0.65,
    "wisdom": 0.25
  },
  "dominant_dimension": "Love",
  "harmony_score": 0.82,
  "service_classification": "Web Service",
  "security_posture": "BALANCED",
  "matched_archetypes": [
    {
      "name": "The Public Gateway",
      "confidence": 0.94
    }
  ],
  "open_ports": [80, 443],
  "recommendations": [
    "Consider HTTPS-only (port 443) and redirect HTTP traffic"
  ],
  "warnings": []
}
```

---

## Tips and Best Practices

### Choosing Scan Depth

- **Quick (`--quick`)**: Use for rapid discovery or when scanning many hosts
- **Standard (default)**: Best balance of speed and coverage
- **Deep (`--deep`)**: Use for comprehensive security audits

### Interpreting Archetypes

- **High confidence (>80%)**: Strong match, trust the classification
- **Moderate confidence (60-80%)**: Likely match, but verify
- **Low confidence (<60%)**: Hybrid or unusual system

### Security Assessment

- Always review warnings and recommendations
- Low Justice + High Love = potential security risk for internal systems
- Very High Justice + Very Low Love = may be over-secured

### Performance Considerations

- Quick scan: ~5-10 seconds
- Standard scan: ~10-15 seconds
- Deep scan: ~20-30 seconds
- Timeout issues may extend duration

---

## Troubleshooting

### "Failed to resolve target hostname"

**Cause:** DNS resolution failed

**Solution:** 
- Check hostname spelling
- Verify DNS is working
- Try using IP address directly

### "No response" for ping

**Cause:** ICMP blocked or host offline

**Solution:**
- This is normal for some hosts (e.g., google.com often blocks ICMP)
- Port scan will still work
- Check if host is actually reachable

### "No open ports detected"

**Cause:** All scanned ports are closed/filtered

**Solution:**
- Try `--deep` for more ports
- Host may be offline or heavily firewalled
- Verify you're scanning the correct target

### Unicode/Emoji display issues

**Cause:** Terminal encoding problems

**Solution:**
- Windows: Already handled with UTF-8 encoding
- Linux/Mac: Ensure terminal supports UTF-8

---

## Future Enhancements

Planned features for future releases:

- **Banner Grabbing**: Identify exact service versions
- **TTL Analysis**: OS fingerprinting from TTL values
- **Traceroute Integration**: Semantic analysis of network path
- **Historical Comparison**: Track profile changes over time
- **Machine Learning**: Improve archetype matching
- **Threat Assessment**: Integration with vulnerability databases

---

## Examples

### Example 1: Public Web Service

```bash
$ python pinpoint.py ljpw google.com --quick

🔍 LJPW Semantic Probe: google.com
======================================================================

📡 DISCOVERY RESULTS
  ✓ DNS: google.com → 142.250.185.46
  ✓ Open Ports: 2/4 scanned
    • 80/tcp   - http
    • 443/tcp  - https

📊 SEMANTIC PROFILE
  Coordinates: Coordinates(L=0.75, J=0.35, P=0.65, W=0.25)
  Dominant Dimension: Love
  Harmony Score: 82% (EXCELLENT)

🎯 CLASSIFICATION
  Primary Archetype: The Public Gateway (confidence: 94%)

💡 SEMANTIC INTERPRETATION
  Web content delivery or API service
  Strong Love (connectivity) characteristics indicate
  design for accessibility and service delivery.

🔒 SECURITY POSTURE: BALANCED
  ✓ Balanced security and accessibility

⚡ RECOMMENDATIONS
  → Consider HTTPS-only (port 443) and redirect HTTP traffic
```

### Example 2: Database Server

```bash
$ python pinpoint.py ljpw db.internal.local

🎯 CLASSIFICATION
  Primary Archetype: The Data Vault (confidence: 91%)
    • Restricted access patterns
    • High performance requirements
    • Data integrity focus
    • Backend service orientation

🔒 SECURITY POSTURE: SECURE
  ✓ Good security posture with appropriate controls
```

### Example 3: Enhanced Ping

```bash
$ python pinpoint.py ping 8.8.8.8 --ljpw-profile

Host: 8.8.8.8
Status: ✓ Reachable
Average Latency: 70.0ms

🌐 LJPW SEMANTIC PROFILE (Quick Scan)
  Target Classification: Secure Web Service
  Matched Archetype: The Public Gateway (confidence: 89%)
  Open Services: https
  Security Posture: BALANCED
  
  💡 Web content delivery or API service
```

---

## Conclusion

The LJPW Semantic Probe transforms network discovery from simple connectivity testing into deep semantic understanding. By revealing the "identity" and purpose of network targets through the LJPW framework, it enables smarter network management, better security auditing, and more informed decision-making.

**Happy probing!** 🚀
