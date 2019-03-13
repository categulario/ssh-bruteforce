from gevent import monkey
import gevent

monkey.patch_all()

import paramiko
import random


def try_pass(password):
    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        '127.0.0.1',
        username='root',
        password='root',
        port='2222',
        allow_agent=False,
        look_for_keys=False,
        auth_timeout=1,
    )
    client.close()


def failedpassword():
    gevent.sleep((.5 - random.random())/10)
    return 'failed'


def foundpassword():
    gevent.sleep((.5 - random.random())/10)
    return 'found'


if __name__ == '__main__':
    greenlets = [
        gevent.spawn(failedpassword) for _ in range(10)
    ] + [gevent.spawn(foundpassword)] + [
        gevent.spawn(failedpassword) for _ in range(10)
    ]

    for g in gevent.iwait(greenlets):
        print(g.value)
        if g.value == 'found':
            gevent.killall(greenlets)
            break

    print('finished')
