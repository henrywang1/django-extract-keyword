# Generated by Django 2.0.4 on 2018-04-26 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extract', '0004_word2vec'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Word2Vec',
            new_name='Word2VecModel',
        ),
    ]
