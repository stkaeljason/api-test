# coding:utf-8
import requests
import json
import logdealer
import argparse
import sys
reload(sys)
sys.setdefaultencoding('utf8')

logger = logdealer.APITestLogger("api_log.log").getLogger()


# 接口测试类
class APITest(object):
    """ test api of connect server """

    def __init__(self, uid, token, base_url='https://api-test.ciwei.io/dse-service/v1/app/', success_result=228):
        self.uid = uid
        self.token = token
        self.base_url = base_url
        self.success_result = success_result
        self.headers = {"content-type": "application/json", "x-access-token": token}

    # 测试方法
    def api_test(self, method, url, params=None):
        if method == 'get':
            response = requests.get(url, data=params, headers=self.headers)
        elif method == 'post':
            response = requests.post(url, data=params, headers=self.headers)
        elif method == 'delete':
            response = requests.delete(url, data=params, headers=self.headers)

        # 对相应的‘code’字段与成功相应的对应code字段做对比，目前为228
        if response.json()['code'] == self.success_result:
            print 'success'            # 暂保留，将来只在终端打印失败的情况，其他全部写进log文件
        else:
            # print response.url        # 当有错误时才打印对应接口发出的请求
            # print ('fail:%s, message:%s') % (response.json()['code'], response.json()['message'])
            logger.error('method: %s, url: %s, fail:%s, message:%s' \
                % (method, url, response.json()['code'], response.json()['message']))
        logger.debug('method: %s, url: %s, response json: %s' \
            % (method, response.url, response.json()))

        return response.json()


def get_personal(uid, token):
    """拉取个人全部属性"""
    personal_api = APITest(uid, token)
    print 'personal_api test result is:'
    personal_api.api_test('get', personal_api.base_url + uid)


def post(uid, token):
    """在火影玩家圈发帖"""
    post_api = APITest(uid, token)
    print 'post_api test result is:'
    body = json.dumps({
        'parentId': '165E67709264E5B0ECB5BA92275B23C2',                                 # 写死为火影玩家圈的gid
        'groupName': '火影玩家圈',
        'content': 'apitesting',
        'pictures': [],
        'authorId': uid,
        'nickname': 'jason',
        'avatar': 'user/750x750/201512071045466320.jpg',
        'type': '0',
           })
    post_api.api_test('post', post_api.base_url+uid+'/post', body)


def get_feed(uid, token):
    """拉取feed流"""
    feed_api = APITest(uid, token)
    print 'feed_api test result is:'
    feed_response = feed_api.api_test('get', feed_api.base_url+uid+'/feed', {'limit': '10', 'offset': '0'})
    return feed_response['data'][0]['id']                                           # 返回feed流的第一个帖子的帖子id


def get_single_group(uid, token):
    """获取单个圈子信息"""
    single_group_api = APITest(uid, token)
    print 'singlegroup_api test result is:'
    gid = 'F15B5412BC419EE532DF8433373BF4F7'                                            # gid写死为刺猬科技同事圈的gid
    single_group_api.api_test('get', single_group_api.base_url+uid+'/group/' + gid + '?gname=刺猬科技同事圈')


def get_message(uid, token):
    """火球全部消息列表"""
    message_api = APITest(uid, token)
    print 'message_api test result is:'
    message_api.api_test('get', message_api.base_url+uid+'/message')


def get_group(uid, token):
    """拉取所有圈子"""
    group_api = APITest(uid, token)
    print 'group_api test result is:'
    group_api.api_test('get', group_api.base_url+uid+'/group')


def qi_niu(uid, token):
    """获取七牛图片上传的Token"""
    qiniu_api = APITest(uid, token)
    print 'qiniu_api test result is:'
    qiniu_api.api_test('get', qiniu_api.base_url+uid+'/token')


def group_post(uid, token):
    """获取圈子中的帖子"""
    quanzipost_api = APITest(uid, token)
    print 'quanzi_post_api test result is:'
    gid = '165E67709264E5B0ECB5BA92275B23C2'                                               # 写死为火影玩家圈的gid
    quanzipost_api.api_test('get', quanzipost_api.base_url+uid + '/post/'+gid, {'limit': '10', 'offset': '0'})


def topic_post(uid, token):
    """获取话题下的帖子列表"""
    topic_post_api = APITest(uid, token)
    print 'topic_post_api test result is:'
    topic_id = '54ba1caa902d43149ec2e87958bd0c8b'                                              # 固定为已知的topicid
    param = {'limit': '10', 'offset': '0'}
    topic_post_api.api_test('get', topic_post_api.base_url+uid + '/post/' + topic_id, param)


def publish_comment(uid, token, post_id):
    """对帖子发表评论"""
    publish_comment_api = APITest(uid, token)
    print 'publish_comment_api test result is:'

    params = json.dumps({
        'parentId': post_id,                                         # feed流中第一个帖子的帖子id
        'rootId': post_id,                                           # 所属帖子的id
        'content': 'good',
        'authorId': uid,
        'nickname': 'jason',
        'avatar': 'user/750x750/201512071045466320.jpg',
        'type': '0',
    }
    )
    publish_comment_api.api_test('post', publish_comment_api.base_url+uid+'/comment', params)


def get_comment(uid, token, post_id):
    """获取帖子的评论"""
    get_post_comment = APITest(uid, token)
    print 'get_post_comment test result is:'
    pid = post_id                                                  # 帖子id
    params = {'limit': '10', 'offset': '0'}
    get_post_comment.api_test('get', get_post_comment.base_url+uid + '/comment/' + pid, params)


def like(uid, token, post_id):
    """点赞"""
    like_api = APITest(uid, token)
    print 'like_api test result is:'
    params = json.dumps({
        'parentId': post_id,                                         # 从feed_api处获取的feed流第一个帖子id
        'rootId': post_id,                                           # 从feed_api处获取的feed流第一个帖子id
        'authorId': uid,
        'nickname': 'jason',
        'avatar': 'user/750x750/201512071045466320.jpg',
        'type': '0',
    }
    )
    like_api.api_test('post', like_api.base_url + uid + '/like', params)


def get_post_detail(uid, token, post_id):
    """获取帖子详情"""
    get_post_detail_api = APITest(uid, token)
    print 'get_post_detail_api test result is:'
    paramter = post_id                                            # 帖子id
    get_post_detail_api.api_test('get', get_post_detail_api.base_url+uid+'/post?id=' + paramter)


def set_push_switch(uid, token):
    """把推送开关打开"""
    push_switch_api = APITest(uid, token)
    print 'push_switch_api test result is:'
    body = json.dumps({
        'enableLikesPush': True,
        'enableReplyPush': True
    })
    push_switch_api.api_test('post', push_switch_api.base_url + uid + '/settings', body)


def get_settings(uid, token):
    """获取个人设置"""
    get_settings_api = APITest(uid, token)
    print 'get_settings_api test result is:'
    get_settings_api.api_test('get', get_settings_api.base_url+uid+'/settings')


def report(uid, token, post_id):
    """举报"""
    report_api = APITest(uid, token)
    print 'report_api test result is:'
    body = json.dumps({
        "targetUserId": uid,
        "reporterId": uid,
        "postId": post_id,
        "commentId": "",
        "reason": "举报原因"
    })

    report_api.api_test('post', report_api.base_url+uid+'/report', body)

    # 读取举报列表,暂保留


def get_unread_message(uid, token):
    """获取未读的消息数"""
    get_unread_api = APITest(uid, token)
    print 'get_unread_api test result is:'
    get_unread_api.api_test('get', get_unread_api.base_url+uid+'/unread_msg')


def delete_post(uid, token, post_id):
    """ 删除帖子：删除feed流中第一个帖子"""
    delete_post_api = APITest(uid, token)
    print 'delete_post_api test result is:'
    delete_post_api.api_test('delete', delete_post_api.base_url+uid+'/post/'+post_id)


if __name__ == '__main__':
    """ 调用测试函数完成接口测试 """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uid', action='store')
    parser.add_argument('-t', '--token', action='store')
    args = parser.parse_args()
    if args.uid is None or args.token is None:
        parser.print_help()
        sys.exit()

    get_personal(args.uid, args.token)                                  # 拉取个人属性
    get_group(args.uid, args.token)                                     # 拉取全部圈子
    get_single_group(args.uid, args.token)                              # 获取单个圈子详情
    group_post(args.uid, args.token)                                    # 拉取圈子中的帖子
    post(args.uid, args.token)                                          # 发帖
    get_feed(args.uid, args.token)                                      # 拉取feed流
    post_id = get_feed(args.uid, args.token)                            # 获取feed流中第一个帖子的帖子id
    publish_comment(args.uid, args.token, post_id)                      # 对feed流第一个帖子评论
    like(args.uid, args.token, post_id)                                 # 对feed流第一个帖子点赞
    get_post_detail(args.uid, args.token, post_id)                      # 获取帖子详情
    get_comment(args.uid, args.token, post_id)                          # 拉取第一个帖子的评论
    report(args.uid, args.token, post_id)                               # 举报
    delete_post(args.uid, args.token, post_id)                          # 删帖
    get_message(args.uid, args.token)                                   # 拉取消息列表
    get_unread_message(args.uid, args.token)                            # 拉取未读的消息列表
    qi_niu(args.uid, args.token)                                        # 获取七牛图片token
    set_push_switch(args.uid, args.token)                               # 打开push开关
    get_settings(args.uid, args.token)                                  # 获取设置配置
    topic_post(args.uid, args.token)                                   # 获取某个话题的帖子
