"""
Gerüst zur Lösung der Aufgabe 1 zur Übung Algorithmische Lösung technischer Probleme - Interpolation
"""

import csv
import matplotlib.pyplot as plt


# Funktion zur linearen Interpolation von x zwischen den Punkten (x1, y1) und (x2, y2)
def linear_interpolation(x, x1, x2, y1, y2) -> float:
    return float(y1 + ((y2 - y1) / (x2 - x1)) * (x - x1))


# Funtion, um die direkten Nachbarn von x zu finden mit den Stützstellen x0 und Stützwerten y0
def nearest_neighbour(x, x0, y0):
    pass


# Funktion zur Laplace Interpolation an Punkt x mit den Stützstellen x0 und Stützwerten y0
def laplace_interpolation(x, x0, y0):
    pass


# Leere Listen erstellen für Radius und Intensität
radius_csv = []
intensity_csv = []

# Einlesen der CSV-Datei und speichern der Daten in den oben erstellten Listen
with open("Daten_Aufgabe_3/intensity.csv", "r") as csv_file:
    # read file content with csv reader
    csv_reader = csv.reader(csv_file, delimiter=',')

    # loop through all lines
    for i, line in enumerate(csv_reader):

        # skip first line and avoid empty lines
        if i > 0 and len(line):
            # convert radius (first column) and intensity (second column)
            # to floats and append to corresponding lists
            radius_csv.append(float(line[0]))
            intensity_csv.append(float(line[1]))

'''
Berechnungen, Auswertung und Ausgaben ergänzen
'''
