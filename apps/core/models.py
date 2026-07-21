# /apps/core/models.py | A.Grachev | 20.07.2026
import os
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


class Drawing(models.Model):
    """
    Модель для хранения чертежей и файлов.
    Используется во всех приложениях (заказы, этапы)
    """
    
    class FileType(models.TextChoices):
        PDF = 'pdf', 'PDF'
        IMAGE = 'image', 'Изображение'
        DWG = 'dwg', 'DWG (Autocad)'
        
        
    # ===== Основные поля =====
    name = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    file = models.FileField(
        upload_to='drawings/%Y/%m',
        verbose_name='Файл'
    )
    file_type = models.CharField(
        max_length=10,
        choices=FileType.choices,
        verbose_name='Тип файла'
    )
    version = models.PositiveIntegerField(
        default=1,
        verbose_name='Версия'
    )
    
    # ===== Описание =====
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    
    # ===== Статус =====
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    
    # ===== Связи =====
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='uploaded_drawings',
        verbose_name='Загрузил'
    )
    
    # ===== Даты =====
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    
    class Meta:
        verbose_name = 'Чертеж'
        verbose_name_plural = 'Чертежи'
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return f"{self.name} (v{self.version})"
    
    def get_file_extencion(self):
        """Возвращает расширение файла"""
        return os.path.splitext(self.file.name)[1][1:].lower()
    
    
class Notification(models.Model):
    """
    Модель для внутренних уведомлений пользователей
    """
    
    class Type(models.TextChoices):
        INFO = 'info', 'Информация'
        SUCCESS = 'success', 'Успех'
        WARNING = 'warning', 'Предпреждение'
        ERROR = 'error', 'Ошибка'
        
    # ===== Основные поля =====
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок'
    )
    message = models.TextField(
        verbose_name='Сообщение'
    )
    type = models.CharField(
        max_length=10,
        choices=Type.choices,
        default=Type.INFO,
        verbose_name='Тип'
    )
    
    # ===== Связи =====
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notification',
        verbose_name='Пользователь'
    )
    
    # ===== Статус =====
    is_read = models.BooleanField(
        default=False,
        verbose_name='Прочитано'
    )
    
    # ===== Ссылка =====
    link = models.URLField(
        blank=True,
        verbose_name='Ссылка для перехода'
    )
    
    # ===== Даты =====
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата прочтения'
    )
    
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-read_at']
        
    def __str__(self):
        return f"{self.get_type_display()}: {self.title[:50]}"
    
    def make_as_read(self):
        """Отметить как прочитанное"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
            
    def make_as_unread(self):
        """Отметить как непрочитанное"""
        if self.is_read:
            self.is_read = False
            self.read_at = None
            self.save()