import typing
from dataclasses import fields

from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)  # Target model type
S = TypeVar("S", bound=BaseModel)  # Source model type

class ClassMapper:
    @staticmethod
    def map_source_to_target_model(source: S, target_class: Type[typing.T]) -> typing.T:
        """Generic function to map one Pydantic model to another"""
        source_dict = source.model_dump(by_alias=True, exclude_unset=True)
        filtered_data = {key: source_dict[key] for key in target_class.model_fields if key in source_dict}
        return target_class(**filtered_data)

    @staticmethod
    def map_args_to_dataclass(cls, input_obj=None, obj_type=None, **kwargs):
        """
        Maps the provided arguments or another class instance to a dataclass.
        If input_obj is provided, its fields are used as defaults, and kwargs override them.
        """
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

    @staticmethod
    def map_class_to_class(source_instance, target_class, overwrite=True):
        """
        Maps attributes from a class instance to a dataclass instance.

        Args:
            source_instance (object): Source class instance with attributes to map.
            target_class (object): Target dataclass instance to update.
            overwrite (bool): If True, overwrite fields in the dataclass even if they are not None.

        Returns:
            object: Updated dataclass instance.

        Raises:
            MappingFailedExceptionError: If the mapping fails for any reason.
        """

        try:
            for field in fields(target_class):
                field_name = field.name
                if hasattr(source_instance, field_name):
                    source_value = getattr(source_instance, field_name)
                    target_value = getattr(target_class, field_name)

                    # Set value only if it is not None in the source or overwrite is True
                    if source_value is not None or overwrite:
                        setattr(target_class, field_name, source_value)

            return target_class
        except Exception as e:
            raise ValueError(type(source_instance).__name__) from e
