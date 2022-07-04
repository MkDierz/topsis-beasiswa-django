from django.db import models

# Create your models here.


class Data(models.Model):
    """Model definition for Data."""

    class Penghasilan(models.IntegerChoices):
        P1 = 1, ">= 5 Juta"
        P2 = 2, ">= 4 Juta"
        P3 = 3, ">= 3 Juta"
        P4 = 4, ">= 2 Juta"
        P5 = 5, ">= 1 Juta"

    class Tanggungan(models.IntegerChoices):
        T1 = 1, "1 Orang"
        T2 = 2, "2 Orang"
        T3 = 3, "3 Orang"
        T4 = 4, "4 Orang"
        T5 = 5, ">5 Orang"

    class Organisasi(models.IntegerChoices):
        O1 = 4, "Ikut"
        O2 = 0, "Tidak Ikut"

    nama = models.CharField(
        null=False,
        max_length=50,
        verbose_name="Nama",
    )
    nilai_rata_rata = models.IntegerField(
        null=False,
        help_text="Dibulatkan dengan skala 1-100",
        verbose_name="Nilai Rata Rata",
    )
    penghasilan = models.IntegerField(
        choices=Penghasilan.choices,
        verbose_name="Penghasilan Orang Tua",
    )
    tanggungan = models.IntegerField(
        choices=Tanggungan.choices,
        verbose_name="Tanggungan Orang Tua",
    )
    organisasi = models.IntegerField(
        choices=Organisasi.choices,
        verbose_name="Ativitas Organisasi",
    )

    class Meta:
        """Meta definition for Data."""

        verbose_name = "Data"
        verbose_name_plural = "Data"

    def __str__(self):
        self.nama

    @property
    def nilai_score(self):
        if self.nilai_rata_rata <= 20:
            return 1
        if self.nilai_rata_rata <= 40:
            return 2
        if self.nilai_rata_rata <= 60:
            return 3
        if self.nilai_rata_rata <= 80:
            return 4
        if self.nilai_rata_rata <= 100:
            return 5
