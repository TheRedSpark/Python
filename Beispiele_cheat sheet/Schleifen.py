import sys

liste = [1, 2, 3, 4, 5, 6, 7, 8, 9]

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
