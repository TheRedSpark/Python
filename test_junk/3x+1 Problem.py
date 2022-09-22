anzahl_zahlen = int(input("Bis zu Welcher Zahl?"))
x = range(anzahl_zahlen)

for zahl in x:
    steps = 0
    print(zahl)
    while True:
        if zahl == 1:
            break
        if zahl % 2 == 0:
            zahl = zahl / 2
            steps = steps + 1
        else:
            zahl = zahl * 3 + 1
            steps = steps + 1
    print(f"Die Anzahl der Schritte {steps} für {zahl}")
