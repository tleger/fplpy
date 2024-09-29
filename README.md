# fplpy

A simple project that reads player data from the Fantasy Premier League API and uses pyomo to 
optimise a team selection.

## Objective Function

The objective function aims to maximize the total points of the selected team. 

## Constraints

The constraints applied in this project ensure that the selected team adheres to the rules of 
the Fantasy Premier League. These constraints include:

- **Budget Constraint**: The total cost of the selected players must not exceed the available budget.
- **Team Size Constraint**: The team must consist of exactly 15 players.
- **Position Constraints**: The team must include a specific number of players for each position 
(e.g., 2 goalkeepers, 5 defenders, 5 midfielders, and 3 forwards).
- **Team Limit Constraint**: No more than 3 players can be selected from the same real-life football team.