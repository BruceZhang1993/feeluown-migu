from fuocore.models import SearchType as FuoSearchType, BaseModel, SearchModel, SongModel, ArtistModel, \
    AlbumModel, PlaylistModel, MvModel, VideoModel, LyricModel  # noqa

from fuo_migu.provider import provider
from fuo_migu.schema import SearchType
from fuo_migu.service import MiguService


class MiguModelException(BaseException):
    pass


class MiguBaseModel(BaseModel):
    class Meta:
        provider = provider


class MiguSongModel(SongModel, MiguBaseModel):
    @classmethod
    def get(cls, identifier):
        result = provider.api.song_detail(identifier)
        return result.data.model()


class MiguArtistModel(ArtistModel, MiguBaseModel):
    pass


class MiguAlbumModel(AlbumModel, MiguBaseModel):
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
