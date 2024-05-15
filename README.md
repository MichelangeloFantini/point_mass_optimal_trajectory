# Point Mass Trajectory Plotting

## Repository Inspiration
This repository contains a Python implementation of time-optimal trajectory generation for a 2D double integrator point mass, as described in [1]. This approach leverages Pontryagin's maximum principle, which states that, given the motion model p_prime_prime = u, the time-optimal control results in a bang-bang policy. An extension is made when velocity constraints are added, generating time-optimal trajectories between waypoints. Note that trajectories are computed between two consecutive waypoints. The final overall shortest trajectory spanning across all waypoints is computed using Dijkstra's algorithm.

The optimization problem described above has a closed-form solution only if starting and ending velocities are provided. The first step is therefore to sample different velocities lying in the cone centered on the centerline connecting two consecutive waypoints. After the velocities are sampled, the trajectory between each waypoint is calculated using positions and velocities as initial conditions. As the integrator moves in a 2D world, after both the x and y trajectories are generated, a scaling factor alpha in the interval (0, 1] is generated to slow down the faster axis. Alpha reduces the bounds of the control input.

## Repository Usage
The main functions that perform the velocity sampling function (compute_velocities_in_cone) and optimization solver function (compute_all_trajectories) are found in the main.py file.

The compute_velocities_in_cone function allows the user to specify the vertex angle, how many angles to sample in such an angle, the minimum and maximum velocity magnitudes, and how many magnitudes to sample in the range. All combinations of angles and parameters will be computed. The function is also equipped with a boolean parameter named loop and a prediction horizon. The latter parameter allows the user to specify how many waypoints (after the first one) the velocities should be generated for. The boolean parameter determines the cone centerline direction of the last waypoint. If loop is true, the centerline will point toward the first waypoint. If loop is false, the sampled velocities at the last waypoint will be centered on the centerline used for the previous waypoint.

The compute_all_trajectories function takes the velocities generated and solves the optimization problem. Similarly to the function above, compute_all_trajectories takes an integer so the trajectory is only planned up to the nth waypoint (after the first waypoint).

## Additional Tools
The repository also offers additional tools for debugging, analysis, and plot. Some of the trajectory_computations functions support setting flags manually for additional information.

Finally, in the example_script, some of the main functions used in the code can be tested with different initial conditions, and the user can get accustomed to the main optimization functions used.

## References
[1] Foehn, Philipp, et al. "Alphapilot: Autonomous drone racing." Autonomous Robots 46.1 (2022): 307-320.