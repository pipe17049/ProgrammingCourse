"""
⚠️ DEMOSTRACIÓN: Errores Comunes al Imprimir Objetos

Este archivo muestra qué pasa cuando intentas imprimir o usar incorrectamente:
- Threads
- Objetos async sin await
- Procesos
- Objetos de IPC

🎯 Propósito educativo: Entender la diferencia entre objetos y sus resultados
"""

import threading
import multiprocessing as mp
import asyncio
import time
from multiprocessing import Queue, Pipe, Array, Value, Manager

# ============================================================================
# 🧵 ¿QUÉ PASA AL IMPRIMIR UN THREAD?
# ============================================================================

def demo_thread_printing():
    """Demostrar qué se ve al imprimir un Thread"""
    print("🧵" + "="*60)
    print("🧵 ¿QUÉ PASA AL IMPRIMIR UN THREAD?")
    print("="*60)
    
    def worker_function():
        """Función que ejecuta el thread"""
        time.sleep(1)
        return "¡Trabajo completado!"
    
    # Crear thread
    thread = threading.Thread(target=worker_function)
    
    print("📊 ANTES de iniciar:")
    print(f"   🔍 Thread object: {thread}")
    print(f"   🔍 Tipo: {type(thread)}")
    print(f"   🔍 ¿Está vivo? {thread.is_alive()}")
    print(f"   🔍 Name: {thread.name}")
    
    # Iniciar thread
    thread.start()
    
    print("\n📊 DESPUÉS de iniciar:")
    print(f"   🔍 Thread object: {thread}")
    print(f"   🔍 ¿Está vivo? {thread.is_alive()}")
    
    # Esperar a que termine
    thread.join()
    
    print("\n📊 DESPUÉS de terminar:")
    print(f"   🔍 Thread object: {thread}")
    print(f"   🔍 ¿Está vivo? {thread.is_alive()}")
    
    print("\n💡 CONCLUSIÓN:")
    print("   ❌ El thread NO devuelve el resultado directamente")
    print("   ❌ Imprimir el thread muestra solo metadata")
    print("   ✅ Para obtener resultados, usa Queue o shared variables")

# ============================================================================
# ⚡ ¿QUÉ PASA CON ASYNC SIN AWAIT?
# ============================================================================

async def demo_async_without_await():
    """Demostrar qué pasa al no usar await"""
    print("\n⚡" + "="*60)
    print("⚡ ¿QUÉ PASA CON ASYNC SIN AWAIT?")
    print("="*60)
    
    async def async_function():
        """Función asíncrona que simula trabajo"""
        await asyncio.sleep(1)
        return "¡Resultado asíncrono!"
    
    print("📊 LLAMADA SIN AWAIT:")
    # ❌ Sin await - esto crea una corrutina, no ejecuta
    coroutine = async_function()
    print(f"   🔍 Sin await: {coroutine}")
    print(f"   🔍 Tipo: {type(coroutine)}")
    print("   ❌ ¡Es un objeto corrutina, no el resultado!")
    
    # Cerrar la corrutina no ejecutada (evita warnings)
    coroutine.close()
    
    print("\n📊 LLAMADA CON AWAIT:")
    # ✅ Con await - esto ejecuta y devuelve el resultado
    result = await async_function()
    print(f"   🔍 Con await: {result}")
    print(f"   🔍 Tipo: {type(result)}")
    print("   ✅ ¡Ahora sí es el resultado!")
    
    print("\n💡 CONCLUSIÓN:")
    print("   ❌ Sin await: obtienes objeto <coroutine>")
    print("   ✅ Con await: obtienes el resultado real")
    print("   ⚠️ Python te da warning si no usas await")

# ============================================================================
# 🔥 ¿QUÉ PASA AL IMPRIMIR UN PROCESO?
# ============================================================================

def demo_process_printing():
    """Demostrar qué se ve al imprimir un Process"""
    print("\n🔥" + "="*60)
    print("🔥 ¿QUÉ PASA AL IMPRIMIR UN PROCESO?")
    print("="*60)
    
    def worker_process():
        """Función que ejecuta el proceso"""
        time.sleep(1)
        print("   🔧 Proceso trabajando...")
    
    # Crear proceso
    process = mp.Process(target=worker_process)
    
    print("📊 ANTES de iniciar:")
    print(f"   🔍 Process object: {process}")
    print(f"   🔍 Tipo: {type(process)}")
    print(f"   🔍 PID: {process.pid}")
    print(f"   🔍 ¿Está vivo? {process.is_alive()}")
    
    # Iniciar proceso
    process.start()
    
    print("\n📊 DESPUÉS de iniciar:")
    print(f"   🔍 Process object: {process}")
    print(f"   🔍 PID: {process.pid}")
    print(f"   🔍 ¿Está vivo? {process.is_alive()}")
    
    # Esperar a que termine
    process.join()
    
    print("\n📊 DESPUÉS de terminar:")
    print(f"   🔍 Process object: {process}")
    print(f"   🔍 ¿Está vivo? {process.is_alive()}")
    print(f"   🔍 Exit code: {process.exitcode}")
    
    print("\n💡 CONCLUSIÓN:")
    print("   ❌ El proceso NO devuelve resultado directamente")
    print("   ❌ Imprimir muestra solo metadata del proceso")
    print("   ✅ Para resultados, usa Queue, Pipe, o Shared Memory")

# ============================================================================
# 🔄 ¿QUÉ PASA AL IMPRIMIR OBJETOS IPC?
# ============================================================================

def demo_ipc_objects():
    """Demostrar qué se ve al imprimir objetos IPC"""
    print("\n🔄" + "="*60)
    print("🔄 ¿QUÉ PASA AL IMPRIMIR OBJETOS IPC?")
    print("="*60)
    
    # Queue
    queue = Queue()
    print("📊 QUEUE:")
    print(f"   🔍 Queue object: {queue}")
    print(f"   🔍 Tipo: {type(queue)}")
    print("   💡 Es el objeto queue, no su contenido")
    
    # Pipe
    parent_conn, child_conn = Pipe()
    print("\n📊 PIPE:")
    print(f"   🔍 Parent connection: {parent_conn}")
    print(f"   🔍 Child connection: {child_conn}")
    print(f"   🔍 Tipo: {type(parent_conn)}")
    print("   💡 Son objetos de conexión, no datos")
    
    # Shared Memory
    shared_array = Array('i', [1, 2, 3, 4])
    shared_value = Value('i', 42)
    print("\n📊 SHARED MEMORY:")
    print(f"   🔍 Shared Array object: {shared_array}")
    print(f"   🔍 Shared Value object: {shared_value}")
    print(f"   🔍 Array content: {list(shared_array[:])}")  # ✅ Contenido real
    print(f"   🔍 Value content: {shared_value.value}")    # ✅ Valor real
    
    # Manager
    manager = Manager()
    shared_list = manager.list([1, 2, 3])
    print("\n📊 MANAGER:")
    print(f"   🔍 Manager object: {manager}")
    print(f"   🔍 Shared List object: {shared_list}")
    print(f"   🔍 List content: {list(shared_list)}")      # ✅ Contenido real
    
    print("\n💡 CONCLUSIÓN:")
    print("   ❌ Los objetos IPC son 'wrappers', no datos")
    print("   ✅ Para ver datos: usa .value, [:], list(), etc.")
    print("   🎯 Cada tipo IPC tiene su forma de acceder a datos")
    
    # Limpiar
    parent_conn.close()
    child_conn.close()
    manager.shutdown()

# ============================================================================
# 🚫 ERRORES COMUNES Y SOLUCIONES
# ============================================================================

def demo_common_mistakes():
    """Demostrar errores típicos y cómo solucionarlos"""
    print("\n🚫" + "="*60)
    print("🚫 ERRORES COMUNES Y SOLUCIONES")
    print("="*60)
    
    print("❌ ERROR 1: Esperar que thread devuelva valor")
    print("   BAD:  result = threading.Thread(target=func)")
    print("   GOOD: Usar Queue o shared variable")
    
    print("\n❌ ERROR 2: Olvidar await en async")
    print("   BAD:  result = async_function()")
    print("   GOOD: result = await async_function()")
    
    print("\n❌ ERROR 3: Imprimir objeto en lugar de contenido")
    print("   BAD:  print(shared_array)      # <object at 0x...>")
    print("   GOOD: print(shared_array[:])   # [1, 2, 3, 4]")
    
    print("\n❌ ERROR 4: Esperar que Process devuelva valor")
    print("   BAD:  result = multiprocessing.Process(target=func)")
    print("   GOOD: Usar Queue, Pipe, o Shared Memory")
    
    print("\n❌ ERROR 5: No cerrar conexiones IPC")
    print("   BAD:  No llamar .close() en pipes/connections")
    print("   GOOD: Siempre cerrar conexiones cuando termines")
    
    print("\n✅ REGLA GENERAL:")
    print("   🎯 Objects != Results")
    print("   🎯 Threads/Processes son 'workers', no resultados")
    print("   🎯 Async necesita await para ejecutar")
    print("   🎯 IPC objects necesitan métodos para acceder datos")

# ============================================================================
# 🎪 DEMOSTRACIÓN INTERACTIVA
# ============================================================================

def interactive_demo():
    """Demostración que el usuario puede seguir paso a paso"""
    print("\n🎪" + "="*60)
    print("🎪 DEMOSTRACIÓN INTERACTIVA")
    print("="*60)
    
    print("👀 Observa estos objetos y sus tipos:")
    print("-"*40)
    
    # Threading
    thread = threading.Thread(target=lambda: time.sleep(0.1))
    print(f"Thread object: {thread}")
    
    # Multiprocessing
    process = mp.Process(target=lambda: None)
    print(f"Process object: {process}")
    
    # Queue
    queue = Queue()
    print(f"Queue object: {queue}")
    
    # Shared Memory
    shared_val = Value('i', 42)
    print(f"Shared Value object: {shared_val}")
    print(f"Shared Value CONTENT: {shared_val.value}")
    
    print("\n🎯 ¿VES LA DIFERENCIA?")
    print("   📦 Objects = Contenedores/Herramientas")
    print("   📊 Content = Datos reales")
    print("   🔑 La clave es saber CÓMO acceder al contenido")

def main():
    """Ejecutar todas las demostraciones"""
    print("⚠️" + "="*70)
    print("⚠️ ERRORES COMUNES: Threads, Async, Procesos e IPC")
    print("="*70)
    
    # Threads
    demo_thread_printing()
    
    # Procesos  
    demo_process_printing()
    
    # Objetos IPC
    demo_ipc_objects()
    
    # Errores comunes
    demo_common_mistakes()
    
    # Demo interactiva
    interactive_demo()
    
    print("\n🎓" + "="*60)
    print("🎓 RESUMEN")
    print("="*60)
    print("💡 LECCIÓN PRINCIPAL:")
    print("   🎯 Objects ≠ Results")
    print("   🎯 Threads/Processes son workers, no resultados")
    print("   🎯 IPC objects son containers, no datos")
    print("   🎯 Async sin await = coroutine object, no resultado")
    print("\n✅ AHORA SABES qué esperar al imprimir estos objetos!")

if __name__ == "__main__":
    # Ejecutar demostraciones síncronas
    main()
    
    # Ejecutar demostración async
    print("\n⚡ EJECUTANDO DEMOSTRACIÓN ASYNC...")
    asyncio.run(demo_async_without_await()) 