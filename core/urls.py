from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('flashcard/', views.flashcard_view, name='flashcard'),
    path('api/word/status/', views.update_word_status, name='update_word_status'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('api/quiz/generate/', views.api_quiz_generate, name='api_quiz_generate'),
    path('api/quiz/save/', views.save_quiz_history, name='save_quiz'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('manage/', views.manage_words_view, name='manage_words'),
    path('api/word/save/', views.api_save_word, name='api_save_word'),
    path('api/word/delete/', views.api_delete_word, name='api_delete_word'),
    path('api/word/import/', views.api_import_words, name='api_import_words'),
    path('api/topic/save/', views.api_save_topic, name='api_save_topic'),
    path('api/word/check-grammar/', views.api_check_grammar, name='api_check_grammar'),
    path('api/word/generate-file/', views.api_generate_vocab_file, name='api_generate_vocab_file'),
]
