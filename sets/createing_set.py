genre_results = ['rap', 'classical', 'rock', 
                 'rock', 'country', 'rap', 'rock', 
                 'latin', 'country', 'k-pop', 'pop', 
                 'rap', 'rock', 'k-pop',  'rap', 'k-pop', 
                 'rock', 'rap', 'latin', 'pop', 'pop', 
                 'classical', 'pop', 'country', 
                 'rock', 'classical', 'country',
                  'pop', 'rap', 'latin']


survey_genres=set(genre_results)
survey_abbreviated={survey[0:3] for survey in survey_genres}
print(survey_abbreviated)
