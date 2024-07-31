from django.db import models


class Malzeme_category(models.Model):
    class Meta:
            verbose_name_plural = ('Категория материала')

    name = models.CharField(max_length=200, verbose_name='Наименование')

    def __str__(self):
        return self.name


class Malzeme_birim(models.Model):
    class Meta:
            verbose_name_plural = ('Измерение единиц')

    name = models.CharField(max_length=200, verbose_name='Наименование')

    def __str__(self):
        return self.name
class Malzeme(models.Model):
    class Meta:
            verbose_name_plural = ('Материал')

    isim = models.CharField(max_length=200, verbose_name='Наименование')
    aciklama = models.TextField(blank=True, null=True, verbose_name='Примичение')
    miktar = models.FloatField(verbose_name='Количество')
    malzeme_category = models.ForeignKey(Malzeme_category, on_delete=models.CASCADE, verbose_name='Category')
    malzeme_birim = models.ForeignKey(Malzeme_birim, on_delete=models.CASCADE, verbose_name='Едиица измерение')

    def __str__(self):
        return self.isim

class GirisHareketi(models.Model):
    malzeme = models.ForeignKey(Malzeme, on_delete=models.CASCADE, verbose_name='Материал')
    miktar = models.FloatField(verbose_name='Количество')
    tedarikci = models.CharField(max_length=200, verbose_name='Поставщик')
    giris_tarihi = models.DateTimeField(auto_now_add=True, verbose_name='Дата поступления')

    def __str__(self):
        return f"{self.malzeme.isim} - {self.miktar} {self.malzeme.birim}"

class CikisHareketi(models.Model):
    malzeme = models.ForeignKey(Malzeme, on_delete=models.CASCADE, verbose_name='Материал')
    miktar = models.FloatField(verbose_name='Штук')
    uretim_siparisi = models.CharField(max_length=200, verbose_name='Производсвенный заказ')
    cikis_tarihi = models.DateTimeField(auto_now_add=True, verbose_name='Дата выпуска')

    def __str__(self):
        return f"{self.malzeme.isim} - {self.miktar} {self.malzeme.birim}"

class TransferHareketi(models.Model):
    malzeme = models.ForeignKey(Malzeme, on_delete=models.CASCADE, verbose_name='Материал')
    miktar = models.FloatField(verbose_name='Штук')
    transfer_tarihi = models.DateTimeField(auto_now_add=True, verbose_name='Дата передачи')
    hedef_ambar = models.CharField(max_length=200, verbose_name='Целевой склад')

    def __str__(self):
        return f"{self.malzeme.isim} - {self.miktar} {self.malzeme.birim} - {self.hedef_ambar}"