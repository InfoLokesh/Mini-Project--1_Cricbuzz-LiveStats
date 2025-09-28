import streamlit as st
import requests
import os
import json

class PlayerStats:
        def player_stats_method(self):

            selected_player_name = ""
            selected_player_id = ""
            player_id_len = 0
            player_id = []
            player_name = []

            st.header("🏃Cricket Player Statistics")
            st.subheader("🔎Search for a Player")
            # st.text("Enter player name:")
            col1, col2 = st.columns([3, 1])

            with col1:
                entered_player_name = st.text_input("", label_visibility="collapsed",placeholder="Enter player name:")

            with col2:
                player_search_clicked = st.button("🔎 Search", type="primary")

            if player_search_clicked:
                print(f'entered_player_name - {entered_player_name}')

                # url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"
                # querystring = {"plrN": entered_player_name}
                # headers = {
                #     "x-rapidapi-key": "2eb5734a90msh34d1b536b5e4d6dp1fde0ajsn16a7edb1f5f8",
                #     "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
                # }
                # response = requests.get(url, headers=headers, params=querystring)
                # # print(response.json())
                # player_search_response = response.json()
                #
                # # with open("../data/player_search_response.json","w") as f:
                # with open("data/player_search_response.json", "w") as f:
                #     json.dump(player_search_response,f,indent=4)

                try:
                    # with open("../data/player_search_response.json","r") as f:
                    with open("data/player_search_response.json", "r") as f:
                        loaded_player_search_response = json.load(f)
                except FileNotFoundError:
                    print("player_search_response.json file not found")
                    print(os.getcwd())

                players = loaded_player_search_response["player"]
                for player in players:
                    player_id.append(player["id"])
                    player_name.append(player["name"])
                    # player_master_data[player["id"]]=player["name"]

                print(f"player_id - {player_id}")
                player_id_len = len(player_id)
                # print(f'player_master_data_len - {player_master_data_len}')


            if(player_id_len == 1):
                selected_player_name = player_name[0]
                selected_player_id = player_id[0]
                st.success(f"Found player: {selected_player_name}")

            if (player_id_len > 1):
                st.subheader(f"Found {player_id_len} Players matching '{entered_player_name}':")
                selected_player_name = st.selectbox("Select a player", player_name)
                if selected_player_name:
                    selected_player_index = player_name.index(selected_player_name)
                    print(f'selected_player_index - {selected_player_index}')
                    selected_player_id = player_id[selected_player_index]

            st.subheader(f"📊{selected_player_name} - Player Profile")








