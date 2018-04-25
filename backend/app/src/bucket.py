
import requests


def draw(account):
    url = 'https://faucet.metamask.io/'
    headers = {'content-type': 'application/rawdata'}
    res = requests.post(url, data=account, headers=headers).text
    return res


"""
curl 'https://faucet.metamask.io/'
-H 'pragma: no-cache'
-H 'cookie: _ga=GA1.2.1713865361.1524650093;
_gid=GA1.2.606880881.1524650093'
-H 'origin: https://faucet.metamask.io'
-H 'accept-encoding: gzip, deflate, br'
-H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'
-H 'user-agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
-H 'content-type: application/rawdata'
-H 'accept: */*' -H 'cache-control: no-cache'
-H 'authority: faucet.metamask.io'
-H 'referer: https://faucet.metamask.io/'
--data-binary '0x88c0cc482762184dca62395b9407c9eb833bdfc8'
--compressed
"""


if __name__ == "__main__":
    account = '0x50f4e3c43e2ca8c3f7ed5a51bb4e295590d6a435'
    print('res is ', draw(account))
