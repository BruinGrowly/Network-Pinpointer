# Network Pinpointer - Calibration Guide

**Version**: 1.0
**Date**: 2025-01-07
**Based on**: LJPW Mathematical Baselines v1.0

This guide explains how to calibrate Network Pinpointer to map **raw packet/network metrics** to **LJPW coordinates** using the mathematical baselines.

---

## Table of Contents

1. [Overview](#overview)
2. [Calibration Philosophy](#calibration-philosophy)
3. [Raw Metrics → LJPW Mapping](#raw-metrics--ljpw-mapping)
4. [Network-Specific Constants](#network-specific-constants)
5. [Implementation Examples](#implementation-examples)
6. [Validation](#validation)
7. [Tuning for Your Environment](#tuning-for-your-environment)

---

## Overview

Network Pinpointer uses the **LJPW Mathematical Baselines** (φ⁻¹, √2-1, e-2, ln2) as objective reference points. To measure real networks, we need to:

1. **Measure** observable network metrics (latency, packet loss, bandwidth, etc.)
2. **Normalize** these to [0, 1] range
3. **Calibrate** to LJPW space using domain knowledge
4. **Compare** to Natural Equilibrium (0.618, 0.414, 0.718, 0.693)

---

## Calibration Philosophy

### Three Principles

1. **Observable**: Metrics must be measurable from packets/flows
2. **Meaningful**: Direct relationship to LJPW dimension
3. **Objective**: Repeatable, not subjective

### Natural Equilibrium as Target

The **Natural Equilibrium** (NE) represents optimal balance:
- Love: 0.618 (golden ratio inverse)
- Justice: 0.414 (Pythagorean ratio)
- Power: 0.718 (exponential base)
- Wisdom: 0.693 (information unit)

**Goal**: Calibrate so that a well-functioning network measures near NE.

---

## Raw Metrics → LJPW Mapping

### Love: Connectivity & Responsiveness

**Measures**:
1. **Reachability** (can we connect?)
2. **Latency** (how fast?)
3. **Packet loss** (how reliable?)
4. **Connection success rate**

**Formula**:

```python
def calculate_love(
    reachability: float,      # 0-1 (1 = reachable)
    rtt_ms: float,            # Round-trip time in ms
    packet_loss_rate: float,  # 0-1 (0 = no loss)
    connection_success_rate: float  # 0-1 (1 = all succeed)
) -> float:
    """
    Calculate Love from network connectivity metrics.

    Targets:
    - Excellent network: RTT < 10ms, 0% loss → Love ≈ 0.9
    - Good network: RTT = 30ms, 1% loss → Love ≈ 0.7
    - Natural Equilibrium: RTT = 50ms, 2% loss → Love ≈ 0.618
    - Poor network: RTT > 200ms, 10% loss → Love ≈ 0.3
    """
    # Normalize RTT (0ms = 1.0, 500ms = 0.0)
    rtt_score = max(0.0, 1.0 - (rtt_ms / 500.0))

    # Normalize packet loss (0% = 1.0, 20% = 0.0)
    loss_score = max(0.0, 1.0 - (packet_loss_rate / 0.20))

    # Combine with weights
    love = (
        0.30 * reachability +
        0.35 * rtt_score +
        0.20 * loss_score +
        0.15 * connection_success_rate
    )

    return min(1.0, max(0.0, love))
```

**Calibration Examples**:

| Network State | RTT | Loss | Success | → Love |
|---------------|-----|------|---------|--------|
| Excellent LAN | 2ms | 0% | 100% | 0.95 |
| Good WAN | 30ms | 1% | 98% | 0.75 |
| **Natural Equilibrium** | 50ms | 2% | 95% | **0.618** |
| Degraded | 150ms | 8% | 85% | 0.35 |
| Failing | 400ms | 18% | 60% | 0.10 |

### Justice: Policy & Boundaries

**Measures**:
1. **Firewall block rate** (how much is filtered?)
2. **Policy compliance** (are rules followed?)
3. **ACL hit rate** (how much traffic is controlled?)
4. **Security event rate**

**Formula**:

```python
def calculate_justice(
    firewall_block_rate: float,   # 0-1 (proportion of packets blocked)
    policy_compliance_rate: float, # 0-1 (1 = all compliant)
    acl_coverage: float,           # 0-1 (proportion of traffic with ACLs)
    security_event_rate: float     # Events per 1000 packets (lower is better)
) -> float:
    """
    Calculate Justice from network security/policy metrics.

    Targets:
    - Too restrictive: Block > 50%, many false positives → Justice > 0.8
    - Natural Equilibrium: Block ≈ 10-15%, balanced → Justice ≈ 0.414
    - Too permissive: Block < 2%, weak security → Justice < 0.2
    """
    # Normalize block rate (target: 10-15% blocking)
    # Below 10%: too permissive, above 15%: too restrictive
    optimal_block_rate = 0.125  # 12.5%
    block_score = 1.0 - abs(firewall_block_rate - optimal_block_rate) / optimal_block_rate

    # Policy compliance (1.0 = perfect compliance)
    compliance_score = policy_compliance_rate

    # ACL coverage (0.5 = good balance, not everything needs ACLs)
    acl_score = 1.0 - abs(acl_coverage - 0.5) / 0.5

    # Security events (0 = 1.0, 10/1000 = 0.0)
    event_score = max(0.0, 1.0 - (security_event_rate / 10.0))

    # Combine
    justice = (
        0.35 * block_score +
        0.30 * compliance_score +
        0.20 * acl_score +
        0.15 * event_score
    )

    return min(1.0, max(0.0, justice))
```

**Calibration Examples**:

| Network State | Block Rate | Compliance | Events/1k | → Justice |
|---------------|------------|------------|-----------|-----------|
| Bureaucratic (over-restrictive) | 45% | 98% | 0.5 | 0.85 |
| **Natural Equilibrium** | 12% | 95% | 2 | **0.414** |
| Permissive (under-secured) | 3% | 85% | 8 | 0.25 |

### Power: Performance & Capacity

**Measures**:
1. **Throughput** (actual vs. capacity)
2. **Bandwidth utilization**
3. **Queue depth** (congestion indicator)
4. **Jitter** (performance stability)

**Formula**:

```python
def calculate_power(
    throughput_mbps: float,       # Current throughput
    link_capacity_mbps: float,    # Link capacity
    bandwidth_utilization: float, # 0-1
    avg_queue_depth: int,         # 0-100 packets
    jitter_ms: float              # Jitter in ms
) -> float:
    """
    Calculate Power from network performance metrics.

    Targets:
    - High performance: 80% utilization, low queue, low jitter → Power ≈ 0.9
    - Natural Equilibrium: 60-70% utilization, moderate queue → Power ≈ 0.718
    - Congested: > 95% utilization, high queue, high jitter → Power < 0.3
    """
    # Throughput efficiency (0.6-0.8 is optimal, not 100%)
    throughput_ratio = throughput_mbps / link_capacity_mbps if link_capacity_mbps > 0 else 0
    optimal_utilization = 0.70
    throughput_score = 1.0 - abs(throughput_ratio - optimal_utilization) / optimal_utilization

    # Bandwidth utilization (similar, 60-70% is good)
    utilization_score = 1.0 - abs(bandwidth_utilization - 0.70) / 0.70

    # Queue depth (0 = 1.0, 50 = 0.0)
    queue_score = max(0.0, 1.0 - (avg_queue_depth / 50.0))

    # Jitter (0ms = 1.0, 50ms = 0.0)
    jitter_score = max(0.0, 1.0 - (jitter_ms / 50.0))

    # Combine
    power = (
        0.35 * throughput_score +
        0.30 * utilization_score +
        0.20 * queue_score +
        0.15 * jitter_score
    )

    return min(1.0, max(0.0, power))
```

**Calibration Examples**:

| Network State | Utilization | Queue | Jitter | → Power |
|---------------|-------------|-------|--------|---------|
| High performance | 75% | 5 pkt | 2ms | 0.90 |
| **Natural Equilibrium** | 68% | 15 pkt | 8ms | **0.718** |
| Congested | 96% | 45 pkt | 35ms | 0.25 |

### Wisdom: Intelligence & Observability

**Measures**:
1. **DNS success rate** (can we discover?)
2. **Monitoring coverage** (what % is observable?)
3. **Routing visibility** (do we understand paths?)
4. **Metadata richness** (how much context?)

**Formula**:

```python
def calculate_wisdom(
    dns_success_rate: float,      # 0-1 (1 = all resolve)
    monitoring_coverage: float,   # 0-1 (1 = full visibility)
    routing_visibility: float,    # 0-1 (1 = all paths known)
    metadata_richness: float      # 0-1 (1 = rich context)
) -> float:
    """
    Calculate Wisdom from network intelligence/observability metrics.

    Targets:
    - High observability: 95%+ DNS, full monitoring → Wisdom ≈ 0.9
    - Natural Equilibrium: 90% DNS, good monitoring → Wisdom ≈ 0.693
    - Poor observability: < 70% DNS, gaps in monitoring → Wisdom < 0.4
    """
    # All components equally weighted
    wisdom = (
        0.30 * dns_success_rate +
        0.30 * monitoring_coverage +
        0.25 * routing_visibility +
        0.15 * metadata_richness
    )

    return min(1.0, max(0.0, wisdom))
```

**Calibration Examples**:

| Network State | DNS | Monitoring | Routing | → Wisdom |
|---------------|-----|------------|---------|----------|
| High visibility | 98% | 95% | 90% | 0.92 |
| **Natural Equilibrium** | 92% | 85% | 75% | **0.693** |
| Low visibility | 75% | 60% | 50% | 0.55 |

---

## Network-Specific Constants

### RTT Thresholds by Network Type

| Network Type | Excellent | Good | NE | Poor |
|--------------|-----------|------|-----|------|
| **LAN** | < 2ms | 2-10ms | 15ms | > 50ms |
| **Enterprise WAN** | < 10ms | 10-30ms | 50ms | > 150ms |
| **Cloud** | < 20ms | 20-50ms | 80ms | > 200ms |
| **Internet/CDN** | < 50ms | 50-100ms | 150ms | > 300ms |

### Block Rate Thresholds by Environment

| Environment | Optimal Block Rate | NE Justice |
|-------------|-------------------|------------|
| **Internal Dev** | 5-8% | 0.30 |
| **Enterprise Office** | 10-15% | 0.414 |
| **DMZ** | 20-30% | 0.55 |
| **Public Internet** | 40-60% | 0.75 |

---

## Implementation Examples

### Example 1: LAN Environment

```python
from network_pinpointer.ljpw_baselines import LJPWBaselines, ReferencePoints

# Measured metrics from LAN
rtt_ms = 3.5
packet_loss = 0.001  # 0.1%
reachability = 1.0
connection_success = 0.99

# Calculate Love
love = calculate_love(reachability, rtt_ms, packet_loss, connection_success)
# Result: love ≈ 0.88 (high, as expected for LAN)

# Other dimensions...
justice = 0.35  # Low, internal network
power = 0.85    # High, good performance
wisdom = 0.80   # High, full visibility

# Compare to Natural Equilibrium
baselines = LJPWBaselines()
d_ne = baselines.distance_from_natural_equilibrium(love, justice, power, wisdom)
# Result: d_ne ≈ 0.45 (moderate distance, Justice too low for NE)

# Get recommendations
diagnostic = baselines.full_diagnostic(love, justice, power, wisdom)
print(f"Primary focus: {diagnostic['improvements']['primary_focus']}")
# Output: "Primary focus: Justice" (needs strengthening)
print(f"Target Justice: {diagnostic['improvements']['primary_target']:.3f}")
# Output: "Target Justice: 0.414" (Natural Equilibrium)
```

### Example 2: Production WAN

```python
# Measured metrics from production WAN
rtt_ms = 48
packet_loss = 0.018  # 1.8%
reachability = 1.0
connection_success = 0.96

love = calculate_love(reachability, rtt_ms, packet_loss, connection_success)
# Result: love ≈ 0.65

# Security metrics
firewall_block_rate = 0.12  # 12%
policy_compliance = 0.95
acl_coverage = 0.50
security_events_per_1k = 1.8

justice = calculate_justice(firewall_block_rate, policy_compliance, acl_coverage, security_events_per_1k)
# Result: justice ≈ 0.42

# Performance
throughput = 850  # Mbps
capacity = 1000   # Mbps
utilization = 0.68
queue_depth = 12
jitter = 7

power = calculate_power(throughput, capacity, utilization, queue_depth, jitter)
# Result: power ≈ 0.72

# Observability
dns_success = 0.94
monitoring = 0.88
routing_vis = 0.80
metadata = 0.75

wisdom = calculate_wisdom(dns_success, monitoring, routing_vis, metadata)
# Result: wisdom ≈ 0.71

# Check against Natural Equilibrium
baselines = LJPWBaselines()
d_ne = baselines.distance_from_natural_equilibrium(love, justice, power, wisdom)
# Result: d_ne ≈ 0.08 (very close to NE! Well-balanced network)

diagnostic = baselines.full_diagnostic(love, justice, power, wisdom)
print(f"Balance status: {diagnostic['interpretation']['balance_status']}")
# Output: "Balance status: near-optimal"
print(f"Composite score: {diagnostic['metrics']['composite_score']:.3f}")
# Output: "Composite score: 1.15" (high-performing)
```

---

## Validation

### Validation Protocol

1. **Measure** baseline network with known characteristics
2. **Calculate** LJPW using calibration formulas
3. **Compare** to expected values:
   - Excellent network: Composite score > 1.2
   - Good network: Composite score > 1.0
   - Near NE: Distance from NE < 0.2
   - Degraded: Composite score < 0.8

4. **Adjust** weights if systematic bias detected

### Expected Ranges by Network Type

| Network Type | Love | Justice | Power | Wisdom | Composite |
|--------------|------|---------|-------|--------|-----------|
| **LAN (Internal)** | 0.85-0.95 | 0.25-0.40 | 0.80-0.95 | 0.75-0.90 | 1.15-1.35 |
| **Enterprise WAN** | 0.60-0.75 | 0.35-0.50 | 0.65-0.80 | 0.65-0.80 | 0.95-1.15 |
| **Cloud** | 0.55-0.70 | 0.40-0.55 | 0.70-0.85 | 0.70-0.85 | 0.95-1.20 |
| **Internet** | 0.40-0.60 | 0.55-0.75 | 0.50-0.70 | 0.60-0.75 | 0.75-1.00 |

---

## Tuning for Your Environment

### Step 1: Baseline Measurement

Measure a **known good** network state for 24 hours:

```python
# Collect metrics
metrics = {
    'rtt_p50': 45,      # 50th percentile RTT
    'rtt_p95': 85,      # 95th percentile RTT
    'packet_loss': 0.015,
    'block_rate': 0.11,
    'utilization': 0.68,
    # ... etc
}
```

### Step 2: Calculate LJPW

```python
love = calculate_love(...)
justice = calculate_justice(...)
power = calculate_power(...)
wisdom = calculate_wisdom(...)

print(f"Baseline LJPW: L={love:.3f}, J={justice:.3f}, P={power:.3f}, W={wisdom:.3f}")
```

### Step 3: Compare to Natural Equilibrium

```python
baselines = LJPWBaselines()
d_ne = baselines.distance_from_natural_equilibrium(love, justice, power, wisdom)

if d_ne < 0.2:
    print("✓ Calibration good! Network near Natural Equilibrium.")
elif d_ne < 0.5:
    print("⚠ Moderate deviation. Check primary focus dimension.")
    diagnostic = baselines.full_diagnostic(love, justice, power, wisdom)
    print(f"  Focus on: {diagnostic['improvements']['primary_focus']}")
else:
    print("✗ Significant deviation. Re-check metric collection or adjust weights.")
```

### Step 4: Adjust Weights (if needed)

If systematic bias detected:

```python
# Example: If Love consistently 20% too high
def calculate_love_adjusted(reachability, rtt_ms, packet_loss, connection_success):
    raw_love = calculate_love(reachability, rtt_ms, packet_loss, connection_success)
    return raw_love * 0.80  # Apply correction factor
```

---

## Summary

**Calibration Process**:
1. ✅ Collect raw network metrics (RTT, loss, block rate, throughput, etc.)
2. ✅ Normalize to [0, 1] using formulas in this guide
3. ✅ Combine into LJPW coordinates
4. ✅ Compare to Natural Equilibrium (0.618, 0.414, 0.718, 0.693)
5. ✅ Use mathematical baselines for interpretation

**Key Formulas**:
- Love: Connectivity (reachability, RTT, packet loss)
- Justice: Policy enforcement (block rate, compliance, ACLs)
- Power: Performance (throughput, utilization, queue, jitter)
- Wisdom: Observability (DNS, monitoring, routing visibility)

**Validation**:
- Well-functioning network should measure **near Natural Equilibrium**
- Distance from NE < 0.2 = "near-optimal"
- Composite score > 1.0 = "solid performance"

**Next Steps**:
1. Implement metric collection in your environment
2. Use calibration formulas to calculate LJPW
3. Compare to Natural Equilibrium and track over time
4. Use improvement suggestions to optimize

---

**For more information**:
- LJPW Mathematical Baselines: `docs/LJPW-MATHEMATICAL-BASELINES.md`
- Network Pinpointer API: `docs/PRODUCTION_FEATURES.md`
- Example implementations: `examples/calibration_examples.py`
