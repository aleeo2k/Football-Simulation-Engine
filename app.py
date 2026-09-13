import math
import io
from contextlib import redirect_stdout
from datetime import date

import pandas as pd
import streamlit as st

from src.services.prediction_service import PredictionService


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Football Engine",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
       ========================= */

    .block-container {
        max-width: 920px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* =========================
       HEADER
       ========================= */

    .app-title {
        font-size: 2.4rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        text-align: center;
        color: #8b8d96;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* =========================
       MATCH CARD
       ========================= */

    .match-card {
        background: #181a21;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0 1.5rem 0;
        border: 1px solid rgba(255,255,255,0.06);
    }

    .match-card-title {
        text-align: center;
        font-size: 0.75rem;
        color: #8b8d96;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.8rem;
    }

    .match-teams {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
    }

    .match-team {
        font-size: 1.35rem;
        font-weight: 750;
        text-align: center;
        flex: 1;
    }

    .match-vs {
        color: #858791;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* =========================
       MAIN PREDICTION
       ========================= */

    .main-prediction {
        background: #181a21;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.06);
    }

    .prediction-label {
        text-align: center;
        color: #8b8d96;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.4rem;
    }

    .prediction-team {
        text-align: center;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }

    .prediction-percent {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 850;
    }

    /* =========================
       SECTION
       ========================= */

    .section-title {
        font-size: 1.35rem;
        font-weight: 750;
        margin-top: 1.8rem;
        margin-bottom: 0.8rem;
    }

    /* =========================
       SCORE
       ========================= */

    .score-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #181a21;
        border-radius: 12px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.45rem;
    }

    .score-value {
        font-weight: 700;
        font-size: 1rem;
    }

    .score-probability {
        color: #b9bbc4;
        font-size: 0.95rem;
    }

    /* =========================
       INFO
       ========================= */

    .model-info {
        text-align: center;
        color: #777984;
        font-size: 0.8rem;
        margin-top: 2rem;
    }

    /* =========================
       MOBILE
       ========================= */

    @media (max-width: 600px) {

        .block-container {
            padding-left: 0.8rem;
            padding-right: 0.8rem;
            padding-top: 0.8rem;
        }

        .app-title {
            font-size: 1.9rem;
        }

        .app-subtitle {
            font-size: 0.9rem;
            margin-bottom: 1.2rem;
        }

        .match-card {
            padding: 1.1rem;
            border-radius: 16px;
        }

        .match-teams {
            gap: 0.7rem;
        }

        .match-team {
            font-size: 1.05rem;
        }

        .prediction-percent {
            font-size: 2.4rem;
        }

        .prediction-team {
            font-size: 1.6rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# POISSON
# ============================================================

def poisson_probability(lmbda, goals):

    return (
        math.exp(-lmbda)
        * (lmbda ** goals)
        / math.factorial(goals)
    )


def match_probabilities(
    home_xg,
    away_xg,
    max_goals=10,
):

    home_probs = [
        poisson_probability(home_xg, i)
        for i in range(max_goals + 1)
    ]

    away_probs = [
        poisson_probability(away_xg, i)
        for i in range(max_goals + 1)
    ]

    home_win = 0.0
    draw = 0.0
    away_win = 0.0

    score_probs = []

    for home_goals in range(max_goals + 1):

        for away_goals in range(max_goals + 1):

            probability = (
                home_probs[home_goals]
                * away_probs[away_goals]
            )

            score_probs.append(
                (
                    probability,
                    home_goals,
                    away_goals,
                )
            )

            if home_goals > away_goals:

                home_win += probability

            elif home_goals == away_goals:

                draw += probability

            else:

                away_win += probability

    under_25 = 0.0
    btts = 0.0

    for (
        probability,
        home_goals,
        away_goals,
    ) in score_probs:

        if home_goals + away_goals <= 2:

            under_25 += probability

        if (
            home_goals >= 1
            and away_goals >= 1
        ):

            btts += probability

    over_25 = 1.0 - under_25

    best_scores = sorted(
        score_probs,
        reverse=True,
    )[:5]

    return {

        "home_win": home_win,

        "draw": draw,

        "away_win": away_win,

        "over_25": over_25,

        "under_25": under_25,

        "btts": btts,

        "no_btts": 1.0 - btts,

        "best_scores": best_scores,

    }


# ============================================================
# LOAD SERVICE
# ============================================================

@st.cache_resource
def load_service():

    return PredictionService()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="app-title">⚽ Football Engine</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-subtitle">'
    'Football match prediction engine'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# LOAD ENGINE
# ============================================================

try:

    service = load_service()

    teams = service.get_teams()

except Exception as error:

    st.error(
        f"Failed to load prediction engine: {error}"
    )

    st.stop()


# ============================================================
# MATCH
# ============================================================

st.markdown(
    '<div class="section-title">Match</div>',
    unsafe_allow_html=True,
)


col1, col2 = st.columns(2)


with col1:

    arsenal_index = (
        teams.index("Arsenal")
        if "Arsenal" in teams
        else 0
    )

    home_team = st.selectbox(
        "Home team",
        teams,
        index=arsenal_index,
    )


with col2:

    default_away = (
        teams.index("Coventry")
        if "Coventry" in teams
        else (
            1
            if len(teams) > 1
            else 0
        )
    )

    away_team = st.selectbox(
        "Away team",
        teams,
        index=default_away,
    )


# ============================================================
# DATE
# ============================================================

st.markdown(
    '<div class="section-title">Match date</div>',
    unsafe_allow_html=True,
)


match_date = st.date_input(
    "Date",
    value=date.today(),
    label_visibility="collapsed",
)


# ============================================================
# PREDICT
# ============================================================

st.write("")

predict_button = st.button(
    "🔮  PREDICT",
    use_container_width=True,
    type="primary",
)


# ============================================================
# PREDICTION
# ============================================================

if predict_button:

    if home_team == away_team:

        st.error(
            "Home and away teams must be different."
        )

        st.stop()

    with st.spinner(
        "Calculating prediction..."
    ):

        try:

            buffer = io.StringIO()

            with redirect_stdout(buffer):

                result = service.predict(
                    home_team,
                    away_team,
                    match_date=str(match_date),
                )

            home_xg = result["home_xg"]
            away_xg = result["away_xg"]

            probabilities = match_probabilities(
                home_xg,
                away_xg,
            )

        except Exception as error:

            st.error(
                f"Prediction error: {error}"
            )

            st.stop()


    # ========================================================
    # MATCH HEADER
    # ========================================================

    st.markdown(
        f"""
        <div class="match-card">

            <div class="match-card-title">
                Match prediction
            </div>

            <div class="match-teams">

                <div class="match-team">
                    {home_team}
                </div>

                <div class="match-vs">
                    VS
                </div>

                <div class="match-team">
                    {away_team}
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # MAIN PREDICTION
    # ========================================================

    outcomes = {

        home_team:
            probabilities["home_win"],

        "Draw":
            probabilities["draw"],

        away_team:
            probabilities["away_win"],

    }

    best_team = max(
        outcomes,
        key=outcomes.get,
    )

    best_probability = outcomes[
        best_team
    ]


    st.markdown(
        f"""
        <div class="main-prediction">

            <div class="prediction-label">
                Model prediction
            </div>

            <div class="prediction-team">
                {best_team}
            </div>

            <div class="prediction-percent">
                {best_probability * 100:.1f}%
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # 1X2
    # ========================================================

    st.markdown(
        '<div class="section-title">Match result</div>',
        unsafe_allow_html=True,
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            home_team,
            f"{probabilities['home_win'] * 100:.1f}%",
        )


    with col2:

        st.metric(
            "Draw",
            f"{probabilities['draw'] * 100:.1f}%",
        )


    with col3:

        st.metric(
            away_team,
            f"{probabilities['away_win'] * 100:.1f}%",
        )


    # ========================================================
    # EXPECTED GOALS
    # ========================================================

    st.markdown(
        '<div class="section-title">Expected Goals</div>',
        unsafe_allow_html=True,
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            home_team,
            f"{home_xg:.2f}",
        )


    with col2:

        st.metric(
            away_team,
            f"{away_xg:.2f}",
        )


    # ========================================================
    # GOALS
    # ========================================================

    st.markdown(
        '<div class="section-title">Goals</div>',
        unsafe_allow_html=True,
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Over 2.5",
            f"{probabilities['over_25'] * 100:.1f}%",
        )


    with col2:

        st.metric(
            "Under 2.5",
            f"{probabilities['under_25'] * 100:.1f}%",
        )


    # ========================================================
    # BTTS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Both Teams To Score'
        '</div>',
        unsafe_allow_html=True,
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "YES",
            f"{probabilities['btts'] * 100:.1f}%",
        )


    with col2:

        st.metric(
            "NO",
            f"{probabilities['no_btts'] * 100:.1f}%",
        )


    # ========================================================
    # MOST LIKELY SCORES
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Most likely scores'
        '</div>',
        unsafe_allow_html=True,
    )


    for (
        probability,
        home_goals,
        away_goals,
    ) in probabilities["best_scores"]:

        st.markdown(
            f"""
            <div class="score-row">

                <div class="score-value">
                    {home_goals} — {away_goals}
                </div>

                <div class="score-probability">
                    {probability * 100:.2f}%
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        '<div class="model-info">'
        'Prediction generated by Football Engine'
        '</div>',
        unsafe_allow_html=True,
    )