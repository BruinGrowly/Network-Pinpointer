"""
Drift Timeline Generator

Generates interactive timelines of semantic drift using Plotly.js.
Visualizes:
- LJPW Coordinates over time
- Semantic Mass over time
- Harmony Score over time
"""

import json
import os
from typing import List, Dict, Any
from datetime import datetime

class DriftTimelineGenerator:
    """Generates interactive drift timelines"""
    
    def __init__(self):
        self.template = """
<!DOCTYPE html>
<html>
<head>
    <title>Network-Pinpointer Drift Timeline: %TARGET%</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body { margin: 0; padding: 20px; background-color: #111; color: #eee; font-family: sans-serif; }
        .chart-container { width: 100%; height: 400px; margin-bottom: 40px; }
        h1 { text-align: center; color: #4facfe; }
        .subtitle { text-align: center; color: #888; margin-bottom: 30px; }
    </style>
</head>
<body>
    <h1>Semantic Drift Timeline</h1>
    <div class="subtitle">Target: %TARGET%</div>
    
    <div id="ljpw-chart" class="chart-container"></div>
    <div id="mass-chart" class="chart-container"></div>
    <div id="harmony-chart" class="chart-container"></div>

    <script>
        const data = %DATA%;
        const timestamps = data.map(d => d.timestamp);
        
        // 1. LJPW Coordinates
        const traceL = {
            x: timestamps,
            y: data.map(d => d.love),
            name: 'Love',
            type: 'scatter',
            line: {color: '#ff0055'}
        };
        const traceJ = {
            x: timestamps,
            y: data.map(d => d.justice),
            name: 'Justice',
            type: 'scatter',
            line: {color: '#00ccff'}
        };
        const traceP = {
            x: timestamps,
            y: data.map(d => d.power),
            name: 'Power',
            type: 'scatter',
            line: {color: '#ffaa00'}
        };
        const traceW = {
            x: timestamps,
            y: data.map(d => d.wisdom),
            name: 'Wisdom',
            type: 'scatter',
            line: {color: '#aa00ff'}
        };
        
        const layout1 = {
            title: 'LJPW Dimensions Over Time',
            paper_bgcolor: '#111',
            plot_bgcolor: '#111',
            font: { color: '#eee' },
            xaxis: { title: 'Time' },
            yaxis: { title: 'Score', range: [0, 1] }
        };
        
        Plotly.newPlot('ljpw-chart', [traceL, traceJ, traceP, traceW], layout1);
        
        // 2. Semantic Mass
        const traceMass = {
            x: timestamps,
            y: data.map(d => d.mass),
            name: 'Mass',
            type: 'scatter',
            fill: 'tozeroy',
            line: {color: '#00f260'}
        };
        
        const layout2 = {
            title: 'Semantic Mass Over Time',
            paper_bgcolor: '#111',
            plot_bgcolor: '#111',
            font: { color: '#eee' },
            xaxis: { title: 'Time' },
            yaxis: { title: 'Mass' }
        };
        
        Plotly.newPlot('mass-chart', [traceMass], layout2);
        
        // 3. Harmony Score
        const traceHarmony = {
            x: timestamps,
            y: data.map(d => d.harmony),
            name: 'Harmony',
            type: 'scatter',
            line: {color: '#ffffff', dash: 'dot'}
        };
        
        const layout3 = {
            title: 'Harmony Score Over Time',
            paper_bgcolor: '#111',
            plot_bgcolor: '#111',
            font: { color: '#eee' },
            xaxis: { title: 'Time' },
            yaxis: { title: 'Score', range: [0, 1] }
        };
        
        Plotly.newPlot('harmony-chart', [traceHarmony], layout3);
        
    </script>
</body>
</html>
"""

    def generate_timeline(self, target: str, profiles: List[Any], output_file: str = None):
        """
        Generate HTML drift timeline from profile history.
        
        Args:
            target: Target hostname/IP
            profiles: List of semantic profiles (objects or dicts) sorted by time
            output_file: Path to output HTML file (optional)
        """
        if not output_file:
            output_file = f"drift_timeline_{target.replace('.', '_')}.html"
            
        data = []
        for p in profiles:
            if isinstance(p, dict):
                ts = p.get('timestamp', '')
                l = p.get('love', 0.0)
                j = p.get('justice', 0.0)
                pow_val = p.get('power', 0.0)
                w = p.get('wisdom', 0.0)
                mass = p.get('semantic_mass', 0.0)
                harmony = p.get('harmony_score', 0.0)
            else:
                ts = p.timestamp.isoformat()
                if p.ljpw_coordinates:
                    l = p.ljpw_coordinates.love
                    j = p.ljpw_coordinates.justice
                    pow_val = p.ljpw_coordinates.power
                    w = p.ljpw_coordinates.wisdom
                else:
                    l, j, pow_val, w = 0.0, 0.0, 0.0, 0.0
                mass = getattr(p, 'semantic_mass', 0.0)
                harmony = p.harmony_score

            data.append({
                'timestamp': ts,
                'love': l,
                'justice': j,
                'power': pow_val,
                'wisdom': w,
                'mass': mass,
                'harmony': harmony
            })
            
        # Sort by timestamp just in case
        data.sort(key=lambda x: x['timestamp'])
            
        html_content = self.template.replace('%DATA%', json.dumps(data))
        html_content = html_content.replace('%TARGET%', target)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return os.path.abspath(output_file)
