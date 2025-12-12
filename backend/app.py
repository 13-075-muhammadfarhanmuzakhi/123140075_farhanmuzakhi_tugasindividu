from pyramid.config import Configurator
from pyramid.response import Response
from waitress import serve
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CORSMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            headers.append(('Access-Control-Allow-Origin', '*'))
            headers.append(('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'))
            headers.append(('Access-Control-Allow-Headers', 'Content-Type, Authorization'))
            headers.append(('Access-Control-Max-Age', '3600'))
            return start_response(status, headers, exc_info)

        if environ['REQUEST_METHOD'] == 'OPTIONS':
            custom_start_response('200 OK', [('Content-Type', 'text/plain')])
            return [b'']

        return self.app(environ, custom_start_response)

def main(global_config, **settings):
    logger.info("Starting Product Review Analyzer API...")
    
    config = Configurator(settings=settings)
    
    try:
        config.include('cornice')
    except:
        pass
    
    config.add_route('health', '/')
    config.add_route('analyze_review', '/api/analyze-review')
    config.add_route('get_reviews', '/api/reviews')
    
    config.scan('views')
    
    logger.info("Configuration completed successfully")
    
    app = config.make_wsgi_app()
    return CORSMiddleware(app)

if __name__ == '__main__':
    settings = {
        'pyramid.reload_templates': True,
        'pyramid.debug_authorization': False,
        'pyramid.debug_notfound': False,
        'pyramid.debug_routematch': False,
        'pyramid.default_locale_name': 'en',
    }
    
    app = main({}, **settings)
    
    host = '0.0.0.0'
    port = 6543
    
    logger.info("=" * 60)
    logger.info(f"🚀 Server running on http://localhost:{port}")
    logger.info("=" * 60)
    logger.info("Endpoints:")
    logger.info("  GET  / - Health check")
    logger.info("  POST /api/analyze-review - Analyze review")
    logger.info("  GET  /api/reviews - Get all reviews")
    logger.info("=" * 60)
    
    serve(app, host=host, port=port)