import streamlit as st
import requests
import json
import os
import pandas as pd


class PlayerStats:

    def player_stats_method(self):
        st.header("🏃Cricket Player Statistics")
        st.subheader("🔎Search for a Player")

        # Layout: input + button on same line
        col1, col2 = st.columns([3, 1])
        with col1:
            entered_player_name = st.text_input(
                "", label_visibility="collapsed", placeholder="Enter player name:",
                key="entered_player_name"  # keep input across reruns
            )
        with col2:
            player_search_clicked = st.button("🔎 Search", type="primary")

        # ensure a place to store search results
        if "player_search_results" not in st.session_state:
            st.session_state.player_search_results = {"player_id": [], "player_name": [], "entered": ""}

        # When user clicks search -> load results and store them in session_state
        if player_search_clicked:
            # clear any previous selection
            st.session_state.pop("selected_player_name", None)
            st.session_state.pop("selected_player_id", None)

            # url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"
            # querystring = {"plrN": entered_player_name}
            # headers = {
            #     "x-rapidapi-key": "2eb5734a90msh34d1b536b5e4d6dp1fde0ajsn16a7edb1f5f8",
            #     "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
            # }
            # response = requests.get(url, headers=headers, params=querystring)
            # # print(response.json())
            # player_search_response = response.json()

            # with open("../data/player_search_response.json","w") as f:
            with open("data/player_search_response.json", "w") as f:
                json.dump(player_search_response,f,indent=4)

            try:
                with open("data/player_search_response.json", "r") as f:
                    loaded_player_search_response = json.load(f)
            except FileNotFoundError:
                st.error("player_search_response.json file not found")
                print(os.getcwd())

            players = loaded_player_search_response.get("player", [])
            player_ids = [p["id"] for p in players]
            player_names = [p["name"] for p in players]

            st.session_state.player_search_results = {
                "player_id": player_ids,
                "player_name": player_names,
                "entered": entered_player_name
            }

        # Read results from session_state (persisted across reruns)
        player_id = st.session_state.player_search_results["player_id"]
        player_name = st.session_state.player_search_results["player_name"]
        player_id_len = len(player_id)

        # Single-match -> auto-select and show success
        if player_id_len == 1:
            st.session_state.selected_player_name = player_name[0]
            st.session_state.selected_player_id = player_id[0]
            st.success(f"Found player: {st.session_state.selected_player_name}")

        # Multiple matches -> render selectbox (use key so value persists)
        elif player_id_len > 1:
            st.subheader(
                f"Found {player_id_len} players matching '{st.session_state.player_search_results['entered']}':")
            selected_player_name = st.selectbox(
                "Select a player",
                player_name,
                key="selected_player"  # persists user's choice
            )
            if selected_player_name:
                selected_idx = player_name.index(selected_player_name)
                st.session_state.selected_player_name = selected_player_name
                st.session_state.selected_player_id = player_id[selected_idx]

        # Show profile header (if a player was selected/persisted)
        if "selected_player_name" in st.session_state:
            st.subheader(f"📊 {st.session_state.selected_player_name} - Player Profile")

            # url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{st.session_state.selected_player_id}"
            # headers = {
            #     "x-rapidapi-key": "2eb5734a90msh34d1b536b5e4d6dp1fde0ajsn16a7edb1f5f8",
            #     "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
            # }
            # response = requests.get(url, headers=headers)
            # print(response.json())
            # player_get_info_response = response.json()
            #
            # # with open("../data/player_get_info_response.json","w") as f:
            # with open("data/player_get_info_response.json", "w") as f:
            #     json.dump(player_get_info_response,f,indent=4)

            try:
                with open("data/player_get_info_response.json", "r") as f:
                    loaded_player_get_info_response = json.load(f)
            except FileNotFoundError:
                st.error("player_get_info_response.json file not found")
                print(os.getcwd())

            tab1, tab2, tab3 = st.tabs(["Profile", "Batting Stats", "Bowling Status"])

            with tab1:
                st.subheader("🎯Personal Information")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f'##### 🏏Cricket Details')
                    st.write(f'**Role** : {loaded_player_get_info_response.get("roles", 'NA')}')
                    st.write(f'**Batting** : {loaded_player_get_info_response.get("bat", 'NA')}')
                    st.write(f'**Bowling** : {loaded_player_get_info_response.get("bowl", 'NA')}')
                    st.write(f'**International Team** : {loaded_player_get_info_response.get("intlTeam", 'NA')}')

                with col2:
                    st.markdown(f'##### 📍Personal Details')
                    st.write(f'**Date of Birth** : {loaded_player_get_info_response.get("DoB", 'NA')}')
                    st.write(f'**Birth Place** : {loaded_player_get_info_response.get("birthPlace", 'NA')}')
                    st.write(f'**Height** : {loaded_player_get_info_response.get("height", 'NA')}')

                with col3:
                    st.markdown(f'##### 🏆Team Played For')
                    st.write(f'{loaded_player_get_info_response.get("teams", 'NA')}')

                st.markdown(
                    f"**Full profile:** {loaded_player_get_info_response.get("appIndex", 'NA').get('webURL', 'NA')}")

            with tab2:
                batting_stats_clicked = st.button("Fetch Batting Statistics", type="primary")
                if batting_stats_clicked:

                    # url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{st.session_state.selected_player_id}/batting"
                    # headers = {
                    #     "x-rapidapi-key": "2eb5734a90msh34d1b536b5e4d6dp1fde0ajsn16a7edb1f5f8",
                    #     "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
                    # }
                    # response = requests.get(url, headers=headers)
                    # print(response.json())
                    #
                    # player_batting_response = response.json()
                    #
                    # # with open("../data/player_batting_response.json","w") as f:
                    # with open("data/player_batting_response.json", "w") as f:
                    #     json.dump(player_batting_response,f,indent=4)

                    try:
                        with open("data/player_batting_response.json", "r") as f:
                            loaded_player_batting_response = json.load(f)
                    except FileNotFoundError:
                        st.error("player_batting_response.json file not found")
                        print(os.getcwd())

                    df = convert_json_to_df(loaded_player_batting_response, 'Statistics')

                    st.subheader("🏏Batting Career Statistics")
                    # st.markdown(f'#### 📊Career Overview')

                    st.markdown(f'#### 📈Batting Detailed Statistics')
                    st.dataframe(df.to_dict("records"), use_container_width=True)

            with tab3:
                bowling_stats_clicked = st.button("Fetch Bowling Statistics", type="primary")
                if bowling_stats_clicked:
                    # url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{st.session_state.selected_player_id}/bowling"
                    # headers = {
                    #     "x-rapidapi-key": "2eb5734a90msh34d1b536b5e4d6dp1fde0ajsn16a7edb1f5f8",
                    #     "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
                    # }
                    # response = requests.get(url, headers=headers)
                    # print(response.json())
                    #
                    # player_bowling_response = response.json()
                    #
                    # # with open("../data/player_bowling_response.json","w") as f:
                    # with open("data/player_bowling_response.json", "w") as f:
                    #     json.dump(player_bowling_response,f,indent=4)

                    try:
                        with open("data/player_bowling_response.json", "r") as f:
                            loaded_player_bowling_response = json.load(f)
                    except FileNotFoundError:
                        st.error("player_bowling_response.json file not found")
                        print(os.getcwd())

                    df = convert_json_to_df(loaded_player_bowling_response, 'Statistics')

                    st.subheader("🏏Bowling Career Statistics")
                    # st.markdown(f'#### 📊Career Overview')

                    st.markdown(f'#### 📈Bowling Detailed Statistics')
                    st.dataframe(df.to_dict("records"), use_container_width=True)


def convert_json_to_df(json_data, index_header):
    # Extract format headers (Test, ODI, T20, IPL)
    headers = json_data['headers']
    formats = []
    for i in range(1, len(headers)):
        formats.append(headers[i])  # Skip the first empty header

    # Prepare statistics and values
    statistics = []
    values = []

    for row in json_data['values']:
        stat_name = row['values'][0]
        stat_values = row['values'][1:]

        statistics.append(stat_name)
        values.append(stat_values)

    # Create DataFrame
    df = pd.DataFrame(values, columns=formats)
    df.insert(0, index_header, statistics)

    # Reset index to avoid showing it
    df = df.reset_index(drop=True)

    return df


def get_stat(df, stat_name, format_name):
    """
    Get a specific statistic value from the career overview DataFrame.

    Parameters:
        df (pd.DataFrame): The stats dataframe
        stat_name (str): The statistic to fetch (e.g., "Runs", "Average", "Strike Rate")
        format_name (str): The format column (e.g., "ODI", "T20", "IPL", "Test")

    Returns:
        value if found, else None
    """
    try:
        value = df.loc[df['Statistics'] == stat_name, format_name].values[0]
        return value
    except (IndexError, KeyError):
        return None
