#!/usr/bin/env python3
"""
🔍 SCRIPT DE DIAGNÓSTICO PARA WINDOWS
Verifica por qué el auto-scaling no funciona en Windows
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
    print("🔍 DIAGNÓSTICO DE AUTO-SCALING PARA WINDOWS")
    print("=" * 60)
    
    # 1. Verificar Kubernetes
    print("\n1️⃣ VERIFICANDO KUBERNETES")
    run_cmd("kubectl version --client", "Kubectl version")
    run_cmd("kubectl cluster-info", "Cluster info")
    
    # 2. Verificar Docker recursos
    print("\n2️⃣ VERIFICANDO DOCKER RESOURCES")
    run_cmd("docker info | findstr /i cpu || docker info | grep -i cpu", "Docker CPU")
    run_cmd("docker info | findstr /i memory || docker info | grep -i memory", "Docker Memory")
    
    # 3. Verificar Metrics Server
    print("\n3️⃣ VERIFICANDO METRICS SERVER")
    run_cmd("kubectl get deployment metrics-server -n kube-system", "Metrics Server Deployment")
    run_cmd("kubectl get pods -n kube-system | findstr metrics || kubectl get pods -n kube-system | grep metrics", "Metrics Server Pods")
    run_cmd("kubectl logs deployment/metrics-server -n kube-system --tail=10", "Metrics Server Logs")
    
    # 4. Verificar HPA
    print("\n4️⃣ VERIFICANDO HPA")
    run_cmd("kubectl get hpa", "HPA Status")
    run_cmd("kubectl describe hpa worker-hpa", "HPA Details")
    
    # 5. Verificar workers
    print("\n5️⃣ VERIFICANDO WORKERS")
    run_cmd("kubectl get pods | findstr worker || kubectl get pods | grep worker", "Worker Pods")
    run_cmd("kubectl top pods | findstr worker || kubectl top pods | grep worker", "Worker CPU Usage")
    
    # 6. Test API endpoint
    print("\n6️⃣ TESTING API ENDPOINT")
    print("Enviando una tarea de prueba...")
    run_cmd('curl -X POST "http://localhost:8000/api/process-batch/distributed/" -H "Content-Type: application/json" -d "{\\"filters\\": [\\"resize\\"], \\"count\\": 1}"', "Test API call")
    
    print("\n" + "=" * 60)
    print("✅ DIAGNÓSTICO COMPLETADO")
    print("📋 VERIFICA LOS RESULTADOS ARRIBA PARA IDENTIFICAR PROBLEMAS")

if __name__ == "__main__":
    main()