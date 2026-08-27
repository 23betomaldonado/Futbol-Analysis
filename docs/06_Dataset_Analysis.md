Feature Engineering for Futbol Analysis

# Fútbol Analysis

# Dataset Analysis

## Overview

This document analyzes the datasets collected for Fútbol Analysis. The purpose is to understand what information each dataset provides, determine its usefulness, identify limitations, and decide how it will be used throughout the project.

The datasets will remain unchanged inside the `data/raw` directory. Rather than combining every dataset into one large table, each dataset will serve a specific purpose. Relevant information from these datasets will later be transformed into features for machine learning.

---

# Dataset 1: FIFA Rankings (2022)

## File Name

fifa_ranking_2022-10-06.csv

## Summary

Rows: 212

Columns: 7

## Columns

team

team_code

association

rank

previous_rank

points

previous_points

## Purpose

Provides the official FIFA rankings shortly before the 2022 FIFA World Cup.

## Strengths

Official FIFA ranking data.

Represents overall team strength.

Easy to integrate into future match predictions.

## Limitations

Only represents one point in time.

Does not include recent match information.

## Decision

Keep.

Use FIFA rank and ranking points as predictive features.

---

# Dataset 2: FIFA Rankings (2026)

## File Name

fifa_ranking_2026-06-08.csv

## Summary

Rows: 212

Columns: 8

## Columns

team

team_code

association

rank

previous_rank

points

previous_points

rated_matches

## Purpose

Provides updated FIFA rankings before the 2026 World Cup.

## Strengths

Most current ranking information.

Includes the number of rated matches.

Useful for predicting future tournaments.

## Limitations

Contains one additional column not present in the 2022 ranking dataset.

## Decision

Keep.

Use for future match predictions.

---

# Dataset 3: Historical Matches

## File Name

matches_1930_2022.csv

## Summary

Rows: 964

Columns: 44

## Purpose

Primary dataset for machine learning.

Contains historical World Cup matches with detailed match statistics and contextual information.

## Strengths

Historical match results.

Scores.

Expected goals (xG).

Managers.

Captains.

Venue information.

Attendance.

Referee information.

Match events.

Provides the foundation for predicting match outcomes.

## Limitations

Does not include recent World Cup tournaments.

Some columns may contain missing values.

## Decision

Core dataset.

This will be the primary dataset used for Version 1 of Fútbol Analysis.

---

# Dataset 4: 2026 Match Schedule

## File Name

schedule_2026.csv

## Summary

Rows: 73

Columns: 10

## Purpose

Contains scheduled matches for the 2026 World Cup.

## Strengths

Useful for generating predictions once machine learning models are completed.

## Limitations

Incomplete.

Several columns contain empty values.

Not suitable for model training.

## Decision

Reserve for future prediction demonstrations.

---

# Dataset 5: World Cup Summary

## File Name

world_cup.csv

## Summary

Rows: 23

Columns: 9

## Purpose

Contains historical tournament information.

## Strengths

Useful for historical summaries and visualizations.

## Limitations

Small dataset.

Insufficient for machine learning.

## Decision

Optional dataset.

Use only for historical insights and visualizations.

---

# Dataset 6: Player Performance

## File Name

player_performance.xlsx

## Summary

Approximately 54,600 player records.

75 columns.

## Purpose

Provides detailed player-level statistics and performance metrics.

## Strengths

Large dataset.

Includes player information.

Performance statistics.

Market value.

Physical attributes.

Advanced performance metrics.

Potential for player comparisons and scouting analysis.

## Limitations

Player-level data must be aggregated before it can be used to predict team match outcomes.

Requires significant preprocessing.

## Decision

Keep.

This dataset will become the foundation for future player analysis and advanced feature engineering.

---

# Overall Conclusions

The project will not merge every dataset into one large table.

Instead, each dataset will remain independent and serve a different purpose.

The historical matches dataset will serve as the primary training dataset.

The FIFA ranking datasets will provide information about team strength.

The player performance dataset will be used to generate team-level features in future versions.

The schedule dataset will be used after models are trained to predict upcoming matches.

The World Cup summary dataset will primarily support visualizations and historical information.

