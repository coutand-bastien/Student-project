'''Middleware for security.'''
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


CSP = "default-src 'self'; script-src 'self' cdn.jsdelivr.net/npm/apexcharts; style-src 'self' fonts.googleapis.com stackpath.bootstrapcdn.com; base-uri 'none';"


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    '''Add security headers to all responses.'''

    def __init__(self, app: FastAPI):
        '''
        Init SecurityHeadersMiddleware.

        :param app: FastAPI instance
        '''
        super().__init__(app)
        

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        '''
        Dispatch of the middleware.

        :param request: Incoming request
        :param call_next: Function to process the request

        :return: Return response coming from from processed request
        '''
        headers = {
            "Content-Security-Policy": f"{CSP}",
            "Cross-Origin-Opener-Policy": "same-origin",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Strict-Transport-Security": "max-age=31556926; includeSubDomains",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
        }

        response = await call_next(request)
        response.headers.update(headers)

        return response