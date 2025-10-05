document.addEventListener('DOMContentLoaded', function() {
    // Инициализация редакторов кода
    document.querySelectorAll('.code-editor').forEach(function(textarea) {
        CodeMirror.fromTextArea(textarea, {
            mode: 'python',
            theme: 'monokai',
            lineNumbers: true,
            indentUnit: 4,
            tabSize: 4,
            indentWithTabs: false,
            lineWrapping: true
        });
    });

    // Прогресс
    const progressText = document.getElementById('progress-text');
    const totalQuestions = parseInt(progressText.dataset.total);
    const progressFill = document.getElementById('progress-fill');

    function updateProgress() {
        const answeredQuestions = new Set();
        
        document.querySelectorAll('input[type="radio"]:checked').forEach(function(radio) {
            answeredQuestions.add(radio.name);
        });
        
        document.querySelectorAll('.CodeMirror').forEach(function(cm) {
            const editor = cm.CodeMirror;
            if (editor.getValue().trim().length > 10) {
                const textarea = editor.getTextArea();
                answeredQuestions.add(textarea.name);
            }
        });
        
        const answered = answeredQuestions.size;
        const percentage = (answered / totalQuestions) * 100;
        
        progressFill.style.width = percentage + '%';
        progressText.textContent = 'Отвечено на ' + answered + ' из ' + totalQuestions + ' вопросов';
    }

    document.querySelectorAll('input[type="radio"]').forEach(function(radio) {
        radio.addEventListener('change', updateProgress);
    });

    setInterval(updateProgress, 1000);
});

// Таймер
const timerElement = document.getElementById('timer-value');
const timerContainer = document.getElementById('timer');
const form = document.getElementById('test-form');
const timeLimitMinutes = parseInt(document.getElementById('timer').dataset.timeLimit);
let timeLeft = timeLimitMinutes * 60;
let timerInterval;

function updateTimer() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    timerElement.textContent = minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
    
    if (timeLeft <= 60) {
        timerContainer.classList.add('warning');
    }
    
    if (timeLeft <= 0) {
        clearInterval(timerInterval);
        alert('⏰ Время истекло! Тест будет отправлен автоматически.');
        form.submit();
        return;
    }
    
    timeLeft--;
}

if (timeLimitMinutes > 0) {
    updateTimer();
    timerInterval = setInterval(updateTimer, 1000);
}

// Синхронизация CodeMirror с textarea перед отправкой
form.addEventListener('submit', function(e) {
    document.querySelectorAll('.CodeMirror').forEach(function(cm) {
        cm.CodeMirror.save();
    });
});

// Предупреждение при уходе
let formSubmitted = false;
window.addEventListener('beforeunload', function(e) {
    if (!formSubmitted) {
        e.preventDefault();
        e.returnValue = '';
    }
});

form.addEventListener('submit', function() {
    formSubmitted = true;
});