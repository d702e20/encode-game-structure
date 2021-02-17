import json


def write_cgs(file, cgs):
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError

    with open(file, 'w+') as o:
        o.writelines(json.dumps(cgs, default=set_default))