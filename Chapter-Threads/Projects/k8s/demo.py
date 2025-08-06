#!/usr/bin/env python3
"""
KUBERNETES AUTO-SCALING DEMO
Cross-platform demo script for the Kubernetes class
"""

import subprocess
import time
import sys
import os

def run_cmd(cmd, description="", show_header=True):
    """Run command and show output"""
    if description and show_header:
        print(f"\n> {description}")
        print("=" * 50)
    
    print(f"$ {cmd}")
    try:
        # Use utf-8 encoding to avoid Windows cp1252 issues
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='ignore'  # Ignore problematic characters
        )
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
    print(f"\nWaiting for pods with label {label} to be ready...")
    cmd = f"kubectl wait --for=condition=ready pod -l {label} --timeout={timeout}s"
    return run_cmd(cmd)

def main():
    print("KUBERNETES AUTO-SCALING DEMO")
    print("================================")
    print("Este demo funciona en Windows, Linux y Mac")
    print("")
    
    # Check if kubectl is available
    if not run_cmd("kubectl version --client", "Checking kubectl"):
        print("ERROR: kubectl no está instalado o no está en PATH")
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
    
    # Check Docker images - look for optimized versions
    print("\nVerificando imágenes Docker optimizadas...")
    # Cross-platform: use docker images with filter instead of grep
    result = subprocess.run("docker images projects*", shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    
    # Check for final API image
    if "projects-api-final" not in result.stdout:
        print("WARNING: No se encontró projects-api-final:latest")
        print("SOLUTION: Necesitas ejecutar: python build.py")
    
    # Check for final worker image  
    if "projects-worker-final" not in result.stdout:
        print("WARNING: No se encontró projects-worker-final:latest")
        print("SOLUTION: Necesitas ejecutar: python build.py")
    
    print("\n" + "="*60)
    print("INICIANDO DEMO - AUTO-SCALING EN KUBERNETES")
    print("="*60)
    print("NOTA: Usamos imágenes FINALES del proyecto:")
    print("   - API: projects-api-final:latest (Django + Debian + OpenCV)")
    print("   - Worker: projects-worker-final:latest (Python + Debian + OpenCV)")
    print("   - Objetivo: Ver AUTO-SCALING funcionando")
    print("="*60)
    
    # Deploy Redis
    run_cmd("kubectl apply -f redis-deployment.yaml", "1️⃣ Deploying Redis")
    
    # Deploy API  
    run_cmd("kubectl apply -f api-deployment.yaml", "2️⃣ Deploying API")
    
    # Deploy Workers + HPA
    run_cmd("kubectl apply -f worker-deployment.yaml", "3️⃣ Deploying Workers + HPA")
    
    # Install metrics server automatically
    print("\n🔧 Installing metrics server...")
    run_cmd("kubectl apply -f metrics-server.yaml", "Installing metrics server (local file)")
    
    # Wait for pods
    print("\n4️⃣ Waiting for all pods to be ready...")
    wait_for_pods("app=redis")
    wait_for_pods("app=image-api") 
    wait_for_pods("app=image-worker")
    
    # Show current status
    run_cmd("kubectl get pods", "5️⃣ Current Pod Status")
    run_cmd("kubectl get hpa", "HPA Status")
    
    # Give metrics server time to collect data
    print("\n⏳ Waiting for metrics server to collect data...")
    print("Esperando hasta que HPA tenga métricas reales (no <unknown>)...")
    
    # Wait until HPA shows real metrics (not <unknown>)
    for attempt in range(30):  # Max 5 minutes
        result = subprocess.run(
            "kubectl get hpa --no-headers", 
            shell=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.stdout and "<unknown>" not in result.stdout:
            print(f"✅ Métricas disponibles después de {attempt*10} segundos")
            break
        
        print(f"⏱️ Intento {attempt+1}/30: Esperando métricas... (aún <unknown>)")
        time.sleep(10)
    else:
        print("⚠️ Timeout esperando métricas, continuando de todos modos...")
    
    # Show current metrics
    run_cmd("kubectl get hpa", "📊 Métricas actuales antes del stress test")
    
    # Purge Redis queue before starting stress test
    print("\n🧹 Purging Redis queue to ensure clean state...")
    try:
        purge_result = subprocess.run(
            "kubectl exec deployment/redis-deployment -- redis-cli FLUSHALL",
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        if purge_result.returncode == 0:
            print("✅ Redis queue purged successfully")
        else:
            print("⚠️ Redis purge warning:", purge_result.stderr.strip())
    except Exception as e:
        print(f"⚠️ Could not purge Redis: {e}")
    
    # Wait for workers to re-register after purge
    print("⏳ Waiting for workers to re-register after purge...")
    for attempt in range(12):  # Max 2 minutes
        try:
            workers_check = subprocess.run(
                "kubectl exec deployment/redis-deployment -- redis-cli HLEN workers",
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            worker_count = int(workers_check.stdout.strip() or 0)
            if worker_count > 0:
                print(f"✅ {worker_count} workers re-registered after purge")
                break
            print(f"⏱️ Attempt {attempt+1}/12: {worker_count} workers registered...")
            time.sleep(10)
        except:
            time.sleep(10)
    else:
        print("⚠️ No workers registered after purge, continuing anyway...")
    
    print("\n" + "="*60)
    print("🔥 STRESS TEST PHASE")
    print("="*60)
    
    # Setup port forwarding
    print("\n6️⃣ Setting up port forwarding...")
    print("Iniciando port-forward en background...")
    
    # Start port forwarding in background
    try:
        port_forward_process = subprocess.Popen(
            ["kubectl", "port-forward", "service/api-service", "8000:8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(3)
        print("✅ Port-forward iniciado")
    except Exception as e:
        print(f"⚠️ Port-forward error: {e}")
    
    print("\n7️⃣ Generando carga CPU real con procesamiento de imágenes...")
    time.sleep(5)  # Wait for API to be ready
    
    # Generate heavy load using real image processing
    print("🖼️ Enviando 10 tareas pesadas de procesamiento...")
    import requests
    from concurrent.futures import ThreadPoolExecutor
    
    def send_heavy_task():
        """Send heavy image processing task"""
        payload = {
            "filters": ["resize", "blur", "sharpen", "edges"],
            "filter_params": {
                "resize": {"width": 2048, "height": 2048},
                "blur": {"radius": 5.0},
                "sharpen": {"factor": 2.0}
            },
            "count": 2
        }
        try:
            response = requests.post(
                "http://localhost:8000/api/process-batch/distributed/",
                json=payload,
                timeout=10
            )
            if response.status_code == 200:
                task_id = response.json().get('task_id', 'unknown')[:8]
                print(f"✅ Heavy task queued: {task_id}")
                return True
            else:
                print(f"❌ HTTP {response.status_code}: {response.text[:100]}")
                return False
        except Exception as e:
            print(f"❌ Task error: {e}")
            return False
    
    # Send multiple heavy tasks to trigger scaling
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(send_heavy_task) for _ in range(10)]
        success_count = sum(1 for f in futures if f.result())
        print(f"📊 {success_count}/10 tareas pesadas enviadas")
    
    print("\n8️⃣ Verificando auto-scaling...")
    for i in range(5):
        print(f"⏱️ Check {i+1}/5:")
        run_cmd("kubectl get hpa", f"Check {i+1}/5 - Auto-scaling status")
        pods_count = subprocess.run("kubectl get pods -l app=image-worker --no-headers | wc -l", shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        print(f"  Pods workers: {pods_count.stdout.strip()}")
        time.sleep(10)
    
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