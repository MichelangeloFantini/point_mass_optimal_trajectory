
from src.point_mass_trajectory_optimization import calculate_tf, compute_alpha
from src.plotting import plot_curves, plot_single_trajectory, plot_multiple_trajectories, plot_multiple_trajectories_and_velocities
from src.trajectory_computations import compute_single_trajectory, compute_trajectory_set


def alpha_example():
    ''' Given the initial conditions first calculate the trajectory and velocity graoh over time, then scale such graph to match the profided tf value. '''
    x0 = 10
    v0 = -2.7649061254141962
    xf = -9
    vf = 0.9934426892429724
    a_max = 1
    a_min = -1
    v_max = 3
    v_min = -3

    wanted_tf = 10

    results = calculate_tf(x0, v0, xf, vf, a_max, a_min, v_max, v_min)
    print('computing alpha')
    results.extend(compute_alpha(x0, v0, xf, vf, a_max, a_min, v_max, v_min, wanted_tf, results[0]))
    plot_curves(results)

def single_trajectory_example():
    ''' Given an initial 2D poind , a final 2D point, velocities and acceleration constraints, compute the trajectory and velocity graph over time and plot them in a x-y graph '''
    start_point = (10, 15)
    end_point = (-9, 7)
    a_max = 1
    a_min = -1
    v_max = 3
    v_min = -3
    v0 = (-2.7649061254141962, -1.1641710001743981)
    vf = (0.9934426892429724, -0.11433119954627809)
    x_result, y_result = compute_single_trajectory(start_point, end_point, a_max, a_min, v_max, v_min, v0, vf)
    plot_single_trajectory(x_result, y_result)

def multiple_trajectories_example():
    ''' Given a list of points, acceleration and velocity constraints, starting and ending velocities, compute the trajectory and velocity graph over time for each trajectory and plot them in a x-y graph '''
    start_point = (0, 0)
    end_point = (-2, -3)
    points = [start_point, end_point]
    a_max = 1
    a_min = -1
    v_max = 0.75
    v_min = -0.75
    starting_velocity_list = [(0.5, 0.5), (0, 0)]
    ending_velocity_list = [(0, 0)]
    results, _ = compute_trajectory_set(points, a_max, a_min, v_max, v_min, starting_velocity_list, ending_velocity_list, {}, 0, 1, len(points))
    plot_multiple_trajectories_and_velocities(results)

if __name__ == '__main__':
    alpha_example()
    single_trajectory_example()
    multiple_trajectories_example()     