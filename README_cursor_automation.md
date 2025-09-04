# Cursor VIP Free & Account Deletion Automation

This repository contains automation scripts to reset Cursor editor and delete account settings automatically.

## 🎯 Purpose

Automate the complete process of:
1. Closing Cursor application
2. Running `cursor vip free` command 
3. Opening Chrome with specific profile
4. Navigating to Cursor dashboard settings
5. Clicking Delete button and confirming deletion

## 📁 Files

### Main Automation Scripts

1. **`keyboard_simulation.scpt`** - ✅ **RECOMMENDED** - Uses AppleScript + keyboard simulation
2. **`full_cursor_reset.sh`** - Complete end-to-end bash script with embedded AppleScript
3. **`manual_console_script.js`** - JavaScript for manual browser console execution

## 🚀 Usage

### Option 1: Keyboard Simulation (Recommended)
```bash
# Run the working keyboard simulation script
osascript keyboard_simulation.scpt
```

### Option 2: Complete End-to-End
```bash
# Make executable if needed
chmod +x full_cursor_reset.sh

# Run complete automation
./full_cursor_reset.sh
```

### Option 3: Manual Browser Console
1. Navigate to `https://cursor.com/dashboard?tab=settings`
2. Click the initial Delete button manually
3. Open browser console (F12 → Console)
4. Paste contents of `manual_console_script.js`
5. Press Enter

## 🔧 How It Works

### Step 1: Initial Setup
- Closes Cursor application: `pkill -f "Cursor"`
- Runs cursor reset: `cursor vip free`
- Opens Chrome with profile: `"carphucng2001a@gmail.com"`

### Step 2: Browser Navigation
- Navigates to: `https://cursor.com/dashboard?tab=settings`
- Finds initial Delete button with class: `dashboard-outline-button-red`
- Clicks button with span text: "Delete"

### Step 3: Confirmation Popup
- Waits for confirmation popup to appear
- Finds input field with placeholder: `"Type 'Delete' to confirm"`
- Types "Delete" using keyboard simulation
- Waits for confirmation button to be enabled

### Step 4: Final Confirmation
- Finds confirmation Delete button (initially `disabled=true`)
- Waits for button to be enabled after input
- Clicks final Delete button to complete deletion

## 🎛️ Target HTML Elements

### Initial Delete Button
```html
<button class="dashboard-outline-button dashboard-outline-button-red">
  <span class="dashboard-outline-button-text">Delete</span>
</button>
```

### Confirmation Input Field
```html
<input type="text" placeholder="Type 'Delete' to confirm">
```

### Final Confirmation Button
```html
<button aria-disabled="true" class="relative inline-flex items-center justify-center..." disabled="">
  <span class="relative z-10 flex">Delete</span>
</button>
```

## 🛠️ Technical Details

- **Language**: AppleScript + JavaScript + Bash
- **Browser**: Google Chrome
- **Profile**: carphucng2001a@gmail.com
- **Platform**: macOS
- **Dependencies**: Chrome browser, Cursor editor

## ⚠️ Requirements

1. macOS with AppleScript support
2. Google Chrome browser installed
3. Chrome profile "carphucng2001a@gmail.com" configured
4. Cursor editor installed
5. Accessibility permissions for Terminal/AppleScript (if needed)

## 🔐 Permissions

If you get permission errors:
1. Go to System Preferences → Security & Privacy → Privacy → Accessibility
2. Add Terminal (or the application running the script) to allowed list
3. Retry the script

## 📝 Logs & Debugging

The scripts include console logging and debugging output. Check the browser console for detailed execution logs when running the automation.

## 🎉 Success Indicators

- "Success: Confirmation button clicked!" message
- Account deletion confirmation on the website
- Chrome profile reset complete

---

**Note**: These scripts automate a legitimate account deletion process. Use responsibly and only on your own accounts.
