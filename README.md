# 21UploadBug
Demonstrates a bug with uploading files on 21 network

## To reproduce
On Server A run:
```
$ python3 server.py
```

In another terminal on Server A run:
```
$ python3 client.py
```

You will notice the upload is successful.

On Server B run:
```
$ python3 client.py --target=SERVER_A_IP
```

You will notice the upload fails with:
```
Failure: ('Connection aborted.', BrokenPipeError(32, 'Broken pipe'))
```
