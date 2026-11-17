# Actividad 1.4: extracción de una clasificación mediante OCR

Este proyecto extrae la clasificación de una liga de fútbol a partir de
`image.png`. La imagen se preprocesa con OpenCV y el texto se reconoce con
Tesseract OCR. Finalmente, las filas detectadas se exportan a
`clasificacion_liga.csv`.

> **Importante:** el OCR no garantiza resultados perfectos. Conviene revisar
> el CSV generado, especialmente cuando la imagen tiene texto pequeño,
> símbolos o nombres de equipos poco habituales.

## Requisitos

- Windows.
- Python 3.14 o una versión compatible con `pyproject.toml`.
- [`uv`](https://docs.astral.sh/uv/), para crear el entorno e instalar las
  dependencias.
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).

El programa espera encontrar Tesseract en:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

Si se instala en otra ubicación, hay que actualizar `tesseract_cmd` en
`main.py`.

Las dependencias de Python son `opencv-python`, `matplotlib`, `Pillow` y
`pytesseract`. Están declaradas en `pyproject.toml` y fijadas en `uv.lock`.

## Instalación

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
uv sync
```

Comprueba también que Tesseract está instalado:

```powershell
& "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
```

## Uso

1. Coloca la imagen de entrada en la raíz del proyecto y llámala `image.png`.
2. Ejecuta el programa desde esa misma carpeta:

   ```powershell
   uv run python main.py
   ```

3. Cierra la ventana de Matplotlib cuando quieras continuar con la
   generación del CSV.

El programa realiza estas etapas:

1. Carga la imagen y elimina la cabecera.
2. Convierte la región de interés a escala de grises.
3. Oculta la zona de escudos y flechas.
4. Amplía la imagen 2,5 veces.
5. Aplica una binarización mediante el método de Otsu.
6. Muestra las imágenes intermedias para poder revisar el preprocesamiento.
7. Reconoce el texto con Tesseract usando `--psm 6`.
8. Corrige algunos errores frecuentes en valores numéricos.
9. Guarda las filas detectadas en `clasificacion_liga.csv`.

Las rutas de `image.png` y `clasificacion_liga.csv` son relativas a la
carpeta desde la que se ejecuta el comando. El CSV se sobrescribe en cada
ejecución; si no se detecta ninguna fila válida, contiene únicamente la
cabecera.

## Formato del CSV

El fichero usa `;` como separador y codificación UTF-8 con BOM. Sus columnas
son:

| Columna | Descripción |
| --- | --- |
| `POS` | Posición en la clasificación |
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

La posición (`POS`) se asigna según el orden de las filas reconocidas, no se
calcula a partir de los puntos.

## Solución de problemas

- **No se encuentra Tesseract:** instala Tesseract o cambia
  `pytesseract.pytesseract.tesseract_cmd` en `main.py`.
- **No se encuentra `image.png`:** coloca la imagen en la carpeta de ejecución
  o ejecuta el comando desde la raíz del proyecto.
- **El OCR confunde números o nombres:** revisa la imagen binarizada que se
  muestra en pantalla y ajusta el recorte, la zona eliminada, el escalado o
  la configuración `--psm 6`.
- **La ventana de visualización parece bloqueada:** ciérrala para que el
  programa continúe con el reconocimiento y la escritura del CSV.
- **El CSV contiene datos incorrectos:** corrige manualmente las filas o
  mejora el preprocesamiento antes de usar los datos en otro proceso.

## Estructura del proyecto

```text
.
├── image.png               # Imagen de entrada
├── main.py                 # Preprocesamiento, OCR y exportación
├── clasificacion_liga.csv  # Resultado generado
├── pyproject.toml          # Metadatos y dependencias
└── uv.lock                 # Versiones bloqueadas
```
