#!/bin/bash
# Network-Pinpointer Demo Script
# Demonstrates all major features

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         NETWORK-PINPOINTER DEMONSTRATION                      ║"
echo "║         Semantic Network Diagnostic Tool (LJPW)               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Change to project root
cd "$(dirname "$0")/.." || exit

echo "📋 Demo Overview:"
echo "  1. Basic ping analysis"
echo "  2. Semantic operation analysis"
echo "  3. ICE harmony analysis"
echo "  4. Port scanning (localhost)"
echo ""
read -p "Press Enter to start demo..."

# Demo 1: Ping Analysis
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "DEMO 1: Semantic Ping Analysis"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Testing connectivity to Google DNS (8.8.8.8)..."
echo "This operation will be mapped to LJPW semantic space."
echo ""
read -p "Press Enter to run ping..."
echo ""

./pinpoint.py ping 8.8.8.8 -c 3

read -p "Press Enter to continue to next demo..."

# Demo 2: Semantic Analysis
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "DEMO 2: Semantic Operation Analysis"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Analyzing various network operations in LJPW space:"
echo ""
echo "Operation 1: 'configure firewall rules to block unauthorized access'"
echo ""
read -p "Press Enter to analyze..."

./pinpoint.py analyze "configure firewall rules to block unauthorized access"

echo ""
echo "Operation 2: 'monitor network traffic for performance issues'"
echo ""
read -p "Press Enter to analyze..."

./pinpoint.py analyze "monitor network traffic for performance issues"

echo ""
echo "Operation 3: 'establish VPN tunnel for secure communication'"
echo ""
read -p "Press Enter to analyze..."

./pinpoint.py analyze "establish VPN tunnel for secure communication"

read -p "Press Enter to continue to next demo..."

# Demo 3: ICE Analysis
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "DEMO 3: ICE Framework - Intent-Context-Execution Harmony"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Analyzing harmony between intent, context, and execution..."
echo ""
echo "Scenario: Database connection in restricted network"
echo "  Intent:    'establish secure fast database connection'"
echo "  Context:   'network has firewall with limited bandwidth'"
echo "  Execution: 'open mysql port configure connection pooling'"
echo ""
read -p "Press Enter to analyze harmony..."

./pinpoint.py ice \
  "establish secure fast database connection" \
  "network has firewall with limited bandwidth" \
  "open mysql port configure connection pooling"

read -p "Press Enter to continue to next demo..."

# Demo 4: Port Scan
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "DEMO 4: Semantic Port Scanning"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Scanning localhost for common services..."
echo "Each service will be classified in LJPW semantic space."
echo ""
read -p "Press Enter to scan..."

./pinpoint.py scan 127.0.0.1 -p 22,80,443,3306,5432,8080

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "DEMO COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Additional commands you can try:"
echo ""
echo "  # Traceroute with semantic analysis"
echo "  ./pinpoint.py traceroute google.com"
echo ""
echo "  # Map your local network (requires sudo)"
echo "  sudo ./pinpoint.py map 192.168.1.0/24"
echo ""
echo "  # Analyze custom operations"
echo "  ./pinpoint.py analyze 'your network operation here'"
echo ""
echo "See README.md for more examples and documentation."
echo ""
