"""
🎨 Image Filters - DÍA 1: Filtros básicos con threading

Implementación de filtros de imagen que evoluciona durante la semana.
"""

import time
import threading
from typing import Tuple, Any
from pathlib import Path

# TODO DÍA 1: Descomentarr cuando instalen PIL
# from PIL import Image, ImageFilter, ImageEnhance
# import numpy as np

class ImageFilters:
    """
    🎨 Colección de filtros para procesamiento de imágenes
    
    DÍA 1: Filtros básicos con PIL
    DÍA 2: Filtros pesados con OpenCV
    DÍA 3: Filtros distribuidos
    """
    
    @staticmethod
    def resize_filter(image_data: Any, size: Tuple[int, int] = (800, 600)) -> Any:
        """
        📏 Redimensionar imagen
        
        TODO DÍA 1: Implementar con PIL
        Args:
            image_data: PIL Image object
            size: Nueva dimensión (ancho, alto)
        Returns:
            Imagen redimensionada
        """
        print(f"🧵 Thread {threading.get_ident()}: Aplicando resize filter")
        time.sleep(0.2)  # Simular procesamiento
        
        # TODO: Implementar resize real
        # return image_data.resize(size, Image.Resampling.LANCZOS)
        
        return image_data  # Placeholder
    
    @staticmethod
    def blur_filter(image_data: Any, radius: float = 2.0) -> Any:
        """
        🌫️ Aplicar efecto blur
        
        TODO DÍA 1: Implementar con PIL
        Args:
            image_data: PIL Image object  
            radius: Intensidad del blur
        Returns:
            Imagen con blur
        """
        print(f"🧵 Thread {threading.get_ident()}: Aplicando blur filter")
        time.sleep(0.3)  # Simular procesamiento
        
        # TODO: Implementar blur real
        # return image_data.filter(ImageFilter.GaussianBlur(radius=radius))
        
        return image_data  # Placeholder
    
    @staticmethod
    def brightness_filter(image_data: Any, factor: float = 1.2) -> Any:
        """
        ☀️ Ajustar brillo
        
        TODO DÍA 1: Implementar con PIL
        Args:
            image_data: PIL Image object
            factor: Factor de brillo (1.0 = sin cambio)
        Returns:
            Imagen con brillo ajustado
        """
        print(f"🧵 Thread {threading.get_ident()}: Aplicando brightness filter")
        time.sleep(0.1)  # Simular procesamiento
        
        # TODO: Implementar brightness real
        # enhancer = ImageEnhance.Brightness(image_data)
        # return enhancer.enhance(factor)
        
        return image_data  # Placeholder

    # =====================================================================
    # 🔥 DÍA 2: FILTROS PESADOS PARA MULTIPROCESSING  
    # =====================================================================
    
    @staticmethod
    def heavy_sharpen_filter(image_data: Any) -> Any:
        """
        ⚡ Filtro pesado para DÍA 2 - requiere multiprocessing
        
        TODO DÍA 2: Implementar con OpenCV
        """
        print(f"🔄 Process {threading.get_ident()}: Heavy sharpen filter")
        time.sleep(2.0)  # Simular procesamiento pesado
        return image_data
    
    @staticmethod
    def edge_detection_filter(image_data: Any) -> Any:
        """
        🔍 Detección de bordes - CPU intensivo
        
        TODO DÍA 2: Implementar con OpenCV
        """
        print(f"🔄 Process {threading.get_ident()}: Edge detection filter")
        time.sleep(1.5)  # Simular procesamiento pesado
        return image_data

# =====================================================================
# 🎯 FACTORY PATTERN PARA FILTROS
# =====================================================================

class FilterFactory:
    """🏭 Factory para crear filtros según tipo"""
    
    AVAILABLE_FILTERS = {
        # DÍA 1: Filtros básicos (threading)
        'resize': ImageFilters.resize_filter,
        'blur': ImageFilters.blur_filter,
        'brightness': ImageFilters.brightness_filter,
        
        # DÍA 2: Filtros pesados (multiprocessing)
        'sharpen': ImageFilters.heavy_sharpen_filter,
        'edges': ImageFilters.edge_detection_filter,
    }
    
    @classmethod
    def get_filter(cls, filter_name: str):
        """Obtener función de filtro por nombre"""
        if filter_name not in cls.AVAILABLE_FILTERS:
            raise ValueError(f"Filter '{filter_name}' not available. "
                           f"Available: {list(cls.AVAILABLE_FILTERS.keys())}")
        
        return cls.AVAILABLE_FILTERS[filter_name]
    
    @classmethod
    def apply_filter_chain(cls, image_data: Any, filter_names: list) -> Any:
        """
        🔗 Aplicar cadena de filtros secuencialmente
        
        TODO DÍA 1: Los estudiantes implementan esto
        """
        result = image_data
        
        for filter_name in filter_names:
            filter_func = cls.get_filter(filter_name)
            result = filter_func(result)
            print(f"✅ Applied {filter_name}")
        
        return result

# =====================================================================
# 📋 EJEMPLO DE USO PARA ESTUDIANTES
# =====================================================================

def demo_filters():
    """🎭 Demo de filtros para testing"""
    print("🎨 DEMO: Image Filters")
    
    # Simular imagen
    fake_image = "test_image_data"
    
    # Test filtros individuales
    print("\n1. Filtros individuales:")
    result1 = ImageFilters.resize_filter(fake_image)
    result2 = ImageFilters.blur_filter(fake_image)
    result3 = ImageFilters.brightness_filter(fake_image)
    
    # Test cadena de filtros
    print("\n2. Cadena de filtros:")
    filter_chain = ['resize', 'blur', 'brightness']
    result_chain = FilterFactory.apply_filter_chain(fake_image, filter_chain)
    
    print("✅ Demo completado")

if __name__ == "__main__":
    demo_filters() 