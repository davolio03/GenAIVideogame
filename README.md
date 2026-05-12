# GenAIVideogame

Proyecto Python que usa la API de Groq para enviar solicitudes al modelo
`openai/gpt-oss-120b`.

## Instalación rápida

Desde la carpeta del proyecto:

```powershell
cd "C:\Users\David\Documentos\Máster\Seminarios\S16 INTELIGENCIA ARTIFICIAL GENERATIVA Y PROMPT ENGINEERING APLICACIONES Y RETOS\GenAIVideogame"
```

O ejecutá el script de setup:

```powershell
.\setup.ps1
```

Ese script crea `.venv`, verifica que estés usando Python `3.10` e instala
`requirements.txt`.

Instalá las dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

> Si ya tenés el entorno virtual activado, también podés usar:
>
> ```powershell
> pip install -r requirements.txt
> ```

## Configurar `.env`

Creá o editá el archivo `.env` en la raíz del proyecto:

```env
GROQ_API_KEY=tu_api_key_de_groq
```

Ejemplo:

```env
GROQ_API_KEY=gsk_...
```

IMPORTANTE: `.env` contiene secretos. No lo subas a Git. Ya está incluido en
`.gitignore` para evitarlo.

## Ejecutar el proyecto

Sin activar el entorno virtual:

```powershell
.\.venv\Scripts\python.exe api.py
```

O, si activaste el entorno:

```powershell
python api.py
```

Cuando el programa arranque, escribí tu solicitud y presioná Enter.
Para salir, dejá la solicitud vacía y presioná Enter.
