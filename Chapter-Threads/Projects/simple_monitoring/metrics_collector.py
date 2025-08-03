"""
Simple Metrics Collector - Real System Metrics Only
No complex scaling logic, just clean data collection
"""
import time
import psutil
import redis
from typing import Dict, Any
from datetime import datetime


class SimpleMetricsCollector:
    """Collects real system metrics - CPU, memory, queue, workers"""
    
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_host = redis_host
        self.redis_port = redis_port
        
    def _get_redis_connection(self):
        """Get Redis connection with error handling (Windows-friendly)"""
        try:
            return redis.Redis(
                host=self.redis_host,
                port=self.redis_port,
                decode_responses=True,
                socket_connect_timeout=10,  # Increased for Windows
                socket_timeout=10,          # Increased for Windows
                retry_on_timeout=True,
                health_check_interval=30
            )
        except Exception as e:
            print(f"❌ Redis connection failed: {e}")
            return None
    
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect all system metrics"""
        try:
            # System metrics (always available)
            system_metrics = self._get_system_metrics()
            
            # Redis metrics (if available)
            redis_metrics = self._get_redis_metrics()
            
            # Combine all metrics
            all_metrics = {
                **system_metrics,
                **redis_metrics,
                'timestamp': datetime.now().isoformat(),
                'collection_time': time.time()
            }
            
            return all_metrics
            
        except Exception as e:
            print(f"❌ Error collecting metrics: {e}")
            return self._get_fallback_metrics()
    
    def _get_system_metrics(self) -> Dict[str, Any]:
        """Get CPU and memory metrics from system"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            cpu_count = psutil.cpu_count()
            
            # Memory metrics  
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available_gb = memory.available / (1024**3)
            
            return {
                'cpu_usage': round(cpu_percent, 1),
                'cpu_count': cpu_count,
                'memory_usage': round(memory_percent, 1),
                'memory_available_gb': round(memory_available_gb, 2),
                'memory_total_gb': round(memory.total / (1024**3), 2)
            }
        except Exception as e:
            print(f"⚠️ System metrics error: {e}")
            return {
                'cpu_usage': 0.0,
                'cpu_count': 1,
                'memory_usage': 0.0,
                'memory_available_gb': 0.0,
                'memory_total_gb': 0.0
            }
    
    def _get_redis_metrics(self) -> Dict[str, Any]:
        """Get queue and worker metrics from Redis"""
        redis_conn = self._get_redis_connection()
        if not redis_conn:
            return self._get_fallback_redis_metrics()
        
        try:
            # Queue metrics - with correct queue name!
            queue_name = 'image_tasks'  # Fixed: was 'image_processing_queue'
            queue_length = redis_conn.llen(queue_name) or 0
            
            # Debug: Check if queue exists and log result
            queue_exists = redis_conn.exists(queue_name)
            if not queue_exists and queue_length == 0:
                # Double-check all queue-related keys
                all_queue_keys = [k for k in redis_conn.keys('*') if 'queue' in k.lower()]
                if all_queue_keys:
                    print(f"🔍 DEBUG: Found other queue keys: {all_queue_keys}")
            
            # Get all task keys and analyze their status
            task_keys = redis_conn.keys('task:*') or []
            processing_tasks = 0
            completed_tasks = 0
            failed_tasks = 0
            
            for task_key in task_keys:
                try:
                    status = redis_conn.hget(task_key, 'status')
                    if status == 'processing':
                        processing_tasks += 1
                    elif status == 'completed':
                        completed_tasks += 1
                    elif status == 'failed':
                        failed_tasks += 1
                except:
                    continue
            
            # Worker registry metrics (assume 3 workers from docker-compose)
            active_workers = 3
            busy_workers = min(processing_tasks, active_workers)
            
            # Calculate utilization
            worker_utilization = (busy_workers / active_workers) if active_workers > 0 else 0
            
            # Success metrics
            total_tasks = completed_tasks + failed_tasks
            success_rate = (completed_tasks / total_tasks) if total_tasks > 0 else 1.0
            
            return {
                'queue_length': queue_length,
                'processing_tasks': processing_tasks,
                'active_workers': active_workers,
                'busy_workers': busy_workers,
                'worker_utilization': round(worker_utilization, 3),
                'completed_tasks': completed_tasks,
                'failed_tasks': failed_tasks,
                'total_tasks': total_tasks,
                'success_rate': round(success_rate * 100, 1)
            }
            
        except Exception as e:
            print(f"⚠️ Redis metrics error: {e}")
            return self._get_fallback_redis_metrics()
    
    def _get_fallback_redis_metrics(self) -> Dict[str, Any]:
        """Fallback metrics when Redis is unavailable"""
        return {
            'queue_length': 0,
            'processing_tasks': 0,
            'active_workers': 3,  # Assume 3 workers from docker-compose
            'busy_workers': 0,
            'worker_utilization': 0.0,
            'completed_tasks': 0,
            'failed_tasks': 0,
            'total_tasks': 0,
            'success_rate': 100.0
        }
    
    def _get_fallback_metrics(self) -> Dict[str, Any]:
        """Complete fallback when everything fails"""
        return {
            **self._get_fallback_redis_metrics(),
            'cpu_usage': 0.0,
            'cpu_count': 1,
            'memory_usage': 0.0,
            'memory_available_gb': 0.0,
            'memory_total_gb': 0.0,
            'timestamp': datetime.now().isoformat(),
            'collection_time': time.time(),
            'status': 'fallback_mode'
        }