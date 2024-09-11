from flask_restx import Model, fields, Namespace


class BaseResponseModelRetriever:
    def __init__(self, namespace):
        self.namespace = namespace

    def register_model_to_namespace(self, name, model_definition):
        """
        Register a model with the provided definition under the given name.
        """
        print(f"Registering response model {name} with fields: {model_definition}")
        return self.namespace.model(name, model_definition)

    def add_message_field(self, model_definition: tuple):
        """
        Enhances a given model definition by adding a 'message' field for response purposes.

        Args:
            model_definition (tuple): A tuple containing the model name and fields dictionary.

        Returns:
            tuple: A new model definition dynamically extended with a 'message' field.
        """
        model_name, fields_dict = model_definition
        enhanced_fields_dict = {**fields_dict}
        enhanced_fields_dict["message"] = fields.String(
            description="Optional response message",
            required=False,
            example="Action completed successfully",
        )
        return self.register_model_to_namespace(model_name, enhanced_fields_dict)
