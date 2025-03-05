file = open('youtube.txt', 'w')

try:
    file.write('This is a text file of YouTube')
finally:
    file.close()
    
# Same thing happening there as happening in the upper side
with open('youtube.txt', 'w') as file:
    file.write('This is a text file of YouTube')