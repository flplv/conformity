This is a project under experimentation. 

We are experimenting with a novel approach to behavior description, our goal is to describe complex robotic behaviour with the simplet logic as possible. 

The core model is "when a given state is true, enable a other given behavior" and then simply use ifs and elses as needed to build complex behavior.

This code...

 
```python
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
```

... yields this robotic behavior: https://github.com/flplv/conformity/blob/master/conformity-demo.mp4
