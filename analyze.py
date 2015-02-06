import csv
import ast
import operator
import numpy as np
import matplotlib.mlab as mlab
from numpy.random import normal
import matplotlib.pyplot as plt

def generate_clean_data_movies( data_file ) :
    f = open(data_file)
    lines = f.readlines()
    f.close
    movie_list = []
    for i in range(0, len(lines)) : 
        split_index = lines[i].index(':') + 2
        title = lines[i][:lines[i].index(':')].strip()
        year = int(lines[i][split_index:].strip())

        movie_list.append([year, '-1', title, 'War', -1, -1, -1, -7, 'Yes'])
    
    movie_list = sorted(movie_list)
    movie_years_list = []
    i = 0
    while i < len(movie_list) :
        current_year = movie_list[i][0]
        count = 1
        stop = False
        i = i + 1
        while i < len(movie_list) and stop == False :
            if movie_list[i][0] == movie_list[i-1][0] :
                count = count + 1
                i = i + 1
            else : 
                stop = True
        
        movie_years_list.append((current_year, count))
        
    rows = [] 
    with open('movie_data/film.csv', 'rb') as doc : 
        spamreader = csv.reader(doc, delimiter = ';')
        for col in spamreader :
            rows.append(col) 
        rows.pop(0)
        rows.pop(0)
    award_winning_movies = []
    for i in range(0, len(rows) ) :
        if rows[i][8] == 'Yes' :
           award_winning_movies.append(rows[i]) 
   
    all_movies = sorted(rows, key=operator.itemgetter(0))
    war_movies = movie_list   
    award_winning_movies = sorted(award_winning_movies, key=operator.itemgetter(0))
    decades = { 1900 : [], 1910 : [], 1920 : [], 1930 : [], 1940 : [], 1950 : [], 1960 : [], 1970 : [], 1980 : [], 1990 : []}
    decades_aw = { 1900 : [], 1910 : [], 1920 : [], 1930 : [], 1940 : [], 1950 : [], 1960 : [], 1970 : [], 1980 : [], 1990 : []}
    decades_war = { 1900 : [], 1910 : [], 1920 : [], 1930 : [], 1940 : [], 1950 : [], 1960 : [], 1970 : [], 1980 : [], 1990 : []}

    '''
        now we want to consolidate our two lists,
        if there is a movie in war_movies that isn't in decades, put it in there.
    '''
    
    for i in range(0, len(all_movies)) :
        for key in sorted(decades.iterkeys()) : 
            if int(all_movies[i][0]) - key < 10 : 
                decades[key].append(all_movies[i])

                if decades[key][len(decades[key]) - 1][8] == 'Yes' :
                    decades_aw[key].append(all_movies[i])
                
                if decades[key][len(decades[key]) -1][3].lower().strip() == 'war' :
                    decades_war[key].append(all_movies[i])
                break
    
    for i in range(0, len(war_movies)) :
        for key in sorted(decades.iterkeys()) :
            if int(war_movies[i][0]) - key < 10 :
                decades_war[key].append(war_movies[i])
                break 
        if search_decade( decades, war_movies[i][2] ) == False :
            insert_decade( decades, decades_aw, war_movies[i])
            
    '''

    at this point we have a few key elements

    1. The list of all movies : all_movies 
    2. The list of award winning war movies: war_movies
    3. The list of all award winning movies : award_winning_movies
    4. The list of all movies by decades (all, award winnging only, war only)

    '''

    war_movies = sorted(war_movies, key=operator.itemgetter(0))
    for jawn in sorted(decades.iterkeys()) :
        decades[jawn]       = sorted(decades[jawn], key=operator.itemgetter(0))
        decades_aw[jawn]    = sorted(decades_aw[jawn], key=operator.itemgetter(0))
        decades_war[jawn]   = sorted(decades_war[jawn], key=operator.itemgetter(0))
    return {'war_movies' : war_movies, 'all_movies' : all_movies, 'decades' : decades, 'decades_aw' : decades_aw, 'decades_war' : decades_war}

def generate_clean_data_books() :

    unsorted, rows, war_novels = [], [], []
    with open('books.csv', 'rb') as doc :
        spamreader = csv.reader(doc, delimiter = ',')
        for col in spamreader : 
            col.pop(6) #Get rid of summary
            col.pop(0) #Get rid of ID
            col.pop(0) #Get rid of FID
            rows.append(col)
            last_e = len(rows) - 1 
            asdf = rows[len(rows) - 1][3]
            if len(asdf) > 0 :
                rows[last_e][3] = eval(rows[len(rows) - 1][3])
            else :
                rows[last_e][3] = {}
            asdf = rows[last_e][2]
            if len(asdf) > 0 :
                rows[last_e][2] = int(rows[last_e][2][:4])
            else :
                rows[last_e][2] = -1
    for line in rows :
        if line[2] < 1900 or line[2] > 2000 :
            rows.remove(line)
    for line in rows :
        
        if ('War novel' in line[3].values()) == True or ('Anti-war' in line[3].values()) == True :
            if line[2] > 1900 and line[2] < 2000 :
                war_novels.append(line)
            

        if line[2] == -1 :
            unsorted.append(line)
        
    war_novels = sorted(war_novels, key=operator.itemgetter(2))
    rows = sorted(rows, key=operator.itemgetter(2))
    for i in range(0, len(rows)) :
        while i < len(rows) and ( rows[i][2] < 1900 or rows[i][2] > 2000 ):
            rows.pop(i)
    return rows

def search_book_genre( booklist, genre ) :
    output = []
    for line in booklist :
        if ( genre in line[3].values()) == True :
            if line[2] >= 1900 and line[2] <= 2000 : 
                output.append(line) 
    if len(output) > 0 :
        return output
    return False
    
def search_decade( decades, title ) : 
    for key in sorted(decades.iterkeys()) :
        for i in range(0,len(decades[key])) :
            if title.lower().strip() == decades[key][i][2].lower().strip() :
                return key
        
    return False;
        
def insert_decade( decades, decades_aw, item) : 
    for key in sorted(decades.iterkeys()) : 
        if int(item[0]) - key < 10 :
            decades[key].append(item)
            if item[8] == 'Yes' :
                decades_aw[key].append(item)


def sort_intervals( input, intervals ) :
    for i in range(0, len(input)) :

        for key in sorted(intervals.iterkeys()) :

            if input[i][2] - key < 10 :
                intervals[key].append(input[i])
                break

    return intervals         
    import pdb; pdb.set_trace() 
def empty_intervals() :
    return {1900 : [], 1910 : [], 1920 : [], 1930 : [], 1940 : [], 1950 : [], 1960 : [], 1970 : [], 1980 : [], 1990 :[]}

def get_popularity(list, decay, start, end) :
    score = 0.0
    threshold = .97
    for i in range(start, end) :
        score = score*(1 - decay)
        l = 0
        while l < len(list) and list[l][2] <= i :
            if list[l][2] == i :
                score = score + 1
            l = l + 1
        if score < threshold :
            score = 0
    
    return score
'''
movies_clean_data = generate_clean_data_movies( 'movie_data/Oscar_Winning_War_Films.txt')

movies_clean_data_instances = { 'decades' : {}, 'decades_aw' : {}, 'decades_war' : {} }
for key in sorted(movies_clean_data['decades'].iterkeys()) :
    movies_clean_data_instances['decades'][key]    = len(movies_clean_data['decades'][key])
    movies_clean_data_instances['decades_aw'][key] = len(movies_clean_data['decades_aw'][key])
    movies_clean_data_instances['decades_war'][key]= len(movies_clean_data['decades_war'][key])
'''
intervals = empty_intervals()

book_library    = generate_clean_data_books()
romance_books   = search_book_genre( book_library , 'Romance novel')
war_books       = search_book_genre( book_library, 'War novel') 
fantasy_books   = search_book_genre( book_library, 'Fantasy')
scifi_books     = search_book_genre( book_library, 'Science Fiction')
specfiction_books=search_book_genre( book_library, 'Speculative fiction')
historical_books= search_book_genre( book_library, 'Historical novel')

intervals_war       = sort_intervals( war_books, empty_intervals())
intervals_romance   = sort_intervals( romance_books, empty_intervals())
intervals_fantasy   = sort_intervals( fantasy_books, empty_intervals())
intervals_scifi     = sort_intervals( scifi_books, empty_intervals())
intervals_specfiction=sort_intervals( specfiction_books, empty_intervals())
intervals_historical= sort_intervals( historical_books, empty_intervals())
intervals_bl        = sort_intervals( book_library, empty_intervals())

for key in sorted(intervals.iterkeys()) :
    print( 'HELLO I"M HERE AND I"M NOT AN INFINITE LOOP' )
    intervals[key].append( {'war' : get_popularity(war_books, .001, key, key + 10), 'romance': get_popularity(romance_books, 0.001, key, key + 10), 'historical' : get_popularity(historical_books, 0.001, key, key + 10 ) })
           

war, romance, historical = [], [], []
fwar,fromance, fhistorical=[], [], []

for key in sorted(intervals.iterkeys()) :
    war.append(intervals[key][0]['war'])
    romance.append(intervals[key][0]['romance'])
    historical.append(intervals[key][0]['historical'])

    fwar.append(intervals[key][0]['war'] / len(war_books))

    fromance.append(intervals[key][0]['romance'] / len(romance_books))


    fhistorical.append(intervals[key][0]['historical'] / len(historical_books))
import pdb; pdb.set_trace()

