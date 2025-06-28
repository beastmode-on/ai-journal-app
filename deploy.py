#!/usr/bin/env python3
"""
AI Journal Deployment Script
Automatically deploys the app to Render.com
"""

import os
import requests
import json
import time
import subprocess
import sys

def run_command(command):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def create_github_repo():
    """Create GitHub repository using GitHub CLI"""
    print("🔧 Setting up GitHub repository...")
    
    # Check if gh is authenticated
    success, stdout, stderr = run_command("gh auth status")
    if not success:
        print("❌ GitHub CLI not authenticated. Please run: gh auth login")
        return False, None
    
    # Create repository
    repo_name = "ai-journal-app"
    success, stdout, stderr = run_command(f"gh repo create {repo_name} --public --source=. --remote=origin --push")
    
    if success:
        print("✅ GitHub repository created successfully!")
        return True, f"https://github.com/{get_github_username()}/{repo_name}"
    else:
        print(f"❌ Failed to create GitHub repository: {stderr}")
        return False, None

def get_github_username():
    """Get GitHub username from gh CLI"""
    success, stdout, stderr = run_command("gh api user --jq .login")
    if success:
        return stdout.strip().strip('"')
    return "your-username"

def deploy_to_render():
    """Deploy to Render.com using their API"""
    print("🚀 Deploying to Render.com...")
    
    # Render API configuration
    RENDER_API_URL = "https://api.render.com/v1/services"
    RENDER_API_KEY = os.getenv("RENDER_API_KEY")
    
    if not RENDER_API_KEY:
        print("❌ RENDER_API_KEY not set. Please set it as an environment variable.")
        print("   Get your API key from: https://render.com/docs/api")
        return False, None
    
    # Service configuration
    service_config = {
        "name": "ai-journal",
        "type": "web_service",
        "env": "python",
        "buildCommand": "pip install -r requirements.txt",
        "startCommand": "gunicorn app:app",
        "plan": "free",
        "repo": f"https://github.com/{get_github_username()}/ai-journal-app",
        "branch": "main"
    }
    
    headers = {
        "Authorization": f"Bearer {RENDER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(RENDER_API_URL, json=service_config, headers=headers)
        if response.status_code == 201:
            service_data = response.json()
            service_id = service_data["id"]
            print(f"✅ Service created! Service ID: {service_id}")
            return True, service_id
        else:
            print(f"❌ Failed to create service: {response.text}")
            return False, None
    except Exception as e:
        print(f"❌ Error deploying to Render: {e}")
        return False, None

def check_deployment_status(service_id):
    """Check deployment status"""
    RENDER_API_URL = f"https://api.render.com/v1/services/{service_id}"
    RENDER_API_KEY = os.getenv("RENDER_API_KEY")
    
    headers = {"Authorization": f"Bearer {RENDER_API_KEY}"}
    
    while True:
        try:
            response = requests.get(RENDER_API_URL, headers=headers)
            if response.status_code == 200:
                service_data = response.json()
                status = service_data.get("status", "unknown")
                print(f"📊 Deployment status: {status}")
                
                if status == "live":
                    service_url = service_data.get("service", {}).get("url")
                    print(f"🎉 Deployment successful!")
                    print(f"🌍 Your app is live at: {service_url}")
                    return True, service_url
                elif status in ["failed", "canceled"]:
                    print("❌ Deployment failed!")
                    return False, None
                
                time.sleep(10)  # Wait 10 seconds before checking again
            else:
                print(f"❌ Error checking status: {response.text}")
                return False, None
        except Exception as e:
            print(f"❌ Error checking deployment status: {e}")
            return False, None

def main():
    """Main deployment function"""
    print("🤖 AI Journal Deployment Script")
    print("=" * 50)
    
    # Step 1: Create GitHub repository
    success, repo_url = create_github_repo()
    if not success:
        print("❌ Failed to create GitHub repository")
        return
    
    print(f"📦 Repository URL: {repo_url}")
    
    # Step 2: Deploy to Render
    success, service_id = deploy_to_render()
    if not success:
        print("❌ Failed to deploy to Render")
        return
    
    # Step 3: Monitor deployment
    print("⏳ Monitoring deployment...")
    success, app_url = check_deployment_status(service_id)
    
    if success:
        print("\n🎉 SUCCESS! Your AI Journal is now live globally!")
        print(f"🌍 Access it at: {app_url}")
        print("\n📱 You can now access your journal from:")
        print("   - Your phone")
        print("   - Any computer")
        print("   - Anywhere in the world!")
    else:
        print("❌ Deployment failed. Check the logs above for details.")

if __name__ == "__main__":
    main() 