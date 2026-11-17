import cv2
import numpy as np
from matplotlib import pyplot as plt
import pytesseract
from PIL import Image
import re
import csv

img = cv2.imread('image.png')
alto, ancho = img.shape[:2]

# Eliminar cabecera
recorte = img[int(alto * 0.08):, :]

# Escala de grises
gray = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)

# Eliminar escudos
sin_escudos = gray.copy()
x_inicio_escudos = int(ancho * 0.021)
x_fin_escudos = int(ancho * 0.068)
sin_escudos[:, x_inicio_escudos:x_fin_escudos] = 255

# Escalar x2.5
resized = cv2.resize(sin_escudos, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)

# Binarización Otsu
_, binary = cv2.threshold(resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

fig, axes = plt.subplots(3, 2, figsize=(16, 9))

axes[0, 0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
axes[0, 0].set_title("1. Imagen Original")
axes[0, 0].axis("off")

axes[0, 1].imshow(cv2.cvtColor(recorte, cv2.COLOR_BGR2RGB))
axes[0, 1].set_title("2. Recorte de filas (ROI)")
axes[0, 1].axis("off")

axes[1, 0].imshow(gray, cmap='gray')
axes[1, 0].set_title("3. Escala de grises")
axes[1, 0].axis("off")

axes[1, 1].imshow(sin_escudos, cmap='gray')
axes[1, 1].set_title("4. Escudos/flechas eliminados")
axes[1, 1].axis("off")

axes[2, 0].imshow(resized, cmap='gray')
axes[2, 0].set_title("5. Redimensionado x2.5")
axes[2, 0].axis("off")

axes[2, 1].imshow(binary, cmap='gray')
axes[2, 1].set_title("6. Binarización final (Otsu)")
axes[2, 1].axis("off")

plt.tight_layout()
plt.show()

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pil_img = Image.fromarray(binary)
texto = pytesseract.image_to_string(pil_img, config='--psm 6')
print("Texto bruto:\n", texto)

# Eliminar errores con números
def limpiar_numero_ocr(valor):
    # 1. Reemplazos completo (Evita errores al leer números)
    reemplazos_completos = {
        ']': '1', '[': '1', 'I': '1', 'l': '1', '|': '1', '!': '1', 'i': '1',
        'N': '11', 'NN': '11', 'nn': '11', 'ii': '11', 'II': '11', 'll': '11', 'H': '11', 'HH': '11', 'u': '11',
        'O': '0', 'o': '0', 'D': '0', 'Q': '0',
        'S': '5', 's': '5', 'SS': '5', 'ss': '5',
        'B': '8', 'Z': '2', 'z': '2', 'A': '4',
        'G': '6', 'g': '9', 'gg': '9', 'q': '9'
    }
    if valor in reemplazos_completos:
        return reemplazos_completos[valor]
    
    # 2. Reemplazo carácter a carácter (Evita errores al leer números)
    reemplazos_char = {
        ']': '1', '[': '1', 'I': '1', 'l': '1', '|': '1', '!': '1', 'i': '1',
        'O': '0', 'o': '0', 'D': '0', 'Q': '0',
        'S': '5', 's': '5', 'B': '8', 'Z': '2', 'z': '2', 'A': '4', 'G': '6', 'g': '9'
    }
    limpio = "".join(reemplazos_char.get(c, c) for c in valor)
    return re.sub(r'\D', '', limpio)

cabeceras = ['POS', 'EQUIPO', 'PTS', 'PJ', 'PG', 'PE', 'PP', 'GF', 'GC', 'TA', 'TR']
filas_estructuradas = []

for linea in texto.splitlines():
    linea = linea.strip()
    if not linea:
        continue
    
    partes = linea.split()

    # Solo procesar líneas con al menos 10 partes (equipo + estadísticas)
    if len(partes) >= 10:
        # Leemos de derecha a izquierda para obtener las estadísticas (Lo demás es el nombre del equipo)
        estadisticas_brutas = partes[-9:]
        estadisticas_limpias = [limpiar_numero_ocr(num) for num in estadisticas_brutas]
        
        if all(col.isdigit() for col in estadisticas_limpias):
            parte_izquierda = " ".join(partes[:-9])
            # Elimina todo lo que haya antes de la primera mayúscula seguida de minúscula. (Antes de Donostia añadia un iH)
            equipo = re.sub(r'^.*?(?=[A-Z][a-z])', '', parte_izquierda).strip()
            pos = str(len(filas_estructuradas) + 1)
            filas_estructuradas.append([pos, equipo] + estadisticas_limpias)

archivo_csv = 'clasificacion_liga.csv'

with open(archivo_csv, mode='w', newline='', encoding='utf-8-sig') as f:
    escritor = csv.writer(f, delimiter=';')
    escritor.writerow(cabeceras)
    escritor.writerows(filas_estructuradas)

print(f"\nSe han guardado {len(filas_estructuradas)} equipos limpios en '{archivo_csv}':")
for fila in filas_estructuradas:
    print(";".join(fila))