# from oic.oic.provider import Provider
import json

from oic import rndstr
from oic.oic import OIDCONF_PATTERN
from oic.utils.sdb import SessionDB
from oic.utils.webfinger import WF_URL
from oidctest.rp.provider import Provider

__author__ = 'roland'

OIDC_PATTERN = OIDCONF_PATTERN[3:]
WEB_FINGER = WF_URL[11:]
NP = 5


def extract_mode(path):
    # path = <test_id>/<sign_alg>/<encrypt>/<behaviortype/<claims>/<endpoint>

    if path == "":
        return {}, ""

    if path[0] == '/':
        path = path[1:]

    if path == WEB_FINGER:
        return None, path

    part = path.split("/", NP)

    mod = {"test_id": part[0]}

    plen = len(part)
    if plen == 3 and path.endswith(OIDC_PATTERN):
        return mod, OIDC_PATTERN

    if plen >= 5:
        if part[4] != "_":
            try:
                mod["claims"] = part[4].split(",")
            except ValueError:
                pass
    if plen >= 4:
        if part[3] != "_":
            try:
                mod["behavior"] = part[3].split(",")
            except ValueError:
                pass

    if plen >= 3:
        if part[2] != "_":
            try:
                _enc_alg, _enc_enc = part[2].split(":")
            except ValueError:
                pass
            else:
                mod.update({"enc_alg": _enc_alg, "enc_enc": _enc_enc})

    if plen >= 2:
        if part[1] != "_":
            mod["sign_alg"] = part[1]

    if plen == NP or plen == 1:
        return mod, ""
    else:
        return mod, part[-1]


def mode2path(mode):
    # test_id/<sig-alg>/<enc-alg>/<behavior>/<userinfo>[/<endpoint>]
    if mode is None:
        mode = {}

    noop = "_/"
    try:
        path = "%s/" % mode["test_id"]
    except KeyError:
        path = ""

    try:
        path += "%s/" % mode["sign_alg"]
    except KeyError:
        path += noop

    try:
        path += "%s:%s/" % (mode["enc_alg"], mode["enc_enc"])
    except KeyError:
        path += noop

    try:
        path += "%s/" % ",".join(mode["behavior"])
    except KeyError:
        path += noop

    try:
        path += ",".join(mode["claims"])
    except KeyError:
        path += "normal"

    return path


def setup_op(mode, com_args, op_arg, trace):
    op = Provider(sdb=SessionDB(com_args["baseurl"]), **com_args)
    op.trace = trace

    for _authn in com_args["authn_broker"]:
        _authn.srv = op

    for key, val in list(op_arg.items()):
        setattr(op, key, val)

    _name = "jwks_{}.json".format(rndstr())
    filename = "./static/{}".format(_name)
    with open(filename, "w") as f:
        f.write(json.dumps(op_arg["jwks"]))
    f.close()

    op.jwks_uri = "{}static/{}".format(op_arg["baseurl"], _name)
    op.jwks_name = filename

    if op.baseurl.endswith("/"):
        div = ""
    else:
        div = "/"

    op.name = op.baseurl = "%s%s%s" % (op.baseurl, div, mode2path(mode))

    for _typ in ["signing_alg", "encryption_alg", "encryption_enc"]:
        try:
            _alg = mode[_typ]
        except (TypeError, KeyError):
            for obj in ["id_token", "request_object", "userinfo"]:
                op.jwx_def[_typ][obj] = ''
        else:
            for obj in ["id_token", "request_object", "userinfo"]:
                op.jwx_def[_typ][obj] = _alg

    if mode:
        try:
            op.claims_type = mode["claims"]
        except KeyError:
            pass

        try:
            op.behavior_type = mode["behavior"]
            op.server.behavior_type = mode["behavior"]
        except KeyError:
            pass

    return op
