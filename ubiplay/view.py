# Python 2/3 compatibility
from __future__ import division, absolute_import, print_function, unicode_literals

from flask import Flask, abort, render_template, url_for, Response, redirect

import core


app = Flask(__name__)


def url_for_entry(entry):
    return url_for("index", filepath=entry.path)


def raw_url_for_entry(entry):
    return url_for("raw", filepath=entry.path)


@app.route("/")
@app.route("/view")
@app.route("/view/")
@app.route("/view/<path:filepath>")
def index(filepath=""):
    content = core.get_content(filepath)
    if content is None:
        abort(404)
    if isinstance(content, core.DirContent):
        breadcrumbs = core.get_breadcrumbs(filepath)
        return render_template("index.html", breadcrumbs=breadcrumbs, content=content, url_for_entry=url_for_entry, raw_url_for_entry=raw_url_for_entry)
    else:
        parent_filepath = core.get_parent_filepath(filepath)
        up_url = url_for("index", filepath=parent_filepath)
        return render_template("view.html", up_url=up_url, content=content, raw_url=raw_url_for_entry(content.entry))


@app.route("/raw/<path:filepath>")
def raw(filepath):
    lst = core.get_raw(filepath)
    if lst is None:
        abort(404)
    data, mimetype = lst
    return Response(data, content_type=mimetype)

@app.route("/favicon.ico")
def favicon():
    return redirect("/static/favicon.ico", 301)
