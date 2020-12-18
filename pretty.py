import json

class Pretty():
    def __init__(self, obj):
        self.data = json.dumps(obj, sort_keys=True, indent=2)