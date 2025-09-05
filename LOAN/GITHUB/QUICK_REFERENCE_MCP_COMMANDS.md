# Quick Reference - MCP GitHub Commands

## ⚠️ MCP Status Notice

**Current Status**: MCP GitHub Projects server may be temporarily unavailable  
**Last Working**: 2025-09-04  
**Alternative**: ✅ GitHub CLI is working perfectly

---

## 🚀 Most Used Commands

### **1. Check Project Status (GitHub CLI)**
```bash
gh issue list --repo PNTSOL/LMA_BACKEND --state open
```

### **2. Create New Task (GitHub CLI)**
```bash
gh issue create --repo PNTSOL/LMA_BACKEND --title "Task Title" --body "Task Description"
```

### **3. Close Task (GitHub CLI)**
```bash
gh issue close --repo PNTSOL/LMA_BACKEND 1
```

### **4. Update Task Progress (GitHub CLI)**
```bash
gh issue edit --repo PNTSOL/LMA_BACKEND 1 --body "Updated task description with progress"
```

### **5. Assign Task (GitHub CLI)**
```bash
gh issue edit --repo PNTSOL/LMA_BACKEND 1 --assignee hot300c
```

---

## 📋 Project Info

- **Repository**: PNTSOL/LMA_BACKEND
- **Current Tasks**: 5 open, 0 closed
- **Assignee**: hot300c
- **Status**: All tasks active

---

## 🎯 Copy-Paste Commands (GitHub CLI)

### **Daily Check**
```bash
gh issue list --repo PNTSOL/LMA_BACKEND --state open
```

### **Add Feature Task**
```bash
gh issue create --repo PNTSOL/LMA_BACKEND --title "New Feature" --body "Feature description" --label enhancement
```

### **Mark Complete**
```bash
gh issue close --repo PNTSOL/LMA_BACKEND 1
```

### **Update Progress**
```bash
gh issue edit --repo PNTSOL/LMA_BACKEND 1 --body "Progress: 75% complete. Working on..."
```

### **Check Closed Issues**
```bash
gh issue list --repo PNTSOL/LMA_BACKEND --state closed
```

---

## 🔄 Alternative Methods (If MCP Down)

### **GitHub CLI (✅ Working):**
```bash
# Check status
gh issue list --repo PNTSOL/LMA_BACKEND

# Create task
gh issue create --repo PNTSOL/LMA_BACKEND --title "Task" --body "Description"

# Close task
gh issue close --repo PNTSOL/LMA_BACKEND 1
```

### **PowerShell Script:**
```bash
.\github-project-manager-fixed.ps1 -Action status
```

### **Web Interface:**
https://github.com/PNTSOL/LMA_BACKEND/issues

---

## 📞 Help Commands

```bash
# Check user info
gh auth status

# List all issues
gh issue list --repo PNTSOL/LMA_BACKEND

# View specific issue
gh issue view --repo PNTSOL/LMA_BACKEND 1
```

---

**Note**: GitHub CLI is working perfectly! Use `gh` commands for reliable project management.
