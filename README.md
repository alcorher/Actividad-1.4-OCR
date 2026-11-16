# Actividad 1.4: extracción de una clasificación de liga mediante OCR

Este proyecto procesa una imagen con una tabla de clasificación de fútbol y
extrae sus datos usando OCR (reconocimiento óptico de caracteres). El resultado
se guarda en `clasificacion_liga.csv`.

## Requisitos

- Windows.
- Python 3.14 o superior.
- [`uv`](https://docs.astral.sh/uv/), para crear el entorno e instalar las
  dependencias de Python.
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract), instalado en:
  `C:\Program Files\Tesseract-OCR\tesseract.exe`.

El programa utiliza `opencv-python`, `matplotlib`, `Pillow` y `pytesseract`.
Las dependencias Python están declaradas en `pyproject.toml` y fijadas en
`uv.lock`.

## Instalación

Desde la carpeta del proyecto:

```powershell
uv sync
```

Si Tesseract está instalado en otra ubicación, modifica la asignación
`pytesseract.pytesseract.tesseract_cmd` de `main.py` para indicar la ruta
correcta al ejecutable.

## Ejecución

La imagen de entrada debe llamarse `image.png` y estar en la raíz del proyecto.
Ejecuta:

```powershell
uv run python main.py
```

El programa:

1. Carga `image.png`.
2. Recorta la cabecera de la tabla.
3. Convierte la imagen a escala de grises.
4. Elimina la zona de escudos y flechas.
5. Amplía la imagen 2,5 veces.
6. Aplica una binarización mediante el método de Otsu.
7. Muestra las etapas del preprocesamiento.
8. Extrae el texto con Tesseract usando la configuración `--psm 6`.
9. Limpia errores frecuentes del OCR en valores numéricos.
10. Guarda las filas detectadas en `clasificacion_liga.csv`.

Durante la ejecución se abre una ventana de Matplotlib con las imágenes
intermedias y se imprime en la consola el texto reconocido y las filas
generadas.

## Archivo de salida

`clasificacion_liga.csv` utiliza `;` como separador. Contiene las siguientes columnas:

| Columna | Descripción |
| --- | --- |
| `POS` | Posición del equipo |
| `EQUIPO` | Nombre del equipo |
| `PTS` | Puntos |
| `PJ` | Partidos jugados |
| `PG` | Partidos ganados |
| `PE` | Partidos empatados |
| `PP` | Partidos perdidos |
| `GF` | Goles a favor |
| `GC` | Goles en contra |
| `TA` | Tarjetas amarillas |
| `TR` | Tarjetas rojas |

El fichero se sobrescribe en cada ejecución. Si no se detectan filas válidas,
se conserva únicamente la cabecera.

## Ajustes y solución de problemas

- **No se encuentra Tesseract:** comprueba que existe el ejecutable indicado o
  actualiza `tesseract_cmd`.
- **No se encuentra `image.png`:** coloca la imagen en la raíz del proyecto o
  cambia la ruta usada en `cv2.imread`.
- **Resultados OCR incorrectos:** revisa la imagen binarizada y ajusta el
  recorte, la zona de escudos, el escalado o la configuración `--psm 6`.
- **La ventana de visualización bloquea el proceso:** cierra la ventana de
  Matplotlib para continuar con la generación del CSV.

## Estructura

```text
.
├── image.png               # Imagen de entrada
├── main.py                 # Preprocesamiento, OCR y exportación
├── clasificacion_liga.csv  # Resultado generado
├── pyproject.toml          # Metadatos y dependencias
└── uv.lock                 # Versiones bloqueadas
```