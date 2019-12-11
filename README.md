# Behavior Planning by Finite State Machine 
 In this section I am going to teach an approach to behavior planning that uses something called a Finite State Machine to solve the behavior planning problem. 
 
## 1.	Introduction
If you think about the over all flow of data in a self-driving car operating on the fastest time scales you have: 

1.	First [Motion](https://github.com/A2Amir/Motion-Model-of-a-Car) Control
2.	Than  you have [Sensor Fusion](https://github.com/A2Amir/Extended-Kalman-Filter-for-Sensor-Fusion-Radar-and-Lidar).
3.	Just lower than you have [localization](https://github.com/A2Amir/Implement-a-particle-filter-in-the-context-of-Cplus) and trajectory planning.
4.	Next is [Prediction](https://github.com/A2Amir/Prediction-Phase-in-the-trajectory-generation-of-cars) which you just learned about.
5.	And then at the top is behavior planning with the lowest update rate.

<p align="right"> <img src="./img/1.png" style="right;" alt=" Pseudocode" width="600" height="400"> </p> 

The inputs to behavior planning come from the prediction module and the localization module and both of which get their inputs from the sensor fusion.

The output from the behavior module goes directly to the trajectory planner, which also takes input from prediction and localization so that it can send trajectories to the motion controll.

Everything inside of the green box in the imag above is the focus of this repository and is commonly referred to as Path Planning.

We will start by doing a brief introduction where you'll learn more about the details of the inputs and outputs to behavior planner and understand what problems a behavior planning module is expected to solve.Next, we will talk about Finite State Machines as one technique for implementing a behavior plan, followed by a more in-depth look at the Cost Functions we will use to actually make behavioral level decisions.
