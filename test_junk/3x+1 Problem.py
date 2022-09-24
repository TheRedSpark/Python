

def rechner(zahlen) -> None:
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


rechner(range(1, int(input("Bis zu welcher Zahl"))))
