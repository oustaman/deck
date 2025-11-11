// ============================================
// MARK CLASSIFICATION TOOL
// ============================================

const gradeScale = [
    { mark: 100, ug: "Exceptional", pgt: "Exceptional", singapore: "A+", gpa: "5.0" },
    { mark: 95, ug: "", pgt: "", singapore: "A+", gpa: "5.0" },
    { mark: 90, ug: "Outstanding", pgt: "Outstanding", singapore: "A+", gpa: "5.0" },
    { mark: 85, ug: "Very high 1st", pgt: "Very high distinction", singapore: "A+", gpa: "4.5" },
    { mark: 78, ug: "High 1st", pgt: "High distinction", singapore: "A", gpa: "4.5" },
    { mark: 75, ug: "Mid 1st", pgt: "Mid distinction", singapore: "A", gpa: "4.5" },
    { mark: 72, ug: "Low 1st", pgt: "Low distinction", singapore: "A", gpa: "4.0" },
    { mark: 68, ug: "High 2.1", pgt: "High merit", singapore: "A-", gpa: "4.0" },
    { mark: 65, ug: "Mid 2.1", pgt: "Mid merit", singapore: "A-", gpa: "4.0" },
    { mark: 62, ug: "Low 2.1", pgt: "Low merit", singapore: "B+", gpa: "3.5" },
    { mark: 58, ug: "High 2.2", pgt: "High pass", singapore: "B+", gpa: "3.5" },
    { mark: 55, ug: "Mid 2.2", pgt: "Mid pass", singapore: "B", gpa: "3.0" },
    { mark: 52, ug: "Low 2.2", pgt: "Low pass", singapore: "B", gpa: "3.0" },
    { mark: 48, ug: "High 3rd", pgt: "Marginal fail", singapore: "B-", gpa: "3.0" },
    { mark: 45, ug: "Mid 3rd", pgt: "", singapore: "B-", gpa: "2.5" },
    { mark: 42, ug: "Low 3rd", pgt: "", singapore: "C+", gpa: "2.5" },
    { mark: 38, ug: "Marginal fail", pgt: "Clear fail", singapore: "C", gpa: "2.0" },
    { mark: 35, ug: "", pgt: "", singapore: "C", gpa: "2.0" },
    { mark: 32, ug: "", pgt: "", singapore: "C-", gpa: "2.0" },
    { mark: 28, ug: "Clear fail", pgt: "", singapore: "D+", gpa: "1.5" },
    { mark: 25, ug: "", pgt: "", singapore: "D", gpa: "1.5" },
    { mark: 22, ug: "", pgt: "", singapore: "D", gpa: "1.5" },
    { mark: 18, ug: "", pgt: "", singapore: "D-", gpa: "1.0" },
    { mark: 15, ug: "", pgt: "", singapore: "F", gpa: "1.0" },
    { mark: 12, ug: "", pgt: "", singapore: "F", gpa: "0.5" },
    { mark: 8, ug: "Low fail", pgt: "Low fail", singapore: "F", gpa: "0.5" },
    { mark: 5, ug: "", pgt: "", singapore: "F", gpa: "0.0" },
    { mark: 2, ug: "", pgt: "", singapore: "F", gpa: "0.0" },
    { mark: 0, ug: "Non-engagement", pgt: "Non-engagement", singapore: "F", gpa: "0.0" }
];

// Global variables for mark classification tool
let currentIntervalValue = 3.0; // Pre-set to 3.0
let currentAdjustmentType = 'percentage';

// Mark classification tool functions
function calculateAdjustedMark(originalMark, adjustmentInfo) {
    let adjustedMark = originalMark;
    
    if (adjustmentInfo.value === 0) {
        return originalMark;
    }
    
    if (adjustmentInfo.type === 'percentage') {
        const adjustment = originalMark * (adjustmentInfo.value / 100);
        if (adjustmentInfo.direction === 'increase') {
            adjustedMark = originalMark + adjustment;
        } else {
            adjustedMark = originalMark - adjustment;
        }
    } else if (adjustmentInfo.type === 'absolute') {
        if (adjustmentInfo.direction === 'increase') {
            adjustedMark = originalMark + adjustmentInfo.value;
        } else {
            adjustedMark = originalMark - adjustmentInfo.value;
        }
    }
    
    // Ensure mark stays within 0-100 range
    adjustedMark = Math.max(0, Math.min(100, adjustedMark));
    
    return adjustedMark;
}

function snapToNearestBoundary(mark) {
    let nearestBoundary = gradeScale[0].mark;
    let minDifference = Math.abs(mark - nearestBoundary);
    
    for (let i = 1; i < gradeScale.length; i++) {
        const difference = Math.abs(mark - gradeScale[i].mark);
        if (difference < minDifference) {
            minDifference = difference;
            nearestBoundary = gradeScale[i].mark;
        }
    }
    
    return nearestBoundary;
}

function getClassification(mark, type) {
    for (let i = 0; i < gradeScale.length; i++) {
        if (mark >= gradeScale[i].mark) {
            return type === 'ug' ? gradeScale[i].ug : gradeScale[i].pgt;
        }
    }
    return "Unknown";
}

function getSingaporeGrade(mark) {
    for (let i = 0; i < gradeScale.length; i++) {
        if (mark >= gradeScale[i].mark) {
            return gradeScale[i].singapore;
        }
    }
    return "Unknown";
}

function getGPA(mark) {
    for (let i = 0; i < gradeScale.length; i++) {
        if (mark >= gradeScale[i].mark) {
            return gradeScale[i].gpa;
        }
    }
    return "Unknown";
}

function populateGradeScaleTable(adjustmentInfo = null) {
    const tbody = document.getElementById('grade-scale-body');
    
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    const hasAdjustment = adjustmentInfo && adjustmentInfo.value !== 0;
    
    // Iterate through gradeScale array to show only stepped marks
    gradeScale.forEach(grade => {
        const row = document.createElement('tr');
        
        // Get original values
        const originalMark = grade.mark;
        const originalUG = grade.ug || '-';
        const originalPGT = grade.pgt || '-';
        const originalSingapore = grade.singapore;
        const originalGPA = grade.gpa;
        
        // Calculate adjusted values if there's an adjustment
        let adjustedMark = originalMark;
        let adjustedGrade = grade;
        
        if (hasAdjustment) {
            adjustedMark = calculateAdjustedMark(originalMark, adjustmentInfo);
            adjustedMark = snapToNearestBoundary(adjustedMark);
            
            // Find grade data for adjusted mark
            for (let i = 0; i < gradeScale.length; i++) {
                if (adjustedMark >= gradeScale[i].mark) {
                    adjustedGrade = gradeScale[i];
                    break;
                }
            }
        }
        
        const adjustedUG = adjustedGrade.ug || '-';
        const adjustedPGT = adjustedGrade.pgt || '-';
        const adjustedSingapore = adjustedGrade.singapore;
        const adjustedGPA = adjustedGrade.gpa;
        
        // UK Marks cell
        const markCell = document.createElement('td');
        markCell.className = 'px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-100';
        
        if (hasAdjustment && Math.abs(adjustedMark - originalMark) > 0.01) {
            markCell.innerHTML = `${originalMark} <span class="text-blue-700 dark:text-blue-300">→ ${adjustedMark.toFixed(0)}</span>`;
            markCell.classList.add('bg-yellow-50', 'dark:bg-yellow-900');
        } else {
            markCell.textContent = originalMark;
        }
        row.appendChild(markCell);
        
        // UG Classification cell
        const ugCell = document.createElement('td');
        ugCell.className = 'px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100';
        
        if (hasAdjustment && originalUG !== adjustedUG) {
            ugCell.innerHTML = `${originalUG} <span class="text-blue-700 dark:text-blue-300">→ ${adjustedUG}</span>`;
            ugCell.classList.add('bg-yellow-50', 'dark:bg-yellow-900');
        } else {
            ugCell.textContent = originalUG;
        }
        row.appendChild(ugCell);
        
        // PGT Classification cell
        const pgtCell = document.createElement('td');
        pgtCell.className = 'px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100';
        
        if (hasAdjustment && originalPGT !== adjustedPGT) {
            pgtCell.innerHTML = `${originalPGT} <span class="text-blue-700 dark:text-blue-300">→ ${adjustedPGT}</span>`;
            pgtCell.classList.add('bg-yellow-50', 'dark:bg-yellow-900');
        } else {
            pgtCell.textContent = originalPGT;
        }
        row.appendChild(pgtCell);
        
        // Singapore Grade cell
        const singaporeCell = document.createElement('td');
        singaporeCell.className = 'px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100';
        
        if (hasAdjustment && originalSingapore !== adjustedSingapore) {
            singaporeCell.innerHTML = `${originalSingapore} <span class="text-blue-700 dark:text-blue-300">→ ${adjustedSingapore}</span>`;
            singaporeCell.classList.add('bg-yellow-50', 'dark:bg-yellow-900');
        } else {
            singaporeCell.textContent = originalSingapore;
        }
        row.appendChild(singaporeCell);
        
        // GPA cell
        const gpaCell = document.createElement('td');
        gpaCell.className = 'px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100';
        
        if (hasAdjustment && originalGPA !== adjustedGPA) {
            gpaCell.innerHTML = `${originalGPA} <span class="text-blue-700 dark:text-blue-300">→ ${adjustedGPA}</span>`;
            gpaCell.classList.add('bg-yellow-50', 'dark:bg-yellow-900');
        } else {
            gpaCell.textContent = originalGPA;
        }
        row.appendChild(gpaCell);
        
        tbody.appendChild(row);
    });
}

function updateResults() {
    const currentIntervalDisplay = document.getElementById('current-interval');
    
    if (!currentIntervalDisplay) return;
    
    // Create adjustment info object using current interval value
    const adjustmentInfo = {
        type: currentAdjustmentType,
        value: Math.abs(currentIntervalValue),
        direction: currentIntervalValue >= 0 ? 'increase' : 'decrease',
        snapToBoundary: true // Always snap to boundaries
    };
    
    // Update interval display
    currentIntervalDisplay.textContent = currentIntervalValue.toFixed(1);
    
    // Update grade scale table with adjustments
    populateGradeScaleTable(adjustmentInfo);
}

// Initialize mark classification tool
function initMarkClassificationTool() {
    // Check if we're on the correct slide
    if (!document.querySelector('[data-section="2"][data-slide="0"]')) return;
    
    // Initialize table
    populateGradeScaleTable();
    
    // Setup toggle controls
    const toggle = document.getElementById('adjustment-toggle');
    const toggleOptions = toggle.querySelectorAll('.toggle-option');
    
    toggleOptions.forEach(option => {
        option.addEventListener('click', function() {
            toggleOptions.forEach(opt => {
                opt.classList.remove('active');
                opt.setAttribute('aria-checked', 'false');
            });
            this.classList.add('active');
            this.setAttribute('aria-checked', 'true');
            
            currentAdjustmentType = this.getAttribute('data-value');
            
            if (currentAdjustmentType === 'absolute') {
                toggle.classList.add('active');
            } else {
                toggle.classList.remove('active');
            }
            
            updateResults();
        });
    });
    
    // Setup interval controls
    const increaseButton = document.getElementById('increase-interval');
    const decreaseButton = document.getElementById('decrease-interval');
    
    if (increaseButton) {
        increaseButton.addEventListener('click', function() {
            currentIntervalValue += 0.5;
            updateResults();
        });
    }
    
    if (decreaseButton) {
        decreaseButton.addEventListener('click', function() {
            currentIntervalValue -= 0.5;
            updateResults();
        });
    }
    
    // Initialize display
    updateResults();
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initMarkClassificationTool);