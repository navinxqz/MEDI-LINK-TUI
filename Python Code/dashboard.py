from flask import Flask, render_template_string, jsonify
import pandas as pd
import os
import socket

app = Flask(__name__)

LOG_FILE = 'patient_log.csv'
COLS = ['Time', 'IDs', 'Meds', 'Status', 'Detail']


def load_log():
    if not os.path.exists(LOG_FILE):
        return pd.DataFrame(columns=COLS)

    try:
        df = pd.read_csv(LOG_FILE, names=COLS)
        return df.tail(200)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame(columns=COLS)


HTML = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Medi-Link Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, sans-serif;
    background: #f8f9fa;
    color: #222;
    padding: 20px;
}

h1 {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 4px;
}

.sub {
    font-size: 13px;
    color: #666;
    margin-bottom: 20px;
}

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
    margin-bottom: 20px;
}

.card {
    background: white;
    border-radius: 10px;
    padding: 14px 16px;
    border: 1px solid #eee;
}

.card-label {
    font-size: 11px;
    color: #888;
    margin-bottom: 4px;
}

.card-val {
    font-size: 26px;
    font-weight: 600;
}

.danger-val {
    color: #dc2626;
}

.safe-val {
    color: #16a34a;
}

.chart-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
}

.chart-wrap {
    background: white;
    border-radius: 10px;
    padding: 16px;
    border: 1px solid #eee;
}

.chart-title {
    font-size: 13px;
    font-weight: 500;
    margin-bottom: 12px;
}

.table-wrap {
    background: white;
    border-radius: 10px;
    padding: 16px;
    border: 1px solid #eee;
    overflow-x: auto;
}

.table-wrap table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
}

.table-wrap th {
    text-align: left;
    padding: 6px 10px;
    border-bottom: 1px solid #eee;
    font-weight: 500;
    color: #555;
    font-size: 11px;
}

.table-wrap td {
    padding: 7px 10px;
    border-bottom: 1px solid #f3f3f3;
}

.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 500;
}

.badge-danger {
    background: #fee2e2;
    color: #991b1b;
}

.badge-safe {
    background: #dcfce7;
    color: #166534;
}

.badge-exp {
    background: #fef9c3;
    color: #854d0e;
}

.refresh {
    font-size: 11px;
    color: #888;
    margin-top: 12px;
}

@media (max-width: 768px) {
    .chart-grid {
        grid-template-columns: 1fr;
    }
}
</style>
</head>

<body>
<h1>Medi-Link TUI 2.0 — Live Dashboard</h1>
<div class="sub">Patient medication monitoring · Auto-refreshes every 5 seconds</div>

<div class="cards">
    <div class="card">
        <div class="card-label">Total events</div>
        <div class="card-val" id="c-total">—</div>
    </div>

    <div class="card">
        <div class="card-label">Danger events</div>
        <div class="card-val danger-val" id="c-danger">—</div>
    </div>

    <div class="card">
        <div class="card-label">Safe events</div>
        <div class="card-val safe-val" id="c-safe">—</div>
    </div>

    <div class="card">
        <div class="card-label">Expired alerts</div>
        <div class="card-val" id="c-exp">—</div>
    </div>

    <div class="card">
        <div class="card-label">Last event</div>
        <div class="card-val" id="c-last" style="font-size:13px;margin-top:4px">—</div>
    </div>
</div>

<div class="chart-grid">
    <div class="chart-wrap">
        <div class="chart-title">Status breakdown</div>
        <canvas id="pie" height="180"></canvas>
    </div>

    <div class="chart-wrap">
        <div class="chart-title">Most detected medicines</div>
        <canvas id="bar" height="180"></canvas>
    </div>
</div>

<div class="table-wrap">
    <div class="chart-title">Recent events (last 20)</div>

    <table>
        <thead>
            <tr>
                <th>Time</th>
                <th>Medicines</th>
                <th>Status</th>
                <th>Detail</th>
            </tr>
        </thead>

        <tbody id="t-body"></tbody>
    </table>
</div>

<div class="refresh" id="last-refresh"></div>

<script>
let pieChart;
let barChart;

async function refresh() {
    try {
        const response = await fetch('/api/data');
        const d = await response.json();

        document.getElementById('c-total').textContent = d.total;
        document.getElementById('c-danger').textContent = d.danger;
        document.getElementById('c-safe').textContent = d.safe;
        document.getElementById('c-exp').textContent = d.expired;
        document.getElementById('c-last').textContent = d.last_time || 'No data';

        // Pie Chart
        if (!pieChart) {
            pieChart = new Chart(document.getElementById('pie'), {
                type: 'doughnut',
                data: {
                    labels: ['Safe', 'Danger', 'Expired'],
                    datasets: [{
                        data: [d.safe, d.danger, d.expired],
                        backgroundColor: ['#86efac', '#fca5a5', '#fde68a'],
                        borderWidth: 0
                    }]
                },
                options: {
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                font: {
                                    size: 11
                                },
                                boxWidth: 12
                            }
                        }
                    }
                }
            });
        } else {
            pieChart.data.datasets[0].data = [d.safe, d.danger, d.expired];
            pieChart.update();
        }

        // Medicine Bar Chart
        const medLabels = Object.keys(d.med_counts);
        const medVals = Object.values(d.med_counts);

        if (!barChart) {
            barChart = new Chart(document.getElementById('bar'), {
                type: 'bar',
                data: {
                    labels: medLabels,
                    datasets: [{
                        data: medVals,
                        backgroundColor: '#a5b4fc',
                        borderRadius: 4,
                        borderWidth: 0
                    }]
                },
                options: {
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            ticks: {
                                stepSize: 1,
                                font: {
                                    size: 11
                                }
                            }
                        },
                        x: {
                            ticks: {
                                font: {
                                    size: 11
                                }
                            }
                        }
                    }
                }
            });
        } else {
            barChart.data.labels = medLabels;
            barChart.data.datasets[0].data = medVals;
            barChart.update();
        }

        // Table
        const tbody = document.getElementById('t-body');

        tbody.innerHTML = d.recent.slice().reverse().map(row => {
            const cls = row.Status === 'DANGER'
                ? 'badge-danger'
                : row.Status === 'EXPIRED'
                ? 'badge-exp'
                : 'badge-safe';

            return `
                <tr>
                    <td>${row.Time}</td>
                    <td>${row.Meds || '—'}</td>
                    <td><span class="badge ${cls}">${row.Status}</span></td>
                    <td>${row.Detail || '—'}</td>
                </tr>
            `;
        }).join('');

        document.getElementById('last-refresh').textContent =
            'Last updated: ' + new Date().toLocaleTimeString();

    } catch (err) {
        console.error('Dashboard refresh error:', err);
    }
}

refresh();
setInterval(refresh, 5000);
</script>
</body>
</html>
'''


@app.route('/api/data')
def api_data():
    df = load_log()

    if df.empty:
        return jsonify({
            'total': 0,
            'danger': 0,
            'safe': 0,
            'expired': 0,
            'last_time': '',
            'med_counts': {},
            'recent': []
        })

    med_counts = {}

    for meds in df['Meds'].dropna():
        for m in str(meds).split(','):
            m = m.strip()
            if m:
                med_counts[m] = med_counts.get(m, 0) + 1

    return jsonify({
        'total': len(df),
        'danger': int((df['Status'] == 'DANGER').sum()),
        'safe': int((df['Status'] == 'SAFE').sum()),
        'expired': int((df['Status'] == 'EXPIRED').sum()),
        'last_time': str(df['Time'].iloc[-1]),
        'med_counts': med_counts,
        'recent': df.tail(20).to_dict('records')
    })


@app.route('/')
def index():
    return render_template_string(HTML)


if __name__ == '__main__':
    print('Dashboard running at: http://localhost:5000')
    print('On your phone (same WiFi) open:')

    try:
        ip = socket.gethostbyname(socket.gethostname())
        print(f'  http://{ip}:5000')
    except:
        print('  Unable to detect local IP')

    app.run(host='0.0.0.0', port=5000, debug=False)
