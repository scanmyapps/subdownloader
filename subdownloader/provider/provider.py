# -*- coding: utf-8 -*-
# Copyright (c) 2019 SubDownloader Developers - See COPYING - GPLv3

from enum import Enum
import logging
import sys

log = logging.getLogger('subdownloader.provider.provider')


class ProviderConnectionError(Exception):
    def __init__(self, msg, extra_data=None):
        Exception.__init__(self)
        self._msg = msg
        self._extra_data = extra_data

    def get_msg(self):
        return self._msg

    def get_extra_data(self):
        return self._extra_data

    def __repr__(self):
        return '<ProviderConnectionError:msg={m}{e}>'.format(
            m=self._msg,
            e=(';extra={!r}'.format(self._extra_data) if self._extra_data else ''))


class ProviderNotConnectedError(ProviderConnectionError):
    def __init__(self):
        ProviderConnectionError.__init__(self, _('Not connected'))


# FIXME: let providers implement interfaces for these capabilities
class ProviderCapability(Enum):
    SEARCH_VIDEO_FILE = 'search_videofile'
    SEARCH_MOVIE_NAME = 'search_moviename'
    UPLOAD_SUBTITLES = 'upload_subtitles'
    LOOKUP_IMDB_NAME = 'lookup_imdb_name'


class SubtitleProvider(object):
    """
    Represents an abstract SubtitleProvider..
    """
    # FIXME: add documentation

    def __init__(self):
        pass

    def __del__(self):
        try:
            self.disconnect()
        except ProviderConnectionError:
            log.debug('Disconnect failed during destructor', exc_info=sys.exc_info())

    def get_settings(self):
        raise NotImplementedError()

    def set_settings(self, settings):
        raise NotImplementedError()

    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()

    def connected(self):
        raise NotImplementedError()

    def login(self):
        raise NotImplementedError()

    def logout(self):
        raise NotImplementedError()

    def logged_in(self):
        raise NotImplementedError()

    def search_videos(self, videos, callback, language=None):
        raise NotImplementedError()

    def query_text(self, query):
        raise NotImplementedError()

    def upload_subtitles(self, local_movie):
        raise NotImplementedError()

    def ping(self):
        raise NotImplementedError()

    def provider_info(self):
        raise NotImplementedError()

    # @classmethod
    # def supports_mode(cls, method):
    #     raise NotImplementedError()

    @classmethod
    def get_name(cls):
        raise NotImplementedError()

    @classmethod
    def get_short_name(cls):
        raise NotImplementedError()

    @classmethod
    def get_icon(cls):
        raise NotImplementedError()


class ProviderSettingsType(Enum):
    String = 'string'
    Password = 'password'


class ProviderSettings(object):
    def __init__(self):
        pass

    @staticmethod
    def key_types():
        raise NotImplementedError()

    def as_dict(self):
        raise NotImplementedError()

    def load(self, **kwargs):
        raise NotImplementedError()


class SubtitleTextQuery(object):
    def __init__(self, query):
        self._query = query

    def get_movies(self):
        raise NotImplementedError()

    def get_nb_movies_online(self):
        raise NotImplementedError()

    @property
    def query(self):
        return self._query

    def more_movies_available(self):
        raise NotImplementedError()

    def search_more_movies(self):
        raise NotImplementedError()

    def search_more_subtitles(self, movie):
        raise NotImplementedError()


class UploadResult(object):
    class Type(Enum):
        OK = 0
        FAILED = 1
        DUPLICATE = 2
        MISSINGDATA = 3

    def __init__(self, type, reason=None, rsubs=None):
        self._type = type
        self._reason = reason
        self._rsubs = rsubs

    @property
    def ok(self):
        return self._type == self.Type.OK

    @property
    def type(self):
        return self._type

    @property
    def reason(self):
        return self._reason

    @property
    def remote_subtitles(self):
        return self._rsubs
