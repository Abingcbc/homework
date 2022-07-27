field_map = {}

with open('../results.txt','r') as file:
    tmp_map = {}
    for line in file:
        split_arr = line.strip().split(':')
        field = split_arr[0].strip().lower().replace(' ', '_')
        if field == '' or len(split_arr) == 1:
            continue
        if field_map.get(field, 0) == 0:
            field_map[field] = 1
        else:
            field_map[field] += 1
count = 0
for key, value in field_map.items():
    if value > 10000:
        print(str(key) + ': ' + str(value))
        count += 1
print('\n' + str(count))
