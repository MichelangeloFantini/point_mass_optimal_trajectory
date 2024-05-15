import numpy as np
import matplotlib.pyplot as plt

from .point_mass_trajectory_optimization import space_curve, velocity_curve

def plot_curves(results):
    '''Plot the space and velocity curves on a time series plot for each trajectory in the results list.'''
    plt.figure(figsize=(12, 6))
    
    for i, args in enumerate(results):
        a0, a1, a2, a3, a4, a5, tf, ts, ts_1 = args

        t_values = np.linspace(0, tf, 1000)
        space_values = [space_curve(t, a0, a1, a2, a3, a4, a5, ts, ts_1) for t in t_values]
        velocity_values = [velocity_curve(t, a1, a2, a3, a4, a5, ts, ts_1) for t in t_values]

        plt.subplot(2, 2, 1)
        plt.plot(t_values, space_values, label='Scenario {}'.format(i+1))
        plt.title('Space Curve')
        plt.xlabel('Time')
        plt.ylabel('Position')

        plt.subplot(2, 2, 2)
        plt.plot(t_values, velocity_values, label='Scenario {}'.format(i+1))
        plt.title('Velocity Curve')
        plt.xlabel('Time')
        plt.ylabel('Velocity')

    plt.tight_layout()
    plt.legend()
    plt.show()

def plot_single_trajectory(x_result, y_result):
    ''' plot a single trajectory given the x and y trajectory results.'''
    plt.figure(figsize=(12, 6))
    
    a0_x, a1_x, a2_x, a3_x, a4_x, a5_x, tf_x, ts_x, ts_1_x = x_result
    a0_y, a1_y, a2_y, a3_y, a4_y, a5_y, tf_y, ts_y, ts_1_y = y_result

    t_values = np.linspace(0, tf_x, 1000)
    x = [space_curve(t, a0_x, a1_x, a2_x, a3_x, a4_x, a5_x, ts_x, ts_1_x) for t in t_values]
    y = [space_curve(t, a0_y, a1_y, a2_y, a3_y, a4_y, a5_y, ts_y, ts_1_y) for t in t_values]
    vx = [velocity_curve(t, a1_x, a2_x, a3_x, a4_x, a5_x, ts_x, ts_1_x) for t in t_values]
    vy = [velocity_curve(t, a1_y, a2_y, a3_y, a4_y, a5_y, ts_y, ts_1_y) for t in t_values]

    plt.subplot(2, 2, 1)
    plt.plot(x, y)
    plt.title('Space Curve')
    plt.xlabel('x')
    plt.ylabel('y')

    plt.subplot(2, 2, 2)
    plt.plot(t_values, vx, label='vx')
    plt.plot(t_values, vy, label='vy')
    plt.title('Velocity Curve')
    plt.xlabel('vx')
    plt.ylabel('vy')

    plt.tight_layout()
    plt.legend()
    plt.show()

def plot_multiple_trajectories_and_velocities(results):
    '''plot all x-y trajectories and their corresponding velocity curves for each scenario in the results list.'''
    plt.figure(figsize=(12, 6))

    for i, element in enumerate(results): 
        x_result, y_result = element
        a0_x, a1_x, a2_x, a3_x, a4_x, a5_x, tf_x, ts_x, ts_1_x = x_result
        a0_y, a1_y, a2_y, a3_y, a4_y, a5_y, tf_y, ts_y, ts_1_y = y_result

        t_values = np.linspace(0, tf_x, 1000)
        x = [space_curve(t, a0_x, a1_x, a2_x, a3_x, a4_x, a5_x, ts_x, ts_1_x) for t in t_values]
        y = [space_curve(t, a0_y, a1_y, a2_y, a3_y, a4_y, a5_y, ts_y, ts_1_y) for t in t_values]
        vx = [velocity_curve(t, a1_x, a2_x, a3_x, a4_x, a5_x, ts_x, ts_1_x) for t in t_values]
        vy = [velocity_curve(t, a1_y, a2_y, a3_y, a4_y, a5_y, ts_y, ts_1_y) for t in t_values]

        plt.subplot(2, 2, 1)
        plt.plot(x, y, label='scenario {}'.format(i))
        plt.title('Space Curve')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()

        plt.subplot(2, 2, 2)
        plt.plot(t_values, vx, label='vx of scenario {}'.format(i))
        plt.plot(t_values, vy, label='vy of scenario {}'.format(i))
        plt.title('Velocity Curve')
        plt.xlabel('vx')
        plt.ylabel('vy')
        plt.legend()


    plt.tight_layout()
    plt.show()

def plot_multiple_trajectories(results, points):
    '''plot all x-y trajectories for each scenario in the results list, and the points to visit.'''
    plt.figure(figsize=(12, 6))

    for i, element in enumerate(results): 
        x_result, y_result = element
        a0_x, a1_x, a2_x, a3_x, a4_x, a5_x, tf_x, ts_x, ts_1_x = x_result
        a0_y, a1_y, a2_y, a3_y, a4_y, a5_y, tf_y, ts_y, ts_1_y = y_result

        t_values = np.linspace(0, tf_x, 1000)
        x = [space_curve(t, a0_x, a1_x, a2_x, a3_x, a4_x, a5_x, ts_x, ts_1_x) for t in t_values]
        y = [space_curve(t, a0_y, a1_y, a2_y, a3_y, a4_y, a5_y, ts_y, ts_1_y) for t in t_values]
        
        plt.subplot(2, 2, 1)
        plt.plot(x, y, label='scenario {}'.format(i), color='grey', linewidth=0.5)
        plt.title('Space Curve')
        plt.xlabel('x')
        plt.ylabel('y')
    plt.scatter([point[0] for point in points], [point[1] for point in points], color='red')
    plt.tight_layout()
    plt.show()

def plot_all_trajectories_and_shortest_path(results, points, dict_res, shortest):
    '''plot all x-y trajectories for each scenario in the results list, the points to visit and the shortest path.'''
    plt.figure(figsize=(12, 6))

    for i, element in enumerate(results): 
        x_result, y_result = element
        a0_x, a1_x, a2_x, a3_x, a4_x, a5_x, tf_x, ts_x, ts_1_x = x_result
        a0_y, a1_y, a2_y, a3_y, a4_y, a5_y, tf_y, ts_y, ts_1_y = y_result

        t_values = np.linspace(0, tf_x, 1000)
        x = [space_curve(t, a0_x, a1_x, a2_x, a3_x, a4_x, a5_x, ts_x, ts_1_x) for t in t_values]
        y = [space_curve(t, a0_y, a1_y, a2_y, a3_y, a4_y, a5_y, ts_y, ts_1_y) for t in t_values]
        
        plt.subplot(2, 2, 1)
        plt.plot(x, y, label='scenario {}'.format(i), color='grey', linewidth=0.5)
        plt.title('Space Curve')
        plt.xlabel('x')
        plt.ylabel('y')
    plt.scatter([point[0] for point in points], [point[1] for point in points], color='red')
    for i in range(len(shortest)-1):
        x_result, y_result = dict_res[shortest[i]][shortest[i+1]]
        a0_x, a1_x, a2_x, a3_x, a4_x, a5_x, tf_x, ts_x, ts_1_x = x_result
        a0_y, a1_y, a2_y, a3_y, a4_y, a5_y, tf_y, ts_y, ts_1_y = y_result

        t_values = np.linspace(0, tf_x, 1000)
        x = [space_curve(t, a0_x, a1_x, a2_x, a3_x, a4_x, a5_x, ts_x, ts_1_x) for t in t_values]
        y = [space_curve(t, a0_y, a1_y, a2_y, a3_y, a4_y, a5_y, ts_y, ts_1_y) for t in t_values]
        plt.subplot(2, 2, 1)
        plt.plot(x, y, label='scenario {}'.format(i), color='red', linewidth=0.7)
        plt.title('Space Curve')
        plt.xlabel('x')
        plt.ylabel('y')

    plt.tight_layout()
    plt.show()

def plot_velocities_in_cone(df, points):
    '''plot the initial velocities within the defined cone for each point in the points list.'''
    fig, ax = plt.subplots()
    print(df)
    # Define a colormap for different starting points
    colormap = plt.cm.get_cmap('viridis', len(df.keys()))
    for i, cone_velocities in df.items():
        x, y = points[i]
        print(cone_velocities)
        print()
        # Plot velocities as vectors with different colors
        vx = np.array([item[0] for item in cone_velocities])
        vy = np.array([item[1] for item in cone_velocities])
        ax.quiver([x] * len(cone_velocities), [y] * len(cone_velocities), vx, vy, color=colormap(i), scale=10)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Initial Velocities within Cone')
    plt.show()