# Football Analytics Dashboard

A Python-based football analytics project that transforms historical match data into a reusable team-level dataset, validates the engineered data, and calculates a range of football performance metrics using Pandas.

The project was designed around a reusable analytics pipeline rather than creating separate data-processing logic for every metric.

---

## Overview

Football match data is naturally stored at the match level, with separate information for home and away teams.

This project transforms that raw match-level data into a standardized **team-match dataset**, where each row represents one team's performance in one match.

From this foundation, the project calculates reusable performance metrics such as:

- Average goals scored
- Goals scored
- Goals conceded
- Goal difference
- Points
- Home points per game
- Away points per game
- Win percentage
- Draw percentage
- Loss percentage
- Clean sheet percentage
- Home clean sheet percentage
- Away clean sheet percentage
- Goal-scoring standard deviation
- Home vs away consistency gap

The project also includes a data-quality layer that validates the engineered dataset before analytics are executed.

---

## Analytical Pipeline

```text
European Soccer Database
          ↓
     Data Loading
          ↓
   Match-Level Dataset
          ↓
 Team-Match Transformation
          ↓
   Feature Engineering
          ↓
    Data Quality Checks
          ↓
   Reusable Analytics
          ↓
 Metric Registry / Execution
          ↓
 Rankings & Analysis
          ↓
 Visualization Components
```

---

## Key Design Idea

Instead of writing separate data preparation logic for every metric, the project creates a centralized `team_matches` dataset.

Each row represents a team's performance in one match.

For example:

```text
Team ID | Goals Scored | Goals Conceded | Venue | Points
---------------------------------------------------------
Barcelona |      2      |       1        | Home  |   3
Real Madrid |   1      |       2        | Away  |   0
```

This structure makes it possible to reuse the same dataset across multiple analytical calculations.

---

## Data Pipeline

### 1. Data Loading

The project loads the required football data from the European Soccer Database using SQLite and Pandas.

The main datasets loaded are:

- Teams
- Matches

Relevant match fields include:

- Home team ID
- Away team ID
- Home team goals
- Away team goals
- Season
- Stage

---

### 2. Team-Match Transformation

The match-level data is transformed into a team-oriented structure.

For every match, two observations are created:

#### Home Team

```text
Team ID        → Home Team
Goals Scored   → Home Goals
Goals Conceded → Away Goals
Venue          → Home
```

#### Away Team

```text
Team ID        → Away Team
Goals Scored   → Away Goals
Goals Conceded → Home Goals
Venue          → Away
```

The two datasets are then combined into a single `team_matches` dataset.

This provides a consistent structure for team-level analysis.

---

## Feature Engineering

Several analytical features are derived from the team-match dataset.

### Goal Difference

```text
Goal Difference = Goals Scored - Goals Conceded
```

### Points

```text
Win  → 3 points
Draw → 1 point
Loss → 0 points
```

### Match Outcome

Boolean indicators are created for:

- Won
- Drawn
- Lost

### Clean Sheet

A clean sheet is identified when:

```text
Goals Conceded = 0
```

### Score

The match score is represented as:

```text
Goals Scored - Goals Conceded
```

These engineered features provide the foundation for the analytical layer.

---

## Data Quality Layer

The project validates the engineered dataset before analytics are executed.

The quality layer contains checks for:

### Null Values

Checks whether required fields contain missing values.

### Goal Difference

Verifies that:

```text
Goal Difference =
Goals Scored - Goals Conceded
```

### Points

Verifies that points correctly correspond to the match result:

```text
Win  → 3
Draw → 1
Loss → 0
```

### Clean Sheets

Verifies that the clean-sheet flag matches:

```text
Goals Conceded = 0
```

### Match Outcome Consistency

Checks that the `won`, `drawn`, and `lost` indicators correctly represent the match result and that exactly one outcome is assigned to every match.

If quality checks fail, the project reports the failed checks and prevents the analytics process from continuing with invalid data.

---

## Analytics Layer

The analytics layer contains reusable functions for calculating team performance metrics from the standardized dataset.

### Attacking Metrics

#### Average Goals Scored

Calculates the average number of goals scored per match.

#### Total Goals Scored

Calculates total goals scored across the available matches.

---

### Defensive Metrics

#### Average Goals Conceded

Calculates the average number of goals conceded per match.

#### Total Goals Conceded

Calculates total goals conceded.

#### Clean Sheet Percentage

Calculates the percentage of matches in which a team conceded zero goals.

---

### Performance Metrics

#### Goal Difference

Calculates:

```text
Goals Scored - Goals Conceded
```

#### Home Points Per Game

Calculates average points earned per home match.

```text
Home Points / Home Matches
```

#### Away Points Per Game

Calculates average points earned per away match.

```text
Away Points / Away Matches
```

#### Home vs Away Consistency Gap

Calculates the absolute difference between home and away points per game:

```text
| Home PPG - Away PPG |
```

A smaller gap indicates that a team's performance is more similar between home and away matches.

---

### Outcome Metrics

The project calculates:

- Win Percentage
- Draw Percentage
- Loss Percentage

These metrics are calculated from the engineered match-outcome indicators.

---

### Goal-Scoring Consistency

The project also calculates the standard deviation of goals scored by each team.

This provides a measure of how much a team's goals scored vary from match to match.

```text
Higher Standard Deviation
        ↓
Greater variation in goals scored
```

---

## Metric Registry

One of the main architectural components of the project is the centralized `METRIC_REGISTRY`.

Instead of hard-coding the behavior of every metric throughout the application, metrics are registered with information such as:

- Calculation function
- Output column
- Display label
- Formatting type
- Whether higher or lower values represent the desired direction

Example:

```python
"avg_goals": {
    "function": getTopAttackingTeams,
    "column": "avg_goals",
    "label": "Average Goals Scored",
    "higher_is_better": True,
    "format": "float"
}
```

This allows the analytics system to execute different metrics through a common interface.

---

## Reusable Analytics Execution

The project includes a `getTeamMetrics()` function that uses the metric registry to determine which analytical functions need to be executed.

The execution plan groups metrics that share the same underlying calculation.

This allows multiple related metrics to be calculated without unnecessarily repeating the same analytical operation.

The resulting metric datasets are merged using the team's unique API ID.

---

## Team Identification

The project uses `team_api_id` as the primary identifier when performing analytical operations.

Team names are added later for presentation.

This separates the analytical identifier from the human-readable team name and avoids relying on team names during the main data-processing steps.

---

## Visualization Layer

The project includes reusable Matplotlib visualization functions for presenting analytical results.

Available visualization types include:

### Horizontal Bar Charts

Used for ranking teams by different metrics.

Examples include:

- Average goals
- Goals scored
- Goals conceded
- Goal difference
- Other registered metrics

### Team Goal Difference Chart

Shows goal difference across match stages for an individual team.

### Goals Scored vs Goals Conceded

Compares a team's goals scored and goals conceded across match stages.

### Scatter Plot

Used to compare two analytical metrics and display their Pearson correlation.

The scatter plot can also annotate individual teams.

### Histogram

Used to display the distribution of a selected metric across teams.

### Correlation Heatmap

Displays correlations between engineered metrics.

---

## Sample Visualizations

The repository contains sample outputs generated from the analysis.

### Choices Panel

![Choices Panel](images/Choices%20panel.png)

### Top Attacking Teams

![Top Attacking Teams](images/Top%20Attacking%20Teams.png)

### Top Defensive Teams

![Top Defensive Teams](images/Top%20Defensive%20Teams.png)

### Goal Difference Rankings

![Goal Difference Rankings](images/Top%20Teams%20By%20Goal%20Difference.png)

### Clean Sheet Rankings

![Clean Sheet Rankings](images/Clean%20Sheets.png)

### Most Consistent Teams

![Most Consistent Teams](images/Most%20Consistent%20Teams.png)

---

## Project Structure

The project separates different responsibilities into dedicated modules.

```text
football-analytics-dashboard/
│
├── data/
│
├── images/
│
├── src/
│   ├── data_loader.py
│   ├── cleaner.py
│   ├── transforms.py
│   ├── quality.py
│   ├── analytics/
│   │   └── analytics.py
│   ├── chart_utils.py
│   ├── visualization.py
│   ├── style.py
│   └── main.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

### `data_loader.py`

Handles loading football data from SQLite into Pandas DataFrames.

### `cleaner.py`

Transforms match-level data into the reusable team-match dataset and creates engineered features.

### `transforms.py`

Handles transformations such as:

- Adding team names
- Formatting analytical results
- Filtering team-match data

### `quality.py`

Contains the data-quality validation checks.

### `analytics/analytics.py`

Contains the analytical functions and the centralized metric registry.

### `chart_utils.py`

Provides reusable chart creation and formatting utilities.

### `visualization.py`

Contains visualization functions for analytical results.

### `style.py`

Stores reusable visualization settings such as:

- Figure size
- Font sizes
- Grid settings
- Title formatting

### `main.py`

Provides the command-line interface for selecting metrics and displaying analytical results.

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- SQLite
- SQL
- Git
- GitHub

---

## Dataset

This project uses the **European Soccer Database** as its source of historical football match data.

The database is not included in the repository.

To run the project, place the SQLite database at:

```text
data/database.sqlite
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Navigate to the Project

```bash
cd football-analytics-dashboard
```

### 3. Install Dependencies

Install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

The project currently requires:

```text
pandas
numpy
matplotlib
```

SQLite is provided through Python's standard library.

### 4. Add the Database

Place the European Soccer Database SQLite file at:

```text
data/database.sqlite
```

### 5. Run the Analysis

```bash
python src/main.py
```

The program will run the data-quality checks before allowing the analytical metrics to be executed.

---

## Example Workflow

After starting the application, the user can select an analytical metric.

The workflow is:

```text
Load Match Data
      ↓
Load Team Data
      ↓
Build Team-Match Dataset
      ↓
Run Quality Checks
      ↓
Select Metric
      ↓
Calculate Team Metrics
      ↓
Add Team Names
      ↓
Format Results
      ↓
Display Ranking
```

---

## Analytical Thresholds

For several team-level ranking metrics, the project uses a minimum number of matches to reduce the influence of teams with very small samples.

The current analytical threshold is generally:

```text
100+ matches
```

This threshold is applied within the relevant analytical functions.

---

## Engineering Decisions

Several design decisions were made to improve maintainability and reuse.

### Centralized Team-Match Dataset

Instead of preparing separate datasets for every metric, the project creates one standardized team-match dataset.

### Feature Engineering Before Analysis

Common features such as points, goal difference, clean sheets, and match outcomes are calculated once and then reused.

### Separation of Responsibilities

The project separates:

```text
Data Loading
      ↓
Transformation
      ↓
Quality Validation
      ↓
Analytics
      ↓
Visualization
```

This keeps data preparation and analytical calculations from being tightly coupled.

### Team API IDs

The project uses `team_api_id` as the analytical identifier and adds human-readable team names when preparing results for presentation.

### Centralized Metric Registry

The metric registry allows the analytical system to work with different metrics through a common interface instead of creating separate execution logic for every metric.

---

## Project Scope

This project focuses on building a reusable football analytics workflow using Python and Pandas.

It is not intended to be a production football analytics platform.

The main objectives are:

- Transforming raw football match data
- Engineering reusable analytical features
- Validating the resulting dataset
- Building reusable team-performance metrics
- Creating visualizations from analytical results
- Structuring the project into separate data, analytics, quality, and visualization layers

---

## Current Limitations

The current project has several areas that could be expanded in the future.

It currently does not include:

- A web-based interactive dashboard
- Automated data collection
- Real-time football data
- Advanced player-level analytics
- Automated report generation
- A production data pipeline
- Advanced statistical modeling

---

## Future Improvements

Potential future improvements include:

- Form analysis based on recent matches
- Additional football performance metrics
- Player-level analysis
- Interactive visualizations
- Automated reporting
- Web-based dashboard interface
- Additional data-quality checks
- Automated data ingestion
- More advanced statistical analysis

---

## Learning Outcomes

Through this project, I gained practical experience with:

- Data extraction from SQLite
- Data transformation with Pandas
- Feature engineering
- Grouping and aggregation
- Analytical dataset design
- Data-quality validation
- Reusable analytics functions
- Metric registry design
- Visualization with Matplotlib
- Correlation analysis
- Modular Python architecture
- Git and GitHub workflows

---

## Author

**Abdelrahman Ahmed**

Computer Science student focused on **Data Analytics**, with a long-term specialization in **Football Analytics**.

Interested in using Python, SQL, and data visualization to transform raw data into useful analytical insights.
