# Cyber-Tactical USB Agent

A lightweight cross-device diagnostic toolkit designed to silently collect basic system telemetry from a host machine and forward it to a secure central endpoint for monitoring and review.

This project is intended for authorized internal diagnostics, system health checks, and controlled environment monitoring. It includes a local data collector, a Flask-based receiver, and a minimal dashboard interface for visualizing the latest audit results.

## Overview

The repository consists of four core components:

- `Audit.py` — a silent system collector that gathers host information and sends it to a configured API endpoint
- `main.py` — a Flask server that accepts telemetry, validates a bearer token, and exposes the latest result
- `templates/dashboard.html` — a simple authenticated dashboard for viewing system diagnostics
- `Run_Silent.vbs` — a Windows helper script to launch the collector in the background without a visible console

## Features

- Hostname detection
- Operating system identification
- IP address collection
- CPU utilization monitoring
- RAM utilization monitoring
- Free disk space measurement
- JSON-based reporting over HTTP
- Token-based API protection
- Browser dashboard for monitoring latest telemetry
- Silent background execution on Windows

## Repository Structure

```text
Cyber-Tactical-USB-Agent/
├── Audit.py
├── main.py
├── README.md
├── Run_Silent.vbs
└── templates/
    └── dashboard.html
```

## How It Works

1. The client script (`Audit.py`) collects a snapshot of the target machine:
   - hostname
   - OS version
   - IP address
   - CPU usage
   - RAM usage
   - free disk space
2. It sends this payload to a configured API URL using an Authorization header with a bearer token.
3. The Flask application (`main.py`) receives the telemetry at `/api/audit`, validates the token, and stores the latest payload.
4. The dashboard (`/dashboard`) is loaded in a browser and fetches the latest data from `/api/audit/latest`, after the user enters the correct token.

## Requirements

Python dependencies:

```bash
pip install flask flask-cors psutil requests
```

## Configuration

Before running the project, replace the placeholder values in the code.

### 1) Configure the telemetry collector

In `Audit.py`:

```python
API_URL = "YOUR_TARGET_URL"
TOKEN = "YOUR_API_TOKEN"
```

Set `API_URL` to the HTTP endpoint that will receive the audit data, and set `TOKEN` to the shared secret used by the receiver.

### 2) Configure the API receiver

In `main.py`:

```python
SECRET_TOKEN = "YOUR_API_TOKEN"
```

This token must match the token configured in `Audit.py`.

### 3) Configure the dashboard fetch URL

In `templates/dashboard.html`, replace:

```javascript
fetch('YOUR_HTTPS_DIRECTORY', {
```

with the actual HTTPS endpoint exposing `/api/audit/latest`.

## Running the Server

From the repository root:

```bash
python main.py
```

This starts the Flask application, which listens on the default local development port.

To access the dashboard, browse to:

```text
http://localhost:5000/dashboard
```

## Running the Client

You can run the audit client directly:

```bash
python Audit.py
```

On Windows, you can silently launch it in the background with:

```bat
wscript Run_Silent.vbs
```

This launches the script with `pythonw`, which hides the console window while the agent continues running in the background.

## API Endpoints

### POST `/api/audit`
Receives the host telemetry payload and stores it as the latest result.

Required Authorization header:

```http
Authorization: Bearer YOUR_API_TOKEN
```

### GET `/api/audit/latest`
Returns the most recent telemetry payload.

### GET `/dashboard`
Renders the diagnostic dashboard UI.

## Example Payload

```json
{
  "hostname": "WORKSTATION-01",
  "os": "Windows 11",
  "ip_address": "192.168.1.42",
  "cpu_usage": 27.4,
  "ram_usage": 62.1,
  "disk_free_gb": 154.23
}
```

## Security and Usage Notes

This project is intended strictly for authorized environments and legitimate internal diagnostics. Use only with explicit permission and in compliance with applicable laws, security policies, and organizational requirements.

- Replace all default tokens before deployment
- Limit access to the API and dashboard to trusted administrators only
- Use HTTPS in production environments
- Avoid exposing sensitive endpoints to untrusted networks

## Disclaimer

This repository is provided as a learning and diagnostics tool for controlled environments. It is not intended for unauthorized surveillance, intrusion, or misuse. Any deployment should be ethically justified, appropriately authorized, and compliant with relevant legal and organizational policies.

## License

This project does not currently include a formal license file. If you intend to distribute or reuse it publicly, consider adding an explicit license such as MIT or Apache-2.0.
