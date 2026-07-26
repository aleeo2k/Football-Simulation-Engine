# Data Sources

## Purpose

This document defines all external data sources used by the Football Simulation Engine.

Each type of data has one primary source to ensure consistency.

---

# Source Priority

| Source | Purpose | Priority |
|----------|---------|----------|
| Understat | Expected Goals (xG), Expected Goals Against (xGA), shot data | Primary |
| FBref | Team statistics, player statistics, possession, passing, cards, corners | Primary |
| football-data.org | Fixtures, results, standings, competitions | Primary |
| Transfermarkt | Injuries, suspensions, transfers, player values | Primary |
| Open-Meteo | Weather conditions | Primary |
| ClubElo | Club Elo ratings | Secondary |

---

# Data Categories

## Match Data

- Date
- Competition
- Season
- Home Team
- Away Team
- Final Score

Source:
football-data.org

---

## Expected Goals

- Team xG
- Team xGA
- Player xG
- Player xA
- Shot xG

Source:
Understat

---

## Team Statistics

- Possession
- Shots
- Shots on Target
- Passes
- Passing Accuracy
- Corners
- Yellow Cards
- Red Cards
- Fouls

Source:
FBref

---

## Player Data

- Minutes Played
- Position
- Injuries
- Suspensions
- Market Value

Sources:
FBref
Transfermarkt

---

## Weather

- Temperature
- Rain
- Wind Speed
- Humidity

Source:
Open-Meteo

---

## Ratings

- Club Elo

Source:
ClubElo
