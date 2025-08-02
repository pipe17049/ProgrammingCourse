#!/usr/bin/env python3
"""
Simple Monitoring CLI - Clean interface for metrics and recommendations
"""
import time
import argparse
import requests
from datetime import datetime


class SimpleMonitoringCLI:
    """
    Clean CLI for monitoring system
    - Show metrics
    - Show recommendations (educational)
    - No confusing scaling commands that fail
    """
    
    def __init__(self, api_url='http://localhost:8000'):
        self.api_url = api_url.rstrip('/')
    
    def check_api(self):
        """Check if API is available"""
        try:
            response = requests.get(f'{self.api_url}/api/health/', timeout=5)
            if response.status_code == 200:
                print("✅ API is healthy and running")
                return True
            else:
                print(f"⚠️ API returned status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ API not available: {e}")
            return False
    
    def show_metrics(self):
        """Display current system metrics"""
        try:
            response = requests.get(f'{self.api_url}/api/metrics/', timeout=10)
            if response.status_code != 200:
                print(f"❌ Failed to get metrics: {response.status_code}")
                return
            
            data = response.json()
            if data['status'] != 'success':
                print(f"❌ API error: {data.get('message', 'Unknown error')}")
                return
            
            metrics = data['metrics']
            recommendation = data['scaling_recommendation']
            
            self._display_metrics(metrics, recommendation)
            
        except Exception as e:
            print(f"❌ Error getting metrics: {e}")
    
    def monitor_live(self, duration=60):
        """Monitor system live for specified duration"""
        print(f"🔄 Live monitoring for {duration} seconds...")
        print("💡 Press Ctrl+C to stop early")
        print("=" * 50)
        
        start_time = time.time()
        
        try:
            while time.time() - start_time < duration:
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"\n⏰ {timestamp}")
                print("-" * 20)
                
                self.show_metrics()
                
                print(f"\n🔄 Next update in 5 seconds...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\n👋 Live monitoring stopped")
    
    def run_stress(self, count=10, filters=None):
        """Generate stress load using existing API endpoint"""
        if filters is None:
            filters = ['resize', 'blur', 'brightness']
        
        payload = {
            'count': count,
            'filters': filters
        }
        
        print(f"🔥 Running stress test: {count} images with {filters}")
        
        try:
            response = requests.post(
                f'{self.api_url}/api/process-batch/stress/',
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                self._display_stress_results(data)
                return True
            else:
                print(f"❌ Stress test failed: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error running stress test: {e}")
            return False
    
    def _display_stress_results(self, data):
        """Display stress test results"""
        results = data.get('stress_test_results', {})
        system = data.get('system_info', {})
        
        print("\n📊 STRESS TEST RESULTS")
        print("=" * 40)
        print(f"⏱️  Total Time:      {results.get('total_time', 0):.2f}s")
        print(f"🖼️  Images:          {results.get('images_processed', 0)}")
        print(f"✅ Success:         {results.get('success_count', 0)}")
        print(f"❌ Errors:          {results.get('error_count', 0)}")
        print(f"📈 Success Rate:    {results.get('success_rate', '0%')}")
        print(f"🚀 Throughput:      {results.get('throughput', '0')}")
        print(f"⚙️  Method:          {system.get('method', 'Unknown')}")
        print(f"🔥 Stress Level:    {system.get('stress_level', 'Unknown')}")
    
    def _display_metrics(self, metrics, recommendation):
        """Display metrics in a clean format"""
        print("\n📊 SYSTEM METRICS")
        print("=" * 40)
        
        # System metrics
        print(f"🔥 CPU Usage:        {metrics.get('cpu_usage', 0):>6.1f}%")
        print(f"🧠 Memory Usage:     {metrics.get('memory_usage', 0):>6.1f}%")
        print(f"💽 Memory Available: {metrics.get('memory_available_gb', 0):>6.1f} GB")
        
        print(f"\n⚙️ WORKER METRICS")
        print("-" * 20)
        print(f"👥 Active Workers:   {metrics.get('active_workers', 0):>6d}")
        print(f"⚡ Busy Workers:     {metrics.get('busy_workers', 0):>6d}")
        print(f"📈 Utilization:      {metrics.get('worker_utilization', 0):>6.1%}")
        print(f"📋 Queue Length:     {metrics.get('queue_length', 0):>6d}")
        print(f"✅ Success Rate:     {metrics.get('success_rate', 0):>6.1f}%")
        
        print(f"\n🎓 SCALING RECOMMENDATION (Educational)")
        print("-" * 40)
        print(f"📊 Current Workers:  {recommendation.get('current_workers', 0):>6d}")
        print(f"🎯 Recommended:      {recommendation.get('recommended_workers', 0):>6d}")
        print(f"🎬 Action:           {recommendation.get('action', 'unknown').upper()}")
        print(f"📝 Reason:           {recommendation.get('reason', 'No reason')}")
        print(f"🎯 Confidence:       {recommendation.get('confidence', 0):>6.1%}")
        print(f"⚡ Urgency:          {recommendation.get('urgency', 'unknown').upper()}")
        
        print(f"\n💡 NOTE: {recommendation.get('note', 'Recommendations are educational only')}")


def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description='Simple Monitoring CLI')
    parser.add_argument('--api-url', default='http://localhost:8000',
                       help='API URL (default: http://localhost:8000)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Check command
    subparsers.add_parser('check', help='Check API status')
    
    # Metrics command
    subparsers.add_parser('metrics', help='Show current metrics')
    
    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Live monitoring')
    monitor_parser.add_argument('--duration', type=int, default=60,
                               help='Duration in seconds (default: 60)')
    
    # Stress command
    stress_parser = subparsers.add_parser('stress', help='Generate stress load')
    stress_parser.add_argument('--count', type=int, default=10,
                              help='Number of images (default: 10)')
    stress_parser.add_argument('--filters', nargs='+', 
                              default=['resize', 'blur', 'brightness'],
                              help='Filters to apply')
    
    args = parser.parse_args()
    
    # Create CLI instance
    cli = SimpleMonitoringCLI(args.api_url)
    
    # Execute command
    if args.command == 'check':
        cli.check_api()
    elif args.command == 'metrics':
        cli.show_metrics()
    elif args.command == 'monitor':
        cli.monitor_live(args.duration)
    elif args.command == 'stress':
        cli.run_stress(args.count, args.filters)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()