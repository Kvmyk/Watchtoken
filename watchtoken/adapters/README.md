# Adaptery WatchToken

Ten katalog zawiera adaptery dla różnych modeli językowych. Każdy adapter implementuje interfejs `BaseAdapter` i zapewnia specyficzną dla modelu tokenizację oraz informacje o kosztach.

## 🏗️ Dostępne adaptery

### 🤖 OpenAI Adapter (`openai.py`)
- **Modele**: gpt-3.5-turbo, gpt-4, gpt-4-turbo, gpt-4-32k
- **Tokenizer**: tiktoken (precyzyjny)
- **Zależności**: `tiktoken>=0.5.0`
- **Status**: ✅ Pełne wsparcie

```python
# Automatycznie używany dla modeli OpenAI
tc = TokenCounter("gpt-4-turbo")
```

### 🎭 Anthropic Adapter (`anthropic.py`) 
- **Modele**: claude-3-sonnet, claude-3-opus, claude-3-haiku
- **Tokenizer**: Estymacja (word + punctuation based)
- **Zależności**: Brak
- **Status**: ✅ Estymacja (~95% dokładność)

```python
tc = TokenCounter("claude-3-sonnet")
```

### 🧠 Google Adapter (`google.py`)
- **Modele**: gemini-2.5-pro, gemini-2.5-flash, gemini-2.5-flash-lite, gemini-1.5-pro
- **Tokenizer**: Estymacja (character based z adjustmentami)
- **Zależności**: Brak  
- **Status**: ✅ Estymacja (~90% dokładność)

```python
tc = TokenCounter("gemini-2.5-pro")
```

### ⚡ Mistral Adapter (`mistral.py`)
- **Modele**: mistral-7b, mixtral-8x7b
- **Tokenizer**: SentencePiece (opcjonalnie) lub estymacja
- **Zależności**: `sentencepiece>=0.1.99` (opcjonalne)
- **Status**: 🚧 Beta (estymacja działa, SentencePiece wymaga modelu)

```python
tc = TokenCounter("mistral-7b")
# lub z SentencePiece:
tc = TokenCounter("mistral-7b")  # adapter automatycznie spróbuje użyć SP
```

## 🔧 Tworzenie własnego adaptera

### 1. Implementacja BaseAdapter

```python
from watchtoken.adapters import BaseAdapter
from typing import Tuple

class MyCustomAdapter(BaseAdapter):
    def __init__(self, model_name: str) -> None:
        super().__init__(model_name)
        # Inicjalizacja specyficzna dla modelu
    
    def count_tokens(self, text: str) -> int:
        """Zlicz tokeny w tekście."""
        # Twoja implementacja tokenizacji
        return len(text.split())  # Przykład
    
    def get_cost_per_token(self) -> Tuple[float, float]:
        """Zwróć (input_cost, output_cost) per token."""
        return (0.001, 0.002)  # Przykład
    
    def get_context_length(self) -> int:
        """Maksymalna długość kontekstu."""
        return 4096  # Przykład
```

### 2. Rejestracja adaptera

```python
from watchtoken import TokenCounter
from watchtoken.models import ModelConfig, ModelProvider, add_model_config

# Dodaj konfigurację modelu
add_model_config("my-model", ModelConfig(
    name="my-model",
    provider=ModelProvider.CUSTOM,
    context_length=4096,
    input_cost_per_token=0.001,
    output_cost_per_token=0.002
))

# Zarejestruj adapter
TokenCounter.register_adapter("my-model", MyCustomAdapter)

# Użycie
tc = TokenCounter("my-model")
```

### 3. Przykład z zewnętrznym tokenizerem

```python
class HuggingFaceAdapter(BaseAdapter):
    def __init__(self, model_name: str, tokenizer_name: str = None):
        super().__init__(model_name)
        try:
            from transformers import AutoTokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                tokenizer_name or model_name
            )
        except ImportError:
            raise TokenizerError(
                "transformers required: pip install transformers", 
                model_name
            )
    
    def count_tokens(self, text: str) -> int:
        tokens = self.tokenizer.encode(text)
        return len(tokens)
    
    def get_cost_per_token(self) -> Tuple[float, float]:
        # Pobierz z konfiguracji modelu
        config = get_model_config(self.model_name)
        return (config.input_cost_per_token, config.output_cost_per_token)
```

## 📊 Dokładność estymacji

| Adapter | Typ tokenizera | Dokładność | Notatki |
|---------|---------------|------------|---------|
| OpenAI | tiktoken | ~100% | Oficjalny tokenizer |
| Anthropic | Estymacja | ~95% | Word + punctuation based |
| Google | Estymacja | ~90% | Character based z adjustmentami |
| Mistral | SentencePiece/Est. | ~85-95% | Zależy od dostępności modelu SP |

## 🔍 Debugowanie adapterów

```python
from watchtoken import TokenCounter

tc = TokenCounter("your-model")

# Sprawdź informacje o modelu
info = tc.get_model_info()
print(f"Model: {info['model']}")
print(f"Provider: {info['provider']}")
print(f"Tokenizer: {info['tokenizer_type']}")

# Test tokenizacji
test_text = "Hello world!"
tokens = tc.count(test_text)
print(f"'{test_text}' -> {tokens} tokens")

# Test kosztów
cost = tc.estimate_cost(test_text, output_tokens=10)
print(f"Cost: ${cost:.6f}")
```

## 🚧 Przyszłe adaptery

- **LLaMA/Alpaca**: Planowane w v0.2.0
- **PaLM**: Planowane w v0.2.0  
- **Cohere**: Rozważane
- **AI21**: Rozważane

## 🤝 Współpraca

Chcesz dodać adapter dla nowego modelu? Zobacz [CONTRIBUTING.md](../CONTRIBUTING.md) dla szczegółów!

### Checklist dla nowego adaptera:
- [ ] Implementuje `BaseAdapter`
- [ ] Ma testy jednostkowe
- [ ] Dokumentacja w README
- [ ] Obsługa błędów z graceful degradation
- [ ] Aktualne ceny w `models.py`
