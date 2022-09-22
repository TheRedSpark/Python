zahl = int(input("Welche Zahl"))
steps = 0
while True:
    if zahl == 1:
        break
    if zahl % 2 == 0:
        zahl = zahl / 2
        steps = +1
    else:
        zahl = zahl * 3 + 1
        steps = +1
    print(zahl)
print(f"Die Anzahl der Schritte {steps}")
