import pandas as pd
import requests


def fetch_fpl_data():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None


if __name__ == "__main__":
    data = fetch_fpl_data()
    player_data = pd.DataFrame(data["elements"])
    player_data.to_csv("fpl_player_data.csv", index=False)
