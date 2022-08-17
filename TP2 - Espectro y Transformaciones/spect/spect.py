import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

plt.rcParams.update({
    "font.size": 18,
    "font.family": "serif"
})

# Crea una imagen negra con un rectángulo blanco en el medio, y la guarda.
shape = (30,30)
f = np.zeros(shape=shape)
f[4:23,12:16] = 1
img = plt.imshow(X=f, cmap="gray", norm=Normalize(vmin=0, vmax=1))
plt.savefig("TP2 - Espectro y Transformaciones\\spect\\imagen.svg")

# Realiza la transformada rápida de Fourier en 2 dimensiones
F = np.fft.fft2(a=f, s=(256,256))
F = np.fft.fftshift(x=F)

absF = abs(F)
minF = np.min(absF)
maxF = np.max(absF)
print(f"min(|F|) = {minF}") # = 0
print(f"max(|F|) = {maxF}") # = 76

logabsF = np.log(1 + absF)
minlogF = np.min(logabsF)
maxlogF = np.max(logabsF)
print(f"min(log(1+|F|)) = {minlogF}") # = 0
print(f"max(log(1+|F|)) = {maxlogF}") # = 4.35

# Grafica el espectro de f (F) en módulo y como logaritmo del módulo
# El objetivo de graficar log(1+|F|) es reducir el rango dinámico,
# de forma que podamos apreciar mejor la imagen.
fig, (ax1, ax2, ax3) = plt.subplots(figsize=(30, 10), nrows=1, ncols=3)
fig.suptitle("Espectros")

ax1.set_title("|F|")
fft2_abs = ax1.imshow(
    X=absF,
    cmap="inferno",
    norm=Normalize(vmin=minF, vmax=maxF)
)
fig.colorbar(fft2_abs, ax=ax1)

ax2.set_title("log(1+|F|)")
fft2_logabs = ax2.imshow(
    X=logabsF,
    cmap="inferno",
    norm=Normalize(vmin=minlogF, vmax=maxlogF)
)
fig.colorbar(fft2_logabs, ax=ax2)


# Grafica la fase de F
angleF = np.angle(F)

ax3.set_title("angle(F)")
fft2_angle = ax3.imshow(
    X=angleF,
    cmap="inferno",
    norm=Normalize(vmin=-np.pi/2, vmax=np.pi/2)
)
fig.colorbar(fft2_angle, ax=ax3)

plt.savefig("TP2 - Espectro y Transformaciones\\spect\\espectros.svg")
