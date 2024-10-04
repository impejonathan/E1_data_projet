from fastapi import APIRouter, Depends
from database.search import get_data_from_db, get_data_by_price_diameter, get_data_by_dimensions
from routers.auth_router import oauth2_scheme

router = APIRouter()

@router.get("/search/{marque}")
def read_data(marque: str, token: str = Depends(oauth2_scheme)):
    data = get_data_from_db(marque)
    return {"data": data}

@router.get("/Prix_Diametre")
def read_data_by_price_diameter(price_min: int, price_max: int, diameter: int, token: str = Depends(oauth2_scheme)):
    data = get_data_by_price_diameter(price_min, price_max, diameter)
    return {"data": data}

@router.get("/Largeur_Hauteur_Diametre")
def read_data_by_dimensions(largeur: int, hauteur: int, diametre: int, token: str = Depends(oauth2_scheme)):
    data = get_data_by_dimensions(largeur, hauteur, diametre)
    return {"data": data}
