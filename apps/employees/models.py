# /apps/employees/models.py | A.Grachev | 21.07.2026
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


class Qualification(models.Model):
    """
    Модель для квалификации сотрудников
    Например: Сварщик, Электрик, Инженер-конструктор, Оператор
    """

    # ===== Основные поля ======
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название квалификации'
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Код квалификации',
        help_text='Например: WELD-01, TURN-01'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения'
    )
    
    class Meta:
        verbose_name = 'Квалификация'
        verbose_name_plural = 'Квалификации'
        ordering = ['name']
        
    def __str__(self):
        return f'{self.code} - {self.name}'
    
    
class Employee(models.Model):
    """
    Модель сотрудника
    """
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Активен'
        VACATION = 'vacation', 'В отпуске'
        SICK = 'sick', 'Больничный'
        FIRED = 'fired', 'Уволен'
        
    # ===== Личные данные =====
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия'
    )
    patronymic = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Отчество'
    )
    birth_date = models.DateField(
        blank=True,
        verbose_name='Дата рождения'
    )
    
    # ===== Рабочая информация =====
    employee_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Табельный номер'
    )
    position = models.CharField(
        max_length=100,
        verbose_name='Должность'
    )
    work_area = models.CharField(
        max_length=100,
        verbose_name='Участок',
        help_text='Цех, участок, отдел'
    )
    qualification = models.ManyToManyField(
        Qualification,
        related_name='employees',
        verbose_name='Квалификации'
    )    
    
    # ===== Статус =====
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name='Статус'
    )
    
    # ===== Контактные данные =====
    phone = models.CharField(
        max_length=16,
        blank=True,
        verbose_name='Телефон'
    )
    email = models.EmailField(
        blank=True,
        verbose_name='Email'
    )
    
    # ===== Связь с пользователем Django =====
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employee_profile',
        verbose_name='Пользователь'
    )
    
    # ===== Даты =====
    hire_date = models.DateField(
        verbose_name='Дата приема на работу'
    )
    fire_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата увольнения'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения записи'
    )
    
    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['last_name', 'first_name', 'patronymic']
        
    
    def __str__(self):
        return self.full_name
    
    @property
    def full_name(self):
        """Возвращает полное имя сотрудника"""
        if self.patronymic:
            return f'{self.last_name} {self.first_name} {self.patronymic}'
        return f'{self.last_name} {self.first_name}'
    
    def short_name(self):
        """Возвращает сокращенное имя (Фамилия И.О.)"""
        if self.patronymic:
            return f'{self.last_name} {self.first_name[0]}.{self.patronymic[0]}.'
        return f'{self.last_name} {self.first_name[0]}.'
    
    def is_active_employee(self):
        """Проверяет, активен ли сотрудник"""
        return self.status == self.Status.ACTIVE
    
    def is_on_vacation(self):
        """Проверяет, сотрудник в отпуске или нет"""
        return self.status == self.Status.VACATION
    
    def is_on_sick(self):
        """Проверяет, болеет сотрудник или нет"""
        return self.status == self.Status.SICK
    
    
class WorkSchedule(models.Model):
    """
    Модель для учета рабочего времени сотрудника
    """
    
    class EntryType(models.TextChoices):
        PLAN = 'plan', 'Плановые часы'
        FACT = 'fact', 'Фактические часы'
        
    # ===== Связи =====
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='work_schedules',
        verbose_name='Сотрудник'
    )
    
    # ===== Информация =====
    entry_type = models.CharField(
        max_length=10,
        choices=EntryType.choices,
        verbose_name='Тип'
    )
    hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Часы'
    )
    
    # ===== Даты =====
    date = models.DateField(
        verbose_name='Дата'
    )
    
    # ===== Комментарий =====
    coment = models.TextField(
        blank=True,
        verbose_name='Комментарий'
    )
    
    # ===== Метаданные =====
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания записи'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления записи'
    )
    
    
    class Meta:
        verbose_name = 'Запись рабочего времени'
        verbose_name_plural = 'Рабочее время'
        ordering = ['date', '-created_at']
        unique_together = [['employee', 'date', 'entry_type']] # Один тип на день
        
    def __str__(self):
        return f'{self.employee.short_name} - {self.date} ({self.get_entry_type_display()}): {self.hours}ч.'
    
    def clean(self):
        """Валидация: часы не могут быть отрицательными"""
        if self.hours < 0:
            return ValidationError('Часы не могут быть отрицательными')
        if self.hours > 24:
            return ValidationError('Часы не могут превышать 24 часа')
        
        