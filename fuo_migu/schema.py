import re
from datetime import date
from enum import Enum
from typing import List, Optional, Type

from pydantic import BaseModel as _Base, Field


class BaseSchema(_Base):
    pass


class SearchType(Enum):
    artist = 1
    song = 2
    album = 4
    mv = 5
    playlist = 6


class SearchSong(BaseSchema):
    id: Optional[str]
    album_name: Optional[str] = Field(alias='albumName')
    album_id: Optional[str] = Field(alias='albumId')
    copyright_id: Optional[str] = Field(alias='copyrightId')
    mp3: Optional[str] = Field(alias='mp3')
    song_name: Optional[str] = Field(alias='songName')
    mv_id: Optional[str] = Field(alias='mvId')
    lyrics: Optional[str]
    mv_copyright_id: Optional[str] = Field(alias='mvCopyrightId')
    singer_id: Optional[str] = Field(alias='singerId')
    title: Optional[str]
    cover: Optional[str]
    has_mv: Optional[bool] = Field(alias='hasMv')
    singer_name: Optional[str] = Field(alias='singerName')
    has_sq: Optional[bool] = Field(alias='hasSQqq')
    has_hq: Optional[bool] = Field(alias='hasHQqq')
    artist: Optional[str]

    @property
    def artist_ids(self) -> List[str]:
        if self.singer_id is None:
            return []
        singer_id = self.singer_id.strip()
        if singer_id == '':
            return []
        return re.split(r',\s+', singer_id)

    @property
    def artist_names(self) -> List[str]:
        if self.singer_name is None:
            return []
        singer_name = self.singer_name.strip()
        if singer_name == '':
            return []
        return re.split(r',\s+', singer_name)

    def model(self):
        artists = [migu_models.ArtistModel(identifier=id_, name=name) for id_, name in
                   zip(self.artist_ids, self.artist_names)]
        return migu_models.MiguSongModel(identifier=self.copyright_id, title=self.title, artists=artists,
                                         album=migu_models.MiguAlbumModel(identifier=self.album_id,
                                                                          name=self.album_name)
                                         if self.album_id is not None else None)


class SearchArtist(BaseSchema):
    id: Optional[str]
    full_song_total: Optional[int] = Field(alias='fullSongTotal')
    title: Optional[str]
    album_num: Optional[int] = Field(alias='albumNum')
    artist_pic_l: Optional[str] = Field(alias='artistPicL')
    artist_pic_m: Optional[str] = Field(alias='artistPicM')
    artist_pic_s: Optional[str] = Field(alias='artistPicS')
    song_num: Optional[int] = Field(alias='songNum')
    highlight_str: Optional[List[str]] = Field(alias='highlightStr')

    def model(self):
        return migu_models.MiguArtistModel(identifier=self.id, name=self.title, cover=self.artist_pic_m)


class SearchAlbum(BaseSchema):
    class Singer(BaseSchema):
        id: Optional[str]
        name: Optional[str]

        def model(self):
            return migu_models.ArtistModel(identifier=self.id, name=self.name)

    id: Optional[str]
    album_pic_s: Optional[str] = Field(alias='albumPicS')
    album_pic_m: Optional[str] = Field(alias='albumPicM')
    album_pic_l: Optional[str] = Field(alias='albumPicL')
    movie_name: Optional[List[str]] = Field(alias='movieName')
    full_song_total: Optional[int] = Field(alias='fullSongTotal')
    title: Optional[str]
    singer: Optional[List[Singer]]
    song_num: Optional[int] = Field(alias='songNum')
    publish_date: Optional[date] = Field(alias='publishDate')
    highlight_str: Optional[List[str]] = Field(alias='highlightStr')

    def model(self):
        return migu_models.MiguAlbumModel(identifier=self.id, name=self.title, cover=self.album_pic_m,
                                          artists=[artist.model() for artist in self.singer])


class SearchPlaylist(BaseSchema):
    id: Optional[str]
    img: Optional[str]
    keep_num: Optional[int] = Field(alias='keepNum')
    music_num: Optional[int] = Field(alias='musicNum')
    highlight_str: Optional[List[str]] = Field(alias='highlightStr')
    name: Optional[str]
    play_num: Optional[int] = Field(alias='playNum')
    priority: Optional[int]
    share_num: Optional[int] = Field(alias='shareNum')
    songlist_type: Optional[int] = Field(alias='songlistType')
    user_id: Optional[str] = Field(alias='userId')

    def model(self):
        return migu_models.MiguPlaylistModel(identifier=self.id, name=self.name, cover=self.img)


class SearchMv(BaseSchema):
    id: Optional[str]
    album_name: Optional[str] = Field(alias='albumName')
    album_id: Optional[str] = Field(alias='albumId')
    copyright_id: Optional[str] = Field(alias='copyrightId')
    song_name: Optional[str] = Field(alias='songName')
    mv_id: Optional[str] = Field(alias='mvId')
    singer_id: Optional[str] = Field(alias='singerId')
    singer_name: Optional[str] = Field(alias='singerName')
    title: Optional[str]
    artist: Optional[str]

    def model(self):
        return migu_models.MiguVideoModel(identifier=self.copyright_id, title=self.title)


class SongDetail(BaseSchema):
    id: Optional[str] = Field(alias='songId')
    song_name: Optional[str] = Field(alias='songName')
    copyright_id: Optional[str] = Field(alias='copyrightId')
    lyric_lrc: Optional[str] = Field(alias='lyricLrc')
    fanyi_lrc: Optional[str] = Field(alias='fanyiLrc')
    has24bit: Optional[bool] = Field(alias='has24Bitqq')
    has3d: Optional[bool] = Field(alias='has3Dqq')
    has_hq: Optional[bool] = Field(alias='hasHQqq')
    has_sq: Optional[bool] = Field(alias='hasSQqq')
    has_mv: Optional[bool] = Field(alias='hasMv')
    listen_url: Optional[str] = Field(alias='listenUrl')
    mv_copyright_id: Optional[str] = Field(alias='mvCopyrightId')
    pic_l: Optional[str] = Field(alias='picL')
    pic_s: Optional[str] = Field(alias='picS')
    pic_m: Optional[str] = Field(alias='picM')
    singer_id: Optional[List[str]] = Field(alias='singerId')
    singer_name: Optional[List[str]] = Field(alias='singerName')
    song_desc: Optional[str] = Field(alias='songDesc')
    qq: Optional[dict]

    @property
    def content_id(self):
        if self.qq is None:
            return ''
        return self.qq.get('productId', '')

    def model(self):
        artists = [migu_models.ArtistModel(identifier=id_, name=name) for id_, name in
                   zip(self.singer_id, self.singer_name)]
        qualities = []
        if self.has_sq:
            qualities.append('shq')
        if self.has_hq:
            qualities.append('hq')
        qualities.append('sq')
        qualities.append('lq')
        return migu_models.MiguSongModel(identifier=self.copyright_id, artists=artists, title=self.song_name,
                                         mv_cpid=self.mv_copyright_id,
                                         url=self.listen_url, has_mv=self.has_mv or False, qualities=qualities,
                                         content_id=self.content_id,
                                         lyric=migu_models.MiguLyricModel(identifier=self.copyright_id,
                                                                          content=self.lyric_lrc,
                                                                          trans_content=self.fanyi_lrc))


class ArtistDetail(BaseSchema):
    id: Optional[int]
    artist_id: Optional[str] = Field(alias='artistId')
    another_name: Optional[str] = Field(alias='anotherName')
    artist_name: Optional[str] = Field(alias='artistName')
    artist_pic_l: Optional[str] = Field(alias='artistPicL')  # 这些地址似乎无法访问
    artist_pic_s: Optional[str] = Field(alias='artistPicS')
    artist_pic_m: Optional[str] = Field(alias='artistPicM')
    local_artist_pic_l: Optional[str] = Field(alias='localArtistPicL')
    local_artist_pic_s: Optional[str] = Field(alias='localArtistPicS')
    local_artist_pic_m: Optional[str] = Field(alias='localArtistPicM')
    awards: Optional[str]
    birth_date: Optional[date] = Field(alias='birthDate')
    birth_place: Optional[str] = Field(alias='birthPlace')
    country: Optional[str]
    company: Optional[str]
    english_name: Optional[str] = Field(alias='englishName')
    former_name: Optional[str] = Field(alias='formerName')
    gender: Optional[int]
    height: Optional[int]  # 身高
    hobby: Optional[str]  # 爱好
    intro: Optional[str]  # 完整简介
    lover: Optional[str]  # 情侣/爱人
    nation: Optional[str]  # 民族
    represent_works: Optional[str] = Field(alias='representWorks')  # 代表作
    school: Optional[str]
    similar_artist: Optional[str] = Field(alias='similarArtist')  # 相似歌手名
    weight: Optional[int]  # 体重


class AlbumDetail(BaseSchema):
    id: Optional[str]
    album_id: Optional[str] = Field(alias='albumId')
    album_intro: Optional[str] = Field(alias='albumIntro')
    album_name: Optional[str] = Field(alias='albumName')
    album_pic_l: Optional[str] = Field(alias='albumPicL')  # 这些地址似乎无法访问
    album_pic_s: Optional[str] = Field(alias='albumPicS')
    album_pic_m: Optional[str] = Field(alias='albumPicM')
    local_album_pic_l: Optional[str] = Field(alias='localAlbumPicL')
    local_album_pic_s: Optional[str] = Field(alias='localAlbumPicS')
    local_album_pic_m: Optional[str] = Field(alias='localAlbumPicM')
    awards: Optional[str]
    language: Optional[str]
    publish_company: Optional[str] = Field(alias='publishCompany')
    production_company: Optional[str] = Field(alias='productionCompany')
    publish_date: Optional[date] = Field(alias='publishDate')
    singer_id: Optional[str] = Field(alias='singerId')
    track_count: Optional[int] = Field(alias='trackCount')

    def model(self):
        return migu_models.MiguAlbumModel(identifier=self.album_id, name=self.album_name, cover=self.local_album_pic_m,
                                          desc=self.album_intro or '')


class MvDetail(BaseSchema):
    class MvSchema(BaseSchema):
        class MvKv(BaseSchema):
            key: Optional[str]
            value: Optional[str]

        entry: Optional[List[MvKv]]

    copyright_id: Optional[str] = Field(alias='copyrightId')
    content_name: Optional[str] = Field(alias='contentName')
    actor_name: Optional[str] = Field(alias='actorName')
    videos: Optional[MvSchema] = Field(alias='videoUrlMap')

    @property
    def url(self):
        if self.videos and self.videos.entry:
            for kv in self.videos.entry:
                if kv.value:
                    return kv.value
        return None

    def model(self):
        url = self.url
        if url is None:
            return None
        return migu_models.MiguMvModel(identifier=self.copyright_id, name=self.content_name, desc=self.actor_name,
                                       media=migu_models.Media(url))


class PlaylistTag(BaseSchema):
    tagid: Optional[str]
    tag_name: Optional[str] = Field(alias='tagName')


class PlaylistDetail(BaseSchema):
    playlist_id: Optional[str] = Field(alias='playListId')
    playlist_name: Optional[str] = Field(alias='playListName')
    playlist_type: Optional[int] = Field(alias='playListType')
    summary: Optional[str]
    image: Optional[str]
    content_count: Optional[int] = Field(alias='contentCount')
    channel: Optional[int]
    tag_list: Optional[List[PlaylistTag]] = Field(alias='tagLists')


class SongListSchema(BaseSchema):
    asc: Optional[bool]
    current_page: Optional[int] = Field(alias='currentPage')
    page_size: Optional[int] = Field(alias='pageSize')
    total_count: Optional[int] = Field(alias='totalCount')  # 总数字段似乎一直为 0
    results: Optional[List[SongDetail]]

    @property
    def page(self):
        if self.current_page is None:
            return 0
        return self.current_page + 1


class PlaylistSong(BaseSchema):
    content_id: Optional[str] = Field(alias='contentId')
    content_type: Optional[str] = Field(alias='contentType')
    content_name: Optional[str] = Field(alias='contentName')
    singer_id: Optional[str] = Field(alias='singerId')
    singer_name: Optional[str] = Field(alias='singerName')
    song_id: Optional[str] = Field(alias='songId')


# 请求结果结构定义

class BaseSearchResult(BaseSchema):
    success: Optional[bool]
    keyword: Optional[str]
    page_no: Optional[int] = Field(alias='pageNo')
    pgt: Optional[int]


class SongSearchResult(BaseSearchResult):
    musics: Optional[List[SearchSong]]


class ArtistSearchResult(BaseSearchResult):
    artists: Optional[List[SearchArtist]]


class AlbumSearchResult(BaseSearchResult):
    albums: Optional[List[SearchAlbum]]


class PlaylistSearchResult(BaseSearchResult):
    playlists: Optional[List[SearchPlaylist]] = Field(alias='songLists')


class MvSearchResult(BaseSearchResult):
    mv: Optional[List[SearchMv]]


class SongDetailResult(BaseSchema):
    data: Optional[SongDetail]


class ArtistDetailResult(BaseSchema):
    data: Optional[ArtistDetail]


class ArtistSongsResult(BaseSchema):
    result: Optional[SongListSchema]


class AlbumSongsResult(BaseSchema):
    result: Optional[SongListSchema]


class PlaylistSongsResult(BaseSchema):
    code: Optional[str]
    info: Optional[str]
    content_list: Optional[List[PlaylistSong]] = Field(alias='contentList')


class AlbumDetailResult(BaseSchema):
    data: Optional[AlbumDetail]


class MvDetailResult(BaseSchema):
    data: Optional[MvDetail]


class PlaylistDetailResult(BaseSchema):
    class Response(BaseSchema):
        code: Optional[str]
        info: Optional[str]
        playlist: Optional[List[PlaylistDetail]]

    code: Optional[int]
    msg: Optional[str]
    rsp: Optional[Response]


def get_result_by_stype(stype: SearchType) -> Optional[Type]:
    """
    根据搜索类型分发对应的请求结果体
    :param stype: 搜索类型（枚举）
    :type stype: SearchType
    :return: 返回类型或 None
    :rtype: Optional[Type]
    """
    if stype == SearchType.song:
        return SongSearchResult
    if stype == SearchType.artist:
        return ArtistSearchResult
    if stype == SearchType.album:
        return AlbumSearchResult
    if stype == SearchType.playlist:
        return PlaylistSearchResult
    if stype == SearchType.mv:
        return MvSearchResult
    return None


from fuo_migu import models as migu_models
