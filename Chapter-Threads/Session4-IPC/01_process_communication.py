"""
🔄 SESIÓN 2.3: Comunicación entre Procesos - Shared Memory y IPC

Este módulo demuestra diferentes formas de comunicación entre procesos
en multiprocessing: Queues, Pipes, Shared Memory, y Locks.

🎯 Objetivos:
- Entender Inter-Process Communication (IPC)
- Usar Queue para comunicación segura
- Implementar Shared Memory para eficiencia
- Coordinar procesos con Locks y Events
"""

import time
import multiprocessing as mp
from multiprocessing import Queue, Pipe, Array, Value, Lock, Event
import os
from typing import List

# ============================================================================
# 🔄 MÉTODO 1: Queue - Comunicación Segura entre Procesos
# ============================================================================

def producer_worker(queue: Queue, worker_id: int, items: int):
    """Proceso productor que envía datos a la queue"""
    process_name = mp.current_process().name
    print(f"📤 Producer {worker_id} ({process_name}): Iniciando producción de {items} items")
    
    for i in range(items):
        # Simular trabajo de producción
        time.sleep(0.1)
        
        item = {
            'id': i,
            'producer': worker_id,
            'data': f"Item-{worker_id}-{i}",
            'timestamp': time.time()
        }
        
        queue.put(item)
        print(f"📤 Producer {worker_id}: Enviado {item['data']}")
    
    # Señal de fin
    queue.put(None)
    print(f"✅ Producer {worker_id}: Completado")

def consumer_worker(queue: Queue, worker_id: int):
    """Proceso consumidor que recibe datos de la queue"""
    process_name = mp.current_process().name
    print(f"📥 Consumer {worker_id} ({process_name}): Iniciando consumo")
    
    items_consumed = 0
    
    while True:
        try:
            # Obtener item de la queue (blocking)
            item = queue.get(timeout=2)
            
            if item is None:
                print(f"📥 Consumer {worker_id}: Recibida señal de fin")
                break
            
            # Procesar item
            print(f"📥 Consumer {worker_id}: Procesando {item['data']}")
            time.sleep(0.05)  # Simular procesamiento
            items_consumed += 1
            
            # Marcar como completado
            queue.task_done()
            
        except:
            print(f"📥 Consumer {worker_id}: Timeout - no hay más items")
            break
    
    print(f"✅ Consumer {worker_id}: Procesados {items_consumed} items")
    return items_consumed

def demonstrate_queue_communication():
    """🔄 DEMOSTRACIÓN: Comunicación con Queue"""
    print("\n" + "🔄" + "="*60)
    print("🔄 COMUNICACIÓN CON QUEUE - Producer/Consumer")
    print("="*60)
    
    # Crear queue compartida
    queue = Queue(maxsize=10)  # Buffer limitado
    
    print(f"📋 Queue creada con buffer máximo de 10 items")
    
    # Configuración
    num_producers = 2
    num_consumers = 3
    items_per_producer = 5
    
    processes = []
    start_time = time.time()
    
    # Crear procesos productores
    for i in range(num_producers):
        process = mp.Process(
            target=producer_worker,
            args=(queue, i+1, items_per_producer)
        )
        processes.append(process)
        process.start()
    
    # Crear procesos consumidores
    for i in range(num_consumers):
        process = mp.Process(
            target=consumer_worker,
            args=(queue, i+1)
        )
        processes.append(process)
        process.start()
    
    # Esperar que terminen
    for process in processes:
        process.join()
    
    total_time = time.time() - start_time
    print(f"\n⏱️ Comunicación completada en {total_time:.2f} segundos")
    print(f"📊 Procesos utilizados: {len(processes)}")

# ============================================================================
# 🔄 MÉTODO 2: Pipe - Comunicación Bidireccional
# ============================================================================

def pipe_sender(conn, worker_id: int, messages: int):
    """Proceso que envía mensajes por pipe"""
    process_name = mp.current_process().name
    print(f"📞 Sender {worker_id} ({process_name}): Iniciando envío")
    
    for i in range(messages):
        message = {
            'id': i,
            'sender': worker_id,
            'content': f"Mensaje-{worker_id}-{i}",
            'timestamp': time.time()
        }
        
        conn.send(message)
        print(f"📞 Sender {worker_id}: Enviado {message['content']}")
        time.sleep(0.2)
    
    # Enviar señal de fin
    conn.send("FIN")
    conn.close()
    print(f"✅ Sender {worker_id}: Completado")

def pipe_receiver(conn, worker_id: int):
    """Proceso que recibe mensajes por pipe"""
    process_name = mp.current_process().name
    print(f"📞 Receiver {worker_id} ({process_name}): Esperando mensajes")
    
    messages_received = 0
    
    while True:
        try:
            message = conn.recv()
            
            if message == "FIN":
                print(f"📞 Receiver {worker_id}: Recibida señal de fin")
                break
            
            print(f"📞 Receiver {worker_id}: Recibido {message['content']}")
            messages_received += 1
            
        except EOFError:
            print(f"📞 Receiver {worker_id}: Conexión cerrada")
            break
    
    conn.close()
    print(f"✅ Receiver {worker_id}: Recibidos {messages_received} mensajes")

def demonstrate_pipe_communication():
    """🔄 DEMOSTRACIÓN: Comunicación con Pipe"""
    print("\n" + "🔄" + "="*60)
    print("🔄 COMUNICACIÓN CON PIPE - Bidireccional")
    print("="*60)
    
    # Crear pipe bidireccional
    parent_conn, child_conn = Pipe()
    
    print(f"📞 Pipe creado para comunicación bidireccional")
    
    start_time = time.time()
    
    # Crear procesos
    sender_process = mp.Process(
        target=pipe_sender,
        args=(child_conn, 1, 3)
    )
    
    receiver_process = mp.Process(
        target=pipe_receiver,
        args=(parent_conn, 1)
    )
    
    # Iniciar procesos
    sender_process.start()
    receiver_process.start()
    
    # Esperar que terminen
    sender_process.join()
    receiver_process.join()
    
    total_time = time.time() - start_time
    print(f"\n⏱️ Comunicación por pipe completada en {total_time:.2f} segundos")

# ============================================================================
# 🔄 MÉTODO 3: Shared Memory - Memoria Compartida
# ============================================================================

def shared_memory_worker(shared_array, shared_value, lock: Lock, worker_id: int):
    """Proceso que modifica memoria compartida"""
    process_name = mp.current_process().name
    print(f"🧠 Worker {worker_id} ({process_name}): Accediendo a memoria compartida")
    
    for i in range(5):
        # 🔒 Usar lock para acceso seguro a memoria compartida
        with lock:
            # Leer valores actuales
            current_value = shared_value.value
            current_array = list(shared_array[:])
            
            print(f"🧠 Worker {worker_id}: Valor actual: {current_value}, Array: {current_array}")
            
            # Modificar memoria compartida
            shared_value.value += worker_id * 10
            shared_array[worker_id-1] = shared_value.value
            
            print(f"🧠 Worker {worker_id}: Nuevo valor: {shared_value.value}")
            
        # Simular trabajo
        time.sleep(0.1)
    
    print(f"✅ Worker {worker_id}: Completado")

def demonstrate_shared_memory():
    """🔄 DEMOSTRACIÓN: Memoria Compartida"""
    print("\n" + "🔄" + "="*60)
    print("🔄 MEMORIA COMPARTIDA - Shared Array y Value")
    print("="*60)
    
    # Crear memoria compartida
    shared_array = Array('i', [0, 0, 0, 0])  # Array de enteros
    shared_value = Value('i', 100)            # Valor entero
    lock = Lock()                             # Lock para sincronización
    
    print(f"🧠 Memoria compartida creada:")
    print(f"   - Array inicial: {list(shared_array[:])}")
    print(f"   - Valor inicial: {shared_value.value}")
    
    start_time = time.time()
    
    # Crear procesos que modifican memoria compartida
    processes = []
    for i in range(3):
        process = mp.Process(
            target=shared_memory_worker,
            args=(shared_array, shared_value, lock, i+1)
        )
        processes.append(process)
        process.start()
    
    # Esperar que terminen
    for process in processes:
        process.join()
    
    total_time = time.time() - start_time
    
    # Mostrar resultado final
    print(f"\n📊 RESULTADO FINAL:")
    print(f"   - Array final: {list(shared_array[:])}")
    print(f"   - Valor final: {shared_value.value}")
    print(f"   ⏱️ Tiempo: {total_time:.2f} segundos")

# ============================================================================
# 🔄 MÉTODO 4: Event - Coordinación entre Procesos
# ============================================================================

def waiter_process(event: Event, worker_id: int):
    """Proceso que espera una señal"""
    process_name = mp.current_process().name
    print(f"⏳ Waiter {worker_id} ({process_name}): Esperando señal...")
    
    # Esperar hasta que el event se active
    event.wait()
    
    print(f"🎉 Waiter {worker_id}: ¡Señal recibida! Continuando trabajo...")
    
    # Simular trabajo después de la señal
    for i in range(3):
        print(f"🔄 Waiter {worker_id}: Trabajando... {i+1}/3")
        time.sleep(0.3)
    
    print(f"✅ Waiter {worker_id}: Trabajo completado")

def signaler_process(event: Event, delay: float):
    """Proceso que envía la señal después de un delay"""
    process_name = mp.current_process().name
    print(f"📡 Signaler ({process_name}): Esperando {delay} segundos antes de enviar señal...")
    
    time.sleep(delay)
    
    print(f"📡 Signaler: ¡Enviando señal a todos los waiters!")
    event.set()  # Activar el event
    
    print(f"✅ Signaler: Señal enviada")

def demonstrate_event_coordination():
    """🔄 DEMOSTRACIÓN: Coordinación con Event"""
    print("\n" + "🔄" + "="*60)
    print("🔄 COORDINACIÓN CON EVENT - Sincronización")
    print("="*60)
    
    # Crear event compartido
    event = Event()
    
    print(f"📡 Event creado para coordinación")
    
    start_time = time.time()
    
    # Crear procesos waiter
    waiter_processes = []
    for i in range(3):
        process = mp.Process(
            target=waiter_process,
            args=(event, i+1)
        )
        waiter_processes.append(process)
        process.start()
    
    # Crear proceso signaler
    signaler = mp.Process(
        target=signaler_process,
        args=(event, 2.0)  # Esperar 2 segundos
    )
    signaler.start()
    
    # Esperar que terminen todos
    signaler.join()
    for process in waiter_processes:
        process.join()
    
    total_time = time.time() - start_time
    print(f"\n⏱️ Coordinación completada en {total_time:.2f} segundos")

# ============================================================================
# 🎓 COMPARACIÓN DE MÉTODOS DE COMUNICACIÓN
# ============================================================================

def compare_communication_methods():
    """🎓 Comparar diferentes métodos de comunicación"""
    print("\n" + "🎓" + "="*60)
    print("🎓 COMPARACIÓN DE MÉTODOS DE COMUNICACIÓN")
    print("="*60)
    
    methods = {
        "Queue": {
            "pros": ["Thread-safe", "FIFO", "Blocking operations", "Size limit"],
            "cons": ["Serialization overhead", "Memory usage"],
            "uso": "Producer-Consumer patterns"
        },
        "Pipe": {
            "pros": ["Bidirectional", "Fast", "Direct connection"],
            "cons": ["Only 2 processes", "No built-in synchronization"],
            "uso": "Communication between 2 processes"
        },
        "Shared Memory": {
            "pros": ["Very fast", "No serialization", "Direct access"],
            "cons": ["Need manual synchronization", "Complex"],
            "uso": "High-performance data sharing"
        },
        "Event": {
            "pros": ["Simple coordination", "Multiple waiters"],
            "cons": ["Only boolean state", "No data transfer"],
            "uso": "Process synchronization"
        }
    }
    
    for method, details in methods.items():
        print(f"\n🔧 {method}:")
        print(f"   ✅ Pros: {', '.join(details['pros'])}")
        print(f"   ⚠️ Cons: {', '.join(details['cons'])}")
        print(f"   🎯 Uso: {details['uso']}")
    
    print(f"\n💡 RECOMENDACIONES:")
    print(f"🔄 Para la mayoría de casos: Queue")
    print(f"🚀 Para alta performance: Shared Memory + Lock")
    print(f"📞 Para comunicación simple: Pipe")
    print(f"⏳ Para coordinación: Event")

# ============================================================================
# 🧪 DEMOSTRACIÓN PRINCIPAL
# ============================================================================

def demonstrate_all_communication():
    """Ejecutar todas las demostraciones de comunicación"""
    print("🔄 DEMOSTRACIÓN: Comunicación entre Procesos")
    print("🎯 Objetivo: Entender IPC (Inter-Process Communication)")
    
    print(f"\n💻 INFORMACIÓN:")
    print(f"🔢 CPU cores: {mp.cpu_count()}")
    print(f"🐍 Proceso principal: {os.getpid()}")
    
    # Demo 1: Queue
    demonstrate_queue_communication()
    
    # Demo 2: Pipe
    demonstrate_pipe_communication()
    
    # Demo 3: Shared Memory
    demonstrate_shared_memory()
    
    # Demo 4: Event
    demonstrate_event_coordination()
    
    # Comparación
    compare_communication_methods()

if __name__ == "__main__":
    print("🔄 DEMOSTRACIÓN: Comunicación entre Procesos")
    print("🎯 IMPORTANTE: Diferentes formas de IPC")
    
    print("\n🎯 ¿Qué quieres ver?")
    print("1. Todas las demostraciones")
    print("2. Solo Queue (Producer-Consumer)")
    print("3. Solo Shared Memory")
    print("4. Solo comparación de métodos")
    choice = input("👉 Opción (1-4): ").strip()
    
    if choice == "1":
        # Todas las demos
        demonstrate_all_communication()
        
    elif choice == "2":
        # Solo Queue
        demonstrate_queue_communication()
        
    elif choice == "3":
        # Solo Shared Memory
        demonstrate_shared_memory()
        
    else:
        # Solo comparación
        compare_communication_methods()
    
    print("\n✅ ¡COMUNICACIÓN ENTRE PROCESOS COMPLETADA!")
    print("🎓 Has aprendido: Queue → Pipe → Shared Memory → Event")
    print("🚀 Próximo paso: 04_comparison_guide.py")
    print("🚀 Guía completa: Threading vs Multiprocessing vs Async") 