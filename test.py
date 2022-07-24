import urllib.request as urllib2
import urllib
import json
from basic import Basic
from poster3.streaminghttp import register_openers

class Material(object):
    def __init__(self):
        register_openers()

    def upload(self, accessToken, filePath, mediaType):
        openFile = open(filePath, "rb")
        fileName = "hello"
        param = {'media': openFile, 'filename': fileName}
        postData, postHeaders = poster.encode.multipart_encode(param)

        postUrl = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=%s" % (accessToken, mediaType)
        request = urllib2.Request(postUrl, postData, postHeaders)
        urlResp = urllib2.urlopen(request)
        print(urlResp.read())

    def get(self, accessToken, mediaId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=%s" % accessToken
        # postData = "{ \"media_id\": \"%s\" }" % mediaId
        # postData = "{ "media_id": \"%s\" }"

        raw = {'media_id': 'rdDqae0kigVCEbdBk88Or8vGP8rJW5dbImR5dgUjGZmEXbEM1pT1t15Mz_l24s3l'}
        data = json.dumps(raw)
        data = bytes(data, 'utf8')
        # postData = bytes(urllib.parse.urlencode({'media_id': 'rdDqae0kigVCEbdBk88Or8vGP8rJW5dbImR5dgUjGZmEXbEM1pT1t15Mz_l24s3l'}), encoding='utf8')
        urlResp = urllib2.urlopen(postUrl, data)
        print(urlResp.info())
        headers = urlResp.info().__dict__['headers']
        if ('Content-Type: application/json\r\n' in headers) or ('Content-Type: text/plain\r\n' in headers):
            jsonDic = json.loads(urlResp.read())
            print(jsonDic)
        else:
            buffer = urlResp.read()
            mediaFile = file("test_media.jpg", "wb")
            mediaFile.write(buffer)
            print("get successful")
    
    def delete(self, accessToken, mediaId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/del_material?access_token=%s" % accessToken
        postData = "{ \"media_id\": \"rdDqae0kigVCEbdBk88Or8vGP8rJW5dbImR5dgUjGZmEXbEM1pT1t15Mz_l24s3l\" }" % mediaId
        urlResp = urllib2.urlopen(postUrl, postData)
        print(urlResp.read())
    
    def batch_get(self, accessToken, mediaType, offset=0, count=20):
        postUrl = ("https://api.weixin.qq.com/cgi-bin/material"
               "/batchget_material?access_token=%s" % accessToken)
        
        postData = ("{ \"type\": \"%s\", \"offset\": %d, \"count\": %d }"
                    % (mediaType, offset, count))
        data = bytes(postData, encoding='utf8')
        print(json.dumps(postData).encode())
        urlResp = urllib2.urlopen(postUrl, json.dumps(postData).encode())
        print(urlResp.read())


if __name__ == '__main__':
    myMaterial = Material()
    accessToken = Basic().get_access_token()
    mediaType = 'image'
    # myMaterial.batch_get(accessToken, mediaType)
    myMaterial.get(accessToken, "rdDqae0kigVCEbdBk88Or8vGP8rJW5dbImR5dgUjGZmEXbEM1pT1t15Mz_l24s3l")