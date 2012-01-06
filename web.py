import os
import simplejson as json
import urllib
import urllib2
from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config.from_object('conf.Config')

def oauth_login_url(*scope):
  fb_login_uri = ("https://www.facebook.com/dialog/oauth"
    "?client_id=%s&redirect_uri=%s" %
    (app.config['FB_APP_ID'], get_home()))

  if scope:
    fb_login_uri += "&scope=%s" % ",".join(scope)
  return fb_login_uri

def fb_get_string(path, domain=u'graph', params=None, access_token=None,
                     encode_func=urllib.urlencode):
    if not params:
        params = {}
    params[u'method'] = u'GET'
    if access_token:
        params[u'access_token'] = access_token

    for k, v in params.iteritems():
        if hasattr(v, 'encode'):
            params[k] = v.encode('utf-8')

    url = u'https://' + domain + u'.facebook.com/' + path
    params_encoded = encode_func(params)
    url = url + '?' + params_encoded
    result = urllib2.urlopen(url).read()

    return result

def fb_get_access_token(code):
  params = {'client_id': app.config['FB_APP_ID'],
            'redirect_uri': get_home(),
            'client_secret': app.config['FB_APP_SECRET'],
            'code': code
           }

  resp= fb_get_string(
    path=u"/oauth/access_token",
    params=params,
    domain=u'graph')

  params = resp.split("&", 1)
  resp_dict = {}
  for kv_pair in params:
    (key, value) = kv_pair.split("=")
    resp_dict[key] = value

  return resp_dict["access_token"]

def fb_gapi_call(call, args=None):
  return json.loads(fb_get_string(path=call, params=args))

def get_home():
  protocol = 'http'
  if request.is_secure:
    protocol = 'https'
  return protocol + '://' + request.host + '/'

@app.route("/", methods=['GET'])
def index():
  if request.args.get('code', None):
    token = fb_get_access_token(request.args.get('code'))
    me = fb_gapi_call('me', args={'access_token':token});
    return render_template('index.html', name=me['name'])
  else:
    return redirect(oauth_login_url())

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
