import os
import requests

class ClaudeProvider:
    def __init__(self, api_key=None, base_url="https://api.claude.ai"):
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided")
        self.base_url = base_url

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_data(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self._get_headers(), params=params)
        return self._handle_response(response)

    def post_data(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self._get_headers(), json=data)
        return self._handle_response(response)

    def process_data(self, data):
        # Implement data processing logic here
        pass