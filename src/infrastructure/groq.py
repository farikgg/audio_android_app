import json

from groq import AsyncGroq
from groq.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

from src.app.config import get_settings
from src.core.constants import AI_TEMPERATURE, ANSWER_FORMAT
from src.core.prompts import SYSTEM_ANALYSIS, USER_ANALYSIS_TEMPLATE

settings = get_settings().groq_settings


class GroqAnalyzer:
    def __init__(self) -> None:
        self.model = settings.llm_model
        self.client = AsyncGroq(api_key=settings.api_key)
        self.json_format = ANSWER_FORMAT

    async def analyze(self, transcript_text: str) -> dict:

        user_text = USER_ANALYSIS_TEMPLATE.format(transcript = transcript_text)

        system_role: ChatCompletionSystemMessageParam = {
            "role": "system",
            "content": SYSTEM_ANALYSIS
        }

        user_role: ChatCompletionUserMessageParam = {
            "role": "user",
            "content": user_text,
        }

        answer = await self.client.chat.completions.create(
            messages=[system_role, user_role],
            model=self.model,
            response_format=self.json_format,
            temperature=AI_TEMPERATURE,
        )

        result = json.loads(answer.choices[0].message.content)

        return result


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
