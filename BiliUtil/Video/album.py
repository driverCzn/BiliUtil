# coding=utf-8
import re
import copy
from urllib import parse
import BiliUtil.Util as Util
import BiliUtil.Video as Video


class Album:
    def __init__(self, aid=None):
        self.aid = str(aid)
        self.num = None
        self.type = None
        self.cover = None
        self.name = None
        self.time = None
        self.desc = None
        self.view = None
        self.danmu = None
        self.reply = None
        self.favorite = None
        self.coin = None
        self.share = None
        self.like = None
        self.cid_list = None
        self.title_list = None  # 标题列表，便于为每个分P文件设置正确文件名

    def set_album(self, aid):
        self.aid = str(aid)

    def set_by_url(self, url):
        input_url = parse.urlparse(url)
        aid = re.match('/video/av([0-9]+)', input_url.path).group(1)
        self.aid = str(aid)

    def sync(self, cookie=None):
        # 检验必要的参数
        if self.aid is None:
            raise Util.ParameterError('缺少获取视频信息的必要参数')

        # 发送网络请求
        http_request = {
            'info_obj': Util.ALBUM,
            'params': {
                'aid': str(self.aid)
            },
            'cookie': cookie
        }
        json_data = Util.http_get(**http_request)

        # 修改对象信息
        self.num = json_data['data']['videos']
        self.type = json_data['data']['tname']
        self.cover = json_data['data']['pic']
        self.name = json_data['data']['title']
        self.time = json_data['data']['ctime']
        self.desc = json_data['data']['desc']
        self.view = json_data['data']['stat']['view']
        self.danmu = json_data['data']['stat']['danmaku']
        self.reply = json_data['data']['stat']['reply']
        self.favorite = json_data['data']['stat']['favorite']
        self.coin = json_data['data']['stat']['coin']
        self.share = json_data['data']['stat']['share']
        self.like = json_data['data']['stat']['like']
        self.cid_list = list(page['cid'] for page in json_data['data']['pages'])
        self.title_list = list(page['part'] for page in json_data['data']['pages'])

        # 返回专辑信息
        return copy.deepcopy(vars(self))

    def get_video_list(self, cookie=None):
        # 检验必要的参数
        if self.aid is None:
            raise Util.ParameterError('缺少获取视频信息的必要参数')

        if self.cid_list is None:
            self.sync(cookie)

        video_list = []
        for index, cid in enumerate(self.cid_list):
            cv = Video.Video(self.aid, cid, self.name, index+1)
            video_list.append(cv)

        return video_list
