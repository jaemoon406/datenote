from django.db import models
from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel

User = get_user_model()


class Book(TimeStampedModel):
    # 추억이 담긴 책을 만들어 보세요.
    name = models.CharField(max_length=25, verbose_name='그룹 이름', null=False, )
    # owner = models.OneToOneField(User, verbose_name='책 주인', on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=125, verbose_name='그룹 설명', null=True)
    # password = models.CharField(max_length=255, null=True, blank=True)
    is_public = models.BooleanField(default=0)
    member = models.ManyToManyField(User, through='BookMember')

    class Meta:
        db_table = 'books'


class Board(TimeStampedModel):
    user = models.ForeignKey(User, verbose_name='게시물 멤버', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', verbose_name='책', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=12, verbose_name='게시물 제목', null=True)
    data = models.DateTimeField(verbose_name='추억 날짜')
    locate = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'boards'


class Comment(TimeStampedModel):
    # 댓글에 대댓글까지
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='유저')
    board = models.ForeignKey('Board', on_delete=models.CASCADE, verbose_name='내용')
    content = models.CharField(max_length=55, null=False, blank=False)
    parents = models.IntegerField(null=True, verbose_name='부모 댓글 id')

    class Meta:
        db_table = 'comments'


class BookMember(TimeStampedModel):
    user = models.ForeignKey(User, verbose_name='구성원', on_delete=models.DO_NOTHING)
    book = models.ForeignKey('Book', verbose_name='책', on_delete=models.CASCADE)
    owner = models.BooleanField()
    class Meta:
        db_table = 'book_member'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                name='unique book member',
            ),
        ]
