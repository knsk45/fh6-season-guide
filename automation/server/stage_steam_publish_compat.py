"""Stage the reviewed publisher with the verified deployed panel test version."""
import hashlib
import types
import urllib.request

URL = ('https://raw.githubusercontent.com/knsk45/fh6-season-guide/'
       '4723cc81819ca6d04b5ab22488374f2aad92f399/'
       'automation/server/stage_steam_publish.py')
INSTALLER_SHA256 = 'edc2295782249d30bdf27b0a552d63c491445c5555605012d516a296b9839830'
DEPLOYED_TEST_SHA256 = '4e702a42278861b5d4a6273f33ab2087a2902dc27458c073d427fbc20d8c3626'


def load_installer(raw):
    if hashlib.sha256(raw).hexdigest() != INSTALLER_SHA256:
        raise RuntimeError('Pinned installer mismatch; nothing changed')
    module = types.ModuleType('fh6_steam_stage')
    exec(compile(raw, URL, 'exec'), module.__dict__)
    item = module.MANIFEST['automation/server/test_phone_view.py']
    if DEPLOYED_TEST_SHA256 not in item['previous']:
        item['previous'].append(DEPLOYED_TEST_SHA256)
    return module


def main():
    with urllib.request.urlopen(URL, timeout=45) as response:
        raw = response.read(200000)
    load_installer(raw).main()


if __name__ == '__main__':
    main()
