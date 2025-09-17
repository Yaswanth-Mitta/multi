#!/usr/bin/env python3
"""Comprehensive system validation script"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
        return False

def check_node_version():
    """Check Node.js version"""
    print("📦 Checking Node.js version...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version} - OK")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False

def check_env_file():
    """Check .env file exists and has required keys"""
    print("🔧 Checking .env configuration...")
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ .env file not found")
        return False
    
    required_keys = [
        'SERP_API_KEY',
        'AWS_ACCESS_KEY_ID', 
        'AWS_SECRET_ACCESS_KEY',
        'PUBLIC_IP'
    ]
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    missing_keys = []
    for key in required_keys:
        if f"{key}=" not in content:
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ Missing required keys: {', '.join(missing_keys)}")
        return False
    else:
        print("✅ .env file has required keys")
        return True

def check_backend_structure():
    """Check backend directory structure"""
    print("🏗️ Checking backend structure...")
    
    required_files = [
        'backend/server.py',
        'backend/orchestrator.py',
        'backend/factory.py',
        'backend/interfaces.py',
        'backend/config.py',
        'backend/requirements.txt',
        'backend/test_imports.py'
    ]
    
    required_dirs = [
        'backend/agents',
        'backend/services'
    ]
    
    missing = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
    
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing.append(dir_path)
    
    if missing:
        print(f"❌ Missing: {', '.join(missing)}")
        return False
    else:
        print("✅ Backend structure complete")
        return True

def check_frontend_structure():
    """Check frontend directory structure"""
    print("🌐 Checking frontend structure...")
    
    required_files = [
        'frontend-nextjs/package.json',
        'frontend-nextjs/next.config.js',
        'frontend-nextjs/app/page.tsx',
        'frontend-nextjs/app/api/research/route.ts'
    ]
    
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
    
    if missing:
        print(f"❌ Missing: {', '.join(missing)}")
        return False
    else:
        print("✅ Frontend structure complete")
        return True

def check_docker_files():
    """Check Docker configuration"""
    print("🐳 Checking Docker configuration...")
    
    required_files = [
        'docker-compose.yml',
        'backend/Dockerfile',
        'frontend-nextjs/Dockerfile'
    ]
    
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
    
    if missing:
        print(f"❌ Missing: {', '.join(missing)}")
        return False
    else:
        print("✅ Docker configuration complete")
        return True

def check_k8s_files():
    """Check Kubernetes configuration"""
    print("☸️ Checking Kubernetes configuration...")
    
    required_files = [
        'k8s/namespace.yaml',
        'k8s/configmap.yaml',
        'k8s/backend-deployment.yaml',
        'k8s/backend-service.yaml',
        'k8s/frontend-deployment.yaml',
        'k8s/frontend-service.yaml'
    ]
    
    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)
    
    if missing:
        print(f"❌ Missing: {', '.join(missing)}")
        return False
    else:
        print("✅ Kubernetes configuration complete")
        return True

def test_backend_imports():
    """Test backend Python imports"""
    print("🧪 Testing backend imports...")
    
    try:
        result = subprocess.run([
            sys.executable, 'backend/test_imports.py'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print("✅ Backend imports successful")
            return True
        else:
            print(f"❌ Backend import errors:\n{result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Failed to test imports: {e}")
        return False

def main():
    """Run all validation checks"""
    print("🔍 AI Research Agent - System Validation")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Node.js Version", check_node_version),
        ("Environment Config", check_env_file),
        ("Backend Structure", check_backend_structure),
        ("Frontend Structure", check_frontend_structure),
        ("Docker Config", check_docker_files),
        ("Kubernetes Config", check_k8s_files),
        ("Backend Imports", test_backend_imports)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 System validation successful! Ready to deploy.")
        return True
    else:
        print(f"\n⚠️ {total - passed} issues found. Please fix before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)