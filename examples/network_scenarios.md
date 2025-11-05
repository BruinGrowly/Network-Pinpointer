# Network-Pinpointer Example Scenarios

Real-world examples of using Network-Pinpointer for semantic network analysis.

## Scenario 1: Diagnosing Slow Web Application

### Problem
Web application is slow, and you need to identify the bottleneck.

### Analysis Approach

```bash
# Step 1: Analyze the intent
./pinpoint.py analyze "provide fast web service to users"

# Output will show high Power (performance) and Love (service) dimensions

# Step 2: Check current network state
./pinpoint.py ping webserver.example.com

# Step 3: Trace the route
./pinpoint.py traceroute webserver.example.com

# Step 4: Scan the web server
./pinpoint.py scan webserver.example.com -p 80,443,8080,3306

# Step 5: ICE Analysis
./pinpoint.py ice \
  "deliver fast responsive web pages" \
  "high latency network many intermediate hops" \
  "serve static html no caching"
```

### Interpretation
- If ICE coherence is low: execution doesn't match intent (e.g., no caching when speed is needed)
- If Power dimension is weak in execution: lacking performance optimization
- If Wisdom dimension is low: insufficient monitoring to diagnose issues

## Scenario 2: Security Audit

### Problem
Need to audit network for security vulnerabilities.

### Analysis Approach

```bash
# Step 1: Map the network
./pinpoint.py map 192.168.1.0/24 --export-json security_audit.json

# Look for:
# - Devices with excessive open ports
# - Insecure services (Telnet, FTP)
# - Devices with unclear purpose
# - Low Justice dimension in security-critical zones

# Step 2: Analyze firewall configuration intent
./pinpoint.py analyze "block all unauthorized access enforce security policy"

# Should show high Justice dimension

# Step 3: Check if execution matches intent
./pinpoint.py ice \
  "block unauthorized access allow only necessary services" \
  "DMZ with public facing servers" \
  "firewall allows all outbound many inbound ports open"

# Low ICE coherence = security policy not properly enforced
```

### Red Flags
- **Critical**: Devices exposing ports 21, 23, 445 (insecure protocols)
- **High**: Justice dimension < 30% for firewall/gateway devices
- **Medium**: Devices with no clear dominant dimension (unclear purpose)

## Scenario 3: Planning New Infrastructure

### Problem
Designing a new microservices architecture. Want to ensure semantic coherence.

### Analysis Approach

```bash
# Define each component's intended purpose

# API Gateway
./pinpoint.py analyze "route requests authenticate validate distribute load"
# Expected: High Love (routing/distribution) + Justice (authentication)

# Authentication Service
./pinpoint.py analyze "verify credentials enforce access control validate tokens"
# Expected: High Justice (policy enforcement)

# Application Server
./pinpoint.py analyze "process requests execute business logic compute results"
# Expected: High Power (execution)

# Monitoring System
./pinpoint.py analyze "collect metrics monitor health track performance"
# Expected: High Wisdom (information gathering)

# Check overall architecture harmony
./pinpoint.py ice \
  "scalable secure reliable microservice platform" \
  "cloud environment with load balancers and autoscaling" \
  "containerized services with API gateway monitoring"
```

### Design Principles
- **Separation of Concerns**: Each component should have clear dominant dimension
- **Balance**: Overall architecture should utilize all four dimensions appropriately
- **Harmony**: ICE analysis should show >70% coherence

### Expected LJPW Distribution

| Component | Love | Justice | Power | Wisdom | Purpose |
|-----------|------|---------|-------|--------|---------|
| API Gateway | 40% | 30% | 20% | 10% | Routing + Auth |
| Auth Service | 10% | 70% | 15% | 5% | Security |
| App Server | 15% | 10% | 65% | 10% | Processing |
| Database | 10% | 20% | 60% | 10% | Storage/Power |
| Cache | 20% | 5% | 65% | 10% | Performance |
| Monitoring | 10% | 10% | 5% | 75% | Observability |
| Load Balancer | 50% | 15% | 30% | 5% | Distribution |

## Scenario 4: Troubleshooting Connectivity

### Problem
Some clients can't reach a service intermittently.

### Analysis Approach

```bash
# Step 1: Test connectivity from multiple points
./pinpoint.py ping target.example.com
./pinpoint.py ping target.example.com  # Run multiple times

# Step 2: Trace the route
./pinpoint.py traceroute target.example.com

# Look for:
# - High latency hops (> 100ms)
# - Route changes between attempts
# - Packet loss

# Step 3: Analyze the connection semantically
./pinpoint.py analyze "establish reliable connection to service"
# Should show high Love (connectivity)

# Step 4: Check if network supports this
./pinpoint.py ice \
  "provide reliable consistent connectivity" \
  "multiple network paths unstable routing" \
  "single path no redundancy"

# Low ICE balance = context doesn't support intent
```

### Diagnostic Indicators
- **High packet loss** + **Low Love dimension** = Connectivity infrastructure issue
- **High latency** + **Low Power dimension** = Performance/bandwidth problem
- **Low ICE coherence** = Network configuration doesn't match needs

## Scenario 5: Capacity Planning

### Problem
Need to add capacity. Where should resources be allocated?

### Analysis Approach

```bash
# Step 1: Map current infrastructure
./pinpoint.py map 10.0.0.0/16 --export-json current_topology.json

# Analyze the JSON to find:
# - Which clusters are largest (may be overloaded)
# - Which dimensions are underrepresented
# - Cohesion scores (low = unclear purpose)

# Step 2: Define growth goals
./pinpoint.py analyze "scale to handle 10x traffic maintain performance"

# Should show high Power dimension need

# Step 3: Check what you're adding
./pinpoint.py analyze "add more application servers increase database capacity"

# Step 4: Verify this matches needs
./pinpoint.py ice \
  "scale to handle 10x traffic" \
  "current bottleneck is database queries" \
  "add more web servers"

# Low coherence = you're adding wrong type of capacity!
```

### Decision Framework
1. Identify which dimension is bottleneck:
   - **Love bottleneck**: Need better networking/load balancing
   - **Justice bottleneck**: Security/validation is slowing things down
   - **Power bottleneck**: Need more compute/processing capacity
   - **Wisdom bottleneck**: Lack of monitoring/observability

2. Add capacity that strengthens that dimension

3. Verify with ICE analysis that addition makes sense

## Scenario 6: Merger Network Integration

### Problem
Merging two company networks. Need to understand both semantically.

### Analysis Approach

```bash
# Step 1: Map both networks
./pinpoint.py map 192.168.1.0/24 --export-json network_a.json
./pinpoint.py map 10.0.0.0/16 --export-json network_b.json

# Compare the JSONs:
# - What clusters exist in each?
# - Are purposes complementary or overlapping?
# - Are there semantic conflicts?

# Step 2: Define integration goal
./pinpoint.py analyze "merge networks maintain security enable communication"

# Should show balance of Love (communication) and Justice (security)

# Step 3: Analyze integration approach
./pinpoint.py ice \
  "merge networks enable cross-company communication maintain isolation" \
  "two separate networks different security policies" \
  "connect via VPN bridge firewalls"

# Check coherence - does the approach match the goal?
```

### Integration Patterns

**Pattern 1: Full Integration**
- High Love dimension (full connectivity)
- Medium Justice (unified security policy)
- Use when: Companies fully merging, shared infrastructure

**Pattern 2: Controlled Bridge**
- Medium Love (selective connectivity)
- High Justice (strict access control)
- Use when: Partnership, need isolation but some sharing

**Pattern 3: Isolated with Services**
- Low Love (minimal connectivity)
- High Justice (strong boundaries)
- High Wisdom (monitoring all cross-network traffic)
- Use when: Acquisition, keeping networks separate long-term

## Tips for Semantic Network Analysis

### 1. Consistency is Key
- Similar devices should have similar LJPW coordinates
- Large coordinate variations in same cluster = configuration drift

### 2. Watch for Dimension Imbalance
- A network with only Power and Wisdom lacks connectivity (Love) and security (Justice)
- All-Love network lacks control and monitoring
- Strive for appropriate balance

### 3. Use ICE for Validation
- Before major changes, run ICE analysis
- Low harmony = rethink your approach
- High harmony = proceed confidently

### 4. Track Over Time
- Export topology regularly
- Watch for semantic drift
- Sudden coordinate changes = configuration changes (intentional or not)

### 5. Document in LJPW Terms
- Describe systems by their dominant dimension
- E.g., "Justice-dominant security cluster" is clearer than "firewall zone"
- Helps new team members understand purpose quickly

## Advanced: Creating Custom Vocabularies

For your specific environment, create a config.json:

```json
{
  "custom_vocabulary": {
    "myapp": "power",
    "myapp_monitor": "wisdom",
    "myapp_gateway": "love",
    "myapp_auth": "justice"
  }
}
```

Then your internal services will be correctly classified in semantic space.
