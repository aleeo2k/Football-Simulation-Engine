# Data Model

## Purpose

This document describes all entities used by the Football Simulation Engine and the relationships between them.

The goal is to design a scalable data model that supports automatic updates, historical data storage, simulations and machine learning.

---

# Core Entities

The system consists of the following entities:

- League
- Season
- Team
- Player
- Match
- Lineup
- Event
- Team Statistics
- Player Statistics
- Team Ratings
- Player Ratings
- Prediction
- Simulation
- Weather

---

## Entity Relationships

League
└── Seasons

Season
└── Matches

Match
├── Home Team
├── Away Team
├── Lineups
├── Events
├── Statistics
├── Weather
├── Prediction
└── Simulation

Team
├── Players
├── Ratings
└── Statistics

Player
├── Ratings
├── Statistics
└── Match Appearances
