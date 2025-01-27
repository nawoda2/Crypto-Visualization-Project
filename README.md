# Crypto Data Visualization Platform

**A scalable end-to-end data engineering workflow for ingesting and analyzing cryptocurrency market data from CoinGecko, orchestrated by Airflow, stored in PostgreSQL, and visualized in Metabase.**

---

## Table of Contents

1. [Overview](#overview)  
2. [Architecture](#architecture)  
3. [Tech Stack](#tech-stack)  
4. [Getting Started](#getting-started)  
   - [Prerequisites](#prerequisites)  
   - [Installation & Setup](#installation--setup)  
5. [Usage](#usage)  
   - [Running the Pipeline](#running-the-pipeline)  
   - [Accessing the Database](#accessing-the-database)  
   - [Metabase Dashboards](#metabase-dashboards)  
6. [Troubleshooting](#troubleshooting)  
7. [Key Learnings](#key-learnings)  
8. [Future Improvements](#future-improvements)  
9. [License](#license)

---

## Overview

This repository demonstrates a **complete data engineering project** that fetches **cryptocurrency market data** from the [CoinGecko API](https://www.coingecko.com/en/api/documentation), loads it into **PostgreSQL**, orchestrates the pipeline with **Apache Airflow**, and presents real-time insights using **Metabase**. The workflow runs on **Docker** containers for reproducibility and ease of deployment.

### Why This Project Matters

- **End-to-End Pipeline**: Showcases ingestion, transformation (basic), storage, orchestration, and visualization.  
- **Scalability**: Modular design allows for easy extension, scaling, or migration to cloud environments.  
- **Data Integrity**: Relational database ensures structured, consistent data storage.  
- **Actionable Insights**: Metabase dashboards reveal market cap distribution, price movements, and more.

---

## Architecture

                         +--------------------+
                         |   CoinGecko API    |
                         +---------+----------+
                                   |
                                   v
                           (1) Ingestion
                                   |
             +------------------------------------+
             |    Docker: ingestion-container      |
             | Python script fetches, transforms,  |
             | and loads data into PostgreSQL.     |
             +----------------+---------------------+
                               |
                               v
                      +-----------------+
                      |   PostgreSQL    |
                      |  crypto_data    |
                      +--------+--------+
                               |
                               v
                         +-------------+
             (2) Orchestration: Airflow
                         +-------------+
                             DAG: crypto_ingestion_dag
                             Schedules and retries ingestion
                               |
                               v
                     +-----------------+
                     |   Metabase      |
                     |   Visualization |
                     +-----------------+

1. **Data Ingestion**  
   - Python script (`data_ingestion.py`) calls CoinGecko API to fetch up to 250 coins per page.  
   - Insert rows into `crypto_data` table in PostgreSQL.

2. **Data Storage**  
   - PostgreSQL table schema:
     ```sql
     CREATE TABLE crypto_data (
       id SERIAL PRIMARY KEY,
       coin_id VARCHAR(50),
       symbol VARCHAR(10),
       name VARCHAR(100),
       current_price NUMERIC,
       market_cap NUMERIC,
       total_volume NUMERIC,
       timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
     ```

3. **Workflow Orchestration**  
   - **Apache Airflow** DAG (`crypto_ingestion_dag`):
     - Runs the ingestion script via **DockerOperator** on a defined schedule (e.g., hourly).
     - Handles retries and logs.

4. **Containerization**  
   - **Docker & Docker Compose** manage consistent environments for:
     - Airflow (Webserver & Scheduler)
     - PostgreSQL
     - Ingestion container
     - (Optional) Metabase

5. **Visualization**  
   - **Metabase** connects to PostgreSQL to create dashboards:
     - Coins by Market Cap  
     - Top Coins with Largest Price Movements  
     - Market Cap Distribution  
     - …and more

---

## Tech Stack

| Category            | Technologies            |
|---------------------|-------------------------|
| **Data Engineering**| Apache Airflow, Docker |
| **Database**        | PostgreSQL             |
| **Language**        | Python 3.x             |
| **Visualization**   | Metabase               |
| **API**             | CoinGecko              |

---

## Getting Started

### Prerequisites

- **Docker** & **Docker Compose** installed on your machine.  
- An optional **CoinGecko API key** if using Pro endpoints. (Public endpoints may not require a key, subject to rate limits.)

### Installation & Setup

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/<your-username>/crypto-visualization.git
   cd crypto-visualization
