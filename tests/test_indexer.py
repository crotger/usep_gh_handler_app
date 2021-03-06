# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging, pprint, unittest
import requests
from usep_gh_handler_app.utils.indexer import Indexer


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)
log.debug( 'test_indexer starting' )


class IndexerTest( unittest.TestCase ):
    """ Tests Indexer functions.
        To use:
        - activate the virtual environment
        - cd to tests directory
        - run python ./test_indexer.py """

    def setUp( self ):
        self.indexer = Indexer( log )

    def test__build_solr_doc(self):
        """ Tests bib-only inscription. """
        inscription_xml_path=u'./test_files/CA.Berk.UC.HMA.G.8-4213.xml'
        solr_xml = self.indexer._build_solr_doc( inscription_xml_path )
        self.assertEqual( unicode, type(solr_xml) )
        self.assertTrue( '<field name="title">CA.Berk.UC.HMA.G.8/4213</field>' in solr_xml, 'solr_xml, ```%s```' % solr_xml )
        self.assertTrue( '<field name="msid_settlement">Berk</field>' in solr_xml, 'solr_xml, ```%s```' % solr_xml )
        self.assertTrue( '<field name="msid_institution">UC</field>' in solr_xml, 'solr_xml, ```%s```' % solr_xml )
        self.assertTrue( '<field name="msid_repository">HMA</field>' in solr_xml, 'solr_xml, ```%s```' % solr_xml )
        self.assertTrue( '<field name="msid_idno">8/4213</field>' in solr_xml, 'solr_xml, ```%s```' % solr_xml )
        self.assertTrue( '<field name="language">grc</field>' in solr_xml, 'solr_xml, ```%s```' % solr_xml )

    def test__post_solr_update(self):
        """ Tests post to solr. """
        inscription_xml_path=u'./test_files/CA.Berk.UC.HMA.G.8-4213.xml'
        solr_xml = self.indexer._build_solr_doc( inscription_xml_path )
        self.assertEqual( '<int name="status">0</int>', self.indexer._post_solr_update(solr_xml) )

    # end class IndexerTest


if __name__ == "__main__":
  unittest.TestCase.maxDiff = None  # allows error to show in long output
  unittest.main()
