import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator


class TimeStampedMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, db_column='created')
    updated = models.DateTimeField(auto_now=True, db_column='updated')

    class Meta:
        abstract = True


class Role(models.TextChoices):
    TEACHER = 'teacher', _('Teacher')
    STUDENT = 'student', _('Student')


class User(AbstractUser):
    third_name = models.CharField("отчество", max_length=500, blank=True)
    role = models.TextField(_('Role'), choices=Role.choices)
    klass = models.ForeignKey(
        'Klass',
        on_delete=models.CASCADE,
        db_column='klass_id',
        verbose_name=_('klass')
    )

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')
        ordering = ['last_name']


class Profile(TimeStampedMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _('профайл')
        verbose_name_plural = _('профайлы')


class Klass(TimeStampedMixin):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    amount_of_students = models.IntegerField()
    best_task_type = models.IntegerField(null=True, blank=True)
    best_task_percent = models.IntegerField(null=True, blank=True)
    worst_task_type = models.IntegerField(null=True, blank=True)
    worst_task_percent = models.IntegerField(null=True, blank=True)

    # def __str__(self):
    #     return self.name


class Meta:
        verbose_name = _('класс')
        name = _('имя')
        subject = _('предмет')
        amount_of_students = _('количество студентов')
        best_task_type = _('наилучше выполняемое задание')
        best_task_percent = _('процент выполнения лучшего задания')
        worst_task_type = _('наихудше выполняемое задание')
        worst_task_percent = _('процент выполнения худшего задания')



class Variant(TimeStampedMixin):
    name = models.CharField("название", max_length=500)
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE,
        db_column='task_id',
        verbose_name=_('task')
    )

    class Meta:
        verbose_name = _('вариант')
        verbose_name_plural = _('варианты')


class Task(TimeStampedMixin):
    name = models.CharField("название", max_length=500)

    class Meta:
        verbose_name = _('задача')
        verbose_name_plural = _('задачи')