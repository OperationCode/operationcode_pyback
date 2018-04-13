import json
import pprint

from flask import render_template
import requests


def handle_code_school():
    return render_template("code_school.html")


def create_issue(request, logo, url_root):
    url = 'https://api.github.com/repos/AllenAnthes/Database-Project-Front-end/issues'
    headers = {"Authorization": "Bearer 8328d8749e5a0ff817f60e97ee05c895e4e270a8"}
    flat = request.to_dict()
    params = make_params(**flat, url_root=url_root, school_logo=logo)
    pprint.pprint(params)
    res = requests.post(url, headers=headers, data=json.dumps(params))
    pprint.pprint(res)
    return res


def make_params(name, url, address1, address2, city, state, zipcode, country, rep_name,
                rep_email, school_logo, url_root, fulltime=False, hardware=False, has_online=False, online_only=False,
                va_accepted=False):
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
