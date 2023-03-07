from django.db import models


class Player(models.Model):
    foreign_id = models.BigIntegerField('Id пользователя')
    first_name = models.TextField(verbose_name='Имя')
    last_name = models.TextField(verbose_name='Фамилия')
    tg_tag = models.TextField(verbose_name='Тег телеграм')
    score = models.IntegerField(verbose_name='Баллы')
    time1 = models.TimeField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class PlayerTask(models.Model):
    foreign_id = models.BigIntegerField('Player')
    place = models.TextField('Корпус')
    stage = models.IntegerField('Этап')
    questions = models.CharField('Tasks', max_length=100)
    qr_codes = models.CharField('QrCodes', max_length=100)

    def __str__(self):
        return str(self.foreign_id)

    class Meta:
        verbose_name = 'Вопросы для участников'


class Tasks(models.Model):
    number = models.IntegerField('Номер вопроса')
    question = models.TextField('Вопрос')
    answer = models.CharField('Ответ', max_length=30)

    def __str__(self):
        return self.question


class QrCodes(models.Model):
    number = models.IntegerField('Номер кода')
    pokr = models.TextField('Описание Покра')
    miem = models.TextField('Описание МИЭМ')
    vsb = models.TextField('Описание ВШБ')
    bas = models.TextField('Описание Басмач')
    mo = models.TextField('Описание Международные отношения')
    code = models.CharField('Код', max_length=30)

    def __str__(self):
        return self.code
