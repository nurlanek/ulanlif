from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя клиента")
    email = models.EmailField(verbose_name="Электронная почта клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон клиента")
    address = models.TextField(verbose_name="Адрес клиента")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['name']

    def __str__(self):
        return self.name
