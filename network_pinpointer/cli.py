#!/usr/bin/env python3
"""
Network-Pinpointer CLI

Command-line interface for semantic network diagnostics and analysis.
"""

import argparse
import sys
from typing import Optional

from .semantic_engine import NetworkSemanticEngine
from .diagnostics import NetworkDiagnostics
from .network_mapper import NetworkMapper
from .semantic_probe import SemanticProbe


def print_banner():
    """Print application banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                    NETWORK-PINPOINTER                         ║
║           Semantic Network Diagnostic Tool (LJPW)             ║
╚═══════════════════════════════════════════════════════════════╝

Love, Justice, Power, Wisdom - The Four Dimensions of Network Operations
"""
    print(banner)


def cmd_ping(args, engine: NetworkSemanticEngine):
    """Handle ping command"""
    diagnostics = NetworkDiagnostics(engine)

    print(f"\n🔍 Pinging {args.host}...")
    print("=" * 70)

    result = diagnostics.ping(args.host, count=args.count, timeout=args.timeout)

    # Print results
    print(f"\nHost: {result.host}")
    print(f"Status: {'✓ Reachable' if result.success else '✗ Unreachable'}")

    if result.success:
        print(f"Packets: {result.packets_received}/{result.packets_sent} received")
        print(f"Packet Loss: {result.packet_loss:.1f}%")
        print(f"Average Latency: {result.avg_latency:.1f}ms")

    # Semantic analysis
    print(f"\n📊 SEMANTIC ANALYSIS")
    print(f"Coordinates: {result.semantic_coords}")
    print(f"Analysis: {result.semantic_analysis}")

    # Visual representation
    l, j, p, w = result.semantic_coords
    print(f"\nDimension Breakdown:")
    print(f"  Love (Connectivity):  {'█' * int(l * 20):20s} {l:.0%}")
    print(f"  Justice (Validation): {'█' * int(j * 20):20s} {j:.0%}")
    print(f"  Power (Execution):    {'█' * int(p * 20):20s} {p:.0%}")
    print(f"  Wisdom (Diagnostic):  {'█' * int(w * 20):20s} {w:.0%}")

    # LJPW Profile if requested
    if hasattr(args, 'ljpw_profile') and args.ljpw_profile:
        print(f"\n🌐 LJPW SEMANTIC PROFILE (Quick Scan)")
        probe = SemanticProbe(engine)
        profile = probe.probe(args.host, quick=True)
        print_ljpw_profile_summary(profile)

    print("\n" + "=" * 70)


def cmd_traceroute(args, engine: NetworkSemanticEngine):
    """Handle traceroute command"""
    diagnostics = NetworkDiagnostics(engine)

    print(f"\n🔍 Tracing route to {args.target}...")
    print("=" * 70)

    result = diagnostics.traceroute(
        args.target, max_hops=args.max_hops, timeout=args.timeout
    )

    # Print results
    print(f"\nTarget: {result.target}")
    print(f"Total Hops: {result.total_hops}")

    if result.hops:
        print(f"\nRoute:")
        for hop in result.hops:
            print(
                f"  {hop.hop_number:2d}. {hop.host:20s} ({hop.ip:15s}) - {hop.latency:.1f}ms"
            )

    # Semantic analysis
    print(f"\n📊 SEMANTIC ANALYSIS")
    print(f"Coordinates: {result.semantic_coords}")
    print(f"Analysis: {result.semantic_analysis}")

    l, j, p, w = result.semantic_coords
    print(f"\nDimension Breakdown:")
    print(f"  Love (Path Discovery): {'█' * int(l * 20):20s} {l:.0%}")
    print(f"  Justice (Validation):  {'█' * int(j * 20):20s} {j:.0%}")
    print(f"  Power (Execution):     {'█' * int(p * 20):20s} {p:.0%}")
    print(f"  Wisdom (Analysis):     {'█' * int(w * 20):20s} {w:.0%}")

    print("\n" + "=" * 70)


def cmd_scan(args, engine: NetworkSemanticEngine):
    """Handle port scan command"""
    diagnostics = NetworkDiagnostics(engine)

    # Parse port range
    if "-" in args.ports:
        start, end = map(int, args.ports.split("-"))
        ports = list(range(start, end + 1))
    else:
        ports = [int(p) for p in args.ports.split(",")]

    print(f"\n🔍 Scanning {args.host} ports {args.ports}...")
    print("=" * 70)

    results = diagnostics.scan_ports(args.host, ports, timeout=args.timeout)

    # Print results
    open_ports = [r for r in results if r.is_open]
    closed_ports = [r for r in results if not r.is_open]

    print(f"\nHost: {args.host}")
    print(f"Open Ports: {len(open_ports)}/{len(results)}")

    if open_ports:
        print(f"\n✓ OPEN PORTS:")
        for result in open_ports:
            print(
                f"  {result.port:5d}/tcp - {result.service_name:15s} - {result.semantic_coords}"
            )

    if args.verbose and closed_ports:
        print(f"\n✗ CLOSED PORTS:")
        for result in closed_ports[:10]:  # Limit output
            print(f"  {result.port:5d}/tcp - closed")
        if len(closed_ports) > 10:
            print(f"  ... and {len(closed_ports) - 10} more closed ports")

    # Aggregate semantic analysis
    if open_ports:
        avg_l = sum(r.semantic_coords.love for r in open_ports) / len(open_ports)
        avg_j = sum(r.semantic_coords.justice for r in open_ports) / len(open_ports)
        avg_p = sum(r.semantic_coords.power for r in open_ports) / len(open_ports)
        avg_w = sum(r.semantic_coords.wisdom for r in open_ports) / len(open_ports)

        print(f"\n📊 AGGREGATE SEMANTIC ANALYSIS")
        print(f"  Love (Services):      {'█' * int(avg_l * 20):20s} {avg_l:.0%}")
        print(f"  Justice (Security):   {'█' * int(avg_j * 20):20s} {avg_j:.0%}")
        print(f"  Power (Capability):   {'█' * int(avg_p * 20):20s} {avg_p:.0%}")
        print(f"  Wisdom (Discovery):   {'█' * int(avg_w * 20):20s} {avg_w:.0%}")

    print("\n" + "=" * 70)


def cmd_ljpw(args, engine: NetworkSemanticEngine):
    """Handle LJPW semantic probe command"""
    probe = SemanticProbe(engine)
    
    print(f"\n🔍 LJPW Semantic Probe: {args.target}")
    print("=" * 70)
    
    # Perform probe
    profile = probe.probe(args.target, quick=args.quick, deep=args.deep)
    
    # Print full profile
    print_ljpw_profile(profile)
    
    # Export if requested
    if args.export:
        import json
        export_data = {
            'target': profile.target,
            'ip_address': profile.ip_address,
            'timestamp': profile.timestamp.isoformat(),
            'scan_duration': profile.scan_duration,
            'ljpw_coordinates': {
                'love': profile.ljpw_coordinates.love if profile.ljpw_coordinates else 0,
                'justice': profile.ljpw_coordinates.justice if profile.ljpw_coordinates else 0,
                'power': profile.ljpw_coordinates.power if profile.ljpw_coordinates else 0,
                'wisdom': profile.ljpw_coordinates.wisdom if profile.ljpw_coordinates else 0,
            },
            'dominant_dimension': profile.dominant_dimension,
            'harmony_score': profile.harmony_score,
            'service_classification': profile.service_classification,
            'security_posture': profile.security_posture,
            'matched_archetypes': [
                {'name': arch.name, 'confidence': conf}
                for arch, conf in profile.matched_archetypes
            ],
            'open_ports': [p.port for p in profile.open_ports if p.is_open],
            'recommendations': profile.recommendations,
            'warnings': profile.warnings,
        }
        
        with open(args.export, 'w') as f:
            json.dump(export_data, f, indent=2)
        print(f"\n✅ Profile exported to {args.export}")


def print_ljpw_profile_summary(profile):
    """Print summary LJPW profile (for --ljpw-profile flag)"""
    if not profile.ljpw_coordinates:
        print("  Unable to generate profile")
        return
    
    print(f"  Target Classification: {profile.service_classification}")
    
    if profile.matched_archetypes:
        arch, conf = profile.matched_archetypes[0]
        print(f"  Matched Archetype: {arch.name} (confidence: {conf:.0%})")
    
    open_services = [p.service_name for p in profile.open_ports if p.is_open and p.service_name != 'unknown']
    if open_services:
        print(f"  Open Services: {', '.join(open_services[:5])}")
    
    print(f"  Security Posture: {profile.security_posture.replace('_', ' ')}")
    
    if profile.inferred_purpose:
        print(f"\n  💡 {profile.inferred_purpose}")


def print_ljpw_profile(profile):
    """Print full LJPW semantic profile"""
    print(f"\n⏱️  Scan completed in {profile.scan_duration:.1f}s | Timestamp: {profile.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Discovery Results
    print(f"\n📡 DISCOVERY RESULTS")
    
    if profile.ping_result and profile.ping_result.success:
        print(f"  ✓ Ping: {profile.ping_result.avg_latency:.1f}ms avg latency, {profile.ping_result.packet_loss:.0f}% loss")
    else:
        print(f"  ✗ Ping: No response")
    
    if profile.dns_name:
        print(f"  ✓ DNS: {profile.dns_name} → {profile.ip_address}")
    
    if profile.reverse_dns:
        print(f"  ✓ Reverse DNS: {profile.reverse_dns}")
    
    open_ports = [p for p in profile.open_ports if p.is_open]
    if open_ports:
        print(f"  ✓ Open Ports: {len(open_ports)}/{len(profile.open_ports)} scanned")
        for port in open_ports[:10]:  # Limit display
            service = port.service_name if port.service_name != 'unknown' else ''
            print(f"    • {port.port}/tcp   - {service}")
        if len(open_ports) > 10:
            print(f"    ... and {len(open_ports) - 10} more")
    else:
        print(f"  ✗ Open Ports: None detected")
    
    # Semantic Profile
    if profile.ljpw_coordinates:
        print(f"\n📊 SEMANTIC PROFILE")
        print(f"  Coordinates: {profile.ljpw_coordinates}")
        print(f"")
        print(f"  Dimension Breakdown:")
        
        l, j, p, w = profile.ljpw_coordinates
        
        def get_rating(val):
            if val > 0.8: return "EXCELLENT"
            if val > 0.6: return "GOOD"
            if val > 0.4: return "MODERATE"
            if val > 0.2: return "LOW"
            return "VERY LOW"
        
        print(f"    Love (Connectivity):  {'█' * int(l * 20):20s} {l:.0%}  {get_rating(l)}")
        print(f"    Justice (Security):   {'█' * int(j * 20):20s} {j:.0%}  {get_rating(j)}")
        print(f"    Power (Performance):  {'█' * int(p * 20):20s} {p:.0%}  {get_rating(p)}")
        print(f"    Wisdom (Monitoring):  {'█' * int(w * 20):20s} {w:.0%}  {get_rating(w)}")
        print(f"")
        print(f"  Dominant Dimension: {profile.dominant_dimension}")
        print(f"  Harmony Score: {profile.harmony_score:.0%} ({get_rating(profile.harmony_score)})")
        print(f"  Semantic Clarity: {profile.semantic_clarity:.0%}")
    
    # Semantic Metrics (Dimensional Combinations)
    if profile.semantic_metrics:
        print(f"\n📈 SEMANTIC METRICS (Dimensional Combinations)")
        
        metrics_summary = profile.semantic_metrics
        print(f"  Overall Grade: {metrics_summary['overall_grade']}")
        
        # Show key metrics
        metrics = metrics_summary['metrics']
        
        print(f"\n  🔐 Security Metrics:")
        sec_conn = metrics['secure_connectivity']
        print(f"    Secure Connectivity (L+J):    {sec_conn.value:.0%}  [{sec_conn.grade}]  {sec_conn.interpretation}")
        
        sec_intel = metrics['security_intelligence']
        print(f"    Security Intelligence (J+W):  {sec_intel.value:.0%}  [{sec_intel.grade}]  {sec_intel.interpretation}")
        
        sec_ops = metrics['security_operations']
        print(f"    Security Operations (J+P+W):  {sec_ops.value:.0%}  [{sec_ops.grade}]  {sec_ops.interpretation}")
        
        print(f"\n  ⚡ Performance Metrics:")
        svc_cap = metrics['service_capacity']
        print(f"    Service Capacity (L+P):       {svc_cap.value:.0%}  [{svc_cap.grade}]  {svc_cap.interpretation}")
        
        int_perf = metrics['intelligent_performance']
        print(f"    Intelligent Performance (P+W): {int_perf.value:.0%}  [{int_perf.grade}]  {int_perf.interpretation}")
        
        print(f"\n  📊 Operational Metrics:")
        ops_exc = metrics['operational_excellence']
        print(f"    Operational Excellence (L+J+P): {ops_exc.value:.0%}  [{ops_exc.grade}]  {ops_exc.interpretation}")
        
        svc_intel = metrics['service_intelligence']
        print(f"    Service Intelligence (L+P+W):  {svc_intel.value:.0%}  [{svc_intel.grade}]  {svc_intel.interpretation}")
        
        # Show warnings if any
        warnings = metrics_summary['warnings']
        if warnings:
            print(f"\n  ⚠️  PATTERN WARNINGS ({len(warnings)}):")
            for warning in warnings[:5]:  # Show top 5
                severity_icon = {
                    'CRITICAL': '🚨',
                    'HIGH': '⚠️ ',
                    'MEDIUM': '📊',
                    'LOW': 'ℹ️ '
                }.get(warning.severity, '•')
                print(f"    {severity_icon} [{warning.severity}] {warning.pattern}")
                print(f"       {warning.description}")
                print(f"       → {warning.recommendation}")
                print()
    
    # Semantic Mass
    if profile.semantic_mass > 0:
        print(f"\n⚖️  SEMANTIC MASS & INFLUENCE")
        print(f"  Mass:      {profile.semantic_mass:.1f}")
        print(f"  Density:   {profile.semantic_density:.1f}")
        print(f"  Influence: {profile.semantic_influence:.1f}")
        
        # Categorize mass
        if profile.semantic_mass < 5:
            category = "Lightweight"
            desc = "Simple, single-purpose system"
        elif profile.semantic_mass < 20:
            category = "Medium"
            desc = "Multi-faceted system with moderate complexity"
        elif profile.semantic_mass < 50:
            category = "Heavyweight"
            desc = "Complex system with significant influence"
        else:
            category = "Massive"
            desc = "Critical infrastructure with dominant influence"
        
        print(f"  Category:  {category} - {desc}")
    
    # Classification
    print(f"\n🎯 CLASSIFICATION")
    
    if profile.matched_archetypes:
        primary_arch, primary_conf = profile.matched_archetypes[0]
        print(f"  Primary Archetype: {primary_arch.name} (confidence: {primary_conf:.0%})")
        for trait in primary_arch.characteristics[:4]:
            print(f"    • {trait}")
    else:
        print(f"  No archetype match found")
    
    # Semantic Interpretation
    if profile.inferred_purpose:
        print(f"\n💡 SEMANTIC INTERPRETATION")
        print(f"  {profile.inferred_purpose}")
        
        if profile.ljpw_coordinates:
            l, j, p, w = profile.ljpw_coordinates
            
            if l > 0.6:
                print(f"\n  This target exhibits strong Love (connectivity) characteristics,")
                print(f"  indicating it's designed for accessibility and service delivery.")
            
            if j > 0.6:
                print(f"\n  High Justice score suggests strong security measures and")
                print(f"  policy enforcement are in place.")
            elif j < 0.3:
                print(f"\n  Low Justice indicates minimal security restrictions,")
                print(f"  appropriate for public services but requiring careful monitoring.")
            
            if p > 0.6:
                print(f"\n  High Power indicates robust performance capabilities,")
                print(f"  consistent with a production service.")
    
    # Security Posture
    print(f"\n🔒 SECURITY POSTURE: {profile.security_posture.replace('_', ' ')}")
    
    posture_desc = {
        'VERY_SECURE': '✓ Highly secure configuration with strict access controls',
        'SECURE': '✓ Good security posture with appropriate controls',
        'BALANCED': '✓ Balanced security and accessibility',
        'MODERATE': '⚠️  Moderate security - review configuration',
        'OPEN': '⚠️  Very accessible - ensure this matches requirements',
        'POTENTIALLY_VULNERABLE': '🚨 Low security detected - immediate review recommended',
        'UNKNOWN': '? Unable to assess security posture',
    }
    
    if profile.security_posture in posture_desc:
        print(f"  {posture_desc[profile.security_posture]}")
    
    # Warnings
    if profile.warnings:
        print(f"\n⚠️  WARNINGS")
        for warning in profile.warnings:
            print(f"  • {warning}")
    
    # Recommendations
    if profile.recommendations:
        print(f"\n⚡ RECOMMENDATIONS")
        for rec in profile.recommendations:
            print(f"  → {rec}")
    
    print("\n" + "=" * 70)


def cmd_ljpw(args, engine: NetworkSemanticEngine):
    """Handle LJPW semantic probe command"""
    probe = SemanticProbe(engine)
    
    print(f"\n🔍 LJPW Semantic Probe: {args.target}")
    print("=" * 70)
    
    # Run probe
    print(f"🔍 Probing {args.target}...")
    
    import asyncio
    
    try:
        # Use async probe for better performance
        profile = asyncio.run(probe.probe_async(
            args.target, 
            quick=args.quick, 
            deep=args.deep
        ))
    except Exception as e:
        print(f"⚠️  Async probe failed, falling back to synchronous: {e}")
        profile = probe.probe(
            args.target, 
            quick=args.quick, 
            deep=args.deep
        )
    
    # Store profile
    try:
        from .semantic_storage import SemanticStorage
        storage = SemanticStorage()
        storage.store_profile(profile)
        # print(f"\n💾 Profile stored in semantic database")
    except Exception as e:
        print(f"\n⚠️  Failed to store profile: {e}")

    print_ljpw_profile(profile)
    
    # Export if requested
    if args.export:
        import json
        export_data = {
            'target': profile.target,
            'ip_address': profile.ip_address,
            'timestamp': profile.timestamp.isoformat(),
            'scan_duration': profile.scan_duration,
            'ljpw_coordinates': {
                'love': profile.ljpw_coordinates.love if profile.ljpw_coordinates else 0,
                'justice': profile.ljpw_coordinates.justice if profile.ljpw_coordinates else 0,
                'power': profile.ljpw_coordinates.power if profile.ljpw_coordinates else 0,
                'wisdom': profile.ljpw_coordinates.wisdom if profile.ljpw_coordinates else 0,
            },
            'dominant_dimension': profile.dominant_dimension,
            'harmony_score': profile.harmony_score,
            'service_classification': profile.service_classification,
            'security_posture': profile.security_posture,
            'matched_archetypes': [
                {'name': arch.name, 'confidence': conf}
                for arch, conf in profile.matched_archetypes
            ],
            'open_ports': [p.port for p in profile.open_ports if p.is_open],
            'recommendations': profile.recommendations,
            'warnings': profile.warnings,
        }
        
        with open(args.export, 'w') as f:
            json.dump(export_data, f, indent=2)
        print(f"\n✅ Profile exported to {args.export}")


def cmd_analyze(args, engine: NetworkSemanticEngine):
    """Analyze a network operation description"""
    print(f"\n🔍 Analyzing operation: '{args.operation}'")
    print("=" * 70)

    result = engine.analyze_operation(args.operation)

    print(f"\nOperation Type: {result.operation_type}")
    print(f"Dominant Dimension: {result.dominant_dimension}")
    print(f"Semantic Clarity: {result.semantic_clarity:.0%}")
    print(f"Harmony Score: {result.harmony_score:.0%}")

    print(f"\n📊 LJPW COORDINATES")
    print(f"Coordinates: {result.coordinates}")

    l, j, p, w = result.coordinates
    print(f"\nDimension Breakdown:")
    print(f"  Love (Connectivity):  {'█' * int(l * 40):40s} {l:.0%}")
    print(f"  Justice (Policy):     {'█' * int(j * 40):40s} {j:.0%}")
    print(f"  Power (Execution):    {'█' * int(p * 40):40s} {p:.0%}")
    print(f"  Wisdom (Information): {'█' * int(w * 40):40s} {w:.0%}")

    print(f"\nDistance from Anchor: {result.distance_from_anchor:.3f}")
    print(f"Concept Count: {result.concept_count}")

    print("\n" + "=" * 70)


def cmd_ice(args, engine: NetworkSemanticEngine):
    """Analyze Intent-Context-Execution harmony"""
    print(f"\n🔍 ICE HARMONY ANALYSIS")
    print("=" * 70)

    print(f"\nIntent:    {args.intent}")
    print(f"Context:   {args.context}")
    print(f"Execution: {args.execution}")

    result = engine.analyze_ice(args.intent, args.context, args.execution)

    print(f"\n📊 HARMONY METRICS")
    print(f"ICE Coherence:     {result['ice_coherence']:.0%}")
    print(f"ICE Balance:       {result['ice_balance']:.0%}")
    print(f"Overall Harmony:   {result['overall_harmony']:.0%}")
    print(f"Harmony Level:     {result['harmony_level']}")
    print(f"Benevolence Score: {result['benevolence_score']:.0%}")
    print(
        f"Intent-Execution Disharmony: {result['intent_execution_disharmony']:.3f}"
    )

    # Show individual components
    print(f"\n📍 COMPONENT COORDINATES")
    intent_result = result["intent"]
    context_result = result["context"]
    execution_result = result["execution"]

    print(f"\nIntent:    {intent_result.coordinates}")
    print(f"  Type: {intent_result.operation_type} ({intent_result.dominant_dimension})")

    print(f"\nContext:   {context_result.coordinates}")
    print(
        f"  Type: {context_result.operation_type} ({context_result.dominant_dimension})"
    )

    print(f"\nExecution: {execution_result.coordinates}")
    print(
        f"  Type: {execution_result.operation_type} ({execution_result.dominant_dimension})"
    )

    # Recommendations
    print(f"\n💡 RECOMMENDATIONS")
    if result["overall_harmony"] < 0.5:
        print(
            "⚠️  Low harmony detected - intent and execution are misaligned"
        )
        if result["intent_execution_disharmony"] > 1.0:
            print(
                "  → Review if the executed action matches the intended goal"
            )
        if result["ice_balance"] < 0.5:
            print(
                "  → Check if current context supports the intended operation"
            )
    elif result["overall_harmony"] < 0.7:
        print(
            "✓ Moderate harmony - minor misalignment between components"
        )
    else:
        print(
            "✅ Excellent harmony - intent, context, and execution are well-aligned"
        )

    print("\n" + "=" * 70)


def cmd_baseline(args, engine: NetworkSemanticEngine):
    """Handle baseline management commands"""
    from .semantic_storage import SemanticStorage
    from .semantic_probe import SemanticProbe
    
    storage = SemanticStorage()
    
    if args.baseline_command == "set":
        print(f"\n🎯 Setting baseline for {args.target}...")
        print("=" * 70)
        
        # Probe the target
        probe = SemanticProbe(engine)
        profile = probe.probe(args.target, quick=args.quick)
        
        # Store as baseline
        storage.store_profile(profile)
        storage.set_baseline(args.target, profile)
        
        print(f"✅ Baseline set for {args.target}")
        print(f"   Mass: {profile.semantic_mass:.1f}")
        print(f"   Clarity: {profile.semantic_clarity:.0%}")
        
    elif args.baseline_command == "show":
        baseline = storage.get_baseline(args.target)
        if baseline:
            print(f"\n📊 Baseline for {args.target}")
            print("=" * 70)
            print_ljpw_profile(baseline)
        else:
            print(f"❌ No baseline found for {args.target}")
    
    elif args.baseline_command == "list":
        baselines = storage.list_baselines()
        print(f"\n📋 Baselines ({len(baselines)} total)")
        print("=" * 70)
        for target in baselines:
            print(f"  • {target}")
    
    elif args.baseline_command == "delete":
        storage.delete_baseline(args.target)
        print(f"✅ Baseline deleted for {args.target}")


def cmd_drift(args, engine: NetworkSemanticEngine):
    """Handle drift detection commands"""
    from .semantic_storage import SemanticStorage
    from .semantic_drift import SemanticDriftDetector
    from .semantic_probe import SemanticProbe
    
    storage = SemanticStorage()
    
    if args.drift_command == "check":
        print(f"\n🔍 Checking drift for {args.target}...")
        print("=" * 70)
        
        # Get baseline
        baseline = storage.get_baseline(args.target)
        if not baseline:
            print(f"❌ No baseline found for {args.target}")
            print(f"   Run: pinpoint baseline set {args.target}")
            return
        
        # Probe current state
        probe = SemanticProbe(engine)
        current = probe.probe(args.target, quick=args.quick)
        
        # Detect drift
        detector = SemanticDriftDetector()
        drift = detector.detect_drift(baseline, current)
        
        # Display results
        print(f"\n📊 DRIFT ANALYSIS")
        print(f"  Magnitude: {drift.magnitude:.2f}")
        print(f"  Severity:  {drift.severity}")
        print(f"  Type:      {drift.drift_type}")
        
        if drift.affected_dimensions:
            print(f"\n  Affected Dimensions:")
            for dim in drift.affected_dimensions:
                print(f"    • {dim}")
        
        if drift.possible_causes:
            print(f"\n  Possible Causes:")
            for cause in drift.possible_causes:
                print(f"    • {cause}")
        
        if drift.recommendations:
            print(f"\n  Recommendations:")
            for rec in drift.recommendations:
                print(f"    → {rec}")
        
        # Store current profile
        storage.store_profile(current)
    
    elif args.drift_command == "history":
        profiles = storage.get_history(args.target, limit=args.limit)
        print(f"\n📈 Drift History for {args.target}")
        print("=" * 70)
        
        if not profiles:
            print(f"No history found for {args.target}")
            return
        
        for i, profile in enumerate(profiles, 1):
            print(f"\n{i}. {profile.timestamp}")
            print(f"   Mass: {profile.semantic_mass:.1f}, Clarity: {profile.semantic_clarity:.0%}")
            print(f"   L={profile.ljpw_coordinates.love:.2f}, J={profile.ljpw_coordinates.justice:.2f}, "
                  f"P={profile.ljpw_coordinates.power:.2f}, W={profile.ljpw_coordinates.wisdom:.2f}")


def cmd_similar(args, engine: NetworkSemanticEngine):
    """Handle similar systems command"""
    from .semantic_storage import SemanticStorage
    from .semantic_relationships import SemanticRelationshipAnalyzer
    from .semantic_probe import SemanticProbe
    
    storage = SemanticStorage()
    analyzer = SemanticRelationshipAnalyzer()
    
    print(f"\n🔍 Finding systems similar to {args.target}...")
    print("=" * 70)
    
    # Load all profiles
    all_targets = storage.list_all_targets()
    for target in all_targets:
        profile = storage.get_latest_profile(target)
        if profile:
            analyzer.add_profile(profile)
    
    # Find similar
    similar = analyzer.find_similar_systems(args.target, threshold=args.threshold, limit=args.limit)
    
    if similar:
        print(f"\n📊 Similar Systems (threshold: {args.threshold})")
        for target, distance in similar:
            similarity = 1.0 - (distance / 2.0)  # Convert distance to similarity
            print(f"  • {target:30s} distance: {distance:.2f}  similarity: {similarity:.0%}")
    else:
        print(f"No similar systems found (threshold: {args.threshold})")


def cmd_outliers(args, engine: NetworkSemanticEngine):
    """Handle outlier detection command"""
    from .semantic_storage import SemanticStorage
    from .semantic_relationships import SemanticRelationshipAnalyzer
    
    storage = SemanticStorage()
    analyzer = SemanticRelationshipAnalyzer()
    
    print(f"\n🔍 Detecting semantic outliers...")
    print("=" * 70)
    
    # Load all profiles
    all_targets = storage.list_all_targets()
    for target in all_targets:
        profile = storage.get_latest_profile(target)
        if profile:
            analyzer.add_profile(profile)
    
    # Detect outliers
    outliers = analyzer.detect_outliers(threshold=args.threshold, min_neighbors=args.min_neighbors)
    
    if outliers:
        print(f"\n⚠️  Outliers Detected ({len(outliers)})")
        for outlier in outliers:
            print(f"\n  • {outlier.target}")
            print(f"    Isolation Score: {outlier.isolation_score:.2f}")
            print(f"    Neighbors: {outlier.neighbor_count}")
            print(f"    Reason: {outlier.reason}")
            if outlier.recommendations:
                print(f"    → {outlier.recommendations[0]}")
    else:
        print(f"No outliers detected")


def cmd_cluster(args, engine: NetworkSemanticEngine):
    """Handle clustering command"""
    from .semantic_storage import SemanticStorage
    from .semantic_relationships import SemanticRelationshipAnalyzer
    
    storage = SemanticStorage()
    analyzer = SemanticRelationshipAnalyzer()
    
    print(f"\n🔍 Clustering systems semantically...")
    print("=" * 70)
    
    # Load all profiles
    all_targets = storage.list_all_targets()
    for target in all_targets:
        profile = storage.get_latest_profile(target)
        if profile:
            analyzer.add_profile(profile)
    
    # Cluster
    clusters = analyzer.cluster_systems(max_distance=args.max_distance, min_cluster_size=args.min_size)
    
    if clusters:
        print(f"\n📊 Clusters Found ({len(clusters)})")
        for i, cluster in enumerate(clusters, 1):
            print(f"\n  Cluster {i}: {cluster.name}")
            print(f"    Size: {cluster.size} systems")
            print(f"    Cohesion: {cluster.cohesion:.0%}")
            print(f"    Radius: {cluster.radius:.2f}")
            print(f"    Dominant: {cluster.dominant_characteristic}")
            print(f"    Members:")
            for member in cluster.members:
                print(f"      • {member}")
    else:
        print(f"No clusters found (max distance: {args.max_distance})")


def cmd_profile(args, engine: NetworkSemanticEngine):
    """Handle fractal profiling command"""
    from .fractal_profiler import FractalSemanticProfiler, Scale
    
    profiler = FractalSemanticProfiler(engine)
    scale = Scale(args.scale)
    
    print(f"\n🔍 Generating {scale.value}-scale profile for {args.target}...")
    print("=" * 70)
    
    try:
        profile = profiler.profile_at_scale(
            args.target, 
            scale, 
            port=args.port,
            service=args.service,
            hosts=args.hosts
        )
        
        print(f"\n🌐 FRACTAL PROFILE: {profile.scale.value.upper()}")
        print(f"Target: {profile.target}")
        print(f"Description: {profile.description}")
        
        print(f"\n📊 SEMANTIC COORDINATES")
        print(f"  Love:    {profile.coordinates.love:.2f}")
        print(f"  Justice: {profile.coordinates.justice:.2f}")
        print(f"  Power:   {profile.coordinates.power:.2f}")
        print(f"  Wisdom:  {profile.coordinates.wisdom:.2f}")
        
        print(f"\n⚖️  METRICS")
        print(f"  Mass:    {profile.semantic_mass:.1f}")
        print(f"  Clarity: {profile.semantic_clarity:.0%}")
        print(f"  Harmony: {profile.harmony_score:.0%}")
        
        if profile.metadata:
            print(f"\n📝 METADATA")
            for k, v in profile.metadata.items():
                print(f"  • {k}: {v}")
        
        if profile.sub_profiles:
            print(f"\n🔍 SUB-PROFILES ({len(profile.sub_profiles)})")
            for sub in profile.sub_profiles:
                print(f"  • {sub.target} ({sub.scale.value})")
                print(f"    L={sub.coordinates.love:.2f} J={sub.coordinates.justice:.2f} "
                      f"P={sub.coordinates.power:.2f} W={sub.coordinates.wisdom:.2f}")

    except Exception as e:
        print(f"❌ Error generating profile: {e}")


def cmd_visualize(args, engine: NetworkSemanticEngine):
    """Handle visualization commands"""
    from .semantic_storage import SemanticStorage
    from .visualization.cluster_map import ClusterMapGenerator
    
    storage = SemanticStorage()
    
    if args.viz_command == "clusters":
        print(f"\n🎨 Generating 3D cluster map...")
        print("=" * 70)
        
        # Load all profiles
        profiles = []
        all_targets = storage.get_all_targets()
        for target in all_targets:
            profile_dict = storage.get_profile(target)
            if profile_dict:
                # Convert dict to SemanticProfile object
                # We need to reconstruct it properly or modify ClusterMapGenerator to accept dicts
                # Let's modify ClusterMapGenerator to be more robust, but for now let's reconstruct
                from .semantic_engine import Coordinates
                from .semantic_probe import SemanticProfile
                
                coords = storage.dict_to_coordinates(profile_dict)
                
                # Create a minimal profile object for visualization
                # We can't easily reconstruct the full object without more data parsing
                # So let's create a dummy object or modify the generator
                
                # Better approach: Modify ClusterMapGenerator to handle dicts or objects
                # But since I can't edit two files at once easily without context switch,
                # I'll create a simple object wrapper here
                
                class SimpleProfile:
                    def __init__(self, d, c):
                        self.target = d['target']
                        self.ljpw_coordinates = c
                        self.semantic_mass = d.get('semantic_mass', 0.0)
                        self.inferred_purpose = d.get('inferred_purpose', '')
                
                profile_obj = SimpleProfile(profile_dict, coords)
                profiles.append(profile_obj)


        
        if not profiles:
            print("❌ No profiles found in storage. Run 'pinpoint ljpw <target>' first.")
            return
            
        # Generate map
        generator = ClusterMapGenerator()
        output_path = generator.generate_map(profiles, args.output)
        
        print(f"✅ Cluster map generated: {output_path}")
        print(f"   Open this file in your browser to view the interactive 3D visualization.")

    elif args.viz_command == "mass":
        from .visualization.mass_chart import MassDistributionChartGenerator
        print(f"\n📊 Generating mass distribution chart...")
        print("=" * 70)
        
        # Load all profiles
        profiles = []
        all_targets = storage.get_all_targets()
        for target in all_targets:
            profile_dict = storage.get_profile(target)
            if profile_dict:
                from .semantic_engine import Coordinates
                coords = storage.dict_to_coordinates(profile_dict)
                
                class SimpleProfile:
                    def __init__(self, d, c):
                        self.target = d['target']
                        self.ljpw_coordinates = c
                        self.semantic_mass = d.get('semantic_mass', 0.0)
                        self.harmony_score = d.get('harmony_score', 0.0)
                        self.inferred_purpose = d.get('inferred_purpose', '')
                
                profile_obj = SimpleProfile(profile_dict, coords)
                profiles.append(profile_obj)
        
        if not profiles:
            print("❌ No profiles found in storage. Run 'pinpoint ljpw <target>' first.")
            return
            
        # Generate chart
        generator = MassDistributionChartGenerator()
        output_path = generator.generate_chart(profiles, args.output)
        
        print(f"✅ Mass distribution chart generated: {output_path}")
        print(f"   Open this file in your browser to view the interactive charts.")

    elif args.viz_command == "drift":
        from .visualization.drift_timeline import DriftTimelineGenerator
        print(f"\n📈 Generating drift timeline for {args.target}...")
        print("=" * 70)
        
        # Load profile history
        profiles_dict = storage.get_profile_history(args.target, limit=100)
        
        if not profiles_dict:
            print(f"❌ No history found for {args.target}. Run 'pinpoint ljpw {args.target}' multiple times to build history.")
            return
            
        # Convert dicts to objects (or pass dicts if generator supports it)
        # The generator supports dicts, so we can pass directly
        
        # Generate timeline
        generator = DriftTimelineGenerator()
        output_path = generator.generate_timeline(args.target, profiles_dict, args.output)
        
        print(f"✅ Drift timeline generated: {output_path}")
        print(f"   Open this file in your browser to view the interactive timeline.")

    elif args.viz_command == "topology":
        from .visualization.topology_graph import NetworkTopologyGraphGenerator
        print(f"\n🕸️  Generating network topology graph...")
        print("=" * 70)
        
        # Load all profiles
        profiles = []
        all_targets = storage.get_all_targets()
        for target in all_targets:
            profile_dict = storage.get_profile(target)
            if profile_dict:
                from .semantic_engine import Coordinates
                coords = storage.dict_to_coordinates(profile_dict)
                
                class SimpleProfile:
                    def __init__(self, d, c):
                        self.target = d['target']
                        self.ljpw_coordinates = c
                        self.semantic_mass = d.get('semantic_mass', 0.0)
                        self.dominant_dimension = d.get('dominant_dimension', 'Unknown')
                
                profile_obj = SimpleProfile(profile_dict, coords)
                profiles.append(profile_obj)
        
        if not profiles:
            print("❌ No profiles found in storage. Run 'pinpoint ljpw <target>' first.")
            return
            
        # Generate graph
        generator = NetworkTopologyGraphGenerator()
        output_path = generator.generate_graph(profiles, args.output)
        
        print(f"✅ Topology graph generated: {output_path}")
        print(f"   Open this file in your browser to view the interactive 3D graph.")

    elif args.viz_command == "dashboard":
        from .visualization.dashboard import DashboardGenerator
        print(f"\n🚀 Generating interactive dashboard...")
        print("=" * 70)
        
        # Load all profiles
        profiles = []
        all_targets = storage.get_all_targets()
        for target in all_targets:
            profile_dict = storage.get_profile(target)
            if profile_dict:
                from .semantic_engine import Coordinates
                coords = storage.dict_to_coordinates(profile_dict)
                
                class SimpleProfile:
                    def __init__(self, d, c):
                        self.target = d['target']
                        self.ljpw_coordinates = c
                        self.semantic_mass = d.get('semantic_mass', 0.0)
                        self.harmony_score = d.get('harmony_score', 0.0)
                        self.dominant_dimension = d.get('dominant_dimension', 'Unknown')
                        self.security_posture = d.get('security_posture', 'UNKNOWN')
                
                profile_obj = SimpleProfile(profile_dict, coords)
                profiles.append(profile_obj)
        
        if not profiles:
            print("❌ No profiles found in storage. Run 'pinpoint ljpw <target>' first.")
            return
            
        # Generate dashboard
        generator = DashboardGenerator()
        output_path = generator.generate_dashboard(profiles, args.output)
        
        print(f"✅ Dashboard generated: {output_path}")
        print(f"   Open this file in your browser to view the unified semantic dashboard.")






def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Network-Pinpointer: Semantic Network Diagnostic Tool (LJPW Framework)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Ping command
    ping_parser = subparsers.add_parser("ping", help="Ping a host with semantic analysis")
    ping_parser.add_argument("host", help="Target host (IP or hostname)")
    ping_parser.add_argument(
        "-c", "--count", type=int, default=4, help="Number of packets (default: 4)"
    )
    ping_parser.add_argument(
        "-t", "--timeout", type=float, default=2.0, help="Timeout in seconds (default: 2.0)"
    )
    ping_parser.add_argument(
        "--ljpw-profile", action="store_true", help="Include LJPW semantic profile"
    )

    # Traceroute command
    traceroute_parser = subparsers.add_parser(
        "traceroute", help="Trace route to target with semantic analysis"
    )
    traceroute_parser.add_argument("target", help="Target host (IP or hostname)")
    traceroute_parser.add_argument(
        "-m", "--max-hops", type=int, default=30, help="Max hops (default: 30)"
    )
    traceroute_parser.add_argument(
        "-t", "--timeout", type=float, default=2.0, help="Timeout in seconds (default: 2.0)"
    )

    # Scan command
    scan_parser = subparsers.add_parser(
        "scan", help="Scan ports with semantic analysis"
    )
    scan_parser.add_argument("target", help="Target host (IP or hostname)")
    scan_parser.add_argument(
        "-p", "--ports", help="Ports to scan (e.g., '80,443' or '1-1000')"
    )
    scan_parser.add_argument(
        "--common", action="store_true", help="Scan common ports"
    )

    # Map command
    map_parser = subparsers.add_parser(
        "map", help="Map entire network with semantic topology analysis"
    )
    map_parser.add_argument("network", help="Network CIDR (e.g., 192.168.1.0/24)")
    map_parser.add_argument(
        "--export-json", help="Export topology to JSON file"
    )
    map_parser.add_argument(
        "-q", "--quiet", action="store_true", help="Minimal output"
    )

    # Analyze command
    analyze_parser = subparsers.add_parser(
        "analyze", help="Analyze a network operation description"
    )
    analyze_parser.add_argument(
        "operation", help="Operation description (e.g., 'configure firewall rules')"
    )

    # ICE analysis command
    ice_parser = subparsers.add_parser(
        "ice", help="Analyze Intent-Context-Execution harmony"
    )
    ice_parser.add_argument("intent", help="Intended operation")
    ice_parser.add_argument("context", help="Current network context")
    ice_parser.add_argument("execution", help="Actual execution")
    
    # LJPW semantic probe command
    ljpw_parser = subparsers.add_parser(
        "ljpw", help="Comprehensive LJPW semantic probe and profiling"
    )
    ljpw_parser.add_argument("target", help="Target host (IP or hostname)")
    ljpw_parser.add_argument(
        "--quick", action="store_true", help="Quick scan (ping + DNS + top 4 ports)"
    )
    ljpw_parser.add_argument(
        "--deep", action="store_true", help="Deep scan (all common ports + extended analysis)"
    )
    ljpw_parser.add_argument(
        "--export", help="Export profile to JSON file"
    )
    
    # Baseline management commands
    baseline_parser = subparsers.add_parser(
        "baseline", help="Manage semantic baselines"
    )
    baseline_subparsers = baseline_parser.add_subparsers(dest="baseline_command", help="Baseline operations")
    
    # baseline set
    baseline_set = baseline_subparsers.add_parser("set", help="Set baseline for a target")
    baseline_set.add_argument("target", help="Target host")
    baseline_set.add_argument("--quick", action="store_true", help="Quick scan")
    
    # baseline show
    baseline_show = baseline_subparsers.add_parser("show", help="Show baseline for a target")
    baseline_show.add_argument("target", help="Target host")
    
    # baseline list
    baseline_list = baseline_subparsers.add_parser("list", help="List all baselines")
    
    # baseline delete
    baseline_delete = baseline_subparsers.add_parser("delete", help="Delete baseline")
    baseline_delete.add_argument("target", help="Target host")
    
    # Drift detection commands
    drift_parser = subparsers.add_parser(
        "drift", help="Detect semantic drift"
    )
    drift_subparsers = drift_parser.add_subparsers(dest="drift_command", help="Drift operations")
    
    # drift check
    drift_check = drift_subparsers.add_parser("check", help="Check drift for a target")
    drift_check.add_argument("target", help="Target host")
    drift_check.add_argument("--quick", action="store_true", help="Quick scan")
    drift_check.add_argument("--threshold", type=float, default=0.3, help="Drift threshold (default: 0.3)")
    
    # drift history
    drift_history = drift_subparsers.add_parser("history", help="Show drift history")
    drift_history.add_argument("target", help="Target host")
    drift_history.add_argument("--limit", type=int, default=10, help="Number of records (default: 10)")
    
    # Relationship analysis commands
    similar_parser = subparsers.add_parser(
        "similar", help="Find semantically similar systems"
    )
    similar_parser.add_argument("target", help="Target host")
    similar_parser.add_argument("--threshold", type=float, default=0.5, help="Similarity threshold (default: 0.5)")
    similar_parser.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")
    
    outliers_parser = subparsers.add_parser(
        "outliers", help="Detect semantic outliers"
    )
    outliers_parser.add_argument("--threshold", type=float, default=1.0, help="Outlier threshold (default: 1.0)")
    outliers_parser.add_argument("--min-neighbors", type=int, default=1, help="Min neighbors (default: 1)")
    
    cluster_parser = subparsers.add_parser(
        "cluster", help="Cluster systems semantically"
    )
    cluster_parser.add_argument("--max-distance", type=float, default=0.5, help="Max cluster distance (default: 0.5)")
    cluster_parser.add_argument("--min-size", type=int, default=2, help="Min cluster size (default: 2)")

    # Fractal profiling command
    profile_parser = subparsers.add_parser(
        "profile", help="Generate fractal semantic profile at specified scale"
    )
    profile_parser.add_argument("target", help="Target to profile")
    profile_parser.add_argument(
        "--scale", 
        choices=["packet", "port", "service", "host", "network", "infrastructure", "organization"],
        default="host",
        help="Fractal scale level (default: host)"
    )
    profile_parser.add_argument("--port", type=int, help="Port number (for port scale)")
    profile_parser.add_argument("--service", help="Service name (for service scale)")
    profile_parser.add_argument("--hosts", nargs="+", help="List of hosts (for network scale)")

    # Visualization command
    viz_parser = subparsers.add_parser(
        "visualize", help="Visualize semantic data"
    )
    viz_subparsers = viz_parser.add_subparsers(dest="viz_command", help="Visualization type")
    
    # visualize clusters
    viz_clusters = viz_subparsers.add_parser("clusters", help="Visualize semantic clusters (3D)")
    viz_clusters.add_argument("--output", default="clusters.html", help="Output HTML file (default: clusters.html)")
    
    # visualize mass
    viz_mass = viz_subparsers.add_parser("mass", help="Visualize semantic mass distribution")
    viz_mass.add_argument("--output", default="mass_distribution.html", help="Output HTML file (default: mass_distribution.html)")
    
    # visualize drift
    viz_drift = viz_subparsers.add_parser("drift", help="Visualize semantic drift timeline")
    viz_drift.add_argument("target", help="Target host to visualize")
    viz_drift.add_argument("--output", help="Output HTML file (default: drift_timeline_<target>.html)")
    
    # visualize topology
    viz_topo = viz_subparsers.add_parser("topology", help="Visualize network topology (3D)")
    viz_topo.add_argument("--output", default="topology.html", help="Output HTML file (default: topology.html)")
    
    # visualize dashboard
    viz_dash = viz_subparsers.add_parser("dashboard", help="Visualize unified dashboard")
    viz_dash.add_argument("--output", default="dashboard.html", help="Output HTML file (default: dashboard.html)")
    
    args = parser.parse_args()

    if not args.command:
        print_banner()
        parser.print_help()
        sys.exit(1)

    # Initialize semantic engine
    engine = NetworkSemanticEngine()

    # Route to appropriate command handler
    if args.command == "ping":
        cmd_ping(args, engine)
    elif args.command == "traceroute":
        cmd_traceroute(args, engine)
    elif args.command == "scan":
        cmd_scan(args, engine)
    elif args.command == "map":
        cmd_map(args, engine)
    elif args.command == "analyze":
        cmd_analyze(args, engine)
    elif args.command == "ice":
        cmd_ice(args, engine)
    elif args.command == "ljpw":
        cmd_ljpw(args, engine)
    elif args.command == "baseline":
        cmd_baseline(args, engine)
    elif args.command == "drift":
        cmd_drift(args, engine)
    elif args.command == "similar":
        cmd_similar(args, engine)
    elif args.command == "outliers":
        cmd_outliers(args, engine)
    elif args.command == "cluster":
        cmd_cluster(args, engine)
    elif args.command == "profile":
        cmd_profile(args, engine)
    elif args.command == "visualize":
        cmd_visualize(args, engine)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
