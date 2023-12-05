from scholarly import scholarly
from scholarly import ProxyGenerator
import json

# Link says stuff may be wrong cause it's done through a parser and web scrapping
# https://support.google.com/websearch/thread/163481940/papers-attributed-to-wrong-author-in-google-scholar?hl=en

# Set up a ProxyGenerator object to use free proxies
# This needs to be done only once per session
pg = ProxyGenerator()
pg.FreeProxies()
scholarly.use_proxy(pg)

# Retrieve the author's data, fill-in, and print
# Get an iterator for the author results
search_query = scholarly.search_author('Joseph Oglio')
# Retrieve the first result from the iterator
first_author_result = next(search_query)

# print("First Author:")
# scholarly.pprint(first_author_result)

# keys for first_author
# ['container_type', 'filled', 'source', 'scholar_id', 'url_picture', 'name', 'affiliation', 'email_domain', 'interests', 'citedby']
# print(list(first_author_result.keys()))


# Retrieve all the details for the author
author = scholarly.fill(first_author_result )
with open('author.json', 'w') as convert_file:
     convert_file.write(json.dumps(author))
# print("First Author Details:")
# scholarly.pprint(author)


# first publication
first_publication = author['publications'][0]
first_publication_filled = scholarly.fill(first_publication)
with open('first_publication.json', 'w') as convert_file:
     convert_file.write(json.dumps(first_publication))
# print("First Publicaiton:")
# scholarly.pprint(first_publication_filled)

# The titles of the author's publications
publication_titles = [pub['bib']['title'] for pub in author['publications']]
with open('publication_titles.json', 'w') as convert_file:
     convert_file.write(json.dumps(publication_titles))
# print("Publication Titles:")
# print(publication_titles)


# Which papers cited the first publication
citations = [citation['bib']['title'] for citation in scholarly.citedby(first_publication_filled)]
with open('citations.json', 'w') as convert_file:
     convert_file.write(json.dumps(citations))
# print("First Publication Cited by:")
# print(citations)