"""
Mass Distribution Chart Generator

Generates comprehensive, self-contained mass distribution visualizations with:
- Statistical analysis (mean, median, std dev, quartiles)
- Outlier detection and highlighting
- Correlation analysis (mass vs harmony)
- Distribution categorization
- Interactive filtering
- Recommendations engine
- Export capabilities (data, charts, reports)
- Theme customization
- Advanced analytics
"""

import json
import os
from typing import List, Dict, Any

class MassDistributionChartGenerator:
    """Generates fully interactive mass distribution analytics"""

    def __init__(self):
        self.template = """
<!DOCTYPE html>
<html>
<head>
    <title>Semantic Mass Distribution Analysis</title>
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
            font-family: 'Segoe UI', sans-serif;
            transition: all 0.3s;
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
        }

        .container {
            padding: 30px 40px;
            max-width: 1600px;
            margin: 0 auto;
        }

        .toolbar {
            background: var(--bg-secondary);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 25px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }

        .control-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .control-group label {
            font-size: 12px;
            color: var(--text-secondary);
            font-weight: 600;
        }

        input[type="range"], select {
            padding: 8px 12px;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: var(--bg-primary);
            color: var(--text-primary);
            font-size: 13px;
        }

        button {
            padding: 10px 16px;
            border: none;
            border-radius: 8px;
            background: var(--accent);
            color: white;
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        button:hover { opacity: 0.9; transform: scale(1.02); }
        button:active { transform: scale(0.98); }

        button.secondary {
            background: var(--bg-tertiary);
            color: var(--text-primary);
            border: 1px solid var(--border);
        }

        button.small { padding: 6px 12px; font-size: 12px; }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }

        .stat-card {
            background: var(--bg-secondary);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            text-align: center;
        }

        .stat-title {
            font-size: 12px;
            color: var(--text-secondary);
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stat-value {
            font-size: 26px;
            font-weight: bold;
            color: var(--accent);
        }

        .stat-label {
            font-size: 11px;
            color: var(--text-secondary);
            margin-top: 5px;
        }

        .chart-card {
            background: var(--bg-secondary);
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }

        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--border);
        }

        .chart-header h2 {
            margin: 0;
            font-size: 18px;
        }

        .chart-actions {
            display: flex;
            gap: 8px;
        }

        .chart-container {
            min-height: 400px;
            background: var(--bg-primary);
            border-radius: 8px;
            padding: 10px;
        }

        .grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 25px;
        }

        .insights {
            background: var(--bg-secondary);
            padding: 25px;
            border-radius: 12px;
            border-left: 4px solid var(--accent);
            margin-bottom: 25px;
        }

        .insight-item {
            padding: 15px 0;
            border-bottom: 1px solid var(--border);
        }

        .insight-item:last-child { border-bottom: none; }

        .insight-title {
            font-weight: 600;
            color: var(--accent);
            margin-bottom: 8px;
            font-size: 15px;
        }

        .insight-desc {
            color: var(--text-secondary);
            line-height: 1.6;
        }

        .outliers-list {
            background: var(--bg-tertiary);
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }

        .outlier-item {
            padding: 8px 12px;
            background: var(--bg-secondary);
            border-radius: 6px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .outlier-target {
            font-weight: 600;
            color: var(--accent);
        }

        .outlier-mass {
            color: var(--danger);
            font-weight: bold;
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

        .modal.active { display: flex; }

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
        }

        kbd {
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 3px 7px;
            font-size: 11px;
            font-family: monospace;
        }

        @media (max-width: 768px) {
            .container { padding: 15px; }
            .header { padding: 15px 20px; }
            .toolbar { flex-direction: column; }
            .stats-grid { grid-template-columns: 1fr; }
            .grid-2 { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Semantic Mass Distribution Analysis</h1>
        <div class="header-actions">
            <button onclick="detectOutliers()" class="small">🔍 Detect Outliers</button>
            <button onclick="generateRecommendations()" class="small">💡 Generate Insights</button>
            <button onclick="exportData()" class="secondary small">💾 Export</button>
            <button onclick="toggleTheme()" class="small">🌓</button>
            <button onclick="showHelp()" class="secondary small">❓</button>
        </div>
    </div>

    <div class="container">
        <!-- Toolbar -->
        <div class="toolbar">
            <div class="control-group">
                <label>Min Mass Filter: <span id="mass-filter-val">0</span></label>
                <input type="range" id="mass-filter" min="0" max="100" value="0" step="1" oninput="applyFilters()">
            </div>
            <div class="control-group">
                <label>Category Filter</label>
                <select id="category-filter" onchange="applyFilters()">
                    <option value="all">All Categories</option>
                    <option value="Lightweight">Lightweight (&lt;5)</option>
                    <option value="Medium">Medium (5-20)</option>
                    <option value="Heavyweight">Heavyweight (20-50)</option>
                    <option value="Massive">Massive (≥50)</option>
                </select>
            </div>
            <div class="control-group">
                <label>Harmony Filter</label>
                <select id="harmony-filter" onchange="applyFilters()">
                    <option value="all">All Harmony Levels</option>
                    <option value="high">High (&gt;0.7)</option>
                    <option value="medium">Medium (0.5-0.7)</option>
                    <option value="low">Low (&lt;0.5)</option>
                </select>
            </div>
            <button onclick="resetFilters()" class="secondary">Reset Filters</button>
            <button onclick="calculateStatistics()">Calculate Statistics</button>
        </div>

        <!-- Statistics -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-title">Total Network Mass</div>
                <div class="stat-value" id="stat-total">0.0</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Average Mass</div>
                <div class="stat-value" id="stat-mean">0.0</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Median Mass</div>
                <div class="stat-value" id="stat-median">0.0</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Std Deviation</div>
                <div class="stat-value" id="stat-stddev">0.0</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Max Mass</div>
                <div class="stat-value" id="stat-max">0.0</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Correlation (r)</div>
                <div class="stat-value" id="stat-correlation">0.00</div>
                <div class="stat-label">Mass vs Harmony</div>
            </div>
        </div>

        <!-- Charts -->
        <div class="grid-2">
            <div class="chart-card">
                <div class="chart-header">
                    <h2>📈 Mass Distribution Histogram</h2>
                    <div class="chart-actions">
                        <button onclick="exportChart('histogram')" class="secondary small">Export</button>
                    </div>
                </div>
                <div id="histogram" class="chart-container"></div>
            </div>

            <div class="chart-card">
                <div class="chart-header">
                    <h2>📊 Category Breakdown</h2>
                    <div class="chart-actions">
                        <button onclick="exportChart('categories')" class="secondary small">Export</button>
                    </div>
                </div>
                <div id="categories" class="chart-container"></div>
            </div>
        </div>

        <div class="chart-card">
            <div class="chart-header">
                <h2>🔗 Mass vs Harmony Correlation</h2>
                <div class="chart-actions">
                    <button onclick="exportChart('scatter')" class="secondary small">Export</button>
                </div>
            </div>
            <div id="scatter" class="chart-container"></div>
        </div>

        <div class="chart-card">
            <div class="chart-header">
                <h2>📦 Box Plot Analysis</h2>
                <div class="chart-actions">
                    <button onclick="exportChart('boxplot')" class="secondary small">Export</button>
                </div>
            </div>
            <div id="boxplot" class="chart-container"></div>
        </div>

        <!-- Insights -->
        <div class="insights" id="insights-panel" style="display:none;">
            <h2 style="margin-top:0;">💡 Statistical Insights & Recommendations</h2>
            <div id="insights-content"></div>
        </div>

        <!-- Outliers -->
        <div class="chart-card" id="outliers-panel" style="display:none;">
            <div class="chart-header">
                <h2>🎯 Detected Outliers</h2>
            </div>
            <div id="outliers-content" class="outliers-list"></div>
        </div>
    </div>

    <!-- Help Modal -->
    <div id="helpModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Mass Distribution Help</h3>
                <button class="close-btn" onclick="closeModal('helpModal')">&times;</button>
            </div>
            <h4>Understanding Mass Distribution</h4>
            <p><strong>Semantic Mass</strong> represents system complexity - higher mass indicates more services, connections, and functionality.</p>

            <h4>Categories</h4>
            <p>• <strong>Lightweight (&lt;5):</strong> Simple systems with few services</p>
            <p>• <strong>Medium (5-20):</strong> Moderate complexity</p>
            <p>• <strong>Heavyweight (20-50):</strong> Complex systems</p>
            <p>• <strong>Massive (≥50):</strong> Highly complex infrastructure</p>

            <h4>Statistical Metrics</h4>
            <p>• <strong>Mean:</strong> Average mass across all targets</p>
            <p>• <strong>Median:</strong> Middle value (50th percentile)</p>
            <p>• <strong>Std Deviation:</strong> Spread/variability of mass</p>
            <p>• <strong>Correlation:</strong> Relationship between mass & harmony</p>

            <h4>Features</h4>
            <p>• Filter by mass range, category, or harmony level</p>
            <p>• Detect statistical outliers automatically</p>
            <p>• Generate AI-powered recommendations</p>
            <p>• Export charts and data</p>
            <p>• Interactive visualizations</p>

            <h4>Keyboard Shortcuts</h4>
            <p><kbd>T</kbd> - Toggle theme</p>
            <p><kbd>O</kbd> - Detect outliers</p>
            <p><kbd>I</kbd> - Generate insights</p>
            <p><kbd>E</kbd> - Export data</p>
            <p><kbd>R</kbd> - Reset filters</p>
        </div>
    </div>

    <div class="toast" id="toast"></div>
    <div class="keyboard-hint">Press <kbd>?</kbd> for help</div>

    <script>
        let allData = %DATA%;
        let filteredData = [...allData];
        let statistics = {};

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            updateAll();
        });

        function updateAll() {
            updateStatistics();
            updateCharts();
        }

        function updateStatistics() {
            if (filteredData.length === 0) return;

            const masses = filteredData.map(d => d.mass);

            // Basic stats
            const total = masses.reduce((a, b) => a + b, 0);
            const mean = total / masses.length;
            const sorted = [...masses].sort((a, b) => a - b);
            const median = sorted[Math.floor(sorted.length / 2)];
            const max = Math.max(...masses);

            // Standard deviation
            const variance = masses.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / masses.length;
            const stddev = Math.sqrt(variance);

            // Correlation (mass vs harmony)
            const harmonies = filteredData.map(d => d.harmony);
            const correlation = calculateCorrelation(masses, harmonies);

            // Update displays
            document.getElementById('stat-total').textContent = total.toFixed(1);
            document.getElementById('stat-mean').textContent = mean.toFixed(2);
            document.getElementById('stat-median').textContent = median.toFixed(2);
            document.getElementById('stat-stddev').textContent = stddev.toFixed(2);
            document.getElementById('stat-max').textContent = max.toFixed(1);
            document.getElementById('stat-correlation').textContent = correlation.toFixed(3);

            statistics = {total, mean, median, stddev, max, correlation};
        }

        function calculateCorrelation(x, y) {
            const n = x.length;
            const sumX = x.reduce((a, b) => a + b, 0);
            const sumY = y.reduce((a, b) => a + b, 0);
            const sumXY = x.reduce((sum, xi, i) => sum + xi * y[i], 0);
            const sumX2 = x.reduce((sum, xi) => sum + xi * xi, 0);
            const sumY2 = y.reduce((sum, yi) => sum + yi * yi, 0);

            const numerator = n * sumXY - sumX * sumY;
            const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));

            return denominator === 0 ? 0 : numerator / denominator;
        }

        function updateCharts() {
            updateHistogram();
            updateCategories();
            updateScatter();
            updateBoxPlot();
        }

        function updateHistogram() {
            const trace = {
                x: filteredData.map(d => d.mass),
                type: 'histogram',
                marker: {
                    color: getComputedStyle(document.documentElement).getPropertyValue('--accent'),
                    line: {color: '#fff', width: 1}
                },
                opacity: 0.75
            };

            const layout = {
                margin: {l: 50, r: 30, b: 50, t: 30},
                paper_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                plot_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                font: {color: getComputedStyle(document.body).getPropertyValue('--text-primary')},
                xaxis: {title: 'Semantic Mass', gridcolor: getComputedStyle(document.body).getPropertyValue('--border')},
                yaxis: {title: 'Frequency', gridcolor: getComputedStyle(document.body).getPropertyValue('--border')},
                bargap: 0.05
            };

            Plotly.react('histogram', [trace], layout, {responsive: true});
        }

        function updateCategories() {
            const categories = {'Lightweight': 0, 'Medium': 0, 'Heavyweight': 0, 'Massive': 0};

            filteredData.forEach(d => {
                if (d.mass >= 50) categories['Massive']++;
                else if (d.mass >= 20) categories['Heavyweight']++;
                else if (d.mass >= 5) categories['Medium']++;
                else categories['Lightweight']++;
            });

            const trace = {
                labels: Object.keys(categories),
                values: Object.values(categories),
                type: 'pie',
                marker: {
                    colors: ['#00f260', '#0575E6', '#e100ff', '#ff0000']
                },
                textinfo: 'label+percent',
                hole: 0.4
            };

            const layout = {
                margin: {l: 20, r: 20, b: 20, t: 20},
                paper_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                font: {color: getComputedStyle(document.body).getPropertyValue('--text-primary')},
                showlegend: true,
                legend: {orientation: 'h', y: -0.1}
            };

            Plotly.react('categories', [trace], layout, {responsive: true});
        }

        function updateScatter() {
            const trace = {
                x: filteredData.map(d => d.mass),
                y: filteredData.map(d => d.harmony),
                mode: 'markers',
                type: 'scatter',
                text: filteredData.map(d => d.target),
                marker: {
                    size: 10,
                    color: filteredData.map(d => d.harmony),
                    colorscale: 'Viridis',
                    showscale: true,
                    colorbar: {title: 'Harmony'}
                },
                hovertemplate: '<b>%{text}</b><br>Mass: %{x:.1f}<br>Harmony: %{y:.2f}<extra></extra>'
            };

            const layout = {
                margin: {l: 60, r: 30, b: 50, t: 30},
                paper_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                plot_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                font: {color: getComputedStyle(document.body).getPropertyValue('--text-primary')},
                xaxis: {title: 'Semantic Mass', gridcolor: getComputedStyle(document.body).getPropertyValue('--border')},
                yaxis: {title: 'Harmony Score', range: [0, 1], gridcolor: getComputedStyle(document.body).getPropertyValue('--border')}
            };

            Plotly.react('scatter', [trace], layout, {responsive: true});
        }

        function updateBoxPlot() {
            const trace = {
                y: filteredData.map(d => d.mass),
                type: 'box',
                name: 'Mass Distribution',
                marker: {color: getComputedStyle(document.documentElement).getPropertyValue('--accent')},
                boxmean: 'sd'
            };

            const layout = {
                margin: {l: 60, r: 30, b: 50, t: 30},
                paper_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                plot_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                font: {color: getComputedStyle(document.body).getPropertyValue('--text-primary')},
                yaxis: {title: 'Semantic Mass', gridcolor: getComputedStyle(document.body).getPropertyValue('--border')},
                showlegend: false
            };

            Plotly.react('boxplot', [trace], layout, {responsive: true});
        }

        function applyFilters() {
            const massMin = parseInt(document.getElementById('mass-filter').value);
            const category = document.getElementById('category-filter').value;
            const harmony = document.getElementById('harmony-filter').value;

            document.getElementById('mass-filter-val').textContent = massMin;

            filteredData = allData.filter(d => {
                if (d.mass < massMin) return false;

                if (category !== 'all') {
                    if (category === 'Lightweight' && d.mass >= 5) return false;
                    if (category === 'Medium' && (d.mass < 5 || d.mass >= 20)) return false;
                    if (category === 'Heavyweight' && (d.mass < 20 || d.mass >= 50)) return false;
                    if (category === 'Massive' && d.mass < 50) return false;
                }

                if (harmony !== 'all') {
                    if (harmony === 'high' && d.harmony <= 0.7) return false;
                    if (harmony === 'medium' && (d.harmony < 0.5 || d.harmony > 0.7)) return false;
                    if (harmony === 'low' && d.harmony >= 0.5) return false;
                }

                return true;
            });

            updateAll();
        }

        function resetFilters() {
            document.getElementById('mass-filter').value = 0;
            document.getElementById('category-filter').value = 'all';
            document.getElementById('harmony-filter').value = 'all';
            filteredData = [...allData];
            updateAll();
            showToast('Filters reset');
        }

        function calculateStatistics() {
            if (statistics.mean === undefined) {
                updateStatistics();
            }

            const insights = [];

            insights.push({
                title: `Statistical Summary (n=${filteredData.length})`,
                desc: `Mean: ${statistics.mean.toFixed(2)} | Median: ${statistics.median.toFixed(2)} | Std Dev: ${statistics.stddev.toFixed(2)}`
            });

            // Distribution skew
            if (statistics.mean > statistics.median * 1.2) {
                insights.push({
                    title: 'Right-Skewed Distribution',
                    desc: 'Mean > Median indicates a few high-mass targets pulling the average up. Consider investigating heavyweight systems.'
                });
            } else if (statistics.mean < statistics.median * 0.8) {
                insights.push({
                    title: 'Left-Skewed Distribution',
                    desc: 'Mean < Median indicates most systems have moderate-to-high mass. Network is generally complex.'
                });
            }

            // Correlation interpretation
            if (Math.abs(statistics.correlation) > 0.7) {
                insights.push({
                    title: `Strong Correlation (r=${statistics.correlation.toFixed(3)})`,
                    desc: statistics.correlation > 0 ?
                        'Higher mass strongly correlates with higher harmony - complex systems are well-balanced.' :
                        'Higher mass correlates with lower harmony - complex systems may need optimization.'
                });
            } else if (Math.abs(statistics.correlation) > 0.4) {
                insights.push({
                    title: `Moderate Correlation (r=${statistics.correlation.toFixed(3)})`,
                    desc: 'Some relationship between mass and harmony exists but other factors are also significant.'
                });
            }

            // Variability
            const cv = (statistics.stddev / statistics.mean) * 100;
            if (cv > 50) {
                insights.push({
                    title: 'High Variability Detected',
                    desc: `Coefficient of variation: ${cv.toFixed(1)}%. Network has very diverse mass distribution - consider standardization.`
                });
            }

            if (insights.length > 0) {
                const content = document.getElementById('insights-content');
                content.innerHTML = insights.map(i => `
                    <div class="insight-item">
                        <div class="insight-title">${i.title}</div>
                        <div class="insight-desc">${i.desc}</div>
                    </div>
                `).join('');
                document.getElementById('insights-panel').style.display = 'block';
                showToast('Statistical analysis complete');
            }
        }

        function detectOutliers() {
            if (filteredData.length < 3) {
                showToast('Need at least 3 data points');
                return;
            }

            const masses = filteredData.map(d => d.mass);
            const sorted = [...masses].sort((a, b) => a - b);
            const q1 = sorted[Math.floor(sorted.length * 0.25)];
            const q3 = sorted[Math.floor(sorted.length * 0.75)];
            const iqr = q3 - q1;
            const lowerBound = q1 - 1.5 * iqr;
            const upperBound = q3 + 1.5 * iqr;

            const outliers = filteredData.filter(d => d.mass < lowerBound || d.mass > upperBound);

            if (outliers.length > 0) {
                const content = document.getElementById('outliers-content');
                content.innerHTML = outliers.map(o => `
                    <div class="outlier-item">
                        <span class="outlier-target">${o.target}</span>
                        <span class="outlier-mass">${o.mass.toFixed(1)}</span>
                    </div>
                `).join('');
                document.getElementById('outliers-panel').style.display = 'block';
                showToast(`Found ${outliers.length} outlier(s)`);
            } else {
                showToast('No statistical outliers detected');
            }
        }

        function generateRecommendations() {
            const recommendations = [];

            // High mass targets
            const highMass = filteredData.filter(d => d.mass > statistics.mean + statistics.stddev);
            if (highMass.length > 0) {
                recommendations.push({
                    title: `${highMass.length} High-Complexity Target(s)`,
                    desc: `Consider breaking down or optimizing: ${highMass.map(d => d.target).slice(0, 3).join(', ')}${highMass.length > 3 ? '...' : ''}`
                });
            }

            // Low harmony with high mass
            const problematic = filteredData.filter(d => d.mass > statistics.mean && d.harmony < 0.5);
            if (problematic.length > 0) {
                recommendations.push({
                    title: '⚠️ Complex but Unbalanced Systems',
                    desc: `${problematic.length} target(s) have high mass but low harmony. Priority optimization candidates.`
                });
            }

            // Consolidation opportunity
            const lightweight = filteredData.filter(d => d.mass < 2);
            if (lightweight.length > 3) {
                recommendations.push({
                    title: '💡 Consolidation Opportunity',
                    desc: `${lightweight.length} lightweight targets could potentially be consolidated to reduce infrastructure complexity.`
                });
            }

            if (recommendations.length > 0) {
                const content = document.getElementById('insights-content');
                content.innerHTML = recommendations.map(r => `
                    <div class="insight-item">
                        <div class="insight-title">${r.title}</div>
                        <div class="insight-desc">${r.desc}</div>
                    </div>
                `).join('');
                document.getElementById('insights-panel').style.display = 'block';
                showToast('Recommendations generated');
            } else {
                showToast('Network mass distribution looks optimal!');
            }
        }

        function exportData() {
            const report = {
                generated: new Date().toISOString(),
                statistics: statistics,
                data: filteredData
            };

            const blob = new Blob([JSON.stringify(report, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `mass_analysis_${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            showToast('Data exported!');
        }

        function exportChart(chartId) {
            Plotly.downloadImage(chartId, {
                format: 'png',
                width: 1920,
                height: 1080,
                filename: `mass_${chartId}_${new Date().toISOString().split('T')[0]}`
            });
            showToast('Chart exported!');
        }

        function toggleTheme() {
            document.body.classList.toggle('light-theme');
            updateCharts();
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
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;

            switch(e.key.toLowerCase()) {
                case 't': toggleTheme(); break;
                case 'o': detectOutliers(); break;
                case 'i': generateRecommendations(); break;
                case 'e': exportData(); break;
                case 'r': resetFilters(); break;
                case '?': showHelp(); break;
            }
        });

        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) modal.classList.remove('active');
            });
        });
    </script>
</body>
</html>
"""

    def generate_chart(self, profiles: List[Any], output_file: str = "mass_distribution.html"):
        """
        Generate fully self-contained HTML mass distribution chart from profiles.

        Args:
            profiles: List of semantic profiles (objects or dicts)
            output_file: Path to output HTML file
        """
        data = []
        for p in profiles:
            if isinstance(p, dict):
                target = p.get('target', 'Unknown')
                mass = p.get('semantic_mass', 0.0)
                harmony = p.get('harmony_score', 0.0)
            else:
                target = p.target
                mass = getattr(p, 'semantic_mass', 0.0)
                harmony = p.harmony_score

            data.append({
                'target': target,
                'mass': mass,
                'harmony': harmony
            })

        html_content = self.template.replace('%DATA%', json.dumps(data))

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return os.path.abspath(output_file)
