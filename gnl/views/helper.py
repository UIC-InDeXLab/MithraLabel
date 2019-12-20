# from future.builtins import next
# from unidecode import unidecode
from difflib import SequenceMatcher
import pandas as pd
# import csv
# import re
import numpy as np
# import dedupe
# import os
# import logging
# import optparse
import gnl
import re
# import math
from copy import deepcopy
_float_regexp = re.compile(r"^[-+]?(?:\b[0-9]+(?:\.[0-9]*)?|\.[0-9]+\b)(?:[eE][-+]?[0-9]+\b)?$").match

# nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords=set(stopwords.words('english'))

alphabet={}
for letter in range(97, 123):
    alphabet[chr(letter)]=0
for letter in range(65, 91):
    alphabet[chr(letter)]=0

def is_stopword(word):
    return word.lower() in stopwords

#no non alphabetic char exists in str
def is_alp(input):
    for i in input:
        if not i in alphabet:
            return False
    return True

#no non alphabetic char exists in str
def has_alp(input):
    for i in input:
        if i in alphabet:
            return True
    return False

def read_unique(file):
    df = pd.read_csv(file)
    for header in list(df):
        if header!="Id":
            t=set(df[header])
            print(header,"\n",len(t),"\n",t)

def edit_distance(s1, s2):
    m=len(s1)+1
    n=len(s2)+1
    tbl = {}
    for i in range(m): tbl[i,0]=i
    for j in range(n): tbl[0,j]=j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)
    return tbl[i,j]

def edit_percent(Q, Mi):
    levDis = edit_distance(Q, Mi)
    bigger = max(len(Q), len(Mi))
    pct = (bigger - levDis) / bigger
    return pct

def seq_similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def gen_data():
    df = pd.DataFrame(np.random.randn(50, 4), columns=["A", "_B_"," C, ", " D_"])
    pass


def jaccard_distance(str1, str2):
    list1, list2=str1.split(), str2.split()
    intersect = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersect
    return float(intersect / union)

# def preProcess(column):
#     try:  # python 2/3 string differences
#         column = column.decode('utf8')
#     except AttributeError:
#         pass
#     column = unidecode(column)
#     column = re.sub('  +', ' ', column)
#     column = re.sub('\n', ' ', column)
#     column = column.strip().strip('"').strip("'").lower().strip()
#
#     if not column:
#         column = None
#     return column
#
# def readData(filename):
#     data_d = {}
#     with open(filename) as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             clean_row = [(k, preProcess(v)) for (k, v) in row.items()]
#             row_id = int(row['Id'])
#             data_d[row_id] = dict(clean_row)
#
#     return data_d
#
# def deduplication(input_file, output_file):
#
#     optp = optparse.OptionParser()
#     optp.add_option('-v', '--verbose', dest='verbose', action='count',
#                     help='Increase verbosity (specify multiple times for more)'
#                     )
#     (opts, args) = optp.parse_args()
#     log_level = logging.WARNING
#     if opts.verbose :
#         if opts.verbose == 1:
#             log_level = logging.INFO
#         elif opts.verbose >= 2:
#             log_level = logging.DEBUG
#     logging.getLogger().setLevel(log_level)
#
#     #import headers data to become rows
#     # input_file = 'input.csv'
#     # output_file = 'out.csv'
#     settings_file = 'csv_example_learned_settings'
#     training_file = 'csv_example_training.json'
#
#     print('importing data ...')
#     data_d = readData(input_file)
#     if os.path.exists(settings_file):
#         os.remove(settings_file)
#         # print('reading from', settings_file)
#         # with open(settings_file, 'rb') as f:
#         #     deduper = dedupe.StaticDedupe(f)
#
#     else:
#
#         fields = [
#                 {'field' : list(pd.read_csv(input_file))[1], 'type': 'String', 'has missing' : True
#                  }
#                 ]
#
#         deduper = dedupe.Dedupe(fields)
#         deduper.sample(data_d, 15000)
#
#         if os.path.exists(training_file):
#             os.remove(training_file)
#             # print('reading labeled examples from ', training_file)
#             # with open(training_file, 'rb') as f:
#             #     deduper.readTraining(f)
#
#         print('starting active labeling...')
#         dedupe.consoleLabel(deduper)
#         deduper.train()
#
#
#         with open(training_file, 'w') as tf:
#             deduper.writeTraining(tf)
#
#         with open(settings_file, 'wb') as sf:
#             deduper.writeSettings(sf)
#
#
#     threshold = deduper.threshold(data_d, recall_weight=1)
#
#     print('clustering...')
#     clustered_dupes = deduper.match(data_d, threshold)
#
#     print('# duplicate sets', len(clustered_dupes))
#
#     cluster_membership = {}
#     cluster_id = 0
#     for (cluster_id, cluster) in enumerate(clustered_dupes):
#         id_set, scores = cluster
#         cluster_d = [data_d[c] for c in id_set]
#         canonical_rep = dedupe.canonicalize(cluster_d)
#         for record_id, score in zip(id_set, scores):
#             cluster_membership[record_id] = {
#                 "cluster id" : cluster_id,
#                 "canonical representation" : canonical_rep,
#                 "confidence": score
#             }
#
#     singleton_id = cluster_id + 1
#
#     with open(output_file, 'w') as f_output, open(input_file) as f_input:
#         writer = csv.writer(f_output)
#         reader = csv.reader(f_input)
#
#         heading_row = next(reader)
#         heading_row.insert(0, 'confidence_score')
#         heading_row.insert(0, 'Cluster ID')
#         canonical_keys = canonical_rep.keys()
#         for key in canonical_keys:
#             heading_row.append('canonical_' + key)
#
#         writer.writerow(heading_row)
#
#         for row in reader:
#             row_id = int(row[0])
#             if row_id in cluster_membership:
#                 cluster_id = cluster_membership[row_id]["cluster id"]
#                 canonical_rep = cluster_membership[row_id]["canonical representation"]
#                 row.insert(0, cluster_membership[row_id]['confidence'])
#                 row.insert(0, cluster_id)
#                 for key in canonical_keys:
#                     row.append(canonical_rep[key].encode('utf8'))
#             else:
#                 row.insert(0, None)
#                 row.insert(0, singleton_id)
#                 singleton_id += 1
#                 for key in canonical_keys:
#                     row.append(None)
#             writer.writerow(row)


def space_to_nan():
    df=pd.read_csv("tmp\\binary_features.csv")
    binary_headers=dict((el,0) for el in list(df)[1:])
    df=pd.read_csv("tmp\\deduped_carspecs_temp.csv")
    headers = list(df)
    df = df.fillna('')
    df.to_csv("tmp\\deduped_carspecs_temp.csv")

def uncamelize(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def is_nan(entry):
    return (type(entry)==float and pd.isna(entry)) or  (type(entry)==str and not entry.strip())

def count_missing_column(df, col):
    cnt = 0;
    for i in df[col]:
        if is_nan(i):
            cnt+=1
    return cnt


def print_types(df,col_name):
    temp_set = set([type(i) for i in df[col_name]])
    print(temp_set)

def find_types_of_table(df):
    col_names = list(df)
    final=[]
    for col_name in col_names:
        temp_set = set([type(i) for i in df[col_name] if not is_nan(i)])
        if len(temp_set)>1:
            print("Not good, more than one actual types exists in a column",temp_set, col_name)
            exit(0)
        elif len(temp_set)==0:
            final+=["empty"]
        else:
            final += [list(temp_set)[0].__name__]

    dff=pd.DataFrame([final], columns=col_names)
    return dff

def find_type_of_column(df, col_name):
    print("find_type_of_column()")
    temp_set = set([type(i) for i in df[col_name] if not is_nan(i)])
    if not temp_set or len(temp_set)>1:
        print("all nulls or len set too big")
    else:
        return list(temp_set)[0].__name__

def find_uniqueness(df, colname):
    tempset=set([entry for entry in df[colname] if not is_nan(entry)])
    try:
        res=float(len(tempset))/float(len(df[colname]))
    except(ZeroDivisionError):
        print(ZeroDivisionError)
        exit(0)
    return res

def fill_na(df):

    col_names = list(df)
    for col_name in col_names:

        #replace with NaN
        if gnl.app.config["CURRENT_COLUMN_TYPES"][col_name][0] =="str":
            df[col_name] = df[col_name].replace(np.nan, 'NaN')
        elif gnl.app.config["CURRENT_COLUMN_TYPES"][col_name][0] =="empty":
            df[col_name] = df[col_name].astype(str).replace(np.nan, 'nan')
        #replace with mean
        else:
            temp=df[col_name].mean()
            df[col_name] = df[col_name].replace(np.nan, temp)
    return df

def get_keywords(df):
    col_names = list(df)

    keywords = {}
    for col_name in col_names:
        if not len(col_name.strip()): continue
        col_name = col_name.replace(" ", "_")

        # possible camel case
        if "_" not in col_name:
            col_name = uncamelize(col_name)
        for i in col_name.split("_"):
            if has_alp(i) and not is_stopword(i) and len(i)!=1:
                if i.title() not in keywords:
                    keywords[i.title()] = 1
                else:
                    keywords[i.title()] += 1
    return [k for k in sorted(keywords, key=lambda k: keywords[k],reverse=True)]


def normalize_colnames(df):
    col_names = list(df)
    tmp = {}
    for col_name in col_names:
        tmp_str=deepcopy(col_name)

        if "_" not in tmp_str:
            tmp_str = uncamelize(tmp_str)
        tmp_col_name=re.sub("[ ,.]", "_", tmp_str)
        tmp_col_name=re.sub("_+", "_", tmp_col_name)
        # tmp_col_name=tmp_str.strip().replace(" ", "_").replace(",", "_").replace(".", "_").replace("__", "_").lower()
        tmp[col_name] = tmp_col_name
    df.rename(columns=tmp, inplace=True)

#clean the non consistent types in each column due to NaN
def clean_csv(df, dest):
    cs = list(df)[3:]
    dff=find_types_of_table(df)
    for c in cs:
        for i, r in enumerate(df[c]):
            if type(r)==str and "#name" in r.lower().strip():
                for j, rr in enumerate(df[c]):
                    df.at[j, c]=np.nan
                break
            if dff[c][0]=="str" and type(r)!=str:
                df.at[i, c] = " "
            if dff[c][0]=="int" and type(r)==int:
                df.at[i, c] = float(r)
    df.to_csv(dest)

def to_space_delimited(df):
    cs = list(df)
    for c in cs:
        for index, entry in enumerate(df[c]):
            if type(entry)==str:
                df.at[index, c]=entry.replace(" ","_").replace("\n\n\n", "\r").replace("\n\n", "\r").\
                    replace("\n", "\r").replace("\r\r\r", "\r").replace("\r\r", "\r")
    df.to_csv("tmp\\deduped_carspecs_temp_temp_space_ready.csv")
    thefile = open('test.dat', 'w+')
    for row in df.iterrows():
        index, data = row
        thefile.write(" ".join(
            [str(i) if not pd.isna(i) else "_" for i in data.tolist()]) + " \n")
    thefile.close()

def is_float(text):
    try:
        if(type(text)==int or type(text)==float): return True
        float(text)
        # check for nan/infinity etc.
        if text.isalpha():
            return False
        return True
    except ValueError:
        return False

def move_large_dataclean(df):
    print("\nCLEAN\n")
    cs = list(df)
    for c in cs:

        # " " is str, "hello" is str
        found_str=False

        ## need edit decimals
        for i, r in enumerate(df[c]):

            # "abc$12345" is string
            if type(r)==str and not is_float(r.strip().replace(",","").replace("$","")):
                found_str=True
                break

        if not found_str:
            for i, r in enumerate(df[c]):
                if type(r) == str:
                    df.at[i, c] = float(r.strip().replace(',', '').replace('$', ''))

                    # int also gets converted to float
            df[c]=df[c].astype(float)
        else:
            for i, r in enumerate(df[c]):
                if type(r) == str:
                    # need edit
                    # todo try different
                    # df.at[i, c] = r.strip().replace(",", "_")
                    ###.replace(" ", "_")
                    #replace("\r\n", "\n").replace("\r\r\r", "\n").replace("\r\r", "\n").replace("\r", "\n"). \
                        #replace("\n\n\n", "\n").replace("\n\n", "\n").

                    df.at[i, c] = r.strip().replace(",", "_").replace("\n", "(<space>)").replace("\r", "(<space>)")

def check_special_char(df):
    cs = list(df)
    for c in cs:
        for i, r in enumerate(df[c]):
            if type(r)==str and ("\n" in r or '\r' in r or "\t" in r):
                print(i,c,r)
                exit(0)
def clean_comma(df):
    cs = list(df)
    for c in cs:
        for i, r in enumerate(df[c]):
            if type(r) == str and ("," in r):
                # print("yes", i,r)
                df.at[i, c] = r.replace(",", "_")

def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def move_large_data(src, dest, chunk_size=1024):
    f_src=open(src)
    with open(dest, 'w+') as f_dest:
        for piece in read_in_chunks(f_src,chunk_size):
            f_dest.write(piece)


def get_corr_ranking(df, other_attribute_currentValues, protected_currentValues):
    # path = os.path.join(
    #     gnl.app.config["UPLOAD_FOLDER"],
    #     "all_types.csv"
    # )
    # dff=gnl.app.config["CURRENT_COLUMN_TYPES"]
    print("corr rank", df)
    d = {}

    res=[]
    # col_names=other_attribute_currentValues
    for i in range(len(other_attribute_currentValues)):
        tmp_list=[]
        for j in range(len(protected_currentValues)):
            try:
                cor=df[other_attribute_currentValues[i]].corr(df[protected_currentValues[j]])
                tmp_list.append(cor if not pd.isna(cor) else 101)
                # if not pd.isna(cor):
                #     d[' --- '.join([other_attribute_currentValues[i], protected_currentValues[j]])] = cor
            except:
                print("no good corr")
                print(other_attribute_currentValues[i],"|",protected_currentValues[j])
                exit(0)
        res.append(tmp_list)
    #             (k, d[k])
    #top 10
    return res

    # return [str(k)+"=>"+str(d[k]) for k in sorted(d, key=lambda dict_key: abs(d[dict_key]), reverse=True)]

    # return [ str(k)+"=>"+str(d[k]) for k in sorted(d, key=d.get, reverse=True)[0:10]]
#if dff[col_names[i]][0]!="str" and dff[protected_currentValues[i]][0]!="str" and\
                    # dff[col_names[i]][0]!="empty" and dff[col_names[j]][0]!="empty":
def clean(df):
    cs = list(df)
    # dff=find_types_of_table(df)
    num1_pattern, num2_pattern=r"^[-+]?[0-9]*\.?[0-9]+$", r"^[-+]?[0-9]*\.?[0-9]+[eE][-+]?[0-9]+$"
    for c in cs:
        found=False
        ##need edit decimals
        for i, r in enumerate(df[c]):
            if type(r)==str :
                entry = re.sub("[ ,$]", "", r)
                if not re.match(num1_pattern,entry) and not re.match(num2_pattern,entry):
                    found=True
                    break
        if not found:
            for i, r in enumerate(df[c]):
                if type(r) == str:
                    print("cur: ", r)
                    entry=re.sub(r"[ ,$]","",r)
                    if re.match(num1_pattern, entry) or re.match(num2_pattern, entry):
                        df.at[i, c] = entry
            df[c]=df[c].astype(float)
        else:
            for i, r in enumerate(df[c]):
                if type(r) == str and ("\n" in r or '\r' in r or "," in r or " " in r):
                    df.at[i, c]=re.sub("[ ,]","_",r.strip())
                    df.at[i, c]=re.sub("\r+","",df.at[i, c])
                    df.at[i, c]=re.sub("\n+","***",df.at[i, c])