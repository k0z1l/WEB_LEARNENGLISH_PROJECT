from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Word, UserWord, QuizHistory

@admin.register(Word)
class WordAdmin(ModelAdmin):
    list_display = ('english_word', 'part_of_speech_badge', 'vietnamese_meaning', 'created_at')
    search_fields = ('english_word', 'vietnamese_meaning')
    list_filter = ('part_of_speech',)
    
    # Trả về tuple (giá trị, màu_sắc) cho Unfold label
    @display(description="Loại từ", label=True)
    def part_of_speech_badge(self, obj):
        return (obj.part_of_speech, "info")

@admin.register(UserWord)
class UserWordAdmin(ModelAdmin):
    list_display = ('user', 'word', 'display_status', 'updated_at')
    list_filter = ('status', 'user')

    # Trả về tuple (giá trị, màu_sắc) cho Unfold label
    @display(description="Trạng thái", label=True)
    def display_status(self, obj):
        if obj.status == 'LEARNED':
            return ("Đã thuộc", "success")
        return ("Cần học lại", "danger")

@admin.register(QuizHistory)
class QuizHistoryAdmin(ModelAdmin):
    list_display = ('user', 'score_display', 'total_questions', 'created_at')
    
    @display(description="Điểm đạt được", label=True)
    def score_display(self, obj):
        # Có thể dùng màu primary/info cho điểm số
        return (f"{obj.score} điểm", "primary")
