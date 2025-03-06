from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Фамилия автора")
    last_name = models.CharField(max_length=100, verbose_name="Имя автора")

    # def __str__(self) -> str:
    #     return "%s %s (%s)" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Book(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название книги")
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books", verbose_name="Автор"
    )
    count = models.IntegerField(verbose_name="Остаток книг на складе")

    def reduce_quantity(self, buy):
        if buy <= 0:
            raise ValueError("Сумма уменьшения должна быть положительной.")
        if buy > self.count:
            raise ValueError("Недостаточно товара на складе.")
        self.count -= buy
        self.save()

    def __str__(self) -> str:
        return "%s %s (%s)" % (self.title, self.author, self.count)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
