from django.db import models


class FacilityDetails(models.Model):
    bldg_no = models.PositiveIntegerField(primary_key=True)
    facility_name = models.CharField(max_length=40)

    class Meta:
        db_table = 'facility_details'

    def __str__(self):
        return self.facility_name


class User(models.Model):

    user_id = models.CharField(max_length=10, primary_key=True)
    password = models.CharField(max_length=30)
    designation = models.CharField(max_length=20)
    bldg_no = models.ForeignKey(FacilityDetails, on_delete=models.CASCADE, db_column='bldg_no')

    class Meta:
        db_table = 'user'
        constraints = [
            models.CheckConstraint(
                check=models.Q(user_id__startswith='U'),
                name='user_id_starts_with_U'
            )
        ]

    def __str__(self):
        return self.user_id


class WasteType(models.Model):

    sl_no = models.CharField(max_length=10, primary_key=True)
    bldg_no = models.ForeignKey(FacilityDetails, on_delete=models.CASCADE, to_field='bldg_no')
    waste_type = models.CharField(max_length=1,
                                  choices=[('A', 'Type A'), ('B', 'Type B'), ('C', 'Type C'), ('D', 'Type D'),
                                           ('E', 'Type E')])

    class Meta:
        db_table = 'waste_type'
        constraints = [
            models.CheckConstraint(
                check=models.Q(sl_no__startswith='S'),
                name='sl_no_starts_with_S'
            )
        ]

    def __str__(self):
        return self.sl_no


class DisposalDetails(models.Model):

    shipment_no = models.CharField(max_length=10, primary_key=True)
    sender_approval = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')])
    receiver_approval = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')])
    disposal_confirmation = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')])

    class Meta:
        db_table = 'disposal_details'
        constraints = [
            models.CheckConstraint(
                check=models.Q(shipment_no__startswith='SH'),
                name='shipment_no_starts_with_SH'
            )
        ]

    def __str__(self):
        return self.shipment_no
