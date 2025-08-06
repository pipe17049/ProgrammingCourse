#!/usr/bin/env python3
"""
🔧 SCRIPT DE FIXES PARA WINDOWS
Aplica fixes específicos para problemas comunes en Windows
"""
import subprocess
import sys
import time

def run_cmd(cmd, description=""):
    """Run command and show output"""
    if description:
        print(f"\n> {description}")
        print("=" * 50)
    
    print(f"$ {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("🔧 FIXES PARA WINDOWS - AUTO-SCALING")
    print("=" * 50)
    
    print("\n1️⃣ REINICIANDO METRICS SERVER...")
    run_cmd("kubectl delete deployment metrics-server -n kube-system", "Delete metrics server")
    time.sleep(5)
    run_cmd("kubectl apply -f metrics-server.yaml", "Apply metrics server")
    
    print("\n2️⃣ ESPERANDO METRICS SERVER...")
    time.sleep(30)
    run_cmd("kubectl get pods -n kube-system | findstr metrics || kubectl get pods -n kube-system | grep metrics", "Check metrics pods")
    
    print("\n3️⃣ REINICIANDO WORKERS...")
    run_cmd("kubectl rollout restart deployment/worker-deployment", "Restart workers")
    time.sleep(20)
    
    print("\n4️⃣ VERIFICANDO HPA...")
    for i in range(5):
        print(f"\nCheck {i+1}/5:")
        run_cmd("kubectl get hpa", f"HPA status check {i+1}")
        time.sleep(10)
    
    print("\n5️⃣ GENERANDO CARGA DE PRUEBA...")
    run_cmd("kubectl port-forward service/api-service 8001:8000", "Port forward (run in separate terminal)")
    
    print("\n" + "=" * 50)
    print("✅ FIXES APLICADOS")
    print("📋 AHORA EJECUTA EL DEMO DE NUEVO")
    print("💡 EN WINDOWS:")
    print("   1. Abre otra terminal")
    print("   2. Ejecuta: kubectl port-forward service/api-service 8001:8000")
    print("   3. Ejecuta: python debug-windows.py")

if __name__ == "__main__":
    main()