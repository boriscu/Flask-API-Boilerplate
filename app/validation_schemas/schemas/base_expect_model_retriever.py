class BaseExpectModelRetriever:
    def __init__(self, namespace):
        self.namespace = namespace

    def register_model_to_namespace(self, model: tuple):
        """
        Register a model with the provided definition under the given name.
        """
        name, model_definition = model
        print(f"Registering expect model {name} with fields: {model_definition}")

        return self.namespace.model(name, model_definition)
