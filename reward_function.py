def reward_function(params):

    import math

    on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle for calculations
    speed = params['speed']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints'] 
    heading = params['heading']
    all_wheels_on_track = params['all_wheels_on_track']

    reward = math.exp(-6 * distance_from_center)

    def on_track_reward(current_reward, on_track):
        if not on_track:
            current_reward = 1e-3
        else:
            current_reward = 1e2
        return current_reward
    
    def distance_from_center_reward(current_reward, track_width, distance_from_center):
    
        # Calculate 3 markers that are at varying distances away from the center line
        marker_1 = 0.1 * track_width
        marker_2 = 0.25 * track_width
        marker_3 = 0.5 * track_width
        
        # Give higher reward if the car is closer to center line and vice versa
        if distance_from_center <= marker_1:
            current_reward *= 1.2
        elif distance_from_center <= marker_2:
            current_reward *= 0.8
        elif distance_from_center <= marker_3:
            current_reward *= 0.5
        else:
            current_reward = 1e-3  # likely crashed/ close to off track
        
        return float(current_reward)

    def throttle_reward(current_reward, speed, steering):
        if speed > 2.5 - (0.4 * abs(steering)):
            current_reward *= 0.8
        return current_reward

    def steering_reward(current_reward, steering):
        if abs(steering) > 25:
            current_reward *= 0.8
        return current_reward

    def straight_line_reward(current_reward, steering, speed):
        # Positive reward if the car is in a straight line going fast
        if abs(steering) < 0.1 and speed > 3:
            current_reward *= 1.2
        return current_reward
    
    def speed_reward(current_reward, speed):
        if speed>2:
            current_reward *= 1.1
        return current_reward

    def stay_inside_border_reward(current_reward, all_wheels_on_track, distance_from_center, track_width):
        
        # Give a very low reward by default
        reward = 1e-3

        # Give a high reward if no wheels go off the track and 
        # the car is somewhere in between the track borders 
        if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
            reward = 1.0

        # Always return a float value
        return reward
        

    reward = on_track_reward(reward, on_track)
    reward = distance_from_center_reward(reward, track_width, distance_from_center)
    reward = throttle_reward(reward, speed, steering)
    reward = steering_reward(reward, steering)
    reward = straight_line_reward(reward, steering, speed)
    reward = speed_reward(reward, speed)

    return float(reward)