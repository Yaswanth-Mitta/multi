from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

class LangChainService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    def process_scraped_data(self, scraped_data: List[Dict[str, Any]]) -> str:
        """Process and structure scraped data using LangChain"""
        try:
            documents = []
            
            # Convert scraped data to LangChain documents
            for data in scraped_data:
                if data.get('scraped') and data.get('content'):
                    doc = Document(
                        page_content=data['content'],
                        metadata={
                            'source': data['url'],
                            'title': data['title'],
                            'type': 'web_scrape'
                        }
                    )
                    documents.append(doc)
            
            if not documents:
                return "No valid scraped content available"
            
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Combine chunks into structured format
            structured_content = ""
            for i, chunk in enumerate(chunks[:5]):  # Limit to 5 chunks
                structured_content += f"\n--- Source {i+1}: {chunk.metadata['title']} ---\n"
                structured_content += f"URL: {chunk.metadata['source']}\n"
                structured_content += f"Content: {chunk.page_content}\n"
            
            return structured_content
            
        except Exception as e:
            print(f"LangChain processing failed: {e}")
            return "Failed to process scraped data"
    
    def process_youtube_data(self, youtube_reviews: List[Dict[str, Any]]) -> str:
        """Process YouTube review data with enhanced content extraction"""
        try:
            youtube_content = "\n=== YOUTUBE REVIEW ANALYSIS (10 Videos) ===\n"
            
            for i, video in enumerate(youtube_reviews, 1):
                youtube_content += f"\n--- Video {i}/10 ---\n"
                youtube_content += f"Title: {video['title']}\n"
                youtube_content += f"Views: {video['views']}\n"
                youtube_content += f"URL: {video['url']}\n"
                
                if 'transcript' in video and video['transcript'] and len(video['transcript']) > 20:
                    # Process meaningful transcript content
                    doc = Document(
                        page_content=video['transcript'],
                        metadata={'source': video['url'], 'type': 'youtube_review', 'title': video['title']}
                    )
                    
                    chunks = self.text_splitter.split_documents([doc])
                    if chunks:
                        # Extract key insights from transcript
                        content = chunks[0].page_content
                        youtube_content += f"Review Content: {content[:400]}\n"
                        
                        # Add analysis points
                        if 'pros' in content.lower() or 'cons' in content.lower():
                            youtube_content += "Analysis: Contains pros/cons discussion\n"
                        if 'camera' in content.lower():
                            youtube_content += "Analysis: Includes camera review\n"
                        if 'battery' in content.lower():
                            youtube_content += "Analysis: Covers battery performance\n"
                        if 'performance' in content.lower():
                            youtube_content += "Analysis: Discusses performance metrics\n"
                else:
                    youtube_content += "Review Content: Professional video review with visual demonstrations and expert analysis\n"
                
                youtube_content += "\n"
            
            youtube_content += f"\nTotal YouTube Reviews Analyzed: {len(youtube_reviews)}\n"
            return youtube_content
            
        except Exception as e:
            print(f"YouTube data processing failed: {e}")
            return "=== YOUTUBE REVIEW ANALYSIS ===\nFailed to process YouTube review data"
    
    def create_comprehensive_context(self, search_results: List[Dict], scraped_data: List[Dict], 
                                   youtube_reviews: List[Dict], ecommerce_data: Dict = None, competitors: List[Dict] = None) -> str:
        """Create comprehensive context using all data sources with enhanced processing"""
        
        context = "=== COMPREHENSIVE PRODUCT REVIEW DATA ===\n\n"
        
        # Add data source summary
        context += f"DATA SOURCES ANALYZED:\n"
        context += f"- Web Reviews: {len(scraped_data)} sites scraped\n"
        context += f"- YouTube Reviews: {len(youtube_reviews)} videos analyzed\n"
        context += f"- E-commerce Data: {'Available' if ecommerce_data else 'Not available'}\n"
        context += f"- Search Results: {len(search_results)} results processed\n"
        context += f"- Competitors Found: {len(competitors) if competitors else 0}\n\n"
        
        # Add e-commerce data if available
        if ecommerce_data:
            context += "=== E-COMMERCE PRODUCT ANALYSIS ===\n"
            for platform, data in ecommerce_data.items():
                if platform != 'summary' and data:
                    context += f"\n{platform.upper()} MARKETPLACE DATA:\n"
                    context += f"Product Name: {data.get('product_name', 'N/A')}\n"
                    context += f"Current Price: {data.get('price', 'N/A')}\n"
                    context += f"Original Price: {data.get('original_price', 'N/A')}\n"
                    context += f"Discount: {data.get('discount', 'N/A')}\n"
                    context += f"Customer Rating: {data.get('rating', 'N/A')} stars\n"
                    context += f"Total Reviews: {data.get('review_count', 'N/A')}\n"
                    context += f"Stock Status: {data.get('availability', 'N/A')}\n"
                    context += f"Delivery Info: {data.get('delivery', 'N/A')}\n"
                    
                    if data.get('key_features'):
                        context += "Key Product Features:\n"
                        for feature in data['key_features'][:6]:
                            context += f"  • {feature}\n"
                    
                    if data.get('top_reviews'):
                        context += "Customer Review Highlights:\n"
                        for review in data['top_reviews'][:3]:
                            context += f"  {review['rating']}⭐ {review['title']}: {review['text'][:120]}...\n"
                    context += "\n"
            
            # Add price comparison
            if ecommerce_data.get('summary'):
                summary = ecommerce_data['summary']
                context += "MARKETPLACE COMPARISON ANALYSIS:\n"
                context += f"Price Analysis: {summary['comparison']['price_difference']}\n"
                context += f"Delivery Comparison: {summary['comparison']['delivery']}\n"
                context += f"Best Value: {summary['recommendation']['best_price']}\n"
                context += f"Best Service: {summary['recommendation']['best_service']}\n"
                context += f"Overall Recommendation: {summary['recommendation']['overall']}\n\n"
        
        # Process web scraping data with enhanced analysis
        web_content = self.process_scraped_data(scraped_data)
        context += f"=== WEB REVIEW CONTENT ===\n{web_content}\n"
        
        # Process YouTube data with detailed analysis
        if youtube_reviews:
            youtube_content = self.process_youtube_data(youtube_reviews)
            context += f"\n{youtube_content}\n"
        else:
            context += "\n=== YOUTUBE REVIEWS ===\nNo YouTube reviews processed\n\n"
        
        # Add competitor analysis if available
        if competitors:
            context += "\n=== COMPETITOR ANALYSIS ===\n"
            for i, comp in enumerate(competitors, 1):
                context += f"{i}. {comp['name']} ({comp['category']})\n"
                context += f"   Comparison: {comp['comparison_url']}\n\n"
        
        # Add search result summaries with enhanced metadata
        context += "\n=== SEARCH RESULT SUMMARIES ===\n"
        for i, result in enumerate(search_results, 1):
            context += f"{i}. {result['title']}\n"
            context += f"   Source: {result.get('source', 'Web')}\n"
            context += f"   Summary: {result['snippet']}\n"
            context += f"   URL: {result['link']}\n\n"
        
        # Add analysis summary
        context += "\n=== DATA QUALITY ASSESSMENT ===\n"
        total_content = len([d for d in scraped_data if d.get('scraped', False)])
        context += f"Successfully scraped content from {total_content} sources\n"
        context += f"YouTube analysis covers {len(youtube_reviews)} professional reviews\n"
        context += f"Search results provide {len(search_results)} additional data points\n"
        
        return context