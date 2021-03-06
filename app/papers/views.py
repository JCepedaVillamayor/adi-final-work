from . import papers
from ..models import Paper
from ..auth import auth
from flask import g, make_response, request, jsonify, abort
from urllib import unquote_plus
from google.appengine.ext import ndb
import re


def check_all_elements(elements):
    return all(elem is not None for elem in elements)


@auth.login_required
def post_paper():
    if not request.json:
        abort(400)
    author_id = request.json.get('author')
    title = request.json.get('title')
    paper_type = request.json.get('type')

    if check_all_elements([author_id, title, paper_type]) is not True:
        abort(400)

    author = ndb.Key('Author', author_id)
    if author.get() is None:
        abort(400)

    if paper_type in ['congress', 'journal']:
        new_paper = Paper(title=title,
                          author=author,
                          paper_type=paper_type)
    else:
        abort(400)

    paper_id = new_paper.put()
    return make_response(jsonify({'created': paper_id.urlsafe()}), 200)


def get_paper(paper_id):
    try:
        paper_key = ndb.Key(urlsafe=paper_id)
    except:
        abort(404)
    if paper_key.get() is None:
        abort(404)
    paper = paper_key.get()
    return make_response(jsonify(paper.toJSON), 200)


@auth.login_required
def delete_paper(paper_id):
    paper = None
    try:
        paper = ndb.Key(urlsafe=paper_id)
    except:
        abort(404)
    if paper.get() is None:
        abort(404)
    paper.delete()
    return make_response(jsonify({'removed': paper.urlsafe()}), 200)


@papers.route('/papers/type/<paper_type>', methods=['GET'])
def request_papers(paper_type):
    if paper_type not in ['congress', 'journal']:
        abort(400)
    papers = Paper.getAll()
    new_papers = []
    for paper in papers:
        if paper['type'] == paper_type:
            new_papers.append(paper)
    return make_response(jsonify(new_papers), 200)

@papers.route('/papers/<paper_id>', methods=['DELETE', 'GET'])
def handle_papers(paper_id):
    if request.method == 'DELETE':
        return delete_paper(paper_id)
    if request.method == 'GET':
        return get_paper(paper_id)


@papers.route('/papers', methods=['POST', 'GET'])
def get_or_post_papers():
    if request.method == 'POST':
        return post_paper()
    if request.method == 'GET':
        return make_response(jsonify(Paper.getAll()), 200)
