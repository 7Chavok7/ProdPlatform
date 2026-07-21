# /apps/core/admin.py | A.Grachev | 20.07.2026
from django.contrib import admin
from django.utils.html import format_html
from .models import Drawing, Notification


@admin.register(Drawing)
class DrawingAdmin(admin.ModelAdmin):
    """
    Админка для модели 'Чертежи'
    """

    # Что показываем в списке
    list_display = [
        'name',
        'file_type',
        'version',
        'uploaded_by',  # Кто загрузил
        'uploaded_at',  # Когда загрузил
        'updated_at',
        'is_active'
    ]

    # Фильтры
    list_filter = [
        'file_type',
        'is_active',
        'uploaded_at'
    ]

    # Поиск
    search_fields = [
        'name',
        'description',
        'uploaded_by__username'
    ]

    # Порядок сортировки
    ordering = ['-uploaded_at']

    # Поля только для чтения
    readonly_fields = [
        'uploaded_at',
        'updated_at',
        'preview'
    ]

    # Группировка полей
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'file', 'file_type', 'version')
        }),
        ('Описание', {
            'fields': ('description',)
        }),
        ('Кто загрузил', {
            'fields': ('uploaded_by',)
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Метаданные', {
            'fields': ('uploaded_at', 'updated_at', 'preview'),
            'classes': ('collapse',)
        }),
    )

    def preview(self, obj):
        """Показывает превью файла"""
        if obj.file_type == 'image':
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 4px;"/>',
                obj.file.url
            )
        elif obj.file_type == 'pdf':
            return format_html(
                '<i class="fas fa-file-pdf" style="font-size: 24px; color: #dc3545;"></i> PDF'
            )

        # !!!!! Добавить сюда остальные форматы и способы отображения в зависимости от формата
        return format_html(
            '<i class="fas fa-file" style="font-size: 24px; color: #6c757d;"></i>'
        )
    preview.short_description = 'Превью'

    # Действия
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        """Активировать выбранные чертежи"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} чертежей автивированно.')
    make_active.short_description = 'Активировать выбранные чертежи'

    def make_inactive(self, request, queryset):
        """Деактевировать выбранные чертежи"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} чертежей деактевированно.')
    make_inactive.short_description = 'Деактевировать выбранные чертежи'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Админка для модели 'Уведомления'
    """
    
    # Что показываем в списке
    list_display = [
        'title',
        'user',
        'type',
        'is_read',
        'created_at'
    ]
    
    # Фильтры
    list_filter = [
        'type',
        'is_read',
        'created_at'
    ]
    
    # Поиск
    search_fields = [
        'title',
        'message',
        'user__username'
    ]
    
    # Поля только для чтения
    readonly_fields = ['created_at']
    
    # Сортировка
    ordering = ['-created_at']
    
    # Группировка полей
    fieldsets = (
        ('Информация', {
            'fields': ('title', 'message', 'type',)
        }),
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Статус', {
            'fields': ('is_read', 'read_at',)
        }),
        ('Ссылка', {
            'fields': ('link',)
        }),
        ('Метаданные', {
            'fields': ('created_at',)
        }),
    )