###############################################################################
#    Copyright (c) 2016 Salvatore Ventura <salvoventura@gmail.com>
#
#      File: photos.py
#
#    Author: Salvatore Ventura <salvoventura@gmail.com>
#      Date: 07 Dec 2016
#   Purpose: Handle Photos, CuratedPhotos, RandomPhotos, and Photo
#
#  Revision: 1
#   Comment: What's new in revision 1
#
###############################################################################
from .liblogging import logger
from .unpage import UnsplashPage
from .unobject import UnsplashObject


class Photos(UnsplashPage):
    def __init__(self, api_key, url='/photos', **kwargs):
        valid_options = ['page', 'per_page', 'order_by']
        super(Photos, self).__init__(url=url, api_key=api_key, valid_options=valid_options, **kwargs)

    @property
    def entries(self):
        for entry in self.body:
            yield Photo(api_key=self.api_key, source=entry)


class CuratedPhotos(UnsplashPage):
    # TODO: 2019 this endpoint is deprecated
    def __init__(self, api_key, url='/photos/curated', **kwargs):
        logger.warning('This endpoint has been deprecated by the Unsplash API')
        valid_options = ['page', 'per_page', 'order_by']
        super(CuratedPhotos, self).__init__(url=url, api_key=api_key, valid_options=valid_options, **kwargs)

    @property
    def entries(self):
        for entry in self.body:
            yield Photo(api_key=self.api_key, source=entry)


class RandomPhotos(UnsplashPage):
    # TODO: update documentation to reflect this at file
    # TODO: docs/source/classes/class_pyunsplash.rst
    #
    def __init__(self, api_key, url='/photos/random', **kwargs):
        valid_options = ['collections', 'featured', 'username', 'query', 'orientation', 'count']
        super(RandomPhotos, self).__init__(url=url, api_key=api_key, valid_options=valid_options, **kwargs)

    @property
    def entries(self):
        for entry in self.body:
            yield Photo(api_key=self.api_key, source=entry)


class Photo(UnsplashObject):
    def __init__(self, api_key, source, **kwargs):
        valid_options = ['w', 'h', 'rect']
        # simplify for source=photoid
        if isinstance(source, str) and not source.startswith(self._api_root):
            # assume it's a photoid
            source = "{}/photos/{}".format(self._api_root, source)
        super(Photo, self).__init__(api_key=api_key, source=source, valid_options=valid_options, **kwargs)

    @property
    def link_html(self):
        return self.links.get('html', None)

    @property
    def stats(self):
        url = '{}/stats'.format(self.url)
        r = self._agent.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            logger.error('Failed stats retrieval for %s with status code %s', url, r.status_code)
            return None

    @property
    def link_download(self):
        return self.links.get('download', None)

    @property
    def link_download_location(self):
        return self.links.get('download_location', None)

    @property
    def hotlink_raw(self):
        return self.hotlink.get('raw', None)

    @property
    def hotlink_regular(self):
        return self.hotlink.get('regular', None)

   
    

