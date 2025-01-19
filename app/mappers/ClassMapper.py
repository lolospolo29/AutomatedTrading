import dataclasses
import typing
from dataclasses import is_dataclass, fields
from typing import Type

from app.mappers.exceptions.MappingFailedExceptionError import MappingFailedExceptionError


class ClassMapper:
    def map_dict_to_dataclass(self, data: dict, cls: Type[dataclasses.dataclass]) -> dataclasses.dataclass:
        """Helper function to convert a dictionary into a dataclass object."""
        try:
                # print(f"Converting data into {cls.__name__}...")  # Debugging
                # Collect all field names for the dataclass
                fieldnames = {f.name for f in dataclasses.fields(cls)}
                init_kwargs = {k: v for k, v in data.items() if k in fieldnames}

                # Get the types of the fields
                field_types = {f.name: f.type for f in dataclasses.fields(cls)}

                # Recursively handle nested dataclasses
                for key, value in init_kwargs.items():
                    # print(f"Processing field: {key} -> {value}")  # Debugging

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
            # Iterate over the fields of the dataclass and set them on the target instance
            for field in fields(data_class_instance):
                setattr(target_instance, field.name, getattr(data_class_instance, field.name))

            return target_instance
        except Exception as e:
            raise MappingFailedExceptionError(type(data_class_instance).__name__)
