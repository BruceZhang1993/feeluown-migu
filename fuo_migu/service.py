from typing import Type, Optional, Union

import requests
import logging

from fuo_migu.util import Singleton


logger = logging.getLogger('migu')


class MiguException(BaseException):
    pass


class MiguService(metaclass=Singleton):
    HOST = 'm.music.migu.cn'
    REFERER = 'https://m.music.migu.cn/migu/l/'
    UA = 'Mozilla/5.0 (Linux; Android 11; ONEPLUS A6003) AppleWebKit/537.36 (KHTML, like Gecko) ' \
         'Chrome/86.0.4240.198 Mobile Safari/537.36'

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'host': self.HOST,
            'referer': self.REFERER,
            'user-agent': self.UA
        })
        self.session.hooks = dict(response=self.request_tracing)

    @staticmethod
    def request_tracing(r: requests.Response, *args, **kwargs):
        logger.info(f'Request: [{r.request.method}] {r.request.url}')

    def search(self, keyword: str, stype: 'SearchType', page: int = 1, page_size: int = 20) \
            -> Union[
                'SongSearchResult', 'ArtistSearchResult', 'AlbumSearchResult', 'PlaylistSearchResult', 'MvSearchResult']:
        uri = 'https://m.music.migu.cn/migu/remoting/scr_search_tag'
        params = {
            'rows': page_size,
            'type': stype.value,
            'keyword': keyword,
            'pgc': page
        }
        with self.session.get(uri, params=params) as r:
            if r.status_code != 200:
                raise MiguException(f'Error: HTTP {r.status_code}')
            result_type: Optional[Type[Union[
                SongSearchResult, ArtistSearchResult, AlbumSearchResult, PlaylistSearchResult, MvSearchResult]]] \
                = get_result_by_stype(
                stype)
            if result_type is None:
                raise MiguException(f'Unsupported type')
            return result_type.parse_raw(r.content)

    def song_detail(self, cpid: str) -> 'SongDetailResult':
        uri = 'https://m.music.migu.cn/migu/remoting/cms_detail_tag'
        params = {'cpid': cpid}
        with self.session.get(uri, params=params) as r:
            if r.status_code != 200:
                raise MiguException(f'Error: HTTP {r.status_code}')
            return SongDetailResult.parse_raw(r.content)

    def artist_detail(self, aid: str) -> 'ArtistDetailResult':
        uri = 'https://m.music.migu.cn/migu/remoting/cms_artist_detail_tag'
        params = {'artistId': aid}
        with self.session.get(uri, params=params) as r:
            if r.status_code != 200:
                raise MiguException(f'Error: HTTP {r.status_code}')
            return ArtistDetailResult.parse_raw(r.content)

    def album_detail(self, aid: str):
        uri = 'https://m.music.migu.cn/migu/remoting/cms_album_detail_tag'
        params = {'albumId': aid}
        with self.session.get(uri, params=params) as r:
            if r.status_code != 200:
                raise MiguException(f'Error: HTTP {r.status_code}')
            return AlbumDetailResult.parse_raw(r.content)

    def playlist_detail(self, pid: str) -> 'PlaylistDetailResult':
        uri = 'https://m.music.migu.cn/migu/remoting/query_playlist_by_id_tag'
        params = {'playListId': pid}
        with self.session.get(uri, params=params) as r:
            if r.status_code != 200:
                raise MiguException(f'Error: HTTP {r.status_code}')
            return PlaylistDetailResult.parse_raw(r.content)

    def artist_songs(self, aid: str, page: int = 1, page_size: int = 20) -> 'ArtistSongsResult':
        uri = 'https://m.music.migu.cn/migu/remoting/cms_artist_song_list_tag'
        params = {
            'artistId': aid,
            'pageNo': page - 1,
            'pageSize': page_size
        }
        with self.session.get(uri, params=params) as r:
            if r.status_code != 200:
                raise MiguException(f'Error: HTTP {r.status_code}')
            return ArtistSongsResult.parse_raw(r.content)

    def album_songs(self, aid: str, page: int = 1, page_size: int = 20):
        uri = 'https://m.music.migu.cn/migu/remoting/cms_album_song_list_tag'
        params = {
            'pageSize': page_size,
            'pageNo': page - 1,
            'albumId': aid
        }
        with self.session.get(uri, params=params) as r:
            if r.status_code != 200:
                raise MiguException(f'Error: HTTP {r.status_code}')
            return AlbumSongsResult.parse_raw(r.content)

    def playlist_songs(self, pid: str, ptype: int = 2, content_count: int = 20):
        uri = 'https://m.music.migu.cn/migu/remoting/playlistcontents_query_tag'
        params = {
            'playListType': ptype,
            'playListId': pid,
            'contentCount': content_count
        }
        with self.session.get(uri, params=params) as r:
            if r.status_code != 200:
                raise MiguException(f'Error: HTTP {r.status_code}')
            return PlaylistSongsResult.parse_raw(r.content)

    def mv_detail(self, cpid: str) -> Optional['MvDetailResult']:
        uri = 'https://m.music.migu.cn/migu/remoting/mv_detail_tag'
        params = {'cpid': cpid, 'n': 3}
        with self.session.get(uri, params=params) as r:
            if r.status_code != 200:
                raise MiguException(f'Error: HTTP {r.status_code}')
            return MvDetailResult.parse_raw(r.content)

    def get_song_media(self, cpid: str, content_id: str, quality: str = 'hq'):
        tone_flags = {
            'lq': 'LQ',
            'sq': 'PQ',
            'hq': 'HQ',
            'shq': 'SQ'
        }
        uri = 'http://app.pd.nf.migu.cn/MIGUM2.0/v1.0/content/sub/listenSong.do'
        params = {
            'toneFlag': tone_flags.get(quality, ''),
            'netType': '00',
            'userId': '15548614588710179085069',
            'ua': 'Android_migu',
            'version': '5.1',
            'copyrightId': cpid,
            'contentId': content_id,
            'resourceType': '2',
            'channel': '0'
        }
        with self.session.head(uri, params=params) as r:
            if r.status_code != 305:
                raise MiguException(f'Error: HTTP {r.status_code}')
            url = r.headers.get('location')
            if url is None:
                raise MiguException('resource not found')
            return url


from fuo_migu.schema import get_result_by_stype, SongSearchResult, ArtistSearchResult, AlbumSearchResult, \
    PlaylistSearchResult, MvSearchResult, SongDetailResult, ArtistDetailResult, ArtistSongsResult, AlbumDetailResult, \
    PlaylistDetailResult, PlaylistSongsResult, AlbumSongsResult, SearchType, MvDetailResult

if __name__ == '__main__':
    print(MiguService().mv_detail('600570YA7ZS'))
