#!/usr/bin/env python3
"""
Simple Stress Tool - Uses existing API endpoint
Wrapper around /api/process-batch/stress/ for easy load generation
"""
import time
import requests
import argparse


class SimpleStressTool:
    """Simple wrapper around the existing stress endpoint"""
    
    def __init__(self, api_url='http://localhost:8000'):
        self.api_url = api_url.rstrip('/')
        self.endpoint = f'{self.api_url}/api/process-batch/stress/'
    
    def check_api(self):
        """Check if API is available"""
        try:
            response = requests.get(f'{self.api_url}/api/health/', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def run_stress(self, count=10, filters=None):
        """Run a single stress test"""
        if filters is None:
            filters = ['resize', 'blur', 'brightness']
        
        payload = {
            'count': count,
            'filters': filters
        }
        
        print(f"🔥 Running stress test: {count} images with {filters}")
        
        try:
            response = requests.post(self.endpoint, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self._display_results(data)
                return True
            else:
                print(f"❌ Stress test failed: HTTP {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def burst_stress(self, waves=3, count_per_wave=5, delay=2):
        """Run multiple stress waves"""
        print(f"🌊 Burst stress: {waves} waves of {count_per_wave} images each")
        print("=" * 50)
        
        for wave in range(waves):
            print(f"\n🌊 WAVE {wave + 1}/{waves}")
            success = self.run_stress(count_per_wave)
            
            if not success:
                print(f"❌ Wave {wave + 1} failed!")
                break
            
            if wave < waves - 1:  # Don't wait after last wave
                print(f"⏸️  Waiting {delay}s before next wave...")
                time.sleep(delay)
        
        print(f"\n🎉 Burst stress completed!")
    
    def _display_results(self, data):
        """Display stress test results"""
        results = data.get('stress_test_results', {})
        system = data.get('system_info', {})
        
        print("\n📊 STRESS TEST RESULTS")
        print("-" * 30)
        print(f"⏱️  Total Time:      {results.get('total_time', 0):.2f}s")
        print(f"🖼️  Images:          {results.get('images_processed', 0)}")
        print(f"✅ Success:         {results.get('success_count', 0)}")
        print(f"❌ Errors:          {results.get('error_count', 0)}")
        print(f"📈 Success Rate:    {results.get('success_rate', '0%')}")
        print(f"🚀 Throughput:      {results.get('throughput', '0')}")
        print(f"⚙️  Method:          {system.get('method', 'Unknown')}")
        print(f"👥 Workers:         {system.get('workers', 0)}")
        print(f"🔥 Stress Level:    {system.get('stress_level', 'Unknown')}")


def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(description='Simple Stress Tool')
    parser.add_argument('--api-url', default='http://localhost:8000',
                       help='API URL (default: http://localhost:8000)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Single stress test
    single_parser = subparsers.add_parser('run', help='Run single stress test')
    single_parser.add_argument('--count', type=int, default=10,
                              help='Number of images (default: 10)')
    single_parser.add_argument('--filters', nargs='+', 
                              default=['resize', 'blur', 'brightness'],
                              help='Filters to apply')
    
    # Burst stress test
    burst_parser = subparsers.add_parser('burst', help='Run burst stress test')
    burst_parser.add_argument('--waves', type=int, default=3,
                             help='Number of waves (default: 3)')
    burst_parser.add_argument('--count', type=int, default=5,
                             help='Images per wave (default: 5)')
    burst_parser.add_argument('--delay', type=int, default=2,
                             help='Delay between waves in seconds (default: 2)')
    
    # Check command
    subparsers.add_parser('check', help='Check API status')
    
    args = parser.parse_args()
    
    # Create stress tool
    stress_tool = SimpleStressTool(args.api_url)
    
    # Execute command
    if args.command == 'check':
        if stress_tool.check_api():
            print("✅ API is available")
        else:
            print("❌ API is not available")
    
    elif args.command == 'run':
        if not stress_tool.check_api():
            print("❌ API not available!")
            return
        stress_tool.run_stress(args.count, args.filters)
    
    elif args.command == 'burst':
        if not stress_tool.check_api():
            print("❌ API not available!")
            return
        stress_tool.burst_stress(args.waves, args.count, args.delay)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()