from django.db import models

# Create your models here.

# Store document content
class Document(models.Model):
    content = models.TextField()

# Store term frequency in a document
# The score is calculated at the end
# to rank the tfidf
class TermFrequency(models.Model):
    term = models.CharField(max_length=200)
    document = models.ForeignKey(Document)
    frequency = models.IntegerField()
    score = models.FloatField()

    
# Store how many document contains a given
# term
class DocFrequency(models.Model):
    term = models.CharField(max_length=200)
    num_docs = models.IntegerField()