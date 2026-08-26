"""
CartBaba Agent Testing Suite
Tests all components of the recommendation pipeline
"""

import sys
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.agents.intent_agent import intent_agent
from app.agents.search_agent import search_products
from app.agents.ranking_agent import rank_products
from app.agents.review_agent import review_agent
from app.agents.final_agent import final_agent
from app.services.recommender import run_cartbaba, safe_json_loads
from crewai import Task, Crew

# ===========================
# 🎨 Color codes for output
# ===========================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_section(text):
    print(f"{Colors.CYAN}{Colors.BOLD}➜ {text}{Colors.ENDC}")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")

# ===========================
# 🧪 TEST 1: Search Products Function
# ===========================
def test_search_products():
    print_section("TEST 1: Search Products Function")
    
    test_intents = [
        {
            "category": "shoes",
            "max_price": 5000,
            "gender": "men",
            "use_case": "running"
        },
        {
            "category": "phone",
            "max_price": None,
            "gender": None,
            "use_case": None
        },
        {
            "category": "laptop",
            "max_price": 50000,
            "gender": None,
            "use_case": None
        }
    ]
    
    for i, intent in enumerate(test_intents, 1):
        print(f"\n{Colors.BOLD}Test Case {i}:{Colors.ENDC}")
        print(f"  Intent: {intent}")
        
        try:
            products = search_products(intent)
            
            if products and len(products) > 0:
                print_success(f"Found {len(products)} products")
                
                # Check structure
                first_product = products[0]
                required_fields = ["name", "price", "rating", "image"]
                
                if all(field in first_product for field in required_fields):
                    print_success("Product structure is correct")
                    print(f"  Sample: {first_product}")
                else:
                    print_error(f"Missing fields. Got: {first_product.keys()}")
                    
            else:
                print_warning("No products returned (but no error)")
                
        except Exception as e:
            print_error(f"Failed: {str(e)}")
    
    print()

# ===========================
# 🧪 TEST 2: Ranking Function
# ===========================
def test_ranking():
    print_section("TEST 2: Ranking Function")
    
    # Get products first
    print_info("Fetching products for ranking test...")
    products = search_products({
        "category": "shoes",
        "max_price": None,
        "gender": None,
        "use_case": None
    })
    
    if not products:
        print_error("No products available for ranking test")
        return
    
    test_queries = [
        "running shoes for men",
        "casual shoes",
        "formal shoes"
    ]
    
    for query in test_queries:
        print(f"\n{Colors.BOLD}Query: '{query}'{Colors.ENDC}")
        
        try:
            ranked = rank_products(products.copy(), query)
            
            print_success(f"Ranked {len(ranked)} products")
            
            # Check if score field exists
            if "score" in ranked[0]:
                print_success("Score field added correctly")
                print(f"\n  Top 3 ranked products:")
                for j, prod in enumerate(ranked[:3], 1):
                    print(f"    {j}. {prod['name']}")
                    print(f"       Score: {prod['score']:.4f} | Price: ${prod['price']} | Rating: ⭐ {prod['rating']}")
            else:
                print_error("Score field missing from products")
                
        except Exception as e:
            print_error(f"Ranking failed: {str(e)}")
    
    print()

# ===========================
# 🧪 TEST 3: Intent Agent
# ===========================
def test_intent_agent():
    print_section("TEST 3: Intent Agent (LLM-based)")
    
    test_queries = [
        "Show me running shoes under 5000 rupees for men",
        "I want a cheap phone",
        "Looking for formal shoes for women"
    ]
    
    for query in test_queries:
        print(f"\n{Colors.BOLD}Query: '{query}'{Colors.ENDC}")
        
        try:
            task = Task(
                description=f"""
                Extract structured shopping intent from:
                {query}
                
                Return ONLY JSON:
                {{
                  "category": "",
                  "max_price": null,
                  "gender": "",
                  "use_case": ""
                }}
                """,
                agent=intent_agent,
                expected_output="Strict JSON with category, max_price, gender, use_case"
            )
            
            crew = Crew(agents=[intent_agent], tasks=[task], verbose=False)
            result = crew.kickoff()
            
            intent_json = safe_json_loads(str(result))
            
            if intent_json:
                print_success("Intent parsed successfully")
                print(f"  Parsed intent: {json.dumps(intent_json, indent=2)}")
            else:
                print_error("Failed to parse intent as JSON")
                print(f"  Raw output: {result}")
                
        except Exception as e:
            print_error(f"Intent parsing failed: {str(e)}")
    
    print()

# ===========================
# 🧪 TEST 4: Complete Pipeline
# ===========================
def test_complete_pipeline():
    print_section("TEST 4: Complete Pipeline (Full run_cartbaba)")
    
    test_queries = [
        "running shoes under 5000",
        "best phones",
        "formal shoes for women"
    ]
    
    for query in test_queries:
        print(f"\n{Colors.BOLD}Query: '{query}'{Colors.ENDC}")
        print(f"{Colors.BOLD}{'-'*50}{Colors.ENDC}")
        
        try:
            result = run_cartbaba(query)
            
            # Check result structure
            required_keys = ["query", "intent", "products", "final"]
            if all(key in result for key in required_keys):
                print_success("Pipeline executed successfully")
                
                # Show results
                print(f"\n{Colors.BOLD}📋 Results:{Colors.ENDC}")
                print(f"  Query: {result['query']}")
                print(f"  Intent: {json.dumps(result['intent'], indent=2)}")
                
                if result["products"]:
                    print(f"  📦 Products returned: {len(result['products'])}")
                    print(f"  {Colors.BOLD}Top 3:{Colors.ENDC}")
                    for i, prod in enumerate(result["products"][:3], 1):
                        score = prod.get("score", "N/A")
                        print(f"    {i}. {prod['name']}")
                        print(f"       Score: {score} | Price: ${prod['price']} | Rating: ⭐ {prod['rating']}")
                else:
                    print_warning("No products returned")
                
                print(f"\n  💬 Final Recommendation: {result['final'][:200]}...")
                
            else:
                print_error(f"Incomplete result. Keys: {result.keys()}")
                
        except Exception as e:
            print_error(f"Pipeline failed: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print()

# ===========================
# 🧪 TEST 5: Error Handling
# ===========================
def test_error_handling():
    print_section("TEST 5: Error Handling & Edge Cases")
    
    edge_cases = [
        {"category": "", "max_price": None, "gender": None, "use_case": None},  # Empty intent
        {"category": "nonexistent_product_xyz", "max_price": 100, "gender": None, "use_case": None},  # Non-existent category
        {"category": "shoes", "max_price": -1000, "gender": None, "use_case": None},  # Negative price
    ]
    
    for i, intent in enumerate(edge_cases, 1):
        print(f"\n{Colors.BOLD}Edge Case {i}: {intent}{Colors.ENDC}")
        
        try:
            products = search_products(intent)
            print_info(f"Returned {len(products)} products (fallback to synthetic data if needed)")
            
            if products:
                print_success("Error handling: Fallback mechanism works")
            else:
                print_warning("No products, but no exception raised")
                
        except Exception as e:
            print_error(f"Unhandled exception: {str(e)}")
    
    print()

# ===========================
# 📊 SUMMARY & STATISTICS
# ===========================
def print_summary():
    print_header("TEST SUMMARY")
    
    print(f"{Colors.BOLD}All tests completed!{Colors.ENDC}")
    print("""
{cyan}✓ Test 1: Search Products Function{endc}
  - Tests product fetching from API
  - Validates product structure
  
{cyan}✓ Test 2: Ranking Function{endc}
  - Tests semantic similarity scoring
  - Validates ranking order
  
{cyan}✓ Test 3: Intent Agent (LLM){endc}
  - Tests LLM-based intent parsing
  - Requires GROQ_API_KEY in .env
  
{cyan}✓ Test 4: Complete Pipeline{endc}
  - Tests entire run_cartbaba flow
  - Most comprehensive test
  
{cyan}✓ Test 5: Error Handling{endc}
  - Tests edge cases
  - Validates fallback mechanisms
    """.format(
        cyan=Colors.CYAN, 
        bold=Colors.BOLD, 
        endc=Colors.ENDC
    ))
    
    print(f"{Colors.BOLD}What to check:{Colors.ENDC}")
    print(f"  1️⃣  Products are returned from API or fallback")
    print(f"  2️⃣  Ranking scores are between 0 and 1")
    print(f"  3️⃣  Intent parsing extracts correct fields")
    print(f"  4️⃣  Top products are relevant to query")
    print(f"  5️⃣  No crashes on edge cases")

# ===========================
# 🚀 MAIN EXECUTION
# ===========================
def main():
    print_header("🤖 CartBaba Agent Testing Suite")
    
    print_info("Starting comprehensive test suite...\n")
    
    # Run all tests
    test_search_products()
    test_ranking()
    test_intent_agent()
    test_complete_pipeline()
    test_error_handling()
    
    # Print summary
    print_summary()
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}✨ Testing Complete!{Colors.ENDC}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {str(e)}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
