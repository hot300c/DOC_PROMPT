tell application "Google Chrome"
    activate
    delay 2
    
    -- Navigate to cursor.com dashboard settings
    set myTab to active tab of front window
    set URL of myTab to "https://cursor.com/dashboard?tab=settings"
    delay 5
    
    -- Click initial Delete button
    set jsCode1 to "
    const allButtons = document.querySelectorAll('button.dashboard-outline-button-red');
    for (let button of allButtons) {
        const span = button.querySelector('span.dashboard-outline-button-text');
        if (span && span.textContent.trim() === 'Delete') {
            button.click();
            return true;
        }
    }
    return false;
    "
    
    execute myTab javascript jsCode1
    
    -- Wait for popup
    delay 4
    
    -- Focus on input field and simulate keyboard typing
    set jsCode2 to "
    const inputs = document.querySelectorAll('input[type=\"text\"]');
    for (let input of inputs) {
        if (input.placeholder && input.placeholder.includes('Delete') && input.offsetParent !== null) {
            input.focus();
            input.value = ''; // Clear first
            return true;
        }
    }
    return false;
    "
    
    execute myTab javascript jsCode2
    
    -- Use System Events to type "Delete"
    tell application "System Events"
        delay 1
        key code 2 -- D
        delay 0.1
        key code 14 -- e
        delay 0.1
        key code 1 -- l
        delay 0.1
        key code 14 -- e
        delay 0.1
        key code 17 -- t
        delay 0.1
        key code 14 -- e
        delay 1
    end tell
    
    -- Wait for button to be enabled
    delay 3
    
    -- Click the confirmation button
    set jsCode3 to "
    const buttons = document.querySelectorAll('button');
    for (let button of buttons) {
        if (button.textContent.trim() === 'Delete' && 
            button.offsetParent !== null && 
            !button.disabled && 
            button.getAttribute('aria-disabled') !== 'true') {
            button.click();
            return 'Success: Confirmation button clicked!';
        }
    }
    
    // If still disabled, try to force enable and click
    for (let button of buttons) {
        if (button.textContent.trim() === 'Delete' && 
            button.offsetParent !== null &&
            (button.disabled || button.getAttribute('aria-disabled') === 'true')) {
            // Force enable
            button.disabled = false;
            button.removeAttribute('aria-disabled');
            button.click();
            return 'Success: Force clicked confirmation button!';
        }
    }
    
    return 'Error: Could not find or click confirmation button';
    "
    
    set result to execute myTab javascript jsCode3
    display dialog "Final result: " & result
    
end tell
