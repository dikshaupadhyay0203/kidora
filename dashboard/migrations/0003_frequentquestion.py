from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_subject_progress_topic_quiz'),
    ]

    operations = [
        migrations.CreateModel(
            name='FrequentQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(db_index=True, max_length=300)),
                ('search_count', models.PositiveIntegerField(default=1)),
                ('last_searched', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
