########### Python 2.7 #############
import httplib, urllib, base64

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '126503e73c86415ea39302b76fa1b6d8',
}

params = urllib.urlencode({
      "name": "sample_list",
  "userData": "User-provided data attached to the face list.",
  "recognitionModel": "recognition_01"
})


try:
    conn = httplib.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
    conn.request("PUT", "/face/v1.0/facelists/simple_user_list?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################
