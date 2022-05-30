import sys

liste = [1, 2, 3, 4, 5, 6, 7, 8, 9]
x = 1
y = 2


def Funktion():
    return 4


"""""""""
Einfachste If-Bedingung
"""

if x == 1:
    print("1")
else:
    pass  # pass, kann als nichtstun betrachtet werden

"""""""""""
Elif-Beispiel
"""
if x == 1:
    print("Erste If-Bedingung trifft zu")
elif x == 2:
    print("Zweite If-Bedingung trifft zu")
elif x == 3:
    print("Dritte If-Bedingung trifft zu")
else:
    print("Keine If-Bedingung trifft zu ")

"""""""""""
If-Beispiel Verkettung
"""

if x == 1 or x >= 2 or Funktion() == 1:
    print("1")
elif x == 1 and y == 2:
    pass
else:
    pass  # pass, kann als nichtstun betrachtet werden

"""""""""
--------------------------------------------Schleifen-------------------------------------------------------------------
"""

"""""""""
Einfachste for-Schleife
"""

for i in liste:
    print(i)

"""""""""
Break und Continue 
"""

for i in liste:
    if i == 5:
        break
    else:
        pass
    print(i)  # Output: 1, 2, 3, 4
print("Ich werde ausgegeben wenn die 5 erreicht ist")

for i in liste:
    if i == 5:
        continue  # wenn die 5 erreicht ist, wird wieder von vorne angefangen
    else:
        pass
    print(i)  # Output: 1, 2, 3, 4, 6, 7, 8, 9

"""""""""
Beispiel für eine Kombination einer for-Schleife und einer if-Bedingung um zu überprüfen ob eine Zahl durch 2 Teilbar ist 
"""
for i in liste:  # jedes einzelne Element in der Liste liste wird in der Variable i gespeichert und die Bedingung ausgefürt
    rest = i % 2  # Element wird durch 2 geteilt der Rest wird in er Variable rest gespeichert
    if rest == 1:  # bei Rest gleich 1 wird print() ausgeführt
        print(f'{i} ist nicht durch 2 Teilbar')
    elif rest == 0:  # bei Rest gleich 0 wird print() ausgeführt
        print(f'{i} ist durch 2 Teilbar')
    else:  # falls Bedingung fehlschlägt
        print("Fehler")
        sys.exit(0)
