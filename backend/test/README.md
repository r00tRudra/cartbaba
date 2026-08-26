# Testing Guide for CartBaba Agents

## 📋 Overview

The `test.py` file contains a comprehensive testing suite for all CartBaba agents and functions. It tests:

1. **Search Products Function** - API calls and fallback mechanism
2. **Ranking Function** - Semantic similarity scoring
3. **Intent Agent** - LLM-based intent parsing (requires GROQ API key)
4. **Complete Pipeline** - Full `run_cartbaba()` workflow
5. **Error Handling** - Edge cases and robustness

## 🚀 Running the Tests

### Step 1: Setup Environment

```bash
# Navigate to backend directory
cd c:\backend\fastapi\cartbaba\backend

# Ensure .env file has GROQ_API_KEY
# Edit .env and add your key:
# GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxx
```

### Step 2: Install Dependencies (if not already done)

```bash
pip install -r requirements.txt
```

### Step 3: Run All Tests

```bash
# From backend directory
python test/test.py
```

Or with more verbosity:

```bash
python -u test/test.py  # Unbuffered output
```

## 📊 Test Breakdown

### ✅ TEST 1: Search Products Function
```
Tests: search_products() function
Checks:
  - Can fetch products from dummyjson API
  - Returns correct product structure (name, price, rating, image)
  - Filters by max_price if provided
  - Falls back to synthetic data if API fails
  
Expected Output:
  ✅ Found X products
  ✅ Product structure is correct
  Sample: {name: ..., price: ..., rating: ..., image: ...}
```

### ✅ TEST 2: Ranking Function
```
Tests: rank_products() function
Checks:
  - Calculates semantic similarity scores
  - Combines similarity + rating (70/30 split)
  - Products are sorted by score (highest first)
  - Score field is added to each product
  
Expected Output:
  ✅ Ranked X products
  ✅ Score field added correctly
  Top 3 ranked products with scores
```

### ✅ TEST 3: Intent Agent
```
Tests: intent_agent (LLM-based)
Checks:
  - Parses natural language queries
  - Extracts: category, max_price, gender, use_case
  - Returns valid JSON
  - Handles various query formats
  
Expected Output:
  ✅ Intent parsed successfully
  Parsed intent: {category: ..., max_price: ..., ...}
  
NOTE: Requires valid GROQ_API_KEY in .env
```

### ✅ TEST 4: Complete Pipeline
```
Tests: run_cartbaba() function (full workflow)
Checks:
  - All components work together
  - Results contain: query, intent, products, final
  - Products are ranked and relevant
  - Final recommendations are generated
  
Expected Output:
  ✅ Pipeline executed successfully
  Results:
    Query: ...
    Intent: {...}
    Products returned: X
    Top 3: [...]
    Final Recommendation: ...
```

### ✅ TEST 5: Error Handling
```
Tests: Edge cases and error scenarios
Checks:
  - Empty intent handling
  - Non-existent categories
  - Invalid price ranges
  - Fallback mechanisms work
  
Expected Output:
  All edge cases handled gracefully
  No crashes on unexpected input
```

## 📈 Understanding Output

### Colors Used:
- 🟦 **BLUE** - Information messages
- 🟩 **GREEN** - Success (✅)
- 🟥 **RED** - Errors (❌)
- 🟨 **YELLOW** - Warnings (⚠️)
- 🟦 **CYAN** - Section headers

### Sample Output:
```
════════════════════════════════════════════════════════════
                    🤖 CartBaba Agent Testing Suite
════════════════════════════════════════════════════════════

➜ TEST 1: Search Products Function

Test Case 1:
  Intent: {'category': 'shoes', 'max_price': 5000, 'gender': 'men', 'use_case': 'running'}
✅ Found 8 products
✅ Product structure is correct
  Sample: {'name': 'Nike Running Shoes', 'price': 4999.0, 'rating': 4.5, 'image': 'https://...'}
```

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'app'`
**Solution:** Ensure you're running from the `backend` directory:
```bash
cd c:\backend\fastapi\cartbaba\backend
python test/test.py
```

### Issue: `GROQ_API_KEY not found`
**Solution:** Check `.env` file has the key:
```bash
# Ensure .env contains:
GROQ_API_KEY=gsk_xxxxxx
```

### Issue: `No products returned` (Test 1)
**Solution:** Could be API temporarily down. The fallback should kick in. If not:
- Check internet connection
- Try manual API call: `https://dummyjson.com/products/search?q=shoes`
- Check if dummyjson.com is accessible

### Issue: `Connection timeout` (Test 3)
**Solution:** LLM requests might be slow. Groq usually responds in 1-3 seconds.
- Check GROQ_API_KEY is valid
- Check internet connection
- Try running test again

## 📝 Interpretation Guide

| Result | Meaning | Action |
|--------|---------|--------|
| ✅ All tests pass | System working perfectly | Ready for production |
| ⚠️ Some warnings | Minor issues (API slow, fallback used) | Monitor, but OK |
| ❌ Test failures | Component broken | Fix the specific test |
| 🔴 Runtime errors | Dependency or config issue | Check logs, reinstall deps |

## 🔧 Customizing Tests

### To test with different queries:
Edit the test case lists in `test.py`:

```python
test_queries = [
    "running shoes under 5000",  # Add your query here
    "best phones",
    "formal shoes for women"
]
```

### To skip certain tests:
Comment out in `main()`:

```python
def main():
    print_header("🤖 CartBaba Agent Testing Suite")
    
    # test_search_products()     # Skip this
    test_ranking()              # Run this
    test_intent_agent()
    # test_complete_pipeline()  # Skip this
    test_error_handling()
```

## 📊 Performance Benchmarks

Expected execution times:
- **Test 1** (Search): 2-3 seconds
- **Test 2** (Ranking): 1-2 seconds
- **Test 3** (Intent Agent): 5-10 seconds (LLM call)
- **Test 4** (Pipeline): 10-15 seconds (full flow)
- **Test 5** (Error Handling): 2-3 seconds

**Total:** ~20-35 seconds for full test suite

## ✨ What Success Looks Like

```
✅ Found X products
✅ Product structure is correct
✅ Ranked X products
✅ Score field added correctly
✅ Intent parsed successfully
✅ Pipeline executed successfully
✅ Error handling: Fallback mechanism works

✨ Testing Complete!
```

All agents working → Ready to deploy! 🚀
