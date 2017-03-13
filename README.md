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
```
cd consulTagUpdater
python con_update.py -U -S service1,service2 -T tag1,tag2
```

If you do not have CONSUL_HTTP_ADDR set you must set the host flag -H.