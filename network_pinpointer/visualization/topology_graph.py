"""
Network Topology Graph Generator

Generates interactive 3D network topology graphs using Plotly.js.
Visualizes:
- Targets as nodes (colored by dominant dimension)
- Semantic relationships as edges (thickness based on similarity)
- Spatial layout based on LJPW coordinates
- Path finding and network analysis
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
        :root {
            --bg-primary: #111;
            --bg-secondary: #1a1a1a;
            --bg-card: #222;
            --text-primary: #eee;
            --text-secondary: #aaa;
            --accent: #4facfe;
            --accent-hover: #00b4ff;
            --border: #333;
            --success: #00ff88;
            --warning: #ffaa00;
            --error: #ff0055;
            --love: #ff0055;
            --justice: #00ccff;
            --power: #ffaa00;
            --wisdom: #aa00ff;
        }

        .light-theme {
            --bg-primary: #fff;
            --bg-secondary: #f9f9f9;
            --bg-card: #f5f5f5;
            --text-primary: #222;
            --text-secondary: #666;
            --accent: #0575E6;
            --accent-hover: #0056b3;
            --border: #ddd;
            --success: #00aa55;
            --warning: #ff8800;
            --error: #cc0044;
            --love: #e6004d;
            --justice: #00b4e6;
            --power: #e68a00;
            --wisdom: #9900e6;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            overflow: hidden;
            transition: background-color 0.3s, color 0.3s;
        }

        #chart {
            width: 100vw;
            height: 100vh;
        }

        .control-panel {
            position: absolute;
            top: 20px;
            left: 20px;
            max-width: 380px;
            max-height: calc(100vh - 40px);
            overflow-y: auto;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            z-index: 100;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: all 0.3s;
        }

        .control-panel.hidden {
            transform: translateX(-420px);
        }

        .control-panel h2 {
            font-size: 1.5em;
            margin-bottom: 15px;
            color: var(--accent);
        }

        .section {
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid var(--border);
        }

        .section:last-child {
            border-bottom: none;
        }

        .section h3 {
            font-size: 1.1em;
            margin-bottom: 10px;
            color: var(--text-primary);
        }

        .control-group {
            margin-bottom: 12px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            color: var(--text-secondary);
            font-size: 0.9em;
        }

        input[type="text"],
        input[type="range"],
        select {
            width: 100%;
            padding: 8px;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text-primary);
            font-size: 0.95em;
        }

        input[type="range"] {
            padding: 0;
        }

        .range-value {
            display: inline-block;
            margin-left: 10px;
            font-weight: bold;
            color: var(--accent);
        }

        button {
            padding: 10px 16px;
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.95em;
            transition: background 0.2s;
            width: 100%;
            margin-bottom: 8px;
        }

        button:hover {
            background: var(--accent-hover);
        }

        button.secondary {
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border);
        }

        button.secondary:hover {
            background: var(--border);
        }

        .stats {
            background: var(--bg-secondary);
            padding: 12px;
            border-radius: 6px;
            font-size: 0.9em;
        }

        .stats p {
            margin: 6px 0;
            display: flex;
            justify-content: space-between;
        }

        .stats .value {
            font-weight: bold;
            color: var(--accent);
        }

        .legend {
            background: var(--bg-secondary);
            padding: 12px;
            border-radius: 6px;
        }

        .legend-item {
            display: flex;
            align-items: center;
            margin: 6px 0;
            font-size: 0.9em;
        }

        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 10px;
            border: 2px solid var(--border);
        }

        .toggle-btn {
            position: absolute;
            top: 20px;
            left: 420px;
            width: 40px;
            height: 40px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 99;
            transition: all 0.3s;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }

        .toggle-btn:hover {
            background: var(--accent);
            transform: scale(1.1);
        }

        .toggle-btn.panel-hidden {
            left: 20px;
        }

        .path-display {
            background: var(--bg-secondary);
            padding: 12px;
            border-radius: 6px;
            max-height: 200px;
            overflow-y: auto;
        }

        .path-step {
            padding: 6px;
            margin: 4px 0;
            background: var(--bg-primary);
            border-radius: 4px;
            font-size: 0.85em;
        }

        .node-select {
            background: var(--bg-secondary);
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 10px;
        }

        .node-select.active {
            background: var(--accent);
            color: white;
        }

        .toast {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--bg-card);
            color: var(--text-primary);
            padding: 12px 24px;
            border-radius: 8px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s;
        }

        .toast.show {
            opacity: 1;
        }

        .shortcuts-help {
            background: var(--bg-secondary);
            padding: 10px;
            border-radius: 6px;
            font-size: 0.85em;
        }

        .shortcuts-help div {
            margin: 4px 0;
        }

        .shortcuts-help kbd {
            background: var(--bg-primary);
            padding: 2px 6px;
            border-radius: 3px;
            border: 1px solid var(--border);
            font-family: monospace;
            margin-right: 8px;
        }

        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent);
        }
    </style>
</head>
<body>
    <div class="toggle-btn" id="toggleBtn" onclick="togglePanel()">☰</div>

    <div class="control-panel" id="controlPanel">
        <h2>🌐 Semantic Topology</h2>

        <!-- Search -->
        <div class="section">
            <h3>🔍 Search</h3>
            <div class="control-group">
                <input type="text" id="search" placeholder="Search nodes..." oninput="applyFilters()">
            </div>
        </div>

        <!-- Filters -->
        <div class="section">
            <h3>🎯 Filters</h3>
            <div class="control-group">
                <label>Dominant Dimension</label>
                <select id="dimension-filter" onchange="applyFilters()">
                    <option value="all">All Dimensions</option>
                    <option value="Love">Love</option>
                    <option value="Justice">Justice</option>
                    <option value="Power">Power</option>
                    <option value="Wisdom">Wisdom</option>
                </select>
            </div>
            <div class="control-group">
                <label>Connection Threshold <span class="range-value" id="threshold-val">0.80</span></label>
                <input type="range" id="threshold" min="0" max="1" step="0.05" value="0.80" oninput="updateThreshold()">
            </div>
            <div class="control-group">
                <label>Min Mass <span class="range-value" id="mass-val">0</span></label>
                <input type="range" id="min-mass" min="0" max="1000" step="10" value="0" oninput="updateMass()">
            </div>
            <button onclick="resetFilters()">Reset Filters</button>
        </div>

        <!-- Layout -->
        <div class="section">
            <h3>📐 Layout</h3>
            <div class="control-group">
                <select id="layout" onchange="changeLayout()">
                    <option value="ljpw">LJPW Space (3D)</option>
                    <option value="force">Force-Directed</option>
                    <option value="circular">Circular</option>
                    <option value="hierarchical">Hierarchical</option>
                </select>
            </div>
        </div>

        <!-- Path Finding -->
        <div class="section">
            <h3>🗺️ Path Finding</h3>
            <div class="node-select" id="source-display">
                Source: <strong id="source-node">Click a node</strong>
            </div>
            <div class="node-select" id="target-display">
                Target: <strong id="target-node">Click a node</strong>
            </div>
            <button onclick="findPath()">Find Shortest Path</button>
            <button class="secondary" onclick="clearPath()">Clear Path</button>
            <div class="path-display" id="path-result" style="display: none; margin-top: 10px;">
                <strong>Path:</strong>
                <div id="path-steps"></div>
            </div>
        </div>

        <!-- Network Metrics -->
        <div class="section">
            <h3>📊 Network Metrics</h3>
            <div class="stats" id="metrics">
                <p><span>Nodes:</span> <span class="value" id="node-count">0</span></p>
                <p><span>Edges:</span> <span class="value" id="edge-count">0</span></p>
                <p><span>Density:</span> <span class="value" id="density">0.00</span></p>
                <p><span>Avg Degree:</span> <span class="value" id="avg-degree">0.00</span></p>
                <p><span>Clustering:</span> <span class="value" id="clustering">0.00</span></p>
            </div>
        </div>

        <!-- Legend -->
        <div class="section">
            <h3>🎨 Legend</h3>
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color" style="background: #ff0055;"></div>
                    <span>Love (Connectivity)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #00ccff;"></div>
                    <span>Justice (Security)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #ffaa00;"></div>
                    <span>Power (Performance)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #aa00ff;"></div>
                    <span>Wisdom (Visibility)</span>
                </div>
            </div>
        </div>

        <!-- Export -->
        <div class="section">
            <h3>💾 Export</h3>
            <button onclick="exportJSON()">Export JSON</button>
            <button onclick="exportCSV()">Export CSV</button>
            <button onclick="exportPNG()">Export PNG</button>
        </div>

        <!-- Keyboard Shortcuts -->
        <div class="section">
            <h3>⌨️ Shortcuts</h3>
            <div class="shortcuts-help">
                <div><kbd>F</kbd> Fullscreen</div>
                <div><kbd>R</kbd> Reset Camera</div>
                <div><kbd>H</kbd> Hide/Show Panel</div>
                <div><kbd>E</kbd> Export JSON</div>
                <div><kbd>T</kbd> Toggle Theme</div>
                <div><kbd>P</kbd> Find Path</div>
            </div>
        </div>

        <!-- Theme -->
        <div class="section">
            <button onclick="toggleTheme()">Toggle Theme</button>
        </div>
    </div>

    <div id="chart"></div>
    <div class="toast" id="toast"></div>

    <script>
        // ===== DATA & STATE =====
        const rawData = %DATA%;
        let allNodes = rawData.nodes;
        let allEdges = rawData.edges;
        let filteredNodes = [...allNodes];
        let filteredEdges = [...allEdges];
        let adjacencyList = {};
        let pathHighlight = null;
        let sourceNode = null;
        let targetNode = null;
        let currentLayout = 'ljpw';

        // ===== INITIALIZATION =====
        buildAdjacencyList();
        applyFilters();
        loadConfig();

        // ===== ADJACENCY LIST =====
        function buildAdjacencyList() {
            adjacencyList = {};
            allNodes.forEach(n => adjacencyList[n.id] = []);

            filteredEdges.forEach(e => {
                adjacencyList[e.source].push({node: e.target, weight: e.weight});
                adjacencyList[e.target].push({node: e.source, weight: e.weight});
            });
        }

        // ===== FILTERS =====
        function applyFilters() {
            const search = document.getElementById('search').value.toLowerCase();
            const dimension = document.getElementById('dimension-filter').value;
            const threshold = parseFloat(document.getElementById('threshold').value);
            const minMass = parseFloat(document.getElementById('min-mass').value);

            // Filter nodes
            filteredNodes = allNodes.filter(n => {
                if (search && !n.label.toLowerCase().includes(search)) return false;
                if (dimension !== 'all' && n.dimension !== dimension) return false;
                if (n.mass < minMass) return false;
                return true;
            });

            const nodeIds = new Set(filteredNodes.map(n => n.id));

            // Filter edges
            filteredEdges = allEdges.filter(e => {
                if (!nodeIds.has(e.source) || !nodeIds.has(e.target)) return false;
                if (e.weight < threshold) return false;
                return true;
            });

            buildAdjacencyList();
            updatePlot();
            updateMetrics();
            saveConfig();
        }

        function resetFilters() {
            document.getElementById('search').value = '';
            document.getElementById('dimension-filter').value = 'all';
            document.getElementById('threshold').value = '0.80';
            document.getElementById('min-mass').value = '0';
            document.getElementById('threshold-val').textContent = '0.80';
            document.getElementById('mass-val').textContent = '0';
            applyFilters();
            showToast('Filters reset');
        }

        function updateThreshold() {
            const val = document.getElementById('threshold').value;
            document.getElementById('threshold-val').textContent = parseFloat(val).toFixed(2);
            applyFilters();
        }

        function updateMass() {
            const val = document.getElementById('min-mass').value;
            document.getElementById('mass-val').textContent = val;
            applyFilters();
        }

        // ===== LAYOUT ALGORITHMS =====
        function changeLayout() {
            currentLayout = document.getElementById('layout').value;
            updatePlot();
            showToast('Layout changed to ' + currentLayout);
        }

        function calculateLayout(nodes) {
            if (currentLayout === 'ljpw') {
                return nodes.map(n => ({
                    x: n.x,
                    y: n.y,
                    z: n.z
                }));
            } else if (currentLayout === 'force') {
                return forceDirectedLayout(nodes);
            } else if (currentLayout === 'circular') {
                return circularLayout(nodes);
            } else if (currentLayout === 'hierarchical') {
                return hierarchicalLayout(nodes);
            }
        }

        function forceDirectedLayout(nodes) {
            // Simple force-directed simulation
            const positions = nodes.map((n, i) => ({
                x: Math.random(),
                y: Math.random(),
                z: Math.random(),
                vx: 0, vy: 0, vz: 0
            }));

            const iterations = 100;
            const k = 0.1; // Spring constant
            const repulsion = 0.01;

            for (let iter = 0; iter < iterations; iter++) {
                // Repulsion between all nodes
                for (let i = 0; i < positions.length; i++) {
                    for (let j = i + 1; j < positions.length; j++) {
                        const dx = positions[j].x - positions[i].x;
                        const dy = positions[j].y - positions[i].y;
                        const dz = positions[j].z - positions[i].z;
                        const dist = Math.sqrt(dx*dx + dy*dy + dz*dz) + 0.001;
                        const force = repulsion / (dist * dist);

                        positions[i].vx -= force * dx / dist;
                        positions[i].vy -= force * dy / dist;
                        positions[i].vz -= force * dz / dist;
                        positions[j].vx += force * dx / dist;
                        positions[j].vy += force * dy / dist;
                        positions[j].vz += force * dz / dist;
                    }
                }

                // Attraction along edges
                filteredEdges.forEach(e => {
                    const i = nodes.findIndex(n => n.id === e.source);
                    const j = nodes.findIndex(n => n.id === e.target);
                    if (i === -1 || j === -1) return;

                    const dx = positions[j].x - positions[i].x;
                    const dy = positions[j].y - positions[i].y;
                    const dz = positions[j].z - positions[i].z;
                    const force = k * e.weight;

                    positions[i].vx += force * dx;
                    positions[i].vy += force * dy;
                    positions[i].vz += force * dz;
                    positions[j].vx -= force * dx;
                    positions[j].vy -= force * dy;
                    positions[j].vz -= force * dz;
                });

                // Update positions with damping
                positions.forEach(p => {
                    p.x += p.vx * 0.1;
                    p.y += p.vy * 0.1;
                    p.z += p.vz * 0.1;
                    p.vx *= 0.9;
                    p.vy *= 0.9;
                    p.vz *= 0.9;
                });
            }

            // Normalize to [0, 1]
            const minX = Math.min(...positions.map(p => p.x));
            const maxX = Math.max(...positions.map(p => p.x));
            const minY = Math.min(...positions.map(p => p.y));
            const maxY = Math.max(...positions.map(p => p.y));
            const minZ = Math.min(...positions.map(p => p.z));
            const maxZ = Math.max(...positions.map(p => p.z));

            return positions.map(p => ({
                x: (p.x - minX) / (maxX - minX),
                y: (p.y - minY) / (maxY - minY),
                z: (p.z - minZ) / (maxZ - minZ)
            }));
        }

        function circularLayout(nodes) {
            return nodes.map((n, i) => {
                const angle = (i / nodes.length) * 2 * Math.PI;
                const radius = 0.4;
                return {
                    x: 0.5 + radius * Math.cos(angle),
                    y: 0.5 + radius * Math.sin(angle),
                    z: 0.5
                };
            });
        }

        function hierarchicalLayout(nodes) {
            // Group by dominant dimension
            const groups = {Love: [], Justice: [], Power: [], Wisdom: []};
            nodes.forEach(n => {
                if (groups[n.dimension]) groups[n.dimension].push(n);
            });

            const positions = [];
            let layer = 0;
            Object.entries(groups).forEach(([dim, grp]) => {
                grp.forEach((n, i) => {
                    positions.push({
                        x: layer * 0.25 + 0.125,
                        y: (i / (grp.length + 1)) * 0.8 + 0.1,
                        z: 0.5
                    });
                });
                layer++;
            });

            return positions;
        }

        // ===== PLOT UPDATE =====
        function updatePlot() {
            const layout_positions = calculateLayout(filteredNodes);

            const nodeX = layout_positions.map(p => p.x);
            const nodeY = layout_positions.map(p => p.y);
            const nodeZ = layout_positions.map(p => p.z);
            const nodeColor = filteredNodes.map(n => n.color);
            const nodeSize = filteredNodes.map(n => n.size);
            const nodeText = filteredNodes.map(n => n.label);
            const nodeIds = filteredNodes.map(n => n.id);

            // Build edge traces
            const edgeX = [], edgeY = [], edgeZ = [];
            filteredEdges.forEach(e => {
                const sIdx = filteredNodes.findIndex(n => n.id === e.source);
                const tIdx = filteredNodes.findIndex(n => n.id === e.target);
                if (sIdx === -1 || tIdx === -1) return;

                edgeX.push(layout_positions[sIdx].x, layout_positions[tIdx].x, null);
                edgeY.push(layout_positions[sIdx].y, layout_positions[tIdx].y, null);
                edgeZ.push(layout_positions[sIdx].z, layout_positions[tIdx].z, null);
            });

            // Path highlight
            let pathX = [], pathY = [], pathZ = [];
            if (pathHighlight && pathHighlight.length > 1) {
                pathHighlight.forEach((nodeId, i) => {
                    if (i < pathHighlight.length - 1) {
                        const sIdx = filteredNodes.findIndex(n => n.id === nodeId);
                        const tIdx = filteredNodes.findIndex(n => n.id === pathHighlight[i + 1]);
                        if (sIdx !== -1 && tIdx !== -1) {
                            pathX.push(layout_positions[sIdx].x, layout_positions[tIdx].x, null);
                            pathY.push(layout_positions[sIdx].y, layout_positions[tIdx].y, null);
                            pathZ.push(layout_positions[sIdx].z, layout_positions[tIdx].z, null);
                        }
                    }
                });
            }

            const traceEdges = {
                x: edgeX, y: edgeY, z: edgeZ,
                mode: 'lines',
                type: 'scatter3d',
                line: { color: '#888', width: 2, opacity: 0.3 },
                hoverinfo: 'none',
                showlegend: false
            };

            const tracePath = {
                x: pathX, y: pathY, z: pathZ,
                mode: 'lines',
                type: 'scatter3d',
                line: { color: '#00ff88', width: 6, opacity: 1 },
                hoverinfo: 'none',
                showlegend: false
            };

            const traceNodes = {
                x: nodeX, y: nodeY, z: nodeZ,
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
                customdata: nodeIds,
                hovertemplate: '<b>%{text}</b><extra></extra>',
                showlegend: false
            };

            const isDark = !document.body.classList.contains('light-theme');
            const bgColor = isDark ? '#111' : '#fff';
            const gridColor = isDark ? '#333' : '#ddd';

            const layout = {
                margin: {l: 0, r: 0, b: 0, t: 0},
                paper_bgcolor: bgColor,
                scene: {
                    xaxis: { title: 'Love', range: [0, 1], backgroundcolor: bgColor, gridcolor: gridColor },
                    yaxis: { title: 'Justice', range: [0, 1], backgroundcolor: bgColor, gridcolor: gridColor },
                    zaxis: { title: 'Power', range: [0, 1], backgroundcolor: bgColor, gridcolor: gridColor },
                    camera: { eye: {x: 1.5, y: 1.5, z: 1.5} }
                },
                showlegend: false
            };

            const traces = [traceEdges];
            if (pathX.length > 0) traces.push(tracePath);
            traces.push(traceNodes);

            Plotly.react('chart', traces, layout);

            // Add click handler
            document.getElementById('chart').on('plotly_click', function(data) {
                if (data.points && data.points[0] && data.points[0].customdata !== undefined) {
                    handleNodeClick(data.points[0].customdata);
                }
            });
        }

        // ===== NODE SELECTION =====
        function handleNodeClick(nodeId) {
            const node = allNodes.find(n => n.id === nodeId);
            if (!node) return;

            if (!sourceNode) {
                sourceNode = nodeId;
                document.getElementById('source-node').textContent = node.label;
                document.getElementById('source-display').classList.add('active');
                showToast('Source selected: ' + node.label);
            } else if (!targetNode) {
                targetNode = nodeId;
                document.getElementById('target-node').textContent = node.label;
                document.getElementById('target-display').classList.add('active');
                showToast('Target selected: ' + node.label);
            } else {
                // Reset and start over
                sourceNode = nodeId;
                targetNode = null;
                document.getElementById('source-node').textContent = node.label;
                document.getElementById('target-node').textContent = 'Click a node';
                document.getElementById('source-display').classList.add('active');
                document.getElementById('target-display').classList.remove('active');
                showToast('Source changed: ' + node.label);
            }
        }

        // ===== PATH FINDING (Dijkstra) =====
        function findPath() {
            if (!sourceNode || !targetNode) {
                showToast('Please select both source and target nodes');
                return;
            }

            if (sourceNode === targetNode) {
                showToast('Source and target are the same');
                return;
            }

            const path = dijkstra(sourceNode, targetNode);
            if (path.length === 0) {
                showToast('No path found between nodes');
                document.getElementById('path-result').style.display = 'none';
                pathHighlight = null;
            } else {
                pathHighlight = path;
                displayPath(path);
                showToast(`Path found: ${path.length} hops`);
            }

            updatePlot();
        }

        function dijkstra(start, end) {
            const dist = {};
            const prev = {};
            const visited = new Set();
            const queue = [];

            // Initialize
            allNodes.forEach(n => {
                dist[n.id] = Infinity;
                prev[n.id] = null;
            });
            dist[start] = 0;
            queue.push({node: start, dist: 0});

            while (queue.length > 0) {
                // Get node with min distance
                queue.sort((a, b) => a.dist - b.dist);
                const {node: current} = queue.shift();

                if (visited.has(current)) continue;
                visited.add(current);

                if (current === end) break;

                // Check neighbors
                const neighbors = adjacencyList[current] || [];
                neighbors.forEach(({node: neighbor, weight}) => {
                    if (visited.has(neighbor)) return;

                    const altDist = dist[current] + (1.0 - weight); // Lower weight = shorter distance
                    if (altDist < dist[neighbor]) {
                        dist[neighbor] = altDist;
                        prev[neighbor] = current;
                        queue.push({node: neighbor, dist: altDist});
                    }
                });
            }

            // Reconstruct path
            if (dist[end] === Infinity) return [];

            const path = [];
            let current = end;
            while (current !== null) {
                path.unshift(current);
                current = prev[current];
            }

            return path;
        }

        function displayPath(path) {
            const stepsDiv = document.getElementById('path-steps');
            stepsDiv.innerHTML = '';

            path.forEach((nodeId, i) => {
                const node = allNodes.find(n => n.id === nodeId);
                const step = document.createElement('div');
                step.className = 'path-step';
                step.textContent = `${i + 1}. ${node.label}`;
                stepsDiv.appendChild(step);
            });

            document.getElementById('path-result').style.display = 'block';
        }

        function clearPath() {
            sourceNode = null;
            targetNode = null;
            pathHighlight = null;
            document.getElementById('source-node').textContent = 'Click a node';
            document.getElementById('target-node').textContent = 'Click a node';
            document.getElementById('source-display').classList.remove('active');
            document.getElementById('target-display').classList.remove('active');
            document.getElementById('path-result').style.display = 'none';
            updatePlot();
            showToast('Path cleared');
        }

        // ===== NETWORK METRICS =====
        function updateMetrics() {
            const nodeCount = filteredNodes.length;
            const edgeCount = filteredEdges.length;

            // Network density
            const maxEdges = (nodeCount * (nodeCount - 1)) / 2;
            const density = maxEdges > 0 ? edgeCount / maxEdges : 0;

            // Average degree
            const degrees = {};
            filteredNodes.forEach(n => degrees[n.id] = 0);
            filteredEdges.forEach(e => {
                degrees[e.source]++;
                degrees[e.target]++;
            });
            const avgDegree = nodeCount > 0 ? Object.values(degrees).reduce((a, b) => a + b, 0) / nodeCount : 0;

            // Clustering coefficient (simplified)
            let clustering = 0;
            if (nodeCount > 0) {
                filteredNodes.forEach(n => {
                    const neighbors = adjacencyList[n.id] || [];
                    const k = neighbors.length;
                    if (k < 2) return;

                    let triangles = 0;
                    for (let i = 0; i < neighbors.length; i++) {
                        for (let j = i + 1; j < neighbors.length; j++) {
                            const n1 = neighbors[i].node;
                            const n2 = neighbors[j].node;
                            if (adjacencyList[n1] && adjacencyList[n1].some(nb => nb.node === n2)) {
                                triangles++;
                            }
                        }
                    }
                    const maxTriangles = (k * (k - 1)) / 2;
                    if (maxTriangles > 0) clustering += triangles / maxTriangles;
                });
                clustering /= nodeCount;
            }

            document.getElementById('node-count').textContent = nodeCount;
            document.getElementById('edge-count').textContent = edgeCount;
            document.getElementById('density').textContent = density.toFixed(3);
            document.getElementById('avg-degree').textContent = avgDegree.toFixed(2);
            document.getElementById('clustering').textContent = clustering.toFixed(3);
        }

        // ===== EXPORT =====
        function exportJSON() {
            const data = {
                nodes: filteredNodes,
                edges: filteredEdges,
                metrics: {
                    nodeCount: filteredNodes.length,
                    edgeCount: filteredEdges.length,
                    density: parseFloat(document.getElementById('density').textContent),
                    avgDegree: parseFloat(document.getElementById('avg-degree').textContent),
                    clustering: parseFloat(document.getElementById('clustering').textContent)
                }
            };

            const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'topology_graph.json';
            a.click();
            URL.revokeObjectURL(url);
            showToast('JSON exported');
        }

        function exportCSV() {
            // Export nodes
            let csv = 'ID,Label,Love,Justice,Power,Wisdom,Dimension,Mass\\n';
            filteredNodes.forEach(n => {
                csv += `${n.id},${n.label},${n.x},${n.y},${n.z},${n.w || 0},${n.dimension},${n.mass}\\n`;
            });
            csv += '\\n\\nEdges\\n';
            csv += 'Source,Target,Weight\\n';
            filteredEdges.forEach(e => {
                const src = allNodes.find(n => n.id === e.source);
                const tgt = allNodes.find(n => n.id === e.target);
                csv += `${src.label},${tgt.label},${e.weight.toFixed(3)}\\n`;
            });

            const blob = new Blob([csv], {type: 'text/csv'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'topology_graph.csv';
            a.click();
            URL.revokeObjectURL(url);
            showToast('CSV exported');
        }

        function exportPNG() {
            Plotly.downloadImage('chart', {
                format: 'png',
                width: 1920,
                height: 1080,
                filename: 'topology_graph'
            });
            showToast('PNG exported');
        }

        // ===== THEME =====
        function toggleTheme() {
            document.body.classList.toggle('light-theme');
            updatePlot();
            saveConfig();
            showToast('Theme toggled');
        }

        // ===== UI CONTROLS =====
        function togglePanel() {
            const panel = document.getElementById('controlPanel');
            const btn = document.getElementById('toggleBtn');
            panel.classList.toggle('hidden');
            btn.classList.toggle('panel-hidden');
        }

        function showToast(message) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 2000);
        }

        // ===== CONFIG PERSISTENCE =====
        function saveConfig() {
            const config = {
                search: document.getElementById('search').value,
                dimension: document.getElementById('dimension-filter').value,
                threshold: document.getElementById('threshold').value,
                minMass: document.getElementById('min-mass').value,
                layout: currentLayout,
                theme: document.body.classList.contains('light-theme') ? 'light' : 'dark'
            };
            localStorage.setItem('topology-config', JSON.stringify(config));
        }

        function loadConfig() {
            const saved = localStorage.getItem('topology-config');
            if (!saved) return;

            try {
                const config = JSON.parse(saved);
                if (config.search) document.getElementById('search').value = config.search;
                if (config.dimension) document.getElementById('dimension-filter').value = config.dimension;
                if (config.threshold) {
                    document.getElementById('threshold').value = config.threshold;
                    document.getElementById('threshold-val').textContent = parseFloat(config.threshold).toFixed(2);
                }
                if (config.minMass) {
                    document.getElementById('min-mass').value = config.minMass;
                    document.getElementById('mass-val').textContent = config.minMass;
                }
                if (config.layout) {
                    currentLayout = config.layout;
                    document.getElementById('layout').value = config.layout;
                }
                if (config.theme === 'light') {
                    document.body.classList.add('light-theme');
                }
            } catch (e) {
                console.error('Failed to load config:', e);
            }
        }

        // ===== KEYBOARD SHORTCUTS =====
        document.addEventListener('keydown', function(e) {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;

            switch(e.key.toLowerCase()) {
                case 'f':
                    e.preventDefault();
                    if (!document.fullscreenElement) {
                        document.documentElement.requestFullscreen();
                    } else {
                        document.exitFullscreen();
                    }
                    break;
                case 'r':
                    e.preventDefault();
                    Plotly.relayout('chart', {
                        'scene.camera': {eye: {x: 1.5, y: 1.5, z: 1.5}}
                    });
                    showToast('Camera reset');
                    break;
                case 'h':
                    e.preventDefault();
                    togglePanel();
                    break;
                case 'e':
                    e.preventDefault();
                    exportJSON();
                    break;
                case 't':
                    e.preventDefault();
                    toggleTheme();
                    break;
                case 'p':
                    e.preventDefault();
                    findPath();
                    break;
            }
        });
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
                w = p.get('wisdom', 0.0)
                mass = p.get('semantic_mass', 0.0)
                dom = p.get('dominant_dimension', 'Unknown')
            else:
                target = p.target
                if p.ljpw_coordinates:
                    l = p.ljpw_coordinates.love
                    j = p.ljpw_coordinates.justice
                    pow_val = p.ljpw_coordinates.power
                    w = getattr(p.ljpw_coordinates, 'wisdom', 0.0)
                else:
                    l, j, pow_val, w = 0.0, 0.0, 0.0, 0.0
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
                'w': w,
                'dimension': dom,
                'color': color,
                'size': size,
                'mass': mass
            })

        # 2. Create Edges (based on semantic similarity)
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
