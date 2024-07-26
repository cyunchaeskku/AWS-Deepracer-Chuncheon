import math

def reward_function(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    progress = params['progress']
    steps = params['steps']
    is_offtrack = params['is_offtrack']

    # Initialize reward
    reward = 1e-3  # Minimum reward

    # Check if all wheels are on track
    if not all_wheels_on_track or is_offtrack:
        return 1e-3  # Penalize if the car goes off track

    # Reward for staying close to the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    if distance_from_center <= marker_1:
        reward += 1.0
    elif distance_from_center <= marker_2:
        reward += 0.5
    elif distance_from_center <= marker_3:
        reward += 0.1
    else:
        return 1e-3  # Penalize if too far from center

    # Calculate the direction of the center line based on the closest waypoints
    next_waypoint = waypoints[closest_waypoints[1]]
    prev_waypoint = waypoints[closest_waypoints[0]]

    track_direction = math.atan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0])
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize if the direction difference is too large
    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5

    # Reward for speed, encouraging faster speeds on straight sections and slower on corners
    straight_line_speed = 3.0  # desired speed on straight lines
    corner_speed = 1.0         # desired speed on corners

    if direction_diff < 10:  # Straight line
        if speed >= straight_line_speed:
            reward += 1.0
        else:
            reward += speed / straight_line_speed  # proportionate reward
    else:  # Corner
        if speed <= corner_speed:
            reward += 1.0
        else:
            reward += corner_speed / speed  # penalize for going too fast in corners

    # Reward for progress
    if (steps % 100) == 0 and progress > (steps / 100):
        reward += 10.0

    return float(reward)
