#!/usr/bin/env python3
"""
🚀 Universal Setup Script
One-command setup for the Image Processing Distributed System

Usage:
    python setup.py                    # Full setup (Docker Compose + K8s ready)
    python setup.py --docker-only      # Docker Compose only
    python setup.py --k8s-only         # Kubernetes only
    python setup.py --check            # Check prerequisites only
"""

import subprocess
import sys
import argparse
import platform
import os
from pathlib import Path

def run_command(cmd, description, ignore_errors=False):
    """Run a command and handle errors"""
    print(f"\n🔨 {description}")
    print(f"💻 {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success!")
        return True
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            print(f"⚠️  Warning: {e}")
            return True
        else:
            print(f"❌ Error: {e}")
            if e.stdout:
                print(f"📤 Output: {e.stdout}")
            if e.stderr:
                print(f"📥 Error: {e.stderr}")
            return False

def check_prerequisites():
    """Check all prerequisites"""
    print("🔍 CHECKING PREREQUISITES...")
    
    issues = []
    
    # Check Python
    print(f"🐍 Python: {sys.version}")
    
    # Check Docker
    if not run_command("docker --version", "Checking Docker", ignore_errors=True):
        issues.append("❌ Docker not found - Install Docker Desktop")
    
    # Check pip packages
    required_packages = ["redis", "requests", "psutil", "Pillow"]
    for package in required_packages:
        if not run_command(f"python -c 'import {package}'", f"Checking {package}", ignore_errors=True):
            issues.append(f"❌ Python package '{package}' missing")
    
    # Check kubectl (optional for K8s)
    if not run_command("kubectl version --client", "Checking kubectl", ignore_errors=True):
        print("⚠️  kubectl not found - Kubernetes features will be unavailable")
    
    if issues:
        print(f"\n🚨 ISSUES FOUND:")
        for issue in issues:
            print(f"   {issue}")
        return False
    else:
        print(f"\n✅ ALL PREREQUISITES OK!")
        return True

def install_python_deps():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    return run_command("pip install -r requirements.txt", "Install requirements.txt")

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    dirs = ["static/processed", "logs"]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Created: {dir_path}")
    
    return True

def setup_docker():
    """Setup Docker environment"""
    print("\n🐳 SETTING UP DOCKER ENVIRONMENT...")
    
    # Create directories
    if not create_directories():
        return False
    
    # Install Python dependencies
    if not install_python_deps():
        return False
    
    # Test Django
    if not run_command("python manage.py check", "Django configuration check"):
        return False
    
    print(f"\n✅ DOCKER SETUP COMPLETE!")
    print(f"📋 Next steps:")
    print(f"   1. docker-compose up")
    print(f"   2. curl -X POST http://localhost:8000/api/process-batch/distributed/")
    
    return True

def setup_kubernetes():
    """Setup Kubernetes environment"""
    print("\n☸️  SETTING UP KUBERNETES ENVIRONMENT...")
    
    # Check kubectl
    if not run_command("kubectl version --client", "Verify kubectl"):
        print("❌ kubectl required for Kubernetes setup")
        return False
    
    # Check cluster connection
    if not run_command("kubectl cluster-info", "Check cluster connection"):
        print("❌ No Kubernetes cluster found")
        print("💡 Enable Kubernetes in Docker Desktop Settings")
        return False
    
    # Build production images
    if not run_command("python build.py", "Build production images"):
        return False
    
    print(f"\n✅ KUBERNETES SETUP COMPLETE!")
    print(f"📋 Next steps:")
    print(f"   1. cd k8s")
    print(f"   2. python demo.py")
    
    return True

def show_status():
    """Show current project status"""
    print("\n📊 PROJECT STATUS:")
    
    # Docker images
    print("\n🐳 Docker Images:")
    run_command("docker images | grep projects", "List project images", ignore_errors=True)
    
    # Docker containers
    print("\n📦 Docker Containers:")
    run_command("docker-compose ps", "List containers", ignore_errors=True)
    
    # Kubernetes (if available)
    if run_command("kubectl cluster-info", "Check K8s cluster", ignore_errors=True):
        print("\n☸️  Kubernetes Pods:")
        run_command("kubectl get pods", "List pods", ignore_errors=True)
        
        print("\n📈 HPA Status:")
        run_command("kubectl get hpa", "List HPA", ignore_errors=True)

def main():
    parser = argparse.ArgumentParser(description="Universal Setup Script")
    parser.add_argument("--docker-only", action="store_true", help="Setup Docker Compose only")
    parser.add_argument("--k8s-only", action="store_true", help="Setup Kubernetes only")
    parser.add_argument("--check", action="store_true", help="Check prerequisites only")
    parser.add_argument("--status", action="store_true", help="Show current status")
    
    args = parser.parse_args()
    
    print("🚀 UNIVERSAL SETUP SCRIPT")
    print(f"🖥️  Platform: {platform.system()} {platform.machine()}")
    print(f"📁 Directory: {os.getcwd()}")
    print("="*60)
    
    # Status check
    if args.status:
        show_status()
        return
    
    # Prerequisites check
    if args.check:
        check_prerequisites()
        return
    
    # Check prerequisites first
    if not check_prerequisites():
        print(f"\n⚠️  Fix prerequisites before continuing...")
        print(f"💡 Install missing components and run: python setup.py --check")
        sys.exit(1)
    
    # Setup based on arguments
    success = True
    
    if args.docker_only:
        success = setup_docker()
    elif args.k8s_only:
        success = setup_kubernetes()
    else:
        # Full setup
        success = setup_docker() and setup_kubernetes()
    
    if success:
        show_status()
        print(f"\n🎉 SETUP COMPLETE! System ready to use! 🚀")
    else:
        print(f"\n❌ SETUP FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()