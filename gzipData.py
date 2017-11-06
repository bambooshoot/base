def gzipData(file):
    if os.path.isfile(file):
        with open(file) as f:
            data = json.load(f)
            g = gzip.GzipFile(filename=none, mode='wb', compresslevel=9, fileobj=open(file + '.gz', 'wb'))
            g.write(str(data))
            g.close()