# Generated by Django 4.2.16 on 2025-01-03 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Page", "0017_issuebook_issue_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="issuebook",
            name="typeOf_issue",
            field=models.CharField(
                default="select", max_length=100, verbose_name="Type of Issue"
            ),
        ),
    ]
