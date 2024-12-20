from django.db import models
from django.utils import timezone


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    division_id = models.IntegerField(null=True, blank=True)
    district_id = models.IntegerField(null=True, blank=True)
    subdistrict_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'admins'


class Applicant(models.Model):
    application_id = models.CharField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=510)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    religion = models.CharField(max_length=255)
    birth_country = models.CharField(max_length=255, null=True, blank=True)
    birth_division_id = models.IntegerField()
    birth_district_id = models.IntegerField()
    birth_subdistrict_id = models.IntegerField()
    birth_date = models.DateField()
    present_address = models.TextField()
    permanent_address = models.TextField()
    father_name = models.CharField(max_length=255)
    father_nid = models.CharField(max_length=20)
    mother_name = models.CharField(max_length=255)
    mother_nid = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=20)
    relationship = models.CharField(max_length=10, choices=[('mother', 'mother'), ('father', 'father'), ('brother', 'brother'), ('sister', 'sister')])
    division_id = models.IntegerField()
    district_id = models.IntegerField()
    subdistrict_id = models.IntegerField()
    healthcare_id = models.IntegerField()
    application_time = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'applicants'


class BabyReg(models.Model):
    reg_no = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    birth = models.CharField(max_length=20, null=True, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    father_nid = models.CharField(max_length=255, null=True, blank=True)
    mother_name = models.CharField(max_length=255, null=True, blank=True)
    mother_nid = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    vaccine_centre = models.CharField(max_length=255, null=True, blank=True)
    user_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'baby_reg'


class Citizen(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    father_nid = models.CharField(max_length=255, null=True, blank=True)
    mother_name = models.CharField(max_length=255, null=True, blank=True)
    mother_nid = models.CharField(max_length=255, null=True, blank=True)
    present_division = models.CharField(max_length=255, null=True, blank=True)
    present_district = models.CharField(max_length=255, null=True, blank=True)
    present_upazila = models.CharField(max_length=255, null=True, blank=True)
    permanent_division = models.CharField(max_length=255, null=True, blank=True)
    permanent_district = models.CharField(max_length=255, null=True, blank=True)
    permanent_upazila = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        db_table = 'citizen'


class District(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    division_id = models.ForeignKey('Division', on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'districts'


class Division(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(null=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'divisions'


class Healthcare(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    subdistrict_id = models.ForeignKey('Subdistrict', on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'healthcare'


class Subdistrict(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    district_id = models.ForeignKey('District', on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'subdistricts'


class VaccinationSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    application_id = models.CharField(max_length=100)
    vaccine_id = models.IntegerField()
    dose_number = models.IntegerField(null=True)
    scheduled_date = models.DateField()
    status = models.CharField(max_length=255, default='Scheduled')
    healthcare_id = models.IntegerField()
    volunteer_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'vaccination_schedule'


class Vaccine(models.Model):
    id = models.AutoField(primary_key=True)
    vaccine_name = models.CharField(max_length=255)
    vaccine_code = models.CharField(max_length=100, unique=True)
    doses = models.IntegerField(null=True)
    time_intervals = models.JSONField(null=True)
    manufactured_country = models.CharField(max_length=255, null=True, blank=True)
    disease = models.CharField(max_length=255, null=True, blank=True)
    storage_temperature = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vaccine'


class VaccineStatus(models.Model):
    application_id = models.CharField(max_length=100, primary_key=True)
    status = models.CharField(max_length=255)

    class Meta:
        db_table = 'vaccine_status'


class Volunteer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    healthcare = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # Password will be hashed
    subdistrict_id = models.IntegerField()
    healthcare_id = models.IntegerField()

    class Meta:
        db_table = 'volunteers'
