import requests
import json
import streamlit as st
import pandas as pd
import os
from pandas import json_normalize

class LiveMatch:

    def __init__(self):
        # url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
        # headers = {
        # 	"x-rapidapi-key": "2eb5734a90msh34d1b536b5e4d6dp1fde0ajsn16a7edb1f5f8",
        # 	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
        # }
        # response = requests.get(url, headers=headers)
        # print(response.json())
        #
        # live_matches_response = response.json()
        # print(type(live_matches_response))
        # print(live_matches_response)
        #
        # # with open("../data/live_matches_response.json","w") as f:
        # with open("data/live_matches_response.json", "w") as f:
        #     json.dump(live_matches_response,f,indent=4)

        try:
            # with open("../data/live_matches_response.json","r") as f:
            with open("data/live_matches_response.json", "r") as f:
                loaded_live_matches_response = json.load(f)
        except FileNotFoundError:
            print("live_matches_response.json file not found")
            print(os.getcwd())

        # print(loaded_live_matches_response)
        # print(type(loaded_live_matches_response))

        live_matches_li = []
        live_matches_data_li = []

        typeMatches = loaded_live_matches_response.get("typeMatches", [])
        # print(f'typeMatches - {typeMatches}')
        typeMatches_len = len(typeMatches)
        # print(f'typeMatches_len - {typeMatches_len}')

        for typeMatch in typeMatches:
            # print(f'typeMatch - {typeMatch}')
            seriesMatches = typeMatch.get("seriesMatches", [])
            # print(f'seriesMatches - {seriesMatches}')
            seriesMatches_len = len(seriesMatches)
            # print(f'seriesMatches_len - {seriesMatches_len}')

            for seriesMatch in seriesMatches:
                seriesAdWrapper = seriesMatch.get("seriesAdWrapper", {})
                # print(f'seriesAdWrapper - {seriesAdWrapper}')
                # seriesId = seriesAdWrapper.get("seriesId")
                # print(type(seriesId))
                # seriesName = seriesAdWrapper.get("seriesName")
                # print(type(seriesName))

                matches = seriesAdWrapper.get("matches", [])
                for match in matches:
                    live_matches_dict = {}
                    matchInfo = match.get("matchInfo", {})
                    # print(matchInfo)
                    matchId = matchInfo.get("matchId")
                    live_matches_dict.update({"matchId": matchId})
                    seriesName = matchInfo.get("seriesName")  # Required
                    live_matches_dict.update({"seriesName": seriesName})

                    matchDesc = matchInfo.get("matchDesc")  # Required
                    live_matches_dict.update({"matchDesc": matchDesc})
                    # matchDescSplit = matchDesc.split(",")[1].split("(")[0];
                    # print(matchDescSplit)
                    # print(len(matchDescSplit))
                    # matchDescSplit = matchDescSplit.strip()
                    # print(matchDescSplit)
                    # print(len(matchDescSplit))
                    matchFormat = matchInfo.get("matchFormat")  # Required
                    live_matches_dict.update({"matchFormat": matchFormat})
                    startDate = matchInfo.get("startDate")
                    endDate = matchInfo.get("endDate")
                    state = matchInfo.get("state")  # Required
                    live_matches_dict.update({"state": state})
                    status = matchInfo.get("status")  # Required
                    live_matches_dict.update({"status": status})

                    team1 = matchInfo.get("team1", {})
                    # team1.get("teamId")
                    team1teamName = team1.get("teamName")  # Required
                    live_matches_dict.update({"team1teamName": team1teamName})
                    team1teamSName = team1.get("teamSName")
                    team1ImageId = team1.get("ImageId")
                    team2 = matchInfo.get("team2", {})
                    # team2.get("teamId")
                    team2teamName = team2.get("teamName")  # Required
                    live_matches_dict.update({"team2teamName": team2teamName})
                    team2teamSName = team2.get("teamSName")
                    team2ImageId = team2.get("ImageId")

                    venueInfo = matchInfo.get("venueInfo", {})
                    ground = venueInfo.get("ground")  # Required
                    live_matches_dict.update({"ground": ground})
                    city = venueInfo.get("city")  # Required
                    live_matches_dict.update({"city": city})

                    matchScore = match.get("matchScore", {})
                    team1Score = matchScore.get("team1Score", {})
                    team1inngs1 = team1Score.get("inngs1", {})  # Required
                    live_matches_dict.update({"team1inngs1": team1inngs1})
                    team1inningsId = team1inngs1.get("inningsId")
                    team1runs = team1inngs1.get("runs")  # Required
                    live_matches_dict.update({"team1runs": team1runs})
                    team1wickets = team1inngs1.get("wickets")  # Required
                    live_matches_dict.update({"team1wickets": team1wickets})
                    team1overs = team1inngs1.get("overs")  # Required
                    live_matches_dict.update({"team1overs": team1overs})

                    team2Score = matchScore.get("team2Score", {})
                    team2inngs1 = team2Score.get("inngs1", {})  # Required
                    live_matches_dict.update({"team2inngs1": team2inngs1})
                    team2inningsId = team2inngs1.get("inningsId")
                    team2runs = team2inngs1.get("runs")  # Required
                    live_matches_dict.update({"team2runs": team2runs})
                    team2wickets = team2inngs1.get("wickets")  # Required
                    live_matches_dict.update({"team2wickets": team2wickets})
                    team2overs = team2inngs1.get("overs")  # Required
                    live_matches_dict.update({"team2overs": team2overs})

                    live_matches_dropdown = f'{team1teamName} vs {team2teamName} - {matchDesc} ({state})'
                    live_matches_li.append(live_matches_dropdown)
                    live_matches_data_li.append(live_matches_dict)

        print(f'live_matches_li - {live_matches_li}')
        print(f'live_matches_data_li - {live_matches_data_li}')

        st.header("🎢Cricbuzz Live Match Dashboard")
        st.subheader("🎯Select a Match")

        selected_match = st.selectbox("Available Matches", live_matches_li)
        if selected_match:
            selected_match_index = live_matches_li.index(selected_match)
            print(f'selected_match_index - {selected_match_index}')
        selected_match_data = live_matches_data_li[selected_match_index]
        print(f'selected_match_data - {selected_match_data}')

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f'🏏{selected_match_data.get("team1teamName")} vs {selected_match_data.get("team2teamName")}')

        with col2:
            st.success(f'📅**Series** : {selected_match_data.get("seriesName")}')

        st.write(f'📅**Match** : {selected_match_data.get("matchDesc")}')
        st.write(f'🏆**Format** : {selected_match_data.get("matchFormat")}')
        st.write(f'🏝**Venue** : {selected_match_data.get("ground")}')
        st.write(f'📍**City** : {selected_match_data.get("city")}')
        st.write(f'📌**Status** : {selected_match_data.get("status")}')
        st.write(f'⏲**State** : {selected_match_data.get("state")}')

        #
        #
        # 🏗
        st.subheader("📊Current Score")
        # st.markdown(st.write(selected_match_data.get("team1teamName")))

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f'##### {selected_match_data.get("team1teamName")}')
            if (len(selected_match_data.get("team1inngs1")) != 0):
                st.success(
                    f'Innings 1: {selected_match_data.get("team1runs")}/{selected_match_data.get("team1wickets")} ({selected_match_data.get("team1overs")} overs)')
                team1_scorecard_flag = True
        with col2:
            st.markdown(f'##### {selected_match_data.get("team2teamName")}')
            if (len(selected_match_data.get("team2inngs1")) != 0):
                st.success(
                    f'Innings 1: {selected_match_data.get("team2runs")}/{selected_match_data.get("team2wickets")} ({selected_match_data.get("team2overs")} overs)')
                team2_scorecard_flag = True
            else:
                st.warning("No score information available yet")

        if (len(selected_match_data.get("team1inngs1")) == 0):
            st.warning("No score information available yet")

        if (team1_scorecard_flag):
            st.subheader("📋Detailed Scorecard")

            loadFullScorecard_clicked = st.button("🔎Load Full Scorecard", type="primary")

            if (loadFullScorecard_clicked):

                # url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{selected_match_data.get("matchId")}/scard"
                # headers = {
                #     "x-rapidapi-key": "2eb5734a90msh34d1b536b5e4d6dp1fde0ajsn16a7edb1f5f8",
                #     "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
                # }
                # response = requests.get(url, headers=headers)
                # print(response.json())
                #
                # scorecard_response = response.json()
                # print(type(scorecard_response))
                # # print(scorecard_response)
                #
                # # with open("../data/scorecard_response.json","w") as f:
                # with open("data/scorecard_response.json", "w") as f:
                #     json.dump(scorecard_response,f,indent=4)

                try:
                    # with open("../data/scorecard_response.json","r") as f:
                    with open("data/scorecard_response.json", "r") as f:
                        loaded_scorecard_response = json.load(f)
                except FileNotFoundError:
                    print("scorecard_response.json file not found")
                    print(os.getcwd())

                scorecard_li = loaded_scorecard_response.get("scorecard", [])
                scorecard_li_len = len(scorecard_li)
                for i in range(scorecard_li_len):
                    # Extract the first innings (you can loop if multiple innings exist)
                    scorecard = scorecard_li[i]

                    st.subheader("📊Match Summary")
                    if(i%2 == 0):
                        st.subheader(f"🏏Innings {i+1}: {selected_match_data.get('team1teamName')}")
                        st.write(f"**Bowling**: {selected_match_data.get('team2teamName')}")
                    else:
                        st.subheader(f"🏏Innings {i+1}: {selected_match_data.get('team2teamName')}")
                        st.write(f"**Bowling**: {selected_match_data.get('team1teamName')}")

                    st.subheader(f"🏏Batting Scorecard")

                    # Convert batsman metrics to DataFrame
                    batsman_df = pd.json_normalize(scorecard["batsman"])
                    # print("Batsman Metrics:")
                    batsman_data_df = batsman_df[['name', 'runs', 'balls', 'fours', 'sixes', 'strkrate', 'outdec']]
                    batsman_data_df = batsman_data_df.rename(columns={
                        'name': 'Batsman',
                        'runs': 'Runs',
                        'balls': 'Balls',
                        'fours': '4s',
                        'sixes': '6s',
                        'strkrate': 'Strike Rate',
                        'outdec': 'Status'
                    })
                    st.dataframe(batsman_data_df.to_dict("records"), use_container_width=True)

                    st.subheader(f"🥎Bowling Scorecard")
                    # Convert bowler metrics to DataFrame
                    bowler_df = pd.json_normalize(scorecard["bowler"])
                    # print("\nBowler Metrics:")
                    bowler_data_df = bowler_df[['name', 'overs', 'maidens', 'runs', 'wickets', 'economy']]
                    bowler_data_df = bowler_data_df.rename(columns={
                        'name': 'Bowler',
                        'overs': 'Overs',
                        'maidens': 'Maidens',
                        'runs': 'Runs',
                        'wickets': 'Wickets',
                        'economy': 'Economy'
                    })
                    st.dataframe(bowler_data_df.to_dict("records"), use_container_width=True)

                    # # Normalize the data
                    # normalized_scorecard_response = json_normalize(loaded_scorecard_response)
                    # loaded_scorecard_df = pd.DataFrame(normalized_scorecard_response)
                    # print(loaded_scorecard_df)
                    #
                    # print(loaded_scorecard_df.columns)
                    # print(loaded_scorecard_df[['score','wickets','overs','runrate','extras']])

                    # loaded_scorecard_df.to_csv('../data/scorecard_response.csv', index=False)
                    # loaded_scorecard_df.to_csv('data/scorecard_response.csv', index=False)
