# -*- coding: utf-8 -*-

import datetime, json, os, pprint, urlparse
import flask, redis, requests, rq
from flask.ext.basicauth import BasicAuth  # http://flask-basicauth.readthedocs.org/en/latest/
from usep_gh_handler_app.utils import log_helper, reindex_all_support
from usep_gh_handler_app.utils.web_app_helper import WebAppHelper


## setup
B_AUTH_PASSWORD = unicode( os.environ[u'usep_gh__BASIC_AUTH_PASSWORD'] )
B_AUTH_USERNAME = unicode( os.environ[u'usep_gh__BASIC_AUTH_USERNAME'] )
app = flask.Flask(__name__)
log = log_helper.setup_logger()
app.config[u'BASIC_AUTH_USERNAME'] = B_AUTH_USERNAME
app.config[u'BASIC_AUTH_PASSWORD'] = B_AUTH_PASSWORD
basic_auth = BasicAuth(app)
app_helper = WebAppHelper( log )
q = rq.Queue( u'usep', connection=redis.Redis() )


@app.route( u'/reindex_all/', methods=[u'GET'] )
@basic_auth.required
def reindex_all():
    """ Triggers a git-pull and a re-index of everything.
        Called via admin. """
    try:
        log.debug( u'in usep_gh_handler.reindex_all(); starting' )
        q.enqueue_call (
            func=u'usep_gh_handler_app.utils.reindex_all_support.run_call_simple_git_pull',
            kwargs = {} )
        return u'pull and reindex initiated.', 200
    except Exception as e:
        log.error( u'in usep_gh_handler.reindex_all(); error, `%s`' % unicode(repr(e)) )


@app.route( u'/', methods=[u'GET', u'POST'] )
@app.route( u'/force/', methods=[u'GET', u'POST'] )  # for testing
@basic_auth.required
def handle_github_push():
    """ Triggers queue jobs: github pull, file copy, and index updates.
        Called from github push webhook.
        TODO: remove GET, now used for testing. """
    try:
        log.debug( u'in usep_gh_handler.handle_github_push(); starting (basic-auth successful)' )
        app_helper.log_github_post( flask.request )
        app_helper.trigger_dev_if_production( flask.request.host )  # github can only hit production; we want dev updated, too
        if flask.request.data or u'force' in flask.request.path:
            files_to_process = app_helper.prep_data_dict( flask.request.data )  # returns dict of lists; files_updated, files_removed
            q.enqueue_call (
                func=u'usep_gh_handler_app.utils.processor.run_call_git_pull',
                kwargs = {u'files_to_process': files_to_process} )
        return u'received', 200
    except Exception as e:
        log.error( u'in usep_gh_handler.handle_github_push(); error, `%s`' % unicode(repr(e)) )
