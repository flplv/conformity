class Registry:
    instances : dict = dict()
    declarations : dict = dict()
    visited : set = set()

    def add(self, name, klass):
        if name not in self.declarations.keys():
            self.declarations[name] = klass

    def get_instance(self, name):
        self.visit(name)
        if name in self.instances:
            return self.instances[name]
        return self.create(name)

    def create(self, name):
        if name not in self.declarations.keys():
            raise Exception("Unable to crate instance of {}, it was not registered.".format(name))
        klass = self.declarations[name]
        obj = klass(name)
        self.instances[name] = obj
        return obj

    def delete(self, name):
        if name in self.instances.keys():
            del self.instances[name]

    def visit(self, name):
        self.visited.add(name)

    def move_unvisited_instances_and_clear_visits(self):
        """Remove marked instances from the `self.instances` and return them.
        Moved instances will actually be deleted if `moves` is not saved elsewhere.
        """
        moves = {name: i for name,i in self.instances.items() if name not in self.visited}
        for name in moves.keys():
            del self.instances[name]
        self.visited.clear()
        return moves


class BdfCallbacks:
    registry : Registry

    def __init__(self, registry):
        self.registry = registry

    def check(self, name, property_name="condition_met"):
        obj = self.registry.get_instance(name)
        obj.activate()
        print("checking " + name + ": " + str(obj.is_true(property_name)))  # debug
        return obj.is_true(property_name)

    def activate(self, name):
        obj = self.registry.get_instance(name)
        obj.activate()
        print("activating " + name)  # debug

    def register(self, name, object_type):
        self.registry.add(name, object_type)
        return name

    def prepare(self, name):
        obj = self.registry.get_instance(name)
        obj.prepare()

    def is_prepared(self, name):
        obj = self.registry.get_instance(name)
        return obj.is_prepared()

    def connect(self, object_from, from_method_name, object_to, to_method_name):
        pass


class Engine:

    bdf = None
    registry : Registry = Registry()

    def __init__(self, behavior_description_function):
        self.bdf = behavior_description_function
    
    def tick(self):
        # Tick instances
        for _, obj in self.registry.instances.items():
            obj.tick()

        # Eval the user function
        self.bdf(BdfCallbacks(self.registry))

        # Delete not visited instances
        deletions = self.registry.move_unvisited_instances_and_clear_visits()
        for _, obj in deletions.items():
            obj.tear_down()
        del deletions


