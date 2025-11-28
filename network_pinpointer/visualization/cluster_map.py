"""
Cluster Map Generator

Generates interactive 3D visualizations of semantic clusters using Plotly.js.
Maps LJPW dimensions to visual properties:
- X Axis: Love (Connectivity)
- Y Axis: Justice (Security)
- Z Axis: Power (Performance)
- Color: Wisdom (Insight)
- Size: Semantic Mass
"""

import json
import os
from typing import List, Dict, Any
from ..semantic_probe import SemanticProfile

class ClusterMapGenerator:
    """Generates interactive cluster maps"""
    
    def __init__(self):
        self.template = """
<!DOCTYPE html>
<html>
<head>
    <title>Network-Pinpointer Semantic Clusters</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body { margin: 0; padding: 0; background-color: #111; color: #eee; font-family: sans-serif; }
        #plot { width: 100vw; height: 100vh; }
        .info-panel {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.8);
            padding: 20px;
            border-radius: 8px;
            pointer-events: none;
            z-index: 100;
        }
    </style>
</head>
<body>
    <div class="info-panel">
        <h2>Semantic Universe</h2>
        <p><strong>X:</strong> Love (Connectivity)</p>
        <p><strong>Y:</strong> Justice (Security)</p>
        <p><strong>Z:</strong> Power (Performance)</p>
        <p><strong>Color:</strong> Wisdom (Insight)</p>
        <p><strong>Size:</strong> Semantic Mass</p>
    </div>
    <div id="plot"></div>
    <script>
        const data = %DATA%;
        
        const trace = {
            x: data.map(d => d.l),
            y: data.map(d => d.j),
            z: data.map(d => d.p),
            mode: 'markers',
            marker: {
                size: data.map(d => Math.max(5, Math.min(50, d.mass * 2))),
                color: data.map(d => d.w),
                colorscale: 'Viridis',
                opacity: 0.8,
                showscale: true,
                colorbar: {title: 'Wisdom'}
            },
            text: data.map(d => `
                <b>${d.target}</b><br>
                Mass: ${d.mass.toFixed(1)}<br>
                L: ${d.l.toFixed(2)}<br>
                J: ${d.j.toFixed(2)}<br>
                P: ${d.p.toFixed(2)}<br>
                W: ${d.w.toFixed(2)}<br>
                <i>${d.desc}</i>
            `),
            hoverinfo: 'text',
            type: 'scatter3d'
        };

        const layout = {
            margin: {l: 0, r: 0, b: 0, t: 0},
            paper_bgcolor: '#111',
            scene: {
                xaxis: {title: 'Love', range: [0, 1], gridcolor: '#333', zerolinecolor: '#555'},
                yaxis: {title: 'Justice', range: [0, 1], gridcolor: '#333', zerolinecolor: '#555'},
                zaxis: {title: 'Power', range: [0, 1], gridcolor: '#333', zerolinecolor: '#555'},
                camera: {
                    eye: {x: 1.5, y: 1.5, z: 1.5}
                }
            }
        };

        Plotly.newPlot('plot', [trace], layout);
    </script>
</body>
</html>
"""

    def generate_map(self, profiles: List[Any], output_file: str = "clusters.html"):
        """
        Generate HTML cluster map from profiles.
        
        Args:
            profiles: List of semantic profiles (objects or dicts) to visualize
            output_file: Path to output HTML file
        """
        data = []
        for p in profiles:
            # Handle both object and dictionary access
            if isinstance(p, dict):
                target = p.get('target', 'Unknown')
                mass = p.get('semantic_mass', 0.0)
                desc = p.get('inferred_purpose', '')
                
                # Handle coordinates in dict
                # It might be flat or nested depending on how it was stored/retrieved
                # Based on semantic_storage.py, it's stored as flat columns
                l = p.get('love', 0.0)
                j = p.get('justice', 0.0)
                p_val = p.get('power', 0.0) # 'p' is already used for loop var
                w = p.get('wisdom', 0.0)
            else:
                target = p.target
                mass = getattr(p, 'semantic_mass', 0.0)
                desc = p.inferred_purpose
                
                if p.ljpw_coordinates:
                    l = p.ljpw_coordinates.love
                    j = p.ljpw_coordinates.justice
                    p_val = p.ljpw_coordinates.power
                    w = p.ljpw_coordinates.wisdom
                else:
                    l, j, p_val, w = 0.0, 0.0, 0.0, 0.0

            data.append({
                'target': target,
                'l': l,
                'j': j,
                'p': p_val,
                'w': w,
                'mass': mass,
                'desc': desc
            })
            
        html_content = self.template.replace('%DATA%', json.dumps(data))
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return os.path.abspath(output_file)
