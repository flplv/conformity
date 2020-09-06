from enum import Enum

class ObjectState(Enum):
    DEACTIVE = 0
    PREPARING = 1
    PREPARED = 2
    ACTIVE = 3

class Object(object):

    def __init__(self, name):
        self.name = name
        self.state = ObjectState.DEACTIVE
        self.on_setup()

    def activate(self):
        if self.state == ObjectState.PREPARING:
            #todo log: "State error, trying to activate an object that is still preparing: object {}".format(self.name)
            return

        if self.state == ObjectState.ACTIVE:
            # already active, ignore.
            return

        self.state = ObjectState.ACTIVE
        self.on_activation()
        return self

    def deactivate(self):
        if self.state != ObjectState.ACTIVE:
            # nothing to deactivate, ignore.
            return

        self.state = ObjectState.DEACTIVE
        self.on_deactivation()
        return self

    def prepare(self):
        if self.state == ObjectState.PREPARING \
            or self.state == ObjectState.PREPARED \
            or self.state == ObjectState.ACTIVE:
            # already preapring or prepared or were prepared before, ignore.
            return

        self.state = ObjectState.PREPARING
        self.on_preparation()
        return self

    def cancel_prepare(self):
        if self.state != ObjectState.PREPARING:
            # nothing to cancel
            return

        self.state = ObjectState.DEACTIVE
        self.on_preparation_cancel()
        return self

    def is_prepared(self):
        return self.state == ObjectState.PREPARED or self.state == ObjectState.ACTIVE

    def is_true(self, attr_name):
        if not hasattr(self, attr_name):
            return False
        return bool(getattr(self, attr_name))

    def tick(self):
        if self.state == ObjectState.ACTIVE:
            self.on_tick()
        elif self.state == ObjectState.PREPARING:
            if self.on_preparation_tick() == True:
                self.state = ObjectState.PREPARED
    
    def tear_down(self):
        self.deactivate()
        self.cancel_prepare()
        self.state = ObjectState.DEACTIVE
        self.on_teardown()


    def on_tick(self):
        pass

    def on_preparation_tick(self):
        pass
    
    def on_preparation(self):
        pass

    def on_preparation_cancel(self):
        pass
    
    def on_activation(self):
        pass
    
    def on_deactivation(self):
        pass

    def on_teardown(self):
        pass

    def on_setup(self):
        pass