# GenAIVideogame

Juego de misterio estilo Cluedo desarrollado en Ren'Py. La partida usa un generador Python para crear un caso aleatorio y pedir a Mercury/Inception Labs el contenido narrativo: introduccion, habitaciones, objetos, dialogos, armas y resultados de acusacion.

## Estructura actual

| Ruta | Funcion |
|---|---|
| `S16Game/` | Proyecto principal del juego Ren'Py. |
| `S16Game/build_prompt.py` | Genera `world_data.json` llamando a Mercury. Es el generador que usa el juego real. |
| `S16Game/randomizador.py` | Decide victima, asesino, complice, arma, escena, ubicaciones y preguntas. |
| `S16Game/api.py` | Cliente HTTP para Mercury/Inception Labs. |
| `S16Game/world_data.json` | Datos narrativos consumidos por el juego. |
| `S16Game/misterio_generado.json` | Estado secreto generado para la partida. |
| `S16Game/world_data_adapter.py` | Adapta `world_data.json` al formato que espera Ren'Py. |
| `requirements.txt` | Dependencias Python necesarias para el generador. |
| `setup.ps1` | Crea `.venv` e instala dependencias. |

> Los archivos Python de la raiz son prototipos o utilidades. Para el juego integrado, usa principalmente los archivos dentro de `S16Game/`.

## 1. Configurar `.env`

Crea un archivo `.env` en la raiz del proyecto, al lado de `requirements.txt`:

```env
MERCURY_API_KEY=tu_api_key_de_mercury
```

No subas `.env` a Git. Ya esta incluido en `.gitignore`.

Si alguna API key se pego en un chat, documento o commit, hay que rotarla.

## 2. Crear el entorno virtual

Desde PowerShell, entra en la carpeta raiz del proyecto:

```powershell
cd "C:\Users\David\Documentos\Máster\Seminarios\S16 INTELIGENCIA ARTIFICIAL GENERATIVA Y PROMPT ENGINEERING APLICACIONES Y RETOS\GenAIVideogame"
```

Ejecuta el setup:

```powershell
.\setup.ps1
```

El script:

1. verifica Python 3.10;
2. crea `.venv` si no existe;
3. actualiza `pip`;
4. instala `requirements.txt`;
5. reintenta con hosts confiables si Windows da problemas SSL con PyPI.

Si PowerShell bloquea scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\setup.ps1
```

Instalacion manual equivalente:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 3. Generar una partida nueva con IA

Para generar el contenido del juego:

```powershell
.\.venv\Scripts\python.exe .\S16Game\build_prompt.py
```

Este comando llama a Mercury y puede tardar porque hace varias llamadas:

1. intro y mapa de pistas;
2. habitaciones;
3. personajes;
4. armas;
5. resultados de acusacion.

Archivos que se actualizan:

```txt
S16Game/misterio_generado.json
S16Game/world_data.json
S16Game/last_mercury_response.txt
```

## 4. Lanzar el juego

El juego se lanza desde Ren'Py abriendo el proyecto:

```txt
S16Game/
```

Flujo recomendado:

1. Genera `S16Game/world_data.json` con `S16Game/build_prompt.py`.
2. Abre Ren'Py Launcher.
3. Selecciona el proyecto `S16Game`.
4. Pulsa `Launch Project`.

Al iniciar, el juego intenta leer `S16Game/world_data.json`. Si existe y es valido, usa esos datos generados. Si no, cae en modo fallback con contenido de reserva.

## 5. Flujo interno de archivos

```txt
S16Game/build_prompt.py
  -> importa S16Game/randomizador.py
      -> genera victima, asesino, complice, arma, escena y preguntas
      -> guarda S16Game/misterio_generado.json

  -> importa S16Game/api.py
      -> llama a Mercury usando MERCURY_API_KEY

  -> genera S16Game/world_data.json

Ren'Py / S16Game/game/script.rpy
  -> lee S16Game/world_data.json
  -> usa S16Game/world_data_adapter.py
  -> carga textos, habitaciones, NPCs, armas y resultados de acusacion
```

## 6. Verificaciones utiles

Comprobar sintaxis Python sin llamar a Mercury:

```powershell
.\.venv\Scripts\python.exe -m py_compile .\S16Game\api.py .\S16Game\build_prompt.py .\S16Game\randomizador.py .\S16Game\world_data_adapter.py
```

Probar solo el cliente Mercury manualmente:

```powershell
.\.venv\Scripts\python.exe .\api.py
```

Revisar la ultima generacion cruda de Mercury:

```txt
S16Game/last_mercury_response.txt
```

## 7. Notas importantes

- `Preguntas.md`, `Armas.md` y `Estancias.md` de la raiz no se usan dentro de `S16Game`.
- En `S16Game`, preguntas, armas y estancias salen de `S16Game/randomizador.py`.
- La victima no aparece en `ubicaciones_personajes`: el juego la trata aparte como `victim_id` / `victim_name` y como cuerpo en la escena del crimen.
- `S16Game/world_data.json` es el archivo clave para la narrativa runtime.
