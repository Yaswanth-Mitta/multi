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
                structured_content += f"\\n--- Source {i+1}: {chunk.metadata['title']} ---\\n"
                structured_content += f"URL: {chunk.metadata['source']}\\n"
                structured_content += f"Content: {chunk.page_content}\\n"
            
            return structured_content
            
        except Exception as e:
            print(f"LangChain processing failed: {e}")
            return "Failed to process scraped data"
    
    def process_youtube_data(self, youtube_reviews: List[Dict[str, Any]]) -> str:
        """Process YouTube review data"""
        try:
            youtube_content = "\\n=== YOUTUBE REVIEW ANALYSIS ===\\n"
            
            for i, video in enumerate(youtube_reviews, 1):
                youtube_content += f"\\nVideo {i}: {video['title']}\\n"
                youtube_content += f"Views: {video['views']}\\n"
                
                if 'transcript' in video and video['transcript']:
                    # Process transcript with text splitter
                    doc = Document(
                        page_content=video['transcript'],
                        metadata={'source': video['url'], 'type': 'youtube_transcript'}
                    )
                    
                    chunks = self.text_splitter.split_documents([doc])
                    if chunks:
                        youtube_content += f"Key Points: {chunks[0].page_content[:300]}...\\n"
                else:
                    youtube_content += "Transcript: Not available\\n"
            
            return youtube_content
            
        except Exception as e:
            print(f"YouTube data processing failed: {e}")
            return "Failed to process YouTube data"
    
    def create_comprehensive_context(self, search_results: List[Dict], scraped_data: List[Dict], 
                                   youtube_reviews: List[Dict], reddit_posts: List[Dict]) -> str:
        """Create comprehensive context using all data sources"""
        
        context = "=== COMPREHENSIVE PRODUCT REVIEW DATA ===\\n\\n"
        
        # Process web scraping data
        web_content = self.process_scraped_data(scraped_data)
        context += f"=== WEB REVIEW CONTENT ===\\n{web_content}\\n"
        
        # Process YouTube data
        if youtube_reviews:
            youtube_content = self.process_youtube_data(youtube_reviews)
            context += f"\\n{youtube_content}\\n"
        
        # Add Reddit discussions (if any)
        if reddit_posts:
            context += "\\n=== REDDIT USER DISCUSSIONS ===\\n"
            for i, post in enumerate(reddit_posts, 1):
                context += f"{i}. {post['title']} ({post['subreddit']})\\n"
        else:
            context += "\\n=== REDDIT DISCUSSIONS ===\\nReddit scraping disabled\\n"
        
        # Add search result summaries
        context += "\\n=== SEARCH RESULT SUMMARIES ===\\n"
        for i, result in enumerate(search_results, 1):
            context += f"{i}. {result['title']}\\n"
            context += f"   Summary: {result['snippet']}\\n\\n"
        
        return context