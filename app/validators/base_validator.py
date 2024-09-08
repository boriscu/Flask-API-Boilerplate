class BaseValidator:
    @classmethod
    def validate_data(cls, data: dict, validation_map: dict) -> tuple[bool, str]:
        """
        Run validation on data based on validation_map
        """
        is_valid, out_message = cls.validate_required(data, validation_map)

        if not is_valid:
            return False, out_message

        is_valid, out_message = cls.validate_type(data, validation_map)

        return is_valid, out_message

    @classmethod
    def validate_required(cls, data: dict, validation_map: dict) -> tuple[bool, str]:
        """
        Check if data has required fields based on validation_map
        """
        missing_keys = []

        for key, specs in validation_map.items():
            if data.get(key) is None and specs.get("required") == True:
                missing_keys.append(key)

        if len(missing_keys) == 0:
            is_valid = True
            out_message = "Validation passed."
        else:
            is_valid = False
            out_message = "Missing required data: "

            for i in range(len(missing_keys) - 1):
                out_message += missing_keys[i] + ", "
            out_message += missing_keys[len(missing_keys) - 1] + "."

        return is_valid, out_message

    @classmethod
    def validate_type(cls, data: dict, validation_map: dict) -> tuple[bool, str]:
        """
        Check field types in data based on validation_map
        """
        out_message = ""

        for key, value in data.items():
            if validation_map.get(key) is None:
                continue
            expected_type = validation_map[key]["type"]
            if hasattr(expected_type, "__origin__"):
                expected_type = expected_type.__origin__

            if not isinstance(value, expected_type):
                out_message += f"Invalid type for key {key}: Expected type {expected_type.__name__}, got {type(value).__name__}. "

        if out_message == "":
            is_valid = True
            out_message = "Validation passed."
        else:
            is_valid = False

        return is_valid, out_message
