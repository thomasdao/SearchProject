'''
Created on Mar 20, 2013

@author: daoxuandung
'''

from os import listdir
from os.path import join
from nltk.tokenize import word_tokenize
from tfidf.models import Document, TermFrequency, DocFrequency
from nltk.probability import FreqDist
from django.db.models import Count
import math

def get_freq_dist(data):
    # Change it to lower case
    lower_data = data.lower()
    
    # Tokenize it
    tokens = word_tokenize(lower_data)
    freq_dist = FreqDist(tokens)
    return freq_dist

def process_data(data):
    freq_dist = get_freq_dist(data)
    
    # Insert into db
    # Save document
    doc = Document(content=data)
    doc.save()
    
    # Save term frequency
    terms = []
    
    # Retrieve Django TermFrequency list of objects
    # words is a dictionary contain key + freq
    for word in freq_dist:
        
        term = TermFrequency()
        term.term = word
        term.frequency = freq_dist.get(word)
        term.document = doc
        term.score = 0
        terms.append(term)
        print term.term + "-" + str(term.frequency)
        
    # Save to DB
    TermFrequency.objects.bulk_create(terms)

def tokenize_docs():
    # Run once
    if TermFrequency.objects.all().exists():
        return
    
    # Else, process files
    # Get list of files inside docs
    files = listdir("docs")
    print files
    
    # Read content of files
    for path in files:
        with open(join("docs", path)) as f:
            data = f.read()
            process_data(data)
    
# Calculate number of appearance of each term in whole
# document space        
def calculate_docs_frequency():
    # Run once
    if DocFrequency.objects.all().exists():
        return
    
    # Else, insert data
    
    # Group by 'term' and Count it
    q = TermFrequency.objects.values('term').annotate(num_docs=Count('term'))
    
    # Create Django object
    doc_freqs = [DocFrequency(**item) for item in q]
    
    # Save it
    DocFrequency.objects.bulk_create(doc_freqs)

# Calculate tfidf for each term
def calculate_tfidf():
    q = TermFrequency.objects.all()
    
    n = DocFrequency.objects.count()
    
    for item in q:
        doc_freq = DocFrequency.objects.filter(term=item.term)[0]
        
        # Calculate tfidf here
        item.score = item.frequency * math.log10(n/doc_freq.num_docs)
        item.save()
    
# Execute
if __name__ == '__main__':
    tokenize_docs()
    calculate_docs_frequency()
    calculate_tfidf()