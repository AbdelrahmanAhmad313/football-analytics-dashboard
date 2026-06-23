# Football Analytics Dashboard

## Overview

This project is a football analytics dashboard built using Python, Pandas, SQLite, and SQL. The goal was to transform raw match data into a reusable analytics dataset and build multiple performance metrics on top of it.

A major focus of the project was analytics engineering and pipeline design. Instead of creating separate queries and calculations for each metric, the project was refactored around a centralized match-level dataset that serves as the foundation for all analytics.

## Dataset

This project uses the European Soccer Database.

The database is not included in this repository due to its size.

## Technologies Used

* Python
* Pandas
* SQLite
* SQL
* Git
* GitHub

## Architecture

The project follows a layered architecture:

```text
Raw Match Data
        ↓
Data Loader
        ↓
Feature Engineering
        ↓
team_matches_df
        ↓
Analytics Layer
        ↓
Visualization Layer
        ↓
Dashboard Output
```

### Project Structure

```text
football-analytics-dashboard/
│
├── data/
│
├── src/
│   ├── analytics.py
│   ├── cleaner.py
│   ├── data_loader.py
│   ├── visualization.py
│   └── main.py
│
├── README.md
└── .gitignore
```

## Reusable Analytics Dataset

The project creates a reusable `team_matches_df` dataset where each row represents a single team's performance in a single match.

### Core Columns

* team_api_id
* goals_scored
* goals_conceded
* venue
* points

### Engineered Features

* goal_diff
* score
* clean_sheet
* won
* drawn
* lost

This dataset serves as the foundation for all analytics calculations.

## Implemented Metrics

### Attacking Metrics

* Top Attacking Teams
* Average Goals Scored

### Defensive Metrics

* Top Defensive Teams
* Average Goals Conceded
* Clean Sheet Percentage
* Home Clean Sheet Percentage
* Away Clean Sheet Percentage

### Performance Metrics

* Goal Difference Rankings
* Average Goal Difference
* Home Points Per Game (PPG)
* Away Points Per Game (PPG)
* Home vs Away Consistency Gap

### Outcome Metrics

* Win Percentage
* Draw Percentage
* Loss Percentage

## Engineering Improvements

During development, the analytics pipeline was refactored to improve maintainability and scalability.

Key improvements included:

* Creating a centralized `team_matches_df` foundation dataset
* Eliminating repeated SQL queries
* Eliminating repeated merge logic
* Replacing team-name joins with `team_api_id`
* Centralizing feature engineering logic
* Building reusable analytics functions
* Separating data loading, cleaning, analytics, and visualization responsibilities

## Running the Project

1. Clone the repository

```bash
git clone <repository-url>
```

2. Navigate to the project directory

```bash
cd football-analytics-dashboard
```

3. Install dependencies

```bash
pip install pandas
```

4. Place the database file inside the `data` directory

```text
data/database.sqlite
```

5. Run the dashboard

```bash
python src/main.py
```

## Future Improvements

Potential future enhancements include:

* Form analysis based on recent matches
* Interactive visualizations
* Additional advanced football metrics
* Automated reporting
* Web-based dashboard interface

## Learning Outcomes

Through this project, I gained hands-on experience with:

* Data cleaning and transformation
* Feature engineering
* Pandas aggregations and grouping
* Analytics pipeline design
* Refactoring and code organization
* Building reusable data products
* Sports analytics concepts
* Git and GitHub workflows
