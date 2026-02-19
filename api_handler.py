import requests
import urllib3

# Inaktivera SSL-varningar för lokala anrop
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class APIHandler:
    def __init__(self, config):
        self.url = config['api_url']
        self.auth = (config['username'], config['password'])

    def get_all_points(self):
        """Hämtar alla mätpunkter från enheten."""
        try:
            res = requests.get(self.url, auth=self.auth, verify=False, timeout=10)
            return res.json()
        except Exception as e:
            print(f"Fel vid hämtning av alla punkter: {e}")
            return {}

    def get_point(self, pid):
        """Hämtar en specifik mätpunkt och hanterar olika svarstyper."""
        try:
            res = requests.get(f"{self.url}/{pid}", auth=self.auth, verify=False, timeout=5)
            data = res.json()
            # Hanterar både om svaret är paketerat {"ID": {data}} eller direkt {data}
            if isinstance(data, dict) and str(pid) in data:
                return data.get(str(pid))
            return data
        except Exception as e:
            print(f"Fel vid hämtning av punkt {pid}: {e}")
            return None

    def update_point(self, pid, raw_value):
        """Skickar en PATCH-request för att ändra ett värde på enheten."""
        try:
            payload = [{
                "type": "datavalue", 
                "variableId": int(pid), 
                "integerValue": int(raw_value)
            }]
            res = requests.patch(self.url, json=payload, auth=self.auth, verify=False, timeout=10)
            return res.status_code == 200
        except Exception as e:
            print(f"Fel vid uppdatering av punkt {pid}: {e}")
            return False