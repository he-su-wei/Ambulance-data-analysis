import pandas as pd
from collections import Counter

import re
import time
import random
import requests
from bs4 import BeautifulSoup


# 來源資料夾(每年的資料夾(當年所有檔案))
# concat_col(str, lsit['str'], list['str']) => 來源資料夾， 每年的資料夾， 合併欄位索引
def concat_col(data_basic_path, years, file_name ,col_names, output_dir, savefileName) :
    df = pd.DataFrame()

    for year in years:
        print(year + ' Concating Please wait'+ ' . . . .'  )
        data = pd.read_csv(data_basic_path +  year + '/' + file_name, usecols=col_names)
        data['year'] = year
        replace_col = ['year']
        for index in col_names:
            replace_col.append(index)
        data = data[replace_col]
        df = pd.concat([df, data], axis=0)

    concat_path_file = output_dir + "{}_concat.csv".format(savefileName)
    print('Saving in' + concat_path_file + '. . . .')
    df.to_csv(concat_path_file, index=False)
    return('Success')

# no year col
def noYear_concat_col(data_basic_path, years, file_name ,col_names, output_dir, savefileName) :
    df = pd.DataFrame()

    for year in years:
        print(year + ' Concating Please wait'+ ' . . . .'  )
        data = pd.read_csv(data_basic_path +  year + '/' + file_name, usecols=col_names)

        df = pd.concat([df, data], axis=0)

    concat_path_file = output_dir + "{}_concat.csv".format(savefileName)
    print('Saving in' + concat_path_file + '. . . .')
    df.to_csv(concat_path_file, index=False)
    return('Success')


# 統計 colName 種類個數。 input type => count(dataFram, string)
def count(dataFram, colName):
    class_Counter = Counter(dataFram[colName])
    # age_range = age_df['ePatientT04'].value_counts() // .value_counts() 不好取值
    return class_Counter

# 字典裡種類計數 (df[欄]資料, 字典名稱)
def dict_count(colData, dictName, value=None):
    for i in colData:
        data = ishan(i) + value

        for item_dict in dictName:
            if data == item_dict:
                dictName[item_dict] += 1
            else:
                pass
    return dictName

# 統計年齡分段。input type => class_Counter = 個年齡總數 、type = dict
def ageRange_sum(class_Counter):
    young_children, children, teenageers, youth, middle_age, old_age, other_01, other_03 = 0, 0, 0, 0, 0, 0, class_Counter[7701001], class_Counter[7701003]

    for age in class_Counter:
        if age >= 0 and age <= 6: # 嬰幼兒 0~6
            young_children += class_Counter[age]
        elif age >= 7 and age <= 12: # 少年 7~12
            children += class_Counter[age]
        elif age >= 13 and age <= 17: # 青少年 13~17
            teenageers += class_Counter[age]
        elif age >= 18 and age <= 45: # 青年 18~45
            youth += class_Counter[age]
        elif age >= 46 and age <= 69: # 中年 45~69
            middle_age += class_Counter[age]
        elif age > 69: # 老年 
            old_age += class_Counter[age]

    type_sum = [young_children, children, teenageers, youth, middle_age, old_age, other_01, other_03]
    return type_sum


def location(proxy, address):
    try:
        proxy_ip = random.choice(proxy)  # 隨機取得Proxy IP
        print(f'使用的Proxy IP：{proxy_ip}')

        url='https://www.google.com/maps/place?q=' + address
        time.sleep(random.randint(7,25))
        
        response = requests.get(url, proxies={'http': f'{proxy_ip}', 'https': f'{proxy_ip}'})
        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.prettify() #text 包含了html的內容
        initial_pos = text.find(";window.APP_INITIALIZATION_STATE")

        data = text[initial_pos+36:initial_pos+85] #將其後的參數進行存取
        line = tuple(data.split(',')) #註1
        print(line[1], line[2])
        return [line[1], line[2]]
    except ValueError as err:
        print(err)


def ishan(txt):
    pattern = re.compile("[\u4e00-\u9fa5]")
    return "".join(pattern.findall(txt))

