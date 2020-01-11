import subprocess

def channel_sub(env, url):
    args = [
        'media-hoard',
        'subscribe',
        url
        ]

    return subprocess.check_output(args=args, encoding='utf-8', env=env)
