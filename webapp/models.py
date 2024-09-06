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
    name = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=20)
    bldg_no = models.ForeignKey(FacilityDetails, on_delete=models.CASCADE, db_column='bldg_no')

    @property
    def facility_name(self):
        return self.bldg_no.facility_name if self.bldg_no else None

    # Define required fields
    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['name', 'designation', 'bldg_no']

    objects = UserManager()

    class Meta:
        db_table = 'user'

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

    def __str__(self):
        return self.sl_no


class RequestStatus(models.Model):
    REQUEST_NO_MAX_LENGTH = 5
    ITEM_MAX_LENGTH = 30
    APPROVAL_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    request_no = models.IntegerField(primary_key=True)
    no_of_items = models.IntegerField()
    total_qty = models.DecimalField(max_digits=7, decimal_places=2)
    sending_engineer = models.CharField(max_length=ITEM_MAX_LENGTH, blank=True, null=True)
    sending_manager = models.CharField(max_length=ITEM_MAX_LENGTH, blank=True, null=True)
    receiving_engineer = models.CharField(max_length=ITEM_MAX_LENGTH, blank=True, null=True)
    receiving_manager = models.CharField(max_length=ITEM_MAX_LENGTH, blank=True, null=True)
    disposing_engineer = models.CharField(max_length=ITEM_MAX_LENGTH, blank=True, null=True)
    disposing_manager = models.CharField(max_length=ITEM_MAX_LENGTH, blank=True, null=True)
    sender_approval = models.CharField(max_length=10, choices=APPROVAL_CHOICES)
    receiver_approval = models.CharField(max_length=10, choices=APPROVAL_CHOICES)
    disposal_confirmation = models.CharField(max_length=10, choices=APPROVAL_CHOICES)

    class Meta:
        db_table = 'request_status'


class FormDetails(models.Model):
    UNIT_CHOICES = [
        ('U1', 'U1'),
        ('U2', 'U2'),
    ]
    WASTE_TYPE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]

    sl_no = models.CharField(max_length=30, primary_key=True)
    request_no = models.ForeignKey(RequestStatus, on_delete=models.CASCADE)
    facility_name = models.CharField(max_length=30, blank=True, null=True)
    bldg_no = models.ForeignKey(FacilityDetails, on_delete=models.CASCADE,
                                db_column='bldg_no')
    unit = models.CharField(max_length=5, choices=UNIT_CHOICES)
    segment_ref_no = models.CharField(max_length=30)
    dispatch_date = models.DateField()
    bag_id_no = models.CharField(max_length=100)
    nature_material = models.CharField(max_length=150)
    waste_type = models.CharField(max_length=5, choices=WASTE_TYPE_CHOICES)
    qty = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        db_table = 'form_details'


class DisposalDetails(models.Model):
    UNIT_CHOICES = [
        ('U1', 'U1'),
        ('U2', 'U2'),
    ]
    WASTE_TYPE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]

    sl_no = models.CharField(max_length=30, primary_key=True)
    request_no = models.ForeignKey(RequestStatus, on_delete=models.CASCADE)
    facility_name = models.CharField(max_length=30)
    unit = models.CharField(max_length=5, choices=UNIT_CHOICES, blank=True, null=True)
    segment_ref_no = models.CharField(max_length=30, blank=True, null=True)
    dispatch_date = models.DateField(blank=True, null=True)
    bag_id_no = models.CharField(max_length=100, blank=True, null=True)
    nature_material = models.CharField(max_length=150, blank=True, null=True)
    waste_type = models.CharField(max_length=5, choices=WASTE_TYPE_CHOICES, blank=True, null=True)
    stored_qty = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    remarks = models.CharField(max_length=300, blank=True, null=True)
    disposed_qty = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'disposal_details'
