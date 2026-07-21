# /apps/employees/admin.py | A.Grachev | 21.07.2026
from django.contrib import admin
from django.utils.html import format_html
from .models import Employee, Qualification, WorkSchedule


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Админка для модели 'Сотрудник'"""
    
    # Что показываем в списке
    list_display = [
        'full_name_display',
        'employee_number',
        'position',
        'work_area',
        'status_badge',
        'qualifications_display',
        'user'
    ]
    
    # Фильтры
    list_filter = [
        'status',
        'work_area',
        'qualification'
    ]
    
    # Поиск
    search_fields = [
        'first_name',
        'last_name',
        'patronymic',
        'employee_number',
        'phone',
        'email'
    ]
    
    # Сортировка
    ordering = ['last_name', 'first_name']

    # Группировка полей
    fieldsets = (
        ('Личные данные', {
            'fields': ('first_name', 'last_name', 'patronymic', 'birth_date',)
        }),
        ('Рабочая информация', {
            'fields': ('employee_number', 'position', 'work_area', 'qualification',)
        }),
        ('Статус', {
            'fields': ('status', 'hire_date', 'fire_date',)
        }),
        ('Контакты', {
            'fields': ('phone', 'email',)
        }),
        ('Связь с пользователем', {
            'fields': ('user',)
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at',),
            'classes': ('collapse',)
        }),
        
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def full_name_display(self, obj):
        return obj.full_name    
    
    full_name_display.short_description = 'ФИО'
    full_name_display.admin_order_field = 'last_name'    
    
    def status_badge(self, obj):
        """Колирование статуса"""
        # Соотношение цветов к статусу
        colors = {
            'active': 'success',
            'vacation': 'warning',
            'sick': 'danger',
            'fired': 'secondary'
        }
        color = colors.get(obj.status, 'secondary')
        status_display = obj.get_status_display()
        return format_html(
            '<span class="badge bg-{}">{}</span>', 
            color, status_display
        )
        
    status_badge.short_description = 'Статус'
    
    def qualifications_display(self, obj):
        """Возвращает список квалификаций"""
        return ', '.join([q.name for q in obj.qualification.all()]) or '-'
    
    qualifications_display.short_description = 'Квалификции'
    
    
@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    """Админка для модели 'Квалификации'"""
    
    # Что показываем в списке
    list_display = [
        'code',
        'name',
        'is_active',
        'created_at'
    ]
    
    # Фильтры
    list_filter = [
        'is_active'
    ]
    
    # Поиск
    search_fields = [
        'name',
        'code',
        'description'
    ]
    
    # Сортировка
    ordering = ['code']
    
    # Группировка полей
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'code', 'description')
        }),
        ('Статус', {
            'fields': ('is_active',)
        })
    )
    

@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    """Админка для модели 'Учет рабочего времени'"""
    
    # Что показываем
    list_display = [
        'employee',
        'date',
        'entry_type_display',
        'hours',
        'coment'
    ]
    
    # Фильтры
    list_filter = [
        'entry_type',
        'date',
        'employee'
    ]
    
    # Поиск
    search_fields = [
        'employee__last_name',
        'employee__first_name',
        'coment'
    ]
    
    # Сортировка
    ordering = ['date', '-created_at']
    
    # Группировка полей
    fieldsets = (
        ('Основаная информация', {
            'fields': ('employee', 'date', 'entry_type', 'hours')
        }),
        ('Комментарий', {
            'fields': ('coment',)
        }),
    )
    
    def entry_type_display(self, obj):
        """Возвращает список типов часов"""
        return obj.get_entry_type_display()
    
    entry_type_display.short_description = 'Тип'