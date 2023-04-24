import pprint

pp = pprint.PrettyPrinter(indent=4)
test = {}

test["123"] = ["Test", "Test", 122123]

pp.pprint(test)

print(test["123"])
try:

    print(test["111"])
except KeyError:
    print("leider nicht verhanden")

test["111"] = ["Manhatten", "Projekt", 420420]


try:

    print(test["111"])
except KeyError:
    print("leider nicht verhanden")
del test["111"]

try:

    print(len(test["111"]))
except KeyError:
    print("leider nicht verhanden")

print(test)