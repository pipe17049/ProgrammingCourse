
from flask import Flask, jsonify, request
from datetime import datetime
import uuid
import websockets
import asyncio
import json
import threading

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración WebSocket
WEBSOCKET_URL = "ws://localhost:8765"

def send_websocket_message(message_data):
    """
    Envía un mensaje al servidor WebSocket de forma asíncrona
    Utiliza threading para no bloquear la aplicación Flask
    """
    def _send_message():
        try:
            # Ejecutar el envío de mensaje WebSocket
            asyncio.run(_async_send_message(message_data))
        except Exception as e:
            print(f"❌ Error enviando mensaje WebSocket: {e}")
    
    # Ejecutar en un hilo separado para no bloquear Flask
    thread = threading.Thread(target=_send_message)
    thread.daemon = True
    thread.start()

async def _async_send_message(message_data):
    """Función asíncrona para enviar mensaje WebSocket"""
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            await websocket.send(json.dumps(message_data))
    except Exception as e:
        print(f"❌ Error conectando con WebSocket server: {e}")
        print("💡 Asegúrate de que el servidor WebSocket esté ejecutándose en ws://localhost:8765")

# Base de datos simulada en memoria para el ejemplo
# En producción usarías una base de datos real
tasks = [
    {
        'id': '1',
        'title': 'Aprender Flask',
        'description': 'Completar el tutorial de Flask API',
        'completed': False,
        'created_at': '2024-01-15T10:00:00Z'
    },
    {
        'id': '2', 
        'title': 'Crear API REST',
        'description': 'Implementar endpoints CRUD completos',
        'completed': True,
        'created_at': '2024-01-15T11:00:00Z'
    }
]

# Ruta principal - Información de la API
@app.route('/')
def index():
    """
    Endpoint principal que muestra información sobre la API
    """
    return jsonify({
        'message': 'Bienvenido a la API de Tareas con Flask',
        'version': '1.0.0',
        'endpoints': {
            'GET /': 'Información de la API',
            'GET /tasks': 'Obtener todas las tareas',
            'GET /tasks/<id>': 'Obtener una tarea específica',
            'GET /tasks/<id>/details': 'Detalles avanzados (PATH + QUERY params)',
            'POST /tasks': 'Crear nueva tarea',
            'PUT /tasks/<id>': 'Actualizar tarea completa',
            'PATCH /tasks/<id>': 'Actualizar parcialmente una tarea',
            'DELETE /tasks/<id>': 'Eliminar una tarea'
        }
    })

# GET /tasks - Obtener todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Obtiene todas las tareas.
    Soporta filtrado opcional por estado completed.
    
    Query parameters:
    - completed: true/false para filtrar por estado
    """
    completed_filter = request.args.get('completed')
    
    if completed_filter is not None:
        # Filtrar por estado completed
        completed_bool = completed_filter.lower() == 'true'
        filtered_tasks = [task for task in tasks if task['completed'] == completed_bool]
        return jsonify({
            'tasks': filtered_tasks,
            'total': len(filtered_tasks)
        })
    
    return jsonify({
        'tasks': tasks,
        'total': len(tasks)
    })

# GET /tasks/<id> - Obtener tarea específica
@app.route('/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Obtiene una tarea específica por su ID
    """
    task = next((task for task in tasks if task['id'] == task_id), None)
    
    if task is None:
        return jsonify({
            'error': 'Tarea no encontrada',
            'message': f'No existe una tarea con ID: {task_id}'
        }), 404
    
    return jsonify(task)

# POST /tasks - Crear nueva tarea
@app.route('/tasks', methods=['POST'])
def create_task():
    """
    Crea una nueva tarea
    
    Body JSON requerido:
    {
        "title": "string",
        "description": "string" (opcional)
    }
    """
    if not request.json or 'title' not in request.json:
        return jsonify({
            'error': 'Datos inválidos',
            'message': 'El campo title es requerido'
        }), 400
    
    # Crear nueva tarea
    new_task = {
        'id': str(uuid.uuid4()),  # Generar ID único
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'completed': False,
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    
    tasks.append(new_task)
    
    # Enviar notificación WebSocket de nueva tarea creada
    websocket_message = {
        "type": "task_created",
        "task": new_task,
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }
    send_websocket_message(websocket_message)
    
    return jsonify({
        'message': 'Tarea creada exitosamente',
        'task': new_task
    }), 201

# PUT /tasks/<id> - Actualizar tarea completa
@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Actualiza una tarea completa (reemplaza todos los campos)
    
    Body JSON requerido:
    {
        "title": "string",
        "description": "string",
        "completed": boolean
    }
    """
    task = next((task for task in tasks if task['id'] == task_id), None)
    
    if task is None:
        return jsonify({
            'error': 'Tarea no encontrada',
            'message': f'No existe una tarea con ID: {task_id}'
        }), 404
    
    if not request.json:
        return jsonify({
            'error': 'Datos inválidos',
            'message': 'Se requiere JSON en el body'
        }), 400
    
    # Actualizar todos los campos
    task['title'] = request.json.get('title', task['title'])
    task['description'] = request.json.get('description', task['description'])
    task['completed'] = request.json.get('completed', task['completed'])
    
    # Enviar notificación WebSocket de tarea actualizada
    websocket_message = {
        "type": "task_updated",
        "task": task,
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }
    send_websocket_message(websocket_message)
    
    return jsonify({
        'message': 'Tarea actualizada exitosamente',
        'task': task
    })

# PATCH /tasks/<id> - Actualización parcial
@app.route('/tasks/<string:task_id>', methods=['PATCH'])
def patch_task(task_id):
    """
    Actualiza parcialmente una tarea (solo los campos enviados)
    
    Body JSON (todos los campos son opcionales):
    {
        "title": "string",
        "description": "string", 
        "completed": boolean
    }
    """
    task = next((task for task in tasks if task['id'] == task_id), None)
    
    if task is None:
        return jsonify({
            'error': 'Tarea no encontrada',
            'message': f'No existe una tarea con ID: {task_id}'
        }), 404
    
    if not request.json:
        return jsonify({
            'error': 'Datos inválidos',
            'message': 'Se requiere JSON en el body'
        }), 400
    
    # Actualizar solo los campos proporcionados
    if 'title' in request.json:
        task['title'] = request.json['title']
    if 'description' in request.json:
        task['description'] = request.json['description']
    if 'completed' in request.json:
        task['completed'] = request.json['completed']
    
    # Enviar notificación WebSocket de tarea actualizada
    websocket_message = {
        "type": "task_updated",
        "task": task,
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }
    send_websocket_message(websocket_message)
    
    return jsonify({
        'message': 'Tarea actualizada parcialmente',
        'task': task
    })

# DELETE /tasks/<id> - Eliminar tarea
@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Elimina una tarea específica
    """
    global tasks
    task = next((task for task in tasks if task['id'] == task_id), None)
    
    if task is None:
        return jsonify({
            'error': 'Tarea no encontrada',
            'message': f'No existe una tarea con ID: {task_id}'
        }), 404
    
    tasks = [task for task in tasks if task['id'] != task_id]
    
    # Enviar notificación WebSocket de tarea eliminada
    websocket_message = {
        "type": "task_deleted",
        "task": task,
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }
    send_websocket_message(websocket_message)
    
    return jsonify({
        'message': 'Tarea eliminada exitosamente',
        'deleted_task': task
    })

# GET /tasks/<id>/details - Ejemplo combinando PATH y QUERY parameters
@app.route('/tasks/<string:task_id>/details', methods=['GET'])
def get_task_details(task_id):
    """
    Obtiene detalles de una tarea específica con opciones de personalización.
    
    PATH PARAMETER:
    - task_id: ID de la tarea a obtener
    
    QUERY PARAMETERS:
    - include_metadata: true/false - incluir metadatos (default: false)
    - format: json/summary/full - formato de respuesta (default: json)
    - lang: es/en - idioma de los mensajes (default: es)
    - fields: title,description,completed - campos específicos a incluir
    
    Ejemplo: /tasks/1/details?include_metadata=true&format=full&lang=en&fields=title,completed
    """
    # Buscar la tarea (PATH PARAMETER)
    task = next((task for task in tasks if task['id'] == task_id), None)
    
    if task is None:
        return jsonify({
            'error': 'Tarea no encontrada',
            'message': f'No existe una tarea con ID: {task_id}'
        }), 404
    
    # Procesar QUERY PARAMETERS
    include_metadata = request.args.get('include_metadata', 'false').lower() == 'true'
    format_type = request.args.get('format', 'json').lower()
    language = request.args.get('lang', 'es').lower()
    fields = request.args.get('fields', '').split(',') if request.args.get('fields') else []
    
    # Validar formato
    if format_type not in ['json', 'summary', 'full']:
        return jsonify({
            'error': 'Formato inválido',
            'message': 'Los formatos válidos son: json, summary, full'
        }), 400
    
    # Construir respuesta base
    response_data = task.copy()
    
    # Filtrar campos específicos si se solicita
    if fields and fields != ['']:
        filtered_task = {}
        valid_fields = ['id', 'title', 'description', 'completed', 'created_at']
        
        for field in fields:
            field = field.strip()
            if field in valid_fields:
                filtered_task[field] = task.get(field)
        
        response_data = filtered_task
    
    # Agregar metadatos si se solicita
    if include_metadata:
        response_data['metadata'] = {
            'request_timestamp': datetime.utcnow().isoformat() + 'Z',
            'task_age_days': (datetime.utcnow() - datetime.fromisoformat(task['created_at'].replace('Z', ''))).days,
            'path_parameter': task_id,
            'query_parameters': dict(request.args),
            'endpoint': f'/tasks/{task_id}/details'
        }
    
    # Diferentes formatos de respuesta
    if format_type == 'summary':
        messages = {
            'es': {
                'summary': f"Tarea '{task['title']}' - {'✅ Completada' if task['completed'] else '⏳ Pendiente'}",
                'details': f"Creada el {task['created_at'][:10]}"
            },
            'en': {
                'summary': f"Task '{task['title']}' - {'✅ Completed' if task['completed'] else '⏳ Pending'}",
                'details': f"Created on {task['created_at'][:10]}"
            }
        }
        
        lang_messages = messages.get(language, messages['es'])
        return jsonify({
            'task_id': task_id,
            'summary': lang_messages['summary'],
            'details': lang_messages['details'],
            'format': 'summary'
        })
    
    elif format_type == 'full':
        # Análisis completo de la tarea
        created_date = datetime.fromisoformat(task['created_at'].replace('Z', ''))
        age_days = (datetime.utcnow() - created_date).days
        
        analysis = {
            'basic_info': response_data,
            'analysis': {
                'word_count': len(task['description'].split()) if task['description'] else 0,
                'title_length': len(task['title']),
                'age_days': age_days,
                'status_emoji': '✅' if task['completed'] else '⏳',
                'priority_suggestion': 'Alta' if not task['completed'] and age_days > 7 else 'Normal'
            },
            'request_info': {
                'path_param_received': task_id,
                'query_params_received': dict(request.args),
                'total_query_params': len(request.args)
            }
        }
        
        return jsonify(analysis)
    
    # Formato JSON por defecto
    return jsonify({
        'task': response_data,
        'request_info': {
            'path_parameter': task_id,
            'query_parameters': dict(request.args),
            'format': format_type
        }
    })

# Manejo de errores globales
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Recurso no encontrado',
        'message': 'El endpoint solicitado no existe'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Error interno del servidor',
        'message': 'Ocurrió un error inesperado'
    }), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask API...")
    print("📝 API de Tareas disponible en: http://localhost:8001")
    print("📚 Documentación disponible en: http://localhost:8001")
    
    # Ejecutar en modo desarrollo
    app.run(
        host='0.0.0.0',  # Permitir conexiones externas
        port=8001,       # Puerto libre
        debug=False      # Sin debug para evitar reinicios automáticos
    )
