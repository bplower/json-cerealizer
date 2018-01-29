# JSON Cerealizer
[![Build Status](https://api.travis-ci.org/bplower/json-cerealizer.svg?branch=master)](https://api.travis-ci.org/bplower/json-cerealizer.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/bplower/json-cerealizer/badge.svg?branch=master)](https://coveralls.io/github/bplower/json-cerealizer?branch=master)

A simple library for monkey patching the python json library, thereby making it
easier to add serializers for objects that cannot be encoded using the default
JSONEncoder.

## Install

```
pip install json-cerealizer
```

## TL;DR Example

Import the library, run the monkey patch, then register functions to handle
class serialization. Call json.dumps as usual and receive output for your
typically un-encodable objects.

```python
>>> from datetime import datetime
>>> import json
>>> import json_cerealizer
>>>
>>> json_cerealizer.patch()
>>> json_cerealizer.add_serializer(datetime, datetime.isoformat)
>>>
>>> time_dict = {"now": datetime.now()}
>>> json.dumps(time_dict)
'{"now": "2017-08-21T19:57:31.761091"}'
```

## Use Case

The JSON standard can only represent a handful of data types. If you attempt to
serialize a non-standard type, you receive a TypeError. The following is an
example showing that datetime objects cannot be serialized by the default
JSON encoder.

```python
>>> import json
>>> from datetime import datetime
>>>
>>> time_dict = {"now": datetime.now()}
>>> time_dict
{'now': datetime.datetime(2017, 8, 21, 19, 47, 17, 785813)}
>>> json.dumps(time_dict)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.5/json/__init__.py", line 230, in dumps
    return _default_encoder.encode(obj)
  File "/usr/lib/python3.5/json/encoder.py", line 198, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "/usr/lib/python3.5/json/encoder.py", line 256, in iterencode
    return _iterencode(o, 0)
  File "/usr/lib/python3.5/json/encoder.py", line 179, in default
    raise TypeError(repr(o) + " is not JSON serializable")
TypeError: datetime.datetime(2017, 8, 21, 19, 47, 17, 785813) is not JSON serializable
```

This issue is easily resolved by subclassing the json.JSONEncoder class,
allowing you to specify how objects should be serialized.

```python
>>> import json
>>> from datetime import datetime
>>>
>>> class MyEncoder(json.JSONEncoder):
...     def default(self, obj):
...         if isinstance(obj, datetime):
...             return obj.isoformat()
...
>>> time_dict = {"now": datetime.now()}
>>> json.dumps(time_dict, cls=MyEncoder)
'{"now": "2017-08-21T19:57:31.761091"}'
```

While this works fine in small cases, it becomes bloated when you want to add
support for several more types. This is where json-cerealizer shines. Here we
monkey patch the json library, then register a function to handle instances of
a particular class. In this case, we are saying instances of `datetime` should
be passed into the function `datetime.isoformat`, which will return a value
that is natively serializable.

```python
>>> from datetime import datetime
>>> import json
>>> import json_cerealizer
>>>
>>> json_cerealizer.patch()
>>> json_cerealizer.add_serializer(datetime, datetime.isoformat)
>>>
>>> time_dict = {"now": datetime.now()}
>>> json.dumps(time_dict)
'{"now": "2017-08-21T19:57:31.761091"}'
```

To solidify our understanding, lets handle a class of our own.

```python
>>> import json
>>> import json_cerealizer
>>>
>>> class Rectangle(object):
...     def __init__(self, x, y):
...         self.x = x
...         self.y = y
...
>>> def rectangle_to_dict(rec):
...     return {"x": rec.x, "y": rec.y, "area": rec.x * rec.y}
...
>>> json_cerealizer.patch()
>>> json_cerealizer.add_serializer(Rectangle, rectangle_to_dict)
>>> r = Rectangle(3, 4)
>>> json.dumps(r)
'{"x": 3, "y": 4, "area": 12}'
```
