import numpy as np
import matplotlib.pyplot as plt
import sys
import csv

x = []
y = []

if len(sys.argv) != 2:
        sys.exit("Usage: python linear_reg path/to/dataset.csv")

# save image file-name or path to variable f
f = sys.argv[1]

with open(f, "r") as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        for row in csv_reader:
                xi = float(row[0].replace(',', '.'))
                yi = float(row[1].replace(',', '.'))
                x.append(xi)
                y.append(yi)

# transformar as listas x e y em arrays do numpy para poder plotar
x = np.array(x)
y = np.array(y)

# cálculo da regressão linear
a, b = np.polyfit(x, y, 1)

# predicted function
f_pred = a * x + b

print(f"equação da reta: y = {a:.2f}x + {b:.2f}")

# Plotar
plt.scatter(x, y, label="Dados", color='blue')
plt.plot(x, f_pred, color='red', label=f"Regressão Linear\ny = {a:.2f}x + {b:.2f}")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.title("Regressão Linear")
plt.grid(True)
plt.show()

        
