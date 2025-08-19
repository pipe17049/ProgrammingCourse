#!/bin/bash

# Script básico de saludo
# Descripción: Un comando simple que saluda al usuario
# Uso: ./01_hello_command.sh

# Obtener el nombre del usuario actual
USERNAME=$(whoami)

# Obtener la fecha y hora actual
CURRENT_TIME=$(date '+%Y-%m-%d %H:%M:%S')

# Función para mostrar un saludo personalizado
show_greeting() {
    echo "============================================"
    echo "¡Hola, $USERNAME!"
    echo "Fecha y hora: $CURRENT_TIME"
    echo "Sistema: $(uname -s)"
    echo "Directorio actual: $(pwd)"
    echo "============================================"
}

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [OPCION]"
    echo ""
    echo "Opciones:"
    echo "  -h, --help     Mostrar esta ayuda"
    echo "  -s, --simple   Saludo simple"
    echo "  (sin opciones) Saludo completo"
    echo ""
    echo "Ejemplos:"
    echo "  $0              # Saludo completo"
    echo "  $0 --simple     # Saludo simple"
}

# Procesamiento de argumentos básico
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    -s|--simple)
        echo "¡Hola, $USERNAME!"
        exit 0
        ;;
    "")
        show_greeting
        exit 0
        ;;
    *)
        echo "ERROR: Opción no reconocida: $1"
        echo "Usa '$0 --help' para ver las opciones disponibles"
        exit 1
        ;;
esac
