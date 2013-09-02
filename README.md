setup
-----

```bash
git clone git@github.com:bninja/swift-buzz.git
cd swift-buzz
mkvirtualenv swift-buzz
pip install -r requirements.txt
```

later

```bash
cd swift-buzz
workon swift-buzz
```

run
---

1
#
```bash
./1/gen.py | ./1/log.py
```

2
#
```bash
./2/party.py < ./2/test.json
./2/party.py --required 'Al Buquerque' < 2/test.json
```

3
#
```bash
./3/parade.py < ./3/test1.txt
./3/parade.py < ./3/test2.txt
```

