import os
import re

from flask import Blueprint, request, abort, current_app, send_file

from logviewer2.constants import Constants

Fproxy = Blueprint('fproxy', __name__, url_prefix='/fproxy')


@Fproxy.get('/gg_sans_normal400')
@Fproxy.get('/gg_sans_italic400')
@Fproxy.get('/gg_sans_normal500')
@Fproxy.get('/gg_sans_italic500')
@Fproxy.get('/gg_sans_normal600')
@Fproxy.get('/gg_sans_italic600')
@Fproxy.get('/gg_sans_normal700')
@Fproxy.get('/gg_sans_italic700')
@Fproxy.get('/gg_sans_normal800')
@Fproxy.get('/gg_sans_italic800')
def rfproxy():
    match = re.match(Constants.RE_FPROXY_FACE, request.url_rule.rule)
    if match:
        if not match.groups()[0] in Constants.FONTS:
            return abort(404)
        try:
            abs_path = os.path.join(current_app.config['FDIR'].name, match.groups()[0])
            if not os.path.exists(abs_path):
                return abort(404)

            # Check if path is a file and serve
            if os.path.isfile(abs_path):
                return send_file(str(abs_path))
        except:
            return abort(404)
    else:
        return abort(404)
