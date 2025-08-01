#!/usr/bin/env python3
"""
CLI cross-platform para auto-scaling system
Funciona en Windows, Mac, Linux
"""

import sys
import time
import requests
import json
import argparse
from datetime import datetime
import platform

class AutoScalingCLI:
    """Command Line Interface para auto-scaling"""
    
    def __init__(self, api_url='http://localhost:8000'):
        self.api_url = api_url.rstrip('/')
        
    def check_api_status(self):
        """Verifica si la API está funcionando"""
        try:
            response = requests.get(f'{self.api_url}/api/health/', timeout=5)
            if response.status_code == 200:
                print(f"✅ API is running at {self.api_url}")
                return True
            else:
                print(f"❌ API returned status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Cannot connect to API: {e}")
            return False
    
    def get_system_metrics(self):
        """Obtiene métricas del sistema"""
        try:
            response = requests.get(f'{self.api_url}/api/system/metrics/')
            if response.status_code == 200:
                data = response.json()
                self._display_metrics(data['metrics'], data['scaling_decision'])
                return data
            else:
                print(f"❌ Failed to get metrics: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error getting metrics: {e}")
            return None
    
    def trigger_stress_test(self, num_tasks=20):
        """Dispara stress test"""
        try:
            print(f"🔥 Triggering stress test with {num_tasks} tasks...")
            
            response = requests.post(f'{self.api_url}/api/stress-test/', 
                                   data={'num_tasks': num_tasks})
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Created {data['task_count']} stress tasks")
                print(f"📊 Task IDs: {', '.join(data['task_ids'][:5])}{'...' if len(data['task_ids']) > 5 else ''}")
                return True
            else:
                print(f"❌ Stress test failed: {response.status_code}")
                if response.text:
                    print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error triggering stress test: {e}")
            return False
    
    def manual_scale(self, target_workers):
        """Scaling manual usando worker manager"""
        try:
            # Importar worker manager (debe estar en PYTHONPATH)
            sys.path.append('.')
            from monitoring.worker_manager import WorkerManager
            
            manager = WorkerManager()
            success = manager.manual_scale(target_workers)
            
            if success:
                print(f"✅ Successfully scaled to {target_workers} workers")
            else:
                print(f"❌ Failed to scale to {target_workers} workers")
                
            return success
            
        except ImportError:
            print("❌ Cannot import WorkerManager. Run from project root directory.")
            return False
        except Exception as e:
            print(f"❌ Error during manual scaling: {e}")
            return False
    
    def monitor_system(self, duration=60, interval=3):
        """Monitorea el sistema por un tiempo determinado"""
        print(f"📈 Monitoring system for {duration} seconds (interval: {interval}s)")
        print("=" * 70)
        
        start_time = time.time()
        last_workers = 0
        scaling_events = []
        
        while time.time() - start_time < duration:
            try:
                response = requests.get(f'{self.api_url}/api/system/metrics/')
                if response.status_code == 200:
                    data = response.json()
                    metrics = data['metrics']
                    decision = data['scaling_decision']
                    
                    # Detectar cambios en workers
                    current_workers = metrics['active_workers']
                    if current_workers != last_workers and last_workers > 0:
                        event = {
                            'time': datetime.now().strftime('%H:%M:%S'),
                            'action': 'scale_up' if current_workers > last_workers else 'scale_down',
                            'from': last_workers,
                            'to': current_workers
                        }
                        scaling_events.append(event)
                        
                        action_icon = "🔺" if event['action'] == 'scale_up' else "🔻"
                        print(f"\n{action_icon} SCALING DETECTED: {event['from']} → {event['to']} workers")
                    
                    # Mostrar estado actual
                    self._display_monitoring_line(metrics, decision)
                    last_workers = current_workers
                    
                else:
                    print(f"❌ Failed to get metrics: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
            
            time.sleep(interval)
        
        # Resumen final
        print(f"\n📊 MONITORING SUMMARY ({duration}s)")
        print("=" * 40)
        if scaling_events:
            print(f"🎯 Scaling events detected: {len(scaling_events)}")
            for event in scaling_events:
                action_icon = "🔺" if event['action'] == 'scale_up' else "🔻"
                print(f"   [{event['time']}] {action_icon} {event['from']} → {event['to']} workers")
        else:
            print("🟢 No scaling events detected")
    
    def run_complete_demo(self):
        """Ejecuta demo completo de auto-scaling"""
        print("🚀 AUTO-SCALING COMPLETE DEMO")
        print("=" * 50)
        
        # Verificar API
        if not self.check_api_status():
            print("❌ Cannot proceed without API")
            return False
        
        # Estado inicial
        print(f"\n📊 INITIAL STATE")
        print("-" * 30)
        initial_data = self.get_system_metrics()
        if not initial_data:
            return False
        
        initial_workers = initial_data['metrics']['active_workers']
        
        # Esperar confirmación del usuario
        input("\n⏸️  Press Enter to start stress test...")
        
        # Stress test
        print(f"\n🔥 STEP 1: STRESS TEST")
        print("-" * 30)
        if not self.trigger_stress_test(25):
            return False
        
        # Monitorear scale up
        print(f"\n📈 STEP 2: MONITORING SCALE UP")
        print("-" * 30)
        self.monitor_system(duration=90, interval=3)
        
        # Esperar estabilización
        input("\n⏸️  Press Enter to wait for scale down...")
        
        # Monitorear scale down
        print(f"\n📉 STEP 3: MONITORING SCALE DOWN")
        print("-" * 30)
        self.monitor_system(duration=120, interval=5)
        
        # Estado final
        print(f"\n📊 FINAL STATE")
        print("-" * 30)
        final_data = self.get_system_metrics()
        if final_data:
            final_workers = final_data['metrics']['active_workers']
            print(f"\n🎯 DEMO RESULTS:")
            print(f"   Initial workers: {initial_workers}")
            print(f"   Final workers:   {final_workers}")
        
        print(f"\n🎉 AUTO-SCALING DEMO COMPLETED!")
        return True
    
    def interactive_mode(self):
        """Modo interactivo"""
        print("🎮 AUTO-SCALING INTERACTIVE MODE")
        print("=" * 40)
        
        while True:
            print(f"\nAvailable commands:")
            print("  1. Check API status")
            print("  2. Get system metrics")  
            print("  3. Trigger stress test")
            print("  4. Manual scale workers")
            print("  5. Monitor system")
            print("  6. Run complete demo")
            print("  q. Quit")
            
            choice = input("\nEnter choice: ").strip().lower()
            
            if choice == 'q':
                print("👋 Goodbye!")
                break
            elif choice == '1':
                self.check_api_status()
            elif choice == '2':
                self.get_system_metrics()
            elif choice == '3':
                num_tasks = input("Number of tasks (default 20): ").strip()
                num_tasks = int(num_tasks) if num_tasks.isdigit() else 20
                self.trigger_stress_test(num_tasks)
            elif choice == '4':
                target = input("Target number of workers: ").strip()
                if target.isdigit():
                    self.manual_scale(int(target))
                else:
                    print("❌ Invalid number")
            elif choice == '5':
                duration = input("Monitor duration in seconds (default 60): ").strip()
                duration = int(duration) if duration.isdigit() else 60
                self.monitor_system(duration)
            elif choice == '6':
                self.run_complete_demo()
            else:
                print("❌ Invalid choice")
    
    def _display_metrics(self, metrics, decision):
        """Muestra métricas formateadas"""
        print("📊 SYSTEM METRICS")
        print("-" * 30)
        print(f"Queue Length:      {metrics['queue_length']:>3d} tasks")
        print(f"Active Workers:    {metrics['active_workers']:>3d}")
        print(f"Busy Workers:      {metrics['busy_workers']:>3d}")
        print(f"Worker Utilization: {metrics['worker_utilization']:>6.1%}")
        print(f"Success Rate:      {metrics['success_rate']:>6.1%}")
        print(f"CPU Usage:         {metrics['cpu_usage']:>6.1f}%")
        print(f"Memory Usage:      {metrics['memory_usage']:>6.1f}%")
        
        print(f"\n🎯 SCALING DECISION")
        print("-" * 30)
        action_icons = {
            'scale_up': '🔺 SCALE UP',
            'scale_down': '🔻 SCALE DOWN', 
            'no_action': '🟢 MAINTAIN'
        }
        action_display = action_icons.get(decision['action'], decision['action'])
        print(f"Action: {action_display}")
        print(f"Target: {decision['target_workers']} workers")
        print(f"Reason: {decision['reason']}")
    
    def _display_monitoring_line(self, metrics, decision):
        """Muestra línea de monitoreo"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        queue = metrics['queue_length']
        workers = metrics['active_workers']
        utilization = metrics['worker_utilization']
        
        action_icons = {
            'scale_up': '🔺',
            'scale_down': '🔻',
            'no_action': '🟢'
        }
        icon = action_icons.get(decision['action'], '❓')
        
        print(f"[{timestamp}] {icon} Queue:{queue:2d} | Workers:{workers:2d} | Util:{utilization:5.1%}")

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Auto-Scaling CLI Tool')
    parser.add_argument('--api-url', default='http://localhost:8000', 
                       help='API URL (default: http://localhost:8000)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Subcomandos
    subparsers.add_parser('check', help='Check API status')
    subparsers.add_parser('metrics', help='Get system metrics')
    
    stress_parser = subparsers.add_parser('stress', help='Trigger stress test')
    stress_parser.add_argument('--tasks', type=int, default=20, help='Number of tasks')
    
    scale_parser = subparsers.add_parser('scale', help='Manual scaling')
    scale_parser.add_argument('workers', type=int, help='Target number of workers')
    
    monitor_parser = subparsers.add_parser('monitor', help='Monitor system')
    monitor_parser.add_argument('--duration', type=int, default=60, help='Duration in seconds')
    monitor_parser.add_argument('--interval', type=int, default=3, help='Check interval in seconds')
    
    subparsers.add_parser('demo', help='Run complete demo')
    subparsers.add_parser('interactive', help='Interactive mode')
    
    args = parser.parse_args()
    
    # Crear CLI instance
    cli = AutoScalingCLI(args.api_url)
    
    # Ejecutar comando
    if args.command == 'check':
        cli.check_api_status()
    elif args.command == 'metrics':
        cli.get_system_metrics()
    elif args.command == 'stress':
        cli.trigger_stress_test(args.tasks)
    elif args.command == 'scale':
        cli.manual_scale(args.workers)
    elif args.command == 'monitor':
        cli.monitor_system(args.duration, args.interval)
    elif args.command == 'demo':
        cli.run_complete_demo()
    elif args.command == 'interactive':
        cli.interactive_mode()
    else:
        # Modo interactivo por defecto
        cli.interactive_mode()

if __name__ == "__main__":
    main()