#!/usr/bin/env python3
"""
🔥 STRESS TEST PARA WINDOWS - GENERAR CARGA REAL
Genera carga CPU sostenida para triggear auto-scaling
"""
import subprocess
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import requests

def send_heavy_task():
    """Send heavy task with large images"""
    payload = {
        "filters": ["resize", "blur", "sharpen", "edges"],
        "filter_params": {
            "resize": {"width": 4096, "height": 4096},  # Muy grande para más CPU
            "blur": {"radius": 10.0},
            "sharpen": {"factor": 3.0}
        },
        "count": 5  # Más imágenes por tarea
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/process-batch/distributed/",
            json=payload,
            timeout=5
        )
        if response.status_code == 200:
            task_id = response.json().get('task_id', 'unknown')[:8]
            print(f"✅ Heavy task sent: {task_id}")
            return True
        else:
            print(f"❌ HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def monitor_scaling():
    """Monitor HPA scaling in background"""
    for i in range(20):  # Monitor for 20 minutes
        try:
            result = subprocess.run(
                "kubectl get hpa --no-headers", 
                shell=True, 
                capture_output=True, 
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.stdout:
                parts = result.stdout.split()
                if len(parts) >= 6:
                    targets = parts[2]  # CPU/Memory targets
                    replicas = parts[5]  # Current replicas
                    print(f"📊 HPA: {targets} | Replicas: {replicas}")
            
            # Check worker count
            pods_result = subprocess.run(
                "kubectl get pods | findstr worker-deployment | find /c \"Running\"", 
                shell=True, 
                capture_output=True, 
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            worker_count = pods_result.stdout.strip() or "0"
            print(f"👥 Workers running: {worker_count}")
            
        except Exception as e:
            print(f"❌ Monitor error: {e}")
        
        time.sleep(60)  # Check every minute

def main():
    print("🔥 STRESS TEST PARA WINDOWS - GENERAR AUTO-SCALING")
    print("=" * 60)
    
    # Start monitoring in background
    monitor_thread = threading.Thread(target=monitor_scaling, daemon=True)
    monitor_thread.start()
    
    print("\n🚀 GENERANDO CARGA SOSTENIDA...")
    print("Objetivo: Superar 50% CPU para triggear auto-scaling")
    
    # Send continuous heavy load
    total_sent = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        for batch in range(10):  # 10 batches
            print(f"\n📦 Batch {batch + 1}/10:")
            
            # Send 20 heavy tasks per batch
            futures = [executor.submit(send_heavy_task) for _ in range(20)]
            success_count = sum(1 for f in futures if f.result())
            total_sent += success_count
            
            print(f"✅ Sent {success_count}/20 tasks (Total: {total_sent})")
            
            # Wait between batches
            if batch < 9:  # Don't wait after last batch
                print("⏳ Waiting 30 seconds before next batch...")
                time.sleep(30)
    
    print(f"\n🎯 TOTAL ENVIADO: {total_sent} tareas pesadas")
    
    # Monitor results for 5 minutes
    print("\n📊 MONITOREANDO AUTO-SCALING POR 5 MINUTOS...")
    for i in range(5):
        print(f"\nMinuto {i+1}/5:")
        subprocess.run("kubectl get hpa", shell=True)
        subprocess.run("kubectl get pods | findstr worker", shell=True)
        if i < 4:
            time.sleep(60)
    
    print("\n" + "=" * 60)
    print("✅ STRESS TEST COMPLETADO")
    print("📋 REVISA LOS RESULTADOS ARRIBA")
    print("💡 Si no escaló, los workers pueden estar procesando muy rápido")

if __name__ == "__main__":
    main()