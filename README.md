## Computational Robotics 2014 ##

Wall Follower
=====
I implemented the wall follower with the following strategy:

1. Move forward until a wall is encountered, approaching the wall with proportional control towards a specified target value
2. Turn to the left until the robot is parallel to the wall
3. Move forward with proportional control, keeping the target value constant

