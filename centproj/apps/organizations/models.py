from django.db import models
from DjangoUeditor.models import UEditorField

from apps.users.models import BaseModel


# class City(BaseModel):
#     name = models.CharField(max_length=20, verbose_name="城市名")
#     desc = models.CharField(max_length=200, verbose_name="描述")

#     class Meta:
#         verbose_name = "城市"
#         verbose_name_plural = verbose_name

#     def __str__(self):
#         return self.name

class Campus(BaseModel):
    name = models.CharField(max_length=20, verbose_name="campus name")
    desc = models.CharField(max_length=200, verbose_name="description")

    class Meta:
        verbose_name = "campus"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(BaseModel):
    name = models.CharField(max_length=50, verbose_name="department name")
    # desc = UEditorField(verbose_name="description", width=600, height=300, imagePath="courses/ueditor/images/",
    #                       filePath="courses/ueditor/files/", default="")
    desc = models.CharField(verbose_name="description", max_length=300)
    tag = models.CharField(default="general", max_length=10, verbose_name="deparment tag")
    category = models.CharField(default="general", verbose_name="program", max_length=50,
                                choices=(("under_grad", "under graduate"), ("grad", "graduated"), ("post_grad_cert", "post graduated certificated")))
    click_nums = models.IntegerField(default=0, verbose_name="click")
    fav_nums = models.IntegerField(default=0, verbose_name="favorite")
    # image = models.ImageField(upload_to="org/%Y/%m", verbose_name="logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name="department address")
    students = models.IntegerField(default=0, verbose_name="students")
    course_nums = models.IntegerField(default=0, verbose_name="courses")

    is_auth = models.BooleanField(default=False, verbose_name="is_required")
    is_gold = models.BooleanField(default=False, verbose_name="is_recommand")

    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, verbose_name="campus")

    # def courses(self):
    #     courses = self.course_set.filter(is_classics=True)[:3]
    #     return courses

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

from apps.users.models import UserProfile

class Teacher(BaseModel):
    user = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, null=True, blank=True,verbose_name="User")
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="department")
    name = models.CharField(max_length=50, verbose_name="instructor name")
    work_years = models.IntegerField(default=0, verbose_name="work years")
    work_company = models.CharField(max_length=50, verbose_name="company / school")
    work_position = models.CharField(max_length=50, verbose_name="job title")
    points = models.CharField(max_length=50, verbose_name="teaching characteristics")
    click_nums = models.IntegerField(default=0, verbose_name="clicks")
    fav_nums = models.IntegerField(default=0, verbose_name="favorite number")
    age = models.IntegerField(default=18, verbose_name="age")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="avatar", max_length=100)

    class Meta:
        verbose_name = "Instructor"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # def course_nums(self):
    #     return self.course_set.all().count()
