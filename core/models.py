from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Tên chủ đề")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Word(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='words', help_text="Chủ đề của từ vựng")
    english_word = models.CharField(max_length=100, help_text="Từ vựng tiếng Anh")
    pronunciation = models.CharField(max_length=100, blank=True, null=True, help_text="Phiên âm quốc tế IPA")
    part_of_speech = models.CharField(max_length=50, help_text="Loại từ: Noun, Verb, Adj...")
    vietnamese_meaning = models.CharField(max_length=255, help_text="Nghĩa tiếng Việt")
    example_sentence = models.TextField(blank=True, null=True, help_text="Câu ví dụ")
    example_meaning = models.TextField(blank=True, null=True, help_text="Nghĩa tiếng Việt của câu ví dụ")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.english_word} ({self.part_of_speech})"

class UserWord(models.Model):
    STATUS_CHOICES = [
        ('LEARNED', 'Đã thuộc'),
        ('REVIEW', 'Cần học lại'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_words')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='user_status')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REVIEW')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Đảm bảo mỗi user chỉ có 1 trạng thái cho mỗi từ
        unique_together = ('user', 'word')

    def __str__(self):
        return f"{self.user.username} - {self.word.english_word} - {self.get_status_display()}"

class QuizHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_histories')
    score = models.IntegerField()
    total_questions = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total_questions}"
