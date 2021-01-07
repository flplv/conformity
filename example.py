from conformity.public_api import *
from conformity.engine import *
import time
import gorobot

class ABallInSight(Condition):
    def on_tick(self):
        #todo search vision subsystem or world model for a ball
        self.condition_met = gorobot.check_sensor("objectinsight")
        self.balls = gorobot.get_all_balls();
        self.robot_location = gorobot.get_robot_location();

    def closest_ball(self):
        return find_closest(self.balls, self.robot_location);
    
    @stasticmethod
    def find_closest(balls, location):
        pass
                     
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
        gorobot.send_control("gotoobjectposition", self.ball_coords)
    
    def on_activation(self, ball_coords):
        self.ball_coords = ball_coords

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

    if not api.check(ball_grasped, "condition_met"):

        if api.check(a_ball_in_sight, "condition_met"):
            api.activate(pursue_ball, api.get(a_ball_in_sight, "closest_ball"))

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

