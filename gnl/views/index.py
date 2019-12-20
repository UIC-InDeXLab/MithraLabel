"""
gnl index (main) view.
URLs include:
/
"""
import os
import shutil
import hashlib
import tempfile
# import json
# import uuid
import flask
import pandas as pd
# from flask import session
from flask import request
from flask import redirect
from flask import url_for
# from flask import g
from flask import render_template
# import arrow
import gnl
# import numpy as np
# from gnl.api import likes
from gnl.views import helper
# from random import randint, uniform

# cache=[]
# inc=0
def sha1sum(filename):
    """Return sha1 hash of file content, similar to UNIX sha1sum."""
    content = open(filename, 'rb').read()
    sha1_obj = hashlib.sha1(content)
    return sha1_obj.hexdigest()

@gnl.app.route('/', methods=['GET', 'POST'])
def index():
    # return redirect(url_for('selection'))
    # print("cur dir", os.getcwd())
    # print("os path", gnl.app.config["UPLOAD_FOLDER"])
    # cache["a"]=np.random.randint(2, size=2)
    # cache.append(1)
    # print("cache index", cache)
    # uid=request.cookies.get('YourSessionCookie')
    context = {"options":[{ "label": "1","value": "Alabama"}, { "label": "2","value": "Alabama"}]}

    gnl.app.config["CURRENT_FILE"]=None
    gnl.app.config["CURRENT_IGNORED_COLUMNS"]=[]
    gnl.app.config["CURRENT_SELECTION"]={}
    gnl.app.config["CURRENT_DF"]=None
    gnl.app.config["CURRENT_COLUMN_TYPES"]=None
    gnl.app.config["CURRENT_MANUAL_INFO"]=None
    gnl.app.config["CURRENT_DF_WITH_IGNORED_COLUMNS"]=None
    gnl.app.config["CURRENT_LOADED"]=False
    gnl.app.config['NUM_MISSING']=0

    # return redirect(url_for('selection'))

    # session["CURRENT_LOADED"] = True
    # return render_template("selection.html")
    # gnl.app.config["CURRENT_FILE"] = os.path.join(
    #         gnl.app.config["UPLOAD_FOLDER"],
    #         "RecidivismData_Original.csv"
    # )

    # return redirect(url_for('selection'))
    print("\n**index**\n")

    if request.method == "POST":
        print("\n**index post**\n")
        # print("requests", request)
        # print("requests files", request.files)
        # print("request.form", request.form)
        # print("task", type(request.form.get('task')))
        # print(request.form.get('task'))

        # read task button

        gnl.app.config['TASK'] = request.form.get('task')
        if request.files and not "submit2" in request.form:
            # Save POST request's file object to a temp file
            dummy, temp_filename = tempfile.mkstemp()
            # print("flask.request.files:", flask.request.files)
            file_name = flask.request.files["filee"]
            file_name.save(temp_filename)
            # print("file_name:",file_name)
            # Compute filename with sha256 for encoding
            hash_txt = sha1sum(temp_filename)
            dummy, suffix = os.path.splitext(file_name.filename)
            hash_filename_basename = hash_txt + suffix
            hash_filename = os.path.join(
                gnl.app.config["UPLOAD_FOLDER"],
                hash_filename_basename
            )

            # Move temp file to permanent location
            print("start moving")

            shutil.move(temp_filename, hash_filename)
            gnl.app.logger.debug("Saved %s", hash_filename_basename)
            # print(hash_filename)

            # ###move csv to data folder
            # shutil.move(temp_filename, os.path.join(
            #     gnl.app.config["DATA_FOLDER"],
            #     hash_filename_basename
            # ))
            # ###

            gnl.app.config["CURRENT_FILE"] = hash_filename

            print("\n**leaving index**\n")
        else:
            gnl.app.config["CURRENT_FILE"] = os.path.join(
                gnl.app.config["UPLOAD_FOLDER"],
                request.form.get('sel')
            )
        return redirect(url_for('selection'))
    return render_template("index.html", **context)

@gnl.app.route('/selection/', methods=['GET', 'POST'])
def selection():
    print("\n**selection**\n")

    # tmp={
    #     "Functional Dependencies": {
    #         "prediction": 0,
    #         "clustering": 0,
    #         "ranking": 0,
    #         "classification": 0,
    #         "selection_and_labeling": 0
    #     },
    #     "Correlations": {
    #         "prediction": 0,
    #         "clustering": 0,
    #         "ranking": 0,
    #         "classification": 0,
    #         "selection_and_labeling": 0
    #     },
    #     "Association Rules": {
    #         "prediction": 0,
    #         "clustering": 0,
    #         "ranking": 0,
    #         "classification": 0,
    #         "selection_and_labeling": 0
    #     },
    #     "Maximal Uncovered Patterns": {
    #         "prediction": 0,
    #         "clustering": 0,
    #         "ranking": 0,
    #         "classification": 0,
    #         "selection_and_labeling": 0
    #     }
    # }
    # with open(os.path.join(gnl.app.config["DATA_FOLDER"], "params.json"), "w") as write_file:
    #     json.dump(tmp, write_file)
    # print("sel table", )
    # if gnl.app.config["CURRENT_LOADED"]:
    #     print("LOADED")
    #     gnl.app.config["CURRENT_COLUMN_TYPES"] = pd.read_csv(os.path.join(
    #         gnl.app.config["UPLOAD_FOLDER"],
    #         "()types().csv"
    #     ))
    #     gnl.app.config["CURRENT_DF"]=pd.read_csv(os.path.join(
    #         gnl.app.config["UPLOAD_FOLDER"],
    #         "()cleaned().csv"
    #     ))
    #     return render_template("label.html")
    ########
    # gnl.app.config["CURRENT_FILE"] = os.path.join(
    #     gnl.app.config["UPLOAD_FOLDER"],
    #     "RecidivismData_Original.csv"
    # )

    # gnl.app.config["CURRENT_DF"]=pd.read_csv(os.path.join(
    #     gnl.app.config["DATA_FOLDER"],
    #     "numeric.csv"))
    # gnl.app.config["CURRENT_DF_WITH_IGNORED_COLUMNS"] = pd.read_csv(os.path.join(
    #     gnl.app.config["DATA_FOLDER"],
    #     "complete.csv"))
    ##########

    # context={}
    df=pd.read_csv(gnl.app.config["CURRENT_FILE"])
    #
    # # standardize the column names
    helper.normalize_colnames(df)
    #
    # # clean the strings that are actually numbers and also invalid string such as those with comma and special chars, or $
    df.to_csv(os.path.join(
        gnl.app.config["UPLOAD_FOLDER"],
        "()cleaned().csv"
    ), index=False)
    # print("selelction")
    # print("df", df)

    gnl.app.config["CURRENT_DF"] = df

    # find types of each col for convenience
    gnl.app.config["CURRENT_COLUMN_TYPES"] = helper.find_types_of_table(df)
    gnl.app.config["CURRENT_COLUMN_TYPES"].to_csv(os.path.join(
        gnl.app.config["UPLOAD_FOLDER"],
        "()types().csv"
    ), index=False)

    print("\n**Leaving selection**\n")

    gnl.app.config["CURRENT_LOADED"] = True
    return render_template("label.html")