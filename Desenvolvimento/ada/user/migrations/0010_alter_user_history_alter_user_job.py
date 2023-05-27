from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='history',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.history'),
        ),
        migrations.AlterField(
            model_name='user',
            name='job',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.job'),
        ),
    ]
