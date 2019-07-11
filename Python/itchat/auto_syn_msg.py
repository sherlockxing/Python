# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 09:33:14 2019

@author: sherlockxing
"""

import itchat
from itchat.content import *
 
     
# 自动回复文本等类别的群聊消息
# isGroupChat=True表示为群聊消息
@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def group_reply_text(msg):
    # 消息来自于哪个群聊
    chatroom_id = msg['FromUserName']
    # 发送者的昵称
    username = msg['ActualNickName']
 
    # 消息并不是来自于需要同步的群
    if not chatroom_id in chatroom_ids:
        return
 
    if msg['Type'] == TEXT:
        content = msg['Content']
    elif msg['Type'] == SHARING:
        content = msg['Text']
 
    # 根据消息类型转发至其他需要同步消息的群聊
    if msg['Type'] == TEXT:
        itchat.send('%s\n%s' % (username, msg['Content']), name)
        
    elif msg['Type'] == SHARING:
        itchat.send('%s\n%s\n%s' % (username, msg['Text'], msg['Url']), name)
 
# 自动回复图片等类别的群聊消息
# isGroupChat=True表示为群聊消息          
@itchat.msg_register([PICTURE, ATTACHMENT, VIDEO], isGroupChat=True)
def group_reply_media(msg):
    # 消息来自于哪个群聊
    chatroom_id = msg['FromUserName']
    # 发送者的昵称
    username = msg['ActualNickName']
 
    # 消息并不是来自于需要同步的群
    if not chatroom_id in chatroom_ids:
        return
    # 如果为gif图片则不转发
    if msg['FileName'][-4:] == '.gif':
        return 
    # 下载图片等文件
    msg['Text'](msg['FileName'])
    # 转发至其他需要同步消息的群聊
    itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']), name)
 
# 扫二维码登录
itchat.auto_login(enableCmdQR=True)
# 获取所有通讯录中的群聊
# 需要在微信中将需要同步的群聊都保存至通讯录
chatrooms = itchat.get_chatrooms(update=True, contactOnly=True)
#chatrooms = chatrooms[1]
chatroom_ids = [c['UserName'] for c in chatrooms]
#chatroom_ids = chatrooms['UserName']
print('正在监测的群聊：'+str(len(chatrooms))+ '个')
print(' '.join([item['NickName'] for item in chatrooms]))

#搜索发送的好友
#friends_list = itchat.get_friends(update=True)
#name = itchat.search_friends(name=u'李鹏辉')[0]["UserName"]

#搜索发送的群聊
group = itchat.get_contact()
for i in range(len(group)):
    if group[i]['NickName'] == 'test':
        name = group[i]['UserName']

# 开始监测
itchat.run()
