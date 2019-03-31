from pymongo import MongoClient
from flask import Flask, render_template, request, url_for

import re


app = Flask(__name__)
title = "List of Web Services"
heading = "Search from API collection as per below criteria (any 1):"

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.mymongodb
api_table = db.apiTable
mashup_table = db.mashupTable


@app.route("/", methods = ['GET','POST'])
def index():

    return render_template('index.html', t=title, h=heading)


def redirect_url():
    return request.args.get('next') or request.referrer or url_for('index')

# API


@app.route("/api_year", methods=['POST'])
def api_year():
    result = []
    api_year = request.form['api_year']
    query = {"year": {"$regex": "^" + api_year + ".*"}}
    temp_result = api_table.find(query)
    for records in temp_result:
        result.append(records["name"])
    return render_template('apiResult.html', result=result, t=title, h=heading)


@app.route("/api_protocol", methods=['POST'])
def api_protocol():
    result = []
    api_protocol = str.upper(request.form['api_protocol'])
    query = {"protocols": {"$regex": "^" + api_protocol}}
    temp_result = api_table.find(query)
    for records in temp_result:
        result.append(records["name"])
    return render_template('apiResult.html', result=result, t=title, h=heading)


@app.route("/api_category", methods=['POST'])
def api_category():
    result=[]
    api_category = request.form['api_category']
    query = {"category": {"$regex": "^" + api_category}}
    temp_result = api_table.find(query)
    for records in temp_result:
        result.append(records["name"])
    return render_template('apiResult.html', result=result, t=title, h=heading)


@app.route("/api_rating", methods=['POST'])
def api_rating():
    result = []
    api_rating = request.form['api_rating']

    if list(api_rating)[0] == "<":
        query = {"rating": {"$lt": list(api_rating)[1]}}
    elif list(api_rating)[0] == ">":
        query = {"rating": { "$gt": list(api_rating)[1]}}
    else:
        query = {"rating": {"$regex": "^" + list(api_rating)[1]}}

    temp_result = api_table.find(query)
    for records in temp_result:
        result.append(records["name"])

    return render_template('apiResult.html', result=result, t=title, h=heading)


@app.route("/api_tag", methods=['POST'])
def api_tags():
    result = []
    api_tags = request.form['api_tag']
    query = {"tags": {"$regex": api_tags, "$options": "$i"}}
    temp_result = api_table.find(query)
    for records in temp_result:
        result.append(records["name"])

    return render_template('apiResult.html', result=result, t=title, h=heading)


@app.route("/api_keyword", methods=['POST'])
def api_keyword():
    result = []
    api_keyword = request.form['api_keyword']
    #api_year = request.values.get("year")
    keywords = api_keyword.split(",")
    for i in keywords:
        query = {"$or": [{"title": {"$regex": i}}, {"summary": {"$regex": i}},
                          {"description": {"$regex": i}}]}
        temp_result = api_table.find(query)
        for records in temp_result:
            result.append(records["name"])
    return render_template('apiResult.html', result=result, t=title, h=heading)


# MASHUP

@app.route("/mashup_year", methods=['POST'])
def mashup_year():
    result = []
    mashup_year = request.form['mashup_year']
    query = {"year": {"$regex": "^" + mashup_year + ".*"}}
    temp_result = mashup_table.find(query)
    for records in temp_result:
        result.append(records["name"])

    return render_template('apiResult.html', result=result, t=title, h=heading)


@app.route("/mashup_api", methods=['POST'])
def mashup_api():
    result = []
    mashup_api = request.form['mashup_api']
    query = {"api": {"$regex": str(mashup_api), "$options": "$i"}}
    temp_result = mashup_table.find(query)
    for records in temp_result:
        result.append(records["name"])

    return render_template('apiResult.html', result=result, t=title, h=heading)


@app.route("/mashup_tag", methods=['POST'])
def mashup_tags():
    mashup_tags = request.form['mashup_tag']
    query = {"tags": {"$regex": mashup_tags, "$options": "$i"}}
    result = []
    temp_result = mashup_table.find(query)
    for records in temp_result:
        result.append(records["name"])
    return render_template('apiResult.html', result=result, t=title, h=heading)


@app.route("/mashup_keyword", methods=['POST'])
def mashup_keyword():
    result = []
    mashup_keyword = request.form['mashup_keyword']
    keywords = mashup_keyword.split(",")
    for keyword in keywords:
        query = {"$or": [{"title": {"$regex": keyword}}, {"summary": {"$regex": keyword}}, {"description": {"$regex": keyword}}]}
        temp_result = mashup_table.find(query)
        for records in temp_result:
            result.append(records["name"])
    return render_template('apiResult.html', result=result, t=title, h=heading)


def main():
    # Field tag in api.txt file
    api_fields = ["id", "title", "summary", "rating", "name", "label", "author", "description",
                  "type", "downloads", "useCount", "sampleUrl", "downloadUrl", "dateModified", "remoteFeed",
                  "numComments", "commentsUrl", "tags", "category", "protocols", "serviceEndPoint",
                  "version", "wsdl", "data_formats", "api_groups", "example", "clientInstall", "authentication",
                  "ssl", "readonly", "vendorApiKits", "communityApiKits", "blog", "forum", "support", "accountReq",
                  "commercial", "provider", "managedby", "nonCommercial", "dataLicensing", "fees", "limits", "terms",
                  "company", "year"]

    # Record tag in mashup.txt file
    mashup_fields = ["id", "title", "summary", "rating", "name", "label", "author", "description", "type",
                     "downloads", "useCount", "sampleUrl", "dateModified", "numComments", "commentsUrl", "tags", "api",
                     "year"]

    api_txt = open('api.txt', 'r', encoding="ISO-8859-1")

    list_of_tags = []
    for line in api_txt:
        line.split("$#$")
        #line = re.sub('[#]', ' ', line)

        api_temp = dict(zip(api_fields, line))
        list_of_tags.append(api_temp)

    api_table.insert_many(list_of_tags)

    mashup_txt = open('mashup.txt', 'r', encoding="ISO-8859-1")

    list_of_tags = []
    for line in mashup_txt:
        line.split("$#$")
        line.strip("###")
        mashup_temp = dict(zip(mashup_fields, line))
        list_of_tags.append(mashup_temp)

    mashup_table.insert_many(list_of_tags)

    app.run(debug=True)


if __name__ == '__main__':
    main()
