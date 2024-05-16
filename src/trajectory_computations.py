import sys
from .analysis import analyze_single_trajectory, analyze_trajectories, remove_trajectory
from .point_mass_trajectory_optimization import calculate_tf, compute_alpha
from .shortest_path_search import shortest_path

def compute_single_trajectory(start_point, end_point, a_max, a_min, v_max, v_min, starting_velocity, ending_velocity, analyze=False, remove_bad=False):
    ''' Given an initial 2D poind, a final 2D point, velocities and acceleration constraints, compute the x and y trajectory parameters. 
        Scale the trajectory with the lowest tf to match the other trajectory and return both trajectories. '''
    x0, y0 = start_point
    xf, yf = end_point
    v0_x, v0_y = starting_velocity
    vf_x, vf_y = ending_velocity
    # Compute x and y trajectories
    x_results = calculate_tf(x0, v0_x, xf, vf_x, a_max, a_min, v_max, v_min)
    y_results = calculate_tf(y0, v0_y, yf, vf_y, a_max, a_min, v_max, v_min)
    # Pick trajectory with the lowest tf for both x and y
    x_result = min(x_results, key=lambda x: x[6])
    y_result = min(y_results, key=lambda x: x[6])
    # Return max of the two tf values
    if max(x_result[6], y_result[6]) == x_result[6]:
        # scale y solution to match x solution
        # scale max accelleration to match y solution
        recomputed_y_result = compute_alpha(y0, v0_y, yf, vf_y, a_max, a_min, v_max, v_min, x_result[6], y_result)
        if recomputed_y_result:
            if analyze:
                analyze_single_trajectory(x_result, recomputed_y_result[0] , start_point, end_point, starting_velocity, ending_velocity)
            if remove_bad and remove_trajectory(x_result, recomputed_y_result[0], start_point, end_point):
                return ((0,0,0,0,0,0,sys.maxsize,0,0), (0,0,0,0,0,0,sys.maxsize,0,0))
            return x_result, recomputed_y_result[0]
        return ((0,0,0,0,0,0,sys.maxsize,0,0), (0,0,0,0,0,0,sys.maxsize,0,0))
    elif max(x_result[6], y_result[6]) == y_result[6]:
        # scale x solution to match y solution
        # scale max accelleration to match x solution
        recomputed_x_result = compute_alpha(x0, v0_x, xf, vf_x, a_max, a_min, v_max, v_min, y_result[6], x_result)
        if recomputed_x_result:
            if analyze:
                analyze_single_trajectory(recomputed_x_result[0], y_result, start_point, end_point, starting_velocity, ending_velocity)
            if remove_bad and remove_trajectory(recomputed_x_result[0], y_result, start_point, end_point):
                return ((0,0,0,0,0,0,sys.maxsize,0,0), (0,0,0,0,0,0,sys.maxsize,0,0))
            return recomputed_x_result[0], y_result
        return ((0,0,0,0,0,0,sys.maxsize,0,0), (0,0,0,0,0,0,sys.maxsize,0,0))

def compute_trajectory_set(points, a_max, a_min, v_max, v_min, starting_velocity_list, ending_velocity_list, df, start_index, end_index, prediction_horizon):
    ''' Given two points, compute all possible trajectories between the two points using the provided velocity lists. Assemble the results in the dictionary used for the shortest path algorithm. 
    In such dictionary, all the intermediate graph nodes with the same starting coordinates but different starting velocities are cosidered as different states'''
    start_point = points[start_index]
    end_point= points[end_index]
    results = []
    for i, v0 in enumerate(starting_velocity_list):
        if start_index == 0 and i == 0:
                df[f'{start_index}'] = {}
        elif start_index !=0:
            df[f'{start_index}_{i}'] = {}
        for j, vf in enumerate(ending_velocity_list):
            x_result, y_result = compute_single_trajectory(start_point, end_point, a_max, a_min, v_max, v_min, v0, vf, analyze=False, remove_bad=False)
            params = (x_result, y_result)
            if start_index == 0 and prediction_horizon == 1:
                if (not f'{end_index}_f' in df[f'{start_index}'].keys()) or (params[0][6]<df[f'{start_index}'][f'{end_index}_f'][0][6]):
                    df[f'{start_index}'][f'{end_index}_f'] = params
                    df[f'{end_index}_f'] = {}
            elif start_index == 0:
                if (not f'{end_index}_{j}' in df[f'{start_index}'].keys()) or (params[0][6]<df[f'{start_index}'][f'{end_index}_{j}'][0][6]):
                    df[f'{start_index}'][f'{end_index}_{j}'] = params # create new state for every in between index
            elif start_index == prediction_horizon - 1:
                if (not f'{end_index}_f' in df[f'{start_index}_{i}'].keys()) or (params[0][6]<df[f'{start_index}_{i}'][f'{end_index}_f'][0][6]):
                    df[f'{start_index}_{i}'][f'{end_index}_f'] = params
                    df[f'{end_index}_f'] = {}
            else:
                if (not f'{end_index}_{j}' in df[f'{start_index}_{i}'].keys()) or (params[0][6]<df[f'{start_index}_{i}'][f'{end_index}_{j}'][0][6]):
                    df[f'{start_index}_{i}'][f'{end_index}_{j}'] = params
            results.append((x_result, y_result))
    return results, df

def compute_all_trajectories(points, df, max_acc, min_acc, max_vel, min_vel, prediction_horizon=None):
    ''' Given a list of points, compute all possible trajectories between the points using the provided acceleration and velocity constraints.'''
    results = []
    dict_res = {}

    if not prediction_horizon:
        prediction_horizon = len(points)
        
    points_to_inspect = points[0:prediction_horizon]
    for i in range(prediction_horizon):
        start_point = points[i]
        start_vel = df[i]
        if i == len(points) - 1:
            end_point = 0
            end_vel = df[0]
        else:
            end_point = i+1
            end_vel = df[i + 1]
        trajectories, dict_res = compute_trajectory_set(points, max_acc, min_acc, max_vel, min_vel, start_vel, end_vel, dict_res, i, end_point, prediction_horizon)
        results.extend(trajectories)
    if prediction_horizon == len(points):
        cost, shortest = shortest_path(dict_res, '0', '0_f')
    else:
        cost, shortest = shortest_path(dict_res, '0', f'{prediction_horizon}_f')
    return results, dict_res, shortest
