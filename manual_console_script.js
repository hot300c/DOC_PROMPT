// Run this in the browser console after clicking the initial Delete button
// and the popup appears

console.log("=== MANUAL DELETE CONFIRMATION SCRIPT ===");

// Step 1: Find the input field
const inputs = document.querySelectorAll('input[type="text"]');
console.log("Found inputs:", inputs.length);

let targetInput = null;
inputs.forEach((input, i) => {
    console.log(`Input ${i}:`, {
        placeholder: input.placeholder,
        visible: input.offsetParent !== null,
        value: input.value
    });
    
    if (input.placeholder && input.placeholder.includes('Delete') && input.offsetParent !== null) {
        targetInput = input;
    }
});

if (!targetInput) {
    console.log("❌ No input field found with 'Delete' placeholder");
    return;
}

console.log("✅ Found target input:", targetInput);

// Step 2: Fill the input
targetInput.focus();
targetInput.value = 'Delete';

// Trigger events
targetInput.dispatchEvent(new Event('input', { bubbles: true }));
targetInput.dispatchEvent(new Event('change', { bubbles: true }));
targetInput.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));

console.log("✅ Input filled with:", targetInput.value);

// Step 3: Wait and check buttons
setTimeout(() => {
    console.log("\n=== CHECKING DELETE BUTTONS AFTER INPUT ===");
    
    const buttons = document.querySelectorAll('button');
    let deleteButtons = [];
    
    buttons.forEach((button, i) => {
        if (button.textContent.trim() === 'Delete' && button.offsetParent !== null) {
            deleteButtons.push({
                index: i,
                button: button,
                disabled: button.disabled,
                ariaDisabled: button.getAttribute('aria-disabled'),
                classes: button.className.substring(0, 60)
            });
        }
    });
    
    console.log("Found Delete buttons:", deleteButtons.length);
    deleteButtons.forEach((btn, i) => {
        console.log(`Delete Button ${i}:`, {
            disabled: btn.disabled,
            ariaDisabled: btn.ariaDisabled,
            classes: btn.classes
        });
    });
    
    // Try to click the enabled one
    const enabledButton = deleteButtons.find(btn => 
        !btn.button.disabled && 
        btn.button.getAttribute('aria-disabled') !== 'true'
    );
    
    if (enabledButton) {
        console.log("✅ Found enabled Delete button, clicking...");
        enabledButton.button.click();
        console.log("🎉 Delete confirmation clicked successfully!");
    } else {
        console.log("❌ No enabled Delete button found");
        console.log("All Delete buttons are still disabled. Input value:", targetInput.value);
        
        // Try forcing the click anyway
        if (deleteButtons.length > 0) {
            console.log("🔧 Attempting to force click disabled button...");
            // Remove disabled attribute temporarily
            const btn = deleteButtons[deleteButtons.length - 1].button; // Get last one (likely the confirmation button)
            btn.disabled = false;
            btn.removeAttribute('aria-disabled');
            btn.click();
            console.log("🔧 Force clicked!");
        }
    }
}, 2000);

console.log("⏳ Waiting 2 seconds before checking buttons...");
