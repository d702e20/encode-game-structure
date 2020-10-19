import json


def write_cgs(file, cgs):
    with open(file, 'w+') as o:
        o.writelines(json.dumps(cgs))


if __name__ == '__main__':
    test = [{0: [1, 2, 3],
            1: [4, 5, 6],
            2: [7, 8, 9]}]
    write_cgs("test.json", test)
