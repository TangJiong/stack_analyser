# -*- coding:utf-8 -*-
from flask import Flask, render_template, request
from controller import *

__author__ = 'tangjiong'

app = Flask(__name__)

# ===================== 所有页面的路由 =========================


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index.html')
def overview():
    return render_template('index.html')


@app.route('/shares.html')
def percentage():
    return render_template('shares.html')


@app.route('/trend.html')
def trend():
    return render_template('trend.html')


@app.route('/customtrend.html')
def customtrend():
    return render_template('customtrend.html')


@app.route('/customshares.html')
def customshares():
    return render_template('customshares.html')


@app.route('/customquery.html')
def customquery():
    return render_template('customquery.html')


@app.route('/tag.html')
def tag():
    tagname = request.args.get('tagname', '')
    return render_template('tag.html', tagname=tagname)

# ==============================================================

# ========================== api列表 ===========================


@app.route('/toprank', methods=['GET', 'POST'])
def toprank():
    if request.method == 'POST':
        period = request.form['period']
        top = request.form['top']
        return get_toprank(period, top)
    else:
        return 'invalid method'


@app.route('/topshares', methods=['GET', 'POST'])
def topshares():
    if request.method == 'POST':
        period = request.form['period']
        top = request.form['top']
        return get_topshares(period, top)
    else:
        return 'invalid method'


@app.route('/toptrend', methods=['GET', 'POST'])
def toptrend():
    if request.method == 'POST':
        recent = request.form['recent']
        period = request.form['period']
        top = request.form['top']
        return get_toptrend(recent, period, top)
    else:
        return 'invalid method'


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        return search_tag(keyword)
    else:
        return 'invalid method'


@app.route('/top_tags', methods=['GET', 'POST'])
def top_tags():
    if request.method == 'POST':
        size = request.form['size']
        return get_top_tags(int(size))
    else:
        return 'invalid method'


@app.route('/tag_info', methods=['GET', 'POST'])
def tag_info():
    if request.method == 'POST':
        tagname = request.form['tagname']
        recent = request.form['recent']
        return get_tag_info(tagname, recent)
    return 'invalid method'


@app.route('/custom_trend', methods=['GET', 'POST'])
def custom_trend():
    if request.method == 'POST':
        taglist = json.loads(request.form['taglist'])
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        return get_custom_trend(taglist, start_date, end_date)
    return 'invalid method'


@app.route('/custom_shares', methods=['GET', 'POST'])
def custom_shares():
    if request.method == 'POST':
        taglist = json.loads(request.form['taglist'])
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        return get_custom_shares(taglist, start_date, end_date)
    return 'invalid method'


# ==============================================================


if __name__ == '__main__':
    app.run(debug=False)
