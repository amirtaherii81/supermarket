# Generated by Django 5.0.6 on 2024-07-13 22:19

import django.db.models.deletion
import django.utils.timezone
import utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_title', models.CharField(max_length=100, verbose_name='نام برند')),
                ('image_name', models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر گروه کالا')),
                ('slug', models.SlugField(max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'برند',
                'verbose_name_plural': 'برندها',
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(max_length=100, verbose_name='نام ویژگی')),
            ],
            options={
                'verbose_name': 'ویژگی',
                'verbose_name_plural': 'ویژگی ها',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=500, verbose_name='نام کالاها')),
                ('discription', models.TextField(blank=True, null=True, verbose_name='توضیحات کالا')),
                ('image_name', models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر کالا')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='قیمت کالا')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='وضعیت فعال / غیر فعال')),
                ('register_date', models.DateField(auto_now_add=True, null=True, verbose_name='تاریخ درج')),
                ('published_date', models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار')),
                ('update_date', models.DateField(auto_now=True, verbose_name='تاریخ آخرین بروز رسانی')),
                ('slug', models.SlugField(max_length=200, null=True)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='products.brand', verbose_name='برند کالا')),
            ],
            options={
                'verbose_name': 'کالا',
                'verbose_name_plural': 'کالاها',
            },
        ),
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100, verbose_name='مقدار ویژگی کالا')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.feature', verbose_name='ویژگی')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='کالا')),
            ],
            options={
                'verbose_name': 'ویژگی محصول',
                'verbose_name_plural': 'ویژگی های محصولات',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='features',
            field=models.ManyToManyField(through='products.ProductFeature', to='products.feature'),
        ),
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر کالا')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='کالا')),
            ],
            options={
                'verbose_name': 'تصویر',
                'verbose_name_plural': 'تصاویر',
            },
        ),
        migrations.CreateModel(
            name='ProductGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_title', models.CharField(max_length=100, verbose_name='عنوان گروه کالا')),
                ('image_name', models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر گروه کالا')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات گروه کالا')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='وضعیت فعال / غیر فعال')),
                ('register_date', models.DateField(auto_now_add=True, null=True, verbose_name='تاریخ درج')),
                ('published_date', models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار')),
                ('update_date', models.DateField(auto_now=True, verbose_name='تاریخ آخرین بروز رسانی')),
                ('slug', models.SlugField(max_length=200, null=True)),
                ('group_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='products.productgroup', verbose_name='والد گروه کالا')),
            ],
            options={
                'verbose_name': 'گروه کالا',
                'verbose_name_plural': 'گروه کالاها',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_group',
            field=models.ManyToManyField(related_name='products_of_groups', to='products.productgroup', verbose_name='گروه کالا'),
        ),
        migrations.AddField(
            model_name='feature',
            name='product_group',
            field=models.ManyToManyField(related_name='features_of_groups', to='products.productgroup', verbose_name='گروه کالا'),
        ),
    ]
