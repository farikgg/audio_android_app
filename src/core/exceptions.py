class GoogleSheetsError(Exception):
    """Ошибки Google Sheets"""
    pass


class GroqAPIError(Exception):
    """Ошибки Groq API"""
    pass


class GroqAnalyzerError(GroqAPIError):
    """Ошибки Groq анализа"""
    pass


class GroqTranscriberError(GroqAPIError):
    """Ошибки Groq транскрибации"""
    pass


class GoogleSheetsRepositoryError(GoogleSheetsError):
    """Ошибки Google Sheets Repository"""
    pass
