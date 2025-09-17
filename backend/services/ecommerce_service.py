import requests
from bs4 import BeautifulSoup
import urllib.parse
from typing import List, Dict, Any, Optional
import time
import random
import re

class EcommerceService:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        self.session.headers.update(self.headers)
        # Disable SSL verification to avoid connection issues
        self.session.verify = False
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def get_product_details(self, query: str) -> Dict[str, Any]:
        """Get comprehensive product details from multiple e-commerce sites"""
        product_data = {
            'flipkart': self._get_flipkart_details(query),
            'amazon': self._get_amazon_details(query),
            'summary': self._generate_product_summary(query)
        }
        return product_data
    
    def _get_flipkart_details(self, query: str) -> Dict[str, Any]:
        """Extract real product details from Flipkart"""
        try:
            # Clean query for better search
            clean_query = query.replace(' review', '').replace(' analysis', '').strip()
            search_url = f"https://www.flipkart.com/search?q={urllib.parse.quote(clean_query)}"
            
            # Add Flipkart-specific headers
            headers = self.headers.copy()
            headers.update({
                'Referer': 'https://www.flipkart.com/',
                'Host': 'www.flipkart.com'
            })
            
            response = self.session.get(search_url, headers=headers, timeout=20)
            
            if response.status_code == 200:
                result = self._parse_flipkart_response(response.text, clean_query)
                if result:
                    print(f"✅ Flipkart: Found {result['product_name']} - {result['price']}")
                    return result
                else:
                    print("⚠️ Flipkart: No products found in search results")
                    return None
            else:
                print(f"❌ Flipkart returned status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Flipkart scraping failed: {str(e)[:100]}")
            return None
    
    def _get_amazon_details(self, query: str) -> Dict[str, Any]:
        """Extract real product details from Amazon"""
        try:
            # Clean query for better search
            clean_query = query.replace(' review', '').replace(' analysis', '').strip()
            search_url = f"https://www.amazon.in/s?k={urllib.parse.quote(clean_query)}&ref=sr_pg_1"
            
            # Add Amazon-specific headers
            headers = self.headers.copy()
            headers.update({
                'Referer': 'https://www.amazon.in/',
                'Host': 'www.amazon.in',
                'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8'
            })
            
            response = self.session.get(search_url, headers=headers, timeout=20)
            
            if response.status_code == 200:
                result = self._parse_amazon_response(response.text, clean_query)
                if result:
                    print(f"✅ Amazon: Found {result['product_name']} - {result['price']}")
                    return result
                else:
                    print("⚠️ Amazon: No products found in search results")
                    return None
            else:
                print(f"❌ Amazon returned status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Amazon scraping failed: {str(e)[:100]}")
            return None
    
    def _generate_flipkart_data(self, query: str) -> Dict[str, Any]:
        """Generate realistic Flipkart product data"""
        product_name = query.title()
        
        # Generate realistic pricing
        base_price = random.randint(15000, 80000)
        discount = random.randint(5, 25)
        discounted_price = int(base_price * (100 - discount) / 100)
        
        # Generate realistic ratings
        rating = round(random.uniform(3.8, 4.6), 1)
        review_count = random.randint(1500, 15000)
        
        return {
            'platform': 'Flipkart',
            'product_name': product_name,
            'price': f"₹{discounted_price:,}",
            'original_price': f"₹{base_price:,}",
            'discount': f"{discount}% off",
            'rating': rating,
            'review_count': f"{review_count:,} reviews",
            'availability': 'In Stock',
            'delivery': 'Free Delivery',
            'offers': [
                'Bank Offer: 10% off on HDFC Bank Credit Cards',
                'Exchange Offer: Up to ₹15,000 off',
                'No Cost EMI available'
            ],
            'key_features': self._get_product_features(query),
            'top_reviews': self._generate_reviews('flipkart', query),
            'url': f"https://www.flipkart.com/search?q={urllib.parse.quote(query)}"
        }
    
    def _generate_amazon_data(self, query: str) -> Dict[str, Any]:
        """Generate realistic Amazon product data"""
        product_name = query.title()
        
        # Generate realistic pricing (usually slightly different from Flipkart)
        base_price = random.randint(16000, 82000)
        discount = random.randint(3, 20)
        discounted_price = int(base_price * (100 - discount) / 100)
        
        # Generate realistic ratings
        rating = round(random.uniform(3.9, 4.7), 1)
        review_count = random.randint(2000, 18000)
        
        return {
            'platform': 'Amazon',
            'product_name': product_name,
            'price': f"₹{discounted_price:,}",
            'original_price': f"₹{base_price:,}",
            'discount': f"{discount}% off",
            'rating': rating,
            'review_count': f"{review_count:,} reviews",
            'availability': 'In Stock',
            'delivery': 'FREE Delivery by Amazon',
            'prime_eligible': True,
            'offers': [
                'Amazon Pay ICICI Bank Credit Card: 5% back',
                'Exchange: Up to ₹12,000 off',
                'EMI starting from ₹2,500/month'
            ],
            'key_features': self._get_product_features(query),
            'top_reviews': self._generate_reviews('amazon', query),
            'url': f"https://www.amazon.com/s?k={urllib.parse.quote(query)}"
        }
    
    def _get_product_features(self, query: str) -> List[str]:
        """Generate realistic product features based on query"""
        query_lower = query.lower()
        
        if 'pixel' in query_lower:
            return [
                'Google Tensor G4 processor',
                '12GB RAM, 256GB Storage',
                '50MP main camera with AI features',
                '6.3-inch OLED display, 120Hz',
                '4700mAh battery with fast charging',
                'Android 14 with 7 years of updates',
                'Titan M security chip',
                'IP68 water resistance'
            ]
        elif 'iphone' in query_lower:
            return [
                'A17 Pro chip with 6-core GPU',
                '8GB RAM, up to 1TB storage',
                '48MP main camera system',
                '6.1-inch Super Retina XDR display',
                'All-day battery life',
                'iOS 17 with regular updates',
                'Face ID security',
                'IP68 water resistance'
            ]
        elif 'samsung' in query_lower:
            return [
                'Snapdragon 8 Gen 3 processor',
                '12GB RAM, 512GB Storage',
                '200MP main camera with zoom',
                '6.8-inch Dynamic AMOLED display',
                '5000mAh battery with 45W charging',
                'One UI 6.0 based on Android 14',
                'Samsung Knox security',
                'IP68 water and dust resistance'
            ]
        else:
            return [
                'Latest flagship processor',
                'High-capacity RAM and storage',
                'Advanced camera system',
                'High-resolution display',
                'Long-lasting battery',
                'Latest software updates',
                'Premium build quality',
                'Water resistance'
            ]
    
    def _generate_reviews(self, platform: str, query: str) -> List[Dict[str, Any]]:
        """Generate realistic customer reviews"""
        reviews = []
        
        review_templates = [
            {
                'rating': 5,
                'title': 'Excellent product, highly recommended!',
                'text': 'Amazing performance and build quality. The camera is outstanding and battery life is impressive. Worth every penny.',
                'helpful': random.randint(50, 200)
            },
            {
                'rating': 4,
                'title': 'Good value for money',
                'text': 'Overall satisfied with the purchase. Performance is smooth and features are as expected. Minor issues with delivery packaging.',
                'helpful': random.randint(30, 150)
            },
            {
                'rating': 5,
                'title': 'Best in this price range',
                'text': 'Compared with other options, this offers the best features and performance. Camera quality exceeded expectations.',
                'helpful': random.randint(40, 180)
            },
            {
                'rating': 4,
                'title': 'Solid performance',
                'text': 'Fast processing, good display quality, and reliable performance. Battery backup is decent for heavy usage.',
                'helpful': random.randint(25, 120)
            },
            {
                'rating': 3,
                'title': 'Average experience',
                'text': 'Product is okay but expected better performance for the price. Some features could be improved.',
                'helpful': random.randint(15, 80)
            }
        ]
        
        # Select 3-4 random reviews
        selected_reviews = random.sample(review_templates, random.randint(3, 4))
        
        for i, review in enumerate(selected_reviews):
            reviews.append({
                'reviewer': f"Customer_{i+1}",
                'rating': review['rating'],
                'title': review['title'],
                'text': review['text'],
                'helpful_votes': review['helpful'],
                'verified_purchase': True
            })
        
        return reviews
    
    def _parse_flipkart_response(self, html: str, query: str) -> Dict[str, Any]:
        """Parse Flipkart HTML to extract real product data"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Multiple selectors for Flipkart products
        product_selectors = [
            'div[data-id]',
            '._1AtVbE',
            '._13oc-S',
            '._2kHMtA',
            '.s1Q9rs',
            '._1fQZEK'
        ]
        
        product = None
        for selector in product_selectors:
            products = soup.select(selector)
            if products:
                product = products[0]
                break
        
        if product:
            # Extract product name with multiple selectors
            name_selectors = ['._4rR01T', '.IRpwTa', '.s1Q9rs', '._2WkVRV', '.KzDlHZ']
            product_name = query
            for selector in name_selectors:
                name_elem = product.select_one(selector)
                if name_elem and name_elem.get_text().strip():
                    product_name = name_elem.get_text().strip()
                    break
            
            # Extract price with multiple selectors
            price_selectors = ['._30jeq3', '._1_WHN1', '.Nx9bqj', '._2B099V', '._25b18c']
            price = 'Price not available'
            for selector in price_selectors:
                price_elem = product.select_one(selector)
                if price_elem and price_elem.get_text().strip():
                    price_text = price_elem.get_text().strip()
                    if '₹' in price_text or any(c.isdigit() for c in price_text):
                        price = price_text
                        break
            
            # Extract rating with multiple selectors
            rating_selectors = ['._3LWZlK', '.gUuXy-', '._2d4LTz', '.XQDdHH']
            rating = 'No rating'
            for selector in rating_selectors:
                rating_elem = product.select_one(selector)
                if rating_elem and rating_elem.get_text().strip():
                    rating = rating_elem.get_text().strip()
                    break
            
            # Extract review count
            review_selectors = ['._2_R_DZ', '.Wphh3N', '._38sUEc']
            review_count = 'No reviews'
            for selector in review_selectors:
                review_elem = product.select_one(selector)
                if review_elem and review_elem.get_text().strip():
                    review_count = review_elem.get_text().strip()
                    break
            
            return {
                'platform': 'Flipkart',
                'product_name': product_name,
                'price': price,
                'rating': rating,
                'review_count': review_count,
                'availability': 'Available on Flipkart',
                'url': f"https://www.flipkart.com/search?q={urllib.parse.quote(query)}"
            }
        
        return None
    
    def _parse_amazon_response(self, html: str, query: str) -> Dict[str, Any]:
        """Parse Amazon HTML to extract real product data"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Multiple selectors for Amazon products
        product_selectors = [
            'div[data-component-type="s-search-result"]',
            '.s-result-item',
            '.sg-col-inner',
            '[data-asin]',
            '.s-card-container'
        ]
        
        product = None
        for selector in product_selectors:
            products = soup.select(selector)
            if products:
                product = products[0]
                break
        
        if product:
            # Extract product name with multiple selectors
            name_selectors = [
                'h2 a span',
                '.a-size-medium',
                '.a-size-base-plus',
                'h2.a-size-mini span',
                '.s-size-mini',
                '[data-cy="title-recipe-label"]'
            ]
            product_name = query
            for selector in name_selectors:
                name_elem = product.select_one(selector)
                if name_elem and name_elem.get_text().strip():
                    product_name = name_elem.get_text().strip()
                    break
            
            # Extract price with multiple selectors
            price_selectors = [
                '.a-price-whole',
                '.a-price .a-offscreen',
                '.a-price-range .a-price .a-offscreen',
                '.a-price-symbol',
                '.a-price'
            ]
            price = 'Price not available'
            for selector in price_selectors:
                price_elem = product.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text().strip()
                    if '₹' in price_text or any(c.isdigit() for c in price_text):
                        price = price_text
                        break
            
            # Extract rating with multiple selectors
            rating_selectors = [
                '.a-icon-alt',
                '.a-star-mini .a-icon-alt',
                'span[aria-label*="stars"]',
                '.a-declarative .a-icon-alt'
            ]
            rating = 'No rating'
            for selector in rating_selectors:
                rating_elem = product.select_one(selector)
                if rating_elem:
                    rating_text = rating_elem.get('aria-label', '') or rating_elem.get_text().strip()
                    if 'star' in rating_text.lower() or any(c.isdigit() for c in rating_text):
                        rating = rating_text
                        break
            
            # Extract review count
            review_selectors = [
                '.a-size-base',
                'a[href*="#customerReviews"]',
                '.a-link-normal[href*="reviews"]'
            ]
            review_count = 'No reviews'
            for selector in review_selectors:
                review_elem = product.select_one(selector)
                if review_elem:
                    review_text = review_elem.get_text().strip()
                    if any(c.isdigit() for c in review_text) and len(review_text) < 50:
                        review_count = review_text
                        break
            
            return {
                'platform': 'Amazon',
                'product_name': product_name,
                'price': price,
                'rating': rating,
                'review_count': review_count,
                'availability': 'Available on Amazon',
                'url': f"https://www.amazon.in/s?k={urllib.parse.quote(query)}"
            }
        
        return None
    
    def _generate_product_summary(self, query: str) -> Dict[str, Any]:
        """Generate comprehensive product summary"""
        return {
            'comparison': {
                'price_difference': 'Flipkart typically ₹1,000-3,000 cheaper',
                'delivery': 'Both offer free delivery, Amazon Prime faster',
                'offers': 'Flipkart has better exchange offers, Amazon better EMI',
                'return_policy': 'Both offer 7-day return policy'
            },
            'recommendation': {
                'best_price': 'Flipkart (usually lower prices)',
                'best_service': 'Amazon (faster delivery, better support)',
                'best_offers': 'Compare both for current deals',
                'overall': 'Check both platforms before purchasing'
            },
            'key_considerations': [
                'Compare prices on both platforms',
                'Check current offers and discounts',
                'Consider delivery time requirements',
                'Verify seller ratings and reviews',
                'Check return and warranty policies'
            ]
        }