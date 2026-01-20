from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx


class OllamaError(RuntimeError):
    pass

@dataclass(frozen=True)
class OllamaAsyncClient:
    base_url: str = "http://localhost:11434"
    model: str = "mistral"
    timeout: float = 120.0

    def _url(self, path: str) -> str:
        return f"{self.base_url.rstrip('/')}{path}"

    async def health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                r = await client.get(self._url("/api/tags"))
                return r.status_code == 200
        except httpx.HTTPError:
            return False

    async def list_models(self) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                r = await client.get(self._url("/api/tags"))
                r.raise_for_status()
                return r.json()
        except httpx.HTTPError as e:
            raise OllamaError(f"Falha ao listar modelos: {e}") from e

    async def generate(
        self,
        prompt: str,
        *,
        model: Optional[str] = None,
        stream: bool = False,
        options: Optional[Dict[str, Any]] = None,
        system: Optional[str] = None,
    ) -> str:
        payload: Dict[str, Any] = {
            "model": model or self.model,
            "prompt": prompt,
            "stream": stream,
        }
        if options:
            payload["options"] = options
        if system:
            payload["system"] = system

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                r = await client.post(self._url("/api/generate"), json=payload)
                r.raise_for_status()
                data = r.json()
        except httpx.TimeoutException as e:
            raise OllamaError(f"Timeout chamando Ollama: {e}") from e
        except httpx.HTTPStatusError as e:
            body = e.response.text
            raise OllamaError(f"Erro HTTP {e.response.status_code}: {body}") from e
        except httpx.HTTPError as e:
            raise OllamaError(f"Erro de rede chamando Ollama: {e}") from e
        except ValueError as e:
            raise OllamaError(f"Resposta não é JSON válido: {e}") from e

        if "error" in data:
            raise OllamaError(f"Ollama retornou erro: {data['error']}")

        return (data.get("response") or "").strip()
