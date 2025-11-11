// ============================================
// DEFINITION QUALITY SCORER
// ============================================

const UX_TERMS = ['usability', 'accessibility', 'wireframe', 'prototype', 'user interface', 'ui', 'ux', 'user experience', 'interaction design', 'information architecture', 'user research', 'user testing', 'heuristic', 'affordance', 'persona', 'user journey', 'user flow', 'sitemap', 'navigation', 'mockup', 'storyboard', 'user-centered', 'a/b testing', 'conversion', 'responsive', 'iteration', 'ideation', 'empathy map', 'pain point', 'stakeholder'];
const ABSTRACT_TERMS = ['concept', 'theory', 'methodology', 'approach', 'framework', 'principle', 'strategy', 'philosophy', 'paradigm', 'perspective', 'insight', 'innovation', 'creativity', 'abstraction', 'ideation', 'intuition', 'perception', 'cognition', 'evaluation', 'analysis', 'synthesis', 'process', 'quality', 'value', 'experience', 'engagement', 'interaction', 'satisfaction', 'emotional', 'psychological'];
const CONCRETE_TERMS = ['button', 'screen', 'device', 'click', 'tap', 'layout', 'menu', 'icon', 'link', 'page', 'scroll', 'swipe', 'keyboard', 'mouse', 'touch', 'display', 'image', 'video', 'audio', 'text', 'font', 'color', 'size', 'shape', 'position', 'desktop', 'mobile', 'tablet', 'app', 'website', 'interface', 'component', 'element'];
const PASSIVE_MARKERS = ['is used', 'are used', 'was used', 'were used', 'is created', 'are created', 'was created', 'were created', 'is defined', 'are defined', 'was defined', 'were defined', 'is designed', 'are designed', 'was designed', 'were designed', 'is developed', 'are developed', 'was developed', 'were developed', 'is implemented', 'are implemented', 'was implemented', 'were implemented', 'is built', 'are built', 'was built', 'were built', 'is made', 'are made', 'was made', 'were made'];

function calculateScore(text) {
    if (!text.trim()) return 0;
    
    const readability = calculateReadability(text);
    const clarity = analyzeClarity(text);
    const jargon = analyzeJargon(text);
    const structure = analyzeSentenceStructure(text);
    const balance = analyzeConcreteAbstract(text);
    const voice = analyzeActivePassive(text);
    
    return Math.round(readability * 0.15 + clarity * 0.25 + jargon * 0.15 + structure * 0.15 + balance * 0.15 + voice * 0.15);
}

function calculateReadability(text) {
    const sentences = text.split(/[.!?]+/).filter(s => s.trim());
    const words = text.split(/\s+/).filter(w => w.match(/[A-Za-z]/));
    
    if (sentences.length === 0 || words.length === 0) return 0;
    
    let syllables = 0;
    words.forEach(word => {
        syllables += countSyllables(word);
    });
    
    const gradeLevel = 0.39 * (words.length / sentences.length) + 11.8 * (syllables / words.length) - 15.59;
    return Math.max(0, Math.min(100, 100 - Math.abs(gradeLevel - 10) * 5));
}

function countSyllables(word) {
    word = word.toLowerCase().replace(/[^a-z]/g, '');
    if (word.length <= 3) return 1;
    
    const vowels = 'aeiouy';
    let count = 0;
    let prevVowel = false;
    
    for (let i = 0; i < word.length; i++) {
        const isVowel = vowels.includes(word[i]);
        if (isVowel && !prevVowel) count++;
        prevVowel = isVowel;
    }
    
    if (word.endsWith('e') && count > 1) count--;
    return Math.max(1, count);
}

function analyzeClarity(text) {
    const sentences = text.split(/[.!?]+/).filter(s => s.trim());
    const words = text.match(/\b\w+\b/g) || [];
    
    let longSentences = 0;
    sentences.forEach(sentence => {
        const sentenceWords = sentence.match(/\b\w+\b/g) || [];
        if (sentenceWords.length > 25) longSentences++;
    });
    
    const longWords = words.filter(word => word.length > 8).length;
    const longSentencePercent = sentences.length > 0 ? (longSentences / sentences.length) * 100 : 0;
    const longWordPercent = words.length > 0 ? (longWords / words.length) * 100 : 0;
    
    let score = 100;
    if (longSentencePercent > 0) score -= longSentencePercent * 2;
    if (longWordPercent > 15) score -= (longWordPercent - 15) * 1.5;
    
    return Math.max(0, Math.min(100, score));
}

function analyzeJargon(text) {
    const lowerText = text.toLowerCase();
    const words = text.match(/\b\w+\b/g) || [];
    
    const jargonCount = UX_TERMS.filter(term => lowerText.includes(term)).length;
    const jargonPercent = words.length > 0 ? (jargonCount / words.length) * 100 : 0;
    
    let score = 0;
    if (jargonPercent <= 5) {
        score = jargonPercent * 10;
    } else if (jargonPercent <= 20) {
        score = 100 - Math.abs(jargonPercent - 15) * 3;
    } else {
        score = Math.max(0, 100 - (jargonPercent - 20) * 4);
    }
    
    return Math.max(0, Math.min(100, score));
}

function analyzeSentenceStructure(text) {
    const sentences = text.split(/[.!?]+/).filter(s => s.trim());
    if (sentences.length === 0) return 0;
    
    let totalComplexity = 0;
    sentences.forEach(sentence => {
        const conjunctions = (sentence.match(/\b(and|but|or|yet|so|for|nor|because|if|when|while|although|since)\b/gi) || []).length;
        const relativeClauses = (sentence.match(/\b(that|which|who|whom|whose)\b/gi) || []).length;
        const clauses = 1 + conjunctions + relativeClauses;
        const words = (sentence.match(/\b\w+\b/g) || []).length;
        totalComplexity += words / Math.max(1, clauses);
    });
    
    const avgComplexity = totalComplexity / sentences.length;
    
    let score = 0;
    if (avgComplexity < 8) {
        score = avgComplexity * 10;
    } else if (avgComplexity <= 15) {
        score = 100 - Math.abs(avgComplexity - 12) * 5;
    } else {
        score = Math.max(0, 100 - (avgComplexity - 15) * 8);
    }
    
    return Math.max(0, Math.min(100, score));
}

function analyzeConcreteAbstract(text) {
    const lowerText = text.toLowerCase();
    
    const concreteCount = CONCRETE_TERMS.filter(term => lowerText.includes(term)).length;
    const abstractCount = ABSTRACT_TERMS.filter(term => lowerText.includes(term)).length;
    
    if (concreteCount === 0 && abstractCount === 0) return 0;
    
    const ratio = abstractCount > 0 ? concreteCount / abstractCount : (concreteCount > 0 ? 3 : 1);
    
    let score = 0;
    if (ratio === 0) {
        score = 40;
    } else if (ratio < 0.5) {
        score = 40 + ratio * 60;
    } else if (ratio <= 2.5) {
        score = 100 - Math.abs(ratio - 1.5) * 20;
    } else {
        score = Math.max(40, 100 - (ratio - 2.5) * 15);
    }
    
    return Math.max(0, Math.min(100, score));
}

function analyzeActivePassive(text) {
    const sentences = text.split(/[.!?]+/).filter(s => s.trim());
    if (sentences.length === 0) return 0;
    
    let passiveCount = 0;
    sentences.forEach(sentence => {
        const lowerSentence = sentence.toLowerCase();
        for (let marker of PASSIVE_MARKERS) {
            if (lowerSentence.includes(marker)) {
                passiveCount++;
                break;
            }
        }
    });
    
    const passivePercent = (passiveCount / sentences.length) * 100;
    
    let score = 0;
    if (passivePercent <= 20) {
        score = 100 - passivePercent * 1.5;
    } else if (passivePercent <= 50) {
        score = 70 - (passivePercent - 20) * 1.3;
    } else {
        score = Math.max(0, 30 - (passivePercent - 50));
    }
    
    return Math.max(0, Math.min(100, score));
}

function updateDefinition(textareaId, counterId, scoreId, progressId) {
    const textarea = document.getElementById(textareaId);
    const counter = document.getElementById(counterId);
    const scoreElement = document.getElementById(scoreId);
    const progress = document.getElementById(progressId);
    
    if (!textarea || !counter || !scoreElement || !progress) return;
    
    const text = textarea.value;
    const length = text.length;
    const score = calculateScore(text);
    
    // Update character counter
    counter.textContent = `${length} / 155 characters`;
    if (length > 155) {
        counter.classList.add('warning');
    } else {
        counter.classList.remove('warning');
    }
    
    // Update score
    scoreElement.textContent = score;
    
    // Update progress bar
    progress.style.width = score + '%';
    
    // color + classes
    progress.classList.remove('low','medium','good');
    scoreElement.classList.remove('low','medium','good');
    
    if (score < 50) {
        progress.classList.add('low');
        scoreElement.classList.add('low');
        progress.style.backgroundColor = '#ef4444'; // Red
    } else if (score < 70) {
        progress.classList.add('medium');
        scoreElement.classList.add('medium');
        progress.style.backgroundColor = '#f59e0b'; // Yellow
    } else {
        progress.classList.add('good');
        scoreElement.classList.add('good');
        progress.style.backgroundColor = '#0f7938'; // Deep green
    }
}

// Initialize definition scorer
function initDefinitionScorer() {
    // Check if we're on the correct slide
    if (!document.querySelector('[data-section="3"][data-slide="3"]')) return;
    
    // Get textareas
    const def1 = document.getElementById('definition1');
    const def2 = document.getElementById('definition2');
    
    if (!def1 || !def2) return;
    
    // Add event listeners
    def1.addEventListener('input', () => {
        updateDefinition('definition1', 'counter1', 'score1', 'progress1');
    });
    
    def2.addEventListener('input', () => {
        updateDefinition('definition2', 'counter2', 'score2', 'progress2');
    });
    
    // Initialize with current values
    updateDefinition('definition1', 'counter1', 'score1', 'progress1');
    updateDefinition('definition2', 'counter2', 'score2', 'progress2');
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initDefinitionScorer);