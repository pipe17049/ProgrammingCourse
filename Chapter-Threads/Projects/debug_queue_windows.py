#!/usr/bin/env python3
"""
DEBUG SCRIPT para Windows - Verificar conexión Redis y cola
"""
import redis
import time
import json

def debug_redis_queue():
    """Debug completo de Redis y cola en Windows"""
    
    print("🔍 DEBUGGING REDIS QUEUE EN WINDOWS")
    print("=" * 50)
    
    # 1. Test básico de conexión
    print("\n1️⃣ TESTING CONEXIÓN REDIS...")
    try:
        # Timeouts más largos para Windows
        r = redis.Redis(
            host='localhost', 
            port=6379, 
            decode_responses=True,
            socket_connect_timeout=10,  # 10s timeout
            socket_timeout=10
        )
        
        # Test ping
        ping_result = r.ping()
        print(f"✅ Ping Redis: {ping_result}")
        
        # Info básica
        info = r.info()
        print(f"✅ Redis version: {info.get('redis_version', 'unknown')}")
        print(f"✅ Connected clients: {info.get('connected_clients', 'unknown')}")
        
    except Exception as e:
        print(f"❌ Error conectando Redis: {e}")
        print("💡 Verifica: docker-compose up -d")
        return
    
    # 2. Test de todas las colas/keys
    print("\n2️⃣ EXPLORANDO TODAS LAS KEYS...")
    try:
        all_keys = r.keys('*')
        print(f"🔑 Total keys en Redis: {len(all_keys)}")
        
        # Mostrar keys relevantes
        queue_keys = [k for k in all_keys if 'queue' in k.lower()]
        task_keys = [k for k in all_keys if 'task' in k.lower()]
        worker_keys = [k for k in all_keys if 'worker' in k.lower()]
        
        print(f"📋 Queue keys: {queue_keys}")
        print(f"📝 Task keys: {len(task_keys)} total")
        print(f"👥 Worker keys: {worker_keys}")
        
    except Exception as e:
        print(f"❌ Error explorando keys: {e}")
    
    # 3. Test específico de la cola principal
    print("\n3️⃣ TESTING COLA PRINCIPAL...")
    try:
        queue_name = 'image_tasks'  # Nombre correcto de la cola
        queue_length = r.llen(queue_name)
        print(f"📊 Cola '{queue_name}' length: {queue_length}")
        
        if queue_length > 0:
            print("✅ HAY TAREAS EN LA COLA!")
            # Mostrar primeras tareas (sin sacarlas)
            first_tasks = r.lrange(queue_name, 0, 2)
            print(f"🎯 Primeras tareas: {first_tasks}")
        else:
            print("⚠️ COLA VACÍA")
            
    except Exception as e:
        print(f"❌ Error consultando cola: {e}")
    
    # 4. Test de tareas en processing
    print("\n4️⃣ TESTING TAREAS EN PROCESSING...")
    try:
        task_keys = r.keys('task:*')
        processing_count = 0
        
        for task_key in task_keys:
            try:
                status = r.hget(task_key, 'status')
                if status == 'processing':
                    processing_count += 1
                    print(f"⚡ Task {task_key}: {status}")
            except:
                continue
                
        print(f"📊 Total tareas processing: {processing_count}")
        
    except Exception as e:
        print(f"❌ Error consultando tasks: {e}")
    
    # 5. Test del método actual de metrics
    print("\n5️⃣ TESTING MÉTODO ACTUAL DE METRICS...")
    try:
        from simple_monitoring.metrics_collector import SimpleMetricsCollector
        collector = SimpleMetricsCollector()
        metrics = collector.collect_metrics()
        
        print(f"📊 Queue Length (método actual): {metrics.get('queue_length', 'ERROR')}")
        print(f"⚡ Busy Workers: {metrics.get('busy_workers', 'ERROR')}")
        print(f"📈 Utilization: {metrics.get('worker_utilization', 'ERROR')}")
        
    except Exception as e:
        print(f"❌ Error con metrics collector: {e}")
        
    print("\n" + "=" * 50)
    print("✅ DEBUG COMPLETO - Revisa resultados arriba")

if __name__ == "__main__":
    debug_redis_queue()