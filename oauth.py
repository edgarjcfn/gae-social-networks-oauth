
def build_signature_string(header_data, post_data, url):
    all_data = {}

    for key, value in header_data.items():
        all_data[key] = value
    for key, value in post_data.items():
        all_data[key] = value

    encoded_data = to_querystring(all_data)

    message = '&'.join(map(encode, [
            "POST", url, encoded_data
            ]))

    return message

def sign_request(signature_string):
    return hmac(encode(CONSUMER_SECRET)+"&", signature_string, sha1).digest().encode('base64')[:-1]

def build_header_string(header_data):
    header_string = "OAuth "
    encoded_values = []
    for key,value in sorted(header_data.items()):
        encoded_values.append('{0}="{1}"'.format(encode(key), encode(value)))

    header_string += ", ".join(encoded_values)
    return header_string

def create_authorization_header(post_data, extra_data):
            header_data = {
                "oauth_consumer_key" : CONSUMER_KEY,
                "oauth_nonce" : getrandbits(64),
                "oauth_signature_method" : "HMAC-SHA1",
                "oauth_timestamp" : int(time()),
                "oauth_version" : "1.0"
            }

            signature_string = build_signature_string(header_data, post_data, REQUEST_TOKEN_URL)
            signature = sign_request(signature_string)
            
            header_data["oauth_signature"] = signature
            
            for key,value in extra_data.iteritems():
                header_data[key] = value

            return build_header_string(header_data)