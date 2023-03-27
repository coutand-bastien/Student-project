''' Main class '''
__name__                = "app.py"
__date__                = "14.11.22"
__version__             = "1.0.0"
__license__             = "ENSIBS - Cyberlog4"
__copyright__           = "Copyright 2022, The S7 Project"
__referent_Professeur__ = "M. Salah SADOU"
__credits__             = ["COUTAND Bastien", "DAOUDI Elyes", "DENOUE Enzo", "MARCHAND Robin"]


from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.router import admin_router, supervisor_router, reader_router, new_user_router, authentification_router, email_router
from api.router.middleware.SecurityHeadersMiddleware import SecurityHeadersMiddleware 
from api.router.dependencies import templates
from api.database.database import Base, engine
from api.database.init_db import init_db


# creation of the tables
Base.metadata.create_all(bind=engine)

# openapi_url="" --> delete the automatic documentation on openAPI
app = FastAPI(openapi_url="")

# include all the routes
app.include_router(admin_router.router)
app.include_router(supervisor_router.router)
app.include_router(reader_router.router)
app.include_router(new_user_router.router)
app.include_router(authentification_router.router)
app.include_router(email_router.router)


###############################################################################
#
#   DATABASE INITIALISATION
#
###############################################################################

init_db()

###############################################################################
#
#   MIDDLEWARE
#
###############################################################################

# app.add_middleware(SecurityHeadersMiddleware) # CSP middleware #TODO finir csp
app.add_middleware(SessionMiddleware, secret_key="NotSoSecretKey") # Session middleware

###############################################################################
#
#   FRONT MOUNT
#
###############################################################################

app.mount("/static", StaticFiles(directory="static"), name="static")

###############################################################################
#
#   ERRORS ROUTES
#
###############################################################################

@app.exception_handler(StarletteHTTPException)
async def exception_handler(request: Request, exception: StarletteHTTPException):
    '''
    '''
    print(exception)
    return templates.TemplateResponse('errors/error.html', {
        'request': request,
        'error_code': exception.status_code
    })

###############################################################################
#
#   MAIN ROUTES
#
###############################################################################

@app.get("/", tags=["root"])
async def root(request: Request):
    '''
    The main route

    @param request: the request

    @return an redirection to the fast api documentation
    '''
    return RedirectResponse(request.url_for('login'))