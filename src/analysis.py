import numpy as np

from .point_mass_trajectory_optimization import space_curve
from .plotting import plot_single_trajectory


def analyze_trajectories(points, results, threshold=0.2):
    ''' Given a list of points and a list of trajectory results, analyze the trajectories and return the bad trajectories.
    A trajectory is considered bad if its end point is not within the threshold distance of any of the points.'''
    bad_trajectories = []
    for i in results:
        tragetory_is_good = False
        x_result, y_result = i
        x0_x, v0_x, a2_x, a3_x, a4_x, a5_x, tf_x, ts_x, ts_1_x = x_result
        y0_y, v0_y, a2_y, a3_y, a4_y, a5_y, tf_y, ts_y, ts_1_y = y_result
        xf = space_curve(tf_x, x0_x, v0_x, a2_x, a3_x, a4_x, a5_x, ts_x, ts_1_x)
        yf = space_curve(tf_y, y0_y, v0_y, a2_y, a3_y, a4_y, a5_y, ts_y, ts_1_y)
        for point in points:
            if np.sqrt((xf - point[0])**2 + (yf - point[1])**2) < threshold:
                tragetory_is_good = True
                continue
        if not tragetory_is_good:
            bad_trajectories.append(i)
    print("percentage of bad trajectories: ", len(bad_trajectories)/len(results))
    return bad_trajectories

def analyze_single_trajectory(x_result, y_result, start_point, end_point, starting_velocity, ending_velocity, threshold=0.2):
    ''' Given a single trajectory, analyze the trajectory and plot it if it does not meet the space constraints.'''
    x0_x, v0_x, a2_x, a3_x, a4_x, a5_x, tf_x, ts_x, ts_1_x = x_result
    y0_y, v0_y, a2_y, a3_y, a4_y, a5_y, tf_y, ts_y, ts_1_y = y_result
    xf = space_curve(tf_x, x0_x, v0_x, a2_x, a3_x, a4_x, a5_x, ts_x, ts_1_x)
    yf = space_curve(tf_y, y0_y, v0_y, a2_y, a3_y, a4_y, a5_y, ts_y, ts_1_y)
    if np.sqrt((xf - end_point[0])**2 + (yf - end_point[1])**2) >  threshold:
        print("trajectory is bad")
        print("start point: ", start_point, "end point: ", end_point)
        print("start velocity: ", starting_velocity, "end velocity: ", ending_velocity)
        print("computed end point: ", (xf, yf))
        print("x result: ", x_result)
        print("y result: ", y_result)
        plot_single_trajectory(x_result, y_result)

def remove_trajectory(x_result, y_result, start_point, end_point, threshold=0.2):
    ''' Given a single trajectory, return True if the trajectory does not meet the space constraints.'''
    x0_x, v0_x, a2_x, a3_x, a4_x, a5_x, tf_x, ts_x, ts_1_x = x_result
    y0_y, v0_y, a2_y, a3_y, a4_y, a5_y, tf_y, ts_y, ts_1_y = y_result
    xf = space_curve(tf_x, x0_x, v0_x, a2_x, a3_x, a4_x, a5_x, ts_x, ts_1_x)
    yf = space_curve(tf_y, y0_y, v0_y, a2_y, a3_y, a4_y, a5_y, ts_y, ts_1_y)
    if np.sqrt((xf - end_point[0])**2 + (yf - end_point[1])**2) > threshold:
        return True
    return False