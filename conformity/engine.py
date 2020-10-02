class Registry:

    def __init__(self):
        self.instances = dict()
        self.declarations = dict()
        self.visited = set()

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

    def __init__(self, registry: Registry):
        self.registry = registry

    def check(self, name, property_name):
        obj = self.registry.get_instance(name)
        obj.activate()
        return obj.is_true(property_name)

    def activate(self, name):
        obj = self.registry.get_instance(name)
        obj.activate()

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

    def __init__(self, behavior_description_function):
        self.registry = Registry()
        self.bdf = behavior_description_function
        self.introspection_function = None
    
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

        if (self.introspection_function):
            self.introspection_function(self._prepare_introspection(self.registry))

    def set_registry_introspection(self, introspection_function):
        """ Set a function to receive the behavior introspection data.
        With the signature `callback(behavior_introspection_data) -> None`.
        `behavior_introspection_data` is a `map[string] = string` where the key represents
        the behavior name and the value is behavior's state.
        """
        self.introspection_function = introspection_function

    @staticmethod
    def _prepare_introspection(registry):
        result = {} # Result is a map of behavior names containing a string describing
                    # the behavior state
        result = {name: "deleted" for name in registry.declarations.keys()}
        for name, instance in registry.instances.items():
            result[name] = instance.state.name.lower()
        return result
