from .common import InfoExtractor
import re


class XiaoxintvIE(InfoExtractor):
    _VALID_URL = r'https?:\/\/(?:www\.)?xiaoxintv\.net\/index.php\/vod\/play\/id\/\d+\/sid\/\d+\/nid\/(?P<id>[0-9]+)\.html'
    _TESTS = [{
        'url': 'https://xiaoxintv.net/index.php/vod/play/id/26838/sid/1/nid/30.html',
        'md5': '89173dc7aeb9c492bae96b3fce0f913f',
        'info_dict': {
            # For videos, only the 'id' and 'ext' fields are required to RUN the test:
            'id': '30',
            'ext': 'mp4',
            'title': '30',
            # 'description': ''
            # Then if the test run fails, it will output the missing/incorrect fields.
            # Properties can be added as:
            # * A value, e.g.
            #     'title': 'Video title goes here',
            # * MD5 checksum; start the string with 'md5:', e.g.
            #     'description': 'md5:098f6bcd4621d373cade4e832627b4f6',
            # * A regular expression; start the string with 're:', e.g.
            #     'thumbnail': r're:^https?://.*\.jpg$',
            # * A count of elements in a list; start the string with 'count:', e.g.
            #     'tags': 'count:10',
            # * Any Python type, e.g.
            #     'view_count': int,
        }
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        manifest_url = re.findall(r'"url":"(https:\\\/\\\/m3u\.haiwaikan\.com\\\/xm3u8\\\/[a-z0-9]+\.m3u8)"', webpage)

        # file = open('./test.html', 'w')

        # print(webpage, file=file)
        if len(manifest_url) == 0:
            raise ValueError('No manifest url found in webpage.')
        elif len(manifest_url) != 1:
            raise ValueError('More than 1 manifest url found. Website html has changed.')
        else:
            manifest_url = manifest_url[0]
            manifest_url = manifest_url.replace('\\', '')

        formats = self._extract_m3u8_formats(manifest_url, video_id, 'mp4')

        return {
            'id': video_id,
            'title': video_id,
            'formats': formats
            # TODO more properties (see yt_dlp/extractor/common.py)
        }
