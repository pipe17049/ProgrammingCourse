#!/usr/bin/env python3
"""
🔧 SCRIPT PARA ARREGLAR RUTAS DE WINDOWS EN KUBERNETES
Detecta automáticamente la ruta correcta del usuario y actualiza worker-deployment-windows.yaml
"""
import os
import platform
import subprocess
import sys
from pathlib import Path

def get_windows_project_path():
    """Detecta la ruta correcta del proyecto en Windows"""
    
    # Obtener la ruta actual del script
    current_path = Path(__file__).parent.parent.absolute()
    print(f"📁 Ruta actual del proyecto: {current_path}")
    
    # Convertir a ruta de Docker Desktop para Windows
    # C:\Users\usuario\... → /run/desktop/mnt/host/c/Users/usuario/...
    
    # Obtener las partes de la ruta
    parts = current_path.parts
    
    if parts[0].lower().startswith('c:'):
        # Convertir C:\ a formato Docker Desktop
        docker_path_parts = ['/run/desktop/mnt/host/c'] + list(parts[1:])
        docker_path = '/'.join(docker_path_parts)
        
        print(f"🐳 Ruta para Docker Desktop: {docker_path}")
        return docker_path
    else:
        print(f"❌ No se detectó una ruta de C:\ - Ruta actual: {current_path}")
        return None

def update_windows_deployment(docker_path):
    """Actualiza worker-deployment-windows.yaml con la ruta correcta"""
    
    deployment_file = Path(__file__).parent / "worker-deployment-windows.yaml"
    
    if not deployment_file.exists():
        print(f"❌ No se encontró {deployment_file}")
        return False
    
    # Leer el archivo actual
    with open(deployment_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar y reemplazar las rutas
    old_pattern = "/run/desktop/mnt/host/c/Users/julia/OneDrive/Documents/Cursos/ProgrammingCourse/Chapter-Threads/Projects"
    new_pattern = docker_path
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        
        # Escribir el archivo actualizado
        with open(deployment_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Actualizado {deployment_file}")
        print(f"   Ruta anterior: {old_pattern}")
        print(f"   Ruta nueva: {new_pattern}")
        return True
    else:
        print(f"⚠️ No se encontró la ruta antigua en el archivo")
        print(f"   Buscando: {old_pattern}")
        return False

def main():
    print("🔧 ARREGLANDO RUTAS DE WINDOWS PARA KUBERNETES")
    print("=" * 60)
    
    # Verificar que estamos en Windows
    if platform.system() != "Windows":
        print("⚠️ Este script es solo para Windows")
        print(f"   Sistema detectado: {platform.system()}")
        return
    
    # Detectar la ruta correcta
    docker_path = get_windows_project_path()
    
    if not docker_path:
        print("\n❌ No se pudo detectar la ruta del proyecto")
        print("💡 SOLUCIÓN MANUAL:")
        print("   1. Anota tu ruta actual del proyecto")
        print("   2. Edita worker-deployment-windows.yaml manualmente")
        return
    
    # Verificar que las carpetas existen
    current_path = Path(__file__).parent.parent.absolute()
    static_dir = current_path / "static"
    processed_dir = static_dir / "processed"
    
    if not static_dir.exists():
        print(f"❌ No existe la carpeta static: {static_dir}")
        return
    
    if not processed_dir.exists():
        print(f"📁 Creando carpeta processed: {processed_dir}")
        processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Actualizar el archivo de deployment
    if update_windows_deployment(docker_path):
        print("\n🎯 PRÓXIMOS PASOS:")
        print("   1. kubectl delete -f worker-deployment-windows.yaml")
        print("   2. kubectl apply -f worker-deployment-windows.yaml")
        print("   3. python demo.py")
        print("\n✅ Ahora las imágenes se deberían guardar correctamente en Windows!")
    else:
        print("\n❌ No se pudo actualizar el archivo automáticamente")
        print("💡 Verifica manualmente las rutas en worker-deployment-windows.yaml")

if __name__ == "__main__":
    main()