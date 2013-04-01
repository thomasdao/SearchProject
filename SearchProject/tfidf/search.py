'''
Created on Mar 23, 2013

@author: daoxuandung
'''

from django.db import connection
from tokenize_docs import get_term_freq_dict
from tfidf.models import Document

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
    terms = process_query(query)
    
    # Prepare to run SQL raw query
    cursor = connection.cursor()
    
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
    
    cursor.execute(raw_sql)

    row = cursor.fetchall()
    
    print row
    
    docs = [x for x in row if is_all_terms_matched(x[1], terms)]
    
    for x in docs:
        print x
    

# Execute
if __name__ == '__main__':
    rank('Interesting conversation')