TEAM_NAMES = {

    # England
    "Man United": "Manchester United",
    "Man City": "Manchester City",
    "Newcastle": "Newcastle United",
    "Nott'm Forest": "Nottingham Forest",
    "West Brom": "West Bromwich Albion",
    "Wolves": "Wolverhampton Wanderers",

    # Spain
    "Ath Bilbao": "Athletic Club",
    "Ath Madrid": "Atletico Madrid",
    "Betis": "Real Betis",
    "Sociedad": "Real Sociedad",
    "Vallecano": "Rayo Vallecano",
    "Celta": "Celta Vigo",
    "Espanol": "Espanyol",
    "Huesca": "SD Huesca",
    "Oviedo": "Real Oviedo",
    "Valladolid": "Real Valladolid",

    # Germany
    "Dortmund": "Borussia Dortmund",
    "M'gladbach": "Borussia M.Gladbach",
    "Leverkusen": "Bayer Leverkusen",
    "RB Leipzig": "RasenBallsport Leipzig",
    "Ein Frankfurt": "Eintracht Frankfurt",
    "FC Koln": "FC Cologne",
    "Stuttgart": "VfB Stuttgart",
    "Mainz": "Mainz 05",
    "Hertha": "Hertha Berlin",
    "Hamburg": "Hamburger SV",
    "Heidenheim": "FC Heidenheim",
    "Bielefeld": "Arminia Bielefeld",
    "Fortuna Dusseldorf": "Fortuna Duesseldorf",
    "Nurnberg": "Nuernberg",
    "St Pauli": "St. Pauli",

    # Italy
    "Milan": "AC Milan",
    "Parma": "Parma Calcio 1913",
    "Spal": "SPAL 2013",

    # France
    "Paris SG": "Paris Saint Germain",
    "Clermont": "Clermont Foot",
    "St Etienne": "Saint-Etienne",

}


def normalize_team(name: str) -> str:

    if not isinstance(name, str):
        return name

    name = name.strip()

    return TEAM_NAMES.get(name, name)