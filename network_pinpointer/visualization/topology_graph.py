"""
Network Topology Graph Generator

Generates interactive 3D network topology graphs using Plotly.js.
Visualizes:
- Targets as nodes (colored by dominant dimension)
- Semantic relationships as edges (thickness based on similarity)
- Spatial layout based on LJPW coordinates
"""

import json
import os
import math
from typing import List, Dict, Any

class NetworkTopologyGraphGenerator:
    """Generates interactive network topology graphs"""
    
    def __init__(self):
        self.template = """
<!DOCTYPE html>
<html>
<head>
    <title>Network-Pinpointer Semantic Topology</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body { margin: 0; padding: 0; background-color: #111; overflow: hidden; }
        #chart { width: 100vw; height: 100vh; }
        .controls { position: absolute; top: 20px; left: 20px; z-index: 100; background: rgba(0,0,0,0.7); padding: 15px; border-radius: 8px; color: #eee; font-family: sans-serif; }
    </style>
</head>
<body>
    <div class="controls">
        <h3>Semantic Topology</h3>
        <p>Nodes: Targets</p>
        <p>Edges: Semantic Similarity</p>
        <p>Position: LJPW Space (L, J, P)</p>
    </div>
    <div id="chart"></div>

    <script>
        const data = %DATA%;
        
        // Nodes
        const nodeX = data.nodes.map(n => n.x);
        const nodeY = data.nodes.map(n => n.y);
        const nodeZ = data.nodes.map(n => n.z);
        const nodeColor = data.nodes.map(n => n.color);
        const nodeSize = data.nodes.map(n => n.size);
        const nodeText = data.nodes.map(n => n.label);
        
        // Edges
        const edgeX = [];
        const edgeY = [];
        const edgeZ = [];
        
        data.edges.forEach(edge => {
            const source = data.nodes[edge.source];
            const target = data.nodes[edge.target];
            
            edgeX.push(source.x, target.x, null);
            edgeY.push(source.y, target.y, null);
            edgeZ.push(source.z, target.z, null);
        });

        const traceNodes = {
            x: nodeX,
            y: nodeY,
            z: nodeZ,
            mode: 'markers+text',
            type: 'scatter3d',
            text: nodeText,
            textposition: 'top center',
            marker: {
                size: nodeSize,
                color: nodeColor,
                opacity: 0.8,
                line: { color: '#fff', width: 1 }
            },
            hoverinfo: 'text'
        };
        
        const traceEdges = {
            x: edgeX,
            y: edgeY,
            z: edgeZ,
            mode: 'lines',
            type: 'scatter3d',
            line: {
                color: '#888',
                width: 2,
                opacity: 0.3
            },
            hoverinfo: 'none'
        };
        
        const layout = {
            margin: {l: 0, r: 0, b: 0, t: 0},
            paper_bgcolor: '#111',
            scene: {
                xaxis: { title: 'Love', range: [0, 1], backgroundcolor: '#111', gridcolor: '#333' },
                yaxis: { title: 'Justice', range: [0, 1], backgroundcolor: '#111', gridcolor: '#333' },
                zaxis: { title: 'Power', range: [0, 1], backgroundcolor: '#111', gridcolor: '#333' },
                camera: {
                    eye: {x: 1.5, y: 1.5, z: 1.5}
                }
            },
            showlegend: false
        };
        
        Plotly.newPlot('chart', [traceEdges, traceNodes], layout);
    </script>
</body>
</html>
"""

    def generate_graph(self, profiles: List[Any], output_file: str = "topology.html"):
        """
        Generate HTML topology graph from profiles.
        
        Args:
            profiles: List of semantic profiles
            output_file: Path to output HTML file
        """
        nodes = []
        edges = []
        
        # 1. Create Nodes
        for i, p in enumerate(profiles):
            if isinstance(p, dict):
                target = p.get('target', 'Unknown')
                l = p.get('love', 0.0)
                j = p.get('justice', 0.0)
                pow_val = p.get('power', 0.0)
                mass = p.get('semantic_mass', 0.0)
                dom = p.get('dominant_dimension', 'Unknown')
            else:
                target = p.target
                if p.ljpw_coordinates:
                    l = p.ljpw_coordinates.love
                    j = p.ljpw_coordinates.justice
                    pow_val = p.ljpw_coordinates.power
                else:
                    l, j, pow_val = 0.0, 0.0, 0.0
                mass = getattr(p, 'semantic_mass', 0.0)
                dom = p.dominant_dimension

            # Color based on dominant dimension
            color_map = {
                'Love': '#ff0055',
                'Justice': '#00ccff',
                'Power': '#ffaa00',
                'Wisdom': '#aa00ff'
            }
            color = color_map.get(dom, '#888888')
            
            # Size based on mass (log scale)
            size = 10 + (math.log(mass + 1) * 5)
            
            nodes.append({
                'id': i,
                'label': target,
                'x': l,
                'y': j,
                'z': pow_val,
                'color': color,
                'size': size
            })
            
        # 2. Create Edges (based on semantic similarity)
        # Connect every node to every other node if similarity > threshold
        threshold = 0.8 # Only connect very similar nodes
        
        for i in range(len(nodes)):
            for k in range(i + 1, len(nodes)):
                n1 = nodes[i]
                n2 = nodes[k]
                
                # Euclidean distance in LJPW space
                dist = math.sqrt(
                    (n1['x'] - n2['x'])**2 + 
                    (n1['y'] - n2['y'])**2 + 
                    (n1['z'] - n2['z'])**2
                )
                
                # Similarity is inverse of distance
                # Max distance is sqrt(3) approx 1.73
                similarity = 1.0 - (dist / 1.732)
                
                if similarity > threshold:
                    edges.append({
                        'source': i,
                        'target': k,
                        'weight': similarity
                    })
        
        graph_data = {
            'nodes': nodes,
            'edges': edges
        }
            
        html_content = self.template.replace('%DATA%', json.dumps(graph_data))
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return os.path.abspath(output_file)
