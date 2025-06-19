swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "News Aggregator API",
        "description": "API documentation for the News Aggregator project",
        "version": "1.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization using Bearer scheme. Format: 'Bearer <your_token>'"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}
