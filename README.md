# Football Simulation Engine

A football match prediction engine built with Python.

## Features

- Understat data collection
- SQLite database
- Team rating calculation
- Expected Goals (xG) model
- Poisson goal model
- Match outcome probabilities
- Most likely scorelines

## Project Structure

```
Football-Simulation-Engine
│
├── data
│
├── src
│   ├── collectors
│   ├── config.py
│   ├── database
│   ├── prediction
│   ├── ratings
│   └── services
│
├── predict.py
├── update_database.py
└── README.md
```

## Installation

```bash
git clone <repository>
cd Football-Simulation-Engine

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

Update database:

```bash
python update_database.py
```

Predict a match:

```bash
python predict.py
```

Example:

```
Match:
Arsenal vs Liverpool
```

## Roadmap

- [x] Understat Collector
- [x] SQLite Database
- [x] Team Ratings
- [x] Expected Goals
- [x] Poisson Model
- [x] Match Prediction
- [x] Prediction Service
- [ ] Evaluation Engine
- [ ] Dixon-Coles Model
- [ ] Monte Carlo Simulation
- [ ] Season Simulation
- [ ] Streamlit Interface

## License

MIT