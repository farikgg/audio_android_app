from functools import lru_cache

from src.infrastructure.groq import GroqAnalyzer, GroqTranscriber


@lru_cache
def get_groq_analyzer() -> GroqAnalyzer:
    return GroqAnalyzer()

@lru_cache
def get_groq_transcriber() -> GroqTranscriber:
    return GroqTranscriber()
