import streamlit as st

import utils.constants as const

class SqlAnalytics:
    def __init__(self):
        st.header("📊Cricket SQL Analytics")
        st.subheader("🛄Database Query Questions")
        questions_dict = const.sql_questions
        options = []
        for k, v in questions_dict.items():
            options.append(f'{k} - {v}')

        question_selected = st.selectbox("Select a question to analyse:", options)

        # Extract key back
        selected_question_key = question_selected.split(" - ")[0]
        print(f"Extracted Key - selected_question_key - {selected_question_key}")

        # st.write("Selected Option:", question_selected)

        st.markdown(f'###### {question_selected}')
        view_sql_query_clicked = st.button("📃View SQL Query")
        if view_sql_query_clicked:
            st.text("Query In Progress")
        execute_query_clicked = st.button("⚡Execute Query", type="primary")
        if execute_query_clicked:
            st.subheader("🛄Query Results")

        # selected_match = st.selectbox("Available Matches", live_matches_li)
        # if selected_match:
        #     selected_match_index = live_matches_li.index(selected_match)
        #     print(f'selected_match_index - {selected_match_index}')
        # selected_match_data = live_matches_data_li[selected_match_index]
        # print(f'selected_match_data - {selected_match_data}')