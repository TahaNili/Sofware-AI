"""
Web browser automation and interaction for Sofware-AI
"""

import asyncio
from typing import Dict, List, Optional, Any
from playwright.async_api import async_playwright, Browser, Page
import json
import re
from urllib.parse import quote_plus

class WebAutomation:
    def __init__(self):
        self._browser: Optional[Browser] = None
        self._context = None
        
    async def __aenter__(self):
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()
        
    async def initialize(self):
        """Initialize the browser instance"""
        try:
            playwright = await async_playwright().start()
            self._browser = await playwright.chromium.launch(headless=True)
            self._context = await self._browser.new_context()
        except Exception as e:
            self._browser = None
            self._context = None
            raise RuntimeError(f"Failed to initialize browser: {str(e)}")
        
    async def cleanup(self):
        """Clean up browser resources"""
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
            
    async def search_product(self, query: str) -> List[Dict[str, Any]]:
        """Search for product information across multiple sources"""
        results = []
        
        # Search major Iranian e-commerce sites
        digikala_results = await self._search_digikala(query)
        if digikala_results:
            results.extend(digikala_results)
            
        technolife_results = await self._search_technolife(query)
        if technolife_results:
            results.extend(technolife_results)
            
        # Add price comparison
        if results:
            results = await self._enrich_with_price_comparison(results)
            
        return results
        
    async def _search_digikala(self, query: str) -> List[Dict[str, Any]]:
        """Search Digikala for products"""
        page = None
        try:
            if not self._context:
                await self.initialize()
            if not self._context:
                raise Exception("Failed to initialize browser context")
            page = await self._context.new_page()
            await page.goto(f"https://www.digikala.com/search/?q={quote_plus(query)}")
            await page.wait_for_selector(".c-product-box")
            
            products = await page.evaluate("""
                () => {
                    const products = [];
                    document.querySelectorAll('.c-product-box').forEach(box => {
                        const title = box.querySelector('.c-product-box__title')?.innerText;
                        const price = box.querySelector('.c-price__value')?.innerText;
                        const link = box.querySelector('a')?.href;
                        const image = box.querySelector('img')?.src;
                        if (title && price) {
                            products.push({ title, price, link, image, source: 'digikala' });
                        }
                    });
                    return products;
                }
            """)
            
            return products
        except Exception as e:
            return []
        finally:
            if page:
                await page.close()
            
    async def _search_technolife(self, query: str) -> List[Dict[str, Any]]:
        """Search Technolife for products"""
        page = None
        try:
            if not self._context:
                await self.initialize()
            if not self._context:
                raise Exception("Failed to initialize browser context")
            page = await self._context.new_page()
            await page.goto(f"https://www.technolife.ir/search?query={quote_plus(query)}")
            await page.wait_for_selector(".product-box")
            
            products = await page.evaluate("""
                () => {
                    const products = [];
                    document.querySelectorAll('.product-box').forEach(box => {
                        const title = box.querySelector('.product-title')?.innerText;
                        const price = box.querySelector('.price')?.innerText;
                        const link = box.querySelector('a')?.href;
                        const image = box.querySelector('img')?.src;
                        if (title && price) {
                            products.push({ title, price, link, image, source: 'technolife' });
                        }
                    });
                    return products;
                }
            """)
            
            await page.close()
            return products
        except Exception:
            return []
            
    async def _enrich_with_price_comparison(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add price comparison data to products"""
        # Group similar products
        product_groups = {}
        for product in products:
            normalized_title = self._normalize_product_name(product['title'])
            if normalized_title not in product_groups:
                product_groups[normalized_title] = []
            product_groups[normalized_title].append(product)
            
        # Add comparison data
        enriched_products = []
        for group in product_groups.values():
            if len(group) > 1:
                prices = [self._extract_price(p['price']) for p in group if self._extract_price(p['price']) > 0]
                if prices:
                    avg_price = sum(prices) / len(prices)
                    for product in group:
                        product['price_comparison'] = {
                            'average': avg_price,
                            'difference_percent': ((self._extract_price(product['price']) - avg_price) / avg_price) * 100
                            if self._extract_price(product['price']) > 0 else None
                        }
            enriched_products.extend(group)
            
        return enriched_products
        
    def _normalize_product_name(self, name: str) -> str:
        """Normalize product name for comparison"""
        # Remove common variations and extra spaces
        name = re.sub(r'\s+', ' ', name.lower())
        name = re.sub(r'[^\w\s]', '', name)
        return name.strip()
        
    def _extract_price(self, price_str: str) -> float:
        """Extract numeric price from string"""
        try:
            # Remove non-numeric characters and convert to float
            price = re.sub(r'[^\d]', '', price_str)
            return float(price) if price else 0
        except ValueError:
            return 0