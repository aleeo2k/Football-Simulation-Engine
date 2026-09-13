import json
import re
from pathlib import Path

import pandas as pd

from src.database.database import Database

from src.pipeline.feature_builder import (
    FeatureBuilder
)

from src.prediction.full_reasonable_xg import (
    FullReasonableXG
)

from src.prediction.match_prediction import (
    MatchPrediction
)

from src.ratings.elo_tracker import (
    PROMOTED_TEAM_RATINGS
)


class PredictionService:

    def __init__(self):

        # ====================================================
        # PATHS
        # ====================================================

        BASE_DIR = Path(__file__).resolve().parents[2]

        self.teams_file = (
            BASE_DIR / "teams.json"
        )

        # ====================================================
        # LOAD TEAMS REGISTRY
        # ====================================================

        self.teams_database = (
            self._load_teams()
        )

        # ====================================================
        # DATABASE
        # ====================================================

        db = Database()

        self.matches = pd.read_sql(
            """
            SELECT *
            FROM matches
            ORDER BY date
            """,
            db.engine,
        )

        # ====================================================
        # FEATURE BUILDER
        # ====================================================

        self.feature_builder = (
            FeatureBuilder()
        )

        # ====================================================
        # FULL REASONABLE xG
        # ====================================================

        self.xg_model = (
            FullReasonableXG()
        )

        # ====================================================
        # MATCH PREDICTION
        # ====================================================

        self.predictor = (
            MatchPrediction()
        )

        # ====================================================
        # ALIAS INDEX
        # ====================================================

        self.alias_index = (
            self._build_alias_index()
        )

        # ====================================================
        # DATABASE TEAM INDEX
        # ====================================================

        self.database_team_index = (
            self._build_database_team_index()
        )

    # ========================================================
    # LOAD TEAMS
    # ========================================================

    def _load_teams(self):

        if not self.teams_file.exists():

            raise FileNotFoundError(
                f"teams.json not found: "
                f"{self.teams_file}"
            )

        with open(
            self.teams_file,
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

    # ========================================================
    # NORMALIZE TEXT
    # ========================================================

    @staticmethod
    def _normalize(
        value
    ):

        if value is None:
            return ""

        value = str(value)

        # lowercase
        value = value.lower()

        # replace special apostrophes
        value = value.replace(
            "’",
            "'"
        )

        # remove accents approximately
        replacements = {
            "á": "a",
            "à": "a",
            "ä": "a",
            "â": "a",
            "ã": "a",
            "å": "a",

            "é": "e",
            "è": "e",
            "ë": "e",
            "ê": "e",

            "í": "i",
            "ì": "i",
            "ï": "i",
            "î": "i",

            "ó": "o",
            "ò": "o",
            "ö": "o",
            "ô": "o",
            "õ": "o",

            "ú": "u",
            "ù": "u",
            "ü": "u",
            "û": "u",

            "ñ": "n",
            "ç": "c",

            "ø": "o",
            "ß": "ss",

            "ø": "o",
        }

        for old, new in replacements.items():

            value = value.replace(
                old,
                new
            )

        # remove punctuation
        value = re.sub(
            r"[^a-zа-яё0-9]+",
            " ",
            value
        )

        # remove extra spaces
        value = re.sub(
            r"\s+",
            " ",
            value
        )

        return value.strip()

    # ========================================================
    # BUILD ALIAS INDEX
    # ========================================================

    def _build_alias_index(self):

        index = {}

        for canonical, info in (
            self.teams_database.items()
        ):

            aliases = set()

            # canonical name itself
            aliases.add(
                canonical
            )

            # aliases from JSON
            for alias in info.get(
                "aliases",
                []
            ):

                aliases.add(alias)

            for alias in aliases:

                normalized = (
                    self._normalize(alias)
                )

                if normalized:

                    index[
                        normalized
                    ] = canonical

        return index

    # ========================================================
    # BUILD DATABASE TEAM INDEX
    # ========================================================

    def _build_database_team_index(self):

        index = {}

        teams = set()

        if "home_team" in self.matches.columns:

            teams.update(
                self.matches[
                    "home_team"
                ].dropna().tolist()
            )

        if "away_team" in self.matches.columns:

            teams.update(
                self.matches[
                    "away_team"
                ].dropna().tolist()
            )

        # Add promoted/cold-start teams
        teams.update(
            PROMOTED_TEAM_RATINGS.keys()
        )

        for team in teams:

            normalized = (
                self._normalize(team)
            )

            if normalized:

                index[
                    normalized
                ] = team

        return index

    # ========================================================
    # GET TEAMS
    # ========================================================

    def get_teams(self):

        return sorted(
            self.teams_database.keys()
        )

    # ========================================================
    # RESOLVE USER TEAM
    # ========================================================

    def resolve_team(
        self,
        team_name
    ):

        if not team_name:

            raise ValueError(
                "Team name cannot be empty."
            )

        normalized = (
            self._normalize(
                team_name
            )
        )

        # ----------------------------------------------------
        # 1. Exact canonical / alias match
        # ----------------------------------------------------

        if normalized in self.alias_index:

            return self.alias_index[
                normalized
            ]

        # ----------------------------------------------------
        # 2. Try matching directly
        #    against database names
        # ----------------------------------------------------

        if normalized in (
            self.database_team_index
        ):

            return self.database_team_index[
                normalized
            ]

        # ----------------------------------------------------
        # 3. Partial alias matching
        # ----------------------------------------------------

        candidates = []

        for alias, canonical in (
            self.alias_index.items()
        ):

            if (
                normalized in alias
                or alias in normalized
            ):

                candidates.append(
                    canonical
                )

        candidates = sorted(
            set(candidates)
        )

        if len(candidates) == 1:

            return candidates[0]

        # ----------------------------------------------------
        # 4. Not found
        # ----------------------------------------------------

        raise ValueError(
            f"Team not found: {team_name}"
        )

    # ========================================================
    # RESOLVE MODEL TEAM
    # ========================================================

    def resolve_model_team(
        self,
        canonical_team
    ):

        normalized = (
            self._normalize(
                canonical_team
            )
        )

        # ----------------------------------------------------
        # Exact database match
        # ----------------------------------------------------

        if normalized in (
            self.database_team_index
        ):

            return self.database_team_index[
                normalized
            ]

        # ----------------------------------------------------
        # Look through aliases
        # ----------------------------------------------------

        info = self.teams_database.get(
            canonical_team
        )

        if info:

            aliases = list(
                info.get(
                    "aliases",
                    []
                )
            )

            aliases.append(
                canonical_team
            )

            # Search database names
            # against all aliases

            for database_name in (
                self.database_team_index.values()
            ):

                database_normalized = (
                    self._normalize(
                        database_name
                    )
                )

                for alias in aliases:

                    alias_normalized = (
                        self._normalize(
                            alias
                        )
                    )

                    if (
                        database_normalized
                        == alias_normalized
                    ):

                        return database_name

        # ----------------------------------------------------
        # Special known mappings
        # ----------------------------------------------------

        special_mappings = {

            "Coventry City":
                "Coventry",

            "Hull City":
                "Hull",

            "Ipswich Town":
                "Ipswich",

            "Paris Saint Germain":
                "Paris Saint Germain",

        }

        if canonical_team in (
            special_mappings
        ):

            mapped = (
                special_mappings[
                    canonical_team
                ]
            )

            # Use mapped team if it exists
            # in historical data

            if (
                mapped in
                self.database_team_index.values()
                or mapped in
                PROMOTED_TEAM_RATINGS
            ):

                return mapped

        # ----------------------------------------------------
        # Cold start
        # ----------------------------------------------------

        return canonical_team

    # ========================================================
    # PREDICT
    # ========================================================

    def predict(
        self,
        home_team,
        away_team,
        match_date=None,
        league_id=None,
    ):

        # ====================================================
        # RESOLVE CANONICAL NAMES
        # ====================================================

        home_canonical = (
            self.resolve_team(
                home_team
            )
        )

        away_canonical = (
            self.resolve_team(
                away_team
            )
        )

        # ====================================================
        # SAME TEAM CHECK
        # ====================================================

        if (
            home_canonical
            == away_canonical
        ):

            raise ValueError(
                "Home team and away team "
                "cannot be the same."
            )

        # ====================================================
        # RESOLVE DATABASE / MODEL NAMES
        # ====================================================

        home_model_team = (
            self.resolve_model_team(
                home_canonical
            )
        )

        away_model_team = (
            self.resolve_model_team(
                away_canonical
            )
        )

        # ====================================================
        # BUILD PRE-MATCH FEATURES
        # ====================================================

        features = (
            self.feature_builder.build_match(
                matches=self.matches,
                home_team=home_model_team,
                away_team=away_model_team,
                match_date=match_date,
                league_id=league_id,
            )
        )

        # ====================================================
        # FULL REASONABLE xG
        # ====================================================

        xg = (
            self.xg_model.predict(
                features
            )
        )

        # ====================================================
        # MATCH PROBABILITIES
        # ====================================================

        prediction = (
            self.predictor.predict(
                xg["home_xg"],
                xg["away_xg"],
            )
        )

        # ====================================================
        # RESULT
        # ====================================================

        result = {

            # UI names
            "home_team":
                home_canonical,

            "away_team":
                away_canonical,

            # Internal names
            "home_model_team":
                home_model_team,

            "away_model_team":
                away_model_team,

            # xG
            "home_xg":
                xg["home_xg"],

            "away_xg":
                xg["away_xg"],

            # probabilities
            **prediction,
        }

        return result