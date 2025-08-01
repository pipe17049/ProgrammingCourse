from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ScalingDecision:
    """Decisión de escalamiento"""
    action: str  # 'scale_up', 'scale_down', 'no_action'
    target_workers: int
    reason: str
    confidence: float  # 0.0 - 1.0

class ScalingRules:
    """Reglas para auto-scaling de workers"""
    
    def __init__(self):
        # Configuración de scaling
        self.min_workers = 1
        self.max_workers = 10
        
        # Thresholds para scale up (🎯 DEMO: Más sensible)
        self.scale_up_queue_threshold = 3  # Era 8, ahora 3
        self.scale_up_utilization_threshold = 0.5  # Era 0.8, ahora 0.5
        self.scale_up_cpu_threshold = 50.0  # Era 75.0, ahora 50.0
        
        # Thresholds para scale down  
        self.scale_down_queue_threshold = 1  # Era 2, ahora 1
        self.scale_down_utilization_threshold = 0.2  # Era 0.3, ahora 0.2
        self.scale_down_idle_time = 300  # 5 minutos
        
        # Cooldown periods (evitar scaling excesivo)
        self.scale_up_cooldown = 60    # 1 minuto
        self.scale_down_cooldown = 180  # 3 minutos
        
        self.last_scale_action = None
        self.last_scale_time = 0
    
    def evaluate_scaling(self, metrics: Dict[str, Any]) -> ScalingDecision:
        """Evalúa si necesita scaling basado en métricas"""
        current_workers = metrics.get('active_workers', 1)
        
        # Verificar si estamos en cooldown
        import time
        current_time = time.time()
        
        if self.last_scale_action and self.last_scale_time:
            time_since_last = current_time - self.last_scale_time
            required_cooldown = (self.scale_up_cooldown if self.last_scale_action == 'scale_up' 
                               else self.scale_down_cooldown)
            
            if time_since_last < required_cooldown:
                return ScalingDecision(
                    action='no_action',
                    target_workers=current_workers,
                    reason=f'Cooldown period ({int(required_cooldown - time_since_last)}s remaining)',
                    confidence=1.0
                )
        
        # Evaluar scale up
        scale_up_decision = self._evaluate_scale_up(metrics)
        if scale_up_decision.action == 'scale_up':
            self._record_scaling_action('scale_up', current_time)
            return scale_up_decision
        
        # Evaluar scale down
        scale_down_decision = self._evaluate_scale_down(metrics)
        if scale_down_decision.action == 'scale_down':
            self._record_scaling_action('scale_down', current_time)
            return scale_down_decision
        
        return ScalingDecision(
            action='no_action',
            target_workers=current_workers,
            reason='System is within optimal parameters',
            confidence=0.8
        )
    
    def _evaluate_scale_up(self, metrics: Dict[str, Any]) -> ScalingDecision:
        """Evalúa necesidad de scale up"""
        current_workers = metrics.get('active_workers', 1)
        queue_length = metrics.get('queue_length', 0)
        utilization = metrics.get('worker_utilization', 0)
        cpu_usage = metrics.get('cpu_usage', 0)
        
        reasons = []
        confidence_factors = []
        
        # Verificar cola muy larga
        if queue_length > self.scale_up_queue_threshold:
            reasons.append(f'High queue length ({queue_length} tasks)')
            confidence_factors.append(min(queue_length / self.scale_up_queue_threshold, 2.0))
        
        # Verificar alta utilización de workers
        if utilization > self.scale_up_utilization_threshold:
            reasons.append(f'High worker utilization ({utilization:.1%})')
            confidence_factors.append(utilization / self.scale_up_utilization_threshold)
        
        # Verificar alto uso de CPU
        if cpu_usage > self.scale_up_cpu_threshold:
            reasons.append(f'High CPU usage ({cpu_usage:.1f}%)')
            confidence_factors.append(cpu_usage / self.scale_up_cpu_threshold)
        
        # Si hay razones para scale up
        if reasons and current_workers < self.max_workers:
            # Calcular número target de workers
            target_workers = min(
                current_workers + max(1, queue_length // 5),  # +1 worker por cada 5 tasks
                self.max_workers
            )
            
            confidence = min(sum(confidence_factors) / len(confidence_factors), 1.0)
            
            return ScalingDecision(
                action='scale_up',
                target_workers=target_workers,
                reason='; '.join(reasons),
                confidence=confidence
            )
        
        return ScalingDecision(
            action='no_action',
            target_workers=current_workers,
            reason='No scale up conditions met',
            confidence=0.5
        )
    
    def _evaluate_scale_down(self, metrics: Dict[str, Any]) -> ScalingDecision:
        """Evalúa necesidad de scale down"""
        current_workers = metrics.get('active_workers', 1)
        queue_length = metrics.get('queue_length', 0)
        utilization = metrics.get('worker_utilization', 0)
        
        reasons = []
        confidence_factors = []
        
        # Verificar cola muy pequeña Y baja utilización
        if (queue_length <= self.scale_down_queue_threshold and 
            utilization < self.scale_down_utilization_threshold and
            current_workers > self.min_workers):
            
            reasons.append(f'Low queue length ({queue_length}) and utilization ({utilization:.1%})')
            confidence_factors.append(
                (self.scale_down_utilization_threshold - utilization) / self.scale_down_utilization_threshold
            )
        
        # Si hay razones para scale down
        if reasons:
            # Calcular número target de workers (reducir gradualmente)
            target_workers = max(
                current_workers - 1,  # Reducir de a 1
                self.min_workers
            )
            
            confidence = min(sum(confidence_factors) / len(confidence_factors), 1.0)
            
            return ScalingDecision(
                action='scale_down',
                target_workers=target_workers,
                reason='; '.join(reasons),
                confidence=confidence
            )
        
        return ScalingDecision(
            action='no_action',
            target_workers=current_workers,
            reason='No scale down conditions met',
            confidence=0.5
        )
    
    def _record_scaling_action(self, action: str, timestamp: float):
        """Registra acción de scaling para cooldown"""
        self.last_scale_action = action
        self.last_scale_time = timestamp
    
    def get_scaling_config(self) -> Dict[str, Any]:
        """Obtiene configuración actual de scaling"""
        return {
            'min_workers': self.min_workers,
            'max_workers': self.max_workers,
            'scale_up_queue_threshold': self.scale_up_queue_threshold,
            'scale_up_utilization_threshold': self.scale_up_utilization_threshold,
            'scale_up_cpu_threshold': self.scale_up_cpu_threshold,
            'scale_down_queue_threshold': self.scale_down_queue_threshold,
            'scale_down_utilization_threshold': self.scale_down_utilization_threshold,
            'scale_up_cooldown': self.scale_up_cooldown,
            'scale_down_cooldown': self.scale_down_cooldown,
        }
    
    def update_config(self, **kwargs):
        """Actualiza configuración de scaling"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                print(f"📊 Updated {key} = {value}")