# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Rahul Handay <rahulha@saltstack.com>`
'''

# Import Python Libs
from __future__ import absolute_import
import os

# Import Salt Testing Libs
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.unit import TestCase, skipIf
from tests.support.mock import (
    MagicMock,
    patch,
    NO_MOCK,
    NO_MOCK_REASON
)

# Import Salt Libs
import salt.config
from salt.syspaths import BASE_FILE_ROOTS_DIR
import salt.states.winrepo as winrepo


class MockRunnerClient(object):
    '''
        Mock RunnerClient class
    '''
    def __init__(self):
        pass

    class RunnerClient(object):
        '''
            Mock RunnerClient class
        '''
        def __init__(self, master_config):
            '''
                init method
            '''
            pass

        @staticmethod
        def cmd(arg1, arg2):
            '''
                Mock cmd method
            '''
            return []


@patch('salt.states.winrepo.salt.runner', MockRunnerClient)
@skipIf(NO_MOCK, NO_MOCK_REASON)
class WinrepoTestCase(TestCase, LoaderModuleMockMixin):
    '''
    Validate the winrepo state
    '''
    def setup_loader_modules(self):
        return {winrepo: {}}

    def test_genrepo(self):
        '''
        Test to refresh the winrepo.p file of the repository
        '''
        ret = {'name': 'salt',
               'changes': {},
               'result': False,
               'comment': ''}
        ret.update({'comment':
                    '{file_roots}/win/repo is '
                    'missing'.format(file_roots=BASE_FILE_ROOTS_DIR)})
        self.assertDictEqual(winrepo.genrepo('salt'), ret)

        mock = MagicMock(return_value={'winrepo_dir': 'salt',
                                       'winrepo_cachefile': 'abc'})
        with patch.object(salt.config, 'master_config', mock):
            mock = MagicMock(return_value=[0, 1, 2, 3, 4, 5, 6, 7, 8])
            with patch.object(os, 'stat', mock):
                mock = MagicMock(return_value=[])
                with patch.object(os, 'walk', mock):
                    with patch.dict(winrepo.__opts__, {'test': True}):
                        ret.update({'comment': '', 'result': None})
                        self.assertDictEqual(winrepo.genrepo('salt'), ret)

                    with patch.dict(winrepo.__opts__, {'test': False}):
                        ret.update({'result': True})
                        self.assertDictEqual(winrepo.genrepo('salt'), ret)

                        ret.update({'changes': {'winrepo': []}})
                        self.assertDictEqual(winrepo.genrepo('salt', True),
                                             ret)
