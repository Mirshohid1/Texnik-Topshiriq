from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


class BlogPost(models.Model):
    """
    A model representing a blog post with title, content, author, and publication status.

    Fields:
        title (CharField): The title of the blog post, with a minimum length of 3 characters.
        content (TextField): The content of the blog post, with a minimum length of 50 characters.
        author (ForeignKey): The user who authored the blog post, linked to the `User` model.
        created_at (DateTimeField): The timestamp when the blog post was created.
        updated_at (DateTimeField): The timestamp when the blog post was last updated.
        is_published (BooleanField): A flag indicating whether the blog post is published or not.

    Features:
        - The `title` and `content` fields are automatically formatted before saving.
        - The `is_published` field defaults to `False`.

    Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
    """

    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(3)],
        verbose_name="Post Title",
    )
    content = models.TextField(
        max_length=1000,
        validators=[MinLengthValidator(50)],
        verbose_name="Content",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created DateTime")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated DateTime")
    is_published = models.BooleanField(default=False, verbose_name="Published")

    def save(self, *args, **kwargs):
        """
        Format title and content before saving.
        """
        self.title = self.title.strip().title()
        self.content = self.content.strip().capitalize()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return f"Post: {self.title} (author: {self.author.username}) (Published: {self.is_published})"
