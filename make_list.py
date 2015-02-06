from __future__ import print_function
import os
import json

def create_list( filename ):
    cont = 'n'
    with open(filename, 'w') as f :
        while cont == 'n' :
            event = raw_input('Event: ')
            if event == 'quit' :
                cont = 's'
                continue
            year = raw_input('Year: ')
            f.write( event + ': ' + year + '\n')

def custom_list( filename, elements = 0) :
    elements = int(elements)
    items = []
    cont = 'n'
    for i in range(0,elements) :
        element = raw_input('Element: ')
        items.append(element)
    
    with open(filename, 'w') as f :

        while cont == 'n' :

            for l in range(0, elements) :

                input = raw_input('Enter ' + items[l] + ': ' ) 
                if input == 'quit':
                    print( 'quit' ) 
                    cont = 's'
                    break

                if l == elements - 1 :
                    f.write( input + '\n')
                else : 
                    f.write( input + ',' ) 
                 

if __name__ == "__main__" :
    file_name = raw_input('Enter filename: ')
    elements = raw_input('Enter Elements: ')
    custom_list( file_name, elements )

