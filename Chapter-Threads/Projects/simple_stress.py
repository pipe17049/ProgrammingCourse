#!/usr/bin/env python3
"""
Stress simple - Envía tareas secuencialmente para llenar la cola gradualmente
"""
import requests
import time
import json


def send_task(task_num):
    """Enviar una tarea pesada"""
    payload = {
        "images": ["static/images/Clocktower_Panorama_20080622_20mb.jpg"],
        "filters": ["sharpen", "edges", "blur"]  # 3 filtros pesados
    }
    
    try:
        print(f"📤 Enviando tarea {task_num}...", end=" ")
        response = requests.post(
            "http://localhost:8000/api/process-batch/distributed/",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('task_id', 'unknown')
            processing_time = data.get('processing_time', 0)
            print(f"✅ {task_id[:8]} ({processing_time:.1f}s)")
            return True
        else:
            print(f"❌ Error {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ {str(e)}")
        return False


def gradual_stress(count=5):
    """Enviar tareas gradualmente"""
    print(f"🎯 OBJETIVO: Enviar {count} tareas pesadas secuencialmente")
    print(f"💡 Para que se acumulen en la cola y cambien las recomendaciones")
    print("=" * 60)
    
    for i in range(1, count + 1):
        success = send_task(i)
        if success:
            time.sleep(0.5)  # Pausa corta entre tareas
        else:
            time.sleep(2)   # Pausa más larga si hay error
    
    print(f"\n🎯 {count} tareas enviadas!")
    print("\n📊 VERIFICAR MÉTRICAS AHORA:")
    print("   python simple_monitoring/cli.py metrics")


if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    gradual_stress(count)