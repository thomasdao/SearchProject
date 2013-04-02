'''
Created on Mar 23, 2013

@author: daoxuandung
'''

from django.db import connection
from tokenize_docs import get_term_freq_dict
from tfidf.models import Document
import math

def process_query(data):
    # Return term
    print get_term_freq_dict(data).keys()
    return get_term_freq_dict(data).keys()

def is_all_terms_matched(doc_terms, terms):
    matched_terms = doc_terms.split(",")
    if len(matched_terms) == len(terms):
        return True
    
    return False
    

def rank(query):
    # Filter when term is inside searched query string
    # terms = process_query(query)
    terms = query.split()
    terms = [str(x.lower()) for x in terms]
    
    
    # Well potentially SQL Injection here
    if len(terms) > 1:
        params = str(tuple(terms))
        
    elif len(terms) == 1:
        params = "('%s')" % terms[0]
        
    else:
        return
    
    raw_sql = '''
    SELECT document_id, Group_Concat(term), SUM(score) as total_score 
    FROM tfidf_termfrequency
    WHERE term IN %s 
    GROUP BY document_id 
    ORDER BY total_score DESC
    LIMIT 100
    ''' % params
    
    print raw_sql
    
    # Prepare to run SQL raw query
    cursor = connection.cursor()
    cursor.execute(raw_sql)

    rows = cursor.fetchall()
    
    print rows
    
    doc_ids = [x[0] for x in rows if is_all_terms_matched(x[1], terms)]
    
    # Retrieve document
    docs = Document.objects.filter(id__in=doc_ids)
    for i in xrange(len(docs)):
        doc = docs[i]
        doc.score = math.ceil(rows[i][2]*100)/100 
    return docs
    

def search_term(term):
    print term
    
    raw_sql = '''
    SELECT term
    FROM tfidf_docfrequency
    WHERE term LIKE \'''' + term + '''%%'
    ORDER BY num_docs DESC
    LIMIT 10
    '''
    print raw_sql
    
    # Prepare to run SQL raw query
    cursor = connection.cursor()
    cursor.execute(raw_sql)

    rows = cursor.fetchall()
    suggested_terms = [x[0] for x in rows]
    return suggested_terms

# Execute
if __name__ == '__main__':
    rank('Interesting conversation')