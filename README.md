# consulTagUpdater
Easily update consul tags


### Install
Python 2 is required.
```
git clone https://github.com/myENA/consulTagUpdater.git
cd consulTagUpdater
python setup.py install
```
#### Run directly

Note: If you do not have CONSUL_HTTP_ADDR set you must set the host flag -H.

To update specific services:
```
$ python2 con_update.py -U -S service1,service2 -T tag1,tag2
```
To list all services with a specific flag:
```
$ python2 con_update.py -H 127.0.0.1 -f ENA
{u'test': [u'ENA'], u'consul': [u'ENA'], u'tag': [u'ENA'], u'adder': [u'ENA']}
```
To list all services:
```
$ python2 con_update.py -H 127.0.0.1 --ls
Available services:
{u'test': [u'rock', u'ENA', u'Tuseday', u'Afternoon', u'proxy-standard', u'TestTag', u'preds'],
u'consul': [u'preds', u'rock', u'ENA', u'Tuseday', u'Afternoon', u'proxy-standard', u'TestTag'],
u'tag': [u'Afternoon', u'proxy-standard', u'TestTag', u'preds', u'rock', u'ENA', u'Tuseday'],
u'adder': [u'proxy-standard', u'TestTag', u'preds', u'rock', u'ENA', u'Tuseday', u'Afternoon', u'SingleService']}
```

Update services with a specific tag
```
$ python2 con_update.py -H 127.0.0.1 -f ENA -U -T proxy-standard
Service test has been updated with tags [u'TestTag', u'preds', u'rock', u'ENA', u'Tuseday', u'Afternoon', 'proxy-standard'] on node node0
Service consul has been updated with tags [u'TestTag', u'preds', u'rock', u'ENA', u'Tuseday', u'Afternoon', 'proxy-standard'] on node node0
Service tag has been updated with tags [u'TestTag', u'preds', u'rock', u'ENA', u'Tuseday', u'Afternoon', 'proxy-standard'] on node node0
Service adder has been updated with tags [u'TestTag', u'preds', u'rock', u'ENA', u'Tuseday', u'Afternoon', u'SingleService', 'proxy-standard'] on node node0
```

Update service tags with a prefix and service name based on filter
```
$ python2 con_update.py -H 127.0.0.1 -f TestTag -U --prefix boom- --Rs
Service test has been updated with tags [u'TestTag', u'again-test', u'test1', u'test2', u'test3', u'again-test', u'boom-test'] on node node0
Service consul has been updated with tags [u'TestTag', u'again-consul', u'test1', u'test2', u'test3', u'again-consul', u'boom-consul'] on node node0
Service tag has been updated with tags [u'TestTag', u'again-tag', u'test1', u'test2', u'test3', u'again-tag', u'boom-tag'] on node node0
Service adder has been updated with tags [u'TestTag', u'again-adder', u'test1', u'test2', u'test3', u'again-adder', u'boom-adder'] on node node0
```