#-*- coding: utf-8 -*-

#把已知人脸添加到人脸集合中

#------------------------------------------------------------------------------
#准备阶段
API_KEY = "a4OWmRJTir1XGFx6vZtwPvlf6nsYxErQ"
API_SECRET = "Q1bR1pHjv7SGWa3xSN0tNivJ4lK0K8Tu"
#国际版的服务器地址
api_server_international = 'https://api-us.faceplusplus.com/facepp/v3/'
# 导入系统库并定义辅助函数
from pprint import pformat
def print_result(hit, result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(v): encode(k) for (v, k) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hit
    result = encode(result)
    print '\n'.join("  " + i for i in pformat(result, width=75).split('\n'))
#导入SDK中的API类
from facepp import API, File
#创建一个API对象
api = API(API_KEY, API_SECRET)

#-----------------------------------------------------------------------------

# 创建一个Faceset用来存储FaceToken
#ret = api.faceset.create(outer_id='finally')
# 本地图片的地址
face_1 = './a1.jpg'
face_2 = './hz.jpg'



# 对图片进行检测
Face = {}

res = api.faceset.getdetail(outer_id='finally')
print_result("11111",res)


res = api.detect(image_file=File(face_1))
print_result("person_1", res)
Face['person_1'] = res["faces"][0]["face_token"]
res=api.face.setuserid(face_token=Face['person_1'] ,user_id="刘哲")
# 将得到的FaceToken存进Faceset里面
api.faceset.addface(outer_id='finally', face_tokens=Face.itervalues())

res = api.detect(image_file=File(face_2))
print_result("person_2", res)
Face['person_2'] = res["faces"][0]["face_token"]
res=api.face.setuserid(face_token=Face['person_2'] ,user_id="蔡鸿铮")
# 将得到的FaceToken存进Faceset里面
api.faceset.addface(outer_id='finally', face_tokens=Face.itervalues())



