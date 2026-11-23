# Nemesis Control Panel (Render)

## Files
- `app.py` — Flask dashboard
- `requirements.txt` — dependencies
- `render.yaml` — Render Blueprint configuration

## Deploy on Render
1. Upload these files to a GitHub repository.
2. In Render, choose **New + → Blueprint** (or create a Web Service).
3. Connect the repository and deploy.
4. Open the generated `onrender.com` URL.

The dashboard shows web-service health, uptime, server time, and recent activity.
Endpoints:
- `/` — dashboard
- `/health` — health check
- `/api/status` — JSON status

This is a standalone monitoring dashboard. It does not run Instagram messaging or automation tasks.
