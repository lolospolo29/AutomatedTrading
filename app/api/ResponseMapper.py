import dataclasses
import typing
from abc import ABC
from typing import Type


class ResponseMapper(ABC):
    def fromDict(self, data: dict, cls: Type[dataclasses.dataclass]) -> dataclasses.dataclass:
        """Helper function to convert a dictionary into a dataclass object."""
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
                init_kwargs[key] = self.fromDict(value, getattr(cls, key))
            elif isinstance(value, list) and hasattr(cls, key):
                # Handle List of dataclasses (and other types)
                field_type = getattr(cls, key)
                origin = typing.get_origin(field_type)  # Get the origin of the field type
                if origin is list:  # If it's a List, handle it properly
                    item_type = typing.get_args(field_type)[0]  # Get the item type of the List
                    # Convert each item in the list to the corresponding dataclass
                    init_kwargs[key] = [
                        self.fromDict(item, item_type) if isinstance(item, dict) else item
                        for item in value
                    ]
                elif isinstance(field_type, type(typing.Union)):  # Handle Optional (Union[Type, None])
                    # If the type is Optional, unwrap it to get the real type (the first part of the Union)
                    if value is not None:
                        item_type = typing.get_args(field_type)[0]
                        init_kwargs[key] = self.fromDict(value, item_type) if isinstance(value, dict) else value
                    else:
                        init_kwargs[key] = value

        # print(f"Final initialized kwargs: {init_kwargs}")  # Debugging
        return cls(**init_kwargs)