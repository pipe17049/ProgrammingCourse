# 🚀 GitHub Actions Setup - Docker Hub Integration

Este documento explica cómo configurar la integración automática de GitHub Actions con Docker Hub para construir y subir las imágenes Docker del proyecto automáticamente.

## 📋 Pre-requisitos

1. **Cuenta en Docker Hub**: Necesitas una cuenta en [Docker Hub](https://hub.docker.com)
2. **Repositorio en GitHub**: El código debe estar en un repositorio de GitHub
3. **Namespace en Docker Hub**: Puedes usar tu username o crear una organización

## 🔧 Configuración de Docker Hub

### 1. Crear Access Token

1. Ve a [Docker Hub Settings → Security](https://hub.docker.com/settings/security)
2. Click en **"New Access Token"**
3. Nombre: `github-actions-token`
4. Permissions: **Read, Write, Delete**
5. Copia el token generado (no podrás verlo de nuevo)

### 2. Configurar Namespace

Edita el archivo `.github/workflows/docker-build.yml` y cambia:

```yaml
env:
  NAMESPACE: programming-course  # 👈 Cambia por tu username/organización
```

Por ejemplo:
```yaml
env:
  NAMESPACE: eduardoarias  # Tu username en Docker Hub
```

## 🔑 Configuración de Secrets en GitHub

### 1. Acceder a Repository Settings

1. Ve a tu repositorio en GitHub
2. Click en **Settings** (tab superior)
3. En el menú lateral, click en **Secrets and variables → Actions**

### 2. Agregar Secrets

Click en **"New repository secret"** y agrega:

**DOCKER_USERNAME**
- Name: `DOCKER_USERNAME`
- Secret: Tu username de Docker Hub

**DOCKER_PASSWORD**  
- Name: `DOCKER_PASSWORD`
- Secret: El access token que creaste en Docker Hub

## 🎯 Cómo Funciona

### Triggers Automáticos

El workflow se ejecuta automáticamente cuando:

- ✅ Haces `push` a `master` o `main`
- ✅ Creas un Pull Request
- ✅ Modificas archivos en `Chapter-Threads/Projects/`
- ✅ Ejecutas manualmente desde GitHub Actions

### Imágenes Generadas

Se crean dos imágenes:

```
docker.io/TU-NAMESPACE/threads-api:latest
docker.io/TU-NAMESPACE/threads-worker:latest
```

### Tags Automáticos

- `latest` - Para el branch principal
- `main-sha123456` - Para cada commit
- `pr-42` - Para Pull Requests

## 🚀 Ejecución Manual

### Desde GitHub UI

1. Ve a **Actions** en tu repositorio
2. Click en **"Build and Push Docker Images"**
3. Click en **"Run workflow"**
4. Selecciona el branch y click **"Run workflow"**

### Monitoring

Puedes ver el progreso en:
- **GitHub**: Tab "Actions" de tu repositorio  
- **Docker Hub**: Tus repositories mostrarán las nuevas imágenes

## 🛠️ Para Estudiantes - Uso de Imágenes

Una vez configurado, tus estudiantes pueden usar el proyecto sin construir imágenes localmente:

### Setup Simplificado

```bash
# 1. Clonar repositorio
git clone https://github.com/TU-USERNAME/ProgrammingCourse.git
cd ProgrammingCourse/Chapter-Threads/Projects

# 2. Ejecutar directamente (las imágenes se descargan automáticamente)
cd k8s
kubectl apply -f .

# 3. Demo automático
python demo.py
```

### No Necesitan

- ❌ `python build.py` (construcción local)
- ❌ Docker instalado localmente para build
- ❌ Esperar 5-10 minutos de construcción

### Solo Necesitan

- ✅ Kubernetes (Docker Desktop, minikube, etc.)
- ✅ `kubectl` configurado
- ✅ Python para ejecutar scripts

## 🔍 Troubleshooting

### Error: "denied: requested access to the resource is denied"

**Causa**: Secrets mal configurados o namespace incorrecto

**Solución**:
1. Verifica que `DOCKER_USERNAME` y `DOCKER_PASSWORD` estén bien configurados
2. Asegúrate que el namespace en el workflow coincida con tu username/org de Docker Hub

### Error: "Error response from daemon: pull access denied"

**Causa**: Las imágenes no existen en Docker Hub o son privadas

**Solución**:
1. Ejecuta el workflow al menos una vez para crear las imágenes
2. Verifica que las imágenes sean públicas en Docker Hub

### Error: "repository does not exist or may require 'docker login'"

**Causa**: El namespace no existe o no tienes permisos

**Solución**:
1. Crea el repositorio manualmente en Docker Hub, o
2. Asegúrate que tu access token tenga permisos de escritura

## 📊 Ejemplo de Ejecución Exitosa

```bash
🔄 Checkout repository          ✅
🐳 Set up Docker Buildx         ✅  
🔑 Log in to Docker Hub         ✅
📝 Extract metadata             ✅
🔨 Build and push Docker image  ✅

### 🎯 Built Images
| Image | Tags |
|-------|------|
| threads-api | programming-course/threads-api:latest, programming-course/threads-api:main-abc1234 |
| threads-worker | programming-course/threads-worker:latest, programming-course/threads-worker:main-abc1234 |
```

¡Con esta configuración, tus estudiantes tendrán una experiencia mucho más fluida! 🎓