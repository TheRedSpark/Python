#gehört zu kreuzaufruf.py

string = "Das ist ein Test"
zahl = 2
ort = ""


def Ort(x):
    if x == "Hier":
        ort = "Schönfeld"
        return ort
    elif x == "Dort":
        ort = "Wohnheim"
        return ort
    else:
        print("Systemerrot")
