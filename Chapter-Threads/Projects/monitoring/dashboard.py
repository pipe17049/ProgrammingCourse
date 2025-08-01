import time
import os
import threading
from datetime import datetime
from monitoring.metrics_collector import MetricsCollector
from monitoring.worker_manager import WorkerManager

class RealTimeDashboard:
    """Dashboard en tiempo real para monitoring"""
    
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.metrics_collector = MetricsCollector(redis_host, redis_port)
        self.worker_manager = WorkerManager(redis_host, redis_port)
        self.is_running = False
        self.refresh_interval = 3  # segundos (menos frecuente = menos parpadeo)
    
    def start(self, auto_scale=False):
        """Inicia el dashboard"""
        self.is_running = True
        
        # Iniciar auto-scaling si se solicita
        if auto_scale:
            self.worker_manager.start_monitoring(interval=15)
            print("🤖 Auto-scaling ENABLED")
        
        print("🚀 AUTO-SCALING DASHBOARD")
        print("=" * 50)
        print("Press Ctrl+C to exit\n")
        
        try:
            while self.is_running:
                self._clear_screen()
                self._display_dashboard()
                time.sleep(self.refresh_interval)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Detiene el dashboard"""
        self.is_running = False
        self.worker_manager.stop_monitoring()
        print("\n👋 Dashboard stopped")
    
    def _clear_screen(self):
        """Limpiar pantalla solo al inicio, luego actualizar en su lugar"""
        # Solo limpiar la primera vez
        if not hasattr(self, '_screen_cleared'):
            import platform
            try:
                if platform.system().lower() == 'windows':
                    os.system('cls')
                else:
                    print('\033[2J\033[H', end='', flush=True)
            except:
                print('\n' * 3)
            self._screen_cleared = True
        else:
            # Solo mover cursor arriba para actualizar en el mismo lugar
            print('\033[H', end='', flush=True)
    
    def _display_dashboard(self):
        """Muestra el dashboard principal"""
        # Obtener datos actuales
        status = self.worker_manager.get_current_status()
        metrics = status['metrics']
        decision = status['scaling_decision']
        
        # Header
        print("=" * 80)
        print("🖼️  DJANGO IMAGE PROCESSING - REAL-TIME DASHBOARD")
        print("=" * 80)
        print(f"⏰ Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Métricas principales
        self._display_main_metrics(metrics)
        print()
        
        # Estado de workers
        self._display_worker_status(metrics)
        print()
        
        # Decisión de scaling
        self._display_scaling_decision(decision)
        print()
        
        # Gráfico de cola
        self._display_queue_chart(metrics)
        print()
        
        # Historial reciente
        self._display_recent_history()
        print()
        
        # Comandos disponibles
        self._display_commands()
    
    def _display_main_metrics(self, metrics):
        """Muestra métricas principales"""
        print("📊 SYSTEM METRICS")
        print("-" * 40)
        
        # Fila 1: Queue y Workers
        queue_length = metrics.get('queue_length', 0)
        active_workers = metrics.get('active_workers', 0)
        busy_workers = metrics.get('busy_workers', 0)
        
        print(f"📦 Queue Length:     {queue_length:>3d} tasks")
        print(f"👷 Active Workers:   {active_workers:>3d}")
        print(f"⚡ Busy Workers:     {busy_workers:>3d}")
        
        # Fila 2: Performance
        utilization = metrics.get('worker_utilization', 0)
        avg_time = metrics.get('avg_processing_time', 0)
        success_rate = metrics.get('success_rate', 1.0)
        
        utilization_icon = self._get_utilization_icon(utilization)
        print(f"📈 Worker Utilization: {utilization_icon} {utilization:>5.1%}")
        print(f"⏱️  Avg Process Time: {avg_time:>5.1f}s")
        print(f"✅ Success Rate:     {success_rate:>5.1%}")
        
        # Fila 3: Sistema
        cpu_usage = metrics.get('cpu_usage', 0)
        memory_usage = metrics.get('memory_usage', 0)
        memory_available = metrics.get('memory_available_gb', 0)
        
        cpu_icon = self._get_cpu_icon(cpu_usage)
        print(f"🖥️  CPU Usage:       {cpu_icon} {cpu_usage:>5.1f}%")
        print(f"💾 Memory Usage:     {memory_usage:>5.1f}%")
        print(f"💽 Memory Available: {memory_available:>5.1f} GB")
    
    def _display_worker_status(self, metrics):
        """Muestra estado detallado de workers"""
        print("👷 WORKER STATUS")
        print("-" * 40)
        
        # Simulamos estado de workers especializados
        active_workers = metrics.get('active_workers', 0)
        busy_workers = metrics.get('busy_workers', 0)
        
        workers_info = [
            ("worker-1", "I/O Specialist", "resize, blur, brightness"),
            ("worker-2", "CPU Specialist", "sharpen, edges"),
            ("worker-3", "General Purpose", "ALL FILTERS"),
        ]
        
        for i, (name, type_name, capabilities) in enumerate(workers_info):
            status = "🟢 ACTIVE" if i < active_workers else "🔴 INACTIVE"
            busy = "⚡ BUSY" if i < busy_workers else "💤 IDLE"
            
            print(f"{name:>10}: {status:<10} {busy:<8} | {capabilities}")
        
        # Workers adicionales (si hay scaling)
        if active_workers > 3:
            extra_workers = active_workers - 3
            for i in range(extra_workers):
                worker_num = 4 + i
                busy = "⚡ BUSY" if (3 + i) < busy_workers else "💤 IDLE"
                print(f"worker-{worker_num}:   🟢 ACTIVE  {busy:<8} | Extra capacity")
    
    def _display_scaling_decision(self, decision):
        """Muestra decisión de scaling actual"""
        print("🎯 SCALING DECISION")
        print("-" * 40)
        
        action = decision.get('action', 'no_action')
        target = decision.get('target_workers', 0)
        reason = decision.get('reason', 'No reason')
        confidence = decision.get('confidence', 0)
        
        action_icons = {
            'scale_up': '🔺 SCALE UP',
            'scale_down': '🔻 SCALE DOWN',
            'no_action': '🟢 MAINTAIN'
        }
        
        action_display = action_icons.get(action, action.upper())
        confidence_bar = self._get_confidence_bar(confidence)
        
        print(f"Action:     {action_display}")
        print(f"Target:     {target} workers")
        print(f"Confidence: {confidence_bar} {confidence:.1%}")
        print(f"Reason:     {reason}")
    
    def _display_queue_chart(self, metrics):
        """Muestra gráfico de cola"""
        print("📈 QUEUE VISUALIZATION")
        print("-" * 40)
        
        queue_length = metrics.get('queue_length', 0)
        max_display = 50
        
        # Crear barra visual
        if queue_length == 0:
            bar = "Empty"
            color = "🟢"
        elif queue_length <= 5:
            bar = "█" * min(queue_length, max_display)
            color = "🟢"
        elif queue_length <= 15:
            bar = "█" * min(queue_length, max_display)
            color = "🟡"
        else:
            bar = "█" * min(queue_length, max_display)
            color = "🔴"
            if queue_length > max_display:
                bar += f"... (+{queue_length - max_display})"
        
        print(f"Queue: {color} {bar}")
        print(f"Scale: |{'-' * 10}|{'-' * 10}|{'-' * 10}|{'-' * 10}|{'-' * 10}|")
        print(f"       0    10   20   30   40   50")
    
    def _display_recent_history(self):
        """Muestra historial reciente"""
        print("📚 RECENT SCALING HISTORY")
        print("-" * 40)
        
        history = self.worker_manager.get_scaling_history(last_n=5)
        
        if not history:
            print("No recent scaling actions")
            return
        
        for entry in history[-5:]:
            timestamp = entry['timestamp'][:19]  # Solo fecha y hora
            action = entry['action']
            from_workers = entry['from_workers']
            to_workers = entry['to_workers']
            success = "✅" if entry['success'] else "❌"
            
            action_icons = {
                'scale_up': '🔺',
                'scale_down': '🔻',
                'no_action': '🟢'
            }
            
            icon = action_icons.get(action, '❓')
            print(f"{timestamp} {icon} {from_workers}→{to_workers} workers {success}")
    
    def _display_commands(self):
        """Muestra comandos disponibles"""
        print("⌨️  AVAILABLE COMMANDS")
        print("-" * 40)
        print("Ctrl+C: Exit dashboard")
        print("In another terminal:")
        print("  python monitoring/worker_manager.py --manual-scale 5")
        print("  curl -X POST localhost:8000/api/stress-test/")
    
    def _get_utilization_icon(self, utilization):
        """Icono basado en utilización"""
        if utilization < 0.3:
            return "🟢"
        elif utilization < 0.7:
            return "🟡"
        else:
            return "🔴"
    
    def _get_cpu_icon(self, cpu_usage):
        """Icono basado en uso de CPU"""
        if cpu_usage < 50:
            return "🟢"
        elif cpu_usage < 80:
            return "🟡"
        else:
            return "🔴"
    
    def _get_confidence_bar(self, confidence):
        """Barra visual de confianza"""
        bars = int(confidence * 10)
        return "█" * bars + "░" * (10 - bars)

class InteractiveDashboard(RealTimeDashboard):
    """Dashboard interactivo con comandos"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command_thread = None
    
    def start(self, auto_scale=False):
        """Inicia dashboard interactivo"""
        self.is_running = True
        
        if auto_scale:
            self.worker_manager.start_monitoring(interval=15)
        
        # Thread para comandos
        self.command_thread = threading.Thread(target=self._command_loop, daemon=True)
        self.command_thread.start()
        
        try:
            while self.is_running:
                self._clear_screen()
                self._display_dashboard()
                self._display_interactive_commands()
                time.sleep(self.refresh_interval)
        except KeyboardInterrupt:
            self.stop()
    
    def _command_loop(self):
        """Loop para comandos interactivos"""
        while self.is_running:
            try:
                cmd = input().strip().lower()
                if cmd == 'q':
                    self.is_running = False
                elif cmd.startswith('scale '):
                    target = int(cmd.split()[1])
                    self.worker_manager.manual_scale(target)
                elif cmd == 'stress':
                    self._trigger_stress_test()
            except:
                pass
    
    def _display_interactive_commands(self):
        """Comandos interactivos"""
        print("\n⌨️  INTERACTIVE COMMANDS")
        print("-" * 40)
        print("q: Quit | scale N: Scale to N workers | stress: Trigger stress test")
    
    def _trigger_stress_test(self):
        """Dispara stress test"""
        try:
            import requests
            response = requests.post('http://localhost:8000/api/stress-test/')
            print(f"Stress test triggered: {response.status_code}")
        except:
            print("Failed to trigger stress test")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Real-time Dashboard')
    parser.add_argument('--auto-scale', action='store_true', help='Enable auto-scaling')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    
    args = parser.parse_args()
    
    if args.interactive:
        dashboard = InteractiveDashboard()
    else:
        dashboard = RealTimeDashboard()
    
    print("🚀 Starting Real-Time Dashboard...")
    print("Press Ctrl+C to exit")
    
    dashboard.start(auto_scale=args.auto_scale)