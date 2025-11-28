"""
Interactive Dashboard Generator

Generates a unified interactive dashboard combining multiple visualizations.
Includes:
- Global Metrics
- Cluster Map (3D)
- Mass Distribution
- Top Targets Table
"""

import json
import os
from typing import List, Dict, Any

class DashboardGenerator:
    """Generates interactive dashboard"""
    
    def __init__(self):
        self.template = """
<!DOCTYPE html>
<html>
<head>
    <title>Network-Pinpointer Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body { margin: 0; padding: 20px; background-color: #111; color: #eee; font-family: 'Segoe UI', sans-serif; }
        .header { text-align: center; margin-bottom: 40px; }
        h1 { color: #4facfe; margin: 0; }
        .subtitle { color: #888; }
        
        .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
        .card { background: #222; border-radius: 8px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .full-width { grid-column: span 2; }
        
        .stats-row { display: flex; justify-content: space-around; margin-bottom: 20px; }
        .stat-box { text-align: center; }
        .stat-val { font-size: 28px; font-weight: bold; color: #00f260; }
        .stat-label { font-size: 14px; color: #aaa; }
        
        h2 { color: #ddd; font-size: 18px; margin-top: 0; border-bottom: 1px solid #333; padding-bottom: 10px; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { text-align: left; padding: 10px; border-bottom: 1px solid #333; }
        th { color: #888; font-weight: normal; }
        tr:hover { background: #2a2a2a; }
        .tag { padding: 2px 6px; border-radius: 4px; font-size: 12px; }
        .tag-high { background: #ff0055; color: white; }
        .tag-med { background: #ffaa00; color: black; }
        .tag-low { background: #00f260; color: black; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Network Semantic Dashboard</h1>
        <div class="subtitle">Real-time Semantic Intelligence Overview</div>
    </div>
    
    <div class="grid">
        <!-- Global Stats -->
        <div class="card full-width">
            <div class="stats-row">
                <div class="stat-box">
                    <div class="stat-val" id="total-targets">0</div>
                    <div class="stat-label">Total Targets</div>
                </div>
                <div class="stat-box">
                    <div class="stat-val" id="avg-harmony">0%</div>
                    <div class="stat-label">Avg Harmony</div>
                </div>
                <div class="stat-box">
                    <div class="stat-val" id="total-mass">0</div>
                    <div class="stat-label">Total Semantic Mass</div>
                </div>
                <div class="stat-box">
                    <div class="stat-val" id="risk-score">Low</div>
                    <div class="stat-label">Overall Risk</div>
                </div>
            </div>
        </div>
        
        <!-- Cluster Map -->
        <div class="card">
            <h2>Semantic Clusters (LJPW)</h2>
            <div id="cluster-map" style="height: 400px;"></div>
        </div>
        
        <!-- Mass Distribution -->
        <div class="card">
            <h2>Mass Distribution</h2>
            <div id="mass-dist" style="height: 400px;"></div>
        </div>
        
        <!-- Top Targets -->
        <div class="card full-width">
            <h2>Top Targets by Semantic Mass</h2>
            <table id="targets-table">
                <thead>
                    <tr>
                        <th>Target</th>
                        <th>Mass</th>
                        <th>Dominant Dimension</th>
                        <th>Harmony</th>
                        <th>Security Posture</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
    </div>

    <script>
        const data = %DATA%;
        
        // 1. Populate Stats
        document.getElementById('total-targets').textContent = data.length;
        
        const avgHarmony = data.reduce((a, b) => a + b.harmony, 0) / data.length || 0;
        document.getElementById('avg-harmony').textContent = (avgHarmony * 100).toFixed(0) + '%';
        
        const totalMass = data.reduce((a, b) => a + b.mass, 0);
        document.getElementById('total-mass').textContent = totalMass.toFixed(1);
        
        // 2. Cluster Map
        const traceCluster = {
            x: data.map(d => d.l),
            y: data.map(d => d.j),
            z: data.map(d => d.p),
            mode: 'markers',
            type: 'scatter3d',
            text: data.map(d => d.target),
            marker: {
                size: data.map(d => 5 + Math.log(d.mass + 1) * 5),
                color: data.map(d => d.w),
                colorscale: 'Viridis',
                opacity: 0.8
            }
        };
        
        const layoutCluster = {
            margin: {l: 0, r: 0, b: 0, t: 0},
            paper_bgcolor: '#222',
            scene: {
                xaxis: { title: 'Love' },
                yaxis: { title: 'Justice' },
                zaxis: { title: 'Power' }
            }
        };
        
        Plotly.newPlot('cluster-map', [traceCluster], layoutCluster);
        
        // 3. Mass Distribution
        const traceMass = {
            x: data.map(d => d.mass),
            type: 'histogram',
            marker: { color: '#4facfe' }
        };
        
        const layoutMass = {
            margin: {l: 40, r: 20, b: 40, t: 20},
            paper_bgcolor: '#222',
            plot_bgcolor: '#222',
            font: { color: '#eee' },
            xaxis: { title: 'Mass' },
            yaxis: { title: 'Count' }
        };
        
        Plotly.newPlot('mass-dist', [traceMass], layoutMass);
        
        // 4. Top Targets Table
        const sortedData = [...data].sort((a, b) => b.mass - a.mass).slice(0, 10);
        const tbody = document.querySelector('#targets-table tbody');
        
        sortedData.forEach(d => {
            const tr = document.createElement('tr');
            
            let postureClass = 'tag-low';
            if (d.posture.includes('VULNERABLE')) postureClass = 'tag-high';
            else if (d.posture.includes('MODERATE')) postureClass = 'tag-med';
            
            tr.innerHTML = `
                <td>${d.target}</td>
                <td>${d.mass.toFixed(1)}</td>
                <td>${d.dominant}</td>
                <td>${(d.harmony * 100).toFixed(0)}%</td>
                <td><span class="tag ${postureClass}">${d.posture}</span></td>
            `;
            tbody.appendChild(tr);
        });
    </script>
</body>
</html>
"""

    def generate_dashboard(self, profiles: List[Any], output_file: str = "dashboard.html"):
        """
        Generate HTML dashboard from profiles.
        
        Args:
            profiles: List of semantic profiles
            output_file: Path to output HTML file
        """
        data = []
        for p in profiles:
            if isinstance(p, dict):
                target = p.get('target', 'Unknown')
                l = p.get('love', 0.0)
                j = p.get('justice', 0.0)
                pow_val = p.get('power', 0.0)
                w = p.get('wisdom', 0.0)
                mass = p.get('semantic_mass', 0.0)
                harmony = p.get('harmony_score', 0.0)
                dom = p.get('dominant_dimension', 'Unknown')
                posture = p.get('security_posture', 'UNKNOWN')
            else:
                target = p.target
                if p.ljpw_coordinates:
                    l = p.ljpw_coordinates.love
                    j = p.ljpw_coordinates.justice
                    pow_val = p.ljpw_coordinates.power
                    w = p.ljpw_coordinates.wisdom
                else:
                    l, j, pow_val, w = 0.0, 0.0, 0.0, 0.0
                mass = getattr(p, 'semantic_mass', 0.0)
                harmony = p.harmony_score
                dom = p.dominant_dimension
                posture = p.security_posture

            data.append({
                'target': target,
                'l': l,
                'j': j,
                'p': pow_val,
                'w': w,
                'mass': mass,
                'harmony': harmony,
                'dominant': dom,
                'posture': posture
            })
            
        html_content = self.template.replace('%DATA%', json.dumps(data))
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return os.path.abspath(output_file)
