# ============================================================
# TEAM REGISTRY
# ============================================================

from typing import Optional


# ============================================================
# TEAM DATA
#
# canonical = название, которое используется моделью
# aliases   = всё, что пользователь может написать
# logo      = URL эмблемы
# league    = основная лига
# country   = страна
# ============================================================

TEAMS = {

    # ========================================================
    # ENGLAND — PREMIER LEAGUE
    # ========================================================

    "Arsenal": {
        "aliases": [
            "arsenal",
            "arsenal fc",
            "arsenal london",
            "gunners",
            "арсенал",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=arsenal.com&sz=128",
    },

    "Aston Villa": {
        "aliases": [
            "aston villa",
            "villa",
            "aston villa fc",
            "avfc",
            "астон вилла",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=avfc.co.uk&sz=128",
    },

    "Bournemouth": {
        "aliases": [
            "bournemouth",
            "afc bournemouth",
            "bournemouth fc",
            "cherries",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=afcb.co.uk&sz=128",
    },

    "Brentford": {
        "aliases": [
            "brentford",
            "brentford fc",
            "bees",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=brentfordfc.com&sz=128",
    },

    "Brighton": {
        "aliases": [
            "brighton",
            "brighton and hove albion",
            "brighton & hove albion",
            "brighton hove albion",
            "brighton fc",
            "seagulls",
            "чайки",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=brightonandhovealbion.com&sz=128",
    },

    "Chelsea": {
        "aliases": [
            "chelsea",
            "chelsea fc",
            "chelsea london",
            "blues",
            "челси",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=chelseafc.com&sz=128",
    },

    "Coventry": {
        "aliases": [
            "coventry",
            "coventry city",
            "coventry city fc",
            "ccfc",
            "ковентри",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=ccfc.co.uk&sz=128",
    },

    "Crystal Palace": {
        "aliases": [
            "crystal palace",
            "crystal palace fc",
            "palace",
            "cpfc",
            "кристал пэлас",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=cpfc.co.uk&sz=128",
    },

    "Everton": {
        "aliases": [
            "everton",
            "everton fc",
            "toffees",
            "эвертон",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=evertonfc.com&sz=128",
    },

    "Fulham": {
        "aliases": [
            "fulham",
            "fulham fc",
            "cottagers",
            "фулхэм",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=fulhamfc.com&sz=128",
    },

    "Hull": {
        "aliases": [
            "hull",
            "hull city",
            "hull city fc",
            "tigers",
            "халл",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=hullcitytigers.com&sz=128",
    },

    "Ipswich": {
        "aliases": [
            "ipswich",
            "ipswich town",
            "ipswich town fc",
            "itfc",
            "ипсвич",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=itfc.co.uk&sz=128",
    },

    "Leeds": {
        "aliases": [
            "leeds",
            "leeds united",
            "leeds united fc",
            "lufc",
            "лидс",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=leedsunited.com&sz=128",
    },

    "Liverpool": {
        "aliases": [
            "liverpool",
            "liverpool fc",
            "lfc",
            "reds",
            "ливерпуль",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=liverpoolfc.com&sz=128",
    },

    "Manchester City": {
        "aliases": [
            "manchester city",
            "man city",
            "manchester city fc",
            "mcfc",
            "city",
            "сити",
            "ман сити",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=mancity.com&sz=128",
    },

    "Manchester United": {
        "aliases": [
            "manchester united",
            "man united",
            "man utd",
            "manchester united fc",
            "mufc",
            "mu",
            "манчестер юнайтед",
            "ман юнайтед",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=manutd.com&sz=128",
    },

    "Newcastle United": {
        "aliases": [
            "newcastle",
            "newcastle united",
            "newcastle united fc",
            "nufc",
            "сороки",
            "ньюкасл",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=nufc.co.uk&sz=128",
    },

    "Nottingham Forest": {
        "aliases": [
            "nottingham forest",
            "nottingham",
            "forest",
            "nffc",
            "ноттингем",
            "ноттингем форест",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=nottinghamforest.co.uk&sz=128",
    },

    "Sunderland": {
        "aliases": [
            "sunderland",
            "sunderland afc",
            "sunderland fc",
            "black cats",
            "сандеpленд",
            "сундерленд",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=safc.com&sz=128",
    },

    "Tottenham": {
        "aliases": [
            "tottenham",
            "tottenham hotspur",
            "tottenham hotspur fc",
            "spurs",
            "thfc",
            "тоттенхэм",
            "шпоры",
        ],
        "league": "Premier League",
        "country": "England",
        "logo": "https://www.google.com/s2/favicons?domain=tottenhamhotspur.com&sz=128",
    },


    # ========================================================
    # SPAIN — LA LIGA
    # ========================================================

    "Athletic Club": {
        "aliases": [
            "athletic club",
            "athletic bilbao",
            "athletic",
            "bilbao",
            "атлетик",
            "атлетик бильбао",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=athletic-club.eus&sz=128",
    },

    "Atletico Madrid": {
        "aliases": [
            "atletico madrid",
            "atlético madrid",
            "atletico",
            "atleti",
            "atm",
            "атлетико",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=atleticodemadrid.com&sz=128",
    },

    "Osasuna": {
        "aliases": [
            "osasuna",
            "ca osasuna",
            "осасуна",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=osasuna.es&sz=128",
    },

    "Celta": {
        "aliases": [
            "celta",
            "celta vigo",
            "rc celta",
            "сельта",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain:rccelta.es&sz=128",
    },

    "Alaves": {
        "aliases": [
            "alaves",
            "alavés",
            "deportivo alaves",
            "депортиво алавес",
            "алавес",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=deportivoalaves.com&sz=128",
    },

    "Elche": {
        "aliases": [
            "elche",
            "elche cf",
            "эльче",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=elchecf.es&sz=128",
    },

    "Barcelona": {
        "aliases": [
            "barcelona",
            "barca",
            "barça",
            "fc barcelona",
            "fcb",
            "барселона",
            "барса",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=fcbarcelona.com&sz=128",
    },

    "Getafe": {
        "aliases": [
            "getafe",
            "getafe cf",
            "хетафе",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=getafecf.com&sz=128",
    },

    "Levante": {
        "aliases": [
            "levante",
            "levante ud",
            "леванте",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=levanteud.com&sz=128",
    },

    "Malaga": {
        "aliases": [
            "malaga",
            "málaga",
            "malaga cf",
            "малага",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=malagacf.com&sz=128",
    },

    "Racing Santander": {
        "aliases": [
            "racing santander",
            "racing",
            "racing de santander",
            "расинг сантандер",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=realracingclub.es&sz=128",
    },

    "Rayo Vallecano": {
        "aliases": [
            "rayo",
            "rayo vallecano",
            "райо",
            "райо вальекано",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=rayovallecano.es&sz=128",
    },

    "Deportivo La Coruna": {
        "aliases": [
            "deportivo",
            "deportivo la coruna",
            "deportivo la coruña",
            "dep la coruna",
            "депортиво",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain:rcdeportivo.es&sz=128",
    },

    "Espanyol": {
        "aliases": [
            "espanyol",
            "rcd espanyol",
            "espanyol barcelona",
            "эспаньол",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=rcdespanyol.com&sz=128",
    },

    "Real Betis": {
        "aliases": [
            "real betis",
            "betis",
            "real betis balompie",
            "бетис",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=realbetisbalompie.es&sz=128",
    },

    "Real Madrid": {
        "aliases": [
            "real madrid",
            "real",
            "madrid",
            "rm",
            "реал",
            "реал мадрид",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=realmadrid.com&sz=128",
    },

    "Real Sociedad": {
        "aliases": [
            "real sociedad",
            "sociedad",
            "ла реал",
            "реал сосьедад",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=realsociedad.eus&sz=128",
    },

    "Sevilla": {
        "aliases": [
            "sevilla",
            "sevilla fc",
            "севилья",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=sevillafc.es&sz=128",
    },

    "Valencia": {
        "aliases": [
            "valencia",
            "valencia cf",
            "валенсия",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=valenciacf.com&sz=128",
    },

    "Villarreal": {
        "aliases": [
            "villarreal",
            "villareal",
            "villarreal cf",
            "вильярреал",
        ],
        "league": "La Liga",
        "country": "Spain",
        "logo": "https://www.google.com/s2/favicons?domain=villarrealcf.es&sz=128",
    },


    # ========================================================
    # GERMANY — BUNDESLIGA
    # ========================================================

    "Bayern Munich": {
        "aliases": [
            "bayern",
            "bayern munich",
            "bayern munchen",
            "bayern münchen",
            "fc bayern",
            "fcb",
            "бавария",
            "бавария мюнхен",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=fcbayern.com&sz=128",
    },

    "Borussia Dortmund": {
        "aliases": [
            "borussia dortmund",
            "dortmund",
            "bvb",
            "боруссия",
            "боруссия дортмунд",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=bvb.de&sz=128",
    },

    "RB Leipzig": {
        "aliases": [
            "rb leipzig",
            "leipzig",
            "rbl",
            "лейпциг",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=rbleipzig.com&sz=128",
    },

    "Stuttgart": {
        "aliases": [
            "stuttgart",
            "vfb stuttgart",
            "штутгарт",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=vfb.de&sz=128",
    },

    "Hoffenheim": {
        "aliases": [
            "hoffenheim",
            "tsg hoffenheim",
            "хоффенхайм",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=tsg-hoffenheim.de&sz=128",
    },

    "Bayer Leverkusen": {
        "aliases": [
            "bayer leverkusen",
            "leverkusen",
            "bayer",
            "byl",
            "байер",
            "байер леверкузен",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=bayer04.de&sz=128",
    },

    "Freiburg": {
        "aliases": [
            "freiburg",
            "sc freiburg",
            "фрайбург",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=scfreiburg.com&sz=128",
    },

    "Eintracht Frankfurt": {
        "aliases": [
            "eintracht frankfurt",
            "frankfurt",
            "eintracht",
            "eintracht frankfurt",
            "айнтрахт",
            "айнтрахт франкфурт",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=eintracht.de&sz=128",
    },

    "Augsburg": {
        "aliases": [
            "augsburg",
            "fc augsburg",
            "аугсбург",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=fcaugsburg.de&sz=128",
    },

    "Mainz": {
        "aliases": [
            "mainz",
            "mainz 05",
            "майнц",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=mainz05.de&sz=128",
    },

    "Union Berlin": {
        "aliases": [
            "union berlin",
            "union",
            "унион",
            "унион берлин",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=fc-union-berlin.de&sz=128",
    },

    "Borussia Monchengladbach": {
        "aliases": [
            "borussia monchengladbach",
            "borussia mönchengladbach",
            "monchengladbach",
            "gladbach",
            "гладбах",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=borussia.de&sz=128",
    },

    "Hamburg": {
        "aliases": [
            "hamburg",
            "hamburger sv",
            "hsv",
            "гамбург",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=hsv.de&sz=128",
    },

    "Cologne": {
        "aliases": [
            "cologne",
            "koln",
            "köln",
            "fc koln",
            "кёльн",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=fc.de&sz=128",
    },

    "Werder Bremen": {
        "aliases": [
            "werder bremen",
            "werder",
            "bremen",
            "вердер",
            "вердер бремен",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=werder.de&sz=128",
    },

    "Schalke": {
        "aliases": [
            "schalke",
            "schalke 04",
            "s04",
            "шальке",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=schalke04.de&sz=128",
    },

    "Elversberg": {
        "aliases": [
            "elversberg",
            "sv elversberg",
            "эльверсберг",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=sv07elversberg.de&sz=128",
    },

    "Paderborn": {
        "aliases": [
            "paderborn",
            "sc paderborn",
            "падерборн",
        ],
        "league": "Bundesliga",
        "country": "Germany",
        "logo": "https://www.google.com/s2/favicons?domain=scp07.de&sz=128",
    },


    # ========================================================
    # ITALY — SERIE A
    # ========================================================

    "Atalanta": {
        "aliases": [
            "atalanta",
            "atalanta bc",
            "бергамо",
            "аталанта",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=atalanta.it&sz=128",
    },

    "Bologna": {
        "aliases": [
            "bologna",
            "bologna fc",
            "болонья",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=bolognafc.it&sz=128",
    },

    "Cagliari": {
        "aliases": [
            "cagliari",
            "cagliari calcio",
            "кальяри",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=cagliaricalcio.com&sz=128",
    },

    "Como": {
        "aliases": [
            "como",
            "como 1907",
            "комо",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=comofootball.com&sz=128",
    },

    "Fiorentina": {
        "aliases": [
            "fiorentina",
            "acf fiorentina",
            "фиорентина",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=acffiorentina.com&sz=128",
    },

    "Frosinone": {
        "aliases": [
            "frosinone",
            "frosinone calcio",
            "фрозиноне",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=frosinonecalcio.com&sz=128",
    },

    "Genoa": {
        "aliases": [
            "genoa",
            "genoa cfc",
            "дженоа",
            "генуя",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=genoacfc.it&sz=128",
    },

    "Inter": {
        "aliases": [
            "inter",
            "inter milan",
            "internazionale",
            "internazionale milano",
            "fc internazionale",
            "интер",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=inter.it&sz=128",
    },

    "Juventus": {
        "aliases": [
            "juventus",
            "juve",
            "juventus fc",
            "ювентус",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=juventus.com&sz=128",
    },

    "Lazio": {
        "aliases": [
            "lazio",
            "ss lazio",
            "лацио",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=sslazio.it&sz=128",
    },

    "Lecce": {
        "aliases": [
            "lecce",
            "us lecce",
            "лечче",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=uslecce.it&sz=128",
    },

    "Milan": {
        "aliases": [
            "milan",
            "ac milan",
            "acm",
            "милан",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=acmilan.com&sz=128",
    },

    "Monza": {
        "aliases": [
            "monza",
            "ac monza",
            "монца",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=acmonza.com&sz=128",
    },

    "Napoli": {
        "aliases": [
            "napoli",
            "ssc napoli",
            "naples",
            "наполи",
            "неаполь",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=sscnapoli.it&sz=128",
    },

    "Parma": {
        "aliases": [
            "parma",
            "parma calcio",
            "парма",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=parmacalcio1913.com&sz=128",
    },

    "Roma": {
        "aliases": [
            "roma",
            "as roma",
            "asr",
            "рома",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=asroma.com&sz=128",
    },

    "Sassuolo": {
        "aliases": [
            "sassuolo",
            "us sassuolo",
            "сассуоло",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=sassuolocalcio.it&sz=128",
    },

    "Torino": {
        "aliases": [
            "torino",
            "torino fc",
            "тoрино",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=torinofc.it&sz=128",
    },

    "Udinese": {
        "aliases": [
            "udinese",
            "udinese calcio",
            "удинезе",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=udinese.it&sz=128",
    },

    "Venezia": {
        "aliases": [
            "venezia",
            "venezia fc",
            "венеция",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=veneziafc.it&sz=128",
    },


    # ========================================================
    # FRANCE — LIGUE 1
    # ========================================================

    "Angers": {
        "aliases": [
            "angers",
            "angers sco",
            "анже",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=angers-sco.fr&sz=128",
    },

    "Auxerre": {
        "aliases": [
            "auxerre",
            "aj auxerre",
            "осер",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=aja.fr&sz=128",
    },

    "Brest": {
        "aliases": [
            "brest",
            "stade brestois",
            "stade brestois 29",
            "брест",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain:sb29.bzh&sz=128",
    },

    "Le Havre": {
        "aliases": [
            "le havre",
            "le havre ac",
            "lehavre",
            "гавр",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=hac-foot.com&sz=128",
    },

    "Lens": {
        "aliases": [
            "lens",
            "rc lens",
            "racing lens",
            "ланс",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=rclens.fr&sz=128",
    },

    "Lille": {
        "aliases": [
            "lille",
            "lille osc",
            "losc",
            "лиль",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=losc.fr&sz=128",
    },

    "Lorient": {
        "aliases": [
            "lorient",
            "fc lorient",
            "лорьян",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=fc-lorient.bzh&sz=128",
    },

    "Lyon": {
        "aliases": [
            "lyon",
            "olympique lyon",
            "olympique lyonnais",
            "ol",
            "лион",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=ol.fr&sz=128",
    },

    "Le Mans": {
        "aliases": [
            "le mans",
            "le mans fc",
            "леман",
            "ле ман",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=lemansfc.fr&sz=128",
    },

    "Marseille": {
        "aliases": [
            "marseille",
            "olympique marseille",
            "olympique de marseille",
            "om",
            "марсель",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=om.fr&sz=128",
    },

    "Monaco": {
        "aliases": [
            "monaco",
            "as monaco",
            "monaco fc",
            "asm",
            "монако",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=asmonaco.com&sz=128",
    },

    "Nice": {
        "aliases": [
            "nice",
            "ogc nice",
            "nice fc",
            "ницца",
            "ницца",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=ogcnice.com&sz=128",
    },

    "Paris FC": {
        "aliases": [
            "paris fc",
            "paris football club",
            "pfc",
            "париж фк",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=parisfootballclub.com&sz=128",
    },

    "Paris Saint Germain": {
        "aliases": [
            "psg",
            "paris",
            "paris saint germain",
            "paris saint-germain",
            "paris sg",
            "psg fc",
            "псж",
            "париж",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=psg.fr&sz=128",
    },

    "Rennes": {
        "aliases": [
            "rennes",
            "stade rennais",
            "stade rennais fc",
            "ренн",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=staderennais.com&sz=128",
    },

    "Strasbourg": {
        "aliases": [
            "strasbourg",
            "rc strasbourg",
            "rc strasbourg alsace",
            "страсбур",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=rcstrasbourgalsace.fr&sz=128",
    },

    "Toulouse": {
        "aliases": [
            "toulouse",
            "toulouse fc",
            "тулуза",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=toulousefc.com&sz=128",
    },

    "Troyes": {
        "aliases": [
            "troyes",
            "estac troyes",
            "труа",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=estac.fr&sz=128",
    },


    # ========================================================
    # CHAMPIONS LEAGUE — OTHER TEAMS
    # ========================================================

    "AEK Athens": {
        "aliases": [
            "aek",
            "aek athens",
            "aek athina",
            "аек",
            "аек афины",
        ],
        "league": "Champions League",
        "country": "Greece",
        "logo": "https://www.google.com/s2/favicons?domain=aekfc.gr&sz=128",
    },

    "Sporting CP": {
        "aliases": [
            "sporting",
            "sporting cp",
            "sporting lisbon",
            "sporting lisboa",
            "спортинг",
        ],
        "league": "Champions League",
        "country": "Portugal",
        "logo": "https://www.google.com/s2/favicons?domain=sporting.pt&sz=128",
    },

    "Porto": {
        "aliases": [
            "porto",
            "fc porto",
            "порту",
        ],
        "league": "Champions League",
        "country": "Portugal",
        "logo": "https://www.google.com/s2/favicons?domain=fcporto.pt&sz=128",
    },

    "Club Brugge": {
        "aliases": [
            "club brugge",
            "brugge",
            "club brugge kv",
            "брюгге",
        ],
        "league": "Champions League",
        "country": "Belgium",
        "logo": "https://www.google.com/s2/favicons?domain=clubbrugge.be&sz=128",
    },

    "PSV": {
        "aliases": [
            "psv",
            "psv eindhoven",
            "eindhoven",
            "псв",
        ],
        "league": "Champions League",
        "country": "Netherlands",
        "logo": "https://www.google.com/s2/favicons?domain=psv.nl&sz=128",
    },

    "Feyenoord": {
        "aliases": [
            "feyenoord",
            "фейеноорд",
        ],
        "league": "Champions League",
        "country": "Netherlands",
        "logo": "https://www.google.com/s2/favicons?domain=feyenoord.nl&sz=128",
    },

    "Bodo Glimt": {
        "aliases": [
            "bodo glimt",
            "bodo/glimt",
            "bodø/glimt",
            "bodø glimt",
            "bodo",
            "бодо глимт",
        ],
        "league": "Champions League",
        "country": "Norway",
        "logo": "https://www.google.com/s2/favicons?domain=glimt.no&sz=128",
    },

    "Fenerbahce": {
        "aliases": [
            "fenerbahce",
            "fenerbahçe",
            "fener",
            "фенербахче",
        ],
        "league": "Champions League",
        "country": "Turkey",
        "logo": "https://www.google.com/s2/favicons?domain=fenerbahce.org&sz=128",
    },

    "Galatasaray": {
        "aliases": [
            "galatasaray",
            "galatasaray sk",
            "gala",
            "галатасарай",
        ],
        "league": "Champions League",
        "country": "Turkey",
        "logo": "https://www.google.com/s2/favicons?domain=galatasaray.org&sz=128",
    },

    "Shakhtar": {
        "aliases": [
            "shakhtar",
            "shakhtar donetsk",
            "shakhtar donieck",
            "шахтер",
            "шахтёр",
            "шахтер донецк",
        ],
        "league": "Champions League",
        "country": "Ukraine",
        "logo": "https://www.google.com/s2/favicons?domain=shakhtar.com&sz=128",
    },

    "Slavia Praha": {
        "aliases": [
            "slavia",
            "slavia praha",
            "slavia prague",
            "славия",
            "славия прага",
        ],
        "league": "Champions League",
        "country": "Czech Republic",
        "logo": "https://www.google.com/s2/favicons?domain=slavia.cz&sz=128",
    },

    "Slovan Bratislava": {
        "aliases": [
            "slovan",
            "slovan bratislava",
            "славан братислава",
            "слован",
        ],
        "league": "Champions League",
        "country": "Slovakia",
        "logo": "https://www.google.com/s2/favicons?domain:skslovan.com&sz=128",
    },

    "LASK": {
        "aliases": [
            "lask",
            "lask linz",
            "линц",
            "ласк",
        ],
        "league": "Champions League",
        "country": "Austria",
        "logo": "https://www.google.com/s2/favicons?domain=lask.at&sz=128",
    },

    "Como": {
        "aliases": [
            "como",
            "como 1907",
            "комо",
        ],
        "league": "Serie A",
        "country": "Italy",
        "logo": "https://www.google.com/s2/favicons?domain=comofootball.com&sz=128",
    },

    "Lens": {
        "aliases": [
            "lens",
            "rc lens",
            "ланс",
        ],
        "league": "Ligue 1",
        "country": "France",
        "logo": "https://www.google.com/s2/favicons?domain=rclens.fr&sz=128",
    },

    "Viking": {
        "aliases": [
            "viking",
            "viking fk",
            "viking stavanger",
            "викинг",
        ],
        "league": "Champions League",
        "country": "Norway",
        "logo": "https://www.google.com/s2/favicons?domain=vikingfotball.no&sz=128",
    },

    "Sabah": {
        "aliases": [
            "sabah",
            "sabah fc",
            "сабах",
        ],
        "league": "Champions League",
        "country": "Azerbaijan",
        "logo": "https://www.google.com/s2/favicons?domain=sabahfc.az&sz=128",
    },

}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_name(name: str) -> str:

    if not name:
        return ""

    return (
        str(name)
        .strip()
        .lower()
        .replace("-", " ")
        .replace("_", " ")
        .replace(".", "")
        .replace("'", "")
        .replace("ё", "е")
    )


# ============================================================
# ALIAS MAP
# ============================================================

ALIAS_MAP = {}


for canonical, data in TEAMS.items():

    ALIAS_MAP[
        normalize_name(canonical)
    ] = canonical

    for alias in data.get(
        "aliases",
        []
    ):

        ALIAS_MAP[
            normalize_name(alias)
        ] = canonical


# ============================================================
# RESOLVE TEAM
# ============================================================

def resolve_team(
    name: str
) -> Optional[str]:

    normalized = normalize_name(name)

    # Exact alias
    if normalized in ALIAS_MAP:
        return ALIAS_MAP[normalized]

    # Partial search
    matches = []

    for alias, canonical in ALIAS_MAP.items():

        if normalized in alias:

            if canonical not in matches:

                matches.append(canonical)

    if len(matches) == 1:

        return matches[0]

    return None


# ============================================================
# SEARCH TEAMS
# ============================================================

def search_teams(
    query: str
):

    normalized_query = normalize_name(query)

    if not normalized_query:

        return list(
            TEAMS.keys()
        )


    scored = []


    for canonical, data in TEAMS.items():

        names = [
            canonical
        ] + data.get(
            "aliases",
            []
        )


        best_score = 0


        for name in names:

            value = normalize_name(name)


            # Exact
            if value == normalized_query:

                best_score = max(
                    best_score,
                    100
                )


            # Starts with
            elif value.startswith(
                normalized_query
            ):

                best_score = max(
                    best_score,
                    80
                )


            # Contains
            elif normalized_query in value:

                best_score = max(
                    best_score,
                    60
                )


        if best_score > 0:

            scored.append(
                (
                    best_score,
                    canonical
                )
            )


    scored.sort(
        key=lambda item: (
            -item[0],
            item[1].lower()
        )
    )


    return [
        canonical
        for _, canonical
        in scored
    ]


# ============================================================
# GET TEAM
# ============================================================

def get_team(
    canonical: str
):

    return TEAMS.get(
        canonical
    )