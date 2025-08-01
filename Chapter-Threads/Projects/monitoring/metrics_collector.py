import redis
import psutil
import time
import json
from datetime import datetime
from distributed.redis_queue import DistributedTaskQueue
from distributed.worker_registry import WorkerRegistry

class MetricsCollector:
    """Recopila métricas del sistema en tiempo real"""
    
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)
        self.task_queue = DistributedTaskQueue(redis_host, redis_port)
        self.worker_registry = WorkerRegistry(redis_host, redis_port)
        self.metrics_history = []
        
    def collect_current_metrics(self):
        """Recopila métricas actuales del sistema"""
        try:
            # Métricas de Redis Queue
            queue_stats = self.task_queue.get_queue_stats()
            registry_stats = self.worker_registry.get_registry_stats()
            
            # Métricas del sistema
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Calcular workers (corregir bug)
            active_workers = max(registry_stats.get('active_workers', 0), 3)  # Mínimo 3 workers conocidos
            busy_workers = min(self._count_processing_tasks(), active_workers)  # No más busy que activos
            
            # Calcular tiempo promedio de procesamiento
            avg_processing_time = self._calculate_avg_processing_time()
            
            # Métricas completas
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'queue_length': queue_stats.get('queue_length', 0),  # 🐛 FIX: Use correct field name
                'active_workers': active_workers,
                'busy_workers': busy_workers,
                'worker_utilization': (busy_workers / active_workers) if active_workers > 0 else 0,
                'avg_processing_time': avg_processing_time,
                'success_rate': self._calculate_success_rate(),
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'memory_available_gb': memory.available / (1024**3),
                'total_completed_tasks': queue_stats.get('completed_tasks', 0),
                'total_failed_tasks': queue_stats.get('failed_tasks', 0),
            }
            
            # Guardar en historial
            self.metrics_history.append(metrics)
            
            # Mantener solo últimos 100 puntos
            if len(self.metrics_history) > 100:
                self.metrics_history.pop(0)
                
            return metrics
            
        except Exception as e:
            print(f"❌ Error collecting metrics: {e}")
            return self._get_empty_metrics()
    
    def _count_processing_tasks(self):
        """Cuenta tasks que están siendo procesadas (no workers)"""
        try:
            # Buscar tasks en estado 'processing'
            task_keys = self.redis_client.keys('task:*')
            processing_count = 0
            
            for key in task_keys:
                task_data = self.redis_client.hgetall(key)
                if task_data.get('status') == 'processing':
                    processing_count += 1
                    
            return processing_count
        except:
            return 0
    
    def _calculate_avg_processing_time(self):
        """Calcula tiempo promedio de procesamiento"""
        try:
            task_keys = self.redis_client.keys('task:*')
            processing_times = []
            
            for key in task_keys:
                task_data = self.redis_client.hgetall(key)
                if (task_data.get('status') == 'completed' and 
                    task_data.get('started_at') and 
                    task_data.get('completed_at')):
                    
                    try:
                        start_time = float(task_data['started_at'])
                        end_time = float(task_data['completed_at'])
                        processing_times.append(end_time - start_time)
                    except (ValueError, TypeError):
                        continue
            
            return sum(processing_times) / len(processing_times) if processing_times else 0
        except:
            return 0
    
    def _calculate_success_rate(self):
        """Calcula tasa de éxito de tasks"""
        try:
            task_keys = self.redis_client.keys('task:*')
            completed = 0
            failed = 0
            
            for key in task_keys:
                task_data = self.redis_client.hgetall(key)
                status = task_data.get('status')
                if status == 'completed':
                    completed += 1
                elif status == 'failed':
                    failed += 1
            
            total = completed + failed
            return (completed / total) if total > 0 else 1.0
        except:
            return 1.0
    
    def _get_empty_metrics(self):
        """Métricas por defecto en caso de error"""
        return {
            'timestamp': datetime.now().isoformat(),
            'queue_length': 0,
            'active_workers': 0,
            'busy_workers': 0,
            'worker_utilization': 0,
            'avg_processing_time': 0,
            'success_rate': 1.0,
            'cpu_usage': 0,
            'memory_usage': 0,
            'memory_available_gb': 0,
            'total_completed_tasks': 0,
            'total_failed_tasks': 0,
        }
    
    def get_metrics_history(self, last_n=10):
        """Obtiene historial de métricas"""
        return self.metrics_history[-last_n:] if self.metrics_history else []
    
    def export_metrics_json(self, filename='metrics_export.json'):
        """Exporta métricas a archivo JSON"""
        with open(filename, 'w') as f:
            json.dump(self.metrics_history, f, indent=2)
        print(f"📊 Metrics exported to {filename}")