# Generated by Django 5.0.6 on 2024-09-07 14:56

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0010_alter_customer_image_name'),
        ('orders', '0008_alter_order_register_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ پرداخت')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش پرداخت')),
                ('amount', models.ImageField(upload_to='', verbose_name='مبلغ پرداخت')),
                ('description', models.TextField(verbose_name='توضیحات پرداخت')),
                ('is_finally', models.BooleanField(default=False, verbose_name='وضعیت پرداخت')),
                ('status_code', models.IntegerField(verbose_name='کد وضعیت پرداخت')),
                ('ref_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='شماره پیگیری پرداخت')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_customer', to='accounts.customer', verbose_name='مشتری')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_order', to='orders.order', verbose_name='سفارش')),
            ],
            options={
                'verbose_name': 'پرداخت',
                'verbose_name_plural': 'پرداخت ها',
            },
        ),
    ]
