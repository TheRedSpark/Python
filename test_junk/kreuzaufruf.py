# Ein kleiner Test um zu zeigen/demonstrieren wie man Variablen/Funktionen in andere Dokumente auslagert
# Hilfreich um den Überblick zu behalten oder um wichtige Daten zu "verbegen"
# gehört zu kreuzaufruf_daten.py
import kreuzaufruf_daten as k

teststring = k.string
testzahl = k.zahl
print(teststring)
print(testzahl)
ort = input("Wo bist du?")
antwort = k.Ort(ort)
print(antwort)