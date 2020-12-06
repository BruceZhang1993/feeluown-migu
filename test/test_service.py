from fuo_migu.schema import SearchType, SongSearchResult
from fuo_migu.service import MiguService


class TestService:
    def test_search_songs(self):
        result: SongSearchResult = MiguService().search('only my railgun', SearchType.song, 1, 10)
        assert result.success is True
        assert result.musics is not None
        assert len(result.musics) > 0
        first = result.musics[0]
        assert first.copyright_id is not None
        assert first.id is not None
        assert first.song_name is not None
