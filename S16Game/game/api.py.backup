import os
import ssl
import tempfile
import time
from pathlib import Path
from typing import Any

import certifi
import requests
from dotenv import load_dotenv


MERCURY_MODEL = "mercury-2"
MERCURY_API_URL = "https://api.inceptionlabs.ai/v1/chat/completions"

def crear_bundle_certificados() -> str:
    """Combina certifi con certificados raiz de Windows para requests."""
    bundle_path = Path(tempfile.gettempdir()) / "mercury_windows_ca_bundle.pem"

    contenido = Path(certifi.where()).read_text(encoding="utf-8")
    if hasattr(ssl, "enum_certificates"):
        for certificado, encoding, _trust in ssl.enum_certificates("ROOT"):
            if encoding != "x509_asn":
                continue
            try:
                contenido += "\n" + ssl.DER_cert_to_PEM_cert(certificado)
            except ValueError:
                continue

    bundle_path.write_text(contenido, encoding="utf-8")
    return str(bundle_path)


def calcular_espera_reintento(response: requests.Response | None, intento: int) -> int:
    """Calcula cuanto esperar antes de reintentar una llamada a Mercury."""
    if response is not None:
        retry_after = response.headers.get("Retry-After")
        if retry_after and retry_after.isdigit():
            return max(1, int(retry_after))

    # Rate limit: esperar una ventana completa de cuota si la API no informa Retry-After.
    if response is not None and response.status_code == 429:
        return 60

    # Errores transitorios de servidor: backoff corto, limitado.
    return min(30, 2 * intento)


def dormir_con_mensaje(segundos: int, motivo: str) -> None:
    print(f"{motivo}. Esperando {segundos}s antes de reintentar...")
    time.sleep(segundos)


load_dotenv()


class MercuryAPIError(RuntimeError):
    """Error devuelto por la API de Mercury/Inception Labs."""


def ask_mercury(
    prompt: str,
    *,
    system_prompt: str = "Sos un asistente util, claro y preciso.",
    temperature: float = 0.7,
    max_tokens: int = 1024,
    response_mime_type: str | None = None,
) -> str:
    """
    Envia una solicitud a Mercury usando MERCURY_API_KEY.

    En .env:
        MERCURY_API_KEY=tu_api_key
    """
    api_key = os.getenv("MERCURY_API_KEY")
    if not api_key:
        raise MercuryAPIError(
            "Falta MERCURY_API_KEY. Configurala en .env o como variable de entorno."
        )

    payload: dict[str, Any] = {
        "model": MERCURY_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    intento = 1
    fallos_transitorios = 0

    while True:
        try:
            response = requests.post(
                MERCURY_API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=120,
                verify=crear_bundle_certificados(),
            )
            response.raise_for_status()
            data = response.json()
            break
        except requests.HTTPError as error:
            response = error.response
            status = response.status_code if response is not None else None

            if status == 429:
                espera = calcular_espera_reintento(response, intento)
                dormir_con_mensaje(espera, "Mercury marco rate limit")
                intento += 1
                continue

            if status in {500, 502, 503, 504}:
                fallos_transitorios += 1
                if fallos_transitorios > 5:
                    raise MercuryAPIError(f"Error conectando con Mercury: {error}") from error
                espera = calcular_espera_reintento(response, intento)
                dormir_con_mensaje(espera, f"Mercury devolvio error transitorio {status}")
                intento += 1
                continue

            raise MercuryAPIError(f"Error conectando con Mercury: {error}") from error
        except requests.RequestException as error:
            fallos_transitorios += 1
            if fallos_transitorios > 5:
                raise MercuryAPIError(f"Error conectando con Mercury: {error}") from error
            espera = calcular_espera_reintento(None, intento)
            dormir_con_mensaje(espera, "Error de red conectando con Mercury")
            intento += 1
        except ValueError as error:
            raise MercuryAPIError("Mercury devolvio una respuesta que no es JSON.") from error

    try:
        choice = data["choices"][0]
        content = choice["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise MercuryAPIError(f"Formato inesperado de Mercury: {data}") from error

    if not content:
        finish_reason = choice.get("finish_reason") if isinstance(choice, dict) else None
        usage = data.get("usage") if isinstance(data, dict) else None
        raise MercuryAPIError(
            "Mercury no devolvio texto en la respuesta. "
            f"finish_reason={finish_reason}, usage={usage}"
        )

    return content


# Alias para mantener compatibilidad con codigo viejo.
def ask_gemini(*args, **kwargs) -> str:
    return ask_mercury(*args, **kwargs)


if __name__ == "__main__":
    print("Escribi tu solicitud para Mercury. Deja vacio y presiona Enter para salir.")

    while True:
        user_prompt = input("\nSolicitud> ").strip()
        if not user_prompt:
            break

        try:
            answer = ask_mercury(user_prompt)
            print(f"\nRespuesta:\n{answer}")
        except MercuryAPIError as error:
            print(f"\nError: {error}")
