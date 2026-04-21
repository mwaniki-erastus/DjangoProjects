from django.db import models

# Create your models here.
class Region(models.Model):
    region_name = models.CharField(max_length=50)
    region_code = models.IntegerField()

    def __str__(self):
        return self.region_name
 
class County(models.Model):
    county_name = models.CharField(max_length=50)
    county_code = models.IntegerField()
    region_code = models.ForeignKey(Region, on_delete=models.PROTECT)

    def __str__(self):
        return self.county_name
    
    class Meta:
        unique_together = ("county_name","region_code")
    
class Sub_County(models.Model):
    sub_county_name = models.CharField(max_length=50)
    sub_county_code = models.IntegerField()
    county_code = models.ForeignKey(County, on_delete=models.PROTECT)

    def __str__(self):
        return self.sub_county_name
    
class School(models.Model):
    school_name = models.CharField(max_length=50)
    school_uic = models.CharField(max_length=10)
    sub_county_code = models.ForeignKey(Sub_County, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.school_name} and uic: {self.schoo_uic}"
    
class Learner(models.Model):
    learner_name = models.CharField(max_length=50)
    learner_upi = models.CharField(max_length=10)
    learner_assessment_number = models.CharField(max_length=10)
    school_uic = models.ForeignKey(School, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.school_name} and uic: {self.schoo_uic}"