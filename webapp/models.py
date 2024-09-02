from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class FacilityDetails(models.Model):
    bldg_no = models.PositiveIntegerField(primary_key=True)
    facility_name = models.CharField(max_length=40)

    class Meta:
        db_table = 'facility_details'

    def __str__(self):
        return self.facility_name


class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        if not user_id:
            raise ValueError('The User ID must be set')
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(user_id, password, **extra_fields)

class User(AbstractBaseUser):
    user_id = models.CharField(max_length=10, unique=True, primary_key=True)
    designation = models.CharField(max_length=20)
    bldg_no = models.ForeignKey(FacilityDetails, on_delete=models.CASCADE, db_column='bldg_no')

    # Define required fields
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['designation', 'bldg_no']

    objects = UserManager()
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
