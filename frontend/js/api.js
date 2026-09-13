// ============================================================
// FOOTBALL PREDICTOR — API
// ============================================================

const API_BASE = "";


/* ============================================================
   GET TEAMS
============================================================ */

async function getTeams(
    search = ""
) {

    const url =
        search
            ? `/teams?search=${encodeURIComponent(search)}`
            : "/teams";


    const response =
        await fetch(url);


    if (!response.ok) {

        throw new Error(
            "Failed to load teams."
        );

    }


    const data =
        await response.json();


    return data.teams || [];
}


/* ============================================================
   PREDICT MATCH
============================================================ */

async function predictMatch(
    homeTeam,
    awayTeam,
    matchDate = null
) {

    const body = {
        home_team: homeTeam,
        away_team: awayTeam,
    };


    // --------------------------------------------------------
    // DATE
    // --------------------------------------------------------

    if (matchDate) {

        body.match_date = matchDate;

    }


    // --------------------------------------------------------
    // REQUEST
    // --------------------------------------------------------

    const response = await fetch(
        `${API_BASE}/predict`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify(body),
        }
    );


    // --------------------------------------------------------
    // ERROR
    // --------------------------------------------------------

    if (!response.ok) {

        let message =
            `Prediction failed: ${response.status}`;

        try {

            const error =
                await response.json();

            if (error.detail) {
                message = error.detail;
            }

        } catch (_) {

            // Ignore invalid error response

        }

        throw new Error(message);
    }


    // --------------------------------------------------------
    // RESULT
    // --------------------------------------------------------

    return await response.json();
}