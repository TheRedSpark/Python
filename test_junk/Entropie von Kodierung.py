import math

data = [0.65, 0.11, 0.05, 0.05, 0.04, 0.04, 0.04, 0.02]
encode = ["V", "Z", "B", "T", ">", "<", "S"]
hoffman = [(0.65, "V"), (0.11, "Z"), (0.05, "B"), (0.05, "E"), (0.04, "T"), (0.04, ">"), (0.04, "<"), (0.02, "S")]
entropie = 0


def tree_hoffmal(data: list):
    result = []
    steps = hoffmal_iter_best(data.copy())
    encoding = hoffmal_alg_iter(data.copy(), steps)
    kodierung = 0
    for zeichen in encoding[0][1]:
        result.append(["",zeichen])


    encoding = hoffmal_alg_iter(data.copy(), steps - 1)
    print(encoding)

    encoding = hoffmal_alg_iter(data.copy(), steps - 2)
    print(encoding)

    encoding = hoffmal_alg_iter(data.copy(), steps - 3)
    print(encoding)

    encoding = hoffmal_alg_iter(data.copy(), steps - 4)
    print(encoding)




    print(result)
    #print(encoding)
    #result.append([kodierung, encoding[0][1][0]])

    #result.append([kodierung, encoding[0][1][0]])
    # print(result)
    return result


def hoffmal_iter_best(data: list) -> int:
    i = 0
    while True:

        second_element = data.pop()
        first_element = data.pop()
        next_element = (first_element[0] + second_element[0], first_element[1] + second_element[1])
        # print(next_element)
        data.append(next_element)
        # print(data)
        data.sort(reverse=True)
        # print(data)
        i = i + 1
        if len(data) == 1:
            break

    # print(data[0])
    return i


def hoffmal_alg_iter(data: list, iterationen: int) -> list:
    i = 0
    while True:
        second_element = data.pop()
        first_element = data.pop()
        next_element = (first_element[0] + second_element[0], first_element[1] + second_element[1])
        # print(next_element)
        data.append(next_element)
        # print(data)
        data.sort(reverse=True)
        # print(data)
        i = i + 1
        if len(data) == 1 or iterationen == i:
            break

    # print(data[0])
    return data


def entropie_calc(data) -> float:
    global entropie
    for auftrittswarscheinlichkeit in data:
        entropie = entropie + auftrittswarscheinlichkeit * math.log(auftrittswarscheinlichkeit, 2)

    entropie = entropie * -1
    return round(entropie, 2)


def main():
    result = hoffmal_alg_iter(hoffman.copy(), 10000)
    #print(result)
    tree_res = tree_hoffmal(hoffman.copy())
    #print(tree_res)


if __name__ == '__main__':
    main()
