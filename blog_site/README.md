## Run Server

`python manage.py runserver`

## Development Steps

`django-admin startproject blog_site`

The outer blog_site/ root directory is a container for your project. Its name doesn’t matter to Django; you can rename it to anything you like.

```
blog_site/
    manage.py
    blog_site/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

### Apply initial migrations

`python manage.py migrate`

### Create new application

`python manage.py startapp blog`

### Apply model changes

```
python manage.py makemigrations blog
python manage.py migrate
```

### Create superuser
`python manage.py createsuperuser` (admin, test)


### Add Post (shell)

`python manage.py shell`

```
from django.contrib.auth.models import User
from blog.models import Post
user = User.objects.get(username='admin')
post = Post(title='Another post',
        slug='another-post',
        body='Post body.',
        author=user)
post.save()
```

### Queries

```
all_posts = Post.objects.all()
Post.objects.filter(title='Another Post')
Post.objects.filter(title__iexact='another post')
Post.objects.filter(title__contains='Django')
Post.objects.filter(title__icontains='django')
Post.objects.filter(id__in=[1, 3])
Post.objects.filter(id__gt=3)
Post.objects.filter(title__istartswith='another')
Post.objects.filter(publish__date=date(2024, 1, 31))
Post.objects.filter(author__username='admin')

Post.objects.filter(publish__year=2024) \
            .filter(author__username='admin')
```