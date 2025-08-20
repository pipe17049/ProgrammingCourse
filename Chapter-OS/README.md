# 🖥️ Chapter-OS: Sistemas Operativos y Línea de Comandos

Este capítulo cubre conceptos fundamentales de sistemas operativos, enfocándose en la creación y manejo de herramientas de línea de comandos.

## 📚 Contenido del Capítulo

### Session1-CommandLine: Creación de Línea de Comandos
- Fundamentos de la línea de comandos
- Creación de scripts bash básicos
- Automatización de tareas del sistema
- Navegación y manipulación de archivos

### Session2-ArgumentsConfig: Manejo de Argumentos y Configuración
- Procesamiento de argumentos de línea de comandos
- Archivos de configuración
- Variables de entorno
- Validación y manejo de errores

## 🎯 Objetivos de Aprendizaje

Al finalizar este capítulo, serás capaz de:
- ✅ Crear scripts de línea de comandos eficientes
- ✅ Manejar argumentos y opciones de manera profesional
- ✅ Implementar sistemas de configuración flexibles
- ✅ Automatizar tareas repetitivas del sistema

## 📖 Referencia Rápida de Comandos

### 🔍 Flags de Verificación de Archivos

| Flag | Descripción | Ejemplo | Uso Común |
|------|-------------|---------|-----------|
| `-e` | **Existe** (archivo o directorio) | `[ -e archivo ]` | Verificar existencia |
| `-f` | Es un **archivo** regular | `[ -f archivo.txt ]` | Verificar archivos |
| `-d` | Es un **directorio** | `[ -d carpeta ]` | Verificar directorios |
| `-r` | Tiene permisos de **lectura** | `[ -r archivo ]` | Verificar acceso |
| `-w` | Tiene permisos de **escritura** | `[ -w archivo ]` | Verificar modificación |
| `-x` | Tiene permisos de **ejecución** | `[ -x script.sh ]` | Verificar ejecutables |

### 💡 Reglas de Sintaxis Importantes

```bash
# ✅ CORRECTO - Espacios obligatorios alrededor de [ ]
[ -d directorio ]
[ -f archivo ]
[ "$var" = "valor" ]

# ❌ INCORRECTO - Sin espacios
[-d directorio]
[ -f archivo]
["$var"="valor"]
```

### 🛠️ Comandos y Opciones Esenciales

#### `echo` - Mostrar texto
```bash
echo "Texto simple"              # Texto básico
echo -e "\033[31mRojo\033[0m"    # Con colores (-e habilita escapes)
echo -n "Sin salto de línea"     # Sin \n al final
```

#### `read` - Leer entrada
```bash
read variable                    # Leer entrada básica
read -r line                     # Sin interpretar backslashes
read -p "Prompt: " variable      # Con mensaje
```

#### Substitución de Comandos
```bash
# Moderna (recomendada)
resultado=$(comando)
fecha=$(date '+%Y-%m-%d')

# Tradicional (compatible con sh)
resultado=`comando`
fecha=`date '+%Y-%m-%d'`
```

### 🐛 Solución de Problemas Comunes

#### Error: `: not found` o `$'\r': command not found`
```bash
# Problema: Terminaciones de línea Windows (CRLF)
# Solución:
tr -d '\r' < archivo.sh > archivo_limpio.sh
# o
sed 's/\r$//' archivo.sh > archivo_limpio.sh
```

#### Error: `missing ]`
```bash
# Problema: Falta espacio antes del ]
[ -d home]     # ❌ Incorrecto

# Solución: Agregar espacio
[ -d home ]    # ✅ Correcto
```

#### Error: `bash: not found`
```bash
# Usar sh en lugar de bash en sistemas mínimos
sh script.sh           # En lugar de bash script.sh
./script.sh            # Si tiene permisos de ejecución
```

### 📋 Comandos Universales (Disponibles en cualquier Unix)

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `echo` | Mostrar texto | `echo "Hola"` |
| `cat` | Mostrar contenido | `cat archivo.txt` |
| `ls` | Listar archivos | `ls -la` |
| `cd` | Cambiar directorio | `cd /home` |
| `pwd` | Directorio actual | `pwd` |
| `whoami` | Usuario actual | `whoami` |
| `date` | Fecha y hora | `date '+%Y-%m-%d'` |
| `uname` | Info del sistema | `uname -s` |
| `chmod` | Cambiar permisos | `chmod +x script.sh` |
| `mkdir` | Crear directorio | `mkdir carpeta` |
| `cp` | Copiar | `cp origen destino` |
| `mv` | Mover/renombrar | `mv viejo nuevo` |
| `rm` | Eliminar | `rm archivo` |
| `find` | Buscar archivos | `find . -name "*.sh"` |
| `grep` | Buscar texto | `grep "patrón" archivo` |

### 🔧 Herramientas de Limpieza

```bash
# Script automático para limpiar terminaciones CRLF
../fix_scripts.sh                    # Limpiar todos los .sh
../fix_scripts.sh archivo.sh         # Limpiar archivo específico

# Comando manual rápido
tr -d '\r' < archivo.sh > temp && mv temp archivo.sh && chmod +x archivo.sh
```

## 🚀 Requisitos Previos

- Conocimientos básicos de programación
- Familiaridad con sistemas Unix/Linux
- Terminal y editor de texto

## 📝 Estructura del Proyecto

```
Chapter-OS/
├── README.md
├── Session1-CommandLine/
│   ├── README.md
│   └── [scripts bash]
└── Session2-ArgumentsConfig/
    ├── README.md
    └── [scripts bash]
```

---
💡 **Tip**: Cada sesión incluye ejemplos prácticos y ejercicios para reforzar el aprendizaje.
