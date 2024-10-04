from .db_connection import create_conn

def get_data_from_db(marque):
    cursor = create_conn()
    query = f"SELECT * FROM Produit WHERE Marque = '{marque}'"
    cursor.execute(query)
    data = cursor.fetchall()
    # Convertir les données en une liste de dictionnaires
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in data]
    return results

def get_data_by_price_diameter(price_min, price_max, diameter):
    cursor = create_conn()
    query = f"""
    SELECT P.*, C.*, D.*
    FROM Produit P
    JOIN Caracteristiques C ON P.ID_Produit = C.ID_Produit
    JOIN Dimensions D ON P.ID_Produit = D.ID_Produit
    WHERE P.Prix BETWEEN {price_min} AND {price_max} AND D.Diametre = {diameter}
    ORDER BY P.Prix ASC
    """
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in data]
    return results

def get_data_by_dimensions(largeur, hauteur, diametre):
    cursor = create_conn()
    query = f"""
    SELECT P.Marque, P.Prix, P.Note, P.URL_Produit
    FROM Produit P
    JOIN Dimensions D ON P.ID_Produit = D.ID_Produit
    WHERE D.Largeur = {largeur} AND D.Hauteur = {hauteur} AND D.Diametre = {diametre}
    ORDER BY P.Prix ASC
    """
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in data]
    return results
