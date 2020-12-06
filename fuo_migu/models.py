from fuocore.media import Media
from fuocore.models import SearchType as FuoSearchType, BaseModel, SearchModel, SongModel, ArtistModel, \
    AlbumModel, PlaylistModel, MvModel, VideoModel, LyricModel  # noqa
from fuocore.reader import SequentialReader

from fuo_migu.provider import provider
from fuo_migu.schema import SearchType
from fuo_migu.service import MiguService


def create_g(func, identifier):
    data = func(identifier, page=1, page_size=30)
    total = data.result.total_count

    def g():
        nonlocal data
        if data is None:
            yield from ()
        else:
            page = 1
            while data.result.results:
                for schema in data.result.results:
                    yield schema.model()
                page += 1
                data = func(identifier, page=page, page_size=30)

    return SequentialReader(g(), total)


class MiguModelException(BaseException):
    pass


class MiguBaseModel(BaseModel):
    class Meta:
        provider = provider


class MiguSongModel(SongModel, MiguBaseModel):
    class Meta:
        fields = ['qualities', 'content_id']
        support_multi_quality = True

    @classmethod
    def get(cls, identifier):
        result = provider.api.song_detail(identifier)
        return result.data.model()

    def list_quality(self):
        return self.qualities

    def get_media(self, quality):
        url = provider.api.get_song_media(self.identifier, self.content_id, quality)
        return Media(url,
                     format='2000kflac' if quality == 'shq' else '320kmp3',
                     bitrate='2000' if quality == 'shq' else '320')


class MiguArtistModel(ArtistModel, MiguBaseModel):
    pass


class MiguAlbumModel(AlbumModel, MiguBaseModel):
    class Meta:
        fields = ['cached_songs']
        fields_no_get = ['type', 'songs']

    @classmethod
    def get(cls, identifier):
        result = provider.api.album_detail(identifier)
        return result.data.model()

    @property
    def songs(self):
        if self.cached_songs is None:
            result = provider.api.album_songs(self.identifier, 1, 30)
            self.cached_songs = [o.model() for o in result.result.results]
        return self.cached_songs

    @songs.setter
    def songs(self, _):
        pass


class MiguPlaylistModel(PlaylistModel, MiguBaseModel):
    pass


class MiguSearchModel(SearchModel, MiguBaseModel):
    pass


class MiguMvModel(MvModel, MiguBaseModel):
    pass


class MiguVideoModel(VideoModel, MiguBaseModel):
    pass


class MiguLyricModel(LyricModel, MiguBaseModel):
    pass


def search_by_type(keyword: str, stype: SearchType):
    data = provider.api.search(keyword, stype, 1, 30)
    items = []
    field = None
    rfield = None
    if stype == SearchType.song:
        field = 'musics'
        rfield = 'songs'
    if stype == SearchType.album:
        field = 'albums'
        rfield = 'albums'
    if stype == SearchType.artist:
        field = 'artists'
        rfield = 'artists'
    if stype == SearchType.playlist:
        field = 'playlists'
        rfield = 'playlists'
    if stype == SearchType.mv:
        field = 'mv'
        rfield = 'videos'
    if not hasattr(data, field):
        raise MiguModelException('field not found')
    for item in getattr(data, field):
        items.append(item.model())
    return MiguSearchModel(**{rfield: items})


def search(keyword: str, **kwargs):
    type_ = FuoSearchType.parse(kwargs['type_'])
    stype = None
    if type_ == FuoSearchType.so:
        stype = SearchType.song
    if type_ == FuoSearchType.al:
        stype = SearchType.album
    if type_ == FuoSearchType.ar:
        stype = SearchType.artist
    if type_ == FuoSearchType.pl:
        stype = SearchType.playlist
    if type_ == FuoSearchType.vi:
        stype = SearchType.mv
    if stype is None:
        raise MiguModelException('unsupported search')
    return search_by_type(keyword, stype)


provider.api = MiguService()
