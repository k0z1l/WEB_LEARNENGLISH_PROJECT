
    let historyDataCache = []; // Cache history for re-rendering on language change

    function renderHistoryTable() {
        const thead = document.getElementById('history-thead');
        const tbody = document.getElementById('history-tbody');
        const emptyState = document.getElementById('history-empty');
        
        tbody.innerHTML = '';

        if (historyDataCache.length === 0) {
            emptyState.classList.remove('hidden');
            thead.classList.add('hidden');
        } else {
            emptyState.classList.add('hidden');
            thead.classList.remove('hidden');
            
            historyDataCache.forEach(item => {
                const dateObj = new Date(item.created_at);
                let dateStr = "Vừa xong";
                let timeStr = "";
                
                if (!isNaN(dateObj.getTime())) {
                    dateStr = dateObj.toLocaleDateString('vi-VN');
                    timeStr = dateObj.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
                }
                
                let badgeHtml = '';
                
                if (item.percentage >= 80) {
                    badgeHtml = `<span class="inline-flex items-center px-3 py-1 text-xs font-black bg-emerald-400 text-black border-2 border-black shadow-[2px_2px_0px_#000] ">${t('badge_excellent')}</span>`;
                } else if (item.percentage >= 50) {
                    badgeHtml = `<span class="inline-flex items-center px-3 py-1 text-xs font-black bg-yellow-300 text-black border-2 border-black shadow-[2px_2px_0px_#000] ">${t('badge_pass')}</span>`;
                } else {
                    badgeHtml = `<span class="inline-flex items-center px-3 py-1 text-xs font-black bg-rose-400 text-black border-2 border-black shadow-[2px_2px_0px_#000] ">${t('badge_try')}</span>`;
                }

                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-100 transition-colors duration-200 group bg-white';
                tr.innerHTML = `
                    <td class="px-10 py-6 border-r-4 border-black">
                        <div class="flex items-center">
                            <div class="w-10 h-10 bg-white border-2 border-black flex items-center justify-center mr-4 shadow-[2px_2px_0px_#000]">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-black" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                            <div>
                                <p class="text-black font-black">${dateStr}</p>
                                <p class="text-black text-xs font-bold mt-0.5">${timeStr}</p>
                            </div>
                        </div>
                    </td>
                    <td class="px-10 py-6 border-r-4 border-black">
                        <div class="flex items-baseline space-x-1">
                            <span class="font-black text-black text-3xl" style="font-family: 'Righteous', cursive;">${item.score}</span>
                            <span class="text-black font-black text-sm">/ ${item.total_questions}</span>
                        </div>
                    </td>
                    <td class="px-10 py-6 border-r-4 border-black">
                        ${badgeHtml}
                    </td>
                    <td class="px-10 py-6 text-right">
                        <span class="font-black text-black bg-white border-2 border-black px-3 py-1 shadow-[2px_2px_0px_#000] text-lg">
                            ${item.percentage}%
                        </span>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        // 1. Thống kê số lượng từ
        const totalWords = parseInt('{{ total_words|default:0 }}');
        
        let learnedCount = 0;
        let reviewCount = totalWords; // Fallback: mặc định bằng tổng số từ
        
        const vocabProgress = JSON.parse(localStorage.getItem('vocab_progress'));
        if (vocabProgress && Array.isArray(vocabProgress.learned)) {
            learnedCount = vocabProgress.learned.length;
            // Tổng số từ cần học = Tổng từ vựng hệ thống - Số từ đã thuộc
            reviewCount = totalWords - learnedCount;
        }
        
        document.getElementById('learned-count').textContent = learnedCount;
        document.getElementById('review-count').textContent = reviewCount;
        
        // 2. Tải và render Lịch sử làm bài
        let backendHistoryStr = '{{ backend_history|escapejs|default:"[]" }}';
        let backendHistory = [];
        try {
            backendHistory = JSON.parse(backendHistoryStr);
        } catch (e) {
            backendHistory = [];
        }
        
        if (Array.isArray(backendHistory) && backendHistory.length > 0) {
            historyDataCache = backendHistory;
        } else {
            let rawHistory = localStorage.getItem('quiz_history');
            try {
                if (rawHistory) {
                    let parsed = JSON.parse(rawHistory);
                    if (Array.isArray(parsed)) {
                        historyDataCache = parsed;
                    }
                }
            } catch (e) {
                console.error('Lỗi parse quiz_history:', e);
                historyDataCache = [];
            }
        }
        
        if (historyDataCache.length > 0) {
            // Chuẩn hóa dữ liệu cũ (Fallback)
            historyDataCache.forEach(item => {
                if (item.percentage === undefined || item.percentage === null) {
                    item.percentage = Math.round((item.score / item.total_questions) * 100) || 0;
                }
                if (!item.created_at) {
                    item.created_at = new Date().toISOString();
                }
            });

            // Sắp xếp mới nhất lên đầu
            historyDataCache.sort((a, b) => {
                const dateA = new Date(a.created_at);
                const dateB = new Date(b.created_at);
                const timeA = isNaN(dateA.getTime()) ? 0 : dateA.getTime();
                const timeB = isNaN(dateB.getTime()) ? 0 : dateB.getTime();
                return timeB - timeA;
            });
        }
        
        renderHistoryTable();
    });

    // Cập nhật lại UI bảng (badge) khi đổi ngôn ngữ
    document.addEventListener('languageChanged', (e) => {
        renderHistoryTable();
    });
