from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from PIL import Image


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Forum(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='anonymous' )
    topic = models.CharField(max_length=31, unique=True)
    description = models.CharField(max_length=1000,blank=True)
    slug = models.SlugField()
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    image = models.ImageField(default='clean_bkg.jpg', upload_to='forum pics')
    def __str__(self):
        return str(self.topic)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.topic)
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
        img.save(self.image.path)


    def get_field_values(self):
        field_dict = {}
        for field in Forum._meta.fields:
            field_name = str(field).replace('pages.Forum.', '')
            field_dict.setdefault(field_name.capitalize(), field.value_to_string(self))
        return field_dict

class Question(models.Model):
    question = models.CharField(max_length=140 ) #, null=True, default=1)
    date = models.DateTimeField(auto_now_add=True)
    collapse = IntegerRangeField(null=True, min_value=0, max_value=1)
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    prediction = models.PositiveIntegerField(null=True)
    slug = models.SlugField(null=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    tracked_by = models.ManyToManyField(User, null=True)


    def __str__(self):
        return self.question

    def find_forum(self):
        return Forum.objects.filter(topic=self.forum)[0].topic


    def get_absolute_url(self):
        return reverse('pages:question-detail', kwargs={'pk':self.pk,
                                                    'slug':self.slug,
                                                    'topic': self.find_forum()})

    def save(self, *args, **kwargs):
        if len(self.question) > 31:
            q_string =self.question[-30:]
        else:
            q_string = self.question
        self.slug = slugify(q_string)
        super(Question, self).save(*args, **kwargs)



class Estimate(models.Model):
    estimate = IntegerRangeField(min_value=0, max_value=100)
    slug = models.SlugField()
    body = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE, default=2, verbose_name='related_question', db_column='related_question_id')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    evaluation = models.DecimalField(null=True, decimal_places=3, max_digits=7)


    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse('pages:estimate-detail', kwargs={'pk':self.pk})






#django-admin runserver --settings=django-react-webpack.settings
