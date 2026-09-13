// ============================================================
// FOOTBALL PREDICTOR — UI
// ============================================================


// ============================================================
// HELPERS
// ============================================================

function $(id) {
    return document.getElementById(id);
}


function formatPercent(value) {

    if (
        value === null ||
        value === undefined ||
        Number.isNaN(Number(value))
    ) {
        return "—";
    }

    return `${(Number(value) * 100).toFixed(1)}%`;
}


function formatXG(value) {

    if (
        value === null ||
        value === undefined ||
        Number.isNaN(Number(value))
    ) {
        return "—";
    }

    return Number(value).toFixed(2);
}


function getInitials(teamName) {

    if (!teamName) {
        return "?";
    }

    const words = teamName
        .trim()
        .split(/\s+/)
        .filter(Boolean);

    if (words.length === 1) {

        return words[0]
            .substring(0, 2)
            .toUpperCase();

    }

    return (
        words[0][0] +
        words[1][0]
    ).toUpperCase();
}


// ============================================================
// TEAM LOGOS
// ============================================================
//
// Пока используем аккуратные текстовые заглушки.
//
// Настоящие эмблемы подключим следующим шагом,
// когда основной интерфейс будет полностью разделён.
//

function setTeamLogo(elementId, teamName) {

    const element = $(elementId);

    if (!element) {
        return;
    }

    element.textContent =
        getInitials(teamName);

    element.classList.remove(
        "logo-image"
    );

    element.removeAttribute(
        "src"
    );
}


// ============================================================
// TEAM NAMES
// ============================================================

function setTeamNames(
    homeTeam,
    awayTeam
) {

    const homeName =
        $("home-name");

    const awayName =
        $("away-name");

    const homeXGTeam =
        $("home-xg-team");

    const awayXGTeam =
        $("away-xg-team");


    if (homeName) {
        homeName.textContent =
            homeTeam;
    }

    if (awayName) {
        awayName.textContent =
            awayTeam;
    }

    if (homeXGTeam) {
        homeXGTeam.textContent =
            homeTeam;
    }

    if (awayXGTeam) {
        awayXGTeam.textContent =
            awayTeam;
    }


    setTeamLogo(
        "home-logo",
        homeTeam
    );

    setTeamLogo(
        "away-logo",
        awayTeam
    );
}


// ============================================================
// MATCH DATE
// ============================================================

function setMatchDate(
    matchDate
) {

    const element =
        $("match-date-display");

    if (!element) {
        return;
    }

    if (!matchDate) {

        element.textContent =
            "";

        return;
    }

    const date =
        new Date(
            `${matchDate}T00:00:00`
        );

    if (Number.isNaN(date.getTime())) {

        element.textContent =
            matchDate;

        return;
    }

    element.textContent =
        date.toLocaleDateString(
            "en-GB",
            {
                day: "2-digit",
                month: "short",
                year: "numeric",
            }
        );
}


// ============================================================
// SHOW MATCH
// ============================================================

function showMatch(
    homeTeam,
    awayTeam,
    matchDate
) {

    setTeamNames(
        homeTeam,
        awayTeam
    );

    setMatchDate(
        matchDate
    );


    const matchCard =
        $("match-card");

    if (matchCard) {

        matchCard.classList.remove(
            "hidden"
        );
    }
}


// ============================================================
// SHOW / HIDE LOADING
// ============================================================

function showLoading() {

    const loading =
        $("loading");

    const results =
        $("results");


    if (loading) {

        loading.classList.remove(
            "hidden"
        );
    }

    if (results) {

        results.classList.add(
            "hidden"
        );
    }
}


function hideLoading() {

    const loading =
        $("loading");

    if (loading) {

        loading.classList.add(
            "hidden"
        );
    }
}


// ============================================================
// SHOW RESULTS
// ============================================================

function showResults() {

    const results =
        $("results");

    if (results) {

        results.classList.remove(
            "hidden"
        );
    }
}


// ============================================================
// 1X2
// ============================================================

function updateResultProbabilities(
    result
) {

    const homeWin =
        Number(result.home_win || 0);

    const draw =
        Number(result.draw || 0);

    const awayWin =
        Number(result.away_win || 0);


    // --------------------------------------------------------
    // TEXT
    // --------------------------------------------------------

    const homeElement =
        $("home-win");

    const drawElement =
        $("draw");

    const awayElement =
        $("away-win");


    if (homeElement) {

        homeElement.textContent =
            formatPercent(homeWin);
    }

    if (drawElement) {

        drawElement.textContent =
            formatPercent(draw);
    }

    if (awayElement) {

        awayElement.textContent =
            formatPercent(awayWin);
    }


    // --------------------------------------------------------
    // BARS
    // --------------------------------------------------------

    const homeBar =
        $("home-win-bar");

    const drawBar =
        $("draw-bar");

    const awayBar =
        $("away-win-bar");


    if (homeBar) {

        homeBar.style.width =
            `${homeWin * 100}%`;
    }

    if (drawBar) {

        drawBar.style.width =
            `${draw * 100}%`;
    }

    if (awayBar) {

        awayBar.style.width =
            `${awayWin * 100}%`;
    }


    // --------------------------------------------------------
    // MODEL PREDICTION
    // --------------------------------------------------------

    let predictionTeam =
        "Draw";

    let predictionProbability =
        draw;


    if (homeWin > predictionProbability) {

        predictionTeam =
            result.home_team;

        predictionProbability =
            homeWin;
    }


    if (awayWin > predictionProbability) {

        predictionTeam =
            result.away_team;

        predictionProbability =
            awayWin;
    }


    const predictionTeamElement =
        $("prediction-team");

    const predictionPercentElement =
        $("prediction-percent");


    if (predictionTeamElement) {

        predictionTeamElement.textContent =
            predictionTeam;
    }

    if (predictionPercentElement) {

        predictionPercentElement.textContent =
            formatPercent(
                predictionProbability
            );
    }
}


// ============================================================
// XG
// ============================================================

function updateXG(
    result
) {

    const homeXG =
        $("home-xg");

    const awayXG =
        $("away-xg");


    if (homeXG) {

        homeXG.textContent =
            formatXG(
                result.home_xg
            );
    }

    if (awayXG) {

        awayXG.textContent =
            formatXG(
                result.away_xg
            );
    }


    if ($("home-xg-team")) {

        $("home-xg-team").textContent =
            result.home_team;
    }

    if ($("away-xg-team")) {

        $("away-xg-team").textContent =
            result.away_team;
    }
}


// ============================================================
// GOALS
// ============================================================

function updateGoals(
    result
) {

    const over =
        $("over-25");

    const under =
        $("under-25");


    if (over) {

        over.textContent =
            formatPercent(
                result.over_25
            );
    }

    if (under) {

        under.textContent =
            formatPercent(
                result.under_25
            );
    }
}


// ============================================================
// BTTS
// ============================================================

function updateBTTS(
    result
) {

    const yes =
        $("btts-yes");

    const no =
        $("btts-no");


    if (yes) {

        yes.textContent =
            formatPercent(
                result.btts
            );
    }

    if (no) {

        no.textContent =
            formatPercent(
                result.no_btts
            );
    }
}


// ============================================================
// MOST LIKELY SCORES
// ============================================================

function updateScores(
    result
) {

    const container =
        $("scores");

    if (!container) {
        return;
    }


    container.innerHTML = "";


    const scores =
        result.best_scores;


    if (
        !Array.isArray(scores) ||
        scores.length === 0
    ) {

        container.innerHTML = `
            <div class="no-data">
                No score data
            </div>
        `;

        return;
    }


    scores.forEach(
        (score, index) => {

            const row =
                document.createElement(
                    "div"
                );

            row.className =
                "score-row";


            if (index === 0) {

                row.classList.add(
                    "top-score"
                );
            }


            const scoreValue =
                document.createElement(
                    "div"
                );

            scoreValue.className =
                "score-value";


            scoreValue.textContent =
                `${score.home_goals}-${score.away_goals}`;


            const probability =
                document.createElement(
                    "div"
                );

            probability.className =
                "score-probability";


            probability.textContent =
                formatPercent(
                    score.probability
                );


            row.appendChild(
                scoreValue
            );

            row.appendChild(
                probability
            );


            container.appendChild(
                row
            );

        }
    );
}


// ============================================================
// COMPLETE RESULT UPDATE
// ============================================================

function updatePredictionUI(
    result,
    matchDate = null
) {

    setTeamNames(
        result.home_team,
        result.away_team
    );

    setMatchDate(
        matchDate
    );

    updateResultProbabilities(
        result
    );

    updateXG(
        result
    );

    updateGoals(
        result
    );

    updateBTTS(
        result
    );

    updateScores(
        result
    );

    showMatch(
        result.home_team,
        result.away_team,
        matchDate
    );

    showResults();

    hideLoading();
}


// ============================================================
// ERROR
// ============================================================

function showError(
    message
) {

    hideLoading();

    alert(
        message || "Something went wrong."
    );
}