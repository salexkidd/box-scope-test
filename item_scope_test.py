#!/usr/bin/env python
"""item_scope_test.py

Usage:
  item_scope_test.py <JWT-FILE> <USER-ID> --test-folder=<BOX-FOLDER-ID> [--scopes=<SCOPES>] [--tests=<TESTS>]

Options:
  --test-folder=<BOX-FOLDER-ID>     Folder tree root folder. [default: 0]
  --scopes=<SCOPES>                 Scopes
  --tests=<TESTS>                    tests
"""
import sys
from datetime import datetime

from docopt import docopt
from loguru import logger
import json
from libs import get_auth, get_client, get_target_user, load_test_modules


def json_format(data):
    try:
        return json.dumps(data, indent=2, ensure_ascii=False)
    except Exception as e:
        return data


def main(opt):
    modules = None
    try:
        modules = load_test_modules(opt)
        logger.success("Load test module complete")
    except Exception as e:
        logger.error(e)
        sys.exit(1)

    sa_client = None
    try:
        sa_client = get_client(get_auth(opt))
    except Exception as e:
        logger.error(e)
        sys.exit(1)

    try:
        target_user = get_target_user(sa_client, opt["<USER-ID>"])
    except Exception as e:
        logger.error(e)
        sys.exit(1)

    try:
        user_client = get_client(get_auth(opt, user=target_user))
    except Exception as e:
        logger.error(e)
        sys.exit(1)

    scopes = list()
    try:
        if opt["--scopes"]:
            scopes = opt["--scopes"].split(",")
    except Exception as e:
        logger.error(e)
        sys.exit(1)


    test_folder = None
    try:
        test_folder = user_client.folder(opt["--test-folder"]).get()
    except Exception as e:
        logger.error("Can't get test folder.")
        sys.exit(1)


    rendering_params = {
        "result": {},
        "modules": [],
    }
    for m in modules:
        module_name = m.__name__.replace(".", "_")
        rendering_params["result"][module_name] = m.test_func(opt, sa_client, user_client, target_user, test_folder, scopes)
        rendering_params["modules"].append(module_name)

    from jinja2 import Template, Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader('./templates', encoding='utf8'))
    env.filters['json_format'] = json_format
    tmpl = env.get_template('result.j2')
    open ("./result.html", "w").write(tmpl.render(rendering_params))


if __name__ == "__main__":
    opt = docopt(__doc__)
    main(opt)
