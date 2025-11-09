# 📤 GitHub Deployment Instructions

## Before You Push

Make sure these files are ready:
- ✅ `README.md` - Updated with one-line installer
- ✅ `install.sh` - One-line installer script
- ✅ `setup.sh` - Interactive setup script
- ✅ `.env.example` - Example configuration
- ✅ All source files in `src/`
- ✅ `requirements.txt`
- ✅ `VERSION` (1.1.0)
- ✅ `CHANGELOG.md`

## Step 1: Initialize Git Repository (if not already)

```bash
cd "/home/kasniya/admin actrion bot"
git init
git add .
git commit -m "Initial commit: Admin Action Bot v1.1.0"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `admin-action-bot` (or your preferred name)
3. Description: "Discord bot for Minecraft server administration via Pterodactyl API"
4. Choose Public or Private
5. **DO NOT** initialize with README (you already have one)
6. Click "Create repository"

## Step 3: Push to GitHub

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Update Installer URLs

After pushing, update these files with your actual GitHub URL:

### Update `README.md`
Replace:
```bash
bash <(curl -s https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/install.sh)
```

With:
```bash
bash <(curl -s https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/main/install.sh)
```

### Update `install.sh`
Edit line 16:
```bash
REPO_URL="https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git"
```

Then commit and push the changes:
```bash
git add README.md install.sh
git commit -m "Update installer URLs with actual GitHub repository"
git push
```

## Step 5: Test the One-Line Installer

On a clean system or another directory:
```bash
bash <(curl -s https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/install.sh)
```

## Step 6: Add Repository Topics (Optional)

On GitHub, go to your repository and add topics:
- `discord-bot`
- `minecraft`
- `pterodactyl`
- `admin-tools`
- `server-management`
- `python`
- `discord-py`

## Step 7: Create a Release (Optional)

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag: `v1.1.0`
4. Title: `Admin Action Bot v1.1.0 - Player Dropdown Release`
5. Description:
   ```markdown
   ## 🎉 Production Ready - v1.1.0
   
   ### ✨ New Features
   - 🎯 **Player Dropdown Selection** - Auto-remembers last 25 players
   - ⚡ **50% Faster Moderation** - Click to select instead of typing
   
   ### ✅ Features
   - 6 working moderation actions (Kill, Kick, Temp Ban, Ban, Freeze, Unfreeze)
   - Persistent buttons (work after restarts)
   - LibertyBan compatibility
   - Comprehensive audit logging
   - One-line installer
   
   ### 🚀 Quick Install
   ```bash
   bash <(curl -s https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/install.sh)
   ```
   
   ### 📚 Documentation
   - [Installation Guide](README.md)
   - [Player Dropdown Feature](PLAYER_DROPDOWN_FEATURE.md)
   - [Changelog](CHANGELOG.md)
   ```
6. Click "Publish release"

## Your One-Line Installer

After pushing, users can install with:

```bash
bash <(curl -s https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/install.sh)
```

This will:
1. ✅ Check prerequisites (Python, git, pip)
2. ✅ Clone your repository
3. ✅ Create virtual environment
4. ✅ Install dependencies
5. ✅ Run interactive configuration
6. ✅ Set up systemd service (optional)
7. ✅ Start the bot

## Example Usage

Once on GitHub, share with your users:

**For Linux/Ubuntu VPS:**
```bash
bash <(curl -s https://raw.githubusercontent.com/yourusername/admin-action-bot/main/install.sh)
```

**Manual Installation:**
```bash
git clone https://github.com/yourusername/admin-action-bot.git
cd admin-action-bot
./setup.sh
```

## Don't Forget!

Before pushing to GitHub:
- [ ] Create `.gitignore` to exclude sensitive files
- [ ] Make sure `.env` is in `.gitignore`
- [ ] Use `.env.example` for template
- [ ] Update `install.sh` with your repo URL
- [ ] Update `README.md` with your repo URL
- [ ] Test the installer on a clean system

## .gitignore Template

Create `.gitignore`:
```gitignore
# Environment
.env
.env.local
*.env.backup.*

# Virtual Environment
venv/
env/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Logs
logs/*.log
logs/agent_log.md
*.log

# Cache
cache/
*.cache

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Test
.pytest_cache/
.coverage
htmlcov/

# Temp
temp/
tmp/
*.tmp
```

Save this as `.gitignore` in your project root before committing!

---

**Ready to deploy? Push to GitHub and share your one-line installer!** 🚀
