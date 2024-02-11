from pyomo.environ import *

def graph_coloring(graph):
    model = ConcreteModel()

    # Define vertices and colors
    vertices = graph.nodes()
    colors = range(1, len(vertices) + 1)

    # Decision Variables
    model.x = Var(vertices, colors, within=Binary)

    # Constraints
    model.constraints = ConstraintList()

    # Each vertex must be assigned exactly one color
    for v in vertices:
        model.constraints.add(sum(model.x[v, c] for c in colors) == 1)

    # No two adjacent vertices can have the same color
    for (i, j) in graph.edges():
        for c in colors:
            model.constraints.add(model.x[i, c] + model.x[j, c] <= 1)

    # # Symmetry breaking constraint
    # for v in vertices:
    #     for c in colors[:-1]:
    #         model.constraints.add(model.x[v, c] >= model.x[v, c + 1])

    # Objective Function (Minimize the total number of colors)
    model.objective = Objective(expr=sum(model.x[v, c] for v in vertices for c in colors), sense=minimize)

    # Solve the model using appsi_highs solver
    solver = SolverFactory('appsi_highs')
    solver.solve(model)

    # Extract and return the solution
    coloring = {}
    for v in vertices:
        for c in colors:
            if value(model.x[v, c]) == 1:
                coloring[v] = c
                break

    return coloring

# Example usage:
if __name__ == '__main__':
    import networkx as nx

    # Create a sample graph (you can replace this with your own graph)
    G = nx.Graph()
    G.add_edges_from([(0, 16), (1, 2), (1, 6), (1, 7), (1, 8), (2, 11), (2, 16), (2, 17), (3, 14), (3, 16), (3, 17), (4, 7), (4, 13), (4, 17), (5, 6), (5, 11), (6, 18), (9, 12), (10, 13), (11, 17), (13, 15), (15, 17), (16, 19)])

    # Solve the graph coloring problem
    solution = graph_coloring(G)
    print("Vertex Coloring:", solution)
