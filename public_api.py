class Condition():
    """Implements a condition to be checked.
    When the condition is active, `on_tick` will be called periodically.
    Use the `on_tick` to evaluate if the condition was met and set
    `self.condition_met` accordingly.
    """

    condition_met = False

    def on_tick(self):
        pass

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass


class Behavior():
    """Implements a behavior to be conditionally activated.
    When the behavior is active, `on_tick` will be called periodically.

    Use `get_from_connection` to retrieve connected data by name.
    """

    def on_tick(self):
        pass

    def on_activated(self):
        pass

    def on_deactivated(self):
        pass
    
    def get_from_connection(self, name):
        pass


def check(condition, condition_property_name='condition_met'):
    """Check if a condition is met

    Returns true if the condition is met.
    If the condition is not active, it will be automatically activated.
    Conditions that are not checked in a tick will be automatically deactivated.

    `condition_property_name` can be used to check different conditions other then 
    the default one.
    """
    pass


def activate(object):
    """Activates a behavior or a condition

    When an object is active, `on_tick` will be called periodically.
    Methods `on_activated` and `on_deactivated` are called accordingly, respectively
    before the first tick and after the last tick of the activation.
    """
    pass


def register(object_name, object_type):
    """Register an Condition or Behavior so that it can be used by the behavior engine.
    """
    return object_name


def connect(object_from, from_method_name, object_to, to_method_name):
    """Connects data from one object to another
    """
    pass