import time
import subprocess
import threading
from datetime import datetime
from monitoring.metrics_collector import MetricsCollector
from monitoring.scaling_rules import ScalingRules, ScalingDecision

class WorkerManager:
    """Administrador de workers con auto-scaling"""
    
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.metrics_collector = MetricsCollector(redis_host, redis_port)
        self.scaling_rules = ScalingRules()
        self.is_running = False
        self.monitoring_thread = None
        self.current_worker_count = 3  # Empezamos con 3 workers por defecto
        
        # Historia de acciones de scaling
        self.scaling_history = []
        
    def start_monitoring(self, interval=10):
        """Inicia el monitoreo automático"""
        if self.is_running:
            print("⚠️ Monitoring already running")
            return
            
        self.is_running = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop, 
            args=(interval,), 
            daemon=True
        )
        self.monitoring_thread.start()
        print(f"🚀 Auto-scaling monitoring started (interval: {interval}s)")
    
    def stop_monitoring(self):
        """Detiene el monitoreo automático"""
        self.is_running = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        print("🛑 Auto-scaling monitoring stopped")
    
    def _monitoring_loop(self, interval):
        """Loop principal de monitoreo"""
        while self.is_running:
            try:
                # Recopilar métricas
                metrics = self.metrics_collector.collect_current_metrics()
                
                # Evaluar necesidad de scaling
                decision = self.scaling_rules.evaluate_scaling(metrics)
                
                # Ejecutar acción si es necesario
                if decision.action != 'no_action':
                    self._execute_scaling_decision(decision, metrics)
                
                # Log del estado
                self._log_system_status(metrics, decision)
                
            except Exception as e:
                print(f"❌ Error in monitoring loop: {e}")
            
            time.sleep(interval)
    
    def _execute_scaling_decision(self, decision: ScalingDecision, metrics):
        """Ejecuta decisión de scaling"""
        print(f"\n🎯 SCALING DECISION:")
        print(f"   Action: {decision.action}")
        print(f"   Current Workers: {metrics['active_workers']}")
        print(f"   Target Workers: {decision.target_workers}")
        print(f"   Reason: {decision.reason}")
        print(f"   Confidence: {decision.confidence:.1%}")
        
        # Ejecutar scaling
        if decision.action == 'scale_up':
            success = self._scale_workers_up(decision.target_workers)
        elif decision.action == 'scale_down':
            success = self._scale_workers_down(decision.target_workers)
        else:
            success = False
        
        # Registrar en historia
        self.scaling_history.append({
            'timestamp': datetime.now().isoformat(),
            'action': decision.action,
            'from_workers': metrics['active_workers'],
            'to_workers': decision.target_workers,
            'reason': decision.reason,
            'confidence': decision.confidence,
            'success': success,
        })
        
        # Mantener solo últimas 50 acciones
        if len(self.scaling_history) > 50:
            self.scaling_history.pop(0)
    
    def _scale_workers_up(self, target_count):
        """Escala workers hacia arriba"""
        try:
            print(f"🔺 Scaling UP to {target_count} workers...")
            
            # Cross-platform docker-compose command
            docker_cmd = self._get_docker_compose_cmd()
            worker_3_count = max(1, target_count - 2)  # worker-1 y worker-2 siempre 1
            
            cmd = docker_cmd + [
                'up', '-d', '--scale', f'worker-1=1', 
                '--scale', f'worker-2=1', '--scale', f'worker-3={worker_3_count}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.current_worker_count = target_count
                print(f"✅ Successfully scaled UP to {target_count} workers")
                return True
            else:
                print(f"❌ Failed to scale UP: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error scaling UP: {e}")
            return False
    
    def _scale_workers_down(self, target_count):
        """Escala workers hacia abajo"""
        try:
            print(f"🔻 Scaling DOWN to {target_count} workers...")
            
            # Cross-platform docker-compose command
            docker_cmd = self._get_docker_compose_cmd()
            worker_3_count = max(0, target_count - 2)  # worker-1 y worker-2 siempre 1
            
            cmd = docker_cmd + [
                'up', '-d', '--scale', f'worker-1=1',
                '--scale', f'worker-2=1', '--scale', f'worker-3={worker_3_count}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.current_worker_count = target_count
                print(f"✅ Successfully scaled DOWN to {target_count} workers")
                return True
            else:
                print(f"❌ Failed to scale DOWN: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error scaling DOWN: {e}")
            return False
    
    def _log_system_status(self, metrics, decision):
        """Log del estado del sistema"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        queue = metrics['queue_length']
        workers = metrics['active_workers']
        utilization = metrics['worker_utilization']
        cpu = metrics['cpu_usage']
        
        status_icon = "🟢" if decision.action == 'no_action' else ("🔺" if decision.action == 'scale_up' else "🔻")
        
        print(f"{status_icon} [{timestamp}] Queue:{queue:2d} | Workers:{workers:2d} | Util:{utilization:5.1%} | CPU:{cpu:5.1f}%")
    
    def get_current_status(self):
        """Obtiene estado actual del sistema"""
        metrics = self.metrics_collector.collect_current_metrics()
        decision = self.scaling_rules.evaluate_scaling(metrics)
        
        return {
            'metrics': metrics,
            'scaling_decision': {
                'action': decision.action,
                'target_workers': decision.target_workers,
                'reason': decision.reason,
                'confidence': decision.confidence,
            },
            'scaling_config': self.scaling_rules.get_scaling_config(),
            'current_worker_count': self.current_worker_count,
            'is_monitoring': self.is_running,
        }
    
    def get_scaling_history(self, last_n=10):
        """Obtiene historial de scaling"""
        return self.scaling_history[-last_n:] if self.scaling_history else []
    
    def manual_scale(self, target_workers):
        """Scaling manual"""
        if target_workers < self.scaling_rules.min_workers:
            print(f"❌ Cannot scale below minimum ({self.scaling_rules.min_workers})")
            return False
        
        if target_workers > self.scaling_rules.max_workers:
            print(f"❌ Cannot scale above maximum ({self.scaling_rules.max_workers})")
            return False
        
        current_metrics = self.metrics_collector.collect_current_metrics()
        current_workers = current_metrics['active_workers']
        
        print(f"🎮 Manual scaling: {current_workers} → {target_workers}")
        
        if target_workers > current_workers:
            return self._scale_workers_up(target_workers)
        elif target_workers < current_workers:
            return self._scale_workers_down(target_workers)
        else:
            print("✅ Already at target worker count")
            return True
    
    def _get_docker_compose_cmd(self):
        """Obtiene comando docker-compose cross-platform"""
        import platform
        
        # Detectar sistema operativo
        system = platform.system().lower()
        
        # Intentar diferentes variantes de docker-compose
        commands_to_try = [
            ['docker-compose'],  # Versión clásica
            ['docker', 'compose'],  # Docker Compose V2
        ]
        
        for cmd in commands_to_try:
            try:
                result = subprocess.run(cmd + ['--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return cmd
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        # Fallback por defecto
        return ['docker-compose']

if __name__ == "__main__":
    # Script para ejecutar worker manager standalone
    import argparse
    
    parser = argparse.ArgumentParser(description='Worker Manager Auto-Scaler')
    parser.add_argument('--auto-scale', action='store_true', help='Start auto-scaling')
    parser.add_argument('--interval', type=int, default=10, help='Monitoring interval (seconds)')
    parser.add_argument('--manual-scale', type=int, help='Manual scale to N workers')
    
    args = parser.parse_args()
    
    manager = WorkerManager()
    
    if args.manual_scale:
        manager.manual_scale(args.manual_scale)
    elif args.auto_scale:
        print("🚀 Starting auto-scaling worker manager...")
        print("Press Ctrl+C to stop")
        
        manager.start_monitoring(args.interval)
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            manager.stop_monitoring()
            print("\n👋 Auto-scaler stopped")