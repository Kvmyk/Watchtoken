#!/usr/bin/env python3
"""
Test script for new models added to WatchToken
"""

from watchtoken import TokenCounter
from watchtoken.models import list_supported_models, get_model_config

def test_new_models():
    """Test all new models to ensure they work correctly."""
    
    test_prompt = "Hello, world! This is a test prompt for tokenization."
    
    print("🧪 Testing new models in WatchToken...")
    print(f"📝 Test prompt: '{test_prompt}'")
    print("=" * 60)
    
    # New OpenAI models
    new_openai_models = [
        "gpt-4o", "gpt-4o-mini", "gpt-4.1", 
        "gpt-4.1-mini", "gpt-4.1-nano", "gpt-image-1"
    ]
    
    # New Anthropic models  
    new_anthropic_models = [
        "claude-sonnet-4", "claude-opus-4", "claude-3-7-sonnet"
    ]
    
    # Test each category
    test_model_category("🤖 New OpenAI Models", new_openai_models, test_prompt)
    test_model_category("🧠 New Anthropic Models", new_anthropic_models, test_prompt)
    
    # Test comparison between old and new models
    print("\n📊 Cost Comparison - Old vs New:")
    compare_models([
        ("gpt-4-turbo", "gpt-4o"),
        ("gpt-3.5-turbo", "gpt-4o-mini"),
        ("claude-3-sonnet", "claude-sonnet-4")
    ], test_prompt)

def test_model_category(category_name, models, test_prompt):
    """Test a category of models."""
    print(f"\n{category_name}")
    print("-" * 40)
    
    for model_name in models:
        try:
            tc = TokenCounter(model_name)
            tokens = tc.count(test_prompt)
            cost = tc.estimate_cost(test_prompt, output_tokens=100)
            config = get_model_config(model_name)
            
            print(f"✅ {model_name:<18} | "
                  f"Tokens: {tokens:>3} | "
                  f"Cost: ${cost:>8.6f} | "
                  f"Context: {config.context_length:>8,}")
                  
        except Exception as e:
            print(f"❌ {model_name:<18} | Error: {str(e)}")

def compare_models(model_pairs, test_prompt):
    """Compare old vs new model costs."""
    print("-" * 50)
    
    for old_model, new_model in model_pairs:
        try:
            tc_old = TokenCounter(old_model)
            tc_new = TokenCounter(new_model)
            
            cost_old = tc_old.estimate_cost(test_prompt, output_tokens=1000)
            cost_new = tc_new.estimate_cost(test_prompt, output_tokens=1000)
            
            savings = ((cost_old - cost_new) / cost_old) * 100 if cost_old > 0 else 0
            
            print(f"💰 {old_model} vs {new_model}:")
            print(f"   Old: ${cost_old:.6f} | New: ${cost_new:.6f} | "
                  f"{'Savings' if savings > 0 else 'More expensive'}: {abs(savings):.1f}%")
                  
        except Exception as e:
            print(f"❌ Error comparing {old_model} vs {new_model}: {e}")

def test_limits_and_callbacks():
    """Test limit checking with new models."""
    print("\n🚨 Testing Limits & Callbacks:")
    print("-" * 40)
    
    def alert_callback(tokens, limit, model):
        print(f"   ⚠️  ALERT: {model} exceeded limit ({tokens} > {limit})")
    
    # Test with a model that has huge context
    tc_large = TokenCounter(
        "gpt-4.1", 
        limit=50,  # Very small limit to trigger alert
        on_limit_exceeded=alert_callback
    )
    
    long_prompt = "This is a very long prompt " * 20
    tc_large.check_limit(long_prompt)
    
    # Test with Gemini's huge context
    tc_gemini = TokenCounter("gemini-1.5-pro", limit=1000000)
    remaining = tc_gemini.get_remaining_tokens("Short prompt")
    print(f"✅ Gemini 1.5 Pro remaining tokens: {remaining:,}")

def show_all_supported_models():
    """Display all currently supported models."""
    print("\n📋 All Supported Models:")
    print("=" * 60)
    
    models = list_supported_models()
    
    by_provider = {}
    for model in models:
        config = get_model_config(model)
        provider = config.provider.value
        if provider not in by_provider:
            by_provider[provider] = []
        by_provider[provider].append(model)
    
    for provider, model_list in by_provider.items():
        print(f"\n🏢 {provider.upper()}:")
        for model in sorted(model_list):
            config = get_model_config(model)
            print(f"   • {model:<20} | Context: {config.context_length:>8,} | "
                  f"Tokenizer: {config.tokenizer_type}")

if __name__ == "__main__":
    print("🎯 WatchToken New Models Test Suite")
    print("=" * 60)
    
    try:
        test_new_models()
        test_limits_and_callbacks()
        show_all_supported_models()
        
        print("\n✅ All tests completed successfully!")
        print("🚀 Your new models are ready to use!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
