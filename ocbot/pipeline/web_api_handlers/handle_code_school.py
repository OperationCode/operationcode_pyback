import json
import pprint

from flask import render_template, jsonify
import requests
from config.configs import configs


recaptcha_secret = configs['recaptcha_secret']
github_jwt = configs['github_jwt']


def handle_code_school():
    return render_template("code_school.html")


def verify_recaptcha(ip_value, recaptcha_value):

    req = requests.post('https://www.google.com/recaptcha/api/siteverify',
                        data={'secret': recaptcha_secret,
                              'response': recaptcha_value,
                              'remoteip': ip_value})

    return req.json().get('success', False)




def handle_recaptcha_and_errors(request, imagefile):
    request_dict = request.form.to_dict()

    recaptcha_val = request_dict.pop('g-recaptcha-response')
    ip_value = request.remote_addr
    if verify_recaptcha(ip_value, recaptcha_val):
        res = create_issue(request_dict, imagefile.filename, url_root=request.url_root)
        if res.status_code == 201:
            return jsonify(
                {"redirect": 'https://github.com/AllenAnthes/Database-Project-Front-end/issues', 'code': 302})
    return ''


def create_issue(request_dict, logo, url_root):
    url = 'https://api.github.com/repos/AllenAnthes/Database-Project-Front-end/issues'
    headers = {"Authorization": f"Bearer {github_jwt}"}

    params = make_params(**request_dict, url_root=url_root, school_logo=logo)
    pprint.pprint(params)
    res = requests.post(url, headers=headers, data=json.dumps(params))
    pprint.pprint(res)
    return res


def make_params(name, url, address1, address2, city, state, zipcode, country, rep_name,
                rep_email, school_logo, url_root, fulltime=False, hardware=False, has_online=False, online_only=False,
                va_accepted=False, g_captcha_response=False):
    fulltime = False if not fulltime else True
    hardware = False if not hardware else True
    has_online = False if not has_online else True
    online_only = False if not online_only else True
    va_accepted = False if not va_accepted else True

    return ({
        'title': f'New Code School Request: {name}',
        'body': (
            f"Name: {name}\n"
            f"url: {url}\n"
            f"full_time: {fulltime}\n"
            f"hardware_included: {hardware}\n"
            f"has_online: {has_online}\n"
            f"online_only: {online_only}\n"
            f"va_accepted: {va_accepted}\n"
            f"address: {address1} {address2}\n"
            f"city: {city}\n"
            f"state: {state}\n"
            f"country: {country}\n"
            f"zip: {zipcode}\n\n"
            f"rep name: {rep_name}\n"
            f"rep email: {rep_email}\n"
            f"logo: ![school-logo]({url_root}images/{school_logo})\n"
            # f"logo: ![school-logo](https://pybot.ngrok.io/images/{school_logo})\n"
        )
    })
