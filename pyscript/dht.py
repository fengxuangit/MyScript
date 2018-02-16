import base64

def thunderEncode(url):
    return ''.join(['thunder://',base64.b64encode(''.join(['AA',url,'ZZ']))])

# using example
if __name__ == "__main__":
    tUrl = thunderEncode("magnet:?xt=urn:btih:9e67f6f94476721834bfcd7f7f4f22c7880b07cb")
    print (tUrl)
