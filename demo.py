#!/usr/bin/env python3
"""
Demo script dla biblioteki WatchToken.
Pokazuje praktyczne przypadki użycia w rzeczywistych scenariuszach.
"""

from watchtoken import TokenCounter, FileLogger
from watchtoken.utils import get_model_summary, calculate_batch_cost
import json


def main():
    """Główna demonstracja funkcjonalności WatchToken."""
    print("🕐 WatchToken Demo - Praktyczne zastosowania")
    print("=" * 50)
    
    # 1. Analiza kosztów dla różnych zadań
    analyze_task_costs()
    
    # 2. Optymalizacja promptów
    optimize_prompts()
    
    # 3. Monitorowanie budżetu
    budget_monitoring()
    
    # 4. Porównanie modeli dla konkretnego zadania
    model_selection()


def analyze_task_costs():
    """Analiza kosztów dla typowych zadań LLM."""
    print("\n📊 Analiza kosztów typowych zadań")
    print("-" * 30)
    
    tasks = {
        "Tłumaczenie": {
            "prompt": "Przetłumacz następujący tekst na język angielski: 'Sztuczna inteligencja rewolucjonizuje sposób, w jaki pracujemy i żyjemy.'",
            "output_tokens": 30
        },
        "Streszczenie": {
            "prompt": "Napisz streszczenie następującego artykułu w 3 zdaniach: [artykuł o AI o długości 1000 słów]",
            "output_tokens": 100
        },
        "Generowanie kodu": {
            "prompt": "Napisz funkcję Python, która sortuje listę słowników według wybranego klucza, z obsługą błędów.",
            "output_tokens": 200
        },
        "Analiza sentymentu": {
            "prompt": "Przeanalizuj sentyment następujących 10 opinii klientów i podsumuj wyniki.",
            "output_tokens": 150
        }
    }
    
    tc = TokenCounter("gpt-4-turbo")
    
    print(f"{'Zadanie':<20} {'Input tokens':<12} {'Output tokens':<13} {'Koszt':<10}")
    print("-" * 60)
    
    total_cost = 0
    for task_name, task_data in tasks.items():
        input_tokens = tc.count(task_data["prompt"])
        cost = tc.estimate_cost(task_data["prompt"], task_data["output_tokens"])
        total_cost += cost
        
        print(f"{task_name:<20} {input_tokens:<12} {task_data['output_tokens']:<13} ${cost:<9.6f}")
    
    print("-" * 60)
    print(f"{'RAZEM':<20} {'':<12} {'':<13} ${total_cost:<9.6f}")


def optimize_prompts():
    """Demonstracja optymalizacji promptów."""
    print("\n🔧 Optymalizacja promptów")
    print("-" * 25)
    
    # Różne wersje tego samego zadania
    versions = {
        "Pełna wersja": """
        Proszę o szczegółową analizę następującego fragmentu kodu Python, 
        uwzględniając następujące aspekty:
        1. Czytelność i styl kodowania
        2. Wydajność algorytmiczna  
        3. Możliwe optymalizacje
        4. Potencjalne błędy lub problemy
        5. Zgodność z PEP 8
        6. Sugestie ulepszeń
        
        Kod do analizy:
        def sort_list(data):
            return sorted(data)
        """,
        
        "Zoptymalizowana": """
        Przeanalizuj kod Python pod kątem: czytelności, wydajności, błędów, PEP 8 i ulepszeń:
        
        def sort_list(data):
            return sorted(data)
        """
    }
    
    tc = TokenCounter("gpt-4-turbo")
    
    print("Porównanie wersji promptu:")
    for version, prompt in versions.items():
        tokens = tc.count(prompt.strip())
        cost = tc.estimate_cost(prompt.strip(), output_tokens=300)
        
        print(f"\n{version}:")
        print(f"  Tokeny: {tokens}")
        print(f"  Koszt: ${cost:.6f}")
    
    # Obliczenie oszczędności
    full_cost = tc.estimate_cost(versions["Pełna wersja"].strip(), output_tokens=300)
    opt_cost = tc.estimate_cost(versions["Zoptymalizowana"].strip(), output_tokens=300)
    savings = full_cost - opt_cost
    savings_percent = (savings / full_cost) * 100
    
    print(f"\n💰 Oszczędności: ${savings:.6f} ({savings_percent:.1f}%)")


def budget_monitoring():
    """Demonstracja monitorowania budżetu."""
    print("\n💰 Monitorowanie budżetu")
    print("-" * 22)
    
    daily_budget = 5.00  # $5 dziennie
    current_usage = 0.0
    
    # Symulacja operacji w ciągu dnia
    operations = [
        ("Analiza dokumentu prawnego", "gpt-4-turbo", 500, 1000),
        ("Tłumaczenie artykułu", "gpt-3.5-turbo", 300, 400),
        ("Generowanie opisów produktów", "gpt-3.5-turbo", 200, 600),
        ("Odpowiedzi na pytania klientów", "gpt-3.5-turbo", 150, 200),
        ("Podsumowanie raportu", "claude-3-sonnet", 400, 300),
    ]
    
    logger = FileLogger("budget_log.json")
    
    print(f"Dzienny budżet: ${daily_budget:.2f}")
    print("\nOperacje:")
    
    for operation, model, input_est, output_est in operations:
        tc = TokenCounter(model, logger=logger)
        
        # Symulacja prompt (używamy estymacji tokenów)
        mock_prompt = "x" * (input_est * 4)  # ~4 znaki na token
        cost = tc.estimate_cost(mock_prompt, output_tokens=output_est)
        
        current_usage += cost
        remaining = daily_budget - current_usage
        
        status = "✅" if remaining > 0 else "❌"
        
        print(f"  {status} {operation[:30]:<30} ({model}) ${cost:.4f}")
        print(f"     Użyto: ${current_usage:.4f} | Pozostało: ${remaining:.4f}")
        
        if remaining <= 0:
            print(f"     ⚠️ Przekroczono budżet dzienny!")
            break
        elif remaining < 1.0:
            print(f"     ⚠️ Mało pozostało do limitu!")


def model_selection():
    """Pomoc w wyborze najlepszego modelu dla zadania."""
    print("\n🎯 Wybór modelu dla zadania")
    print("-" * 27)
    
    task_prompt = "Napisz szczegółową recenzję filmu 'Inception' uwzględniając fabułę, reżyserię, muzykę i efekty specjalne."
    expected_output = 800  # tokenów
    
    models_to_test = ["gpt-3.5-turbo", "gpt-4-turbo", "claude-3-sonnet", "claude-3-haiku"]
    
    print(f"Zadanie: Recenzja filmu (szacowane {expected_output} tokenów wyjścia)")
    print(f"{'Model':<20} {'Input tokens':<12} {'Koszt':<10} {'Koszt/1K out':<12}")
    print("-" * 60)
    
    results = []
    for model in models_to_test:
        try:
            tc = TokenCounter(model)
            input_tokens = tc.count(task_prompt)
            cost = tc.estimate_cost(task_prompt, output_tokens=expected_output)
            
            # Koszt na 1000 tokenów wyjścia (dla porównania)
            cost_per_1k = (cost / (input_tokens + expected_output)) * 1000
            
            results.append({
                "model": model,
                "input_tokens": input_tokens,
                "cost": cost,
                "cost_per_1k": cost_per_1k
            })
            
            print(f"{model:<20} {input_tokens:<12} ${cost:<9.6f} ${cost_per_1k:<11.6f}")
            
        except Exception as e:
            print(f"{model:<20} {'Error:':<12} {str(e)[:20]}")
    
    # Rekomendacja
    if results:
        cheapest = min(results, key=lambda x: x["cost"])
        print(f"\n💡 Rekomendacja: {cheapest['model']} (najtańszy: ${cheapest['cost']:.6f})")


def export_model_comparison():
    """Export porównania modeli do JSON."""
    print("\n📄 Export danych o modelach")
    print("-" * 26)
    
    summary = get_model_summary()
    
    # Zapis do pliku
    with open("models_comparison.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("✅ Dane o modelach wyeksportowane do 'models_comparison.json'")
    print(f"Znaleziono {len(summary)} modeli")


if __name__ == "__main__":
    try:
        main()
        export_model_comparison()
        
        print("\n" + "=" * 50)
        print("✅ Demo zakończone pomyślnie!")
        print("\nPliki utworzone:")
        print("  - token_usage.log (podstawowe logowanie)")
        print("  - budget_log.json (monitorowanie budżetu)")
        print("  - models_comparison.json (porównanie modeli)")
        
    except Exception as e:
        print(f"\n❌ Błąd podczas demo: {e}")
        import traceback
        traceback.print_exc()
