import json

# A dictionary containing the same keyword arguments that are provided to the
# standard JSONEncoder in the json module here:
# https://github.com/python/cpython/blob/master/Lib/json/__init__.py#L110
ENCODER_KWARGS = {"skipkeys": False, "ensure_ascii": True, "separators": None,
                  "check_circular": True, "allow_nan": True, "indent": None,
                  "default": None}

class CerealJSONEncoder(json.JSONEncoder):
    """ Extended JSONEncoder supporting entensible serializers
    """
    serializers = {}

    def default(self, obj): # pylint: disable=method-hidden,arguments-differ
        """ The JSONEncoder entrypoint for handling objects that can't be
        natively serialized.
        """
        # Check if this object class has been associated with a serializer. If
        # it hasn't, we let the base class default method raise the TypeError.
        if obj.__class__ not in self.serializers:
            return json.JSONEncoder.default(self, obj)
        # Reaching this means we have a function associated with the class of
        # the provided object. Call the registered function, providing the
        # given object as the first argument.
        return self.serializers[obj.__class__](obj)

    @classmethod
    def register_instance(cls, target_class, serializer_func):
        """ Stores an association between a class, and a function that should
        be able to represent said class in terms of native json data types
        """
        cls.serializers[target_class] = serializer_func

def patch():
    """ Insert our custom JSONEncoder
    """
    # Create an instance of our custom JSONEncoder
    encoder = CerealJSONEncoder(**ENCODER_KWARGS)
    # Replace the value of _default_encoder with our new encoder instance
    json.__dict__['_default_encoder'] = encoder

def unpatch():
    """ Remove the monkey patched custom JSONEncoder
    """
    # Make an instance of the standard JSONEncoder
    encoder = json.JSONEncoder(**ENCODER_KWARGS)
    # Replace our custom encoder with the default
    json.__dict__['_default_encoder'] = encoder

def add_serializer(class_ref, serializer):
    """ Helper function for registering serializer functions
    """
    CerealJSONEncoder.register_instance(class_ref, serializer)
