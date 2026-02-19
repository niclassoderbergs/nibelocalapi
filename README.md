# Nibe S1256 Expert Interface 🌡️

A professional, Flask-based web interface designed for real-time monitoring and advanced control of the **Nibe S1256 heat pump** via its local REST API. This dashboard provides a clean "Expert View" for technical users to manage device attributes, track historical data, and export system states.

> **Note:** This interface is specifically built to communicate with the Nibe S-series via the **Local API** (Port 8443).

---

## 🚀 Key Features

* **Real-time Monitoring:** Live updates of pump attributes with a single click.
* **Expert Modal:** Detailed technical view for every parameter, including Modbus registers, data types, and valid ranges.
* **Hardware Control:** Seamlessly update writable attributes directly from the UI with built-in range validation.
* **Historical Trends:** Integrated line charts (Chart.js) showing data fluctuations over the last 24 hours.
* **Excel Export:** One-click generation of system-wide data reports for analysis.
* **Smart Filtering:** "iOS-style" toggle to quickly isolate editable attributes.
* **Background Logging:** Automatic data logging to a local SQLite database every 3 minutes.

---

## ⚠️ Disclaimer

**This software is not affiliated with, authorized, or endorsed by Nibe.** Use this tool at your own risk. Incorrectly modifying parameters via the API can potentially harm your heating system or void your warranty. The author assumes no responsibility for hardware damage, loss of data, or any other issues caused by the use of this script.

---

## 🛠 Prerequisites

Before running the script, ensure you have **Python 3.8+** installed on your system.

### Required Libraries
Install the necessary dependencies using pip:

```bash
pip install flask flask-apscheduler requests pandas openpyxl

    flask: The web framework.

    flask-apscheduler: Handles background data logging tasks.

    requests: Manages communication with the Nibe Local API.

    pandas & openpyxl: Required for generating Excel reports.

⚙️ Configuration

    Enable the Local API in your Nibe S1256 unit settings.

    Update the config.json file with your device's local IP and credentials:

JSON

{
    "api_url": "https://<YOUR-NIBE-IP>:8443/api/v1/devices/0/points",
    "username": "your_username",
    "password": "your_password"
}

🏃 How to Run

    Initialize Database: The script automatically creates history.db on the first run.

    Start the Server:
    Bash

    python main.py

    Access the Dashboard: Open your web browser and navigate to:
    http://127.0.0.1:5000

📂 Project Structure

    main.py: The core Flask application and routing logic.

    api_handler.py: Manages REST API communication with the Nibe unit.

    db_handler.py: Handles SQLite storage and historical data retrieval.

    utils.py: Helper functions for data formatting.

    static/: Contains the CSS (styles) and JS (dashboard logic).

    templates/: HTML structures and UI components.

💡 Pro Tip

If you make changes to the CSS or JavaScript, remember to use Ctrl + F5 in your browser to perform a hard reload and see the latest updates immediately.
📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
