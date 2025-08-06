#!/usr/bin/env python3
"""
🖼️ STRESS TEST CON PROCESAMIENTO REAL DE IMÁGENES
Genera carga CPU real procesando imágenes en los workers
"""
import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import json

def generate_heavy_image_task():
    """Genera una tarea de procesamiento pesado"""
    payload = {
        "filters": ["resize", "blur", "sharpen", "edges"],
        "filter_params": {
            "resize": {"width": 2048, "height": 2048},  # Imagen grande
            "blur": {"radius": 5.0},
            "sharpen": {"factor": 2.0}
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/process-batch/distributed/",
            json=payload,
            timeout=10
        )
        if response.status_code == 200:
            print(f"✅ Task queued: {response.json().get('task_id', 'unknown')[:8]}")
            return True
        else:
            print(f"❌ HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ API no accesible")
        return False
    except requests.exceptions.Timeout:
        print("❌ API timeout")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def stress_test_real():
    """Ejecuta stress test con procesamiento real"""
    print("🖼️ INICIANDO STRESS TEST CON PROCESAMIENTO REAL")
    print("=" * 60)
    
    # Generar 20 tareas pesadas en paralelo
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i in range(20):
            future = executor.submit(generate_heavy_image_task)
            futures.append(future)
            time.sleep(0.5)  # Una tarea cada 0.5 segundos
        
        # Esperar resultados
        success_count = sum(1 for future in futures if future.result())
        print(f"\n📊 RESUMEN: {success_count}/20 tareas enviadas")

if __name__ == "__main__":
    stress_test_real()
