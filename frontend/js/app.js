// ============================================================
// FOOTBALL PREDICTOR — APP
// ============================================================


// ============================================================
// DOM
// ============================================================

const homeSearchInput =
    document.getElementById("home-team-search");

const awaySearchInput =
    document.getElementById("away-team-search");


const homeTeamInput =
    document.getElementById("home-team");

const awayTeamInput =
    document.getElementById("away-team");


const homeResults =
    document.getElementById("home-team-results");

const awayResults =
    document.getElementById("away-team-results");


const matchDateInput =
    document.getElementById("match-date");

const predictButton =
    document.getElementById("predict-button");


// ============================================================
// SEARCH STATE
// ============================================================

let homeSearchTimeout = null;
let awaySearchTimeout = null;


// ============================================================
// INITIALIZATION
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    init
);


async function init() {

    setupTeamSearch(
        homeSearchInput,
        homeTeamInput,
        homeResults,
        "home"
    );


    setupTeamSearch(
        awaySearchInput,
        awayTeamInput,
        awayResults,
        "away"
    );


    if (predictButton) {

        predictButton.addEventListener(
            "click",
            handlePrediction
        );

    }


    document.addEventListener(
        "click",
        handleOutsideClick
    );

    setupPredictionHistory();
}


// ============================================================
// TEAM SEARCH
// ============================================================

function setupTeamSearch(
    input,
    hiddenInput,
    resultsContainer,
    side
) {

    if (
        !input ||
        !hiddenInput ||
        !resultsContainer
    ) {
        return;
    }


    input.addEventListener(
        "input",
        () => {

            const query =
                input.value.trim();


            // ------------------------------------------------
            // User changed the text.
            // Therefore previous selection is invalid.
            // ------------------------------------------------

            hiddenInput.value = "";


            if (query.length === 0) {

                hideResults(
                    resultsContainer
                );

                return;
            }


            clearTimeout(
                side === "home"
                    ? homeSearchTimeout
                    : awaySearchTimeout
            );


            const timeout =
                setTimeout(
                    () => {

                        searchTeams(
                            query,
                            resultsContainer,
                            input,
                            hiddenInput
                        );

                    },
                    150
                );


            if (side === "home") {

                homeSearchTimeout =
                    timeout;

            } else {

                awaySearchTimeout =
                    timeout;

            }

        }
    );


    input.addEventListener(
        "focus",
        () => {

            const query =
                input.value.trim();


            if (query.length > 0) {

                searchTeams(
                    query,
                    resultsContainer,
                    input,
                    hiddenInput
                );

            }

        }
    );


    input.addEventListener(
        "keydown",
        event => {

            if (
                event.key === "Escape"
            ) {

                hideResults(
                    resultsContainer
                );

                input.blur();

            }

        }
    );
}


// ============================================================
// SEARCH API
// ============================================================

async function searchTeams(
    query,
    resultsContainer,
    input,
    hiddenInput
) {

    try {

        const teams =
            await getTeams(query);


        renderTeamResults(
            teams,
            resultsContainer,
            input,
            hiddenInput
        );


    } catch (error) {

        console.error(
            "Team search error:",
            error
        );


        resultsContainer.innerHTML = `
            <div class="team-no-results">
                Search error
            </div>
        `;


        resultsContainer.classList.remove(
            "hidden"
        );

    }
}


// ============================================================
// RENDER SEARCH RESULTS
// ============================================================

function renderTeamResults(
    teams,
    resultsContainer,
    input,
    hiddenInput
) {

    resultsContainer.innerHTML = "";


    if (
        !Array.isArray(teams) ||
        teams.length === 0
    ) {

        resultsContainer.innerHTML = `
            <div class="team-no-results">
                Team not found
            </div>
        `;


        resultsContainer.classList.remove(
            "hidden"
        );


        return;
    }


    // Limit dropdown size
    const visibleTeams =
        teams.slice(0, 10);


    visibleTeams.forEach(
        team => {

            const button =
                document.createElement(
                    "button"
                );


            button.type = "button";

            button.className =
                "team-result";


            // ====================================================
            // LOGO
            // ====================================================

            const logoContainer =
                document.createElement(
                    "div"
                );

            logoContainer.className =
                "team-result-logo";


            if (team.logo) {

                const logo =
                    document.createElement(
                        "img"
                    );

                logo.src =
                    team.logo;

                logo.alt =
                    `${team.name} logo`;

                logo.loading =
                    "eager";


                logo.onerror =
                    () => {

                        logo.remove();

                        logoContainer.textContent =
                            "⚽";

                    };


                logoContainer.appendChild(
                    logo
                );

            } else {

                logoContainer.textContent =
                    "⚽";

            }


            // ====================================================
            // CONTENT
            // ====================================================

            const content =
                document.createElement(
                    "div"
                );

            content.className =
                "team-result-content";


            // ----------------------------------------------------
            // TEAM NAME
            // ----------------------------------------------------

            const name =
                document.createElement(
                    "div"
                );

            name.className =
                "team-result-name";

            name.textContent =
                team.name;


            // ----------------------------------------------------
            // LEAGUE
            // ----------------------------------------------------

            const meta =
                document.createElement(
                    "div"
                );

            meta.className =
                "team-result-meta";

            meta.textContent =
                team.league || "";


            content.appendChild(
                name
            );

            if (team.league) {

                content.appendChild(
                    meta
                );

            }


            // ====================================================
            // BUILD RESULT
            // ====================================================

            button.appendChild(
                logoContainer
            );

            button.appendChild(
                content
            );


            // ====================================================
            // SELECT TEAM
            // ====================================================

            button.addEventListener(
                "click",
                event => {

                    event.preventDefault();

                    event.stopPropagation();


                    selectTeam(
                        team,
                        input,
                        hiddenInput,
                        resultsContainer
                    );

                }
            );


            resultsContainer.appendChild(
                button
            );

        }
    );


    resultsContainer.classList.remove(
        "hidden"
    );
}


// ============================================================
// SELECT TEAM
// ============================================================

function selectTeam(
    team,
    input,
    hiddenInput,
    resultsContainer
) {

    // Visible value
    input.value =
        team.name;


    // Actual canonical value
    hiddenInput.value =
        team.name;


    // Save useful metadata
    input.dataset.teamName =
        team.name;

    input.dataset.teamLeague =
        team.league || "";

    input.dataset.teamCountry =
        team.country || "";

    input.dataset.teamLogo =
        team.logo || "";


    hideResults(
        resultsContainer
    );


    input.blur();
}


// ============================================================
// HIDE RESULTS
// ============================================================

function hideResults(
    resultsContainer
) {

    if (!resultsContainer) {
        return;
    }


    resultsContainer.classList.add(
        "hidden"
    );
}


// ============================================================
// OUTSIDE CLICK
// ============================================================

function handleOutsideClick(
    event
) {

    if (
        !event.target.closest(
            ".team-search"
        )
    ) {

        hideResults(
            homeResults
        );

        hideResults(
            awayResults
        );

    }
}


// ============================================================
// PREDICTION
// ============================================================

async function handlePrediction() {

    const homeTeam =
        homeTeamInput
            ? homeTeamInput.value
            : "";


    const awayTeam =
        awayTeamInput
            ? awayTeamInput.value
            : "";


    const matchDate =
        matchDateInput
            ? matchDateInput.value
            : "";


    // ========================================================
    // VALIDATION
    // ========================================================

    if (!homeTeam) {

        showError(
            "Выберите домашнюю команду из списка."
        );


        if (homeSearchInput) {

            homeSearchInput.focus();

        }


        return;
    }


    if (!awayTeam) {

        showError(
            "Выберите гостевую команду из списка."
        );


        if (awaySearchInput) {

            awaySearchInput.focus();

        }


        return;
    }


    if (
        homeTeam === awayTeam
    ) {

        showError(
            "Домашняя и гостевая команды должны различаться."
        );


        return;
    }


    // ========================================================
    // LOADING
    // ========================================================

    setButtonLoading(
        true
    );


    showLoading();


    try {

        const result =
            await predictMatch(
                homeTeam,
                awayTeam,
                matchDate || null
            );


        updatePredictionUI(
            result,
            matchDate || null
        );

        savePredictionToHistory(
            result,
            matchDate || null
        );

        renderPredictionHistory();


    } catch (error) {

        console.error(
            "Prediction error:",
            error
        );


        showError(
            error.message ||
            "Не удалось получить прогноз."
        );


    } finally {

        setButtonLoading(
            false
        );

    }
}


// ============================================================
// BUTTON LOADING
// ============================================================

function setButtonLoading(
    loading
) {

    if (!predictButton) {
        return;
    }


    if (loading) {

        predictButton.disabled =
            true;


        predictButton.dataset
            .originalText =
            predictButton.textContent;


        predictButton.textContent =
            "CALCULATING...";


    } else {

        predictButton.disabled =
            false;


        predictButton.textContent =
            predictButton.dataset
                .originalText ||
            "PREDICT MATCH";

    }
}


// ============================================================
// ENTER KEY
// ============================================================

document.addEventListener(
    "keydown",
    event => {

        if (
            event.key !== "Enter"
        ) {
            return;
        }


        const activeElement =
            document.activeElement;


        if (
            activeElement ===
            homeSearchInput
        ) {

            const firstResult =
                homeResults
                    ?.querySelector(
                        ".team-result"
                    );


            if (firstResult) {

                event.preventDefault();

                firstResult.click();

            }


            return;
        }


        if (
            activeElement ===
            awaySearchInput
        ) {

            const firstResult =
                awayResults
                    ?.querySelector(
                        ".team-result"
                    );


            if (firstResult) {

                event.preventDefault();

                firstResult.click();

            }


            return;
        }


        if (
            activeElement &&
            (
                activeElement.tagName ===
                "INPUT"
            )
        ) {

            event.preventDefault();

            handlePrediction();

        }

    }
);

/* ============================================================
   PREDICTION RESULT UI
============================================================ */

let predictionResultElement = null;

function ensurePredictionResultUI() {
    if (predictionResultElement) return predictionResultElement;

    predictionResultElement = document.createElement("section");
    predictionResultElement.id = "prediction-result";
    predictionResultElement.className = "prediction-result hidden";

    predictionResultElement.innerHTML = `
        <div class="prediction-result-card">
            <div class="prediction-result-header">
                <div>
                    <div class="prediction-result-kicker">MATCH PREDICTION</div>
                    <h2 class="prediction-result-title">Prediction</h2>
                </div>
                <button type="button" class="prediction-result-close" aria-label="Close">×</button>
            </div>

            <div class="prediction-teams">
                <div class="prediction-team">
                    <div class="prediction-team-logo home-logo"></div>
                    <div class="prediction-team-name home-name"></div>
                    <div class="prediction-team-league home-league"></div>
                </div>
                <div class="prediction-vs">VS</div>
                <div class="prediction-team">
                    <div class="prediction-team-logo away-logo"></div>
                    <div class="prediction-team-name away-name"></div>
                    <div class="prediction-team-league away-league"></div>
                </div>
            </div>

            <div class="prediction-main-outcome">
                <div class="prediction-main-label">MOST LIKELY OUTCOME</div>
                <div class="prediction-main-value">—</div>
                <div class="prediction-main-probability">—</div>
            </div>

            <div class="prediction-probabilities">
                <div class="prediction-probability"><span>HOME WIN</span><strong class="home-win">—</strong></div>
                <div class="prediction-probability"><span>DRAW</span><strong class="draw">—</strong></div>
                <div class="prediction-probability"><span>AWAY WIN</span><strong class="away-win">—</strong></div>
            </div>

            <div class="prediction-probability-bar">
                <div class="bar-home"></div>
                <div class="bar-draw"></div>
                <div class="bar-away"></div>
            </div>

            <div class="prediction-section">
                <div class="prediction-section-title">EXPECTED GOALS</div>
                <div class="prediction-xg-grid">
                    <div class="prediction-xg"><span>HOME</span><strong class="home-xg">—</strong></div>
                    <div class="prediction-xg"><span>AWAY</span><strong class="away-xg">—</strong></div>
                </div>
            </div>

            <div class="prediction-section">
                <div class="prediction-section-title">MOST LIKELY SCORES</div>
                <div class="prediction-scores"></div>
            </div>

            <div class="prediction-stats">
                <div class="prediction-stat"><span>OVER 2.5</span><strong class="over25">—</strong></div>
                <div class="prediction-stat"><span>BTTS</span><strong class="btts">—</strong></div>
            </div>

            <div class="prediction-analysis">
                <div class="prediction-section-title">MATCH ANALYSIS</div>

                <div class="analysis-headline">
                    <div class="analysis-headline-label">MODEL VIEW</div>
                    <strong class="analysis-headline-value">—</strong>
                </div>

                <div class="analysis-grid">
                    <div class="analysis-item">
                        <div class="analysis-item-top">
                            <span>EXPECTED GOALS</span>
                            <strong class="analysis-xg-diff">—</strong>
                        </div>
                        <div class="analysis-bars">
                            <div class="analysis-bar-row">
                                <span class="analysis-team home-analysis-name">HOME</span>
                                <div class="analysis-bar-track">
                                    <div class="analysis-bar home-analysis-bar"></div>
                                </div>
                                <strong class="home-analysis-xg">—</strong>
                            </div>
                            <div class="analysis-bar-row">
                                <span class="analysis-team away-analysis-name">AWAY</span>
                                <div class="analysis-bar-track">
                                    <div class="analysis-bar away-analysis-bar"></div>
                                </div>
                                <strong class="away-analysis-xg">—</strong>
                            </div>
                        </div>
                    </div>

                    <div class="analysis-item analysis-confidence">
                        <div class="analysis-item-top">
                            <span>WIN PROBABILITY</span>
                            <strong class="analysis-confidence-value">—</strong>
                        </div>
                        <p class="analysis-description"></p>
                    </div>
                </div>
            </div>

            <div class="prediction-date"></div>
        </div>
    `;

    predictionResultElement.querySelector(".prediction-result-close")
        .addEventListener("click", () => {
            predictionResultElement.classList.add("hidden");
        });

    injectPredictionStyles();

    const anchor = predictButton?.closest("form") || predictButton?.parentElement;
    if (anchor?.parentElement) {
        anchor.parentElement.insertBefore(predictionResultElement, anchor.nextSibling);
    } else {
        document.body.appendChild(predictionResultElement);
    }

    return predictionResultElement;
}

function injectPredictionStyles() {
    if (document.getElementById("prediction-result-styles")) return;

    const style = document.createElement("style");
    style.id = "prediction-result-styles";

    style.textContent = `
        .prediction-result{width:100%;margin:28px 0 0;box-sizing:border-box}
        .prediction-result.hidden{display:none!important}
        .prediction-result-card{box-sizing:border-box;width:100%;padding:28px;border:1px solid #e8e9ec;border-radius:24px;background:#fff;box-shadow:0 12px 40px rgba(20,24,32,.08);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#17191d}
        .prediction-result-header{display:flex;justify-content:space-between;gap:20px;margin-bottom:28px}
        .prediction-result-kicker{margin-bottom:5px;color:#8b8f98;font-size:11px;font-weight:700;letter-spacing:.14em}
        .prediction-result-title{margin:0;font-size:24px;line-height:1.15;font-weight:700;letter-spacing:-.03em}
        .prediction-result-close{width:36px;height:36px;border:0;border-radius:50%;background:#f3f4f6;color:#666a72;font-size:23px;cursor:pointer}
        .prediction-teams{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);align-items:center;gap:20px;padding:22px 0 26px;border-top:1px solid #eceef1;border-bottom:1px solid #eceef1}
        .prediction-team{text-align:center;min-width:0}
        .prediction-team-logo{width:72px;height:72px;margin:0 auto 12px;display:flex;align-items:center;justify-content:center;font-size:38px}
        .prediction-team-logo img{width:100%;height:100%;object-fit:contain}
        .prediction-team-name{font-size:17px;line-height:1.25;font-weight:700;word-break:break-word}
        .prediction-team-league{margin-top:4px;color:#858991;font-size:12px;font-style:italic}
        .prediction-vs{color:#a0a3aa;font-size:12px;font-weight:700;letter-spacing:.08em}
        .prediction-main-outcome{text-align:center;padding:28px 10px 24px}
        .prediction-main-label{margin-bottom:7px;color:#8a8e97;font-size:11px;font-weight:700;letter-spacing:.12em}
        .prediction-main-value{font-size:28px;font-weight:800;letter-spacing:-.04em}
        .prediction-main-probability{margin-top:5px;color:#555961;font-size:15px;font-weight:600}
        .prediction-probabilities{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
        .prediction-probability,.prediction-xg,.prediction-stat,.prediction-score{background:#f7f7f8;border-radius:14px;text-align:center}
        .prediction-probability{padding:15px 12px}
        .prediction-probability span,.prediction-stat span,.prediction-xg span{display:block;margin-bottom:5px;color:#858991;font-size:10px;font-weight:700;letter-spacing:.08em}
        .prediction-probability strong{font-size:19px}
        .prediction-probability-bar{display:flex;width:100%;height:8px;margin:10px 0 28px;overflow:hidden;border-radius:999px;background:#eceef1}
        .bar-home,.bar-draw,.bar-away{height:100%}
        .bar-home{background:#17191d}.bar-draw{background:#aeb2b9}.bar-away{background:#d9dbe0}
        .prediction-section{padding:22px 0;border-top:1px solid #eceef1}
        .prediction-section-title{margin-bottom:14px;color:#858991;font-size:10px;font-weight:700;letter-spacing:.1em}
        .prediction-xg-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
        .prediction-xg{padding:18px}
        .prediction-xg strong{font-size:28px}
        .prediction-scores{display:grid;grid-template-columns:repeat(5,1fr);gap:8px}
        .prediction-score{padding:13px 8px}
        .prediction-score-value{display:block;font-size:18px;font-weight:800}
        .prediction-score-probability{display:block;margin-top:4px;color:#858991;font-size:10px}
        .prediction-stats{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding-top:22px;border-top:1px solid #eceef1}
        .prediction-stat{padding:17px}
        .prediction-stat strong{font-size:21px}
        .prediction-date{margin-top:20px;color:#999ca3;font-size:11px;text-align:center}
        .prediction-analysis {
            margin-top: 22px;
            padding-top: 22px;
            border-top: 1px solid #eceef1;
        }

        .analysis-headline {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 14px;
            padding: 17px 18px;
            border-radius: 16px;
            background: #f7f7f8;
        }

        .analysis-headline-label {
            color: #858991;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: .08em;
        }

        .analysis-headline-value {
            font-size: 17px;
            font-weight: 800;
            text-align: right;
        }

        .analysis-grid {
            display: grid;
            grid-template-columns: 1.4fr 1fr;
            gap: 12px;
        }

        .analysis-item {
            min-width: 0;
            padding: 18px;
            border-radius: 16px;
            background: #f7f7f8;
        }

        .analysis-item-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 16px;
        }

        .analysis-item-top > span {
            color: #858991;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: .08em;
        }

        .analysis-item-top > strong {
            font-size: 13px;
            font-weight: 800;
        }

        .analysis-bar-row {
            display: grid;
            grid-template-columns: 78px minmax(0, 1fr) 40px;
            align-items: center;
            gap: 9px;
            margin-top: 11px;
        }

        .analysis-team {
            overflow: hidden;
            color: #555961;
            font-size: 10px;
            font-weight: 700;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .analysis-bar-track {
            height: 7px;
            overflow: hidden;
            border-radius: 999px;
            background: #e2e4e8;
        }

        .analysis-bar {
            height: 100%;
            border-radius: 999px;
            background: #17191d;
            transition: width .45s ease;
        }

        .away-analysis-bar {
            background: #9ea3ab;
        }

        .analysis-bar-row > strong {
            font-size: 12px;
            text-align: right;
        }

        .analysis-description {
            margin: 0;
            color: #555961;
            font-size: 13px;
            line-height: 1.55;
        }

        @media(max-width:640px){
            .analysis-grid {
                grid-template-columns: 1fr;
            }

            .analysis-bar-row {
                grid-template-columns: 70px minmax(0, 1fr) 38px;
            }

            .analysis-headline {
                align-items: flex-start;
                flex-direction: column;
                gap: 5px;
            }

            .analysis-headline-value {
                text-align: left;
            }

            .prediction-result-card{padding:20px;border-radius:20px}
            .prediction-result-title{font-size:21px}
            .prediction-teams{gap:8px}
            .prediction-team-logo{width:56px;height:56px;font-size:30px}
            .prediction-team-name{font-size:14px}
            .prediction-probabilities{gap:6px}
            .prediction-probability{padding:13px 5px}
            .prediction-probability strong{font-size:16px}
            .prediction-scores{grid-template-columns:repeat(3,1fr)}
        }
    `;

    document.head.appendChild(style);
}

function predictionPercent(value) {
    if (value === null || value === undefined || value === "") return "—";
    let n = Number(value);
    if (!Number.isFinite(n)) return "—";
    if (n <= 1) n *= 100;
    return `${n.toFixed(1)}%`;
}

function predictionNumber(value) {
    if (value === null || value === undefined || value === "") return "—";
    const n = Number(value);
    return Number.isFinite(n) ? n.toFixed(2) : "—";
}

function predictionValue(result, keys) {
    for (const key of keys) {
        if (result && result[key] !== undefined && result[key] !== null) {
            return result[key];
        }
    }
    return null;
}

function predictionScores(result) {
    const raw = predictionValue(result, ["top_scores", "likely_scores", "most_likely_scores"]);
    if (!raw) return [];

    if (Array.isArray(raw)) return raw.slice(0, 5);

    if (typeof raw === "object") {
        return Object.entries(raw)
            .map(([score, probability]) => ({score, probability}))
            .sort((a,b) => Number(b.probability || 0) - Number(a.probability || 0))
            .slice(0,5);
    }

    return [];
}

function normalizePredictionScore(raw) {
    if (typeof raw === "string") return {score:raw, probability:null};

    if (Array.isArray(raw)) {
        return {
            score: raw.length >= 2 ? `${raw[0]}-${raw[1]}` : String(raw[0] ?? "—"),
            probability: raw.length >= 3 ? raw[2] : null
        };
    }

    if (raw && typeof raw === "object") {
        const score = raw.score ?? raw.result ?? raw.name ??
            (raw.home_score !== undefined && raw.away_score !== undefined
                ? `${raw.home_score}-${raw.away_score}` : "—");

        return {
            score,
            probability: raw.probability ?? raw.prob ?? raw.percentage ?? null
        };
    }

    return {score:String(raw ?? "—"), probability:null};
}

function setPredictionLogo(container, url) {
    container.innerHTML = "";

    if (!url) {
        container.textContent = "⚽";
        return;
    }

    // /predict currently returns the original SofaScore URL.
    // Convert it to our same-origin proxy to avoid browser CORS/ORB blocking.
    const proxyMatch = String(url).match(
        /\/api\/v1\/team\/(\d+)\/image/
    );

    const finalUrl = proxyMatch
        ? `/team-logo/${proxyMatch[1]}`
        : url;

    const img = document.createElement("img");
    img.src = finalUrl;
    img.alt = "";
    img.loading = "eager";

    img.onerror = () => {
        container.innerHTML = "⚽";
    };

    container.appendChild(img);
}

function calculateOver25FromXG(homeXg, awayXg) {
    const h = Number(homeXg);
    const a = Number(awayXg);

    if (!Number.isFinite(h) || !Number.isFinite(a) || h < 0 || a < 0) {
        return null;
    }

    const total = h + a;

    // P(Total <= 2) for a Poisson(total) distribution.
    const under25 =
        Math.exp(-total) *
        (1 + total + (total * total) / 2);

    return 1 - under25;
}

function calculateBTTSFromXG(homeXg, awayXg) {
    const h = Number(homeXg);
    const a = Number(awayXg);

    if (!Number.isFinite(h) || !Number.isFinite(a) || h < 0 || a < 0) {
        return null;
    }

    return (1 - Math.exp(-h)) * (1 - Math.exp(-a));
}

function updatePredictionUI(result, matchDate = null) {
    const panel = ensurePredictionResultUI();

    const homeName = predictionValue(result, ["home_team"]) || homeTeamInput?.value || "Home";
    const awayName = predictionValue(result, ["away_team"]) || awayTeamInput?.value || "Away";

    const homeWin = predictionValue(result, ["home_win", "home_win_probability"]);
    const draw = predictionValue(result, ["draw", "draw_probability"]);
    const awayWin = predictionValue(result, ["away_win", "away_win_probability"]);

    const homePercent = Number(homeWin || 0) <= 1 ? Number(homeWin || 0) * 100 : Number(homeWin || 0);
    const drawPercent = Number(draw || 0) <= 1 ? Number(draw || 0) * 100 : Number(draw || 0);
    const awayPercent = Number(awayWin || 0) <= 1 ? Number(awayWin || 0) * 100 : Number(awayWin || 0);

    const outcomes = [
        {name:homeName, value:homePercent},
        {name:"DRAW", value:drawPercent},
        {name:awayName, value:awayPercent}
    ];

    const best = outcomes.reduce((a,b) => b.value > a.value ? b : a, outcomes[0]);

    panel.querySelector(".prediction-result-title").textContent = `${homeName} vs ${awayName}`;
    panel.querySelector(".home-name").textContent = homeName;
    panel.querySelector(".away-name").textContent = awayName;

    panel.querySelector(".home-league").textContent =
        predictionValue(result, ["home_league"]) || homeSearchInput?.dataset?.teamLeague || "";

    panel.querySelector(".away-league").textContent =
        predictionValue(result, ["away_league"]) || awaySearchInput?.dataset?.teamLeague || "";

    setPredictionLogo(
        panel.querySelector(".home-logo"),
        predictionValue(result, ["home_logo"]) || homeSearchInput?.dataset?.teamLogo || ""
    );

    setPredictionLogo(
        panel.querySelector(".away-logo"),
        predictionValue(result, ["away_logo"]) || awaySearchInput?.dataset?.teamLogo || ""
    );

    panel.querySelector(".prediction-main-value").textContent = best.name;
    panel.querySelector(".prediction-main-probability").textContent = predictionPercent(best.value);

    panel.querySelector(".home-win").textContent = predictionPercent(homeWin);
    panel.querySelector(".draw").textContent = predictionPercent(draw);
    panel.querySelector(".away-win").textContent = predictionPercent(awayWin);

    panel.querySelector(".bar-home").style.width = `${Math.max(0,Math.min(100,homePercent))}%`;
    panel.querySelector(".bar-draw").style.width = `${Math.max(0,Math.min(100,drawPercent))}%`;
    panel.querySelector(".bar-away").style.width = `${Math.max(0,Math.min(100,awayPercent))}%`;

    const homeXg = predictionValue(
        result,
        ["home_xg", "home_expected_goals", "xg_home"]
    );

    const awayXg = predictionValue(
        result,
        ["away_xg", "away_expected_goals", "xg_away"]
    );

    panel.querySelector(".home-xg").textContent =
        predictionNumber(homeXg);

    panel.querySelector(".away-xg").textContent =
        predictionNumber(awayXg);

    const scores = panel.querySelector(".prediction-scores");
    scores.innerHTML = "";

    predictionScores(result).forEach(raw => {
        const item = normalizePredictionScore(raw);

        const div = document.createElement("div");
        div.className = "prediction-score";

        const score = document.createElement("span");
        score.className = "prediction-score-value";
        score.textContent = item.score;
        div.appendChild(score);

        if (item.probability !== null) {
            const probability = document.createElement("span");
            probability.className = "prediction-score-probability";
            probability.textContent = predictionPercent(item.probability);
            div.appendChild(probability);
        }

        scores.appendChild(div);
    });

    if (!scores.children.length) {
        scores.innerHTML =
            `<div class="prediction-score"><span class="prediction-score-value">—</span></div>`;
    }

    const over25FromAPI = predictionValue(
        result,
        ["over_2_5", "over25", "over_2_5_probability"]
    );

    const bttsFromAPI = predictionValue(
        result,
        ["btts", "btts_probability"]
    );

    const over25 = over25FromAPI !== null
        ? over25FromAPI
        : calculateOver25FromXG(homeXg, awayXg);

    const btts = bttsFromAPI !== null
        ? bttsFromAPI
        : calculateBTTSFromXG(homeXg, awayXg);

    panel.querySelector(".over25").textContent =
        predictionPercent(over25);

    panel.querySelector(".btts").textContent =
        predictionPercent(btts);

    // ========================================================
    // MATCH ANALYSIS
    // ========================================================

    const safeHomeXg = Number(homeXg);
    const safeAwayXg = Number(awayXg);
    const xgDiff = safeHomeXg - safeAwayXg;

    const analysisHeadline = panel.querySelector(
        ".analysis-headline-value"
    );

    const analysisDescription = panel.querySelector(
        ".analysis-description"
    );

    const xgDiffElement = panel.querySelector(
        ".analysis-xg-diff"
    );

    const homeAnalysisBar = panel.querySelector(
        ".home-analysis-bar"
    );

    const awayAnalysisBar = panel.querySelector(
        ".away-analysis-bar"
    );

    panel.querySelector(
        ".home-analysis-name"
    ).textContent = homeName;

    panel.querySelector(
        ".away-analysis-name"
    ).textContent = awayName;

    panel.querySelector(
        ".home-analysis-xg"
    ).textContent = predictionNumber(homeXg);

    panel.querySelector(
        ".away-analysis-xg"
    ).textContent = predictionNumber(awayXg);

    if (
        Number.isFinite(safeHomeXg) &&
        Number.isFinite(safeAwayXg)
    ) {
        const totalXg = safeHomeXg + safeAwayXg;

        const homeWidth =
            totalXg > 0
                ? (safeHomeXg / totalXg) * 100
                : 50;

        const awayWidth =
            totalXg > 0
                ? (safeAwayXg / totalXg) * 100
                : 50;

        homeAnalysisBar.style.width =
            `${Math.max(0, Math.min(100, homeWidth))}%`;

        awayAnalysisBar.style.width =
            `${Math.max(0, Math.min(100, awayWidth))}%`;

        xgDiffElement.textContent =
            `${xgDiff >= 0 ? "+" : ""}${xgDiff.toFixed(2)} xG`;

        const favoriteProbability =
            Math.max(
                homePercent,
                drawPercent,
                awayPercent
            );

        panel.querySelector(
            ".analysis-confidence-value"
        ).textContent =
            predictionPercent(favoriteProbability);

        if (best.name === "DRAW") {
            analysisHeadline.textContent =
                "The model expects a balanced match";

            analysisDescription.textContent =
                `The win probabilities are relatively close, with a ${favoriteProbability.toFixed(1)}% highest outcome probability. Expected goals are ${safeHomeXg.toFixed(2)} for ${homeName} and ${safeAwayXg.toFixed(2)} for ${awayName}.`;
        } else {
            analysisHeadline.textContent =
                `${best.name} have the advantage`;

            const xgLeader =
                safeHomeXg > safeAwayXg
                    ? homeName
                    : safeAwayXg > safeHomeXg
                        ? awayName
                        : "Neither team";

            analysisDescription.textContent =
                `${xgLeader} have the higher expected-goals output. The model gives ${best.name} a ${best.value.toFixed(1)}% probability of the most likely outcome, with expected goals of ${safeHomeXg.toFixed(2)}–${safeAwayXg.toFixed(2)}.`;
        }
    } else {
        xgDiffElement.textContent = "—";
        homeAnalysisBar.style.width = "50%";
        awayAnalysisBar.style.width = "50%";
        panel.querySelector(
            ".analysis-confidence-value"
        ).textContent = "—";
        analysisHeadline.textContent =
            "Analysis unavailable";
        analysisDescription.textContent =
            "There is not enough model data to generate the analysis.";
    }

    panel.querySelector(".prediction-date").textContent =
        matchDate ? `Match date: ${matchDate}` : "";

    panel.classList.remove("hidden");

    requestAnimationFrame(() => {
        panel.scrollIntoView({behavior:"smooth", block:"start"});
    });
}

function showLoading() {
    const panel = ensurePredictionResultUI();

    panel.classList.remove("hidden");
    panel.querySelector(".prediction-result-title").textContent = "Calculating prediction...";
    panel.querySelector(".prediction-main-value").textContent = "—";
    panel.querySelector(".prediction-main-probability").textContent = "Please wait";

    panel.querySelector(".prediction-scores").innerHTML =
        `<div class="prediction-score"><span class="prediction-score-value">...</span></div>`;

    const analysisHeadline = panel.querySelector(".analysis-headline-value");
    const analysisDescription = panel.querySelector(".analysis-description");

    if (analysisHeadline) {
        analysisHeadline.textContent = "Calculating...";
    }

    if (analysisDescription) {
        analysisDescription.textContent = "Analyzing the available model data...";
    }
}

function showError(message) {
    const panel = ensurePredictionResultUI();

    panel.classList.remove("hidden");
    panel.querySelector(".prediction-result-title").textContent = "Prediction error";
    panel.querySelector(".prediction-main-value").textContent = "Something went wrong";
    panel.querySelector(".prediction-main-probability").textContent =
        message || "Please try again.";

    panel.querySelector(".prediction-scores").innerHTML = "";
}

// ============================================================
// PREDICTION HISTORY
// ============================================================

const PREDICTION_HISTORY_KEY =
    "football_prediction_history_v1";

const MAX_PREDICTION_HISTORY =
    20;

let predictionHistoryElement =
    null;


function readPredictionHistory() {
    try {
        const raw =
            localStorage.getItem(
                PREDICTION_HISTORY_KEY
            );

        if (!raw) {
            return [];
        }

        const history =
            JSON.parse(raw);

        return Array.isArray(history)
            ? history
            : [];
    } catch (error) {
        console.error(
            "Could not read prediction history:",
            error
        );

        return [];
    }
}


function writePredictionHistory(history) {
    try {
        localStorage.setItem(
            PREDICTION_HISTORY_KEY,
            JSON.stringify(history)
        );
    } catch (error) {
        console.error(
            "Could not save prediction history:",
            error
        );
    }
}


function savePredictionToHistory(
    result,
    matchDate = null
) {
    if (!result) {
        return;
    }

    const homeTeam =
        result.home_team ||
        homeTeamInput?.value ||
        "";

    const awayTeam =
        result.away_team ||
        awayTeamInput?.value ||
        "";

    if (!homeTeam || !awayTeam) {
        return;
    }

    const history =
        readPredictionHistory();

    const entry = {
        id:
            `${Date.now()}_${Math.random()
                .toString(36)
                .slice(2, 8)}`,

        created_at:
            new Date().toISOString(),

        match_date:
            matchDate || null,

        home_team:
            homeTeam,

        away_team:
            awayTeam,

        home_logo:
            result.home_logo || "",

        away_logo:
            result.away_logo || "",

        home_league:
            result.home_league || "",

        away_league:
            result.away_league || "",

        home_win:
            result.home_win ?? null,

        draw:
            result.draw ?? null,

        away_win:
            result.away_win ?? null,

        home_xg:
            result.home_xg ?? null,

        away_xg:
            result.away_xg ?? null,

        top_scores:
            Array.isArray(result.top_scores)
                ? result.top_scores.slice(0, 5)
                : [],

        over25:
            result.over_2_5 ??
            result.over25 ??
            null,

        btts:
            result.btts ??
            null,
    };

    // Remove the immediately duplicated match/date.
    const filtered =
        history.filter(item =>
            !(
                item.home_team === entry.home_team &&
                item.away_team === entry.away_team &&
                item.match_date === entry.match_date
            )
        );

    filtered.unshift(entry);

    writePredictionHistory(
        filtered.slice(
            0,
            MAX_PREDICTION_HISTORY
        )
    );
}


function setupPredictionHistory() {
    if (predictionHistoryElement) {
        renderPredictionHistory();
        return;
    }

    predictionHistoryElement =
        document.createElement("section");

    predictionHistoryElement.id =
        "prediction-history";

    predictionHistoryElement.className =
        "prediction-history";

    predictionHistoryElement.innerHTML = `
        <div class="prediction-history-header">
            <div>
                <div class="prediction-history-kicker">
                    RECENT
                </div>
                <h2 class="prediction-history-title">
                    Prediction History
                </h2>
            </div>

            <button
                type="button"
                class="prediction-history-clear"
            >
                Clear
            </button>
        </div>

        <div class="prediction-history-list"></div>
    `;

    predictionHistoryElement
        .querySelector(
            ".prediction-history-clear"
        )
        .addEventListener(
            "click",
            clearPredictionHistory
        );

    injectPredictionHistoryStyles();

    const resultPanel =
        document.getElementById(
            "prediction-result"
        );

    if (resultPanel?.parentElement) {
        resultPanel.parentElement.insertBefore(
            predictionHistoryElement,
            resultPanel.nextSibling
        );
    } else if (predictButton) {
        const parent =
            predictButton.closest("form") ||
            predictButton.parentElement;

        if (parent?.parentElement) {
            parent.parentElement.appendChild(
                predictionHistoryElement
            );
        } else {
            document.body.appendChild(
                predictionHistoryElement
            );
        }
    } else {
        document.body.appendChild(
            predictionHistoryElement
        );
    }

    renderPredictionHistory();
}


function renderPredictionHistory() {
    if (!predictionHistoryElement) {
        return;
    }

    const list =
        predictionHistoryElement.querySelector(
            ".prediction-history-list"
        );

    if (!list) {
        return;
    }

    const history =
        readPredictionHistory();

    list.innerHTML = "";

    if (!history.length) {
        const empty =
            document.createElement("div");

        empty.className =
            "prediction-history-empty";

        empty.textContent =
            "Your predictions will appear here.";

        list.appendChild(empty);

        return;
    }

    history.forEach(entry => {
        const card =
            document.createElement("button");

        card.type = "button";
        card.className =
            "prediction-history-item";

        const dateText =
            entry.match_date ||
            formatHistoryDate(
                entry.created_at
            );

        const homeWin =
            historyPercent(entry.home_win);

        const draw =
            historyPercent(entry.draw);

        const awayWin =
            historyPercent(entry.away_win);

        const favorite =
            getHistoryFavorite(
                entry
            );

        const homeXg =
            historyNumber(entry.home_xg);

        const awayXg =
            historyNumber(entry.away_xg);

        card.innerHTML = `
            <div class="history-team">
                <div class="history-logo home-history-logo"></div>
                <span>${escapeHistoryHTML(entry.home_team)}</span>
            </div>

            <div class="history-middle">
                <strong>${escapeHistoryHTML(favorite)}</strong>
                <span>${escapeHistoryHTML(dateText)}</span>
                <small class="history-xg">
                    xG ${homeXg} — ${awayXg}
                </small>
            </div>

            <div class="history-team">
                <div class="history-logo away-history-logo"></div>
                <span>${escapeHistoryHTML(entry.away_team)}</span>
            </div>

            <div class="history-probabilities">
                <span>${homeWin}</span>
                <span>${draw}</span>
                <span>${awayWin}</span>
            </div>
        `;

        setPredictionLogo(
            card.querySelector(
                ".home-history-logo"
            ),
            historyLogoUrl(
                entry.home_logo
            )
        );

        setPredictionLogo(
            card.querySelector(
                ".away-history-logo"
            ),
            historyLogoUrl(
                entry.away_logo
            )
        );

        card.addEventListener(
            "click",
            () => {
                restorePredictionFromHistory(
                    entry
                );
            }
        );

        list.appendChild(card);
    });
}


function historyLogoUrl(url) {
    if (!url) {
        return "";
    }

    const match =
        String(url).match(
            /\/api\/v1\/team\/(\d+)\/image/
        );

    return match
        ? `/team-logo/${match[1]}`
        : url;
}


function restorePredictionFromHistory(
    entry
) {
    if (!entry) {
        return;
    }

    const result = {
        home_team:
            entry.home_team,

        away_team:
            entry.away_team,

        home_logo:
            historyLogoUrl(
                entry.home_logo
            ),

        away_logo:
            historyLogoUrl(
                entry.away_logo
            ),

        home_league:
            entry.home_league,

        away_league:
            entry.away_league,

        home_win:
            entry.home_win,

        draw:
            entry.draw,

        away_win:
            entry.away_win,

        home_xg:
            entry.home_xg,

        away_xg:
            entry.away_xg,

        top_scores:
            entry.top_scores || [],

        over_2_5:
            entry.over25,

        btts:
            entry.btts,
    };

    updatePredictionUI(
        result,
        entry.match_date || null
    );
}


function clearPredictionHistory() {
    const history =
        readPredictionHistory();

    if (!history.length) {
        return;
    }

    localStorage.removeItem(
        PREDICTION_HISTORY_KEY
    );

    renderPredictionHistory();
}


function getHistoryFavorite(entry) {
    const values = [
        {
            name: entry.home_team,
            value: Number(
                entry.home_win || 0
            ),
        },
        {
            name: "DRAW",
            value: Number(
                entry.draw || 0
            ),
        },
        {
            name: entry.away_team,
            value: Number(
                entry.away_win || 0
            ),
        },
    ];

    const best =
        values.reduce(
            (a, b) =>
                b.value > a.value
                    ? b
                    : a,
            values[0]
        );

    return best.name;
}


function historyNumber(value) {
    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return "—";
    }

    const number =
        Number(value);

    if (!Number.isFinite(number)) {
        return "—";
    }

    return number.toFixed(2);
}


function historyPercent(value) {
    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return "—";
    }

    let number =
        Number(value);

    if (!Number.isFinite(number)) {
        return "—";
    }

    if (number <= 1) {
        number *= 100;
    }

    return `${number.toFixed(1)}%`;
}


function formatHistoryDate(value) {
    if (!value) {
        return "";
    }

    const date =
        new Date(value);

    if (Number.isNaN(date.getTime())) {
        return "";
    }

    return date.toLocaleDateString(
        undefined,
        {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
        }
    );
}


function escapeHistoryHTML(value) {
    return String(
        value ?? ""
    )
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );
}


function injectPredictionHistoryStyles() {
    if (
        document.getElementById(
            "prediction-history-styles"
        )
    ) {
        return;
    }

    const style =
        document.createElement(
            "style"
        );

    style.id =
        "prediction-history-styles";

    style.textContent = `
        .prediction-history {
            width: 100%;
            margin: 22px 0 0;
            box-sizing: border-box;
            font-family:
                Inter,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }

        .prediction-history-header {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 20px;
            margin-bottom: 12px;
        }

        .prediction-history-kicker {
            margin-bottom: 4px;
            color: #8b8f98;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: .14em;
        }

        .prediction-history-title {
            margin: 0;
            color: #17191d;
            font-size: 21px;
            line-height: 1.15;
            font-weight: 700;
            letter-spacing: -.03em;
        }

        .prediction-history-clear {
            border: 0;
            padding: 8px 11px;
            border-radius: 9px;
            background: #f3f4f6;
            color: #666a72;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
        }

        .prediction-history-clear:hover {
            background: #e9eaed;
            color: #17191d;
        }

        .prediction-history-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .prediction-history-item {
            position: relative;
            display: grid;
            grid-template-columns:
                minmax(0, 1fr)
                92px
                minmax(0, 1fr);
            align-items: center;
            gap: 12px;
            width: 100%;
            box-sizing: border-box;
            padding: 13px 14px 30px;
            border: 1px solid #e8e9ec;
            border-radius: 15px;
            background: #fff;
            box-shadow: 0 5px 18px rgba(20,24,32,.045);
            color: #17191d;
            text-align: center;
            cursor: pointer;
        }

        .prediction-history-item:hover {
            border-color: #dfe1e5;
            box-shadow: 0 8px 24px rgba(20,24,32,.07);
        }

        .history-team {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            min-width: 0;
            font-size: 13px;
            font-weight: 700;
        }

        .history-team span {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .history-logo {
            width: 28px;
            height: 28px;
            flex: 0 0 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }

        .history-logo img {
            width: 100%;
            height: 100%;
            object-fit: contain;
        }

        .history-middle {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 3px;
        }

        .history-middle strong {
            font-size: 11px;
            line-height: 1.2;
        }

        .history-middle span {
            color: #8b8f98;
            font-size: 9px;
        }

        .history-xg {
            display: block;
            margin-top: 1px;
            color: #555961;
            font-size: 9px;
            font-weight: 700;
        }

        .history-probabilities {
            position: absolute;
            left: 14px;
            right: 14px;
            bottom: 7px;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
            color: #858991;
            font-size: 9px;
            font-weight: 600;
        }

        .prediction-history-empty {
            padding: 22px;
            border: 1px dashed #dfe1e5;
            border-radius: 15px;
            color: #999ca3;
            background: #fff;
            font-size: 12px;
            text-align: center;
        }

        @media(max-width:640px) {
            .prediction-history-item {
                grid-template-columns:
                    minmax(0, 1fr)
                    65px
                    minmax(0, 1fr);
                gap: 6px;
                padding-left: 9px;
                padding-right: 9px;
            }

            .history-team {
                font-size: 11px;
            }

            .history-logo {
                width: 24px;
                height: 24px;
                flex-basis: 24px;
            }
        }
    `;

    document.head.appendChild(style);
}
