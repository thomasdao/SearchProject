# Steps

1) Get a few text docs

2) Use WordNet to parse:
- terms, frequency in a document
- insert into database: new document, update TermFrequencyInDoc, TermFrequencyOverall

3) Until the above steps done, process the tfidf for each pair of term-document, store in the score column

4) Begin to search:
- SELECT document_id, sum(score) as T from tfidf_termfrequencyindoc
  WHERE term IN %s
  GROUPBY document_id
  ORDER BY T desc
  LIMIT 100
  
- From retrieved document_id, get the real docs