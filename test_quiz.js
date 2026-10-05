
    let quizData = JSON.parse('{{ quiz_data_json|escapejs }}');
    let currentQuestionIndex = 0;
    let score = 0;
    let isAnswered = false;

    const csrfToken = "{{ csrf_token }}";
    
    // DOM Elements
    const qWord = document.getElementById('question-word');
    const qPron = document.getElementById('question-pron');
    const optionsContainer = document.getElementById('options-container');
    const currentQNum = document.getElementById('current-q-num');
    const totalQNum = document.getElementById('total-q-num');
    const scoreDisplay = document.getElementById('score-display');
    const progressBar = document.getElementById('progress-bar');
    const nextBtnContainer = document.getElementById('next-btn-container');
    const quizContainer = document.getElementById('quiz-container');
    const resultsScreen = document.getElementById('results-screen');

    function loadQuestion() {
        if (quizData.length === 0) return;
        
        isAnswered = false;
        const q = quizData[currentQuestionIndex];
        
        // Update UI
        qWord.textContent = q.english_word;
        qPron.textContent = q.pronunciation ? `/${q.pronunciation}/` : '';
        currentQNum.textContent = currentQuestionIndex + 1;
        totalQNum.textContent = quizData.length;
        progressBar.style.width = `${((currentQuestionIndex) / quizData.length) * 100}%`;
        
        nextBtnContainer.classList.add('opacity-0');
        nextBtnContainer.classList.add('pointer-events-none');
        
        // Render Options
        optionsContainer.innerHTML = '';
        q.options.forEach((opt, index) => {
            const btn = document.createElement('button');
            btn.className = `option-btn w-full p-5 text-left bg-white border-4 border-black text-black font-black shadow-[4px_4px_0px_#000] hover:translate-x-1 hover:translate-y-1 hover:shadow-none hover:bg-slate-100 transition-all focus:outline-none flex items-center relative`;
            btn.innerHTML = `<span class="inline-flex items-center justify-center w-8 h-8 bg-black text-white text-sm font-black mr-4">${String.fromCharCode(65 + index)}</span> <span>${opt.text}</span>`;
            btn.onclick = () => selectOption(btn, opt.is_correct);
            optionsContainer.appendChild(btn);
        });
    }

    function selectOption(selectedBtn, isCorrect) {
        if (isAnswered) return;
        isAnswered = true;
        
        const allBtns = document.querySelectorAll('.option-btn');
        allBtns.forEach(btn => {
            btn.classList.remove('hover:translate-x-1', 'hover:translate-y-1', 'hover:shadow-none', 'hover:bg-slate-100', 'cursor-pointer');
            btn.classList.add('opacity-50', 'cursor-default');
            btn.onclick = null;
        });
        
        selectedBtn.classList.remove('opacity-50', 'bg-white');
        
        if (isCorrect) {
            selectedBtn.classList.add('bg-emerald-400');
            score++;
            scoreDisplay.textContent = score;
        } else {
            selectedBtn.classList.add('bg-rose-400');
            
            // Highlight the correct one
            const correctIndex = quizData[currentQuestionIndex].options.findIndex(o => o.is_correct);
            const correctBtn = allBtns[correctIndex];
            correctBtn.classList.remove('opacity-50', 'bg-white');
            correctBtn.classList.add('bg-emerald-400', 'border-dashed');
        }
        
        // Show next button
        nextBtnContainer.classList.remove('opacity-0', 'pointer-events-none');
    }

    function nextQuestion() {
        if (currentQuestionIndex < quizData.length - 1) {
            currentQuestionIndex++;
            loadQuestion();
        } else {
            finishQuiz();
        }
    }

    function finishQuiz() {
        progressBar.style.width = '100%';
        quizContainer.classList.add('hidden');
        resultsScreen.classList.remove('hidden');
        
        document.getElementById('final-score').textContent = score;
        document.getElementById('final-total').textContent = quizData.length;

        const percentage = Math.round((score / quizData.length) * 100);

        // Lưu vào LocalStorage an toàn
        let rawHistory = localStorage.getItem('quiz_history');
        let history = [];
        try {
            if (rawHistory) {
                let parsed = JSON.parse(rawHistory);
                if (Array.isArray(parsed)) {
                    history = parsed;
                }
            }
        } catch (e) {
            console.error('Lỗi parse quiz_history:', e);
            history = []; // Reset nếu lỗi
        }

        history.push({
            score: Number(score),
            total_questions: Number(quizData.length),
            percentage: Number(percentage),
            created_at: new Date().toISOString()
        });
        
        localStorage.setItem('quiz_history', JSON.stringify(history));

        // Sync Backend
        fetch('/api/quiz/save/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrfToken},
            body: JSON.stringify({score: score, total_questions: quizData.length})
        }).catch(err => console.error('Lỗi khi lưu điểm:', err));
    }

    // Lọc theo Topic qua API
    function filterQuizByTopic() {
        const topicId = document.getElementById('topic-filter').value;
        
        document.getElementById('quiz-container').classList.add('hidden');
        document.getElementById('results-screen').classList.add('hidden');
        document.getElementById('empty-state').classList.add('hidden');
        document.getElementById('quiz-loading').classList.remove('hidden');

        fetch(`/api/quiz/generate/?topic_id=${topicId}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById('quiz-loading').classList.add('hidden');
                if (data.success) {
                    quizData = data.quiz_data;
                    currentQuestionIndex = 0;
                    score = 0;
                    scoreDisplay.textContent = 0;
                    document.getElementById('quiz-container').classList.remove('hidden');
                    loadQuestion();
                } else {
                    document.getElementById('empty-state').classList.remove('hidden');
                    const emptyMsgEl = document.getElementById('empty-msg');
                    
                    if (data.error === 'Chủ đề này chưa có từ vựng nào.') {
                        emptyMsgEl.dataset.errorKey = 'msg_empty_topic';
                        emptyMsgEl.textContent = t('msg_empty_topic');
                    } else if (data.error === 'Hệ thống cần ít nhất 4 từ vựng để tạo bài Quiz.') {
                        emptyMsgEl.dataset.errorKey = 'quiz_error_desc';
                        emptyMsgEl.textContent = t('quiz_error_desc');
                    } else {
                        emptyMsgEl.dataset.errorKey = '';
                        emptyMsgEl.textContent = data.error;
                    }
                }
            })
            .catch(err => {
                document.getElementById('quiz-loading').classList.add('hidden');
                alert(t('msg_quiz_load_err'));
            });
    }

    document.addEventListener('languageChanged', (e) => {
        // Cập nhật lại empty msg nếu có
        const emptyMsgEl = document.getElementById('empty-msg');
        if (emptyMsgEl && emptyMsgEl.dataset.errorKey) {
            emptyMsgEl.textContent = t(emptyMsgEl.dataset.errorKey);
        }
    });

    // Init
    loadQuestion();
