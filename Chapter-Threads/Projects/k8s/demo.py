#!/usr/bin/env python3
"""
🚀 KUBERNETES AUTO-SCALING DEMO
Cross-platform demo script for the Kubernetes class
"""

import subprocess
import time
import sys
import os

def run_cmd(cmd, description=""):
    """Run command and show output"""
    if description:
        print(f"\n🔧 {description}")
        print("=" * 50)
    
    print(f"$ {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def wait_for_pods(label, timeout=60):
    """Wait for pods to be ready"""
    print(f"\n⏳ Waiting for pods with label {label} to be ready...")
    cmd = f"kubectl wait --for=condition=ready pod -l {label} --timeout={timeout}s"
    return run_cmd(cmd)

def main():
    print("🚀 KUBERNETES AUTO-SCALING DEMO")
    print("================================")
    print("Este demo funciona en Windows, Linux y Mac")
    print("")
    
    # Check if kubectl is available
    if not run_cmd("kubectl version --client", "Checking kubectl"):
        print("❌ kubectl no está instalado o no está en PATH")
        print("Instala kubectl desde: https://kubernetes.io/docs/tasks/tools/")
        sys.exit(1)
    
    # Check cluster connection
    if not run_cmd("kubectl cluster-info", "Checking cluster connection"):
        print("❌ No hay conexión a un cluster de Kubernetes")
        print("Opciones:")
        print("  - minikube start")
        print("  - kind create cluster") 
        print("  - Docker Desktop → Enable Kubernetes")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🎬 INICIANDO DEMO - AUTO-SCALING EN KUBERNETES")
    print("="*60)
    
    # Deploy Redis
    run_cmd("kubectl apply -f redis-deployment.yaml", "1️⃣ Deploying Redis")
    
    # Deploy API  
    run_cmd("kubectl apply -f api-deployment.yaml", "2️⃣ Deploying API")
    
    # Deploy Workers + HPA
    run_cmd("kubectl apply -f worker-deployment.yaml", "3️⃣ Deploying Workers + HPA")
    
    # Wait for pods
    print("\n4️⃣ Waiting for all pods to be ready...")
    wait_for_pods("app=redis")
    wait_for_pods("app=image-api") 
    wait_for_pods("app=image-worker")
    
    # Show current status
    run_cmd("kubectl get pods", "5️⃣ Current Pod Status")
    run_cmd("kubectl get hpa", "HPA Status")
    
    print("\n" + "="*60)
    print("🔥 STRESS TEST PHASE")
    print("="*60)
    
    # Setup port forwarding
    print("\n6️⃣ Setting up port forwarding to API...")
    print("En otra terminal, ejecuta:")
    print("  kubectl port-forward service/api-service 8000:8000")
    print("")
    print("Luego presiona ENTER para continuar...")
    input()
    
    # Generate load
    print("\n7️⃣ Para generar carga, ejecuta en otra terminal:")
    print("  python burst_stress.py 50")
    print("")
    print("8️⃣ Para ver auto-scaling en tiempo real, ejecuta:")
    print("  kubectl get hpa -w")
    print("  kubectl get pods -w")
    print("")
    print("Deberías ver:")
    print("  - CPU usage: 0% → 70%+")
    print("  - Pods: 2 → 4 → 6 → 8 (auto-scaling!)")
    print("")
    print("Presiona ENTER cuando termines de ver el auto-scaling...")
    input()
    
    # Final status
    run_cmd("kubectl get hpa", "9️⃣ Final HPA Status")
    run_cmd("kubectl get pods", "Final Pod Count")
    run_cmd("kubectl describe hpa worker-hpa", "HPA Details")
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETADO")
    print("="*60)
    print("")
    print("¿Quieres limpiar los recursos? (y/n): ", end="")
    cleanup = input().strip().lower()
    
    if cleanup == 'y':
        print("\n🧹 Cleaning up...")
        run_cmd("kubectl delete -f .", "Removing all K8s resources")
        print("✅ Cleanup completado")
    else:
        print("\n📝 Para limpiar manualmente más tarde:")
        print("  kubectl delete -f k8s/")

if __name__ == "__main__":
    # Change to k8s directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()