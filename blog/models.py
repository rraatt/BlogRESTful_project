from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver


class Tag(models.Model):
    """Модель тегу для можливості пошуку блогів за потрібною тематикою"""
    title = models.CharField(max_length=255, verbose_name='Тег')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class BlogPost(models.Model):
    """Модель для збереження посту в блозі, містить заголовок, текст, час створення, редакції. Має можливість додавання
     тегів для полегшення пошуку цікавлячих постів. Можливе додання зображень у майбутньому"""
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Зміст')
    Tags = models.ManyToManyField(Tag, related_name='posts', verbose_name='Теги', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'


class Profile(models.Model):
    """Модель профілю для розширення стандартного аккаунту джанго, автоматично створюється при реєстрації
     містить посилання на аккаунт та біо користувача можливе доповнення аватаркою у майбутньому"""
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(verbose_name='Про себе', null=True)

    def __str__(self):
        return self.account.get_full_name()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    class Meta:
        verbose_name = 'Профіль користувача'
        verbose_name_plural = 'Профілі користувачів'


class CommentOwner(models.Model):
    """Проміжна модель для визначення належності коментарю, містить посилання на пост чи інший комментар, автоматично
    створюється при створенні коментаря"""
    post = models.OneToOneField(BlogPost, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.OneToOneField('Comment', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Належність коментарю'
        verbose_name_plural = 'Належності коментарів'
        constraints = [
            models.CheckConstraint(
                check=Q(post__isnull=False) | Q(comment__isnull=False),
                name='not_both_null'
            ), models.CheckConstraint(
                check=Q(post__isnull=True) | Q(comment__isnull=True),
                name='not_both_true')]

    def __str__(self):
        ref = self.post or self.comment
        return str(ref)

    @receiver(post_save, sender='Comment')
    def create_owner(sender, instance, created, **kwargs):
        if created:
            CommentOwner.objects.create(group=instance)

    @receiver(post_save, sender='Comment')
    def save_owner(sender, instance, **kwargs):
        instance.commentowner.save()


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, verbose_name='Пост коментаря')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор коментаря')
    content = models.CharField(max_length=255, verbose_name='Зміст коментаря')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = "Коментарі"
        ordering = ['time_update', 'time_create']
