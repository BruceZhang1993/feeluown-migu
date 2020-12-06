import re
from datetime import date
from enum import Enum
from typing import List, Optional, Type

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
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


class SearchAlbum(BaseSchema):
    class Singer(BaseSchema):
        id: Optional[str]
        name: Optional[str]

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


def get_result_by_stype(stype: SearchType) -> Optional[Type]:
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
