from datetime import timedelta
from django.utils import timezone
from django.db import models

# Create your models here.
class MasterClock(models.Model):
    time_difference = models.IntegerField(default=0)  # الفرق بالثواني بين الوقت الفعلي والوقت الذي اختاره المستخدم

    def set_time(self, new_time):
        """يحسب الفرق بين الوقت الجديد و timezone.now()"""
        time_diff = int((new_time - timezone.now()).total_seconds())
        self.time_difference = time_diff
        self.save()

    def get_adjusted_time(self):
        """يرجع الوقت المعدل بناءً على الفرق المخزن"""
        return timezone.now() + timedelta(seconds=self.time_difference)
      

class Doctor(models.Model):
  name = models.CharField(max_length=70)
  specialty = models.CharField(max_length=255, blank=True, null=True)
  
  def __str__(self):
    return f"{self.name}: {self.specialty if self.specialty else ''}".strip()


class Patient(models.Model):
  STATUS_CHOICES = [
      ("stable", "Stable"),
      ("critical", "Critical"),
      ("under_observation", "Under Observation"),
  ]

  Gender_Choices = [
      ("male", "Male"),
      ("female", "Female"),
  ]

  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  age = models.IntegerField(blank=True, null=True)
  gender = models.CharField(max_length=10, choices=Gender_Choices, blank=True, null=True)
  status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="stable")
  doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patients', blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
      return f"{self.first_name} {self.last_name}: ({self.status})"
    
    
    
class Room(models.Model):
  room_number = models.CharField(max_length=10, unique=True)
  room_temperature = models.FloatField(blank=True, null=True)
  last_updated = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Room {self.room_number}"
  
  
class RoomAssignment(models.Model):
  patient = models.ForeignKey("Patient", on_delete=models.CASCADE, related_name="admissions")
  room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="admissions")
  doctor = models.ForeignKey("Doctor", on_delete=models.SET_NULL, related_name="admissions", blank=True, null=True)

  admission_date = models.DateTimeField(auto_now_add=True)   # وقت الدخول
  discharge_date = models.DateTimeField(blank=True, null=True)  # وقت الخروج (ممكن يبقى None لو لسه في الغرفة)

  def __str__(self):
      return f"{self.patient} in {self.room} ({self.admission_date} - {self.discharge_date or 'Present'})"