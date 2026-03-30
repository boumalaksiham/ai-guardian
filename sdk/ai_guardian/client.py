import httpx
import os
from typing import Optional, Dict, Any

class GuardianClient:
    def __init__(self, base_url: Optional[str] = None, timeout: int = 5):
        self.base_url = base_url or os.getenv("AI_GUARDIAN_URL", "http://localhost:8000")
        self.timeout = timeout

    def send_event(self, event_data: Dict[str, Any]) -> Optional[Dict]:
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(f"{self.base_url}/api/events/", json=event_data)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"[AI Guardian] Warning: Failed to send event — {e}")
            return None

    def get_summary(self) -> Optional[Dict]:
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(f"{self.base_url}/api/metrics/summary")
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"[AI Guardian] Warning: Failed to fetch summary — {e}")
            return None