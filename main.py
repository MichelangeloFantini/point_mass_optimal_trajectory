from src.velocity_generation import compute_velocities_in_cone
from src.trajectory_computations import compute_all_trajectories
from src.plotting import plot_all_trajectories_and_shortest_path, plot_multiple_trajectories_and_velocities

if __name__ == '__main__':
    points = [(1, 2), (10, 15), (-9, 7), (7,6)]  # Example 2D points
    module_min = 1  # Minimum velocity magnitude
    module_max = 3  # Maximum velocity magnitude
    vertex_angle_deg = 20  # Vertex angle of the cone in degrees
    prediction_horizon = 3
    if not prediction_horizon:
        df = compute_velocities_in_cone(points, module_min, module_max,vertex_angle_deg=vertex_angle_deg, angle_step=5, prediction_horizon=prediction_horizon, loop=True)
    else:
        df = compute_velocities_in_cone(points, module_min, module_max, vertex_angle_deg=vertex_angle_deg, angle_step=5, prediction_horizon=prediction_horizon, loop=False)
    results, dict_res, shortest = compute_all_trajectories(points,df, 1, -1, module_max, -module_max, prediction_horizon=prediction_horizon)
    plot_all_trajectories_and_shortest_path(results, points, dict_res, shortest)
