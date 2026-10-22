# MAPPO — Air-Quality Forecasting & Low-Pollution Routing

Backend for **MAPPO**, a citizen-science mobile app that shows urban air pollution, forecasts NO₂ levels and suggests walking or driving routes that minimise exposure. Built as a team project for the *Advanced Engineering Project* (PAE) course at UPC · ETSETB (2022), in collaboration with environmental-sensor data from shared e-scooters.

This repository contains the parts I worked on: the **forecasting models**, the **pollution-aware routing engine** and the **REST API server** that integrates them.

## What it does

| Endpoint | Description |
|---|---|
| `GET /database?option=avg_no2` | Pollutant measurements (CO, NO₂, PM10 — detailed or averaged) from the PostgreSQL sensor database |
| `GET /routing?option=lesspolluted&city=…&originx=…&originy=…&destinationx=…&destinationy=…` | Route between two points: `shortest`, `lesspolluted` or `mix` |
| `GET /forecast?option=…` | Next-day NO₂ forecast from an LSTM trained on station history |

## How it works

**Pollution map.** Point measurements are interpolated onto a grid over the city (nearest-neighbour averaging) to produce a continuous pollution surface.

**Routing.** The city street network is downloaded from OpenStreetMap with `osmnx` (walk or drive network). Each edge is weighted with the pollution value of the grid cells it crosses, and `networkx` shortest-path search is run on either distance, pollution exposure, or a mix of both. Routes are rendered on an interactive `folium` map.

**Forecasting.** Daily NO₂ averages are framed as a supervised time-series problem (lagged inputs, differencing, Min-Max scaling) and fitted with a Keras LSTM. Notebooks compare it against a persistence baseline and tune lag, neurons and epochs.

```
          ┌───────────── Flask API (server/app.py, gunicorn, Docker) ─────────────┐
 mobile ──►  /database ── PostgreSQL     /routing ── osmnx + networkx     /forecast ── LSTM
 app      └──────────────────────────────────────────────────────────────────────┘
```

## Repository layout

```
├── server/        Flask API, routing engine (mappoAPIserver_latest.py), LSTM, Dockerfile
├── routing/       Stand-alone pollution-map generator and route experiments (CLI menu)
├── forecast/      Data extraction from PostgreSQL and forecasting scripts
└── notebooks/     LSTM training, hyperparameter search, persistence baseline
```

## Run

```bash
cd server
pip install -r requirements.txt
export DATABASE_URL=postgresql://user:password@host:5432/dbname   # see .env.example
gunicorn --bind 0.0.0.0:8000 wsgi
```

Or with Docker (originally deployed on Heroku):

```bash
docker build -t mappo-server server/
docker run -e PORT=8000 -e DATABASE_URL=... -p 8000:8000 mappo-server
```

The first routing request for a city downloads and caches its OSM graph, which can take a while.

## Tech

Python · Flask · gunicorn · Docker · PostgreSQL (psycopg2) · Keras/TensorFlow · scikit-learn · pandas · osmnx · networkx · folium

## Team

MAPPO was developed by a multidisciplinary student team at UPC. The original team repository is [annapuig/MAPPO](https://github.com/annapuig/MAPPO); this repo is a cleaned-up extract of my contributions with credentials removed and large data files omitted.
