from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    class Meta:
        db_table = 'user'
    userId = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True, blank=True)

    @property
    def id(self):
        return self.userId

class Locations(models.Model):
    class Meta:
        db_table = 'locations'
    location = models.CharField(max_length=100, primary_key=True)
    address = models.CharField(max_length=200)
    pincode = models.CharField(max_length=6)


class Lots(models.Model):
    class Meta:
        db_table = 'lots'
    lotId = models.CharField(max_length=10, primary_key=True)
    location = models.ForeignKey(Locations, to_field='location', on_delete=models.CASCADE)
    maxSlots = models.IntegerField()
    price = models.FloatField()


class Slots(models.Model):
    id = models.CharField(primary_key=True, max_length=15)  # Combine slotId + lotId
    slotId = models.IntegerField()
    lotId = models.ForeignKey(Lots, to_field='lotId', on_delete=models.CASCADE)
    isOccupied = models.BooleanField(default=False)

    class Meta:
        unique_together = (('slotId', 'lotId'),)
        db_table = 'slots'
        # Alternatively, use constraints with Meta.constraints for more control


class OccupiedSlot(models.Model):
    id = models.CharField(primary_key=True, max_length=15)
    slotId = models.IntegerField()
    lotId = models.ForeignKey('Lots', to_field='lotId', on_delete=models.CASCADE)
    userId = models.ForeignKey('User', to_field='userId', on_delete=models.CASCADE)
    vehicleNo = models.CharField(max_length=15)
    price = models.FloatField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

    class Meta:
        unique_together = (('slotId', 'lotId'),)
        db_table = 'occupied_slot'
