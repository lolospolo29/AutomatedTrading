import uuid


class IDDecorator:
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, *args, **kwargs):
        # Instantiate the original class
        instance = self.cls(*args, **kwargs)
        # Add a unique ID attribute
        instance.id = str(uuid.uuid4())
        return instance