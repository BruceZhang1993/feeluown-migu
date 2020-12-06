from typing import Type, Optional, Union

import requests

from fuo_migu.schema import SearchType, get_result_by_stype, SongSearchResult, ArtistSearchResult, AlbumSearchResult, \
    PlaylistSearchResult, MvSearchResult, SongDetailResult
from fuo_migu.util import Singleton


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

    def search(self, keyword: str, stype: SearchType = SearchType.song, page: int = 1, page_size: int = 20) \
            -> Union[SongSearchResult, ArtistSearchResult, AlbumSearchResult, PlaylistSearchResult, MvSearchResult]:
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

    def song_detail(self, cpid: str):
        uri = 'https://m.music.migu.cn/migu/remoting/cms_detail_tag'
        params = {'cpid': cpid}
        with self.session.get(uri, params=params) as r:
            if r.status_code != 200:
                raise MiguException(f'Error: HTTP {r.status_code}')
            return SongDetailResult.parse_raw(r.content)

    def artist_detail(self, aid: str):
        uri = 'https://m.music.migu.cn/migu/remoting/cms_artist_detail_tag'
        params = {'artistId': aid}
        with self.session.get(uri, params=params) as r:
            if r.status_code != 200:
                raise MiguException(f'Error: HTTP {r.status_code}')
            print(r.text)

    def artist_songs(self, aid: str, page: int = 1, page_size: int = 20):
        uri = 'https://m.music.migu.cn/migu/remoting/cms_artist_song_list_tag'
        params = {
            'artistId': aid,
            'pageNo': page - 1,
            'pageSize': page_size
        }
        with self.session.get(uri, params=params) as r:
            if r.status_code != 200:
                raise MiguException(f'Error: HTTP {r.status_code}')
            print(r.text)


if __name__ == '__main__':
    MiguService().artist_songs('112', 2, 20)
