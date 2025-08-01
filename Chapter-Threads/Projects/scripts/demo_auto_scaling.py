#!/usr/bin/env python3
"""
Demo script para mostrar auto-scaling en acción
"""

import time
import requests
import threading
from datetime import datetime

class AutoScalingDemo:
    """Demo completo de auto-scaling"""
    
    def __init__(self, api_url='http://localhost:8000'):
        self.api_url = api_url
        
    def run_complete_demo(self):
        """Ejecuta demo completo de auto-scaling"""
        print("🚀 STARTING AUTO-SCALING DEMO")
        print("=" * 60)
        
        # Paso 1: Estado inicial
        self._show_initial_state()
        self._wait_for_input("Press Enter to start stress test...")
        
        # Paso 2: Stress test (trigger scale up)
        self._trigger_stress_test()
        self._wait_for_input("Press Enter to monitor scaling up...")
        
        # Paso 3: Monitorear scale up
        self._monitor_scaling(duration=60, expected_action='scale_up')
        
        # Paso 4: Esperar que se calme (trigger scale down)
        self._wait_for_input("Press Enter to wait for scale down...")
        self._monitor_scaling(duration=120, expected_action='scale_down')
        
        print("\n🎉 AUTO-SCALING DEMO COMPLETED!")
        
    def _show_initial_state(self):
        """Muestra estado inicial del sistema"""
        print("\n📊 INITIAL SYSTEM STATE")
        print("-" * 40)
        
        try:
            response = requests.get(f'{self.api_url}/api/system/metrics/')
            if response.status_code == 200:
                data = response.json()
                metrics = data['metrics']
                
                print(f"Queue Length: {metrics['queue_length']} tasks")
                print(f"Active Workers: {metrics['active_workers']}")
                print(f"Worker Utilization: {metrics['worker_utilization']:.1%}")
                print(f"CPU Usage: {metrics['cpu_usage']:.1f}%")
            else:
                print("❌ Could not fetch metrics")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def _trigger_stress_test(self):
        """Dispara stress test"""
        print("\n🔥 TRIGGERING STRESS TEST")
        print("-" * 40)
        
        try:
            response = requests.post(f'{self.api_url}/api/stress-test/', 
                                   data={'num_tasks': 25})
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Created {data['task_count']} stress tasks")
                print(f"Filters used: {', '.join(data['filters_used'])}")
            else:
                print(f"❌ Stress test failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def _monitor_scaling(self, duration=60, expected_action=None):
        """Monitorea el sistema durante scaling"""
        print(f"\n📈 MONITORING SCALING ({duration}s)")
        print("-" * 40)
        
        start_time = time.time()
        last_workers = 0
        scaling_detected = False
        
        while time.time() - start_time < duration:
            try:
                response = requests.get(f'{self.api_url}/api/system/metrics/')
                if response.status_code == 200:
                    data = response.json()
                    metrics = data['metrics']
                    decision = data['scaling_decision']
                    
                    # Detectar cambio en workers
                    current_workers = metrics['active_workers']
                    if current_workers != last_workers and last_workers > 0:
                        action = "🔺 SCALED UP" if current_workers > last_workers else "🔻 SCALED DOWN"
                        print(f"\n{action}: {last_workers} → {current_workers} workers")
                        scaling_detected = True
                    
                    # Mostrar estado actual
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    queue = metrics['queue_length']
                    workers = metrics['active_workers']
                    utilization = metrics['worker_utilization']
                    
                    action_icon = self._get_action_icon(decision['action'])
                    print(f"[{timestamp}] {action_icon} Queue:{queue:2d} | Workers:{workers:2d} | Util:{utilization:5.1%}")
                    
                    if decision['action'] == expected_action:
                        print(f"🎯 Expected scaling action detected: {decision['action']}")
                        print(f"   Reason: {decision['reason']}")
                        print(f"   Target: {decision['target_workers']} workers")
                        break
                    
                    last_workers = current_workers
                    
                else:
                    print(f"❌ Failed to get metrics: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
            
            time.sleep(3)
        
        if not scaling_detected and expected_action:
            print(f"⚠️ Expected {expected_action} not detected in {duration}s")
    
    def _get_action_icon(self, action):
        """Icono para acción de scaling"""
        icons = {
            'scale_up': '🔺',
            'scale_down': '🔻', 
            'no_action': '🟢'
        }
        return icons.get(action, '❓')
    
    def _wait_for_input(self, message):
        """Espera input del usuario"""
        print(f"\n⏸️  {message}")
        input()

def manual_stress_test():
    """Stress test manual simple"""
    print("🔥 Manual Stress Test")
    
    try:
        num_tasks = input("Number of tasks (default 20): ").strip()
        num_tasks = int(num_tasks) if num_tasks else 20
        
        response = requests.post('http://localhost:8000/api/stress-test/', 
                               data={'num_tasks': num_tasks})
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Created {data['task_count']} tasks")
        else:
            print(f"❌ Failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def check_system_status():
    """Verificar estado del sistema"""
    print("📊 System Status Check")
    
    try:
        response = requests.get('http://localhost:8000/api/system/metrics/')
        if response.status_code == 200:
            data = response.json()
            metrics = data['metrics']
            decision = data['scaling_decision']
            
            print(f"Queue Length: {metrics['queue_length']}")
            print(f"Active Workers: {metrics['active_workers']}")
            print(f"Busy Workers: {metrics['busy_workers']}")
            print(f"Worker Utilization: {metrics['worker_utilization']:.1%}")
            print(f"Success Rate: {metrics['success_rate']:.1%}")
            print(f"CPU Usage: {metrics['cpu_usage']:.1f}%")
            print(f"Scaling Action: {decision['action']}")
            if decision['action'] != 'no_action':
                print(f"Scaling Reason: {decision['reason']}")
                print(f"Target Workers: {decision['target_workers']}")
        else:
            print(f"❌ Failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'demo':
            demo = AutoScalingDemo()
            demo.run_complete_demo()
        elif command == 'stress':
            manual_stress_test()
        elif command == 'status':
            check_system_status()
        else:
            print("Usage: python demo_auto_scaling.py [demo|stress|status]")
    else:
        print("🚀 Auto-Scaling Demo Script")
        print("Usage:")
        print("  python demo_auto_scaling.py demo   - Full demo")
        print("  python demo_auto_scaling.py stress - Manual stress test")
        print("  python demo_auto_scaling.py status - Check system status")