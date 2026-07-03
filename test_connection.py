import os
import json
import pymongo
from pymongo.errors import PyMongoError

print("======================================================================")
print(" DIAGNÓSTICO DE CONEXIÓN A BASE DE DATOS - ARENA-MATCH (MONGODB) ")
print("======================================================================")

# Cargar configuración de db_config.json
config_path = "db_config.json"
mongo_uri = "mongodb://localhost:27017/"

if os.path.exists(config_path):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            mongo_uri = config.get("MONGO_URI", mongo_uri)
    except Exception as e:
        print(f" [!] Aviso: Error al leer db_config.json: {e}")

try:
    # Conectarse a MongoDB
    client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
    # Ping
    client.admin.command('ping')
    db = client['ArenaMatchNoSQL']
    print(f" [+] Conexión exitosa a MongoDB Local ({mongo_uri})!")
    
    # Colecciones
    cols = db.list_collection_names()
    print(f" [+] Colecciones encontradas: {cols}")
    
    # Documentos
    user_docs = db.Usuarios.count_documents({})
    team_docs = db.Equipos.count_documents({})
    torneo_docs = db.Torneos.count_documents({})
    pago_docs = db.Pagos.count_documents({})
    partidas_docs = db.PartidasTelemetria.count_documents({})
    
    print(f" [+] Cantidad de documentos en 'Usuarios': {user_docs}")
    print(f" [+] Cantidad de documentos en 'Equipos': {team_docs}")
    print(f" [+] Cantidad de documentos en 'Torneos': {torneo_docs}")
    print(f" [+] Cantidad de documentos en 'Pagos': {pago_docs}")
    print(f" [+] Cantidad de documentos en 'PartidasTelemetria': {partidas_docs}")
    
    client.close()
    print("\n[OK] ¡Diagnóstico completado con éxito! Todo está en orden para MongoDB.")
except Exception as e:
    print(f" [X] ERROR al intentar conectar a MongoDB:")
    print(f"     Detalles: {e}")

print("======================================================================")
