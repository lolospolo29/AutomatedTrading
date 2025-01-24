import dataclasses
import typing
from dataclasses import is_dataclass, fields
from typing import Type

from app.mappers.exceptions.MappingFailedExceptionError import MappingFailedExceptionError
from app.monitoring.logging.logging_startup import logger


class ClassMapper:
    """Maps different kinds of classes to different kinds of objects."""
    def map_dict_to_dataclass(self, data: dict, cls: Type[dataclasses.dataclass]) -> dataclasses.dataclass:
        """Helper function to convert a dictionary into a dataclass object."""
        try:
                logger.debug(f"Mapping {cls.__name__} to dataclass {data}")
                # print(f"Converting data into {cls.__name__}...")  # Debugging
                # Collect all field names for the dataclass
                fieldnames = {f.name for f in dataclasses.fields(cls)}
                init_kwargs = {k: v for k, v in data.items() if k in fieldnames}

                # Get the types of the fields
                field_types = {f.name: f.type for f in dataclasses.fields(cls)}

                logger.debug("Initializing class mapper with fieldnames: %s", fieldnames)

                # Recursively handle nested dataclasses
                for key, value in init_kwargs.items():
                    # print(f"Processing field: {key} -> {value}")  # Debugging
                    logger.debug(f"{key}={value}")

                    if isinstance(value, dict) and hasattr(cls, key) and hasattr(getattr(cls, key), '__annotations__'):
                        # Recursively convert nested dataclass
                        init_kwargs[key] = self.map_dict_to_dataclass(value, getattr(cls, key))
                    elif isinstance(value, list) and hasattr(cls, key):
                        # Handle List of dataclasses (and other types)
                        field_type = getattr(cls, key)
                        origin = typing.get_origin(field_type)  # Get the origin of the field type
                        if origin is list:  # If it's a List, handle it properly
                            item_type = typing.get_args(field_type)[0]  # Get the item type of the List
                            # Convert each item in the list to the corresponding dataclass
                            init_kwargs[key] = [
                                self.map_dict_to_dataclass(item, item_type) if isinstance(item, dict) else item
                                for item in value
                            ]
                        elif isinstance(field_type, type(typing.Union)):  # Handle Optional (Union[Type, None])
                            # If the type is Optional, unwrap it to get the real type (the first part of the Union)
                            if value is not None:
                                item_type = typing.get_args(field_type)[0]
                                init_kwargs[key] = self.map_dict_to_dataclass(value, item_type) if isinstance(value, dict) else value
                            else:
                                init_kwargs[key] = value

                return cls(**init_kwargs)
        except Exception as e:
            raise MappingFailedExceptionError(type(data).__name__)

    @staticmethod
    def map_args_to_dataclass(cls, input_obj=None, obj_type=None, **kwargs):
        """
        Maps the provided arguments or another class instance to a dataclass.
        If input_obj is provided, its fields are used as defaults, and kwargs override them.
        """
        try:
            logger.debug(f"Mapping {cls.__name__} to dataclass {input_obj}")
            # Get all field names of the target dataclass
            cls_fields = {field.name: field for field in fields(cls)}

            # Prepare values for the new dataclass instance
            field_values = {}

            if input_obj and isinstance(input_obj, obj_type):
                # Map from input object attributes if it's an instance of the dataclass
                for key, field in cls_fields.items():
                    field_values[key] = getattr(input_obj, key, None)

            # Override with any explicitly provided kwargs
            for key, value in kwargs.items():
                if key in cls_fields:
                    field_values[key] = value

            # Create and return the new dataclass instance
            return cls(**field_values)
        except Exception as e:
            raise MappingFailedExceptionError(type(input_obj).__name__)
    @staticmethod
    def map_dataclass_to_class(dataclass_instance, target_cls):
        """
        Maps the fields of a dataclass instance to a regular class instance.

        Args:
            dataclass_instance: An instance of a dataclass.
            target_cls: The target class to map to.

        Returns:
            An instance of the target class with attributes populated from the dataclass instance.
        """
        try:
            logger.debug(f"Mapping {target_cls.__name__} to class {dataclass_instance}")
            if not is_dataclass(dataclass_instance):
                raise ValueError("The provided instance is not a dataclass.")

            # Create an instance of the target class
            target_instance = target_cls()

            # Populate attributes from the dataclass fields
            for field in fields(dataclass_instance):
                setattr(target_instance, field.name, getattr(dataclass_instance, field.name))

            return target_instance
        except Exception as e:
            raise MappingFailedExceptionError(type(dataclass_instance).__name__)
    @staticmethod
    def update_class_with_dataclass(data_class_instance, target_instance):
        """
        Updates the attributes of a regular class instance with values from a dataclass instance.

        Args:
            data_class_instance: An instance of a dataclass.
            target_instance: An instance of a regular class.

        Returns:
            The updated target_instance.
        """
        try:
            logger.debug(f"Updating class attributes from class {data_class_instance} to class {target_instance}")
            # Iterate over the fields of the dataclass and set them on the target instance only if not None
            for field in fields(data_class_instance):
                value = getattr(data_class_instance, field.name)
                if value is not None:  # Check if the field is not None
                    setattr(target_instance, field.name, value)

            return target_instance
        except Exception as e:
            raise MappingFailedExceptionError(type(data_class_instance).__name__)

    @staticmethod
    def map_class_to_dataclass(source_instance, target_dataclass_instance, overwrite=False):
        """
        Maps attributes from a class instance to a dataclass instance.

        Args:
            source_instance (object): Source class instance with attributes to map.
            target_dataclass_instance (object): Target dataclass instance to update.
            overwrite (bool): If True, overwrite fields in the dataclass even if they are not None.

        Returns:
            object: Updated dataclass instance.

        Raises:
            MappingFailedExceptionError: If the mapping fails for any reason.
        """
        if not is_dataclass(target_dataclass_instance):
            raise TypeError("Target instance must be a dataclass")

        try:
            for field in fields(target_dataclass_instance):
                field_name = field.name
                if hasattr(source_instance, field_name):
                    source_value = getattr(source_instance, field_name)
                    target_value = getattr(target_dataclass_instance, field_name)

                    # Set value only if it is not None in the source or overwrite is True
                    if source_value is not None or overwrite:
                        setattr(target_dataclass_instance, field_name, source_value)

            return target_dataclass_instance
        except Exception as e:
            raise MappingFailedExceptionError(type(source_instance).__name__) from e
