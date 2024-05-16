import numpy as np

from pyroboplan.models.two_dof import (
    load_models,
)
from pyroboplan.planning.prm import PRMPlanner, PRMPlannerOptions


# Use a fixed seed for random number generation in tests.
np.random.seed(1234)


def test_construct_roadmap():
    model, collision_model, _ = load_models()
    options = PRMPlannerOptions(max_construction_nodes=100)

    # Initial the planner and do the sampling
    planner = PRMPlanner(model, collision_model, options=options)
    planner.construct_roadmap()

    # Planning should succeed and should have the correct start and end poses
    assert len(planner.graph.nodes) > 0
    assert len(planner.graph.edges) > 0


def test_plan_trivial_prm():
    model, collision_model, _ = load_models()
    q_start = np.array([0.0, 0.0])
    q_goal = q_start + 0.01

    # Plan with default parameters, we do not need to initialize as the start and goal
    # configurations are directly connectable.
    planner = PRMPlanner(model, collision_model)
    path = planner.plan(q_start, q_goal)

    assert path is not None
    assert len(path) == 2
    assert np.all(path[0] == q_start)
    assert np.all(path[1] == q_goal)


def test_prm():
    model, collision_model, _ = load_models()
    q_start = np.array([0.0, 0.0])
    q_goal = np.array([0.5, 0.5])

    # Be very generous with connections.
    options = PRMPlannerOptions(
        max_angle_step=0.05,
        max_neighbor_radius=0.5,
        max_neighbor_connections=5,
        max_construction_nodes=2500,
        construction_timeout=1.0,
        prm_file=None,
    )

    # Initial the planner and do the sampling
    planner = PRMPlanner(model, collision_model, options=options)
    planner.construct_roadmap()
    path = planner.plan(q_start, q_goal)

    # Planning should succeed and should have the correct start and end poses
    assert path is not None
    assert len(path) > 2
    assert np.array_equal(path[0], q_start)
    assert np.array_equal(path[-1], q_goal)