"""FastAPI integration tests."""
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_ok(self):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


class TestOrdersEndpoints:
    def test_create_order(self):
        payload = {
            "customer_name": "Test User",
            "drinks": [{"name": "Latte", "base": "espresso", "milk": "oat", "shots": 2}],
        }
        r = client.post("/orders/", json=payload)
        assert r.status_code == 201
        data = r.json()
        assert data["customer_name"] == "Test User"
        assert data["order_id"].startswith("#")
        assert data["complexity_score"] > 0

    def test_get_queue(self):
        r = client.get("/orders/queue")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_complete_nonexistent_order_404(self):
        import urllib.parse
        r = client.delete(f"/orders/{urllib.parse.quote('#NOTEXIST', safe='')}")
        assert r.status_code == 404

    def test_create_and_complete_order(self):
        import urllib.parse
        payload = {
            "customer_name": "Flow Test",
            "drinks": [{"name": "Americano", "base": "lungo", "milk": "none", "shots": 2}],
        }
        create_r = client.post("/orders/", json=payload)
        order_id = create_r.json()["order_id"]
        encoded_id = urllib.parse.quote(order_id, safe="")

        delete_r = client.delete(f"/orders/{encoded_id}")
        assert delete_r.status_code == 200
        assert delete_r.json()["status"] == "completed"


class TestSchedulerEndpoint:
    def test_schedule_returns_action(self):
        # Add an order first
        client.post("/orders/", json={
            "customer_name": "Sched Test",
            "drinks": [{"name": "Flat white", "base": "ristretto", "milk": "whole", "shots": 2}],
        })
        r = client.get("/schedule/")
        assert r.status_code == 200
        data = r.json()
        assert "action_main" in data
        assert "concurrency_ratio" in data
        assert data["concurrency_ratio"] >= 0


class TestMetricsEndpoint:
    def test_metrics_shape(self):
        r = client.get("/metrics/")
        assert r.status_code == 200
        data = r.json()
        assert "throughput_per_hour" in data
        assert "avg_wait_minutes" in data
        assert "concurrency_ratio" in data


class TestConfigEndpoints:
    def test_get_config(self):
        r = client.get("/config/")
        assert r.status_code == 200
        data = r.json()
        assert "machine" in data
        assert "scheduler" in data
        assert "rl" in data

    def test_update_config(self):
        r = client.post("/config/", json={
            "machine": {"group1_shot_secs": 30, "group2_shot_secs": 27,
                        "steamer_warmup_secs": 8, "grinder_secs": 10, "assemble_secs": 15,
                        "milk_whole_secs": 24, "milk_oat_secs": 35, "milk_almond_secs": 30,
                        "milk_soy_secs": 28},
            "scheduler": {"max_concurrent_slots": 3, "wait_weight": 0.7,
                          "complexity_weight": 0.2, "machine_weight": 0.1},
            "rl": {"learning_rate": 0.05, "discount_factor": 0.95,
                   "epsilon": 0.1, "live_training": True},
            "features": {"rush_mode_auto": True, "concurrent_suggestions": True,
                         "rl_live_retraining": True, "demand_forecasting": True,
                         "post_rush_report": True, "error_recovery": False},
        })
        assert r.status_code == 200
        assert r.json()["machine"]["group1_shot_secs"] == 30
        assert r.json()["machine"]["milk_oat_secs"] == 35

    def test_reset_config(self):
        r = client.post("/config/reset")
        assert r.status_code == 200
        assert r.json()["machine"]["milk_oat_secs"] == 32   # default value
