from public_api import *
from engine import *
import time
import gorobot

class ABallInSight(Condition):
    def on_tick(self):
        #todo search vision subsystem or world model for a ball
        self.condition_met = gorobot.check_sensor("objectinsight")

    def get_ball(self):
        return None

class ABallInFork(Condition):
    def on_tick(self):
        #todo check fork camera for a ball
        self.condition_met = gorobot.check_sensor("objectinrange")

class BallGraspped(Condition):
    def on_tick(self):
        #todo check sensors if grasp was detected and set self.condition_met
        self.condition_met = gorobot.check_sensor("objectgrasped")

class InBasketLocation(Condition):
    def on_tick(self):
        #todo check sensors to verify that the robot is in the basket location
        self.condition_met = gorobot.check_sensor("robotindropzone")

class PursueBall(Behavior):
    def on_tick(self):
        #todo send goals to the navigation subsystem
        gorobot.send_control("gotoobjectposition")
    
    def set_ball(self, ball):
        self.ball = ball

class GraspAction(Behavior):
    def on_tick(self):
        gorobot.send_control("graspobject")
    
    def on_activation(self):
        #todo send close fork commands to fork subsystem
        pass
    
    def on_deactivation(self):
        #todo send open fork commands to fork subsystem
        pass
    
    def on_preparation_tick(self):
        #todo send open fork commands to fork subsystem
        # return true if fork is open
        return True

class GoToBasketLocation(Behavior):
    def on_tick(self):
        gorobot.send_control("gotodropzone")
        #todo send basket goal to the navigation subsystem

class DropBall(Behavior):
    def on_tick(self):
        gorobot.send_control("dropobject")
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
    while(1):
        my_engine.tick()
        time.sleep(0.1)


if __name__ == '__main__':
    Start()

