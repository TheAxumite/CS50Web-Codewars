# Generated by Django 4.1.5 on 2023-04-30 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_user_followers_user_following_posts_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='child_comments',
            field=models.ManyToManyField(related_name='child_comments_lists', to='network.posts'),
        ),
        migrations.AddField(
            model_name='posts',
            name='parent_comment',
            field=models.ManyToManyField(related_name='parent', to='network.posts'),
        ),
    ]
