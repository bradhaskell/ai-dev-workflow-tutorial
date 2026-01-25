"""
LMU Baseball Practice Dashboard

A Streamlit dashboard for visualizing batting practice metrics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="LMU Baseball Practice Dashboard",
    page_icon="baseball",
    layout="wide"
)

DATA_FILE = "data/sample_batting_practice.csv"


@st.cache_data
def load_data() -> pd.DataFrame | None:
    """Load and cache batting practice data from CSV file."""
    try:
        df = pd.read_csv(DATA_FILE)
        if df.empty:
            return None
        df["date"] = pd.to_datetime(df["date"])
        return df
    except FileNotFoundError:
        st.error(f"Data file not found: {DATA_FILE}")
        return None


def main():
    """Main application entry point."""
    st.title("LMU Baseball Practice Dashboard")
    st.markdown("Batting practice performance metrics and analysis")

    # Load data
    df = load_data()
    if df is None:
        st.stop()

    # --- KPI Cards ---
    st.header("Team Performance Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        avg_ev = df["exit_velocity"].mean()
        st.metric("Avg Exit Velocity", f"{avg_ev:.1f} mph")

    with col2:
        avg_la = df["launch_angle"].mean()
        st.metric("Avg Launch Angle", f"{avg_la:.1f}°")

    with col3:
        avg_dist = df["distance"].mean()
        st.metric("Avg Distance", f"{avg_dist:.0f} ft")

    with col4:
        hard_hit_pct = (df["quality_of_contact"] == "Hard").sum() / len(df) * 100
        st.metric("Hard Hit %", f"{hard_hit_pct:.1f}%")

    st.divider()

    # --- Charts ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Exit Velocity by Player")
        player_ev = df.groupby("player_name")["exit_velocity"].mean().sort_values(ascending=True)
        fig_ev = px.bar(
            x=player_ev.values,
            y=player_ev.index,
            orientation="h",
            labels={"x": "Avg Exit Velocity (mph)", "y": "Player"},
            color=player_ev.values,
            color_continuous_scale="Blues"
        )
        fig_ev.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_ev, use_container_width=True)

    with col_right:
        st.subheader("Performance by Drill Type")
        drill_metrics = df.groupby("drill_type").agg({
            "exit_velocity": "mean",
            "launch_angle": "mean",
            "distance": "mean"
        }).round(1)
        fig_drill = px.bar(
            drill_metrics,
            x=drill_metrics.index,
            y="exit_velocity",
            labels={"drill_type": "Drill Type", "exit_velocity": "Avg Exit Velocity (mph)"},
            color="exit_velocity",
            color_continuous_scale="Reds"
        )
        fig_drill.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_drill, use_container_width=True)

    # --- Quality of Contact Distribution ---
    st.subheader("Quality of Contact Distribution")

    col_pie, col_table = st.columns([1, 1])

    with col_pie:
        contact_counts = df["quality_of_contact"].value_counts()
        fig_pie = px.pie(
            values=contact_counts.values,
            names=contact_counts.index,
            color=contact_counts.index,
            color_discrete_map={"Hard": "#2ecc71", "Medium": "#f1c40f", "Weak": "#e74c3c"}
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_table:
        st.subheader("Player Summary")
        player_summary = df.groupby("player_name").agg({
            "exit_velocity": "mean",
            "launch_angle": "mean",
            "distance": "mean"
        }).round(1)
        player_summary.columns = ["Avg EV (mph)", "Avg LA (°)", "Avg Dist (ft)"]
        player_summary = player_summary.sort_values("Avg EV (mph)", ascending=False)
        st.dataframe(player_summary, use_container_width=True)


if __name__ == "__main__":
    main()
