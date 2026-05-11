import os
from typing import Any

import requests
from dotenv import load_dotenv


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"

load_dotenv()


class GroqAPIError(RuntimeError):
    """Error devuelto por la API de Groq."""


def ask_groq(
    prompt: str,
    *,
    system_prompt: str = "Sos un asistente útil, claro y preciso.",
    temperature: float = 0.7,
    max_tokens: int = 1024,
) -> str:
    """
    Envía una solicitud al modelo openai/gpt-oss-120b usando Groq.

    Antes de ejecutar:
        PowerShell:
            $env:GROQ_API_KEY = "tu_api_key"

        Linux/macOS:
            export GROQ_API_KEY="tu_api_key"
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise GroqAPIError(
            "Falta GROQ_API_KEY. Configurala como variable de entorno; "
            "no la hardcodees en el archivo."
        )

    payload: dict[str, Any] = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    response = requests.post(
        GROQ_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )

    if not response.ok:
        raise GroqAPIError(f"Groq error {response.status_code}: {response.text}")

    data = response.json()
    return data["choices"][0]["message"]["content"]


if __name__ == "__main__":
    print("Escribí tu solicitud para Groq. Dejá vacío y presioná Enter para salir.")

    while True:
        user_prompt = input("\nSolicitud> ").strip()
        if not user_prompt:
            break

        try:
            answer = ask_groq(user_prompt)
            print(f"\nRespuesta:\n{answer}")
        except GroqAPIError as error:
            print(f"\nError: {error}")
