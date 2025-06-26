# tests/unit/test_product_context.py

from unittest.mock import patch
import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from services.product_context import ProductContextProvider

def test_generate_context_from_products():
    # Mock DB
    with patch('services.product_context.db') as mock_db:
        mock_db.products.find.return_value = [
            {
                "name": "Product A",
                "description": "Description A",
                "price": 100,
                "tags": ["tech", "sale"]
            }
        ]
        
        context_provider = ProductContextProvider()
        result = context_provider.fetch_product_context()
        
        assert "Product A" in result
        assert "Description A" in result
        assert "$100" in result
