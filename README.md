# Behavior Planning by Finite State Machine 
 In this section I am going to teach an approach to behavior planning that uses something called a Finite State Machine to solve the behavior planning problem. 
 
## 1.	Introduction
If you think about the over all flow of data in a self-driving car operating on the fastest time scales you have: 

1.	First [Motion](https://github.com/A2Amir/Motion-Model-of-a-Car) Control
2.	Than  you have [Sensor Fusion](https://github.com/A2Amir/Extended-Kalman-Filter-for-Sensor-Fusion-Radar-and-Lidar).
3.	Just lower than you have [localization](https://github.com/A2Amir/Implement-a-particle-filter-in-the-context-of-Cplus) and trajectory planning.
4.	Next is [Prediction](https://github.com/A2Amir/Prediction-Phase-in-the-trajectory-generation-of-cars) which you just learned about.
5.	And then at the top is behavior planning with the lowest update rate.

<p align="right"> <img src="./img/1.png" style="right;" alt=" the fastest time scales" width="600" height="400"> </p> 

The inputs to behavior planning come from the prediction module and the localization module and both of which get their inputs from the sensor fusion.

The output from the behavior module goes directly to the trajectory planner, which also takes input from prediction and localization so that it can send trajectories to the motion controll.

Everything inside of the green box in the imag above is the focus of this repository and is commonly referred to as Path Planning.

We will start by doing a brief introduction where you'll learn more about the details of the inputs and outputs to behavior planner and understand what problems a behavior planning module is expected to solve.Next, we will talk about Finite State Machines as one technique for implementing a behavior plan, followed by a more in-depth look at the Cost Functions we will use to actually make behavioral level decisions.


## 2.	Understanding Output
It's possible to suggest a wide variety of behaviors by specifying only a few quantities. For example by specifying only a target lane, a target vehicle (to follow), a target speed, and a time to reach these targets, we can make suggestions as nuanced as "stay in your lane but get behind that vehicle in the right lane so that you can pass it when the gap gets big enough."
Look at the picture below and 5 potential json representations of output and see the json representation match with the corresponding verbal description.
<p align="right"> <img src="./img/2.png" style="right;" alt=" the fastest time scales" width="600" height="400"> </p> 


<p align="center"> <img src="./img/3.png" style="center;" alt="potential json representations of output" > </p> 
To see 3 potential json representations of output ckick  <a href="https://github.com/A2Amir/Behavior-Planning-by-Finite-State-Machine/blob/master/img/4.png" rel="Here">Here</a>



## 3.	The Behavior Problem
The behavior planner is currently a black box, which takes as input a map of the world,a route to the destinations,and predictions about what other static and dynamic obstacles are likely to do and it produces as output a adjusted maneuver for the vehicle which the trajectory planner is responsible for reaching collision-free, smooth, and safe.The goal of this repository is to open up this black box and learn how to implement a behavior planner.

<p align="right"> <img src="./img/5.png" style="right;" alt=" The Behavior Problem" width="600" height="400"> </p> 

 
The responsibilities of the behavior module are to suggest maneuvers which are feasible, as safe as possible, legal, and efficient. What the behavior planner is not responsible for are execution details and collision avoidance.

The approach to behavior planning we are going to teach in is the same one used by most of the vehicles, including the winning one in the DARPA Urban Challenge. In fact, it's the approach to behavior planning that Mercedes used in their Bertha Benz Drive,which you can see is capable of handling complex traffic situations like navigating intersections and dense urban traffic.

