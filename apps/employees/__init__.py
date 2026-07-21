# apps/employees/__init__.py | A.Grachev | 21.07.2026
"""
Приложение employees - управление сотрудниками.
Содержит модели: Employee, Qualification, WorkSchedule.
"""

from .apps import EmployeesConfig

__all__ = [
    'EmployeesConfig',
]
