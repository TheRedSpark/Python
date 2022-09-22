zahl = input("Welche Zahl")

while True:
    if zahl == 1:
        break
    if zahl % 2 == 0:
        zahl = zahl / 2
    else:
        zahl = zahl * 3 + 1
    print(zahl)
