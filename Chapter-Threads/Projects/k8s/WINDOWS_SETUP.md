# 🪟 KUBERNETES EN WINDOWS - SETUP RÁPIDO

## 🎯 **OPCIONES PARA WINDOWS:**

### **⭐ OPCIÓN 1: Docker Desktop (RECOMENDADO)**
```powershell
# 1. Instalar Docker Desktop for Windows
# Download: https://www.docker.com/products/docker-desktop

# 2. Habilitar Kubernetes
# Docker Desktop → Settings → Kubernetes → Enable Kubernetes → Apply & Restart

# 3. Verificar
kubectl version --client
kubectl cluster-info
```

### **⭐ OPCIÓN 2: Minikube**
```powershell
# 1. Instalar minikube
# Download: https://minikube.sigs.k8s.io/docs/start/

# 2. Iniciar cluster
minikube start

# 3. Verificar
kubectl cluster-info
```

### **⭐ OPCIÓN 3: Browser (Sin instalación)**
```
# Si nada funciona:
# 1. Ir a: https://labs.play-with-k8s.com/
# 2. Login con Docker Hub account
# 3. Create instance
# 4. Usar terminal web
```

---

## 🚀 **DEMO RÁPIDO - WINDOWS:**

### **Paso 1: Setup**
```powershell
# Cambiar a directorio k8s
cd k8s

# Verificar conexión
kubectl cluster-info
```

### **Paso 2: Deploy**
```powershell
# Deploy todo de una vez
kubectl apply -f .

# Ver status
kubectl get pods
kubectl get hpa
```

### **Paso 3: Port Forward**
```powershell
# En terminal 1:
kubectl port-forward service/api-service 8000:8000
```

### **Paso 4: Stress Test**
```powershell
# En terminal 2:
cd ..
python burst_stress.py 50
```

### **Paso 5: Watch Auto-scaling**
```powershell
# En terminal 3:
kubectl get hpa -w

# En terminal 4:
kubectl get pods -w
```

**¡Verás auto-scaling real: 2→4→6→8 pods!** 🚀

### **Paso 6: Cleanup**
```powershell
cd k8s
kubectl delete -f .
```

---

## 🛠️ **TROUBLESHOOTING WINDOWS:**

### **Error: kubectl no encontrado**
```powershell
# Agregar kubectl a PATH:
# 1. Descargar kubectl.exe
# 2. Poner en C:\Windows\System32\
# O usar chocolatey:
choco install kubernetes-cli
```

### **Error: No cluster connection**
```powershell
# Docker Desktop:
# Settings → Kubernetes → Reset Kubernetes Cluster

# Minikube:
minikube delete
minikube start
```

### **Error: Port 8000 ocupado**
```powershell
# Ver qué usa el puerto:
netstat -ano | findstr :8000

# Usar otro puerto:
kubectl port-forward service/api-service 8001:8000
```

### **Error: Python no encontrado**
```powershell
# Instalar Python:
# https://www.python.org/downloads/

# O usar Microsoft Store:
# Search "Python" → Install

# Verificar:
python --version
```

---

## 📋 **CHECKLIST PRE-CLASE:**

### **Para Instructor:**
- ✅ Docker Desktop instalado y K8s habilitado
- ✅ `kubectl version` funciona 
- ✅ `python --version` funciona
- ✅ Archivos YAML en directorio `k8s/`
- ✅ `burst_stress.py` en directorio padre
- ✅ **Backup:** Video de auto-scaling por si algo falla

### **Para Estudiantes:**
- ✅ Al menos Docker Desktop OR minikube instalado
- ✅ Python instalado
- ✅ Account en play-with-k8s.com (backup)
- ✅ 3-4 terminales disponibles

---

## 🎬 **DEMO ALTERNATIVO SI FALLA:**

### **Manual Scaling (Funciona siempre):**
```powershell
# Mostrar estado inicial
kubectl get pods

# Escalar manualmente 
kubectl scale deployment worker-deployment --replicas=8

# Ver cambio
kubectl get pods

# Simular auto-scaling visual
kubectl scale deployment worker-deployment --replicas=2
kubectl scale deployment worker-deployment --replicas=6
kubectl scale deployment worker-deployment --replicas=10
```

### **Python Demo Script:**
```powershell
# Si todo falla, usar script guiado:
python demo.py
```

---

## 🏆 **RESULTADO ESPERADO:**

**Al final de la clase, en Windows:**
- ✅ Kubernetes funciona local
- ✅ Auto-scaling real funcionando
- ✅ Estudiantes ven 2→8 pods automático
- ✅ Entienden diferencia Docker vs K8s

**"¡Por fin auto-scaling REAL en Windows!"** 🚀✨