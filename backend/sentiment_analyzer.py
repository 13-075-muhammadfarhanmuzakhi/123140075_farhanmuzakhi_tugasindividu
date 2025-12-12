from transformers import pipeline
import os
from dotenv import load_dotenv

load_dotenv()

class SentimentAnalyzer:
    def __init__(self):
        # Using multilingual model that supports Indonesian, English, and many other languages
        hf_token = os.getenv('HUGGINGFACE_API_KEY')
        
        try:
            self.analyzer = pipeline(
                "sentiment-analysis",
                model="nlptown/bert-base-multilingual-uncased-sentiment",
                token=hf_token if hf_token else None,
                device=-1  # Use CPU explicitly to avoid meta tensor issues
            )
            print("Loaded multilingual sentiment analyzer (supports Indonesian)")
        except Exception as e:
            print(f"Error loading multilingual model: {e}")
            try:
                # Fallback to English model
                self.analyzer = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    token=hf_token if hf_token else None,
                    device=-1
                )
                print("Loaded English sentiment analyzer (fallback)")
            except Exception as e2:
                print(f"Error loading model: {e2}")
                raise
    
    def analyze(self, text):
        """
        Analyze sentiment of text (supports Indonesian and other languages)
        Returns: dict with 'sentiment' and 'confidence_score'
        """
        try:
            result = self.analyzer(text[:512])[0]  # Limit to 512 chars
            
            # Map different label formats from different models
            label = result['label'].upper().strip()
            
            # Handle multilingual model output (5 STARS, 4 STARS, etc.)
            if label in ['5 STARS', '5STARS', '4 STARS', '4STARS']:
                sentiment = 'positive'
            elif label in ['1 STAR', '1STAR', '2 STARS', '2STARS', '3 STARS', '3STARS']:
                sentiment = 'negative' if label.startswith('1') or label.startswith('2') else 'neutral'
            # Handle English model output (POSITIVE, NEGATIVE, NEUTRAL)
            elif label in ['POSITIVE']:
                sentiment = 'positive'
            elif label in ['NEGATIVE']:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            confidence = result['score']
            
            print(f"Label: {label}, Sentiment: {sentiment}, Score: {confidence}")
            
            return {
                'sentiment': sentiment,
                'confidence_score': round(confidence, 4)
            }
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {
                'sentiment': 'neutral',
                'confidence_score': 0.5
            }