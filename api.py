from datetime import date
from pathlib import Path
from typing import Optional

import json
from curl_cffi import requests as curl_requests

from fastapi import (
    FastAPI,
    HTTPException,
    Query,
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from fastapi.responses import (
    FileResponse, Response
)

from fastapi.staticfiles import (
    StaticFiles
)

from pydantic import (
    BaseModel
)

from src.services.prediction_service import (
    PredictionService
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

FRONTEND_DIR = (
    BASE_DIR / "frontend"
)

INDEX_FILE = (
    FRONTEND_DIR / "index.html"
)

TEAMS_FILE = (
    BASE_DIR / "teams.json"
)


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="Football Prediction API",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(
        directory=FRONTEND_DIR
    ),
    name="static",
)


# ============================================================
# LOAD TEAMS
# ============================================================

def load_teams():

    if not TEAMS_FILE.exists():

        raise FileNotFoundError(
            f"teams.json not found: "
            f"{TEAMS_FILE}"
        )

    with open(
        TEAMS_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    if not isinstance(data, dict):

        raise ValueError(
            "teams.json must contain "
            "a JSON object."
        )

    return data


teams_database = load_teams()


# ============================================================
# PREDICTION SERVICE
# ============================================================

service = PredictionService()


# ============================================================
# REQUEST MODEL
# ============================================================

class PredictionRequest(BaseModel):

    home_team: str

    away_team: str

    match_date: Optional[str] = None

    league_id: Optional[int] = None


# ============================================================
# FRONTEND
# ============================================================

@app.get("/team-logo/{sofascore_id}")
def team_logo(sofascore_id: int):
    url = (
        f"https://img.sofascore.com/"
        f"api/v1/team/{sofascore_id}/image"
    )

    try:
        response = curl_requests.get(
            url,
            impersonate="chrome",
            timeout=15,
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail="Team logo not found.",
            )

        return Response(
            content=response.content,
            media_type=response.headers.get(
                "content-type",
                "image/png",
            ),
            headers={
                "Cache-Control":
                    "public, max-age=86400",
            },
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Logo request failed: {error}",
        )
    
@app.get("/")
def root():

    return FileResponse(
        INDEX_FILE
    )


# ============================================================
# TEAMS
# ============================================================

@app.get("/teams")
def get_teams(
    search: Optional[str] = Query(
        default=None
    )
):

    # --------------------------------------------------------
    # ALL TEAMS
    # --------------------------------------------------------

    if not search:

        return {
            "teams": [
                {
                    "name": name,
                    "league": info.get(
                        "league"
                    ),
                    "country": info.get(
                        "country"
                    ),
                    "logo": (
                        f"/team-logo/{info['sofascore_id']}"
                        if info.get("sofascore_id")
                        else ""
                    ),
                }

                for name, info
                in teams_database.items()
            ]
        }

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    search_normalized = (
        service._normalize(search)
    )

    results = []

    for name, info in (
        teams_database.items()
    ):

        aliases = info.get(
            "aliases",
            []
        )

        candidates = [
            name,
            *aliases,
        ]

        found = False

        for candidate in candidates:

            candidate_normalized = (
                service._normalize(
                    candidate
                )
            )

            if (
                search_normalized
                in candidate_normalized
                or candidate_normalized
                in search_normalized
            ):

                found = True
                break

        if found:

            results.append(
                {
                    "name": name,
                    "league": info.get("league"),
                    "country": info.get("country"),
                    "logo": (
                        f"/team-logo/{info['sofascore_id']}"
                        if info.get("sofascore_id")
                        else ""
                    ),
                }
            )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {
        "teams": results
    }


# ============================================================
# TEAMS TEST
# ============================================================

@app.get("/teams-test")
def teams_test():

    return {
        "count": len(
            teams_database
        ),

        "teams": [
            {
                "name": name,
                "league": info.get(
                    "league"
                ),
                "country": info.get(
                    "country"
                ),
                "logo": (
                    f"/team-logo/{info['sofascore_id']}"
                    if info.get("sofascore_id")
                    else ""
                ),
            }

            for name, info
            in teams_database.items()
        ],
    }


# ============================================================
# TEAM BY NAME
# ============================================================

@app.get("/teams/{team_name}")
def get_team(
    team_name: str
):

    try:

        canonical = (
            service.resolve_team(
                team_name
            )
        )

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    info = (
        teams_database.get(
            canonical
        )
    )

    if not info:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Team not found: "
                f"{team_name}"
            ),
        )

    return {
        "name": canonical,
        "league": info.get(
            "league"
        ),
        "country": info.get(
            "country"
        ),
        "logo": (
            f"/team-logo/{info['sofascore_id']}"
            if info.get("sofascore_id")
            else ""
        ),
        "aliases": info.get(
            "aliases",
            []
        ),
    }


# ============================================================
# PREDICT
# ============================================================

@app.post("/predict")
def predict(
    request: PredictionRequest
):

    try:

        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        match_date = None

        if request.match_date:

            try:

                match_date = (
                    date.fromisoformat(
                        request.match_date
                    )
                )

            except ValueError:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Invalid date format. "
                        "Use YYYY-MM-DD."
                    ),
                )

        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        result = service.predict(

            home_team=(
                request.home_team
            ),

            away_team=(
                request.away_team
            ),

            match_date=match_date,

            league_id=(
                request.league_id
            ),
        )

        # ----------------------------------------------------
        # ADD TEAM INFORMATION
        # ----------------------------------------------------

        home_info = (
            teams_database.get(
                result["home_team"],
                {}
            )
        )

        away_info = (
            teams_database.get(
                result["away_team"],
                {}
            )
        )

        result["home_logo"] = (
            home_info.get(
                "logo",
                ""
            )
        )

        result["away_logo"] = (
            away_info.get(
                "logo",
                ""
            )
        )

        result["home_league"] = (
            home_info.get(
                "league"
            )
        )

        result["away_league"] = (
            away_info.get(
                "league"
            )
        )

        return result

    except HTTPException:

        raise

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )