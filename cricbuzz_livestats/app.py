import streamlit as st
import importlib
import pages.live_matches as lm
import pages.player_stats as ps
import pages.sql_analytics as sa
importlib.reload(lm)
importlib.reload(ps)
importlib.reload(sa)

# import live_matches as lm
# import player_stats as ps
# import sql_analytics as sa

class home:
    st.title("Cricbuzz Livestats")

    tab1, tab2, tab3, tab4 = st.tabs(["Live Match", "Player Stats", "SQL Analytics", "CRUD Operations"])

    with tab1:
        lm = lm.LiveMatch()

    with tab2:
        ps = ps.PlayerStats()
        ps.player_stats_method()

    with tab3:
        sa = sa.SqlAnalytics()



