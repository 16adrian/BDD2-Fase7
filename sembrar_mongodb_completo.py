import os
import json
from pymongo import MongoClient

def seed():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['ArenaMatchNoSQL']
    
    # Limpiar colecciones
    db.Usuarios.drop()
    db.Equipos.drop()
    db.PartidasTelemetria.drop()
    db.Torneos.drop()
    db.Pagos.drop()
    
    # Ruta de archivos base
    data_dir = r"C:\Users\jeanc\Desktop\Universidad\BDD2 AuraFleet\ArenaMatch_Fase5-6\Datos Migrados JSON"
    
    # 1. Usuarios
    with open(os.path.join(data_dir, "usuarios.json"), "r", encoding="utf-8") as f:
        usuarios = json.load(f)
    for u in usuarios:
        u["apodoGamer"] = u.get("apodoGamer", "")
        u["equipoId"] = u.get("equipoId", None)
        
    db.Usuarios.insert_many(usuarios)
    print(f"Seeded {len(usuarios)} users into MongoDB.")
    
    # 2. Equipos
    with open(os.path.join(data_dir, "equipos.json"), "r", encoding="utf-8") as f:
        equipos = json.load(f)
    db.Equipos.insert_many(equipos)
    print(f"Seeded {len(equipos)} teams into MongoDB.")
    
    # Actualizar equipoId en los usuarios según el roster de equipos
    for eq in equipos:
        eq_id = eq.get("equipoId")
        jugadores = eq.get("jugadores", [])
        if jugadores:
            for j in jugadores:
                db.Usuarios.update_one({"usuarioId": int(j["usuarioId"])}, {"$set": {"equipoId": int(eq_id)}})
    
    # 3. PartidasTelemetria
    with open(os.path.join(data_dir, "partidas_telemetria.json"), "r", encoding="utf-8") as f:
        partidas = json.load(f)
    db.PartidasTelemetria.insert_many(partidas)
    print(f"Seeded {len(partidas)} game telemetries into MongoDB.")
    
    # 4. Torneos
    torneos = [
        {
            "torneoId": 1,
            "nombreTorneo": "Copa Latinoamericana LoL 2026",
            "videojuego": "League of Legends",
            "fechaInicio": "2026-06-01",
            "fechaFin": "2026-06-30",
            "premioPool": 10000.00,
            "costoInscripcion": 100.00,
            "estadoTorneo": "En Curso"
        },
        {
            "torneoId": 2,
            "nombreTorneo": "Valorant Challengers Latam",
            "videojuego": "Valorant",
            "fechaInicio": "2026-07-01",
            "fechaFin": "2026-07-20",
            "premioPool": 8000.00,
            "costoInscripcion": 80.00,
            "estadoTorneo": "Inscripciones Abiertas"
        },
        {
            "torneoId": 3,
            "nombreTorneo": "EA FC Masters 2026",
            "videojuego": "EA Sports FC",
            "fechaInicio": "2026-08-01",
            "fechaFin": "2026-08-15",
            "premioPool": 5000.00,
            "costoInscripcion": 50.00,
            "estadoTorneo": "Planificacion"
        }
    ]
    db.Torneos.insert_many(torneos)
    print(f"Seeded {len(torneos)} tournaments into MongoDB.")
    
    # 5. Pagos
    pagos = [
        {
            "pagoId": 1,
            "equipoId": 1,
            "torneoId": 1,
            "montoPago": 100.00,
            "fechaPago": "2026-05-25",
            "metodoPago": "Tarjeta"
        },
        {
            "pagoId": 2,
            "equipoId": 2,
            "torneoId": 1,
            "montoPago": 100.00,
            "fechaPago": "2026-05-26",
            "metodoPago": "Tarjeta"
        }
    ]
    db.Pagos.insert_many(pagos)
    print(f"Seeded {len(pagos)} payments into MongoDB.")
    
    client.close()

if __name__ == "__main__":
    seed()
