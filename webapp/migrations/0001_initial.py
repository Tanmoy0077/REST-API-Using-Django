# Generated by Django 5.1 on 2024-09-14 15:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityDetails',
            fields=[
                ('bldg_no', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('facility_name', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'facility_details',
            },
        ),
        migrations.CreateModel(
            name='Remarks',
            fields=[
                ('request_no', models.IntegerField(primary_key=True, serialize=False)),
                ('sm_remarks', models.CharField(blank=True, max_length=200, null=True)),
                ('rm_remarks', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RequestStatus',
            fields=[
                ('request_no', models.IntegerField(primary_key=True, serialize=False)),
                ('facility_name', models.CharField(max_length=30)),
                ('no_of_items', models.IntegerField()),
                ('total_qty', models.DecimalField(decimal_places=2, max_digits=7)),
                ('sending_engineer', models.CharField(blank=True, max_length=30, null=True)),
                ('sending_manager', models.CharField(blank=True, max_length=30, null=True)),
                ('receiving_engineer', models.CharField(blank=True, max_length=30, null=True)),
                ('receiving_manager', models.CharField(blank=True, max_length=30, null=True)),
                ('disposing_engineer', models.CharField(blank=True, max_length=30, null=True)),
                ('disposing_manager', models.CharField(blank=True, max_length=30, null=True)),
                ('sender_approval', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=10)),
                ('make_changes', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=10)),
                ('receiver_validated', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=10)),
                ('receiver_approval', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=10)),
                ('disposal_validated', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=10)),
                ('disposal_confirmation', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=10)),
            ],
            options={
                'db_table': 'request_status',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('user_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('designation', models.CharField(max_length=20)),
                ('bldg_no', models.ForeignKey(db_column='bldg_no', on_delete=django.db.models.deletion.CASCADE, to='webapp.facilitydetails')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='FormDetails',
            fields=[
                ('sl_no', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('facility_name', models.CharField(blank=True, max_length=30, null=True)),
                ('unit', models.CharField(choices=[('U1', 'U1'), ('U2', 'U2')], max_length=5)),
                ('segment_ref_no', models.CharField(max_length=30)),
                ('dispatch_date', models.DateField()),
                ('bag_id_no', models.CharField(max_length=100)),
                ('nature_material', models.CharField(max_length=150)),
                ('waste_type', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=5)),
                ('qty', models.DecimalField(decimal_places=2, max_digits=7)),
                ('disposed', models.BooleanField(default=False)),
                ('bldg_no', models.ForeignKey(db_column='bldg_no', on_delete=django.db.models.deletion.CASCADE, to='webapp.facilitydetails')),
                ('request_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.requeststatus')),
            ],
            options={
                'db_table': 'form_details',
            },
        ),
        migrations.CreateModel(
            name='DisposalDetails',
            fields=[
                ('sl_no', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('facility_name', models.CharField(max_length=30)),
                ('unit', models.CharField(blank=True, choices=[('U1', 'U1'), ('U2', 'U2')], max_length=5, null=True)),
                ('segment_ref_no', models.CharField(blank=True, max_length=30, null=True)),
                ('dispatch_date', models.DateField(blank=True, null=True)),
                ('bag_id_no', models.CharField(blank=True, max_length=100, null=True)),
                ('nature_material', models.CharField(blank=True, max_length=150, null=True)),
                ('waste_type', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=5, null=True)),
                ('stored_qty', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('remarks', models.CharField(blank=True, max_length=300, null=True)),
                ('disposed_qty', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('request_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.requeststatus')),
            ],
            options={
                'db_table': 'disposal_details',
            },
        ),
        migrations.CreateModel(
            name='WasteType',
            fields=[
                ('sl_no', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('waste_type', models.CharField(choices=[('A', 'Type A'), ('B', 'Type B'), ('C', 'Type C'), ('D', 'Type D'), ('E', 'Type E')], max_length=1)),
                ('bldg_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.facilitydetails')),
            ],
            options={
                'db_table': 'waste_type',
            },
        ),
    ]
