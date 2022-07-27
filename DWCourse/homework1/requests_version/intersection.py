movies_id = set([])
with open('movies_id.txt','r') as file:
    for line in file:
        movies_id.add(line.strip())

found_id = set([])
with open('found.txt', 'r') as file:
    for line in file:
        found_id.add(line.strip())

to_found = movies_id - found_id
with open('to_find.txt', 'w') as file:
    for i in to_found:
        file.write(i + '\n')