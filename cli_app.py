import os
import sys
import json
from datetime import datetime
import pymongo
from pymongo.errors import PyMongoError

# Configuración de conexión local
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "ArenaMatchNoSQL"

def get_db_connection():
    """
    Intenta conectarse a la base de datos local 'ArenaMatchNoSQL' en MongoDB.
    Realiza un ping para comprobar la disponibilidad del servidor.
    """
    try:
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        # Ping para validar conexión
        client.admin.command('ping')
        return client, client[DB_NAME]
    except PyMongoError as e:
        print("\n[X] ERROR DE CONEXIÓN A MONGODB:")
        print(f"    No se pudo establecer conexión con '{MONGO_URI}'.")
        print(f"    Detalles: {e}\n")
        print("[*] Asegúrate de que el servicio de MongoDB esté activo localmente.")
        sys.exit(1)

def mostrar_menu():
    print("\n" + "="*50)
    print("      ARENA-MATCH: CONSOLA DE OPERACIONES NOSQL  ")
    print("="*50)
    print(" 1. Crear Gamer (Create)")
    print(" 2. Consultar Gamers / Listar Todos (Read)")
    print(" 3. Actualizar Datos de Gamer (Update)")
    print(" 4. Eliminar Gamer (Delete)")
    print(" 5. Agregación: Top League of Legends Players")
    print(" 6. Agregación: Fondos de Patrocinios por Equipo")
    print(" 0. Salir del Programa")
    print("="*50)

def crear_gamer(db):
    print("\n--- [1] CREAR GAMER EN MONGODB ---")
    try:
        nombre = input("Nombres del Gamer: ").strip()
        apellido = input("Apellidos del Gamer: ").strip()
        email = input("Correo Electrónico: ").strip()
        
        # Validar tipo de usuario
        print("Roles de Usuario: Jugador, Administrador, Arbitro, Patrocinador")
        tipo = input("Rol del Gamer [Jugador]: ").strip() or "Jugador"
        if tipo not in ['Jugador', 'Administrador', 'Arbitro', 'Patrocinador']:
            tipo = 'Jugador'
            
        apodo = input("Apodo Gamer (Gamertag): ").strip()
        
        # Calcular ID autoincremental
        max_user = list(db.Usuarios.find().sort("usuarioId", -1).limit(1))
        new_id = (max_user[0]["usuarioId"] + 1) if max_user else 1
        
        doc = {
            "usuarioId": new_id,
            "nombreUsuario": nombre,
            "apellidoUsuario": apellido,
            "emailUsuario": email,
            "passwordHash": "pbkdf2_sha256$1200000$LHLdXOHJUu61dYZ4soYgE5$Cv53YJ/akdsrmtG/5G1mU91RhPKobWDV2uHWKlLddv8=",
            "tipoUsuario": tipo,
            "fechaRegistro": datetime.now().strftime("%Y-%m-%d"),
            "apodoGamer": apodo if apodo else "",
            "equipoId": None,
            "torneos_jugados": []
        }
        
        db.Usuarios.insert_one(doc)
        print(f"\n[OK] ¡Gamer registrado exitosamente en MongoDB!")
        print(f"     ID de Negocio asignado: {new_id}")
    except Exception as e:
        print(f"\n[X] Error al insertar en la base de datos: {e}")

def consultar_gamers(db):
    print("\n--- [2] CONSULTAR GAMERS / LISTAR TODOS ---")
    opcion = input("¿Deseas buscar por ID [1] o listar todos [2]?: ").strip()
    
    if opcion == "1":
        try:
            uid_in = input("Ingresa el ID del usuario (usuarioId): ").strip()
            uid = int(uid_in)
            user = db.Usuarios.find_one({"usuarioId": uid})
            if user:
                print("\nDocumento Encontrado:")
                user.pop("_id", None) # Quitar _id interno para legibilidad
                print(json.dumps(user, indent=4, ensure_ascii=False))
            else:
                print(f"\n[-] No se encontró ningún gamer con ID: {uid}")
        except ValueError:
            print("\n[X] Entrada inválida. El ID debe ser un número entero.")
        except Exception as e:
            print(f"\n[X] Error al buscar en la base de datos: {e}")
            
    elif opcion == "2":
        try:
            users = list(db.Usuarios.find({}).sort("usuarioId", 1))
            print(f"\nTotal de usuarios registrados: {len(users)}")
            print("-" * 75)
            print(f"{'ID':<5} | {'NOMBRES Y APELLIDOS':<30} | {'ROL':<15} | {'GAMERTAG':<15}")
            print("-" * 75)
            for u in users:
                nom_comp = f"{u.get('nombreUsuario')} {u.get('apellidoUsuario')}"
                print(f"{u.get('usuarioId'):<5} | {nom_comp:<30} | {u.get('tipoUsuario'):<15} | {u.get('apodoGamer', 'N/A'):<15}")
            print("-" * 75)
        except Exception as e:
            print(f"\n[X] Error al consultar colecciones: {e}")
    else:
        print("\n[X] Opción inválida.")

def actualizar_gamer(db):
    print("\n--- [3] ACTUALIZAR DATOS DE GAMER ---")
    try:
        uid_in = input("Ingresa el ID del usuario a modificar (usuarioId): ").strip()
        uid = int(uid_in)
        user = db.Usuarios.find_one({"usuarioId": uid})
        if not user:
            print(f"\n[-] No se encontró ningún gamer con ID: {uid}")
            return
            
        print(f"\nModificando gamer: {user.get('nombreUsuario')} {user.get('apellidoUsuario')} ({user.get('apodoGamer')})")
        nombre = input(f"Nuevos Nombres [{user.get('nombreUsuario')}]: ").strip() or user.get('nombreUsuario')
        apellido = input(f"Nuevos Apellidos [{user.get('apellidoUsuario')}]: ").strip() or user.get('apellidoUsuario')
        tipo = input(f"Nuevo Rol [{user.get('tipoUsuario')}]: ").strip() or user.get('tipoUsuario')
        apodo = input(f"Nuevo Gamertag [{user.get('apodoGamer')}]: ").strip() or user.get('apodoGamer')
        
        db.Usuarios.update_one(
            {"usuarioId": uid},
            {"$set": {
                "nombreUsuario": nombre,
                "apellidoUsuario": apellido,
                "tipoUsuario": tipo,
                "apodoGamer": apodo
            }}
        )
        print(f"\n[OK] ¡Documento del gamer {uid} actualizado con éxito!")
    except ValueError:
        print("\n[X] Entrada inválida. El ID debe ser un número entero.")
    except Exception as e:
        print(f"\n[X] Error al actualizar base de datos: {e}")

def eliminar_gamer(db):
    print("\n--- [4] ELIMINAR GAMER EN MONGODB ---")
    try:
        uid_in = input("Ingresa el ID del usuario a eliminar (usuarioId): ").strip()
        uid = int(uid_in)
        user = db.Usuarios.find_one({"usuarioId": uid})
        if not user:
            print(f"\n[-] No se encontró ningún gamer con ID: {uid}")
            return
            
        print(f"\n¿Estás seguro de eliminar a {user.get('nombreUsuario')} {user.get('apellidoUsuario')} ({user.get('apodoGamer')})?")
        confirmar = input("Escribe 'SI' para confirmar: ").strip().upper()
        
        if confirmar == "SI":
            db.Usuarios.delete_one({"usuarioId": uid})
            print(f"\n[OK] ¡El gamer con ID {uid} ha sido eliminado definitivamente de MongoDB!")
        else:
            print("\n[-] Operación cancelada por el usuario.")
    except ValueError:
        print("\n[X] Entrada inválida. El ID debe ser un número entero.")
    except Exception as e:
        print(f"\n[X] Error al eliminar de la base de datos: {e}")

def aggregate_top_players(db):
    print("\n--- [5] REPORTE: TOP LEAGUE OF LEGENDS PLAYERS ---")
    print("Consolidando kills y asistencias totales acumuladas desde PartidasTelemetria...")
    try:
        pipeline = [
            { "$match": { "videojuego": "League of Legends" } },
            {
                "$project": {
                    "jugadores_partida": { "$concatArrays": [ "$equipo1.jugadores", "$equipo2.jugadores" ] }
                }
            },
            { "$unwind": "$jugadores_partida" },
            {
                "$group": {
                    "_id": "$jugadores_partida.nombreUsuario",
                    "totalKills": { "$sum": "$jugadores_partida.kills" },
                    "totalAsistencias": { "$sum": "$jugadores_partida.assists" }
                }
            },
            { "$sort": { "totalKills": -1 } },
            {
                "$project": {
                    "_id": 0,
                    "nombreUsuario": "$_id",
                    "kills": "$totalKills",
                    "asistencias": "$totalAsistencias"
                }
            }
        ]
        results = list(db.PartidasTelemetria.aggregate(pipeline))
        
        if not results:
            print("\n[-] No se encontraron registros de partidas de LoL para agregar.")
            return
            
        print("-" * 55)
        print(f"{'JUGADOR':<25} | {'KILLS TOTALES':<12} | {'ASISTENCIAS':<12}")
        print("-" * 55)
        for r in results:
            print(f"{r['nombreUsuario']:<25} | {r['kills']:<12} | {r['asistencias']:<12}")
        print("-" * 55)
    except Exception as e:
        print(f"\n[X] Error al ejecutar agregación de telemetría: {e}")

def aggregate_sponsorship_funds(db):
    print("\n--- [6] REPORTE: FONDOS DE PATROCINIOS POR EQUIPO ---")
    print("Consolidando total recaudado desglosando marcas patrocinadoras de Equipos...")
    try:
        pipeline = [
            { "$unwind": "$patrocinadores" },
            {
                "$group": {
                    "_id": "$nombreEquipo",
                    "totalRecaudadoPatrocinio": { "$sum": "$patrocinadores.montoContrato" },
                    "cantidadMarcas": { "$sum": 1 }
                }
            },
            { "$sort": { "totalRecaudadoPatrocinio": -1 } },
            {
                "$project": {
                    "_id": 0,
                    "nombreEquipo": "$_id",
                    "totalPatrocinio": "$totalRecaudadoPatrocinio",
                    "marcas": "$cantidadMarcas"
                }
            }
        ]
        results = list(db.Equipos.aggregate(pipeline))
        
        if not results:
            print("\n[-] No se encontraron patrocinios registrados en los equipos.")
            return
            
        print("-" * 55)
        print(f"{'EQUIPO':<20} | {'TOTAL CONTRATOS ($)':<18} | {'MARCAS SPONSORS'}")
        print("-" * 55)
        for r in results:
            print(f"{r['nombreEquipo']:<20} | ${r['totalPatrocinio']:<17.2f} | {r['marcas']}")
        print("-" * 55)
    except Exception as e:
        print(f"\n[X] Error al ejecutar agregación de patrocinios: {e}")

def main():
    # Establecer conexión
    client, db = get_db_connection()
    
    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción [0-6]: ").strip()
        
        if opcion == "1":
            crear_gamer(db)
        elif opcion == "2":
            consultar_gamers(db)
        elif opcion == "3":
            actualizar_gamer(db)
        elif opcion == "4":
            eliminar_gamer(db)
        elif opcion == "5":
            aggregate_top_players(db)
        elif opcion == "6":
            aggregate_sponsorship_funds(db)
        elif opcion == "0":
            print("\nCerrando conexión y saliendo de la consola. ¡Hasta pronto!\n")
            client.close()
            break
        else:
            print("\n[X] Opción no válida. Ingresa un número del 0 al 6.")
            
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[-] Programa interrumpido por teclado. Saliendo de forma segura...\n")
