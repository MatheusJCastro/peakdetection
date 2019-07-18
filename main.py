#########################################################
# Detectção de Picos em imagens monocromáticas          #
# Peak Detection on monochrome pictures                 #
#                                                       #
# Author: Matheus J. Castro                             #
# Created on Jul 2019                                   #
#                                                       #
##########################################################

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def peak_detection(data, half_window=50, threshold=50):
    n, m = data.shape
    peaks = np.zeros(n * m).reshape(n, m)
    for i in range(n):
        imin = i - half_window
        imax = i + half_window
        if imin < 0:
            imin = 0
        if imax >= n:
            imax = n - 1

        for j in range(m):
            jmin = j - half_window
            jmax = j + half_window
            if jmin < 0:
                jmin = 0
            if jmax >= m:
                jmax = m - 1

            if (data[i, j] == data[imin:imax, jmin:jmax].max()) and (data[i, j] > threshold):
                peaks[i, j] = 1

    peaks = peaks.reshape(n * m, )
    ch_peaks = np.arange(0, n * m)[peaks == 1]
    peaks = peaks.reshape(n, m)

    return ch_peaks, peaks


def rescale_array(peak1, data):
    n, m = data.shape
    data = np.arange(0, n * m).reshape(n, m)
    peak2 = np.zeros(len(peak1)*2).reshape(len(peak1), 2)
    for k in range(len(peak1)):
        for i in range(n):
            for j in range(m):
                if peak1[k] == data[j, i]:
                    peak2[k, 0] = i
                    peak2[k, 1] = j
    return peak2


def peak_profile(image, peaks):
    linha = peaks[0, 1]
    # linha = 277 #escolha da linha de perfil manual
    lista = np.zeros(image.shape[0])
    tamanho = 0

    for i in range(len(lista)):
        lista[i] = image[int(linha), i]

    no_peak = True
    for i in range(peaks.shape[0]):
        if peaks[i, 1] == linha:
            tamanho += 1
            no_peak = False

    if no_peak:
        return np.zeros(image.shape[0]), 0, [0, 0], [0, 0]

    peak_x = np.zeros(tamanho)
    peak_y = np.zeros(tamanho)

    count = 0
    for i in range(peaks.shape[0]):
        if peaks[i, 1] == linha:
            peak_x[count] = peaks[i, 0]
            peak_y[count] = image[int(linha), int(peak_x[count])]
            count += 1

    return lista, linha, peak_x, peak_y


# imag = Image.open("800,800.bmp")
imag = Image.open("test.bmp")
# imag.show()

im = np.asarray(imag)

peak_list, peak_array = peak_detection(im, half_window=10, threshold=10)
peak_xy = rescale_array(peak_list, im)
print(peak_list)
print(peak_xy)
# np.savetxt("data.txt", peak_array)


perfil, line, peak_perfil_x, peak_perfil_y = peak_profile(im, peak_xy)


plt.figure(figsize=(15, 4))
plt.subplot(131)
plt.title("Matriz da Imagem")
plt.xlabel("Pixel")
plt.ylabel("Pixel")
plt.imshow(im)

plt.subplot(132)
plt.xlim(0, 300)
plt.ylim(300, 0)
plt.title("Matriz de Detecção de Pico")
plt.xlabel("Pixel")
plt.ylabel("Pixel")
#plt.xlabel("Pico em: {}".format(peak_xy))
plt.imshow(peak_array)

plt.subplot(133)
plt.title("Perfil na Linha {} (pico)".format(line))
plt.xlabel("Posição x na matriz")
plt.ylabel("Counts")
plt.plot(np.arange(0, im.shape[0]), perfil)
plt.plot(peak_perfil_x, peak_perfil_y, " ", marker="o", markersize=5)
plt.annotate("Pico: {}".format(peak_xy[0]), xy=(peak_perfil_x[0], peak_perfil_y[0]), arrowprops=dict(arrowstyle='->'),
             xytext=(150, 150))
plt.savefig("plot.png", format='png')
plt.show()
