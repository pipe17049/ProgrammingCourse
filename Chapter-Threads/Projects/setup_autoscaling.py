#!/usr/bin/env python3
"""
Setup script cross-platform para Auto-Scaling System
Funciona en Windows, Mac, Linux
"""

import sys
import subprocess
import platform
import os
from pathlib import Path

class AutoScalingSetup:
    """Setup automatizado para el sistema de auto-scaling"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.python_cmd = self._get_python_command()
        self.project_root = Path(__file__).parent
        
    def run_complete_setup(self):
        """Ejecuta setup completo"""
        print("🚀 AUTO-SCALING SYSTEM SETUP")
        print("=" * 50)
        print(f"Sistema detectado: {platform.system()} {platform.release()}")
        print(f"Python: {sys.version}")
        print(f"Directorio: {self.project_root}")
        print()
        
        steps = [
            ("Verificar Python", self._check_python),
            ("Instalar dependencias", self._install_dependencies),
            ("Crear directorios", self._create_directories),
            ("Verificar Docker", self._check_docker),
            ("Configurar environment", self._setup_environment),
            ("Verificar instalación", self._verify_installation),
        ]
        
        for step_name, step_func in steps:
            print(f"📋 {step_name}...")
            try:
                success = step_func()
                if success:
                    print(f"✅ {step_name} - OK")
                else:
                    print(f"❌ {step_name} - FAILED")
                    return False
            except Exception as e:
                print(f"❌ {step_name} - ERROR: {e}")
                return False
            print()
        
        self._show_success_message()
        return True
    
    def _get_python_command(self):
        """Detecta comando Python correcto"""
        commands = ['python3', 'python', 'py']
        
        for cmd in commands:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0 and '3.' in result.stdout:
                    return cmd
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        return 'python'  # Fallback
    
    def _check_python(self):
        """Verifica versión de Python"""
        version = sys.version_info
        if version.major != 3 or version.minor < 8:
            print(f"❌ Python 3.8+ requerido, tienes {version.major}.{version.minor}")
            return False
        
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    
    def _install_dependencies(self):
        """Instala dependencias Python"""
        requirements_files = [
            'requirements.txt',
            'requirements_autoscaling.txt'
        ]
        
        # Actualizar pip primero
        print("   Actualizando pip...")
        try:
            subprocess.run([self.python_cmd, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                         check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("   ⚠️ No se pudo actualizar pip, continuando...")
        
        # Instalar requirements
        for req_file in requirements_files:
            req_path = self.project_root / req_file
            if req_path.exists():
                print(f"   Instalando desde {req_file}...")
                try:
                    # Usar --only-binary para evitar problemas de compilación en Windows
                    cmd = [
                        self.python_cmd, '-m', 'pip', 'install', 
                        '-r', str(req_path),
                        '--only-binary=opencv-python,numpy',
                        '--prefer-binary'
                    ]
                    subprocess.run(cmd, check=True, capture_output=True)
                    print(f"   ✅ {req_file} instalado")
                except subprocess.CalledProcessError as e:
                    print(f"   ❌ Error instalando {req_file}: {e}")
                    # Intentar instalación básica sin flags
                    try:
                        cmd_basic = [self.python_cmd, '-m', 'pip', 'install', '-r', str(req_path)]
                        subprocess.run(cmd_basic, check=True, capture_output=True)
                        print(f"   ✅ {req_file} instalado (básico)")
                    except subprocess.CalledProcessError:
                        return False
        
        return True
    
    def _create_directories(self):
        """Crea directorios necesarios"""
        directories = [
            'static/processed',
            'logs',
            'monitoring',
            'scripts',
            'tests'
        ]
        
        for dir_name in directories:
            dir_path = self.project_root / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   📁 {dir_name}")
        
        return True
    
    def _check_docker(self):
        """Verifica Docker (opcional)"""
        docker_commands = ['docker', 'docker.exe']
        
        for cmd in docker_commands:
            try:
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"   ✅ Docker disponible: {result.stdout.strip()}")
                    
                    # Verificar docker-compose
                    compose_commands = ['docker-compose', 'docker compose']
                    for compose_cmd in compose_commands:
                        try:
                            result = subprocess.run(compose_cmd.split() + ['--version'], 
                                                  capture_output=True, text=True, timeout=10)
                            if result.returncode == 0:
                                print(f"   ✅ Docker Compose disponible")
                                return True
                        except (subprocess.TimeoutExpired, FileNotFoundError):
                            continue
                    
                    print("   ⚠️ Docker encontrado pero Docker Compose no disponible")
                    return True
                    
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        print("   ⚠️ Docker no encontrado - Sistema funcionará en modo local")
        return True  # No es crítico
    
    def _setup_environment(self):
        """Configura variables de environment"""
        env_vars = {
            'REDIS_HOST': 'localhost',
            'REDIS_PORT': '6379',
            'DJANGO_SETTINGS_MODULE': 'django_image_server.settings'
        }
        
        # Crear archivo .env si no existe
        env_file = self.project_root / '.env'
        if not env_file.exists():
            with open(env_file, 'w') as f:
                f.write("# Auto-Scaling System Environment Variables\n")
                for key, value in env_vars.items():
                    f.write(f"{key}={value}\n")
            print(f"   📄 .env creado con variables por defecto")
        else:
            print(f"   📄 .env ya existe")
        
        return True
    
    def _verify_installation(self):
        """Verifica que todo esté instalado correctamente"""
        critical_packages = [
            'django',
            'redis', 
            'psutil',
            'PIL',  # Pillow
            'requests'
        ]
        
        for package in critical_packages:
            try:
                __import__(package)
                print(f"   ✅ {package}")
            except ImportError:
                print(f"   ❌ {package} - NO DISPONIBLE")
                return False
        
        # Verificar OpenCV separadamente (nombre diferente)
        try:
            import cv2
            print(f"   ✅ opencv-python")
        except ImportError:
            print(f"   ❌ opencv-python - NO DISPONIBLE")
            return False
        
        return True
    
    def _show_success_message(self):
        """Muestra mensaje de éxito con instrucciones"""
        print("🎉 SETUP COMPLETADO EXITOSAMENTE!")
        print("=" * 50)
        print()
        print("📋 PRÓXIMOS PASOS:")
        print()
        print("1️⃣  Iniciar sistema básico:")
        print(f"   {self.python_cmd} manage.py runserver 8000")
        print()
        print("2️⃣  Iniciar sistema distribuido (si tienes Docker):")
        print("   docker-compose up -d")
        print()
        print("3️⃣  Probar auto-scaling:")
        print(f"   {self.python_cmd} scripts/auto_scaling_cli.py interactive")
        print()
        print("4️⃣  Dashboard en tiempo real:")
        print(f"   {self.python_cmd} monitoring/dashboard.py --auto-scale")
        print()
        print("🚀 COMANDOS ÚTILES:")
        print()
        print("   # Demo completo")
        print(f"   {self.python_cmd} scripts/auto_scaling_cli.py demo")
        print()
        print("   # Stress test")
        print(f"   {self.python_cmd} scripts/auto_scaling_cli.py stress --tasks 25")
        print()
        print("   # Verificar métricas")
        print(f"   {self.python_cmd} scripts/auto_scaling_cli.py metrics")
        print()
        print("📚 Para más información, ver:")
        print("   - README.md")
        print("   - daily_guides/DAY4_FRIDAY_AUTO_SCALING.md")
        print()
        print("🔧 Si hay problemas:")
        print("   - Verificar que Redis esté corriendo (para sistema distribuido)")
        print("   - Verificar que Docker esté corriendo (para workers)")
        print("   - Revisar logs/ directory para errores")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Auto-Scaling System Setup')
    parser.add_argument('--check-only', action='store_true', 
                       help='Solo verificar requisitos, no instalar')
    parser.add_argument('--minimal', action='store_true',
                       help='Instalación mínima (sin OpenCV)')
    
    args = parser.parse_args()
    
    setup = AutoScalingSetup()
    
    if args.check_only:
        print("🔍 VERIFICACIÓN DE REQUISITOS")
        print("=" * 40)
        
        # Solo verificar sin instalar
        success = (setup._check_python() and 
                  setup._check_docker() and 
                  setup._verify_installation())
        
        if success:
            print("\n✅ Sistema listo para usar")
        else:
            print("\n❌ Faltan requisitos - ejecutar sin --check-only")
            sys.exit(1)
    else:
        # Setup completo
        success = setup.run_complete_setup()
        if not success:
            print("\n❌ Setup falló - revisar errores arriba")
            sys.exit(1)

if __name__ == "__main__":
    main()