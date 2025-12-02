"""
Cluster Map Generator

Generates interactive 3D visualizations of semantic clusters using Plotly.js.
Maps LJPW dimensions to visual properties:
- X Axis: Love (Connectivity)
- Y Axis: Justice (Security)
- Z Axis: Power (Performance)
- Color: Wisdom (Insight)
- Size: Semantic Mass

Enhanced with:
- Interactive filters
- Search functionality
- Export capabilities (CSV, JSON)
- Theme toggle (dark/light)
- Keyboard shortcuts
- Help tooltips
- Fullscreen mode
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
        :root {
            --bg-primary: #111;
            --bg-secondary: #222;
            --text-primary: #eee;
            --text-secondary: #aaa;
            --accent: #4facfe;
            --border: #333;
        }

        .light-theme {
            --bg-primary: #fff;
            --bg-secondary: #f5f5f5;
            --text-primary: #222;
            --text-secondary: #666;
            --accent: #0575E6;
            --border: #ddd;
        }

        body {
            margin: 0;
            padding: 0;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: 'Segoe UI', sans-serif;
            transition: all 0.3s ease;
        }

        #plot { width: 100vw; height: 100vh; }

        .control-panel {
            position: fixed;
            top: 20px;
            left: 20px;
            background: var(--bg-secondary);
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 1000;
            max-width: 320px;
            max-height: 90vh;
            overflow-y: auto;
        }

        .control-panel h3 {
            margin: 0 0 15px 0;
            color: var(--accent);
            font-size: 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .control-section {
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid var(--border);
        }

        .control-section:last-child {
            border-bottom: none;
        }

        .control-section h4 {
            margin: 0 0 10px 0;
            font-size: 14px;
            color: var(--text-secondary);
            font-weight: 600;
        }

        .dimension-info {
            font-size: 12px;
            line-height: 1.6;
            margin: 5px 0;
        }

        .dimension-info strong {
            color: var(--accent);
            display: inline-block;
            width: 80px;
        }

        input[type="text"] {
            width: calc(100% - 12px);
            padding: 8px;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: var(--bg-primary);
            color: var(--text-primary);
            font-size: 13px;
            margin-bottom: 8px;
        }

        input[type="range"] {
            width: calc(100% - 10px);
            margin: 5px 0;
        }

        .range-label {
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: var(--text-secondary);
            margin-top: -3px;
        }

        button {
            padding: 8px 12px;
            border: none;
            border-radius: 6px;
            background: var(--accent);
            color: white;
            cursor: pointer;
            font-size: 13px;
            margin: 4px 4px 4px 0;
            transition: opacity 0.2s;
        }

        button:hover {
            opacity: 0.8;
        }

        button.secondary {
            background: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border);
        }

        .stats-box {
            background: var(--bg-primary);
            padding: 10px;
            border-radius: 6px;
            margin-top: 10px;
            font-size: 12px;
        }

        .stat-row {
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
        }

        .toggle-btn {
            width: 30px;
            height: 30px;
            padding: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-left: 10px;
        }

        .help-tooltip {
            position: relative;
            display: inline-block;
            cursor: help;
        }

        .help-tooltip .tooltip-text {
            visibility: hidden;
            width: 250px;
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            text-align: left;
            border-radius: 6px;
            padding: 10px;
            position: absolute;
            z-index: 1001;
            bottom: 125%;
            left: 50%;
            margin-left: -125px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }

        .help-tooltip:hover .tooltip-text {
            visibility: visible;
            opacity: 1;
        }

        .keyboard-shortcuts {
            font-size: 11px;
            color: var(--text-secondary);
            margin-top: 10px;
            padding: 8px;
            background: var(--bg-primary);
            border-radius: 6px;
        }

        kbd {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 3px;
            padding: 2px 5px;
            font-size: 10px;
        }

        .hidden {
            display: none;
        }

        .filter-count {
            color: var(--accent);
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="control-panel">
        <h3>
            Semantic Universe
            <button class="toggle-btn" onclick="toggleTheme()" title="Toggle Theme">🌓</button>
        </h3>

        <div class="control-section">
            <h4>📊 Axis Mapping</h4>
            <div class="dimension-info"><strong>X (Red):</strong> Love (Connectivity)</div>
            <div class="dimension-info"><strong>Y (Cyan):</strong> Justice (Security)</div>
            <div class="dimension-info"><strong>Z (Orange):</strong> Power (Performance)</div>
            <div class="dimension-info"><strong>Color:</strong> Wisdom (Insight)</div>
            <div class="dimension-info"><strong>Size:</strong> Semantic Mass</div>
        </div>

        <div class="control-section">
            <h4>🔍 Search & Filter</h4>
            <input type="text" id="search" placeholder="Search by target name..." oninput="applyFilters()">

            <label>Love (L): <span id="love-val">0.0 - 1.0</span></label>
            <input type="range" id="love-min" min="0" max="1" step="0.05" value="0" oninput="applyFilters()">
            <input type="range" id="love-max" min="0" max="1" step="0.05" value="1" oninput="applyFilters()">

            <label>Justice (J): <span id="justice-val">0.0 - 1.0</span></label>
            <input type="range" id="justice-min" min="0" max="1" step="0.05" value="0" oninput="applyFilters()">
            <input type="range" id="justice-max" min="0" max="1" step="0.05" value="1" oninput="applyFilters()">

            <label>Power (P): <span id="power-val">0.0 - 1.0</span></label>
            <input type="range" id="power-min" min="0" max="1" step="0.05" value="0" oninput="applyFilters()">
            <input type="range" id="power-max" min="0" max="1" step="0.05" value="1" oninput="applyFilters()">

            <label>Wisdom (W): <span id="wisdom-val">0.0 - 1.0</span></label>
            <input type="range" id="wisdom-min" min="0" max="1" step="0.05" value="0" oninput="applyFilters()">
            <input type="range" id="wisdom-max" min="0" max="1" step="0.05" value="1" oninput="applyFilters()">

            <label>Semantic Mass: <span id="mass-val">Any</span></label>
            <input type="range" id="mass-min" min="0" max="100" step="1" value="0" oninput="applyFilters()">

            <button onclick="resetFilters()" class="secondary">Reset Filters</button>
        </div>

        <div class="control-section">
            <h4>📈 Statistics</h4>
            <div class="stats-box">
                <div class="stat-row">
                    <span>Visible:</span>
                    <span class="filter-count" id="stat-visible">0</span>
                </div>
                <div class="stat-row">
                    <span>Total:</span>
                    <span id="stat-total">0</span>
                </div>
                <div class="stat-row">
                    <span>Avg Mass:</span>
                    <span id="stat-mass">0.0</span>
                </div>
                <div class="stat-row">
                    <span>Avg Harmony:</span>
                    <span id="stat-harmony">0%</span>
                </div>
            </div>
        </div>

        <div class="control-section">
            <h4>💾 Export</h4>
            <button onclick="exportJSON()">Export JSON</button>
            <button onclick="exportCSV()" class="secondary">Export CSV</button>
            <button onclick="exportImage()" class="secondary">Save Image</button>
        </div>

        <div class="control-section">
            <h4>⚡ Actions</h4>
            <button onclick="resetView()">Reset View</button>
            <button onclick="toggleFullscreen()" class="secondary">Fullscreen</button>
            <button onclick="togglePanel()" class="secondary">Hide Panel</button>
        </div>

        <div class="keyboard-shortcuts">
            <strong>Keyboard Shortcuts:</strong><br>
            <kbd>F</kbd> Fullscreen &nbsp;
            <kbd>R</kbd> Reset View &nbsp;
            <kbd>H</kbd> Hide Panel<br>
            <kbd>E</kbd> Export JSON &nbsp;
            <kbd>T</kbd> Toggle Theme
        </div>
    </div>

    <div id="plot"></div>

    <script>
        let allData = %DATA%;
        let filteredData = [...allData];
        let plotDiv = document.getElementById('plot');

        // Initial render
        updatePlot();
        updateStats();

        function updatePlot() {
            const trace = {
                x: filteredData.map(d => d.l),
                y: filteredData.map(d => d.j),
                z: filteredData.map(d => d.p),
                mode: 'markers',
                marker: {
                    size: filteredData.map(d => Math.max(5, Math.min(50, d.mass * 2))),
                    color: filteredData.map(d => d.w),
                    colorscale: 'Viridis',
                    opacity: 0.8,
                    showscale: true,
                    colorbar: {title: 'Wisdom', titleside: 'right'}
                },
                text: filteredData.map(d => `
                    <b>${d.target}</b><br>
                    Mass: ${d.mass.toFixed(1)}<br>
                    L: ${d.l.toFixed(2)} (Love)<br>
                    J: ${d.j.toFixed(2)} (Justice)<br>
                    P: ${d.p.toFixed(2)} (Power)<br>
                    W: ${d.w.toFixed(2)} (Wisdom)<br>
                    <i>${d.desc}</i>
                `),
                hoverinfo: 'text',
                type: 'scatter3d',
                name: 'Targets'
            };

            const layout = {
                margin: {l: 0, r: 0, b: 0, t: 0},
                paper_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                scene: {
                    xaxis: {
                        title: 'Love (Connectivity)',
                        range: [0, 1],
                        gridcolor: getComputedStyle(document.body).getPropertyValue('--border'),
                        zerolinecolor: '#555'
                    },
                    yaxis: {
                        title: 'Justice (Security)',
                        range: [0, 1],
                        gridcolor: getComputedStyle(document.body).getPropertyValue('--border'),
                        zerolinecolor: '#555'
                    },
                    zaxis: {
                        title: 'Power (Performance)',
                        range: [0, 1],
                        gridcolor: getComputedStyle(document.body).getPropertyValue('--border'),
                        zerolinecolor: '#555'
                    },
                    camera: {
                        eye: {x: 1.5, y: 1.5, z: 1.5}
                    }
                }
            };

            Plotly.react('plot', [trace], layout, {responsive: true});
        }

        function applyFilters() {
            const search = document.getElementById('search').value.toLowerCase();
            const lMin = parseFloat(document.getElementById('love-min').value);
            const lMax = parseFloat(document.getElementById('love-max').value);
            const jMin = parseFloat(document.getElementById('justice-min').value);
            const jMax = parseFloat(document.getElementById('justice-max').value);
            const pMin = parseFloat(document.getElementById('power-min').value);
            const pMax = parseFloat(document.getElementById('power-max').value);
            const wMin = parseFloat(document.getElementById('wisdom-min').value);
            const wMax = parseFloat(document.getElementById('wisdom-max').value);
            const massMin = parseFloat(document.getElementById('mass-min').value);

            // Update range labels
            document.getElementById('love-val').textContent = `${lMin.toFixed(1)} - ${lMax.toFixed(1)}`;
            document.getElementById('justice-val').textContent = `${jMin.toFixed(1)} - ${jMax.toFixed(1)}`;
            document.getElementById('power-val').textContent = `${pMin.toFixed(1)} - ${pMax.toFixed(1)}`;
            document.getElementById('wisdom-val').textContent = `${wMin.toFixed(1)} - ${wMax.toFixed(1)}`;
            document.getElementById('mass-val').textContent = massMin > 0 ? `>= ${massMin}` : 'Any';

            filteredData = allData.filter(d => {
                if (search && !d.target.toLowerCase().includes(search)) return false;
                if (d.l < lMin || d.l > lMax) return false;
                if (d.j < jMin || d.j > jMax) return false;
                if (d.p < pMin || d.p > pMax) return false;
                if (d.w < wMin || d.w > wMax) return false;
                if (d.mass < massMin) return false;
                return true;
            });

            updatePlot();
            updateStats();
        }

        function resetFilters() {
            document.getElementById('search').value = '';
            ['love', 'justice', 'power', 'wisdom'].forEach(dim => {
                document.getElementById(dim + '-min').value = '0';
                document.getElementById(dim + '-max').value = '1';
            });
            document.getElementById('mass-min').value = '0';
            applyFilters();
        }

        function updateStats() {
            document.getElementById('stat-visible').textContent = filteredData.length;
            document.getElementById('stat-total').textContent = allData.length;

            if (filteredData.length > 0) {
                const avgMass = filteredData.reduce((sum, d) => sum + d.mass, 0) / filteredData.length;
                document.getElementById('stat-mass').textContent = avgMass.toFixed(1);

                // Calculate harmony as average of all dimensions
                const avgHarmony = filteredData.reduce((sum, d) => {
                    const harmony = (d.l + d.j + d.p + d.w) / 4;
                    return sum + harmony;
                }, 0) / filteredData.length;
                document.getElementById('stat-harmony').textContent = (avgHarmony * 100).toFixed(0) + '%';
            }
        }

        function resetView() {
            Plotly.relayout('plot', {
                'scene.camera.eye': {x: 1.5, y: 1.5, z: 1.5}
            });
        }

        function toggleFullscreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen();
            } else {
                document.exitFullscreen();
            }
        }

        function togglePanel() {
            const panel = document.querySelector('.control-panel');
            panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        }

        function toggleTheme() {
            document.body.classList.toggle('light-theme');
            updatePlot(); // Refresh plot with new theme colors
        }

        function exportJSON() {
            const dataStr = JSON.stringify(filteredData, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'semantic_clusters_' + new Date().toISOString().split('T')[0] + '.json';
            link.click();
        }

        function exportCSV() {
            let csv = 'Target,Love,Justice,Power,Wisdom,Mass,Description\\n';
            filteredData.forEach(d => {
                csv += `"${d.target}",${d.l},${d.j},${d.p},${d.w},${d.mass},"${d.desc}"\\n`;
            });
            const dataBlob = new Blob([csv], {type: 'text/csv'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'semantic_clusters_' + new Date().toISOString().split('T')[0] + '.csv';
            link.click();
        }

        function exportImage() {
            Plotly.downloadImage('plot', {
                format: 'png',
                width: 1920,
                height: 1080,
                filename: 'semantic_clusters_' + new Date().toISOString().split('T')[0]
            });
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.target.tagName === 'INPUT') return; // Ignore if typing in input

            switch(e.key.toLowerCase()) {
                case 'f':
                    toggleFullscreen();
                    break;
                case 'r':
                    resetView();
                    break;
                case 'h':
                    togglePanel();
                    break;
                case 'e':
                    exportJSON();
                    break;
                case 't':
                    toggleTheme();
                    break;
            }
        });
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
                l = p.get('love', 0.0)
                j = p.get('justice', 0.0)
                p_val = p.get('power', 0.0)
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
