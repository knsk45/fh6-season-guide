# Tasks from the private phone panel

The existing authenticated VPN/LAN panel accepts one owner task at a time
(up to 2000 characters). `fh6-phone-tasks.timer` checks every 30 seconds.
The worker uses the publisher's existing runner lock and reserves the daily
05:35–06:20 and Thursday 20:05–21:50 Asia/Krasnoyarsk schedule windows.

Codex runs as `fh6-editor`, using its existing private login, in
`/var/lib/fh6/task-workspaces/<id>`. Only tracked regular repository files and
current canonical state/source notes are copied; `.git`, ignored credentials,
guard run state and symlink targets are not copied. The task is plain model
input, never interpolated into a shell command. No privileged task-command
endpoint or publisher invocation is provided.

The panel displays the final response and terminal state. It escapes model
and owner text. Raw process logs remain root-only in `/var/lib/fh6/task-logs`.
Tasks time out after 20 minutes; process groups and systemd control groups
are stopped. Interrupted tasks are marked explicitly rather than replayed.
Login errors require the owner to reconnect and submit again.

This is a proposal workspace, not unattended deployment. Edits stay in the
task workspace. They do not change `/opt/fh6/repo`, update a guide or install
a service. Steam publication still requires its separate owner approval,
authenticated browser editing and public verification.

Install the pinned `automation/server/install_phone_tasks.py` as root inside
CT109. It refuses unknown panel versions or an active pipeline, backs up
replaced files, runs isolated tests, then enables the queue timer and restarts
the existing panel. It never submits a real task during installation.

Try: “Проверь, что потребуется для обновления двух разделов Steam после
разрешения владельца. Подготовь план; ничего не публикуй.”

For rollback, stop/disable `fh6-phone-tasks.timer`, stop
`fh6-phone-tasks.service`, restore the previous panel from the printed backup
and restart `fh6-phone.service`. Existing task records and workspace proposals
can be retained for review. The daily refresh/recovery configuration is not
modified by this installer.
