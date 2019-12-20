"""REST API for likes."""
import flask
import gnl
# from flask import make_response
from flask import jsonify
from flask import request
import numpy as np
from gnl.views import apriori
from gnl.views.fd.utils import reader
from gnl.views.fd.utils import writer
from gnl.views.fd.algorithm import tane
from gnl.views import helper
# from statistics import mean, median
# import pandas as pd
import os
import json
# import pprint
from pprint import pprint
import pandas as pd
from jpype import *
import random
from copy import deepcopy
# import datetime

"""you might end up refactoring parts of this code later 
to avoid copy-pasted code shared between the REST API and 
server-side template views."""




@gnl.app.route('/api/sel/', methods=['GET', 'POST'])
def get_sel():
    print("\n***access get sel***\n")
    context = {}
    context["sel"] = gnl.app.config["CURRENT_SELECTION"]["widget_currentValues"] if "widget_currentValues" in \
                                                                                    gnl.app.config[
                                                                                        "CURRENT_SELECTION"] else []

    df=gnl.app.config["CURRENT_DF_WITH_IGNORED_COLUMNS"]
    dff = gnl.app.config["CURRENT_COLUMN_TYPES"]

    sel = gnl.app.config["CURRENT_SELECTION"]
    tmp = {}
    # print("sel['protected_currentValues']: ",sel['protected_currentValues'])
    if sel["is_single_column"] and sel['protected_currentValues'] and dff[sel['protected_currentValues'][0]["label"]][0]=="str":
        for entry in df[sel['protected_currentValues'][0]["label"]]:
            if entry:
                entry=str(entry)
                if entry not in tmp:
                    tmp[entry]=0
                tmp[entry]+=1

        context["single_colname"]=sel['protected_currentValues'][0]["label"]
    context["labels"]=list(tmp.keys())
    context["values"]=[tmp[key] for key in tmp]
    context['no_numeric']=gnl.app.config['no_numeric']
    return jsonify(**context)


@gnl.app.route('/api/parse_single/', methods=['GET', 'POST'])
def get_parse_single():
    print("access get_parse_single")
    try:
        tmp = pd.read_csv(os.path.join(gnl.app.config["DATA_FOLDER"], "numeric_single.csv"))
    except pd.errors.EmptyDataError:
        context = {"re": [{"No Data Available": 0}]}
        return jsonify(**context)
    # darray=[{list(tmp)[0]:entry} for entry in tmp[list(tmp)[0]]]
    darray = []
    for index, row in tmp.iterrows():
        darray.append(dict(row))
    # print("darray: ", darray)
    context = {"re": darray}
    return jsonify(**context)


@gnl.app.route('/api/parse_multi/', methods=['GET', 'POST'])
def get_parse_multi():
    print("access get_parse_multi")
    try:
        tmp = pd.read_csv(os.path.join(gnl.app.config["DATA_FOLDER"], "numeric.csv"))
    except pd.errors.EmptyDataError:
        context = {"re": [{"No Data Available": 0}]}
        return jsonify(**context)
    # darray=[{list(tmp)[0]:entry} for entry in tmp[list(tmp)[0]]]
    darray = []
    for index, row in tmp.iterrows():
        darray.append(dict(row))
    # print("darray: ", darray)
    context = {"re": darray}
    return jsonify(**context)


@gnl.app.route('/api/form_submit/', methods=['GET', 'POST'])
def form_submit():
    print("\n***form_submit***\n")
    # here do stuff and save json
    # print("in form submit", datetime.datetime.now())
    context = {}
    if not request.json:
        flask.abort(400)

    # context['keywords'] = helper.get_keywords(df)
    # context['num_rows'] = df.shape[0]
    # context['num_cols'] = df.shape[1]
    # context['num_missing'] = gnl.app.config['NUM_MISSING']

    gnl.app.config["CURRENT_SELECTION"] = request.json
    sel = gnl.app.config["CURRENT_SELECTION"]



    # load params
    with open(os.path.join(gnl.app.config["DATA_FOLDER"], "params.json")) as f:
        table = json.load(f)


    num_widgets=int(sel['num_widgets'])


    # ~
    if sel["is_manually_widgets"]:

        # Take in selection and perform profit table change
        # print("selected widgets", sel['widget_currentValues'])
        for item in sel['widget_currentValues']:
            table[item["label"]][gnl.app.config['TASK']] += (1 / max(len(sel['widget_currentValues']),1))

        with open(os.path.join(gnl.app.config["DATA_FOLDER"], "params.json"), "w") as write_file2:
            json.dump(table, write_file2)

    widget2value = {
        "Correlations": 1,
        "Functional Dependencies": 2,
        "Association Rules": 3,
        "Maximal Uncovered Patterns": 4
    }

    # print("cur table after (optional update):")
    # pprint(table)
    if not sel["is_manually_widgets"]:
        tmp_dic = {key: table[key][gnl.app.config['TASK']] for key in table}

        #~
        sorted_widgets = [k for k in sorted(tmp_dic, key=lambda k: tmp_dic[k], reverse=True)][:num_widgets]

        if not sel['is_single_column']:
            sel['widget_currentValues'] = [{"label": k, "value": widget2value[k]} for k in sorted_widgets]
        else:
            if num_widgets==2:
                sel['widget_currentValues']=[{"label": "Correlations", "value": 1}, {"label": "Functional Dependencies", "value": 2}, ]
            elif num_widgets==1:
                sel['widget_currentValues']=[{"label": "Correlations", "value": 1}] if table['Correlations'][gnl.app.config['TASK']]>table['Functional Dependencies'][gnl.app.config['TASK']] else [{"label": "Functional Dependencies", "value": 2}, ]
            else: sel['widget_currentValues']=[]
        # sel['widget_currentValues'] = [{"label": k, "value": widget2value[k]} for k in sorted_widgets] if not sel[
        #     'is_single_column'] else [{"label": "Correlations", "value": 1},
        #                               {"label": "Functional Dependencies", "value": 2}, ]
        # print("new sel['widget_currentValues']: ", sel['widget_currentValues'])

    # record previous selections
    with open(os.path.join(gnl.app.config["DATA_FOLDER"], "prev_sel.json"), "w") as write_file:
        json.dump(sel, write_file)

    col_names = list(gnl.app.config["CURRENT_DF"])
    attribute_currentValues = [i['label'] for i in sel['attribute_currentValues']] if not sel['is_whole'] else col_names

    if sel['is_single_column']: sel['protected_currentValues'] = [sel['protected_currentValues']] if sel[
        'protected_currentValues'] else []
    protected_currentValues = [i['label'] for i in sel['protected_currentValues']]
    # if gnl.app.config["CURRENT_COLUMN_TYPES"][i['label']][0] not in ["empty"]

    all_values = list(set(attribute_currentValues + protected_currentValues))

    # slice value range first
    # print("pattrs are ", protected_currentValues)
    # print("attrs are ", attribute_currentValues)
    # select range
    if sel["is_query"]:
        print("is query")
        query_ranges = sel["query_rangeValues"]
        for key in query_ranges:

            # check the key has an existing range
            if query_ranges[key]:
                if gnl.app.config["CURRENT_COLUMN_TYPES"][key][0] != "str":
                    gnl.app.config["CURRENT_DF"] = \
                        gnl.app.config["CURRENT_DF"][
                            gnl.app.config["CURRENT_DF"][key] \
                                .between(float(query_ranges[key][0]), float(query_ranges[key][1]), inclusive=True)]
                else:
                    gnl.app.config["CURRENT_DF"] = \
                        gnl.app.config["CURRENT_DF"][
                            gnl.app.config["CURRENT_DF"][key] == query_ranges[key]]

    # then slice cols
    gnl.app.config["CURRENT_DF"] = gnl.app.config["CURRENT_DF"][all_values]

    # slicing completed, count missing before fill in nan
    if not sel["is_single_column"]:
        gnl.app.config['NUM_MISSING'] = 0
        print("in not single")
        # print(gnl.app.config["CURRENT_DF"].isnull().sum())
        for col_name in list(gnl.app.config["CURRENT_DF"]):
            for entry in gnl.app.config["CURRENT_DF"][col_name]:
                if helper.is_nan(entry):
                    gnl.app.config['NUM_MISSING'] += 1

    dff = gnl.app.config["CURRENT_COLUMN_TYPES"]

    # drop empty ones
    gnl.app.config["CURRENT_DF"].drop(columns=[col for col in list(gnl.app.config["CURRENT_DF"])
                                               if (dff[col][0] == "empty")], inplace=True)
    gnl.app.config["CURRENT_DF"] = gnl.app.config["CURRENT_DF"].fillna(method='ffill')
    # gnl.app.config['CURRENT_DF'] = helper.fill_na(gnl.app.config['CURRENT_DF'])

    # print("null 1", gnl.app.config['CURRENT_DF'].isna().sum())
    # now clean after fill na
    helper.clean(gnl.app.config['CURRENT_DF'])

    gnl.app.config["CURRENT_DF"] = gnl.app.config["CURRENT_DF"].fillna(method='ffill')
    # gnl.app.config['CURRENT_DF'] = helper.fill_na(gnl.app.config['CURRENT_DF'])
    # print("null 2", gnl.app.config['CURRENT_DF'].isna().sum())

    gnl.app.config["CURRENT_IGNORED_COLUMNS"] = []
    gnl.app.config["CURRENT_IGNORED_COLUMNS"] += [col for col in list(gnl.app.config["CURRENT_DF"])
                                                  if (dff[col][0] == "str" or dff[col][0] == "empty")]

    # print("gnl.app.config[CURRENT_IGNORED_COLUMNS]", gnl.app.config["CURRENT_IGNORED_COLUMNS"])
    # keep full dataset
    gnl.app.config["CURRENT_DF_WITH_IGNORED_COLUMNS"] = gnl.app.config["CURRENT_DF"].copy()

    # print("null in form", gnl.app.config["CURRENT_DF_WITH_IGNORED_COLUMNS"].isna().sum())

    # print("cur df", gnl.app.config["CURRENT_DF"])
    gnl.app.config["CURRENT_DF"].drop(columns=gnl.app.config["CURRENT_IGNORED_COLUMNS"], inplace=True)

    # print("s write numeric single ", datetime.datetime.now())
    # numeric single column
    if sel["is_single_column"] and sel['protected_currentValues'] and \
            dff[sel['protected_currentValues'][0]['label']][0] not in ["str", "empty"]:
        # print("in num single: ", sel['protected_currentValues'][0]['label'])
        # print(gnl.app.config["CURRENT_DF"][[sel['protected_currentValues'][0]['label']]])
        # os.remove(os.path.join(gnl.app.config["DATA_FOLDER"], "numeric_single123.csv"))
        gnl.app.config["CURRENT_DF"][[sel['protected_currentValues'][0]['label']]]. \
            to_csv(os.path.join(gnl.app.config["DATA_FOLDER"], "numeric_single.csv"), index=False)
        # gnl.app.config["CURRENT_DF"][sel['protected_currentValues'][0]['label']].to_csv(os.path.join(gnl.app.config["DATA_FOLDER"], "toy.csv"))

    # print("e write numeric single", datetime.datetime.now())
    # numeric.csv and complete.csv

    # print("s write numeric", datetime.datetime.now())
    gnl.app.config["CURRENT_DF"].to_csv(os.path.join(gnl.app.config["DATA_FOLDER"], "numeric.csv"), index=False)
    print(list(gnl.app.config["CURRENT_DF"]))


    if not list(gnl.app.config["CURRENT_DF"]):
        gnl.app.config['no_numeric']=1
    else: gnl.app.config['no_numeric']=0
    # print("e write numeric", datetime.datetime.now())
    gnl.app.config["CURRENT_DF_WITH_IGNORED_COLUMNS"].to_csv(
        os.path.join(gnl.app.config["DATA_FOLDER"], "complete.csv"), index=False)

    gnl.app.config["CURRENT_SELECTION"] = deepcopy(sel)
    # context["sel"] = sel
    # print("sel after fb: ")
    # pprint(sel["widget_currentValues"])
    return jsonify(**context)


@gnl.app.route('/api/params/', methods=['GET', 'POST'])
def set_params():
    print("\n***accessed set params\n")

    context = {}

    sel = request.json

    sys_sel = gnl.app.config["CURRENT_SELECTION"]
    num_widgets=sys_sel['num_widgets']
    # print("sel")
    # pprint(sel)

    with open(os.path.join(gnl.app.config["DATA_FOLDER"], "prev_sel.json")) as f1:
        prev_sel = json.load(f1)
        # print("prev sel")
        # pprint(prev_sel)
    with open(os.path.join(gnl.app.config["DATA_FOLDER"], "params.json")) as f2:
        table = json.load(f2)

    # if prev is label page

    tmp_dict = {
        "has_Correlation": "Correlations",
        "has_FunctionalDependency": "Functional Dependencies",
        "has_AssociationRule": "Association Rules",
        "has_Coverage": "Maximal Uncovered Patterns",
    }

    if "additional" in prev_sel:
        print("in label")
        for key in sel:
            if key in tmp_dict:
                if sel[key] != prev_sel[key]:
                    if sel[key]:
                        table[tmp_dict[key]][gnl.app.config['TASK']] += (1 / num_widgets)
                    # else:
                    #     table[tmp_dict[key]][gnl.app.config['TASK']] -= (1 / num_widgets)
    else:

        widgets = set([item['label'] for item in prev_sel['widget_currentValues']])
        new_widgets = set()
        for key in sel:
            if (key in tmp_dict) and sel[key]:
                new_widgets.add(tmp_dict[key])
        # new_widgets = set([tmp_dict[key] for key in sel if (key in tmp_dict and sel[key]))
        dif = (new_widgets - widgets).union(widgets - new_widgets)
        # print("dif")
        # pprint(dif)
        for key in dif:
            if key in new_widgets:
                table[key][gnl.app.config['TASK']] += (1 / num_widgets)
            # else:
            #     table[key][gnl.app.config['TASK']] -= (1 / num_widgets)
    with open(os.path.join(gnl.app.config["DATA_FOLDER"], "params.json"), "w") as write_file2:
        json.dump(table, write_file2)
    with open(os.path.join(gnl.app.config["DATA_FOLDER"], "prev_sel.json"), "w") as write_file1:
        json.dump(sel, write_file1)
    # print("after set cur table")
    # pprint(table)

    return jsonify(**context)


@gnl.app.route('/api/get_colnames/', methods=['GET'])
def get_colnames():
    print("\n***accessed get colnames\n")
    context = {'colnames': list(gnl.app.config["CURRENT_COLUMN_TYPES"])}
    # 'colnames': list(set(list(cur_df)) - set(gnl.app.config["CURRENT_IGNORED_COLUMNS"]))
    # print("context are", context)
    # todo
    context['str_colnames'] = [col for col in list(gnl.app.config["CURRENT_DF"])
                               if gnl.app.config["CURRENT_COLUMN_TYPES"][col][0] == "str"]
    # print(context)
    # gnl.app.config["JSON_OUT"].update(context)
    # with open(os.path.join(gnl.app.config["DATA_FOLDER"], "output.json"), 'w') as outfile:
    #     json.dump(gnl.app.config["JSON_OUT"], outfile)
    with open(os.path.join(gnl.app.config["DATA_FOLDER"], "params.json")) as f2:
        table = json.load(f2)
    names=[" "]+list(table["Functional Dependencies"].keys())
    tmp={}
    out=[]
    for key in table:
        tmp=table[key]
        tmp[" "]=key
        out.append(tmp)
    context['repr_names'] = names
    context['repr'] = out
    # pprint(context)
    context["is_demo"]=gnl.app.config["CURRENT_FILE"].split("/")[-1]=="RecidivismData_Original.csv"
    # print("now file", gnl.app.config["CURRENT_FILE"])

    return jsonify(**context)


@gnl.app.route('/api/coverage/', methods=['GET'])
def get_coverage():
    print("\n**get coverage**\n")

    # get classes
    cpopt = "-Djava.class.path=%s" % (gnl.app.config["COVERAGE_FOLDER"] + "/target/classes")
    if not isJVMStarted():
        startJVM(getDefaultJVMPath(), "-ea", cpopt)
    # print("classpath:", cpopt)

    dataset = JClass('io.DataSet')
    hybrid = JClass('search.HybridSearch')

    # read entire dataset
    df = gnl.app.config["CURRENT_DF_WITH_IGNORED_COLUMNS"].copy()
    dff = gnl.app.config["CURRENT_COLUMN_TYPES"]

    # now only for str cols
    # todo
    df = df.drop(columns=[col for col in list(df) if dff[col][0] == "empty"])
    valid_cols, valid_col_indices, cardinality, categories = [], [], [], []

    # grouping numerical
    for col in list(df):
        if dff[col][0] != "str":
            cur_col = list(df[col])
            dimension = len(set(cur_col))
            if dimension <= 9:
                df[col] = str(df[col])
            else:
                df[col] = [str(bucket) for bucket in pd.cut(cur_col, dimension)]

    for i, col in enumerate(list(df)):

        # restrict cardinality
        temp_set = set(list(df[col]))

        if len(temp_set) <= 9 and len(temp_set) >= 2:
            valid_cols.append(col)
            valid_col_indices.append(i)
            cardinality.append(len(temp_set))

            # encoding valid categorical columns
            labels, uniques = pd.factorize(list(df[col]), sort=True)
            df[col] = labels
            categories.append([col + ": " + str(unique) for unique in uniques])

    df = df[valid_cols].astype(str)
    df.to_csv(gnl.app.config["CURRENT_TEMP_FILE"], index=False)

    dataset1 = dataset(gnl.app.config["CURRENT_TEMP_FILE"], cardinality, [i for i in range(len(valid_cols))],
                       df.shape[0])

    hybrid1 = hybrid(dataset1)
    a = hybrid1.findMaxUncoveredPatternSet(30, 3)

    mups = [i.getStr() for i in a]

    ###
    # shutdownJVM()
    ###

    uncovered_patterns = []
    val_cnt = {}
    pattern_lists = []
    for i, mup in enumerate(mups):
        tmp_list = []
        for j, char in enumerate(mup):
            if char != 'x':
                tmp_list.append(categories[j][ord(char) - ord('0')])
                if categories[j][ord(char) - ord('0')] not in val_cnt:
                    val_cnt[categories[j][ord(char) - ord('0')]] = 0
                    val_cnt[categories[j][ord(char) - ord('0')]] += 1
        pattern_lists.append(tmp_list)
        uncovered_patterns.append(" ".join(tmp_list))

    # generate tree
    sprop = {"width": 20,
             "height": 20,
             "x": -10,
             "y": -10,
             "fill": 'red'}
    tree = [{"node": "patterns", "children": []}]
    if not mups: tree[0] = {"node": "no patterns discovered", "children": []}
    ptrs = [tree[0]] * len(pattern_lists)
    for i in range(len(ptrs)):
        ptrs[i] = tree[0]
    pos, cur = 0, tree[0]
    while True:
        found_at_least_one = False

        # each pattern
        for i, pattern_list in enumerate(pattern_lists):

            # sort the pattern values according to count, to minimize horizontal distance
            pattern_lists[i] = sorted(pattern_list, key=lambda x: -val_cnt.get(x))

            # if current position is still not passing the end
            if pos < len(pattern_list):
                found_at_least_one = True
                exist_node = False

                # check whether the current is already a child from the last ptr
                for j, child in enumerate(ptrs[i]["children"]):
                    if child["node"] == pattern_list[pos]:
                        exist_node = True
                        ptrs[i] = ptrs[i]["children"][j]
                        break
                if not exist_node:
                    sprop["fill"] = random.choice(["red", "blue", "green", "yellow", "purple"])
                    ptrs[i]["children"].append({"node": pattern_list[pos], "children": []})
                    ptrs[i] = ptrs[i]["children"][-1]
        pos += 1

        # if pos passed the end of all pattern lists, then stop
        if not found_at_least_one:
            break

    # to mup.json
    context = {"tree": tree}

    return jsonify(**context)


@gnl.app.route('/api/multi_basic/', methods=['GET', 'POST'])
def get_multi_basic():
    print("\n***get_multi_basic\n")
    context = {}
    # todo

    # df = gnl.app.config["CURRENT_DF_WITH_IGNORED_COLUMNS"]
    df = gnl.app.config["CURRENT_DF_WITH_IGNORED_COLUMNS"]
    context['keywords'] = helper.get_keywords(df)
    context['num_rows'] = df.shape[0]
    context['num_cols'] = df.shape[1]
    context['num_missing'] = gnl.app.config['NUM_MISSING']




    colnames=list(df)
    rand_names=np.random.choice(colnames,min(len(colnames), 5), replace =False)
    context['repr_names']=list(rand_names)
    tmp=df[rand_names].astype(str).to_dict("records")
    context['repr']=list(np.random.choice(tmp,min(len(tmp), 50), replace=False))
    # print("num missing: ", gnl.app.config['NUM_MISSING'])
    # gnl.app.config["JSON_OUT"].update(context)
    # with open(os.path.join(gnl.app.config["DATA_FOLDER"], "result.json"), 'w') as outfile:
    #     json.dump(gnl.app.config["JSON_OUT"], outfile)

    return jsonify(**context)


@gnl.app.route('/api/multi_fd/', methods=['GET', 'POST'])
def get_multi_fd():
    print("\n***get_multi_fd\n")
    context = {}
    df = gnl.app.config["CURRENT_DF_WITH_IGNORED_COLUMNS"].copy()
    col_names = list(df)

    # sampling
    if df.shape[0] * (2**df.shape[1]) > 3584000:
        df = df.sample(n=int(3584000 / (2**df.shape[1])), replace=False)

    # too many columns
    if df.empty:
        nodes, links=[{"id": "TOO MANY COLUMNS"}],[]
        context["nodes"] = nodes
        context["links"] = links
        return jsonify(**context)



    sel = gnl.app.config["CURRENT_SELECTION"]
    pattrs = [i['label'] for i in sel["protected_currentValues"]]
    cols = [i['label'] for i in sel['attribute_currentValues']] if not sel['is_whole'] else col_names

    for pattr in pattrs:
        if pattr not in cols:
            cols.append(pattr)

    # drop the spaces and commas
    df.to_csv(gnl.app.config["CURRENT_TEMP_FILE"], index=False)

    # start discovering
    table = reader.Reader.read_table_from_file(gnl.app.config["CURRENT_TEMP_FILE"], ",")
    tne = tane.TANE(table)
    tne.run()
    wt = writer.Writer(col_names)
    output = wt.write_dependency_to_file(tne.ans)
    releveant_output = [comb for comb in output if any([item in pattrs for item in comb.split("=>")[1].split(", ")])]
    if output and output[0] == "Timelimit=>Exceeded(because of too many columns)":
        releveant_output = output

    node_set, link_set, nodes, links = set(), set(), [], []
    for fd in releveant_output:
        l, r = fd.split("=>")
        # l_list,r_list=l.split(","),r.split(",")
        node_set.add(l)
        node_set.add(r)
        link_set.add((l, r))
    for node in node_set:
        nodes.append({"id": node})
    for link in link_set:
        links.append({"source": link[0], "target": link[1]})
    if not nodes: nodes.append({"id": "NONE EXISTS"})
    context["nodes"] = nodes
    context["links"] = links
    # print("fd context")
    # print(context)
    return jsonify(**context)


@gnl.app.route('/api/multi_ar/', methods=['GET', 'POST'])
def get_multi_ar():
    print("\n***get_multi_ar\n")

    context = {}
    df = gnl.app.config["CURRENT_DF_WITH_IGNORED_COLUMNS"].copy()
    col_names = list(df)

    # sel = gnl.app.config["CURRENT_SELECTION"]
    # cols = [i['label'] for i in sel['attribute_currentValues']] if not sel['is_whole'] else col_names

    ### modify so that each entry has it corresponding column name indicator
    df = df[col_names].astype(str)
    # print("prev df", df)
    for j, colname in enumerate(list(df)):
        df[colname] = colname + ":" + df[colname].astype(str)

    # sampling
    if df.shape[0] * (2**df.shape[1]) > 3584000:
        print("here")
        df = df.sample(n=int(3584000 / (2**df.shape[1])), replace=False)

    # too many columns
    if df.empty:
        nodes, links=[{"id": "TOO MANY COLUMNS"}],[]
        context["nodes"] = nodes
        context["links"] = links
        return jsonify(**context)

    # drop the spaces and commas
    df.to_csv(gnl.app.config["CURRENT_TEMP_FILE"], index=False)

    # start apriori
    a = apriori.Apriori(gnl.app.config["CURRENT_TEMP_FILE"], 0.25, -1)
    a.run()

    node_set, link_set, nodes, links = set(), set(), [], []
    for ar in a.true_associations:
        l, r = ar.split("=>")
        # l_list,r_list=l.split(","),r.split(",")
        node_set.add(l)
        node_set.add(r)
        link_set.add((l, r))
        # for i, l_item in enumerate(l_list):
        #     for j, r_item in enumerate(r_list):
        #         node_set.add(l_item)
        #         node_set.add(r_item)
        #         link_set.add((l_item, r_item))
    for node in node_set:
        nodes.append({"id": node})
    for link in link_set:
        links.append({"source": link[0], "target": link[1]})

    if not nodes: nodes.append({"id": "NO ASSOCIATION RULE EXISTS"})
    context["nodes"] = nodes
    context["links"] = links
    # print("ar context")
    # print(context)
    # gnl.app.config["JSON_OUT"].update(context)
    # with open(os.path.join(gnl.app.config["DATA_FOLDER"], "result.json"), 'w') as outfile:
    #     json.dump(gnl.app.config["JSON_OUT"], outfile)

    return jsonify(**context)
