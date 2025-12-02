"""
Interactive Dashboard Generator

Generates a comprehensive, self-contained interactive dashboard that combines
multiple visualizations with full functionality including:
- Data import/export (JSON, CSV)
- Config save/load
- Report generation
- Interactive filtering and sorting
- Theme customization
- All-in-one functionality like CLI
"""

import json
import os
from typing import List, Dict, Any

class DashboardGenerator:
    """Generates fully self-contained interactive dashboard"""

    def __init__(self):
        self.template = """
<!DOCTYPE html>
<html>
<head>
    <title>Network-Pinpointer Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        :root {
            --bg-primary: #111;
            --bg-secondary: #222;
            --bg-tertiary: #2a2a2a;
            --text-primary: #eee;
            --text-secondary: #aaa;
            --accent: #4facfe;
            --accent-secondary: #00f260;
            --border: #333;
            --danger: #ff0055;
            --warning: #ffaa00;
            --success: #00f260;
        }

        .light-theme {
            --bg-primary: #fff;
            --bg-secondary: #f5f5f5;
            --bg-tertiary: #e8e8e8;
            --text-primary: #222;
            --text-secondary: #666;
            --accent: #0575E6;
            --accent-secondary: #00a651;
            --border: #ddd;
            --danger: #dc3545;
            --warning: #ffc107;
            --success: #28a745;
        }

        * { box-sizing: border-box; }

        body {
            margin: 0;
            padding: 0;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            transition: background-color 0.3s, color 0.3s;
        }

        .header {
            background: var(--bg-secondary);
            padding: 20px 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header h1 {
            color: var(--accent);
            margin: 0;
            font-size: 24px;
        }

        .header-actions {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .container {
            padding: 30px 40px;
            max-width: 1800px;
            margin: 0 auto;
        }

        .toolbar {
            background: var(--bg-secondary);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 30px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }

        .search-box {
            flex: 1;
            min-width: 250px;
        }

        .search-box input {
            width: 100%;
            padding: 10px 15px;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: var(--bg-primary);
            color: var(--text-primary);
            font-size: 14px;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }

        .grid-full {
            grid-column: 1 / -1;
        }

        .card {
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.3);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--border);
        }

        .card-header h2 {
            margin: 0;
            font-size: 18px;
            color: var(--text-primary);
        }

        .card-actions {
            display: flex;
            gap: 8px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .stat-box {
            background: var(--bg-tertiary);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 2px solid transparent;
            transition: border-color 0.3s;
        }

        .stat-box:hover {
            border-color: var(--accent);
        }

        .stat-value {
            font-size: 32px;
            font-weight: bold;
            color: var(--accent);
            margin-bottom: 8px;
        }

        .stat-label {
            font-size: 13px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        button, .btn {
            padding: 10px 18px;
            border: none;
            border-radius: 8px;
            background: var(--accent);
            color: white;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: opacity 0.2s, transform 0.1s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        button:hover, .btn:hover {
            opacity: 0.9;
            transform: scale(1.02);
        }

        button:active, .btn:active {
            transform: scale(0.98);
        }

        button.secondary {
            background: var(--bg-tertiary);
            color: var(--text-primary);
            border: 1px solid var(--border);
        }

        button.danger {
            background: var(--danger);
        }

        button.success {
            background: var(--success);
        }

        button.small {
            padding: 6px 12px;
            font-size: 12px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        thead {
            background: var(--bg-tertiary);
        }

        th {
            text-align: left;
            padding: 12px 15px;
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            cursor: pointer;
            user-select: none;
        }

        th:hover {
            background: var(--bg-primary);
        }

        th.sortable::after {
            content: ' ⇅';
            opacity: 0.3;
        }

        th.sorted-asc::after {
            content: ' ↑';
            opacity: 1;
        }

        th.sorted-desc::after {
            content: ' ↓';
            opacity: 1;
        }

        td {
            padding: 12px 15px;
            border-bottom: 1px solid var(--border);
        }

        tr:hover {
            background: var(--bg-tertiary);
        }

        .tag {
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            display: inline-block;
        }

        .tag-high { background: var(--danger); color: white; }
        .tag-med { background: var(--warning); color: black; }
        .tag-low { background: var(--success); color: white; }

        .recommendations {
            background: var(--bg-tertiary);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid var(--accent);
        }

        .recommendation-item {
            padding: 12px 0;
            border-bottom: 1px solid var(--border);
        }

        .recommendation-item:last-child {
            border-bottom: none;
        }

        .recommendation-title {
            font-weight: 600;
            color: var(--accent);
            margin-bottom: 5px;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background: var(--bg-secondary);
            padding: 30px;
            border-radius: 16px;
            max-width: 600px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .modal-header h3 {
            margin: 0;
            color: var(--accent);
        }

        .close-btn {
            background: none;
            border: none;
            font-size: 28px;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 0;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: var(--text-secondary);
            font-size: 13px;
            font-weight: 600;
        }

        .form-group input, .form-group textarea, .form-group select {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: var(--bg-primary);
            color: var(--text-primary);
            font-size: 14px;
            font-family: inherit;
        }

        .form-group textarea {
            min-height: 100px;
            resize: vertical;
        }

        .help-text {
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 5px;
        }

        .toast {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: var(--accent);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 2000;
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.3s, transform 0.3s;
        }

        .toast.show {
            opacity: 1;
            transform: translateY(0);
        }

        .keyboard-hint {
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: var(--bg-secondary);
            padding: 15px 20px;
            border-radius: 10px;
            font-size: 12px;
            color: var(--text-secondary);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 100;
        }

        kbd {
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 3px 7px;
            font-size: 11px;
            font-family: monospace;
        }

        .chart-container {
            min-height: 400px;
            background: var(--bg-primary);
            border-radius: 8px;
            padding: 10px;
        }

        @media (max-width: 768px) {
            .container { padding: 15px; }
            .grid { grid-template-columns: 1fr; }
            .header { padding: 15px 20px; }
            .toolbar { flex-direction: column; }
            .search-box { min-width: 100%; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌐 Network Semantic Dashboard</h1>
        <div class="header-actions">
            <button onclick="importData()" class="secondary small">📁 Import Data</button>
            <button onclick="exportReport()" class="small">📊 Export Report</button>
            <button onclick="saveConfig()" class="secondary small">💾 Save Config</button>
            <button onclick="loadConfig()" class="secondary small">📂 Load Config</button>
            <button onclick="toggleTheme()" class="small" title="Toggle Theme (T)">🌓</button>
            <button onclick="showHelp()" class="secondary small">❓</button>
        </div>
    </div>

    <div class="container">
        <div class="toolbar">
            <div class="search-box">
                <input type="text" id="search" placeholder="🔍 Search targets..." oninput="applyFilters()">
            </div>
            <select id="posture-filter" onchange="applyFilters()">
                <option value="all">All Security Postures</option>
                <option value="SECURE">Secure Only</option>
                <option value="MODERATE">Moderate Risk</option>
                <option value="VULNERABLE">Vulnerable</option>
            </select>
            <select id="dimension-filter" onchange="applyFilters()">
                <option value="all">All Dimensions</option>
                <option value="Love">Love Dominant</option>
                <option value="Justice">Justice Dominant</option>
                <option value="Power">Power Dominant</option>
                <option value="Wisdom">Wisdom Dominant</option>
            </select>
            <button onclick="resetFilters()" class="secondary">Reset</button>
            <button onclick="generateInsights()">Generate Insights</button>
        </div>

        <!-- Statistics -->
        <div class="card grid-full">
            <div class="card-header">
                <h2>📈 Network Overview</h2>
            </div>
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-value" id="stat-total">0</div>
                    <div class="stat-label">Total Targets</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="stat-visible">0</div>
                    <div class="stat-label">Visible (Filtered)</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="stat-harmony">0%</div>
                    <div class="stat-label">Avg Harmony</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="stat-mass">0.0</div>
                    <div class="stat-label">Total Mass</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" id="stat-risk">Low</div>
                    <div class="stat-label">Risk Level</div>
                </div>
            </div>
        </div>

        <div class="grid">
            <!-- Cluster Map -->
            <div class="card">
                <div class="card-header">
                    <h2>🎯 Semantic Clusters (3D)</h2>
                    <div class="card-actions">
                        <button onclick="resetClusterView()" class="secondary small">Reset View</button>
                    </div>
                </div>
                <div id="cluster-map" class="chart-container"></div>
            </div>

            <!-- Mass Distribution -->
            <div class="card">
                <div class="card-header">
                    <h2>📊 Mass Distribution</h2>
                    <div class="card-actions">
                        <button onclick="exportChart('mass')" class="secondary small">Export</button>
                    </div>
                </div>
                <div id="mass-dist" class="chart-container"></div>
            </div>
        </div>

        <!-- Recommendations -->
        <div class="card grid-full" id="recommendations-card" style="display:none;">
            <div class="card-header">
                <h2>💡 AI-Powered Recommendations</h2>
            </div>
            <div class="recommendations" id="recommendations-content"></div>
        </div>

        <!-- Targets Table -->
        <div class="card grid-full">
            <div class="card-header">
                <h2>🎯 Targets Overview</h2>
                <div class="card-actions">
                    <button onclick="exportTableCSV()" class="secondary small">Export CSV</button>
                </div>
            </div>
            <table id="targets-table">
                <thead>
                    <tr>
                        <th class="sortable" onclick="sortTable('target')">Target</th>
                        <th class="sortable" onclick="sortTable('mass')">Mass</th>
                        <th class="sortable" onclick="sortTable('dominant')">Dominant</th>
                        <th class="sortable" onclick="sortTable('harmony')">Harmony</th>
                        <th class="sortable" onclick="sortTable('posture')">Security</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
    </div>

    <!-- Import Modal -->
    <div id="importModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Import Data</h3>
                <button class="close-btn" onclick="closeModal('importModal')">&times;</button>
            </div>
            <div class="form-group">
                <label>Upload JSON File</label>
                <input type="file" id="file-upload" accept=".json">
                <p class="help-text">Upload semantic profile data in JSON format</p>
            </div>
            <div class="form-group">
                <label>Or Paste JSON Data</label>
                <textarea id="json-input" placeholder='[{"target": "example.com", "l": 0.8, ...}]'></textarea>
                <p class="help-text">Paste JSON data directly</p>
            </div>
            <button onclick="processImport()">Import</button>
            <button onclick="closeModal('importModal')" class="secondary">Cancel</button>
        </div>
    </div>

    <!-- Help Modal -->
    <div id="helpModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Dashboard Help</h3>
                <button class="close-btn" onclick="closeModal('helpModal')">&times;</button>
            </div>
            <h4>Keyboard Shortcuts</h4>
            <p><kbd>T</kbd> - Toggle theme</p>
            <p><kbd>F</kbd> - Fullscreen</p>
            <p><kbd>I</kbd> - Import data</p>
            <p><kbd>E</kbd> - Export report</p>
            <p><kbd>R</kbd> - Reset filters</p>
            <p><kbd>?</kbd> - Show this help</p>

            <h4>LJPW Dimensions</h4>
            <p><strong>Love (L):</strong> Connectivity & communication</p>
            <p><strong>Justice (J):</strong> Security & policies</p>
            <p><strong>Power (P):</strong> Performance & execution</p>
            <p><strong>Wisdom (W):</strong> Visibility & monitoring</p>

            <h4>Features</h4>
            <p>• Search and filter targets in real-time</p>
            <p>• Sort table columns by clicking headers</p>
            <p>• Export data as CSV or JSON</p>
            <p>• Generate AI-powered insights</p>
            <p>• Save/load custom configurations</p>
        </div>
    </div>

    <div class="toast" id="toast"></div>
    <div class="keyboard-hint">Press <kbd>?</kbd> for help</div>

    <script>
        let allData = %DATA%;
        let filteredData = [...allData];
        let currentSort = {column: null, direction: 'asc'};
        let config = {};

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            updateAll();
            loadSavedConfig();
        });

        function updateAll() {
            updateStats();
            updateClusterMap();
            updateMassChart();
            updateTable();
        }

        function updateStats() {
            document.getElementById('stat-total').textContent = allData.length;
            document.getElementById('stat-visible').textContent = filteredData.length;

            if (filteredData.length > 0) {
                const avgHarmony = filteredData.reduce((sum, d) => sum + d.harmony, 0) / filteredData.length;
                document.getElementById('stat-harmony').textContent = (avgHarmony * 100).toFixed(0) + '%';

                const totalMass = filteredData.reduce((sum, d) => sum + d.mass, 0);
                document.getElementById('stat-mass').textContent = totalMass.toFixed(1);

                // Calculate risk
                const vulnerableCount = filteredData.filter(d => d.posture.includes('VULNERABLE')).length;
                const riskPct = vulnerableCount / filteredData.length;
                const riskLevel = riskPct > 0.3 ? 'High' : riskPct > 0.1 ? 'Medium' : 'Low';
                document.getElementById('stat-risk').textContent = riskLevel;
            }
        }

        function updateClusterMap() {
            const trace = {
                x: filteredData.map(d => d.l),
                y: filteredData.map(d => d.j),
                z: filteredData.map(d => d.p),
                mode: 'markers',
                type: 'scatter3d',
                text: filteredData.map(d => `<b>${d.target}</b><br>Mass: ${d.mass.toFixed(1)}<br>Harmony: ${(d.harmony*100).toFixed(0)}%`),
                marker: {
                    size: filteredData.map(d => 5 + Math.log(d.mass + 1) * 5),
                    color: filteredData.map(d => d.w),
                    colorscale: 'Viridis',
                    opacity: 0.8,
                    showscale: true,
                    colorbar: {title: 'Wisdom'}
                },
                hoverinfo: 'text'
            };

            const layout = {
                margin: {l: 0, r: 0, b: 0, t: 0},
                paper_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                scene: {
                    xaxis: {title: 'Love', gridcolor: getComputedStyle(document.body).getPropertyValue('--border')},
                    yaxis: {title: 'Justice', gridcolor: getComputedStyle(document.body).getPropertyValue('--border')},
                    zaxis: {title: 'Power', gridcolor: getComputedStyle(document.body).getPropertyValue('--border')},
                    camera: {eye: {x: 1.5, y: 1.5, z: 1.5}}
                }
            };

            Plotly.react('cluster-map', [trace], layout, {responsive: true});
        }

        function updateMassChart() {
            const trace = {
                x: filteredData.map(d => d.mass),
                type: 'histogram',
                marker: {color: getComputedStyle(document.documentElement).getPropertyValue('--accent')}
            };

            const layout = {
                margin: {l: 40, r: 20, b: 40, t: 20},
                paper_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                plot_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                font: {color: getComputedStyle(document.body).getPropertyValue('--text-primary')},
                xaxis: {title: 'Semantic Mass', gridcolor: getComputedStyle(document.body).getPropertyValue('--border')},
                yaxis: {title: 'Count', gridcolor: getComputedStyle(document.body).getPropertyValue('--border')}
            };

            Plotly.react('mass-dist', [trace], layout, {responsive: true});
        }

        function updateTable() {
            const tbody = document.querySelector('#targets-table tbody');
            tbody.innerHTML = '';

            filteredData.forEach(d => {
                const tr = document.createElement('tr');
                let postureClass = 'tag-low';
                if (d.posture.includes('VULNERABLE')) postureClass = 'tag-high';
                else if (d.posture.includes('MODERATE')) postureClass = 'tag-med';

                tr.innerHTML = `
                    <td><strong>${d.target}</strong></td>
                    <td>${d.mass.toFixed(1)}</td>
                    <td>${d.dominant}</td>
                    <td>${(d.harmony * 100).toFixed(0)}%</td>
                    <td><span class="tag ${postureClass}">${d.posture}</span></td>
                    <td>
                        <button class="small secondary" onclick="viewDetails('${d.target}')">View</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function applyFilters() {
            const search = document.getElementById('search').value.toLowerCase();
            const posture = document.getElementById('posture-filter').value;
            const dimension = document.getElementById('dimension-filter').value;

            filteredData = allData.filter(d => {
                if (search && !d.target.toLowerCase().includes(search)) return false;
                if (posture !== 'all' && !d.posture.includes(posture)) return false;
                if (dimension !== 'all' && d.dominant !== dimension) return false;
                return true;
            });

            updateAll();
        }

        function resetFilters() {
            document.getElementById('search').value = '';
            document.getElementById('posture-filter').value = 'all';
            document.getElementById('dimension-filter').value = 'all';
            filteredData = [...allData];
            updateAll();
        }

        function sortTable(column) {
            if (currentSort.column === column) {
                currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
            } else {
                currentSort.column = column;
                currentSort.direction = 'asc';
            }

            filteredData.sort((a, b) => {
                let aVal = a[column];
                let bVal = b[column];

                if (typeof aVal === 'string') {
                    aVal = aVal.toLowerCase();
                    bVal = bVal.toLowerCase();
                }

                if (currentSort.direction === 'asc') {
                    return aVal > bVal ? 1 : -1;
                } else {
                    return aVal < bVal ? 1 : -1;
                }
            });

            // Update sort indicators
            document.querySelectorAll('th').forEach(th => {
                th.classList.remove('sorted-asc', 'sorted-desc');
            });
            const th = document.querySelector(`th[onclick="sortTable('${column}')"]`);
            th.classList.add(currentSort.direction === 'asc' ? 'sorted-asc' : 'sorted-desc');

            updateTable();
        }

        function generateInsights() {
            const recommendations = [];

            // Analyze vulnerability
            const vulnerable = filteredData.filter(d => d.posture.includes('VULNERABLE'));
            if (vulnerable.length > 0) {
                recommendations.push({
                    title: `🔴 ${vulnerable.length} Vulnerable Target(s) Detected`,
                    desc: `Immediate attention required for: ${vulnerable.map(d => d.target).join(', ')}`
                });
            }

            // Low harmony
            const lowHarmony = filteredData.filter(d => d.harmony < 0.5);
            if (lowHarmony.length > 0) {
                recommendations.push({
                    title: `⚠️ ${lowHarmony.length} Target(s) with Low Harmony`,
                    desc: `Review configuration and balance for improved performance`
                });
            }

            // High mass concentration
            const avgMass = filteredData.reduce((sum, d) => sum + d.mass, 0) / filteredData.length;
            const highMass = filteredData.filter(d => d.mass > avgMass * 2);
            if (highMass.length > 0) {
                recommendations.push({
                    title: `📊 ${highMass.length} High-Complexity Target(s)`,
                    desc: `Consider segmentation or optimization for: ${highMass.map(d => d.target).join(', ')}`
                });
            }

            // Display recommendations
            if (recommendations.length > 0) {
                const content = document.getElementById('recommendations-content');
                content.innerHTML = recommendations.map(r => `
                    <div class="recommendation-item">
                        <div class="recommendation-title">${r.title}</div>
                        <div>${r.desc}</div>
                    </div>
                `).join('');
                document.getElementById('recommendations-card').style.display = 'block';
                showToast('Generated ' + recommendations.length + ' insights');
            } else {
                showToast('No issues detected - network looks healthy!');
            }
        }

        function importData() {
            document.getElementById('importModal').classList.add('active');
        }

        function processImport() {
            const fileInput = document.getElementById('file-upload');
            const jsonInput = document.getElementById('json-input');

            if (fileInput.files.length > 0) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    try {
                        allData = JSON.parse(e.target.result);
                        filteredData = [...allData];
                        updateAll();
                        closeModal('importModal');
                        showToast('Data imported successfully!');
                    } catch (err) {
                        showToast('Error parsing JSON: ' + err.message);
                    }
                };
                reader.readAsText(fileInput.files[0]);
            } else if (jsonInput.value) {
                try {
                    allData = JSON.parse(jsonInput.value);
                    filteredData = [...allData];
                    updateAll();
                    closeModal('importModal');
                    showToast('Data imported successfully!');
                } catch (err) {
                    showToast('Error parsing JSON: ' + err.message);
                }
            }
        }

        function exportReport() {
            const report = {
                generated: new Date().toISOString(),
                stats: {
                    total: allData.length,
                    visible: filteredData.length,
                    avgHarmony: filteredData.reduce((sum, d) => sum + d.harmony, 0) / filteredData.length,
                    totalMass: filteredData.reduce((sum, d) => sum + d.mass, 0)
                },
                data: filteredData
            };

            const blob = new Blob([JSON.stringify(report, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `network_report_${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            showToast('Report exported successfully!');
        }

        function exportTableCSV() {
            let csv = 'Target,Mass,Dominant,Harmony,Security\\n';
            filteredData.forEach(d => {
                csv += `"${d.target}",${d.mass},"${d.dominant}",${d.harmony},"${d.posture}"\\n`;
            });
            const blob = new Blob([csv], {type: 'text/csv'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `targets_${new Date().toISOString().split('T')[0]}.csv`;
            a.click();
            showToast('Table exported as CSV!');
        }

        function saveConfig() {
            config = {
                filters: {
                    search: document.getElementById('search').value,
                    posture: document.getElementById('posture-filter').value,
                    dimension: document.getElementById('dimension-filter').value
                },
                sort: currentSort,
                theme: document.body.classList.contains('light-theme') ? 'light' : 'dark'
            };
            localStorage.setItem('dashboard-config', JSON.stringify(config));
            showToast('Configuration saved!');
        }

        function loadConfig() {
            const saved = localStorage.getItem('dashboard-config');
            if (saved) {
                config = JSON.parse(saved);
                document.getElementById('search').value = config.filters.search || '';
                document.getElementById('posture-filter').value = config.filters.posture || 'all';
                document.getElementById('dimension-filter').value = config.filters.dimension || 'all';
                if (config.theme === 'light') {
                    document.body.classList.add('light-theme');
                }
                applyFilters();
                showToast('Configuration loaded!');
            } else {
                showToast('No saved configuration found');
            }
        }

        function loadSavedConfig() {
            const saved = localStorage.getItem('dashboard-config');
            if (saved) {
                config = JSON.parse(saved);
                if (config.theme === 'light') {
                    document.body.classList.add('light-theme');
                }
            }
        }

        function toggleTheme() {
            document.body.classList.toggle('light-theme');
            updateClusterMap();
            updateMassChart();
        }

        function resetClusterView() {
            Plotly.relayout('cluster-map', {
                'scene.camera.eye': {x: 1.5, y: 1.5, z: 1.5}
            });
        }

        function viewDetails(target) {
            const data = allData.find(d => d.target === target);
            alert(`Target: ${data.target}\\n\\nLJPW Coordinates:\\nLove: ${data.l.toFixed(2)}\\nJustice: ${data.j.toFixed(2)}\\nPower: ${data.p.toFixed(2)}\\nWisdom: ${data.w.toFixed(2)}\\n\\nMass: ${data.mass.toFixed(1)}\\nHarmony: ${(data.harmony*100).toFixed(0)}%\\nDominant: ${data.dominant}\\nSecurity: ${data.posture}`);
        }

        function showHelp() {
            document.getElementById('helpModal').classList.add('active');
        }

        function closeModal(id) {
            document.getElementById(id).classList.remove('active');
        }

        function showToast(message) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 3000);
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

            switch(e.key.toLowerCase()) {
                case 't': toggleTheme(); break;
                case 'f': document.documentElement.requestFullscreen(); break;
                case 'i': importData(); break;
                case 'e': exportReport(); break;
                case 'r': resetFilters(); break;
                case '?': showHelp(); break;
            }
        });

        // Close modals on outside click
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('active');
                }
            });
        });
    </script>
</body>
</html>
"""

    def generate_dashboard(self, profiles: List[Any], output_file: str = "dashboard.html"):
        """
        Generate fully self-contained HTML dashboard from profiles.

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
