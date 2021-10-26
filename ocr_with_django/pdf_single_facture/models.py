from django.db import models

class image(models.Model):
    photo = models.ImageField(upload_to='images')

class filePdf(models.Model):
    photo = models.FileField(upload_to='images')

    def delete(self, *args, **kwargs):
        self.photo.delete()
        super().delete(*args, **kwargs)


    def __str__(self):
        return str(self.photo.name)

    def save(self, *args, **kwargs):
        # Call standard save
        super(filePdf, self).save(*args, **kwargs)