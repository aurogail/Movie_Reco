from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
import asyncio
import threading
import json
from pydantic import BaseModel
import sys
from api_directory.preferences import get_user_preferences
from api_directory.generate_token import *
sys.path.append('../src')
from src.models.collab_predict import collab_reco, generate_new_recommendations
from src.models.hybrid_predict import hybride_reco
from src.models.train_model_svd import load_svd_model

# Cration of logger object
logger = logging.getLogger(__name__)
logging.basicConfig(filename='./app/logs/api_log.log', level=logging.INFO)

app = FastAPI(
    title="Movie Recommandation's API",
    description="API powered by FastAPI",
    version="1.2.0", 
    openapi_tags=[
    {
        'name':'Authentication',
        'description':'functions used to authenticate as a user'
    },
    {
        'name':'Recommandations',
        'description': 'functions returning a recommandation'
    }
])

# Add CORS to API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

svd_model = None
df_ratings = None

def load_svd_model_sync():
    return load_svd_model() 

async def load_models_and_data():
    global svd_model
    #global svd_model, df_ratings
    svd_model = await asyncio.to_thread(load_svd_model_sync)

# Load model when API start
@app.on_event("startup")
async def startup_event():
    await load_models_and_data()

@app.get("/")
async def read_root():
    model_status = "Model Loaded" if svd_model else "Model Not Loaded"
    return {"model_status": model_status}

# Log Middleware
async def log_requests(request: Request, call_next):
    start_time = datetime.utcnow()

    user_id = None

    # Extraction du user_id pour les requêtes GET et POST
    if request.method in ["POST", "PUT"]:
        try:
            request_body = await request.json()
            user_id = request_body.get("user_id")
        except Exception:
            pass

    if request.method == "GET":
        user_id = request.query_params.get("user_id")

    # Extraction du user_id à partir du JWT si aucun user_id n'a été trouvé
    if not user_id:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = decode_jwt(token)  # Assurez-vous que la fonction decode_jwt retourne le payload
                user_id = payload.get("user_id")
            except Exception:
                pass

    response = await call_next(request)

    process_time = datetime.utcnow() - start_time

    logger.info({
        "timestamp": start_time.isoformat(),
        "user_id": user_id,
        "request_path": request.url.path,
        "request_method": request.method,
        "response_status_code": response.status_code,
        "process_time": process_time.total_seconds()
    })

    return response

# Object containing JWTBearer class from api_directory/generate_token.py
jwt_bearer = JWTBearer()

# Definition of BaseModel class
class UserLogin(BaseModel):
    ''' User Id available in dataset '''
    user_id: int

class HybridRecoRequest(BaseModel):
    ''' Movie title available in dataset '''
    titre: str

@app.post("/login", name='Generate Token', tags=['Authentication'])
async def login(user_data: UserLogin):
    """
    Description:
    This endpoint allows a user to log in by providing login details : user_id. If the details are valid, it returns a JWT token. Otherwise, an error is raised.

    Args:
    - user_data (UserLogin) : user details to log in.

    Returns:
    - str : a JWT token if the login is successful.

    Raises:
    - HTTPException(404, detail="User not found"): If details, user_id is not recognized, an HTTP 404 exception is raised.
    """
    
    # Extract user_id from class UserLogin
    user_id = user_data.user_id
    
    # Looking for user_id in list users defined in api_directory/genrate_token.py
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create a new token for the user_id with the function sign_jwt from generate_token.py
    token = sign_jwt(user_id)

    return {"access_token": token}

@app.get("/welcome", name='Logged', tags=['Authentication'])
async def welcome(user_id: int = Depends(jwt_bearer)):
    """
    Description:
    This endpoint returns a message "Welcome {user_id}" only if user is authenticated with a JWT token.

    Args:
    - user_id (int, dependency) : the user_id extracted from the payload of the JWT token sent.

    Returns:
    - JSON : returns a JSON with a welcoming message if user is authenticated.

    Raises:
    - HTTPException(403, details = ["Invalid authentication scheme.", "Invalid token or expired token.", "Invalid authorization code."]): If the token is not valid and the user cannot be authenticated.
    """

    return {"message": f"Welcome {user_id}"}

@app.get("/recommendations", name='Collaborative Filtering Recommandations', tags=['Recommandations'])
async def get_recommendations(user_id: int = Depends(jwt_bearer)):
    """
    Description:
    This endpoint retrieves personalized movie recommendations for the authenticated user based on collaborative filtering.

    Args:
    - user_id (int, dependency) : the user_id extracted from the payload of the JWT token sent.

    Returns:
    - JSON: returns a JSON object containing a list of personalized movies recommendations for the user.
    
    Raises:
    - HTTPException(403, details = ["Invalid authentication scheme.", "Invalid token or expired token.", "Invalid authorization code."]): If the token is not valid and the user cannot be authenticated.
    """

    try:
        recommendations = collab_reco(user_id, svd_model)  # Utilise le modèle chargé globalement
        titles = recommendations['title']
        return {"user_id": user_id, "recommendations": titles.tolist()}  # Conversion en dictionnaire pour JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

'''
@app.get("/preferences", name='Top Movie Genres', tags=['Recommandations'])
async def get_preferences(user_id: int = Depends(jwt_bearer)):
    """
    Description:
    This endpoint retrieves personalized top movie genres for the authenticated user.

    Args:
    - user_id (int, dependency) : the user_id extracted from the payload of the JWT token sent.

    Returns:
    - JSON: returns a JSON object containing personalized top movie genres for the user.
    
    Raises:
    - HTTPException(403, details = ["Invalid authentication scheme.", "Invalid token or expired token.", "Invalid authorization code."]): If the token is not valid and the user cannot be authenticated.
    """
    # Obtaining top 3 movie genres for the user. The function called is in api_directory/preferences/
    
    preferences = get_user_preferences(user_id, "src/data/processed/user_matrix.csv")
    return {"user_id": user_id, "preferences": preferences}

'''

@app.post("/hybrid", name='Hybrid Filtering Recommandations', tags=['Recommandations'])
async def hybrid_reco(request: HybridRecoRequest, user_id: int = Depends(jwt_bearer)):
    """
    Description:
    This endpoint retrieves personalized movie recommendations for the authenticated user based on content-based filtering.

    Args:
    - request (ContentRecoRequest, body): The request object containing the movie title and similarity matrix type.
    - user_id (int, dependency): The user_id extracted from the payload of the JWT token sent.

    Returns:
    - JSON: Returns a JSON object containing a list of personalized movie recommendations for the user. The movies returned should be similar to the one sent in the request body.

    Raises:
    - HTTPException(403, details=["Invalid authentication scheme.", "Invalid token or expired token.", "Invalid authorization code."]): If the token is not valid and the user cannot be authenticated.
    """

    # Check if the movie title is recognized
    if request.titre not in indices.index:
        raise HTTPException(status_code=404, detail="Unknown movie title.")
    try:
        recommendations = hybride_reco(user_id, svd_model, request.titre) 
        titles = recommendations['title']
        return {"user_id": user_id, "recommendations": titles.tolist()}  # Conversion en dictionnaire pour JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 