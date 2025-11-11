// ============================================
// MANUAL CUSTOMIZATION FOR DOTS
// ============================================

// Define which slides should have medium gray tooltips
const mediumGraySlides = [2, 6, 11, 12, 15, 16, 18]; // Add any slide numbers you want

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎨 Manual Dot Customization Loaded');
    console.log('📋 Medium gray slides:', mediumGraySlides);
    console.log('');
    console.log('Available commands:');
    console.log('  setTooltip(slideNumber, "text") - Set tooltip for specific slide');
    console.log('  setMediumGray(slideNumber, slideNumber, ...) - Mark slides as medium gray');
    console.log('  clearTooltip(slideNumber) - Remove tooltip from slide');
    console.log('  clearAllTooltips() - Remove all tooltips');
    console.log('');
    console.log('Examples:');
    console.log('  setTooltip(5, "Projects")');
    console.log('  setTooltip(11, "Mark Classification Tool")');
    console.log('  setTooltip(12, "Marksheet Generator")');
    console.log('  setTooltip(15, "Autonomy by Design")');
    console.log('  setTooltip(16, "UX Dictionary")');
    console.log('  setTooltip(18, "Definition Quality Scorer")');
    
    // Expose functions to global window for easy console access
    window.setTooltip = function(slideNumber, text) {
        if (typeof slideNumber === 'number' && slideNumber >= 1 && slideNumber <= 23) {
            // Create tooltip element if it doesn't exist
            let tooltip = document.querySelector(`.dot-tooltip[data-slide="${slideNumber}"]`);
            
            if (!tooltip) {
                tooltip = document.createElement('div');
                tooltip.className = 'dot-tooltip';
                tooltip.textContent = text;
                tooltip.setAttribute('data-slide', slideNumber);
                
                // Find the dot container for this slide
                let dotContainer = document.querySelector(`.dot-container[data-slide="${slideNumber}"]`);
                
                if (dotContainer) {
                    dotContainer.appendChild(tooltip);
                } else {
                    // Create a new dot container if it doesn't exist
                    dotContainer = document.createElement('div');
                    dotContainer.className = 'dot-container';
                    dotContainer.setAttribute('data-slide', slideNumber);
                    
                    // Create the dot
                    const dot = document.createElement('div');
                    dot.className = 'mini-progress-dot';
                    dot.setAttribute('aria-label', `Go to slide ${slideNumber}`);
                    dot.setAttribute('role', 'button');
                    dot.tabIndex = 0;
                    
                    // Add the tooltip
                    dotContainer.appendChild(tooltip);
                    dotContainer.appendChild(dot);
                    
                    // Add the container to the progress bar
                    const miniProgress = document.getElementById('miniProgress');
                    if (miniProgress) {
                        miniProgress.appendChild(dotContainer);
                    }
                }
                
                console.log(`✅ Tooltip set for slide ${slideNumber}: "${text}"`);
            } else {
                // Just update existing tooltip
                if (text) {
                    tooltip.textContent = text;
                    console.log(`✅ Tooltip set for slide ${slideNumber}: "${text}"`);
                } else {
                    tooltip.textContent = '';
                    console.log(`✅ Tooltip cleared for slide ${slideNumber}`);
                }
            }
        }
    };
    
    window.setMediumGray = function(...slideNumbers) {
        slideNumbers.forEach(num => {
            if (typeof num === 'number' && num >= 1 && num <= 23) {
                // Find the dot element for this slide
                const dot = document.querySelector(`.mini-progress-dot[data-slide="${num}"]`);
                
                if (dot) {
                    dot.classList.add('medium-gray');
                    console.log(`✅ Slide ${num} marked as medium gray`);
                }
            }
        });
    };
    
    window.clearTooltip = function(slideNumber) {
        if (typeof slideNumber === 'number' && slideNumber >= 1 && slideNumber <= 23) {
            // Find the tooltip element for this slide
            const tooltip = document.querySelector(`.dot-tooltip[data-slide="${slideNumber}"]`);
            
            if (tooltip) {
                tooltip.textContent = '';
                console.log(`✅ Tooltip cleared for slide ${slideNumber}`);
            }
        }
    };
    
    window.clearAllTooltips = function() {
        for (let i = 1; i <= 23; i++) {
            const tooltip = document.querySelector(`.dot-tooltip[data-slide="${i}"]`);
            if (tooltip) {
                tooltip.textContent = '';
            }
        }
        console.log('✅ All tooltips cleared');
    };
    
    window.listCustomization = function() {
        console.log('🎨 Current Customization:');
        console.log('Tooltips:');
        for (let i = 1; i <= 23; i++) {
            const tooltip = document.querySelector(`.dot-tooltip[data-slide="${i}"]`);
            if (tooltip) {
                console.log(`  Slide ${i}: "${tooltip.textContent}"`);
            }
        }
        console.log('Dot Colors:');
        for (let i = 1; i <= 23; i++) {
            const dot = document.querySelector(`.mini-progress-dot[data-slide="${i}"]`);
            if (dot) {
                const bgColor = dot.style.backgroundColor;
                console.log(`  Slide ${i}: ${bgColor}`);
            }
        }
        console.log('');
        console.log('Commands:');
        console.log('  setTooltip(slideNumber, "text") - Set custom tooltip');
        console.log('  setMediumGray(slideNumber, slideNumber, ...) - Mark slides as medium gray');
        console.log('  clearTooltip(slideNumber) - Remove tooltip from slide');
        console.log('  clearAllTooltips() - Remove all tooltips');
        console.log('');
        console.log('Examples:');
        console.log('  setTooltip(5, "Projects")');
        console.log('  setTooltip(11, "Mark Classification Tool")');
        console.log('  setTooltip(12, "Marksheet Generator")');
        console.log('  setTooltip(15, "Autonomy by Design")');
        console.log('  setTooltip(16, "UX Dictionary")');
        console.log('  setTooltip(18, "Definition Quality Scorer")');
    };
});