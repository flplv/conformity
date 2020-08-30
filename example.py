from public_api import *


class ABallInSight(Condition):
    def on_tick(self):
        #todo search vision subsystem or world model for a ball
        self.condition_met = False

    def get_ball(self):
        return None


class ABallInFork(Condition):
    def on_tick(self):
        #todo check fork camera for a ball
        self.condition_met = False


class PursueBall(Behavior):
    def on_tick(self):
        #todo send goals to the navigation subsystem
        pass

    def set_ball(self, ball):
        self.ball = ball

class GraspAction(Behavior):
    def on_enable(self):
        #todo send close fork commands to fork subsystem
        pass
    def on_disable(self):
        #todo send open fork commands to fork subsystem
        pass

class BallGraspped(Condition):
    def on_tick(self):
        #todo check sensors if grasp was detected and set self.condition_met
        pass


class InBasketLocation(Condition):
    def on_tick(self):
        #todo check sensors to verify that the robot is in the basket location
        pass


class GoToBasketLocation(Behavior):
    def on_tick(self):
        #todo send basket goal to the navigation subsystem
        pass


def my_example_application():

    a_ball_in_sight = register('a_ball_in_sight', ABallInSight)
    pursue_ball = register('pursue_ball', PursueBall)
    a_ball_in_fork = register('a_ball_in_fork', ABallInFork)
    ball_grasped = register('ball_grasped', BallGraspped)
    grasp_action = register('grasp_action', GraspAction)

    in_basket_location = register('in_basket_location', InBasketLocation)
    go_to_basket_location = register('go_to_basket_location', GoToBasketLocation)
    drop_ball = register('drop_ball', DropBall())

    connect(a_ball_in_sight, 'get_ball', pursue_ball, 'set_ball')

    if not check(ball_grasped):

        if check(a_ball_in_sight):
            activate(pursue_ball)

        if check(a_ball_in_fork):
            activate(grasp_action)

    else:
        if check(in_basket_location):
            activate(drop_ball)
        else:
            activate(go_to_basket_location)

if __name__ == '__main__':
    pass


