import requests
import random
from typing import Dict


class AccountChecker:
    def __init__(self):
        self.session = requests.Session()
        self.sites = {
            "GitHub": {
                "url": "https://github.com/{username}",
                "errorType": "http_status"
            },
            "GitLab": {
                "url": "https://gitlab.com/api/v4/users?username={username}",
                "errorType": "json_object"
            },
            "YouTube": {
                "url": "https://www.youtube.com/@{username}",
                "errorType": "http_status"
            }
        }
        self.set_user_agent()

    def set_user_agent(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
        ]
        self.session.headers.update({'User-Agent': random.choice(user_agents)})

    def check(self, username: str) -> Dict[str, bool]:
        results = {}
        for site_name, site_data in self.sites.items():
            try:
                url = site_data['url'].format(username=username)
                response = self.session.get(url, timeout=5)

                if site_data['errorType'] == 'http_status':
                    exists = response.status_code == 200
                elif site_data['errorType'] == 'json_object':
                    exists = len(response.json()) > 0
                else:
                    exists = response.status_code == 200

                results[site_name] = exists
            except Exception as e:
                print(f"Error checking {site_name}: {str(e)}")
                results[site_name] = False

        return results

