import matplotlib.pyplot as plt


def rechner(zahlen) -> list:
    final = []
    for zahl in zahlen:
        steps = []
        steps.append(zahl)
        while True:
            if zahl == 1:
                break
            if zahl % 2 == 0:
                zahl = zahl / 2
                steps.append(zahl)
            else:
                zahl = zahl * 3 + 1
                steps.append(zahl)
        print(f"{len(steps)} Schritte für {steps[0]}")
        final.append(len(steps))
    return final


list_steps = rechner(range(1, int(input("Bis zu welcher Zahl"))))

plt.plot(list_steps)
plt.show()