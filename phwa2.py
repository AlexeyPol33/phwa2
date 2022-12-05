import csv
import re

def read_file (file_name):
    out = []
    with open("phonebook_raw.csv",encoding='utf8') as f:
        rows = csv.reader(f, delimiter=",")
        out= list(rows)
    return out

def write_file (file_name,contacts_list):
    with open(file_name, "w",encoding='utf8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)

def to_list_str(list):
    text = []
    for i in list:
        text.append(','.join(i))
    return text

def fix_phone (list_str):
    phone_pattern = r'(8|\+7)\s*\D{0,1}(\d{3})\D{0,2}(\d{3})\D{0,1}(\d{2})\D{0,1}(\d{2})'
    out = []
    for i in list_str:
        result = re.sub(phone_pattern,r'+7(\2)\3-\4-\5',i)
        result = re.sub(r'\D+(доб.)\D+(\d{4})[)]*',r' \1 \2',result)
        out.append(result)
    return out

def fix_lfs(list_str):
    lfs_pattern = r'^(\w+)[,\s](\w+)[,\s](\w+){0,1}'
    out = []
    for i in list_str:
        result = re.sub(lfs_pattern,r'\1,\2,\3',i)
        out.append(result)
    return out

def delet_void (lst,count):
    for i in range(count):
        lst.remove('')
    return lst


def split_text(list_text):
    out = []
    for i in list_text:
        out.append(i.split(','))
    return out

def merge_contact (contact_one,contact_two):
    for i in range(len(contact_one) - 1):
        if (contact_one[i] == '' and contact_two[i] != ''):
            contact_one.insert(i, contact_two[i])
            
    return(contact_one)
        
def remove_duplicates (list_list):
    counter = len(list_list)
    out = []
    while counter > 0:
        try:
            obj = list_list.pop()
            for i in list_list:
                if obj[0] == i[0] and obj[1] == i[1]:
                    obj = merge_contact(obj,i)
                    list_list.remove(i)
            out.append(obj)
        except:
            pass
        counter -= 1
    return(out)

def create_csv_list(list_list):
    pattern = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']
    out = []
    for i in list_list:
        j = i
        if len(j) > len(pattern):
            j = delet_void(j, len(j) - len(pattern))
        out.append(j)
    out = remove_duplicates(out)
    return out[::-1]

if __name__ == '__main__':
    phonebook = read_file('phonebook_raw.csv')
    phonebook = to_list_str(phonebook)
    phonebook = fix_lfs(phonebook)
    phonebook = fix_phone(phonebook)
    write_file('test.csv',create_csv_list(split_text(phonebook)))
