"""
Szybki start z WatchToken - minimalistyczny przykład.
"""

def quick_start_example():
    """5-minutowy tutorial WatchToken."""
    print("🕐 WatchToken - Szybki start")
    print("=" * 30)
    
    # Import biblioteki
    from watchtoken import TokenCounter
    
    # 1. Podstawowe liczenie tokenów
    print("\n1️⃣ Podstawowe liczenie tokenów:")
    tc = TokenCounter("gpt-3.5-turbo")
    
    prompt = "Napisz krótkie streszczenie książki 'Lalka' Bolesława Prusa."
    tokens = tc.count(prompt)
    print(f"   Prompt: '{prompt}'")
    print(f"   Tokeny: {tokens}")
    
    # 2. Sprawdzanie limitów
    print("\n2️⃣ Sprawdzanie limitów:")
    tc_limited = TokenCounter("gpt-3.5-turbo", limit=20)
    
    if tc_limited.is_over(prompt):
        print(f"   ❌ Prompt przekracza limit {tc_limited.limit} tokenów")
        remaining = tc_limited.get_remaining_tokens("")
        print(f"   💡 Dostępne tokeny: {remaining}")
    else:
        print(f"   ✅ Prompt mieści się w limicie")
    
    # 3. Estymacja kosztów
    print("\n3️⃣ Estymacja kosztów:")
    cost = tc.estimate_cost(prompt, output_tokens=100)
    print(f"   Szacowany koszt (100 tokenów odpowiedzi): ${cost:.6f}")
    
    # 4. Porównanie modeli
    print("\n4️⃣ Porównanie modeli dla tego samego zadania:")
    models = ["gpt-3.5-turbo", "gpt-4-turbo", "claude-3-sonnet"]
    
    print(f"   {'Model':<15} {'Tokeny':<8} {'Koszt':<12}")
    print("   " + "-" * 35)
    
    for model in models:
        try:
            tc_model = TokenCounter(model)
            model_tokens = tc_model.count(prompt)
            model_cost = tc_model.estimate_cost(prompt, output_tokens=100)
            print(f"   {model:<15} {model_tokens:<8} ${model_cost:<11.6f}")
        except Exception as e:
            print(f"   {model:<15} Error: {str(e)[:20]}")
    
    # 5. Callback przy przekroczeniu
    print("\n5️⃣ Ostrzeżenia przy przekroczeniu limitu:")
    
    def alert_callback(tokens, limit, model):
        print(f"   🚨 UWAGA: {model} przekroczył limit ({tokens} > {limit})")
    
    tc_callback = TokenCounter(
        "gpt-3.5-turbo", 
        limit=10, 
        on_limit_exceeded=alert_callback
    )
    
    long_prompt = "To jest bardzo długi prompt, który na pewno przekroczy ustalony limit tokenów dla tego przykładu demonstracyjnego."
    tc_callback.check_limit(long_prompt)
    
    print("\n✅ Gotowe! Teraz możesz używać WatchToken w swoich projektach.")
    print("\n📚 Więcej przykładów:")
    print("   - python examples/basic_examples.py")
    print("   - python examples/advanced_examples.py") 
    print("   - python demo.py")


if __name__ == "__main__":
    try:
        quick_start_example()
    except ImportError:
        print("❌ Błąd: Zainstaluj bibliotekę: pip install -e .")
    except Exception as e:
        print(f"❌ Błąd: {e}")
