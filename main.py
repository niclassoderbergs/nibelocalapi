import json
import pandas as pd
from datetime import datetime
from io import BytesIO
from flask import Flask, render_template, request, jsonify, send_file
from flask_apscheduler import APScheduler
from api_handler import APIHandler
import db_handler as db
import utils

app = Flask(__name__)
scheduler = APScheduler()

# Ladda konfig
with open('main/config.json') as f:
    config = json.load(f)

api = APIHandler(config)

def background_logger():
    try:
        data = api.get_all_points()
        for pid, p in data.items():
            if isinstance(p, dict):
                m = p.get('metadata', {})
                v = p.get('value') or p.get('datavalue') or {}
                val = v.get('integerValue', 0) / (m.get('divisor', 1) or 1)
                db.save_value(int(pid), val)
    except Exception as e:
        print(f"Loggningsfel: {e}")

@app.route('/')
def index():
    try:
        raw_data = api.get_all_points()
        points = []
        for pid, d in raw_data.items():
            if not isinstance(d, dict): continue
            points.append({
                "id": pid, 
                "title": d.get('title'), 
                "unit": d.get('metadata', {}).get('unit'),
                "writable": d.get('metadata', {}).get('isWritable'),
                "display": utils.format_display_value(d), 
                "raw": d
            })
        return render_template('index.html', points=points, config=config)
    except Exception as e:
        return f"Kunde inte ladda sidan: {e}"

@app.route('/get_point/<int:pid>')
def get_point(pid):
    data = api.get_point(pid)
    if data:
        return jsonify({
            "display": utils.format_display_value(data),
            "raw": data
        })
    return jsonify({"error": "Ej hittad"}), 404

@app.route('/get_history/<int:pid>')
def get_history(pid):
    return jsonify(db.get_history(pid))

@app.route('/update', methods=['POST'])
def update():
    req = request.json
    success = api.update_point(req['pid'], req['raw_val'])
    return "OK" if success else ("Error", 400)

@app.route('/export')
def export():
    try:
        raw_data = api.get_all_points()
        rows = []
        for pid, d in raw_data.items():
            if not isinstance(d, dict): continue
            m = d.get('metadata', {})
            v = d.get('value') or d.get('datavalue') or {}
            div = m.get('divisor', 1) or 1
            rows.append({
                "ID": pid, "Namn": d.get('title'),
                "Värde": v.get('integerValue', 0) / div,
                "Enhet": m.get('unit'), "Modbus ID": m.get('modbusRegisterID'),
                "Skrivbar": "Ja" if m.get('isWritable') else "Nej"
            })
        
        df = pd.DataFrame(rows)
        out = BytesIO()
        with pd.ExcelWriter(out, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Systemdata')
        out.seek(0)
        return send_file(out, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                         as_attachment=True, download_name=f"export_{datetime.now().strftime('%Y%m%d')}.xlsx")
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    db.init_db()
    scheduler.add_job(id='log', func=background_logger, trigger='interval', minutes=3)
    scheduler.start()
    app.run(debug=False, port=5000, use_reloader=False)