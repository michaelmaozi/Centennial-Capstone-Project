from django.db import models
from datetime import datetime

from apps.users.models import BaseModel
from apps.organizations.models import Teacher
from apps.organizations.models import CourseOrg

from DjangoUeditor.models import UEditorField


class Course(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="instructor")
    course_org = models.ForeignKey(CourseOrg, null=True, blank=True, on_delete=models.CASCADE, verbose_name="department")
    name = models.CharField(verbose_name="course name", max_length=50)
    desc = models.CharField(verbose_name="course description", max_length=300)
    learn_times = models.IntegerField(default=0, verbose_name="length(mins)")
    degree = models.CharField(verbose_name="difficulty", choices=(("low", "entry level"), ("mid", "intermediated"), ("high", "advanced")), max_length=20)
    students = models.IntegerField(default=0, verbose_name='students number')
    fav_nums = models.IntegerField(default=0, verbose_name='favorite number')
    click_nums = models.IntegerField(default=0, verbose_name="clicks")
    notice = models.CharField(verbose_name="notice", max_length=300, default="")
    category = models.CharField(default="General Course", max_length=20, verbose_name="course category")
    tag = models.CharField(default="", verbose_name="course tag", max_length=10)
    youneed_know = models.CharField(default="", max_length=300, verbose_name="course requirements")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name="instructor notices")
    is_classics = models.BooleanField(default=False, verbose_name="is recommanded")
    detail = UEditorField(verbose_name="course details", width=600, height=300, imagePath="courses/ueditor/images/",
                          filePath="courses/ueditor/files/", default="")
    is_banner = models.BooleanField(default=False, verbose_name="is AD. banner")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="course image", max_length=100)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # def lesson_nums(self):
    #     return self.lesson_set.all().count()

    # def show_image(self):
    #     from django.utils.safestring import mark_safe
    #     return mark_safe("<img src='{}'>".format(self.image.url))
    # show_image.short_description = "images"

    # def go_to(self):
    #     from django.utils.safestring import mark_safe
    #     return mark_safe("<a href='/course/{}'>go to</a>".format(self.id))
    # go_to.short_description = "go to"


class BannerCourse(Course):
    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = verbose_name
        proxy = True
    
    def __str__(self):
        return self.name

class CourseTag(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="course")
    tag = models.CharField(max_length=100, verbose_name="course tag")

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="course")
    name = models.CharField(max_length=100, verbose_name="chapter name")
    learn_times = models.IntegerField(default=0, verbose_name="length(mins)")

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, verbose_name="chapter", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="vide name")
    learn_times = models.IntegerField(default=0, verbose_name="length(mins)")
    url = models.CharField(max_length=1000, verbose_name="video url")

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="course")
    name = models.CharField(max_length=100, verbose_name="course resource name")
    file = models.FileField(upload_to="course/resourse/%Y/%m", verbose_name="download path", max_length=200)

    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
