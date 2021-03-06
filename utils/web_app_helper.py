# -*- coding: utf-8 -*-

import datetime, json, os, pprint
import flask, requests


class WebAppHelper( object ):
    """ Contains support functions for usep_gh_handler.py """

    def __init__( self, log ):
        """ Settings. """
        self.log = log

    def log_github_post( self, flask_request ):
        """ Logs data posted from github.
            Called by usep_gh_handler.handle_github_push() """
        post_data_dict = {
            u'datetime': datetime.datetime.now(),
            u'args': flask_request.args,
            u'cookies': flask_request.cookies,
            u'data': flask_request.data,
            u'form': flask_request.form,
            u'headers': unicode(repr(flask_request.headers)),
            u'host': flask_request.host,
            u'method': flask_request.method,
            u'path': flask_request.path,
            u'remote_addr': flask_request.remote_addr,
            u'values': flask_request.values,
            }
        self.log.debug( u'in utils.processor.log_github_post(); post_data_dict, `%s`' % pprint.pformat(post_data_dict) )
        return

    def trigger_dev_if_production( self, flask_request_host ):
        """ Sends github `data` to dev-server if this is the production-server.
            Called by usep_gh_handler.handle_github_push() """
        B_AUTH_PASSWORD = unicode( os.environ[u'usep_gh__BASIC_AUTH_PASSWORD'] )
        B_AUTH_USERNAME = unicode( os.environ[u'usep_gh__BASIC_AUTH_USERNAME'] )
        DEV_URL = unicode( os.environ[u'usep_gh__DEV_URL'] )
        PRODUCTION_HOSTNAME = unicode( os.environ[u'usep_gh__PRODUCTION_HOSTNAME'] )
        if flask_request_host == PRODUCTION_HOSTNAME:
            self.log.debug( u'in usep_gh_handler.handle_github_push(); gonna hit dev, too' )
            self.log.debug( u'in usep_gh_handler.handle_github_push(); type(flask.request.data), `%s`' % type(flask.request.data) )
            payload = flask.request.data
            r = requests.post( DEV_URL, data=payload, auth=(B_AUTH_USERNAME, B_AUTH_PASSWORD) )
        return

    def prep_data_dict( self, flask_request_data ):
        """ Prepares the data-dict to be sent to run_call_git_pull().
            Called by usep_gh_handler.handle_github_push() """
        self.log.debug( u'in processor.prep_data_dict(); flask_request_data, `%s`' % flask_request_data )
        files_to_process = { u'files_updated': [], u'files_removed': [], u'timestamp': unicode(datetime.datetime.now()) }
        if flask_request_data:
            commit_info = json.loads( flask_request_data )
            ( added, modified, removed ) = self._examine_commits( commit_info )
            files_to_process[u'files_updated'] = added
            files_to_process[u'files_updated'].extend( modified )  # solrization same for added or modified
            files_to_process[u'files_removed'] = removed
        self.log.debug( u'in processor.prep_data_dict(); files_to_process, `%s`' % pprint.pformat(files_to_process) )
        return files_to_process

    def _examine_commits( self, commit_info ):
        """ Extracts and returns file-paths for the different kinds of commits.
            Called by prep_data_dict(). """
        added = []
        modified = []
        removed = []
        for commit in commit_info[u'commits']:
            added.extend( commit[u'added'] )
            modified.extend( commit[u'modified'] )
            removed.extend( commit[u'removed'] )
        return ( added, modified, removed )

    ## end class WebAppHelper()
