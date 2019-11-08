"""
Author: sunshicheng
DateTime : 2019-11-08 08:32
File : main.py

尝试使用flask处理页面，解析视频

"""

from flask import Flask, render_template, session, redirect, flash,url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = 'hard to guess string'


class UrlForm(FlaskForm):
    url = StringField('输入需要解析的url:', validators=[DataRequired()])
    submit = SubmitField('立即播放', validators=[DataRequired()])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UrlForm()
    if form.validate_on_submit():
        old_url = session.get('url')
        if old_url is not None and old_url != form.url.data:
            flash('解析成功，欢迎观看')
        session['url'] = form.url.data
        form.url.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(),form=form, url=session.get('url'))
