import base64
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name,HERE/(name+'.py'))
    value = importlib.util.module_from_spec(spec);spec.loader.exec_module(value)
    return value


class DesktopTests(unittest.TestCase):
    def test_guard_scopes_only_reserved_ports_and_named_table(self):
        text=load('steam_desktop_guard').rules(1000,33,True)
        self.assertTrue(text.startswith('delete table inet fh6_steam_desktop\n'))
        self.assertNotIn('flush ruleset',text)
        self.assertIn('meta skuid != { 0, 1000 } reject',text)
        self.assertIn('meta skuid != { 0, 1000, 33 } reject',text)
        self.assertIn('iifname != "lo"',text)

    def test_payload_matches_sources(self):
        stage=load('install_steam_desktop')
        self.assertEqual(len(stage.PAYLOAD),4)
        for name,item in stage.PAYLOAD.items():
            raw=base64.b64decode(item['data'],validate=True)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),item['sha256'])
            self.assertEqual(raw,(HERE/name).read_bytes())

    def test_nginx_inherits_auth_for_browser(self):
        stage=load('install_steam_desktop')
        new=stage.NGINX_EXPECTED.replace('    location / {',stage.NGINX_BLOCK+'    location / {',1)
        self.assertEqual(new.count('location ^~ /steam-browser/'),1)
        self.assertNotIn('auth_basic off',stage.NGINX_BLOCK)
        self.assertIn('auth_basic "FH6 private";',new)
        self.assertIn('proxy_set_header Upgrade $http_upgrade;',new)

    def test_failed_uid_isolation_stops_installation(self):
        stage=load('install_steam_desktop')
        with patch.object(stage.subprocess,'run',return_value=subprocess.CompletedProcess([],0)):
            with self.assertRaises(RuntimeError):stage.check_port(9222,'fh6-editor',False)

    def test_sandbox_and_profile_retained(self):
        text=(HERE/'steam_desktop.py').read_text()
        self.assertNotIn('--no-sandbox',text)
        self.assertIn("'-nolisten', 'tcp'",text)
        self.assertIn("PROFILE.chmod(0o700)",text)
        self.assertIn('input=f\'add :91 .',text)
        self.assertIn('stderr=subprocess.DEVNULL',text)

    def test_private_environment_replaces_hidden_home(self):
        module=load('steam_desktop');profile=Path('/private/profile');runtime=Path('/private/runtime')
        env=module.browser_environment(profile,runtime,runtime/'Xauthority',
              {'HOME':'/home/hidden','XDG_RUNTIME_DIR':'/run/user/0','DBUS_SESSION_BUS_ADDRESS':'bad','PATH':'/usr/bin'})
        self.assertEqual(env['HOME'],str(profile))
        self.assertEqual(env['XDG_CONFIG_HOME'],str(profile/'config'))
        self.assertEqual(env['XDG_RUNTIME_DIR'],str(runtime))
        self.assertNotIn('DBUS_SESSION_BUS_ADDRESS',env)
        self.assertEqual(env['PATH'],'/usr/bin')


if __name__=='__main__':unittest.main()
