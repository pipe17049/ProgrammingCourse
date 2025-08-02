"""
Simple Dashboard - Real-time Metrics + Scaling Recommendations
Clean, educational interface showing system status
"""
import time
import os
import argparse
from datetime import datetime
from simple_monitoring.metrics_collector import SimpleMetricsCollector
from simple_monitoring.recommendations import ScalingRecommendations


class SimpleDashboard:
    """
    Clean dashboard showing:
    - Real system metrics
    - Scaling recommendations (educational)
    - No confusing options or false promises
    """
    
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.metrics_collector = SimpleMetricsCollector(redis_host, redis_port)
        self.recommendations = ScalingRecommendations()
        self.refresh_interval = 3  # seconds
        
    def run(self, show_recommendations=True):
        """Run the dashboard"""
        print("🚀 SIMPLE MONITORING DASHBOARD")
        print("=" * 60)
        
        if show_recommendations:
            print("📊 Showing: Metrics + Scaling Recommendations (Educational)")
        else:
            print("📊 Showing: System Metrics Only")
        
        print("💡 Press Ctrl+C to exit")
        print("=" * 60)
        
        try:
            # Clear screen once
            self._clear_screen()
            
            while True:
                # Move cursor to top (avoid flicker)
                print("\033[H", end='')
                
                # Get fresh metrics
                metrics = self.metrics_collector.collect_metrics()
                
                # Display dashboard
                self._display_header()
                self._display_system_metrics(metrics)
                self._display_worker_metrics(metrics)
                
                if show_recommendations:
                    self._display_scaling_recommendations(metrics)
                
                self._display_footer()
                
                # Wait for next update
                time.sleep(self.refresh_interval)
                
        except KeyboardInterrupt:
            print("\n\n👋 Dashboard stopped")
    
    def _clear_screen(self):
        """Clear screen once (avoid flicker)"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _display_header(self):
        """Display dashboard header"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"📊 SYSTEM MONITORING DASHBOARD - {timestamp}")
        print("=" * 60)
    
    def _display_system_metrics(self, metrics):
        """Display system-level metrics"""
        print("\n🖥️  SYSTEM METRICS")
        print("-" * 30)
        
        cpu = metrics.get('cpu_usage', 0)
        memory = metrics.get('memory_usage', 0)
        memory_gb = metrics.get('memory_available_gb', 0)
        
        cpu_icon = self._get_load_icon(cpu, 50, 80)
        memory_icon = self._get_load_icon(memory, 60, 85)
        
        print(f"🔥 CPU Usage:      {cpu_icon} {cpu:>6.1f}%")
        print(f"🧠 Memory Usage:   {memory_icon} {memory:>6.1f}% ({memory_gb:.1f}GB free)")
    
    def _display_worker_metrics(self, metrics):
        """Display worker and queue metrics"""
        print("\n⚙️  WORKER METRICS")
        print("-" * 30)
        
        active = metrics.get('active_workers', 0)
        busy = metrics.get('busy_workers', 0)
        utilization = metrics.get('worker_utilization', 0)
        queue = metrics.get('queue_length', 0)
        success_rate = metrics.get('success_rate', 0)
        
        util_icon = self._get_load_icon(utilization * 100, 50, 80)
        queue_icon = "🟢" if queue == 0 else "🟡" if queue < 5 else "🔴"
        success_icon = "🟢" if success_rate >= 90 else "🟡" if success_rate >= 70 else "🔴"
        
        print(f"👥 Active Workers: {active:>3d}")
        print(f"⚡ Busy Workers:   {busy:>3d}")
        print(f"📈 Utilization:    {util_icon} {utilization:>6.1%}")
        print(f"📋 Queue Length:   {queue_icon} {queue:>3d} tasks")
        print(f"✅ Success Rate:   {success_icon} {success_rate:>6.1f}%")
    
    def _display_scaling_recommendations(self, metrics):
        """Display scaling recommendations (educational)"""
        print("\n🎓 SCALING RECOMMENDATIONS (Educational)")
        print("-" * 50)
        
        recommendation = self.recommendations.analyze_metrics(metrics)
        
        # Action icon
        action_icons = {
            'scale_up': '🔺',
            'scale_down': '🔻', 
            'maintain': '🟢'
        }
        action_icon = action_icons.get(recommendation.action, '❓')
        
        # Urgency color (using emojis since we can't use colors easily)
        urgency_indicators = {
            'high': '🚨',
            'medium': '⚠️',
            'low': '💡',
            'none': '✅'
        }
        urgency_icon = urgency_indicators.get(recommendation.urgency, '❓')
        
        print(f"📊 Current Workers:    {recommendation.current_workers}")
        print(f"🎯 Recommended:        {recommendation.recommended_workers}")
        print(f"🎬 Action:             {action_icon} {recommendation.action.upper()}")
        print(f"📝 Reason:             {recommendation.reason}")
        print(f"🎯 Confidence:         {recommendation.confidence:.1%}")
        print(f"⚡ Urgency:            {urgency_icon} {recommendation.urgency}")
        
        # Educational note
        print("\n💡 NOTE: These are educational recommendations only")
        print("   No automatic scaling is performed")
    
    def _display_footer(self):
        """Display dashboard footer"""
        print("\n" + "=" * 60)
        print("🔄 Updates every 3 seconds | Ctrl+C to exit")
        
    def _get_load_icon(self, value, medium_threshold, high_threshold):
        """Get load indicator icon"""
        if value < medium_threshold:
            return "🟢"
        elif value < high_threshold:
            return "🟡"
        else:
            return "🔴"


def main():
    """Command-line interface for the dashboard"""
    parser = argparse.ArgumentParser(description='Simple Monitoring Dashboard')
    parser.add_argument('--no-recommendations', action='store_true', 
                       help='Hide scaling recommendations')
    parser.add_argument('--redis-host', default='localhost',
                       help='Redis host (default: localhost)')
    parser.add_argument('--redis-port', type=int, default=6379,
                       help='Redis port (default: 6379)')
    
    args = parser.parse_args()
    
    # Create and run dashboard
    dashboard = SimpleDashboard(args.redis_host, args.redis_port)
    dashboard.run(show_recommendations=not args.no_recommendations)


if __name__ == '__main__':
    main()