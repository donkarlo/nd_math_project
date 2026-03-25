from pyomo.environ import ConcreteModel, Var, Objective, Constraint, NonNegativeReals, minimize, SolverFactory

# Create model
model = ConcreteModel()

# Variables
model.x_A = Var(domain=NonNegativeReals)
model.x_B = Var(domain=NonNegativeReals)

# Objective: minimize cost
model.cost = Objective(expr=2 * model.x_A + 5 * model.x_B, sense=minimize)

# Constraint: total production >= 10
model.demand = Constraint(expr=model.x_A + model.x_B >= 10)

# Solve (using GLPK or Gurobi if installed)
solver = SolverFactory("glpk")  # or "gurobi"
solver.solve(model)

# Results
print("x_A =", model.x_A())
print("x_B =", model.x_B())
print("Total cost =", model.cost())