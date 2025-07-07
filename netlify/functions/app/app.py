import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))

from app import create_app

# Create the Flask application
application = create_app()

def handler(event, context):
    """
    Netlify Functions handler for Flask app
    """
    import io
    
    try:
        # Extract request info from event
        method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        query_string = event.get('queryStringParameters', {})
        headers = event.get('headers', {})
        body = event.get('body', '')
        
        # Build query string
        if query_string:
            query_params = '&'.join([f"{k}={v}" for k, v in query_string.items()])
            if query_params:
                path += '?' + query_params
        
        # Create a WSGI environ
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path.split('?')[0],
            'QUERY_STRING': path.split('?')[1] if '?' in path else '',
            'CONTENT_TYPE': headers.get('content-type', ''),
            'CONTENT_LENGTH': str(len(body)) if body else '0',
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': io.BytesIO(body.encode() if body else b''),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
        }
        
        # Add headers to environ
        for key, value in headers.items():
            key = 'HTTP_' + key.upper().replace('-', '_')
            environ[key] = value
        
        # Handle the request
        response_data = []
        status_code = None
        response_headers = []
        
        def start_response(status, response_headers_list):
            nonlocal status_code, response_headers
            status_code = int(status.split()[0])
            response_headers = response_headers_list
        
        app_iter = application(environ, start_response)
        response_data = b''.join(app_iter)
        
        # Convert headers to dict
        headers_dict = {}
        for header_name, header_value in response_headers:
            headers_dict[header_name] = header_value
        
        return {
            'statusCode': status_code,
            'headers': headers_dict,
            'body': response_data.decode('utf-8'),
            'isBase64Encoded': False
        }
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in handler: {e}")
        print(f"Traceback: {error_trace}")
        
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f"Internal Server Error: {str(e)}\n\nTraceback:\n{error_trace}",
            'isBase64Encoded': False
        }
