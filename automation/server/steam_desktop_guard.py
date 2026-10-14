"""Isolate dedicated browser ports without changing other firewall tables."""
import pwd
import subprocess


def rules(publisher, nginx, exists=False):
    prefix = 'delete table inet fh6_steam_desktop\n' if exists else ''
    return prefix + f'''table inet fh6_steam_desktop {{
 chain input {{
  type filter hook input priority -10; policy accept;
  iifname != "lo" tcp dport {{ 9222, 5901, 6081 }} drop
 }}
 chain output {{
  type filter hook output priority -10; policy accept;
  oifname "lo" tcp dport {{ 9222, 5901 }} meta skuid != {{ 0, {publisher} }} reject
  oifname "lo" tcp dport 6081 meta skuid != {{ 0, {publisher}, {nginx} }} reject
 }}
}}
'''


def main():
    exists = subprocess.run(['/usr/sbin/nft', 'list', 'table', 'inet', 'fh6_steam_desktop'],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
    content = rules(pwd.getpwnam('fh6').pw_uid, pwd.getpwnam('www-data').pw_uid, exists)
    subprocess.run(['/usr/sbin/nft', '-c', '-f', '-'], input=content, text=True, check=True)
    subprocess.run(['/usr/sbin/nft', '-f', '-'], input=content, text=True, check=True)
    print('STEAM_DESKTOP_PORT_GUARD_READY')


if __name__ == '__main__':
    main()
