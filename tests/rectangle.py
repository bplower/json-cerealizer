import json
import json_cerealizer

class Rectangle(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def rectangle_to_dict(rec):
    return {"x": rec.x, "y": rec.y, "area": rec.x * rec.y}

json_cerealizer.patch()
json_cerealizer.add_serializer(Rectangle, rectangle_to_dict)
r = Rectangle(3, 4)
print(json.dumps(r))
