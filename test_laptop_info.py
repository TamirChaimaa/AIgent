from services.product_context import ProductContextProvider
from services.ai_services import AiService
import json

def test_laptop_information():
    """Test how laptop information is displayed"""
    
    print("🖥️ TESTING LAPTOP INFORMATION DISPLAY")
    print("=" * 50)
    
    # Test 1: Get product context to see how laptops are described
    print("\n1. 📋 PRODUCT CONTEXT (How AI sees laptops):")
    print("-" * 30)
    context = ProductContextProvider.fetch_product_context()
    
    # Find laptop entries in context
    lines = context.split('\n')
    laptop_lines = [line for line in lines if 'laptop' in line.lower() or 'macbook' in line.lower() or 'Laptops' in line]
    
    for line in laptop_lines[:3]:  # Show first 3 laptops
        print(line)
    
    # Test 2: Test AI recommendation for laptops
    print("\n2. 🤖 AI RECOMMENDATION TEST:")
    print("-" * 30)
    
    ai_service = AiService()
    
    # Test different laptop queries
    test_questions = [
        "Show me laptops under $1000",
        "What are the best programming laptops?",
        "I need a laptop with good battery life"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\nQuestion {i}: {question}")
        try:
            response = ai_service.ask_question(question)
            print(f"AI Response: {response['message']}")
            print("Recommended Products:")
            for product in response['products']:
                print(f"  📱 {product['name']} - ${product['price']}")
                if product.get('brand'):
                    print(f"     Brand: {product['brand']}")
                if product.get('specs'):
                    specs = product['specs']
                    if specs.get('processor'):
                        print(f"     CPU: {specs['processor']}")
                    if specs.get('ram'):
                        print(f"     RAM: {specs['ram']}")
                    if specs.get('storage'):
                        print(f"     Storage: {specs['storage']}")
                    if specs.get('screen_size'):
                        print(f"     Screen: {specs['screen_size']}")
                    if specs.get('battery_life'):
                        print(f"     Battery: {specs['battery_life']}")
                    if specs.get('weight'):
                        print(f"     Weight: {specs['weight']}")
                    if specs.get('os'):
                        print(f"     OS: {specs['os']}")
                if product.get('rating'):
                    print(f"     Rating: {product['rating']}/5 ({product.get('reviews_count', 0)} reviews)")
                if product.get('warranty'):
                    print(f"     Warranty: {product['warranty']}")
                if product.get('available') == False:
                    print(f"     Status: Out of Stock")
                print()
        except Exception as e:
            print(f"Error: {e}")
    
    # Test 3: Show full product details structure
    print("\n3. 📊 FULL PRODUCT DETAILS STRUCTURE:")
    print("-" * 30)
    
    # Get a sample laptop
    sample_laptops = ProductContextProvider.get_products_by_names(["MacBook Air M2"])
    if sample_laptops:
        laptop = sample_laptops[0]
        print("Sample laptop JSON structure:")
        print(json.dumps(laptop, indent=2, default=str))
    
    print("\n✅ TEST COMPLETED!")

if __name__ == "__main__":
    test_laptop_information() 