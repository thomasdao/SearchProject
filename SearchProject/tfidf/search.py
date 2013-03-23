'''
Created on Mar 23, 2013

@author: daoxuandung
'''

from django.db import connection
from tokenize_docs import get_freq_dist

def process_query(data):
    # Return term
    return get_freq_dist(data).keys()

def rank(query):
    # Filter when term is inside searched query string
    terms = process_query(query)
    
    # Prepare to run SQL raw query
    cursor = connection.cursor()
    
    # Well potentially SQL Injection here
    raw_sql = '''
    SELECT document_id, SUM(score) as total_score FROM tfidf_termfrequency
    WHERE term IN %s
    GROUP BY document_id
    ORDER BY total_score DESC
    LIMIT 10
    ''' % str(tuple(terms))
    
    print raw_sql
    
    cursor.execute(raw_sql)

    row = cursor.fetchall()

    print row
    

# Execute
if __name__ == '__main__':
    rank('population white paper')