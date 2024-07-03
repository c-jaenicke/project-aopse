import json

import hibpwned

from app.config import ConfigSingleton


class HIBP:

    def __init__(self):
        self.config = ConfigSingleton.get_instance()
        self.hibp = None

    def get_breaches(self, email):
        self.hibp = hibpwned.Pwned(email, agent="AOPSE", key=self.config.aopse.tools["hibp"].api_key)
        breaches = self.hibp.search_all_breaches()
        json_breaches = json.dumps(breaches)
        print(json_breaches)
        return json_breaches
