anzahl_zahlen = int(input("Bis zu Welcher Zahl?"))
x = range(1, anzahl_zahlen)
print(x)
for zahl in x:
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
    print(f"{len(steps)} Schritte für {steps[0]} mit der Liste{steps}")
