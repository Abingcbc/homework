from bs4 import BeautifulSoup
import re
import collections
import traceback

def get_content(html_tag):
    return html_tag.string if not html_tag is None else ""

def get_meta_info(meta_info: collections.defaultdict, dl_tag):
    info_type = dl_tag.dt.span.string
    # Because of limited time and capacity, I may try in the future.
    if info_type.find('Devices') >= 0:
        return
    meta_info[info_type] = ''.join([c.string \
        if not c.string is None else '' \
        for c in dl_tag.dd.contents])

def prime_parse(response: BeautifulSoup, ID: str):
    try:
        name = response.find(attrs={'data-automation-id':'title'})
        name = get_content(name)

        star_score = response.find(attrs={'href':'#customer-review-section'})
        star_score = re.search(r'(?<=Rated).*?(?=out)', 
            star_score['aria-label']).group(0).strip() \
            if not star_score is None else ""

        imdb_score = response.find(attrs={'data-automation-id':'imdb-rating-badge'})
        imdb_score = get_content(imdb_score)

        time_len = response.find(attrs={'data-automation-id':'runtime-badge'})
        time_len = get_content(time_len)

        year = response.find(attrs={'data-automation-id':'release-year-badge'})
        year = get_content(year)

        restrict_level = response.find(attrs={'data-automation-id':'rating-badge'})
        restrict_level = get_content(restrict_level)

        price = response.find_all(attrs={'data-purchasing-modal-text':True})
        if len(price) > 1:
            rent_price = '$'+re.search(r'(?<=\$).*', 
                price[0]['data-purchasing-modal-text']).group(0).strip() \
                if not price is None else '' 
            buy_price = '$'+re.search(r'(?<=\$).*',
                price[1]['data-purchasing-modal-text']).group(0).strip() \
                if not price is None else ''
        elif len(price) == 0:
            rent_price = ''
            buy_price = ''
        else:
            rent_price = ''
            buy_price = '$'+re.search(r'(?<=\$).*',
                price[0]['data-purchasing-modal-text']).group(0).strip() \
                if not price is None else ''

        meta_info_list = response.find_all(attrs={'data-automation-id':'meta-info'})
        meta_info = collections.defaultdict()
        for m in meta_info_list:
            info_list = m.contents
            for info in info_list:
                get_meta_info(meta_info, info)
        
        return name, star_score, imdb_score, time_len, year, \
        restrict_level, rent_price, buy_price, meta_info, True
    except Exception as e:
        with open('error.log', 'a') as file:
            file.write('ID: ' + ID + '\n')
            file.write(traceback.format_exc())
            file.write('\n')
        return '','','','','','','','',{},False
