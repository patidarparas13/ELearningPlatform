from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Course(models.Model):
    '''
    A foreign key with cascade delete means that if a record in the
    parent table is deleted, then the corresponding
    records in the child table will automatically be deleted.
    '''
    owner = models.ForeignKey(User,related_name='courses_created',on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,related_name='courses',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    #The field used for ordering.Prepend a minus for reverse
    # ordering: '-order'
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

'''
content_type: A ForeignKey field to the ContentType model
object_id: This is PositiveIntegerField to store the primary key of
the related object
item: A GenericForeignKey field to the related object by combining
the two previous fields
Only the content_type and object_id fields have a corresponding column
in the database table of this model. The item field allows you to
retrieve or set the related object directly, and its functionality is
built on top of the other two fields.
We are going to use a different model for each type of content. Our
content models will have some common fields, but they will differ
in the actual data they can store.
'''


class Content(models.Model):
    module = models.ForeignKey(Module,related_name='contents',on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,limit_choices_to={
        'model_in':('text','video','image','file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type','object_id')

class ItemBase(models.Model):
    owner = models.ForeignKey(User,related_name='%(class)s_related',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class video(ItemBase):
    url = models.URLField()






