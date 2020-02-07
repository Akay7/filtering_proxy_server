# Filtering Proxy Server
All requests to this server proxied to the original site. 
On the way back for all words contains six letters will be added symbol ™(copyright).

## Preparation
Install requirements
```
pip install -r requirements
```
If you are going to use gunicorn additionally you should install it too
```
pip install gunicorn
```

## Start proxy server
Possible start proxy server calling one of next commands from terminal: 
 ```bash
python3 proxy.py 
python3 -m aiohttp.web -H localhost -P 8070 proxy:proxy_app_factory
gunicorn proxy:proxy_app_factory --bind localhost:8060 --worker-class aiohttp.GunicornWebWorker # gunicorn is required
```

## Run tests
Possible run tests from a terminal with the command:
```bash
python3 -m tests
````

## Style Guide 
Code complies pep8 style guide except length of lines. Here max line length is 119 symbols. 
