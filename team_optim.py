import pandas as pd
from pyomo.environ import (
    ConcreteModel,
    Var,
    Objective,
    Constraint,
    SolverFactory,
    maximize,
    Binary,
)

player_data = pd.read_csv("fpl_player_data.csv")

model = ConcreteModel()

model.players = Var(player_data.index, within=Binary)

# Pick, as a starting point, a team that maximises total points scored so far.
model.objective = Objective(
    expr=sum(
        player_data.loc[i, "total_points"] * model.players[i] for i in player_data.index
    ),
    sense=maximize,
)

# Define the constraints
# Budget constraint
model.budget_constraint = Constraint(
    expr=sum(
        player_data.loc[i, "now_cost"] * model.players[i] for i in player_data.index
    )
    <= 1000  # 100.0 in FPL terms
)

# Team size constraint
model.team_size_constraint = Constraint(
    expr=sum(model.players[i] for i in player_data.index) == 15
)

# Position constraints
model.goalkeepers_constraint = Constraint(
    expr=sum(
        model.players[i]
        for i in player_data.index
        if player_data.loc[i, "element_type"] == 1
    )
    == 2
)
model.defenders_constraint = Constraint(
    expr=sum(
        model.players[i]
        for i in player_data.index
        if player_data.loc[i, "element_type"] == 2
    )
    == 5
)
model.midfielders_constraint = Constraint(
    expr=sum(
        model.players[i]
        for i in player_data.index
        if player_data.loc[i, "element_type"] == 3
    )
    == 5
)
model.forwards_constraint = Constraint(
    expr=sum(
        model.players[i]
        for i in player_data.index
        if player_data.loc[i, "element_type"] == 4
    )
    == 3
)

# Team constraints (max 3 players per team)
teams = player_data["team"].unique()
for team in teams:
    model.add_component(
        f"team_{team}_constraint",
        Constraint(
            expr=sum(
                model.players[i]
                for i in player_data.index
                if player_data.loc[i, "team"] == team
            )
            <= 3
        ),
    )

# Solve the model
solver = SolverFactory("glpk")
solver.solve(model)

# Extract the selected players
selected_players = [i for i in player_data.index if model.players[i].value == 1]
print(player_data.loc[selected_players])
