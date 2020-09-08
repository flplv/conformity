from public_api import *
from engine import *
import time
import sys
import gorobot

sensor_ball_in_sight = gorobot.MockSensor(period=2)
sensor_ball_in_fork = gorobot.MockSensor(period=4)
sensor_ball_grasped = gorobot.MockSensor(period=8)
sensor_ball_in_basket = gorobot.MockSensor(period=16)

class ABallInSight(Condition):
    def on_tick(self):
        #todo search vision subsystem or world model for a ball
        self.condition_met = sensor_ball_in_sight.get_data_bool(start_true=False)
        print(self.name + " condition: " + str(self.condition_met))
    def get_ball(self):
        return None

class ABallInFork(Condition):
    def on_tick(self):
        #todo check fork camera for a ball
        self.condition_met = sensor_ball_in_fork.get_data_bool(start_true=False)
        print(self.name + " condition: " + str(self.condition_met))

class BallGraspped(Condition):
    def on_tick(self):
        #todo check sensors if grasp was detected and set self.condition_met
        self.condition_met = sensor_ball_grasped.get_data_bool(start_true=False)
        print(self.name + " condition: " + str(self.condition_met))

class InBasketLocation(Condition):
    def on_tick(self):
        #todo check sensors to verify that the robot is in the basket location
        self.condition_met = sensor_ball_in_basket.get_data_bool(start_true=False)
        print(self.name + " condition: " + str(self.condition_met))

class PursueBall(Behavior):
    def on_tick(self):
        #todo send goals to the navigation subsystem
        print(self.name + " tick")
    
    def set_ball(self, ball):
        self.ball = ball

class GraspAction(Behavior):
    def on_tick(self):
        print(self.name + " tick")
    
    def on_activation(self):
        #todo send close fork commands to fork subsystem
        pass
    
    def on_deactivation(self):
        #todo send open fork commands to fork subsystem
        pass
    
    def on_preparation_tick(self):
        #todo send open fork commands to fork subsystem
        # return true if fork is open
        print("preparing " + self.name)
        return True

class GoToBasketLocation(Behavior):
    def on_tick(self):
        print(self.name + " tick")
        #todo send basket goal to the navigation subsystem

class DropBall(Behavior):
    def on_tick(self):
        print(self.name + " tick")
        #todo send basket goal to the navigation subsystem
    
    def on_activation(self):
        #todo send open fork commands to fork subsystem
        pass
    
    def on_deactivation(self):
        #todo send open fork commands to fork subsystem
        pass


def my_example_application(api : BdfCallbacks):
    
    a_ball_in_sight = api.register('a_ball_in_sight', ABallInSight)
    pursue_ball = api.register('pursue_ball', PursueBall)
    a_ball_in_fork = api.register('a_ball_in_fork', ABallInFork)
    ball_grasped = api.register('ball_grasped', BallGraspped)
    grasp_action = api.register('grasp_action', GraspAction)

    in_basket_location = api.register('in_basket_location', InBasketLocation)
    go_to_basket_location = api.register('go_to_basket_location', GoToBasketLocation)
    drop_ball = api.register('drop_ball', DropBall)

    api.connect(a_ball_in_sight, 'get_ball', pursue_ball, 'set_ball')

    if not api.check(ball_grasped, "condition_met"):

        if api.check(a_ball_in_sight, "condition_met"):
            api.activate(pursue_ball)

        api.prepare(grasp_action) 

        if api.check(a_ball_in_fork, "condition_met") and api.is_prepared(grasp_action):
            api.activate(grasp_action)

    else:
        if api.check(in_basket_location, "condition_met"):
            api.activate(drop_ball)
        else:
            api.activate(go_to_basket_location)


def Start():
    my_engine = Engine(my_example_application)
    time_start = time.time()
    while(1):
        time_elapsed = time.time() - time_start
        print("time: " + str(time_elapsed))
        my_engine.tick()
        # sensor_data = gorobot.request_sensor("1")
        # gorobot.tick_simulation()
        time.sleep(0.5)
        print("----")


if __name__ == '__main__':
    Start()

