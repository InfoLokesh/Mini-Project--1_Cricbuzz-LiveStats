import requests
import json
import os
import pandas as pd
import utils.db_connection as db
import utils.mysql_queries as queries


def write_json_to_file(response_json, file_name):
    with open(f"../data/{file_name}", "w") as f:
        # with open(f"data/{file_name}", "w") as f:
        json.dump(response_json, f, indent=4)


def read_json_from_file(file_name):
    try:
        with open(f"../data/{file_name}", "r") as f:
            loaded_response_json = json.load(f)
            return loaded_response_json
    except FileNotFoundError:
        print(f"{file_name} is not found")
        print(os.getcwd())


# # teams/get-players
# # Path Params - teamId - 2 (India)
# url = "https://cricbuzz-cricket.p.rapidapi.com/teams/v1/2/players"
# headers = {
#     "x-rapidapi-key": "2eb5734a90msh34d1b536b5e4d6dp1fde0ajsn16a7edb1f5f8",
#     "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
# }
# response = requests.get(url, headers=headers)
#
# response_json = response.json()
# write_json_to_file(response_json, "teams_get_players_response.json")

loaded_response_json = read_json_from_file("teams_get_players_response.json")

# Normalize JSON
df = pd.json_normalize(loaded_response_json["player"])
df = df[df["id"].notna()]  # Keep only rows where id exists

# # Connect to MySQL
conn = db.create_connection_to_mysql_db()
cursor = conn.cursor()

# Create table if not exists (adjust schema as needed)
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100),
    imageId BIGINT,
    battingStyle VARCHAR(50),
    bowlingStyle VARCHAR(50)
)
""")

# Insert DataFrame rows into table
for _, row in df.iterrows():
    # Replace NaN with None (so MySQL accepts NULL)
    row = row.where(pd.notnull(row), None)

    cursor.execute("""
INSERT INTO players (id, name, imageId, battingStyle, bowlingStyle)
VALUES (%s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    imageId = VALUES(imageId),
    battingStyle = VALUES(battingStyle),
    bowlingStyle = VALUES(bowlingStyle)
""", (row["id"], row["name"], row["imageId"],
      row.get("battingStyle"), row.get("bowlingStyle")))

# Commit and close
conn.commit()
cursor.close()
conn.close()

