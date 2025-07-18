#!/bin/bash

# Script para demostrar la diferencia entre desarrollo y producción

echo "🎯 Build and Test Script for Producer-Consumer System"
echo "====================================================="

show_help() {
    echo ""
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  dev       - Modo desarrollo (hot reload)"
    echo "  prod      - Modo producción (código embebido)"
    echo "  build     - Solo construir imágenes"
    echo "  export    - Exportar imágenes para distribución"
    echo "  test      - Probar diferencias entre dev y prod"
    echo "  help      - Mostrar esta ayuda"
    echo ""
}

build_images() {
    echo "🔨 Construyendo imágenes..."
    docker-compose -f docker-compose.prod.yml build
    echo "✅ Imágenes construidas"
}

run_development() {
    echo "🚀 Iniciando en modo DESARROLLO (hot reload)..."
    echo "📁 Código: Desde archivos locales (volumes)"
    echo "🔄 Auto-reload: ACTIVADO"
    echo ""
    docker-compose -f docker-compose.dev.yml up
}

run_production() {
    echo "🚀 Iniciando en modo PRODUCCIÓN (standalone)..."
    echo "📦 Código: Embebido en la imagen"
    echo "🔒 Auto-reload: DESACTIVADO"
    echo ""
    docker-compose -f docker-compose.prod.yml up
}

export_images() {
    echo "📦 Exportando imágenes para distribución..."
    
    # Obtener nombres de las imágenes
    producer_image=$(docker-compose -f docker-compose.prod.yml config | grep "image:" | grep producer | awk '{print $2}' || echo "chapter-ci-producer")
    consumer_image=$(docker-compose -f docker-compose.prod.yml config | grep "image:" | grep consumer | awk '{print $2}' || echo "chapter-ci-consumer")
    
    # Usar nombres por defecto si no se encuentran
    producer_image="chapter-ci-producer"
    consumer_image="chapter-ci-consumer"
    
    echo "📤 Exportando $producer_image..."
    docker save -o producer-image.tar $producer_image
    
    echo "📤 Exportando $consumer_image..."
    docker save -o consumer-image.tar $consumer_image
    
    echo "✅ Imágenes exportadas:"
    echo "   📁 producer-image.tar"
    echo "   📁 consumer-image.tar"
    echo ""
    echo "💡 Para importar en otra máquina:"
    echo "   docker load -i producer-image.tar"
    echo "   docker load -i consumer-image.tar"
}

test_differences() {
    echo "🧪 Demostrando diferencias entre DEV y PROD..."
    echo ""
    
    echo "🔍 DESARROLLO (con volumes):"
    echo "   - Código en: /host/path/Chapter-CI/my_first_ci_project"
    echo "   - Container ve: Archivos del host en tiempo real"
    echo "   - Cambios: Se aplican inmediatamente"
    echo "   - Uso: Solo desarrollo local"
    echo ""
    
    echo "🔍 PRODUCCIÓN (sin volumes):"
    echo "   - Código en: Embebido dentro de la imagen"
    echo "   - Container ve: Snapshot del código al momento del build"
    echo "   - Cambios: Requieren rebuild de la imagen"
    echo "   - Uso: Despliegue, distribución, cloud"
    echo ""
    
    echo "📋 Para probar la diferencia:"
    echo "1. docker-compose -f docker-compose.dev.yml up -d"
    echo "2. Edita api/views.py y guarda"
    echo "3. Verás logs: 'views.py changed, reloading'"
    echo "4. docker-compose down"
    echo "5. docker-compose -f docker-compose.prod.yml up -d"
    echo "6. Edita api/views.py y guarda"
    echo "7. NO verás cambios (código está embebido)"
}

# Main logic
case "${1:-help}" in
    "dev")
        run_development
        ;;
    "prod")
        run_production
        ;;
    "build")
        build_images
        ;;
    "export")
        build_images
        export_images
        ;;
    "test")
        test_differences
        ;;
    "help"|*)
        show_help
        ;;
esac 