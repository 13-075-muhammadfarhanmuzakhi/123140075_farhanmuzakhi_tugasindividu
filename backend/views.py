from pyramid.view import view_config
from pyramid.response import Response
import json
import logging
import traceback

logger = logging.getLogger(__name__)

# Initialize analyzers globally (loaded once at startup)
sentiment_analyzer = None
gemini_analyzer = None

def get_sentiment_analyzer():
    """Lazy load sentiment analyzer"""
    global sentiment_analyzer
    if sentiment_analyzer is None:
        logger.info("Loading sentiment analyzer...")
        from sentiment_analyzer import SentimentAnalyzer
        sentiment_analyzer = SentimentAnalyzer()
        logger.info("Sentiment analyzer loaded successfully")
    return sentiment_analyzer

def get_gemini_analyzer():
    """Lazy load gemini analyzer"""
    global gemini_analyzer
    if gemini_analyzer is None:
        logger.info("Loading Gemini analyzer...")
        from gemini_analyzer import GeminiAnalyzer
        gemini_analyzer = GeminiAnalyzer()
        logger.info("Gemini analyzer loaded successfully")
    return gemini_analyzer

@view_config(route_name='analyze_review', renderer='json', request_method='POST')
def analyze_review(request):
    """
    POST /api/analyze-review
    Body: { "product_name": "...", "review_text": "..." }
    """
    try:
        logger.info("Received analyze request")
        
        # Parse request body
        try:
            data = request.json_body
        except Exception as e:
            logger.error(f"Failed to parse JSON: {e}")
            return Response(
                json.dumps({'error': 'Format JSON tidak valid'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        review_text = data.get('review_text', '').strip()
        product_name = data.get('product_name', '').strip()
        language = data.get('language', 'id').strip().lower()
        if language not in ('id', 'en'):
            language = 'id'
        logger.info(f"Review text length: {len(review_text)}")
        
        if not review_text:
            return Response(
                json.dumps({'error': 'Teks review wajib diisi'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        if len(review_text) < 10:
            return Response(
                json.dumps({'error': 'Teks review terlalu pendek (minimal 10 karakter)'}),
                status=400,
                content_type='application/json; charset=utf-8'
            )
        
        # Analyze sentiment
        logger.info("Starting sentiment analysis...")
        try:
            analyzer = get_sentiment_analyzer()
            sentiment_result = analyzer.analyze(review_text)
            logger.info(f"Sentiment: {sentiment_result}")
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            logger.error(traceback.format_exc())
            return Response(
                json.dumps({'error': 'Analisis sentimen gagal. Coba lagi.'}),
                status=500,
                content_type='application/json; charset=utf-8'
            )
        
        # Extract key points with Gemini
        logger.info("Starting key points extraction...")
        try:
            gemini = get_gemini_analyzer()
            key_points = gemini.extract_key_points(review_text, language=language)
            logger.info("Key points extracted successfully")
        except Exception as e:
            logger.error(f"Gemini analysis failed: {e}")
            logger.error(traceback.format_exc())
            # Continue with partial results
            key_points = "- Tidak bisa ekstrak poin penting saat ini" if language == 'id' else "- Unable to extract key points at this time"
        
        # Save to database
        logger.info("Saving to database...")
        try:
            from models import Session, Review
            session = Session()
            review = Review(
                product_name=product_name if product_name else None,
                language=language,
                review_text=review_text,
                sentiment=sentiment_result['sentiment'],
                confidence_score=sentiment_result['confidence_score'],
                key_points=key_points
            )
            session.add(review)
            session.commit()
            
            result = review.to_dict()
            session.close()
            
            logger.info(f"Review saved with ID: {result['id']}")
            return result
            
        except Exception as e:
            logger.error(f"Database error: {e}")
            logger.error(traceback.format_exc())
            return Response(
                json.dumps({'error': 'Gagal menyimpan review ke database'}),
                status=500,
                content_type='application/json; charset=utf-8'
            )
        
    except Exception as e:
        logger.error(f"Unexpected error in analyze_review: {e}")
        logger.error(traceback.format_exc())
        return Response(
            json.dumps({'error': 'Error server. Coba lagi nanti.'}),
            status=500,
            content_type='application/json; charset=utf-8'
        )

@view_config(route_name='get_reviews', renderer='json', request_method='GET')
def get_reviews(request):
    """
    GET /api/reviews
    Returns all reviews from database
    """
    try:
        logger.info("Fetching all reviews...")
        from models import Session, Review
        
        session = Session()
        reviews = session.query(Review).order_by(Review.created_at.desc()).all()
        result = [review.to_dict() for review in reviews]
        session.close()
        
        logger.info(f"Returned {len(result)} reviews")
        return result
        
    except Exception as e:
        logger.error(f"Error in get_reviews: {e}")
        logger.error(traceback.format_exc())
        return Response(
            json.dumps({'error': 'Gagal mengambil data reviews'}),
            status=500,
            content_type='application/json; charset=utf-8'
        )

@view_config(route_name='health', renderer='json', request_method='GET')
def health_check(request):
    """Health check endpoint"""
    logger.info("Health check requested")
    return {
        'status': 'healthy',
        'message': 'Product Review Analyzer API is running',
        'version': '1.0.0'
    }