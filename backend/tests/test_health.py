import os
from pathlib import Path
import sys

from fastapi.testclient import TestClient

os.environ["NEXUSHR_BOOTSTRAP_DATABASE"] = "false"
os.environ["NEXUSHR_AUTH_MODE"] = "local"

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.main import app

client = TestClient(app)


def test_backend_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_domain_health_summary() -> None:
    response = client.get("/health/domains")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert len(payload["domains"]) == 8
    assert {item["domain"] for item in payload["domains"]} == {
        "auth",
        "employee",
        "attendance",
        "payroll",
        "performance",
        "notifications",
        "assistant",
        "audit",
    }


def test_login_and_dashboard_flow() -> None:
    login_response = client.post(
        "/v1/auth/login",
        json={
            "email": "maya.rao@nexushr.example",
            "password": "NexusHR!2026",
            "mfa_code": "246810",
            "method": "password",
        },
    )

    assert login_response.status_code == 200
    payload = login_response.json()
    assert payload["access_token"]

    dashboard_response = client.get(
        "/v1/dashboard/me",
        headers={"Authorization": f"Bearer {payload['access_token']}"},
    )

    assert dashboard_response.status_code == 200
    dashboard_payload = dashboard_response.json()
    assert dashboard_payload["employee"]["employee_id"] == "emp-maya-rao"
    assert dashboard_payload["calendar"]
