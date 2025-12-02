"""
Drift Timeline Generator

Generates comprehensive, self-contained drift timeline visualizations with:
- Date range selection and zoom
- Statistical overlays (trends, averages, std dev)
- Change rate calculations
- Baseline comparison
- Alert thresholds
- Annotations for significant events
- Export capabilities (data, images, reports)
- Theme customization
- Interactive analysis tools
"""

import json
import os
from typing import List, Dict, Any
from datetime import datetime

class DriftTimelineGenerator:
    """Generates fully interactive drift timelines"""

    def __init__(self):
        self.template = """
<!DOCTYPE html>
<html>
<head>
    <title>Drift Timeline: %TARGET%</title>
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
            --love: #ff0055;
            --justice: #00ccff;
            --power: #ffaa00;
            --wisdom: #aa00ff;
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

        input[type="date"], select {
            padding: 8px 12px;
            border: 1px solid var(--border);
            border-radius: 6px;
            background: var(--bg-primary);
            color: var(--text-primary);
            font-size: 13px;
        }

        button, .btn {
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
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }

        .stat-card {
            background: var(--bg-secondary);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }

        .stat-title {
            font-size: 13px;
            color: var(--text-secondary);
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stat-value {
            font-size: 28px;
            font-weight: bold;
            color: var(--accent);
        }

        .stat-change {
            font-size: 13px;
            margin-top: 5px;
        }

        .stat-change.positive { color: var(--success); }
        .stat-change.negative { color: var(--danger); }

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
            color: var(--text-primary);
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

        .insights {
            background: var(--bg-secondary);
            padding: 25px;
            border-radius: 12px;
            border-left: 4px solid var(--accent);
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

        .legend {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            padding: 15px;
            background: var(--bg-tertiary);
            border-radius: 8px;
            margin-bottom: 20px;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
        }

        .legend-color {
            width: 20px;
            height: 3px;
            border-radius: 2px;
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

        .annotation-list {
            max-height: 300px;
            overflow-y: auto;
        }

        .annotation-item {
            background: var(--bg-tertiary);
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 10px;
        }

        .annotation-date {
            font-size: 12px;
            color: var(--text-secondary);
            margin-bottom: 5px;
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

        .form-group input, .form-group textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: var(--bg-primary);
            color: var(--text-primary);
            font-family: inherit;
        }

        .form-group textarea {
            min-height: 80px;
            resize: vertical;
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
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📈 Drift Timeline: <span style="color: var(--accent-secondary);">%TARGET%</span></h1>
        <div class="header-actions">
            <button onclick="addAnnotation()" class="secondary small">📝 Add Note</button>
            <button onclick="exportData()" class="small">💾 Export Data</button>
            <button onclick="generateReport()" class="small">📊 Generate Report</button>
            <button onclick="toggleTheme()" class="small" title="Toggle Theme">🌓</button>
            <button onclick="showHelp()" class="secondary small">❓</button>
        </div>
    </div>

    <div class="container">
        <!-- Toolbar -->
        <div class="toolbar">
            <div class="control-group">
                <label>Start Date</label>
                <input type="date" id="date-start" onchange="applyDateFilter()">
            </div>
            <div class="control-group">
                <label>End Date</label>
                <input type="date" id="date-end" onchange="applyDateFilter()">
            </div>
            <div class="control-group">
                <label>View Mode</label>
                <select id="view-mode" onchange="updateCharts()">
                    <option value="all">All Dimensions</option>
                    <option value="ljpw">LJPW Only</option>
                    <option value="mass">Mass Only</option>
                    <option value="harmony">Harmony Only</option>
                </select>
            </div>
            <div class="control-group">
                <label>Analysis</label>
                <select id="analysis-mode" onchange="updateCharts()">
                    <option value="none">Raw Data</option>
                    <option value="trend">+ Trend Lines</option>
                    <option value="average">+ Moving Average</option>
                    <option value="all">+ All Overlays</option>
                </select>
            </div>
            <button onclick="resetFilters()" class="secondary">Reset</button>
            <button onclick="calculateDriftRate()">Calculate Drift Rate</button>
        </div>

        <!-- Statistics -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-title">Data Points</div>
                <div class="stat-value" id="stat-points">0</div>
                <div class="stat-change" id="stat-points-change"></div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Time Span</div>
                <div class="stat-value" id="stat-timespan">0 days</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Avg Drift Velocity</div>
                <div class="stat-value" id="stat-velocity">0.00</div>
                <div class="stat-change" id="stat-velocity-desc">per day</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Total Drift</div>
                <div class="stat-value" id="stat-drift">0.00</div>
                <div class="stat-change" id="stat-drift-severity"></div>
            </div>
        </div>

        <!-- Legend -->
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background: var(--love);"></div>
                <span>Love (Connectivity)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: var(--justice);"></div>
                <span>Justice (Security)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: var(--power);"></div>
                <span>Power (Performance)</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: var(--wisdom);"></div>
                <span>Wisdom (Visibility)</span>
            </div>
        </div>

        <!-- LJPW Chart -->
        <div class="chart-card">
            <div class="chart-header">
                <h2>🎯 LJPW Dimensions Over Time</h2>
                <div class="chart-actions">
                    <button onclick="resetZoom('ljpw')" class="secondary small">Reset Zoom</button>
                    <button onclick="exportChart('ljpw')" class="secondary small">Export</button>
                </div>
            </div>
            <div id="ljpw-chart" class="chart-container"></div>
        </div>

        <!-- Mass Chart -->
        <div class="chart-card">
            <div class="chart-header">
                <h2>⚖️ Semantic Mass Over Time</h2>
                <div class="chart-actions">
                    <button onclick="resetZoom('mass')" class="secondary small">Reset Zoom</button>
                    <button onclick="exportChart('mass')" class="secondary small">Export</button>
                </div>
            </div>
            <div id="mass-chart" class="chart-container"></div>
        </div>

        <!-- Harmony Chart -->
        <div class="chart-card">
            <div class="chart-header">
                <h2>🎵 Harmony Score Over Time</h2>
                <div class="chart-actions">
                    <button onclick="resetZoom('harmony')" class="secondary small">Reset Zoom</button>
                    <button onclick="exportChart('harmony')" class="secondary small">Export</button>
                </div>
            </div>
            <div id="harmony-chart" class="chart-container"></div>
        </div>

        <!-- Insights -->
        <div class="insights" id="insights-panel" style="display:none;">
            <h2 style="margin-top:0;">💡 Drift Analysis & Insights</h2>
            <div id="insights-content"></div>
        </div>
    </div>

    <!-- Annotation Modal -->
    <div id="annotationModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Add Annotation</h3>
                <button class="close-btn" onclick="closeModal('annotationModal')">&times;</button>
            </div>
            <div class="form-group">
                <label>Date</label>
                <input type="date" id="annotation-date">
            </div>
            <div class="form-group">
                <label>Note</label>
                <textarea id="annotation-text" placeholder="Describe what happened at this point..."></textarea>
            </div>
            <button onclick="saveAnnotation()">Save Annotation</button>
            <button onclick="closeModal('annotationModal')" class="secondary">Cancel</button>

            <h4 style="margin-top: 30px;">Existing Annotations</h4>
            <div class="annotation-list" id="annotation-list"></div>
        </div>
    </div>

    <!-- Help Modal -->
    <div id="helpModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Drift Timeline Help</h3>
                <button class="close-btn" onclick="closeModal('helpModal')">&times;</button>
            </div>
            <h4>Features</h4>
            <p>• <strong>Date Range:</strong> Filter data by selecting start and end dates</p>
            <p>• <strong>View Modes:</strong> Focus on specific metrics or view all</p>
            <p>• <strong>Analysis Overlays:</strong> Add trend lines and moving averages</p>
            <p>• <strong>Annotations:</strong> Mark significant events on the timeline</p>
            <p>• <strong>Drift Rate:</strong> Calculate velocity of changes</p>
            <p>• <strong>Export:</strong> Save charts and data for reports</p>

            <h4>Keyboard Shortcuts</h4>
            <p><kbd>T</kbd> - Toggle theme</p>
            <p><kbd>A</kbd> - Add annotation</p>
            <p><kbd>E</kbd> - Export data</p>
            <p><kbd>R</kbd> - Reset filters</p>
            <p><kbd>?</kbd> - Show this help</p>

            <h4>Understanding Drift</h4>
            <p><strong>Drift Velocity:</strong> Rate of change per day</p>
            <p><strong>Total Drift:</strong> Cumulative distance from baseline</p>
            <p><strong>Severity Levels:</strong></p>
            <p>&nbsp;&nbsp;• Low (&lt;0.2): Normal variance</p>
            <p>&nbsp;&nbsp;• Medium (0.2-0.5): Notable changes</p>
            <p>&nbsp;&nbsp;• High (&gt;0.5): Significant drift</p>
        </div>
    </div>

    <div class="toast" id="toast"></div>
    <div class="keyboard-hint">Press <kbd>?</kbd> for help</div>

    <script>
        const TARGET = '%TARGET%';
        let allData = %DATA%;
        let filteredData = [...allData];
        let annotations = JSON.parse(localStorage.getItem('annotations-' + TARGET) || '[]');

        // Parse dates
        allData.forEach(d => {
            d.date = new Date(d.timestamp);
        });
        filteredData = [...allData];

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            initializeDateFilters();
            updateAll();
            loadAnnotations();
        });

        function initializeDateFilters() {
            if (allData.length > 0) {
                const dates = allData.map(d => d.date);
                const minDate = new Date(Math.min(...dates));
                const maxDate = new Date(Math.max(...dates));

                document.getElementById('date-start').valueAsDate = minDate;
                document.getElementById('date-end').valueAsDate = maxDate;
            }
        }

        function updateAll() {
            updateStats();
            updateCharts();
        }

        function updateStats() {
            document.getElementById('stat-points').textContent = filteredData.length;

            if (filteredData.length >= 2) {
                const dates = filteredData.map(d => d.date);
                const minDate = Math.min(...dates);
                const maxDate = Math.max(...dates);
                const daysDiff = (maxDate - minDate) / (1000 * 60 * 60 * 24);
                document.getElementById('stat-timespan').textContent = Math.round(daysDiff) + ' days';

                // Calculate drift
                const first = filteredData[0];
                const last = filteredData[filteredData.length - 1];
                const drift = Math.sqrt(
                    Math.pow(last.love - first.love, 2) +
                    Math.pow(last.justice - first.justice, 2) +
                    Math.pow(last.power - first.power, 2) +
                    Math.pow(last.wisdom - first.wisdom, 2)
                );

                document.getElementById('stat-drift').textContent = drift.toFixed(3);

                const velocity = daysDiff > 0 ? drift / daysDiff : 0;
                document.getElementById('stat-velocity').textContent = velocity.toFixed(4);

                // Severity
                let severity = 'Low (Normal)';
                if (drift > 0.5) severity = 'High (Significant)';
                else if (drift > 0.2) severity = 'Medium (Notable)';
                document.getElementById('stat-drift-severity').textContent = severity;
                document.getElementById('stat-drift-severity').className = 'stat-change ' +
                    (drift > 0.5 ? 'negative' : drift > 0.2 ? '' : 'positive');
            }
        }

        function updateCharts() {
            const viewMode = document.getElementById('view-mode').value;
            const analysisMode = document.getElementById('analysis-mode').value;

            if (viewMode === 'all' || viewMode === 'ljpw') {
                updateLJPWChart(analysisMode);
            }
            if (viewMode === 'all' || viewMode === 'mass') {
                updateMassChart(analysisMode);
            }
            if (viewMode === 'all' || viewMode === 'harmony') {
                updateHarmonyChart(analysisMode);
            }
        }

        function updateLJPWChart(analysisMode) {
            const timestamps = filteredData.map(d => d.timestamp);

            const traces = [
                {
                    x: timestamps,
                    y: filteredData.map(d => d.love),
                    name: 'Love',
                    type: 'scatter',
                    line: {color: 'var(--love)', width: 2}
                },
                {
                    x: timestamps,
                    y: filteredData.map(d => d.justice),
                    name: 'Justice',
                    type: 'scatter',
                    line: {color: 'var(--justice)', width: 2}
                },
                {
                    x: timestamps,
                    y: filteredData.map(d => d.power),
                    name: 'Power',
                    type: 'scatter',
                    line: {color: 'var(--power)', width: 2}
                },
                {
                    x: timestamps,
                    y: filteredData.map(d => d.wisdom),
                    name: 'Wisdom',
                    type: 'scatter',
                    line: {color: 'var(--wisdom)', width: 2}
                }
            ];

            // Add trend lines if requested
            if (analysisMode === 'trend' || analysisMode === 'all') {
                ['love', 'justice', 'power', 'wisdom'].forEach((dim, i) => {
                    const values = filteredData.map(d => d[dim]);
                    const trend = calculateTrend(values);
                    traces.push({
                        x: timestamps,
                        y: trend,
                        name: dim + ' trend',
                        type: 'scatter',
                        line: {color: traces[i].line.color, dash: 'dash', width: 1},
                        showlegend: false
                    });
                });
            }

            const layout = {
                margin: {l: 60, r: 30, b: 50, t: 30},
                paper_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                plot_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                font: {color: getComputedStyle(document.body).getPropertyValue('--text-primary')},
                xaxis: {
                    title: 'Time',
                    gridcolor: getComputedStyle(document.body).getPropertyValue('--border')
                },
                yaxis: {
                    title: 'Score',
                    range: [0, 1],
                    gridcolor: getComputedStyle(document.body).getPropertyValue('--border')
                },
                hovermode: 'x unified',
                legend: {orientation: 'h', y: -0.2}
            };

            // Add annotation shapes
            const shapes = annotations
                .filter(a => {
                    const aDate = new Date(a.date);
                    return filteredData.some(d => Math.abs(d.date - aDate) < 86400000);
                })
                .map(a => ({
                    type: 'line',
                    x0: a.date,
                    x1: a.date,
                    y0: 0,
                    y1: 1,
                    line: {
                        color: 'var(--accent)',
                        width: 2,
                        dash: 'dot'
                    }
                }));

            layout.shapes = shapes;

            Plotly.react('ljpw-chart', traces, layout, {responsive: true});
        }

        function updateMassChart(analysisMode) {
            const timestamps = filteredData.map(d => d.timestamp);

            const trace = {
                x: timestamps,
                y: filteredData.map(d => d.mass),
                name: 'Semantic Mass',
                type: 'scatter',
                fill: 'tozeroy',
                fillcolor: 'rgba(0, 242, 96, 0.2)',
                line: {color: 'var(--success)', width: 2}
            };

            const layout = {
                margin: {l: 60, r: 30, b: 50, t: 30},
                paper_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                plot_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                font: {color: getComputedStyle(document.body).getPropertyValue('--text-primary')},
                xaxis: {
                    title: 'Time',
                    gridcolor: getComputedStyle(document.body).getPropertyValue('--border')
                },
                yaxis: {
                    title: 'Mass',
                    gridcolor: getComputedStyle(document.body).getPropertyValue('--border')
                }
            };

            Plotly.react('mass-chart', [trace], layout, {responsive: true});
        }

        function updateHarmonyChart(analysisMode) {
            const timestamps = filteredData.map(d => d.timestamp);

            const trace = {
                x: timestamps,
                y: filteredData.map(d => d.harmony),
                name: 'Harmony Score',
                type: 'scatter',
                line: {color: 'var(--accent)', width: 2, dash: 'dot'}
            };

            const layout = {
                margin: {l: 60, r: 30, b: 50, t: 30},
                paper_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                plot_bgcolor: getComputedStyle(document.body).getPropertyValue('--bg-primary'),
                font: {color: getComputedStyle(document.body).getPropertyValue('--text-primary')},
                xaxis: {
                    title: 'Time',
                    gridcolor: getComputedStyle(document.body).getPropertyValue('--border')
                },
                yaxis: {
                    title: 'Score',
                    range: [0, 1],
                    gridcolor: getComputedStyle(document.body).getPropertyValue('--border')
                }
            };

            Plotly.react('harmony-chart', [trace], layout, {responsive: true});
        }

        function calculateTrend(values) {
            const n = values.length;
            const indices = Array.from({length: n}, (_, i) => i);
            const sumX = indices.reduce((a, b) => a + b, 0);
            const sumY = values.reduce((a, b) => a + b, 0);
            const sumXY = indices.reduce((sum, x, i) => sum + x * values[i], 0);
            const sumX2 = indices.reduce((sum, x) => sum + x * x, 0);

            const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
            const intercept = (sumY - slope * sumX) / n;

            return indices.map(x => slope * x + intercept);
        }

        function applyDateFilter() {
            const startDate = document.getElementById('date-start').valueAsDate;
            const endDate = document.getElementById('date-end').valueAsDate;

            if (startDate && endDate) {
                filteredData = allData.filter(d =>
                    d.date >= startDate && d.date <= endDate
                );
                updateAll();
            }
        }

        function resetFilters() {
            initializeDateFilters();
            document.getElementById('view-mode').value = 'all';
            document.getElementById('analysis-mode').value = 'none';
            filteredData = [...allData];
            updateAll();
            showToast('Filters reset');
        }

        function calculateDriftRate() {
            if (filteredData.length < 2) {
                showToast('Need at least 2 data points');
                return;
            }

            const insights = [];

            // Calculate dimension-specific drift
            ['love', 'justice', 'power', 'wisdom'].forEach(dim => {
                const first = filteredData[0][dim];
                const last = filteredData[filteredData.length - 1][dim];
                const change = last - first;
                const absChange = Math.abs(change);

                if (absChange > 0.1) {
                    insights.push({
                        title: `${dim.charAt(0).toUpperCase() + dim.slice(1)} Drift: ${change > 0 ? '+' : ''}${(change * 100).toFixed(1)}%`,
                        desc: `${dim} has ${change > 0 ? 'increased' : 'decreased'} by ${(absChange * 100).toFixed(1)}% over the period.`
                    });
                }
            });

            // Mass change
            const massChange = filteredData[filteredData.length - 1].mass - filteredData[0].mass;
            if (Math.abs(massChange) > 1) {
                insights.push({
                    title: `Mass Change: ${massChange > 0 ? '+' : ''}${massChange.toFixed(1)}`,
                    desc: `Semantic mass has ${massChange > 0 ? 'increased' : 'decreased'}, indicating ${massChange > 0 ? 'more' : 'less'} system complexity.`
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
                showToast('Drift analysis complete');
            } else {
                showToast('No significant drift detected');
            }
        }

        function addAnnotation() {
            document.getElementById('annotationModal').classList.add('active');
            if (filteredData.length > 0) {
                const midDate = filteredData[Math.floor(filteredData.length / 2)].date;
                document.getElementById('annotation-date').valueAsDate = midDate;
            }
        }

        function saveAnnotation() {
            const date = document.getElementById('annotation-date').value;
            const text = document.getElementById('annotation-text').value;

            if (date && text) {
                annotations.push({date, text});
                localStorage.setItem('annotations-' + TARGET, JSON.stringify(annotations));
                loadAnnotations();
                updateCharts();
                closeModal('annotationModal');
                showToast('Annotation saved');
            }
        }

        function loadAnnotations() {
            const list = document.getElementById('annotation-list');
            list.innerHTML = annotations.map((a, i) => `
                <div class="annotation-item">
                    <div class="annotation-date">${new Date(a.date).toLocaleDateString()}</div>
                    <div>${a.text}</div>
                    <button onclick="deleteAnnotation(${i})" class="small secondary" style="margin-top:8px;">Delete</button>
                </div>
            `).join('') || '<p style="text-align:center;color:var(--text-secondary);">No annotations yet</p>';
        }

        function deleteAnnotation(index) {
            annotations.splice(index, 1);
            localStorage.setItem('annotations-' + TARGET, JSON.stringify(annotations));
            loadAnnotations();
            updateCharts();
            showToast('Annotation deleted');
        }

        function exportData() {
            const report = {
                target: TARGET,
                generated: new Date().toISOString(),
                timespan: {
                    start: filteredData[0]?.timestamp,
                    end: filteredData[filteredData.length - 1]?.timestamp
                },
                data: filteredData,
                annotations: annotations
            };

            const blob = new Blob([JSON.stringify(report, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `drift_${TARGET}_${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            showToast('Data exported!');
        }

        function generateReport() {
            const report = {
                target: TARGET,
                generated: new Date().toISOString(),
                summary: {
                    dataPoints: filteredData.length,
                    timespan: document.getElementById('stat-timespan').textContent,
                    totalDrift: document.getElementById('stat-drift').textContent,
                    velocity: document.getElementById('stat-velocity').textContent
                },
                data: filteredData
            };

            const blob = new Blob([JSON.stringify(report, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `drift_report_${TARGET}_${new Date().toISOString().split('T')[0]}.json`;
            a.click();
            showToast('Report generated!');
        }

        function exportChart(chartId) {
            Plotly.downloadImage(chartId + '-chart', {
                format: 'png',
                width: 1920,
                height: 1080,
                filename: `${TARGET}_${chartId}_${new Date().toISOString().split('T')[0]}`
            });
            showToast('Chart exported!');
        }

        function resetZoom(chartId) {
            Plotly.relayout(chartId + '-chart', {
                'xaxis.autorange': true,
                'yaxis.autorange': true
            });
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
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

            switch(e.key.toLowerCase()) {
                case 't': toggleTheme(); break;
                case 'a': addAnnotation(); break;
                case 'e': exportData(); break;
                case 'r': resetFilters(); break;
                case '?': showHelp(); break;
            }
        });

        // Close modals on outside click
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) modal.classList.remove('active');
            });
        });
    </script>
</body>
</html>
"""

    def generate_timeline(self, target: str, profiles: List[Any], output_file: str = None):
        """
        Generate fully self-contained HTML drift timeline from profile history.

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

        # Sort by timestamp
        data.sort(key=lambda x: x['timestamp'])

        html_content = self.template.replace('%DATA%', json.dumps(data))
        html_content = html_content.replace('%TARGET%', target)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return os.path.abspath(output_file)
