from groq import AsyncGroq
from groq.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from src.app.config import get_settings


settings = get_settings().groq_settings


class GroqAnalyzer:
    def __init__(self) -> None:
        self.model = settings.llm_model
        self.client = AsyncGroq(api_key=settings.api_key)

    async def analyze(self, system: str, prompt: str) -> str:
        system_role: ChatCompletionSystemMessageParam = {
            "role": "system",
            "content": system
        }

        user_role: ChatCompletionUserMessageParam = {
            "role": "user",
            "content": prompt,
        }

        answer = await self.client.chat.completions.create(
            messages=[system_role, user_role],
            model=self.model,
        )

        return answer.choices[0].message.content


class GroqTranscriber:
    def __init__(self) -> None:
        self.model = settings.whisper_model
        self.client = AsyncGroq(api_key=settings.api_key)

    async def transcribe(self, file: tuple[str, bytes]) -> str:
        audio_text = await self.client.audio.transcriptions.create(
            model=self.model,
            file=file,
        )

        return audio_text.text
