# Network Pinpointer - Windows Installation Guide

Complete guide to installing and using Network Pinpointer on Windows.

---

## Prerequisites

### 1. Install Python 3.8+

**Download Python**:
1. Go to https://www.python.org/downloads/windows/
2. Download the latest Python 3.x installer (3.8 or higher)
3. Run the installer

**Important**: Check "Add Python to PATH" during installation!

**Verify installation**:
```powershell
python --version
# Should show: Python 3.x.x
```

### 2. Install Npcap (Required for Packet Capture)

Network Pinpointer uses Scapy for packet capture, which requires Npcap on Windows.

**Download and Install**:
1. Go to https://npcap.com/#download
2. Download Npcap installer
3. Run installer with these options:
   - ✅ Install Npcap in WinPcap API-compatible mode
   - ✅ Support raw 802.11 traffic (optional)
4. Restart your computer after installation

**Note**: Without Npcap, Network Pinpointer will use fallback mode (limited packet capture).

---

## Installation

### Method 1: Using Git (Recommended)

**Install Git for Windows** (if not already installed):
1. Download from https://git-scm.com/download/win
2. Run installer (use default settings)

**Clone the repository**:
```powershell
# Open PowerShell or Command Prompt
cd C:\Users\YourUsername\Documents
git clone https://github.com/BruinGrowly/Network-Pinpointer.git
cd Network-Pinpointer
```

### Method 2: Direct Download

1. Go to https://github.com/BruinGrowly/Network-Pinpointer
2. Click green "Code" button → "Download ZIP"
3. Extract ZIP to a folder (e.g., `C:\Users\YourUsername\Documents\Network-Pinpointer`)
4. Open PowerShell/Command Prompt in that folder

### Install Dependencies

```powershell
# Install required Python packages
pip install scapy
pip install pyyaml

# Verify installation
python -c "import scapy; print('Scapy installed successfully')"
```

---

## Running Network Pinpointer on Windows

### Option 1: Using Python Directly (Easiest)

Since the `pinpoint` script uses a Unix shebang, on Windows you need to run it with Python:

```powershell
# Instead of: ./pinpoint health
# Use:
python pinpoint health

# Examples:
python pinpoint --help
python pinpoint health
python pinpoint quick-check 8.8.8.8
python pinpoint patterns
python pinpoint recipes
```

### Option 2: Create Windows Batch File (Recommended)

Create a `pinpoint.bat` file for easier usage:

**Create the file**:
```powershell
# In the Network-Pinpointer directory
notepad pinpoint.bat
```

**Add this content**:
```batch
@echo off
python "%~dp0pinpoint" %*
```

**Save and close**, then you can use:
```powershell
pinpoint health
pinpoint patterns
pinpoint quick-check 8.8.8.8
```

### Option 3: Create PowerShell Script

Create `pinpoint.ps1`:

```powershell
# In the Network-Pinpointer directory
notepad pinpoint.ps1
```

**Add this content**:
```powershell
python "$PSScriptRoot\pinpoint" @args
```

**Save and run**:
```powershell
.\pinpoint.ps1 health
.\pinpoint.ps1 patterns
```

---

## Administrator Privileges

Some network diagnostics require Administrator privileges on Windows.

### Run PowerShell as Administrator

1. Press `Win + X`
2. Select "Windows PowerShell (Admin)" or "Terminal (Admin)"
3. Navigate to Network-Pinpointer directory
4. Run commands

```powershell
cd C:\Users\YourUsername\Documents\Network-Pinpointer
python pinpoint ping 8.8.8.8
```

### Commands That Need Admin

- `ping` (for packet capture mode)
- `quick-check` (for packet capture)
- Any recipe that captures packets

### Commands That Don't Need Admin

- `health` (shows current state)
- `patterns` (shows pattern library)
- `recipes` (lists recipes)
- `explain` (explains LJPW)
- `config` (manages configuration)
- `diff` (compares states)
- `export` (exports results)

---

## Windows-Specific Configuration

### Configure for Windows Environment

```powershell
python pinpoint config create-example
```

This creates `%USERPROFILE%\.network-pinpointer\config.yaml`

**Edit the config** (adjust for Windows):
```yaml
network_type: enterprise
monitoring_interval: 300

# Windows paths use backslashes or forward slashes
export_dir: C:/Users/YourUsername/Documents/network_reports

# Or use environment variables
export_dir: %USERPROFILE%/network_reports

# Alerting still works the same
alert_slack_webhook: https://hooks.slack.com/services/YOUR/WEBHOOK
alert_email: oncall@example.com
```

---

## Common Windows Commands

### Basic Diagnostics

```powershell
# Show help
python pinpoint --help

# View pattern library
python pinpoint patterns

# List all recipes
python pinpoint recipes

# Explain LJPW dimensions
python pinpoint explain love
python pinpoint explain ljpw

# Show network health
python pinpoint health

# Quick 30-second check
python pinpoint quick-check 8.8.8.8
```

### Advanced Diagnostics

```powershell
# Run diagnostic recipes (requires Admin for full features)
python pinpoint run slow_connection api.example.com
python pinpoint run cant_connect db.example.com
python pinpoint run dns_troubleshooting nameserver.example.com

# Compare network states
python pinpoint diff before.json after.json

# View historical data
python pinpoint history api.prod.com --hours 24

# Continuous monitoring
python pinpoint watch api.prod.com db.prod.com --interval 300
```

### Export Results

```powershell
# Export to HTML (Windows paths)
python pinpoint health > C:\Temp\results.json
python pinpoint export C:\Temp\results.json -f html

# Opens in default browser
start C:\Temp\results.html
```

---

## Windows Firewall Considerations

Network Pinpointer may be blocked by Windows Firewall. If you get permission errors:

### Allow Python Through Firewall

1. Open "Windows Defender Firewall"
2. Click "Allow an app through firewall"
3. Click "Change settings" (requires admin)
4. Find "Python" in the list and check both "Private" and "Public"
5. If not in list, click "Allow another app" and browse to Python executable

### Or Create Firewall Rule (PowerShell Admin)

```powershell
New-NetFirewallRule -DisplayName "Network Pinpointer" `
  -Direction Inbound -Program "C:\Python3x\python.exe" `
  -Action Allow
```

---

## Troubleshooting Windows Issues

### Issue: "python: command not found"

**Solution**: Python not in PATH
```powershell
# Find Python installation
where python

# If not found, add to PATH:
# 1. Win + X → System → Advanced → Environment Variables
# 2. Edit "Path" variable
# 3. Add: C:\Python3x and C:\Python3x\Scripts
# 4. Restart PowerShell
```

### Issue: "scapy not found" or "No module named scapy"

**Solution**: Install Scapy
```powershell
pip install scapy
# Or specify Python version:
python -m pip install scapy
```

### Issue: "WARNING: scapy not available"

**Solution**: Install Npcap
1. Download from https://npcap.com/#download
2. Install in WinPcap-compatible mode
3. Restart computer
4. Test: `python -c "from scapy.all import *"`

### Issue: "Permission denied" or "Access denied"

**Solution**: Run as Administrator
```powershell
# Right-click PowerShell → "Run as Administrator"
cd C:\path\to\Network-Pinpointer
python pinpoint ping 8.8.8.8
```

### Issue: Packet capture not working

**Causes**:
1. Npcap not installed → Install Npcap
2. Not running as Admin → Run PowerShell as Admin
3. VPN interfering → Disconnect VPN temporarily

**Fallback**: Network Pinpointer works without packet capture (limited mode)

### Issue: Line endings / file encoding

If you get strange errors, the Unix line endings might be the issue:

**Fix line endings**:
```powershell
# Install dos2unix for Windows
# Or use Git Bash:
dos2unix pinpoint

# Or in PowerShell:
(Get-Content pinpoint) | Set-Content -Encoding utf8 pinpoint
```

---

## Using with Windows Subsystem for Linux (WSL)

**Alternative**: Run Network Pinpointer in WSL for native Linux experience

### Install WSL (Windows 10/11)

```powershell
# In PowerShell (Admin)
wsl --install
# Restart computer
```

### Use Network Pinpointer in WSL

```bash
# Inside WSL
cd /mnt/c/Users/YourUsername/Documents
git clone https://github.com/BruinGrowly/Network-Pinpointer.git
cd Network-Pinpointer

# Install dependencies
pip3 install scapy pyyaml

# Run normally
./pinpoint health
./pinpoint patterns
```

**Advantages of WSL**:
- Native Linux environment
- Scripts work as intended
- Better packet capture support
- All docs/examples work directly

---

## Windows-Specific Examples

### Example 1: Quick Health Check

```powershell
# Open PowerShell (Admin)
cd C:\Users\YourUsername\Documents\Network-Pinpointer

# Check Google's DNS
python pinpoint quick-check 8.8.8.8

# Check your corporate API
python pinpoint quick-check api.company.com
```

### Example 2: Diagnose Slow VPN

```powershell
# Run VPN diagnosis recipe
python pinpoint run vpn_diagnosis vpn.company.com

# View results with pattern matching
# Network Pinpointer will show LJPW analysis
```

### Example 3: Before/After Firewall Change

```powershell
# Capture baseline before change
python pinpoint health > C:\Temp\before-firewall-update.json

# Make firewall changes in Windows Defender Firewall...

# Capture after state
python pinpoint health > C:\Temp\after-firewall-update.json

# Compare
python pinpoint diff C:\Temp\before-firewall-update.json C:\Temp\after-firewall-update.json
```

### Example 4: Monitor Production Services

```powershell
# Create config
python pinpoint config create-example

# Edit: %USERPROFILE%\.network-pinpointer\config.yaml
notepad %USERPROFILE%\.network-pinpointer\config.yaml

# Start monitoring
python pinpoint watch api.prod.com db.prod.com --interval 300

# Runs continuously, Ctrl+C to stop
```

---

## Performance Notes for Windows

### Packet Capture Performance

Windows packet capture (via Npcap) is typically slower than Linux:
- **Linux**: Can capture 1000+ packets/second
- **Windows**: Usually 100-500 packets/second

**Tip**: For intensive packet capture, consider using WSL.

### File Paths

Network Pinpointer handles both Windows and Unix paths:
- `C:\Users\Name\file.json` ✅ Works
- `C:/Users/Name/file.json` ✅ Works
- `/mnt/c/Users/Name/file.json` ✅ Works (in WSL)

---

## Quick Reference Card

```powershell
# Installation
pip install scapy pyyaml

# Basic usage (no admin needed)
python pinpoint --help          # Show help
python pinpoint patterns        # Pattern library
python pinpoint recipes         # Available recipes
python pinpoint explain love    # Learn LJPW

# Diagnostics (admin recommended)
python pinpoint health          # Current health
python pinpoint quick-check HOST
python pinpoint run RECIPE HOST

# Advanced (no admin needed)
python pinpoint diff FILE1 FILE2
python pinpoint history HOST --hours 24
python pinpoint export FILE -f html
python pinpoint config show

# Monitoring (admin recommended)
python pinpoint watch HOST1 HOST2 --interval 300
```

---

## Getting Help

### Documentation
- **Usage Guide**: `docs\USAGE_GUIDE.md`
- **Demo Walkthrough**: `docs\DEMO_WALKTHROUGH.md`
- **Patterns**: `python pinpoint patterns`
- **Recipes**: `python pinpoint recipes`

### Online Help
```powershell
python pinpoint --help
python pinpoint COMMAND --help
python pinpoint explain ljpw
```

### Common Issues
See "Troubleshooting Windows Issues" section above

### Report Issues
GitHub: https://github.com/BruinGrowly/Network-Pinpointer/issues

---

## Summary: Quick Start for Windows Users

1. **Install Python 3.8+** (with PATH)
2. **Install Npcap** (for packet capture)
3. **Clone repository** or download ZIP
4. **Install dependencies**: `pip install scapy pyyaml`
5. **Run with Python**: `python pinpoint health`
6. **Optional**: Create `pinpoint.bat` for easier usage
7. **Use Admin** for packet capture features

**First commands to try**:
```powershell
python pinpoint patterns        # See what it can detect
python pinpoint recipes         # See diagnostic workflows
python pinpoint explain ljpw    # Understand the framework
python pinpoint quick-check 8.8.8.8  # Try a diagnostic
```

Welcome to semantic network diagnostics! 🌐
