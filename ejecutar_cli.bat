@echo off
chcp 65001 > nul
color 0C
title Consola NoSQL - Arena-Match

echo [*] Iniciando aplicación de consola (CLI) NoSQL...
:: Ejecutar con el python del entorno virtual compartido
"C:\Users\jeanc\Desktop\Grupo 8 Fase 7\BDD2 Syncro\venv\Scripts\python.exe" cli_app.py
pause
