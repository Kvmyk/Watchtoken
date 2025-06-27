# 🕐 WatchToken - Struktura Projektu

## 📁 Struktura katalogów

```
watchtoken/
├── 📁 watchtoken/                 # Główny pakiet biblioteki
│   ├── 📄 __init__.py            # Eksporty publiczne API
│   ├── 📄 counter.py             # Główna klasa TokenCounter
│   ├── 📄 models.py              # Konfiguracje modeli i ceny
│   ├── 📄 exceptions.py          # Niestandardowe wyjątki
│   ├── 📄 loggers.py             # System logowania
│   ├── 📄 utils.py               # Funkcje pomocnicze
│   └── 📁 adapters/              # Adaptery dla różnych modeli
│       ├── 📄 __init__.py        # Bazowy adapter (BaseAdapter)
│       ├── 📄 openai.py          # Adapter OpenAI (tiktoken)
│       ├── 📄 anthropic.py       # Adapter Anthropic (estymacja)
│       ├── 📄 google.py          # Adapter Google (estymacja)
│       └── 📄 mistral.py         # Adapter Mistral (SentencePiece)
├── 📁 tests/                     # Testy jednostkowe
│   └── 📄 test_watchtoken.py     # Główne testy
├── 📁 examples/                  # Przykłady użycia
│   ├── 📄 basic_examples.py      # Podstawowe przykłady
│   └── 📄 advanced_examples.py   # Zaawansowane przykłady
├── 📄 demo.py                    # Kompleksowe demo
├── 📄 README.md                  # Dokumentacja główna
├── 📄 CONTRIBUTING.md            # Przewodnik dla współtwórców
├── 📄 LICENSE                    # Licencja MIT
├── 📄 pyproject.toml             # Konfiguracja projektu i zależności
├── 📄 requirements-dev.txt       # Zależności deweloperskie
├── 📄 MANIFEST.in                # Manifest do dystrybucji
└── 📄 .gitignore                 # Pliki ignorowane przez Git
```

## 🚀 Główne komponenty

### 1. **TokenCounter** (główna klasa)
- **Lokalizacja**: `watchtoken/counter.py`
- **Funkcja**: Główny interfejs do liczenia tokenów i zarządzania limitami
- **Możliwości**:
  - Liczenie tokenów dla różnych modeli
  - Sprawdzanie limitów z callbackami
  - Estymacja kosztów
  - Automatyczne logowanie
  - Rejestracja własnych adapterów

### 2. **System Adapterów**
- **Lokalizacja**: `watchtoken/adapters/`
- **Funkcja**: Modularna architektura dla różnych tokenizerów
- **Adaptery**:
  - `OpenAIAdapter`: tiktoken dla precyzyjnej tokenizacji
  - `AnthropicAdapter`: estymacja dla Claude
  - `GoogleAdapter`: estymacja dla Gemini
  - `MistralAdapter`: SentencePiece (opcjonalne)

### 3. **Konfiguracje Modeli**
- **Lokalizacja**: `watchtoken/models.py`
- **Funkcja**: Centralna baza danych modeli z cenami
- **Zawiera**: 12+ predefiniowanych modeli z aktualnymi cenami

### 4. **System Logowania**
- **Lokalizacja**: `watchtoken/loggers.py`
- **Typy**:
  - `FileLogger`: JSON logs
  - `ConsoleLogger`: Wyjście na konsolę
  - `MultiLogger`: Kombinacja loggerów

### 5. **Obsługa Błędów**
- **Lokalizacja**: `watchtoken/exceptions.py`
- **Wyjątki**:
  - `TokenLimitExceededError`
  - `UnsupportedModelError`
  - `TokenizerError`
  - `ConfigurationError`

## 🎯 Główne funkcje biblioteki

### ✅ Zaimplementowane
- [x] **Obsługa 12+ modeli** (OpenAI, Anthropic, Google, Mistral)
- [x] **Precyzyjna tokenizacja** dla OpenAI (tiktoken)
- [x] **Inteligentna estymacja** dla innych modeli
- [x] **Elastyczne limity** z callbackami
- [x] **Estymacja kosztów** z aktualnymi cenami
- [x] **System logowania** (plik/konsola/multi)
- [x] **Modularna architektura** (łatwa rozbudowa)
- [x] **Pełne typowanie** (mypy compatible)
- [x] **Obsługa błędów** z opisowymi komunikatami
- [x] **Testy jednostkowe** (pytest)
- [x] **Przykłady użycia** (basic + advanced)
- [x] **Dokumentacja** (README + CONTRIBUTING)

### 🔄 API Overview

```python
from watchtoken import TokenCounter, FileLogger

# Podstawowe użycie
tc = TokenCounter("gpt-4-turbo", limit=8000)
tokens = tc.count("Hello world!")
cost = tc.estimate_cost("Hello world!", output_tokens=50)

# Z logowaniem
logger = FileLogger("usage.log")
tc = TokenCounter("gpt-4", logger=logger, auto_log=True)

# Z callbackiem
def on_limit(tokens, limit, model):
    print(f"Przekroczono limit: {tokens} > {limit}")

tc = TokenCounter("gpt-3.5-turbo", limit=1000, on_limit_exceeded=on_limit)

# Własny adapter
from watchtoken.adapters import BaseAdapter
TokenCounter.register_adapter("my-model", MyAdapter)
```

## 🛠️ Rozwój i testowanie

### Instalacja deweloperska
```bash
pip install -e .[dev]
```

### Uruchomienie testów
```bash
pytest                    # Wszystkie testy
pytest -v                 # Verbose mode
pytest --cov=watchtoken   # Z coverage
```

### Formatowanie kodu
```bash
black watchtoken tests
isort watchtoken tests
flake8 watchtoken tests
mypy watchtoken
```

### Przykłady
```bash
python examples/basic_examples.py      # Podstawowe przykłady
python examples/advanced_examples.py   # Zaawansowane funkcje
python demo.py                         # Pełne demo
```

## 📊 Wsparcie dla modeli

| Provider | Model | Tokenizer | Status |
|----------|-------|-----------|--------|
| **OpenAI** | gpt-3.5-turbo, gpt-4, gpt-4-turbo | tiktoken | ✅ |
| **Anthropic** | claude-3-sonnet, claude-3-opus, claude-3-haiku | Estymacja | ✅ |
| **Google** | gemini-pro, gemini-pro-vision | Estymacja | ✅ |
| **Mistral** | mistral-7b, mixtral-8x7b | SentencePiece | 🚧 |
| **Custom** | Własne modele | Plugin API | ✅ |

## 🎯 Roadmapa

### v0.2.0 (Planowane)
- [ ] CLI interface
- [ ] Więcej modeli (LLaMA, PaLM)
- [ ] Asynchroniczne API
- [ ] Cache dla tokenizerów

### v0.3.0 (Przyszłość)
- [ ] Integracje (LangChain, LlamaIndex)
- [ ] Monitoring dashboard
- [ ] API rate limiting
- [ ] Batch processing optimizations

## 📝 Licencja i wkład

- **Licencja**: MIT
- **Współpraca**: Zobacz `CONTRIBUTING.md`
- **Issues**: GitHub Issues
- **Dokumentacja**: README.md

---

**WatchToken** - Kontroluj swoje tokeny, zanim one kontrolują Twój budżet! 💰
