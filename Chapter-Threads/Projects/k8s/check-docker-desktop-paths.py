#!/usr/bin/env python3
"""
🔍 DIAGNÓSTICO DE PATHS EN DOCKER DESKTOP WINDOWS
Verifica si Docker Desktop está montando correctamente las carpetas
"""
import subprocess
import platform
from pathlib import Path

def check_docker_mounts():
    """Verificar si Docker Desktop puede acceder a las carpetas del proyecto"""
    
    if platform.system() != "Windows":
        print("⚠️ Este script es específico para Windows")
        return
    
    print("🔍 DIAGNÓSTICO DE DOCKER DESKTOP EN WINDOWS")
    print("=" * 60)
    
    # Obtener la ruta actual del proyecto
    project_path = Path(__file__).parent.parent.absolute()
    static_path = project_path / "static"
    images_path = static_path / "images"
    processed_path = static_path / "processed"
    
    print(f"📁 Proyecto: {project_path}")
    print(f"📁 Static: {static_path}")
    print(f"📁 Images: {images_path}")
    print(f"📁 Processed: {processed_path}")
    
    # Verificar que las carpetas existen
    print("\n🔍 VERIFICANDO CARPETAS LOCALES:")
    print(f"   Static exists: {static_path.exists()}")
    print(f"   Images exists: {images_path.exists()}")
    print(f"   Processed exists: {processed_path.exists()}")
    
    if images_path.exists():
        images = list(images_path.glob("*.jpg"))
        print(f"   Images found: {len(images)}")
        for img in images:
            size_mb = img.stat().st_size / (1024*1024)
            print(f"     - {img.name}: {size_mb:.1f} MB")
    
    # Verificar Docker Desktop settings
    print("\n🐳 PROBANDO ACCESO CON DOCKER:")
    
    # Intentar montar la carpeta con Docker run
    docker_project_path = str(project_path).replace("\\", "/").replace("C:", "/run/desktop/mnt/host/c")
    
    test_cmd = [
        "docker", "run", "--rm",
        "-v", f"{docker_project_path}/static:/test_static",
        "alpine:latest",
        "ls", "-la", "/test_static"
    ]
    
    print(f"🧪 Test command: {' '.join(test_cmd)}")
    
    try:
        result = subprocess.run(test_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Docker Desktop puede acceder a la carpeta static:")
            print(result.stdout)
        else:
            print("❌ Docker Desktop NO puede acceder a la carpeta static:")
            print(f"Error: {result.stderr}")
            
            print("\n💡 POSIBLES SOLUCIONES:")
            print("1. Verificar Docker Desktop Settings > Resources > File Sharing")
            print("2. Asegurar que C:\\ está habilitado para compartir")
            print("3. Reiniciar Docker Desktop")
            
    except subprocess.TimeoutExpired:
        print("❌ Docker command timeout - Docker Desktop puede no estar funcionando")
    except Exception as e:
        print(f"❌ Error ejecutando Docker: {e}")

def suggest_fix():
    """Sugerir la configuración correcta para hostPath"""
    
    project_path = Path(__file__).parent.parent.absolute()
    docker_path = str(project_path).replace("\\", "/").replace("C:", "/run/desktop/mnt/host/c")
    
    print("\n🔧 CONFIGURACIÓN CORRECTA PARA worker-deployment-windows.yaml:")
    print("=" * 60)
    print(f"""
volumes:
- name: static-images
  hostPath:
    path: {docker_path}/static
    type: Directory
- name: processed-output
  hostPath:
    path: {docker_path}/static/processed
    type: DirectoryOrCreate
""")

def main():
    check_docker_mounts()
    suggest_fix()
    
    print("\n🎯 SIGUIENTE PASO:")
    print("Si el test de Docker falló, configura File Sharing en Docker Desktop")
    print("Si el test pasó, actualiza worker-deployment-windows.yaml con la ruta correcta")

if __name__ == "__main__":
    main()