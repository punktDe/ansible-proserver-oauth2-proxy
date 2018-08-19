import hashlib
import base64


def oauth2_proxy_htpasswd(username_password):
    hash = hashlib.new('sha1')
    hash.update(username_password[1].encode('utf-8'))
    return '{}:{{{}}}{}'.format(username_password[0], 'SHA', base64.standard_b64encode(hash.digest()).decode())


class FilterModule(object):
    def filters(self):
        return {
            'oauth2_proxy_htpasswd': oauth2_proxy_htpasswd,
        }
