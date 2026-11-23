import os
import time
import logging
from collections import deque
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)
STARTED_AT = time.time()
LOGS = deque(maxlen=100)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("render-panel")

def add_log(message):
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    LOGS.appendleft({"time": stamp, "message": message})

add_log("Dashboard initialized.")

PAGE = r"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nemesis • Control Panel</title>
<style>
:root{--bg:#08070d;--card:#12101c;--line:#29213c;--purple:#9b5cff;--pink:#df65ff;--muted:#a49bb7;--green:#4ade80}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at top,#24113d 0%,#0b0812 42%,var(--bg) 78%);color:#f5f1ff;font-family:Inter,system-ui,Arial,sans-serif;min-height:100vh}
.wrap{max-width:1050px;margin:auto;padding:34px 20px}.top{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:28px}
.brand{font-size:23px;font-weight:800;letter-spacing:1px}.brand span{color:var(--pink)}.pill{border:1px solid #345b45;color:var(--green);background:#102319;padding:8px 13px;border-radius:30px;font-size:12px}
h1{font-size:clamp(28px,5vw,42px);margin:0 0 8px}.sub{color:var(--muted);margin:0 0 26px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.card{background:linear-gradient(145deg,#171323,#100e18);border:1px solid var(--line);border-radius:18px;padding:21px;box-shadow:0 12px 35px #0005}
.label{color:var(--muted);font-size:13px}.value{font-size:28px;font-weight:750;margin-top:10px}.accent{color:var(--pink)}
.section{margin-top:18px}.section h2{font-size:17px;margin:0 0 14px}.logs{max-height:320px;overflow:auto}.log{padding:12px 0;border-bottom:1px solid #29213c;font-size:13px}.time{color:var(--purple);margin-right:10px}.empty{color:var(--muted)}
.foot{color:#766d89;font-size:12px;margin-top:22px;text-align:center}
@media(max-width:700px){.grid{grid-template-columns:1fr}.top{align-items:flex-start;flex-direction:column}.value{font-size:25px}}
</style>
</head>
<body><main class="wrap">
<div class="top"><div class="brand">NEMESIS <span>CONTROL</span></div><div class="pill">● WEB SERVICE ONLINE</div></div>
<h1>Dashboard Overview</h1><p class="sub">Render service status and runtime information.</p>
<div class="grid">
 <div class="card"><div class="label">Service status</div><div class="value accent" id="status">ONLINE</div></div>
 <div class="card"><div class="label">Uptime</div><div class="value" id="uptime">—</div></div>
 <div class="card"><div class="label">Server time</div><div class="value" id="clock">—</div></div>
</div>
<div class="card section"><h2>Recent activity</h2><div class="logs" id="logs"><div class="empty">Loading activity…</div></div></div>
<div class="foot">Dark Panel • Flask • Render</div>
</main>
<script>
function duration(s){s=Math.max(0,Math.floor(s));let d=Math.floor(s/86400);s%=86400;let h=Math.floor(s/3600);s%=3600;let m=Math.floor(s/60);let sec=s%60;return `${d}d ${h}h ${m}m ${sec}s`}
async function refresh(){try{const r=await fetch('/api/status');const d=await r.json();document.getElementById('status').textContent=d.status;document.getElementById('uptime').textContent=duration(d.uptime_seconds);document.getElementById('clock').textContent=d.server_time;const box=document.getElementById('logs');box.innerHTML=d.logs.length?d.logs.map(x=>`<div class="log"><span class="time">${x.time}</span>${x.message}</div>`).join(''):'<div class="empty">No activity yet.</div>';}catch(e){document.getElementById('status').textContent='CHECKING';}}
refresh();setInterval(refresh,5000);
</script>
</body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "nemesis-panel"}), 200

@app.get("/api/status")
def status():
    return jsonify({
        "status": "ONLINE",
        "uptime_seconds": int(time.time() - STARTED_AT),
        "server_time": datetime.now(timezone.utc).strftime("%H:%M:%S UTC"),
        "logs": list(LOGS)
    })

@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
