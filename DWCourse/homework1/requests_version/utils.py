import logging
from init import count

def write_result(item):
    global count
    if not item['validation']:
        return
    count += 1
    log(item['ID'] + ' : ' + str(count))
    with open('found.txt', 'a') as file:
        file.write(item['ID']+'\n')
    with open('results.txt', 'a') as file:
        for key, value in item.items():
            if key == 'meta_info':
                for k, v in value.items():
                    if v.strip() == '':
                        continue
                    file.write(k.strip().replace(':','') + ': ' 
                    + v.strip().replace(':','') + '\n')
            elif key == 'validation':
                continue
            elif value.strip() == '':
                    continue
            else:
                file.write(key.strip().replace(':','') + ': ' 
                + value.strip().replace(':','') + '\n')
        file.write('\n')

# print log in console and into file
def log(message):
    print(message)
    logging.info(message)