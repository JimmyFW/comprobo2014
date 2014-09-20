## Computational Robotics 2014 ##

I implemented the wall follower and person follower.

Wall Follower Strategy
=====

I implemented the wall follower with the following strategy:

1. Detect the nearest wall and move towards it
2. Turn until the robot is perpendicular to the wall
3. Move the robot normal to the wall until it is at the specified target distance
4. Turn to the left until the robot is parallel to the wall
5. Move forward

Wall Follower Code Structure
=====

These behaviors were codified into various states of a finite state machine.

As implemented, the robot starts out in state #4. In this state, the robot rotates until its forward sensor detects that there is an object somewhere in front of it.

If the robot is not perpendicular to the wall, then the FSM transitions to state #5, which sets the robot perpendicular to the wall using proportional control.

Either way, once the robot is perpendicular, the robot then goes into a loop between states 0 and 1, in which it adjusts itself so that the target distance is set with proportional control.

After this, the robot enters state 2, in which it turns parallel to the wall (again using proportional control).

Finally the robot enters state 3, where it moves forward parallel to the wall.

These behaviors were implemented using 6 states in total.

Person Follower Strategy
=====

I implemented the person follower with the following strategy:

1. Scan 45 degrees left of zero, and 45 degrees to the right
2. Append all of the angles with nonzero distance to a list
3. From this list, obtain the average angle. Keep track of the previously computer average angle.
4. From the average angle, obtain the average distance
5. Use the angle and distance computed to position the robot with proportional control. The distance has a target value of 1 meter following, and the angle is adjusted to point the neato towards the person

Person Follower Code Structure
=====

The person follower was structed as one of the states of the finite state machine. No other states transition into this one, and you cannot transition out of the person following state. The whole point is so you can set which mode you want the neato to be in when you run the node: state 4 for the wall follower, and state 6 for the person follower.

Challenges
=====

I didn't have enough time to implement more complex behaviors. I wanted the robot in wall follower mode to proportionally maintain a target distance from the wall as it is traveling parallel, so that it could follow curved walls. I also wanted it to round corners. The person follower uses a naive strategy and it would have been nice to implement a clustering algorithm to identify clusters and keep track of their relative movement at every time step, instructing the neato to follow a particular cluster.

Future projects
=====

I am generally very excited at the prospect of using machine learning to make the robot controllers more sophisticated.