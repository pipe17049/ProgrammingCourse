# 🚀 QUICK TEST - WINDOWS

## **⚡ PRUEBA RÁPIDA (5 min):**

### **1. Setup rápido**
```powershell
# En Windows PowerShell:
cd k8s

# Verificar que tienes lo necesario:
kubectl version --client
python --version
```

### **2. Opción A: Demo automático**
```powershell
python demo.py
# Sigue las instrucciones paso a paso
```

### **3. Opción B: Manual**
```powershell
# Deploy todo:
kubectl apply -f .

# Ver status:
kubectl get pods
kubectl get hpa

# Port forward (terminal 1):
kubectl port-forward service/api-service 8000:8000

# Stress test (terminal 2):
cd ..
python burst_stress.py 50

# Ver auto-scaling (terminal 3):
kubectl get hpa -w
kubectl get pods -w
```

## **🎯 QUE ESPERAR:**

### **Antes del stress:**
```
NAME            READY   STATUS    
worker-xxx-1    1/1     Running   
worker-xxx-2    1/1     Running   

NAME         REFERENCE               TARGETS   MINPODS   MAXPODS   REPLICAS
worker-hpa   Deployment/worker       0%/70%    1         10        2
```

### **Durante el stress:**
```
# CPU sube:
worker-hpa   Deployment/worker       85%/70%   1         10        2

# Pods aumentan automáticamente:
worker-xxx-1    1/1     Running   
worker-xxx-2    1/1     Running   
worker-xxx-3    1/1     Running   ← NUEVO!
worker-xxx-4    1/1     Running   ← NUEVO!
worker-xxx-5    1/1     Running   ← NUEVO!
```

## **✅ ÉXITO SI VES:**
- ✅ Pods: 2 → 4 → 6 → 8 (automático)
- ✅ CPU: 0% → 70%+ → vuelta a 0%
- ✅ HPA: "scaled up/down" eventos
- ✅ Sin errores en `kubectl get events`

## **🔧 Si algo falla:**

### **Error: No cluster**
```powershell
# Docker Desktop:
# Settings → Kubernetes → Enable Kubernetes

# O minikube:
minikube start
```

### **Error: Image not found**
```powershell
# Usar imágenes genéricas:
kubectl set image deployment/api-deployment api=nginx
kubectl set image deployment/worker-deployment worker=busybox
```

### **Error: Port ocupado**
```powershell
kubectl port-forward service/api-service 8001:8000
# Cambia 8000 por 8001 en burst_stress.py
```

## **🧹 Cleanup:**
```powershell
kubectl delete -f .
```

---

## **🏆 OBJETIVO DE LA PRUEBA:**

> **Confirmar que auto-scaling K8s funciona en Windows antes de la clase**

**Si funciona:** ✅ Clase lista  
**Si no funciona:** ❌ Backup plan necesario