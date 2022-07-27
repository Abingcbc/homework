from bs4 import BeautifulSoup
import re
import collections
import traceback

def ordinary_parse(response: BeautifulSoup, ID: str):
    try:
        name = response.find(id='productTitle')
        name = name.string.split('"')[0].strip() if not name is None else ''

        star_score = response.find(text=re.compile('out of 5 stars'))
        star_score = star_score.string.split(' ')[0].strip() if not star_score is None \
            else ''

        imdb_score = ''

        detail_table = response.find(id='detail-bullets').table.td.div.ul

        time_len = detail_table.find(text=re.compile(r'^Run*'))
        _, time_len = time_len.parent.parent.stripped_strings if not time_len is None \
            else '', ''
        
        year = detail_table.find(text=re.compile(r'Date'))
        year = year.find_parent(name='li').get_text() if not year is None else ''
        year = year.strip().split(',')[-1].strip()

        restrict_level = response.find(id='bylineInfo').find(text=re.compile(r'^Rated*'))
        restrict_level = restrict_level.parent.next_sibling.next_sibling.get_text().strip() \
            if not restrict_level is None else ''
        
        rent_price = ''

        buy_price = response.find(attrs={'class':'a-color-price'}).string

        meta_info = collections.defaultdict()
        info_list = detail_table.find_all(name='li')
        for info in info_list:
            info_type = info.find(name='b')
            if info_type is None:
                continue
            info_type = info_type.get_text().strip().replace(':','')
            if info_type.find('Run') >= 0 or \
                info_type.find('Data') >= 0 or \
                info_type.find('Rated') >= 0 or \
                info_type.find('Rank') >= 0 or \
                info_type.find('Review') >= 0:
                continue
            info_content = info.get_text().replace(info_type, '')
            meta_info[info_type] = info_content.strip()

        return name, star_score, imdb_score, time_len, year, \
            restrict_level, rent_price, buy_price, meta_info, True
    except Exception as e:
        with open('error.log', 'a') as file:
            file.write(ID + '\n')
            file.write(traceback.format_exc())
            file.write('\n')
        return '','','','','','','','',{},False

