from django.db import models

class WeightCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    weight_limit = models.CharField(max_length=100, blank=True, verbose_name="Лимит веса")

    def __str__(self):
        return f"{self.name} ({self.weight_limit})" if self.weight_limit else self.name

    class Meta:
        verbose_name = "Весовая категория"
        verbose_name_plural = "Весовые категории"

class Fighter(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя Фамилия")
    nickname = models.CharField(max_length=100, blank=True, verbose_name="Прозвище")
    image = models.ImageField(upload_to='fighters/', blank=True, null=True, verbose_name="Изображение")
    country = models.CharField(max_length=100, verbose_name="Страна")
    country_flag = models.ImageField(upload_to='flags/', blank=True, null=True, verbose_name="Флаг страны")
    is_champion = models.BooleanField(default=False, verbose_name="Чемпион")
    weight_category = models.ForeignKey(WeightCategory, on_delete=models.CASCADE, related_name='fighters', verbose_name="Весовая категория")
    ranking = models.PositiveIntegerField(verbose_name="Ранг")
    age = models.PositiveIntegerField(blank=True, null=True, verbose_name="Возраст")
    height = models.CharField(max_length=20, blank=True, verbose_name="Рост")
    weight = models.CharField(max_length=20, blank=True, verbose_name="Вес")
    reach = models.CharField(max_length=20, blank=True, verbose_name="Размах рук")
    record = models.CharField(max_length=50, blank=True, verbose_name="Рекорд")
    strikes_landed_per_min = models.FloatField(blank=True, null=True, verbose_name="Ударов в минуту")
    strike_accuracy = models.FloatField(blank=True, null=True, verbose_name="Точность ударов")
    takedown_avg = models.FloatField(blank=True, null=True, verbose_name="Среднее количество тейкдаунов")
    takedown_accuracy = models.FloatField(blank=True, null=True, verbose_name="Точность тейкдаунов")


    class Meta:
        ordering = ['weight_category', 'ranking']
        verbose_name = "Боец"
        verbose_name_plural = "Бойцы"

    def __str__(self):
        return f"{self.name} ({self.weight_category})"

    @property
    def country_flag_url(self):
        if self.country_flag and hasattr(self.country_flag, 'url'):
            return self.country_flag.url
        return None

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None
