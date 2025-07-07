import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app import create_app
import json

# Create Flask app
app = create_app()

def handler(event, context):
    """
    Netlify Functions handler for Flask app
    """
    try:
        # Get request details from event
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        query_string = event.get('queryStringParameters') or {}
        headers = event.get('headers', {})
        body = event.get('body', '')
        
        # Handle different content types
        if headers.get('content-type', '').startswith('application/json'):
            try:
                body = json.loads(body) if body else {}
            except json.JSONDecodeError:
                body = {}
        
        # Create a test client to simulate the request
        with app.test_client() as client:
            # Prepare query string
            query_params = '&'.join([f"{k}={v}" for k, v in query_string.items()]) if query_string else ''
            full_path = f"{path}?{query_params}" if query_params else path
            
            # Make the request
            if http_method == 'GET':
                response = client.get(full_path, headers=headers)
            elif http_method == 'POST':
                if isinstance(body, dict):
                    response = client.post(full_path, json=body, headers=headers)
                else:
                    response = client.post(full_path, data=body, headers=headers)
            elif http_method == 'PUT':
                response = client.put(full_path, data=body, headers=headers)
            elif http_method == 'DELETE':
                response = client.delete(full_path, headers=headers)
            else:
                response = client.get(full_path, headers=headers)
            
            # Return response
            return {
                'statusCode': response.status_code,
                'headers': {
                    'Content-Type': response.content_type,
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                },
                'body': response.get_data(as_text=True)
            }
            
    except Exception as e:
        print(f"Error in Netlify function: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Internal server error'
            })
        }
