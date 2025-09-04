#!/bin/bash

echo "Starting complete Cursor reset automation..."

# Step 1: Close Cursor
echo "Step 1: Closing Cursor application..."
pkill -f "Cursor" 2>/dev/null || true
sleep 2

# Step 2: Run cursor vip free
echo "Step 2: Running cursor vip free..."
cursor vip free
sleep 2

# Step 3: Open Chrome with profile and complete delete flow
echo "Step 3: Opening Chrome and executing complete delete flow..."
open -a "Google Chrome" --args --profile-directory="carphucng2001a@gmail.com"
sleep 3

# Step 4: Execute the complete delete automation
osascript - <<'EOF'
tell application "Google Chrome"
    activate
    delay 2
    
    -- Navigate to cursor.com dashboard settings
    set myTab to active tab of front window
    set URL of myTab to "https://cursor.com/dashboard?tab=settings"
    delay 5
    
    -- Complete delete flow: initial click + confirmation
    set jsCode to "
    async function completeDeleteFlow() {
        // Step 1: Click initial Delete button
        const allButtons = document.querySelectorAll('button.dashboard-outline-button, button.dashboard-outline-button-red');
        let initialClicked = false;
        
        for (let button of allButtons) {
            const span = button.querySelector('span.dashboard-outline-button-text');
            if (span && span.textContent.trim() === 'Delete') {
                console.log('Clicking initial Delete button:', button);
                button.click();
                initialClicked = true;
                break;
            }
        }
        
        if (!initialClicked) {
            return 'Error: Initial Delete button not found';
        }
        
        // Wait for popup to appear
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Step 2: Find input field and fill it
        const inputs = document.querySelectorAll('input[type=\"text\"], input:not([type])');
        let inputFilled = false;
        
        for (let input of inputs) {
            if (input.offsetParent !== null && input.style.display !== 'none') {
                console.log('Filling input field:', input);
                input.focus();
                input.value = 'Delete';
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
                input.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
                inputFilled = true;
                break;
            }
        }
        
        if (!inputFilled) {
            return 'Error: Input field not found';
        }
        
        // Wait for button to be enabled
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Step 3: Click confirmation Delete button
        const confirmButtons = document.querySelectorAll('button');
        for (let button of confirmButtons) {
            const span = button.querySelector('span');
            if (span && span.textContent.trim() === 'Delete' && 
                !button.disabled && 
                button.getAttribute('aria-disabled') !== 'true' &&
                button.offsetParent !== null) {
                console.log('Clicking confirmation Delete button:', button);
                button.click();
                return 'Success: Complete delete flow completed successfully!';
            }
        }
        
        return 'Error: Confirmation Delete button not found or still disabled';
    }
    
    completeDeleteFlow().then(result => {
        console.log('Final result:', result);
        return result;
    });
    "
    
    set result to execute myTab javascript jsCode
    return result
end tell
EOF

echo "Complete Cursor reset automation finished!"
