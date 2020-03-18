# MINIOFS

MINIOFS is a [PyFilesystem](https://www.pyfilesystem.org/) interface to [MinIO](https://github.com/minio/minio)'s very special dialect of the Amazon S3 cloud storage api.

As a PyFilesystem concrete class, [MINIOFS](http://fs-miniofs.readthedocs.io/en/latest/) allows you to work with MinIO-flavored S3 in the same way as any other supported filesystem.

MINIOFS is a minimal fork of the [S3FS project](https://github.com/PyFilesystem/s3fs), which is a PyFilesystem interface that works with the vanilla S3 api.

## Installing

You can install MINIOFS from pip as follows:

```
pip install fs-miniofs
```

## Opening a MINIOFS

Open an MINIOFS by explicitly using the constructor:

```python
from fs_miniofs import MINIOFS
miniofs = MINIOFS('mybucket')
```

Or with a FS URL:

```python
  from fs import open_fs
  miniofs = open_fs('s3://mybucket')
```

## Downloading Files

To *download* files from an S3 bucket, open a file on the S3
filesystem for reading, then write the data to a file on the local
filesystem. Here's an example that copies a file `example.mov` from
S3 to your HD:

```python
from fs.tools import copy_file_data
with miniofs.open('example.mov', 'rb') as remote_file:
    with open('example.mov', 'wb') as local_file:
        copy_file_data(remote_file, local_file)
```

Although it is preferable to use the higher-level functionality in the
`fs.copy` module. Here's an example:

```python
from fs.copy import copy_file
copy_file(miniofs, 'example.mov', './', 'example.mov')
```

## Uploading Files

You can *upload* files in the same way. Simply copy a file from a
source filesystem to the S3 filesystem.
See [Moving and Copying](https://docs.pyfilesystem.org/en/latest/guide.html#moving-and-copying)
for more information.

## ExtraArgs

S3 objects have additional properties, beyond a traditional
filesystem. These options can be set using the ``upload_args``
and ``download_args`` properties. which are handed to upload
and download methods, as appropriate, for the lifetime of the
filesystem instance.

For example, to set the ``cache-control`` header of all objects
uploaded to a bucket:

```python
import fs, fs.mirror
miniofs = MINIOFS('example', upload_args={"CacheControl": "max-age=2592000", "ACL": "public-read"})
fs.mirror.mirror('/path/to/mirror', miniofs)
```

see [the Boto3 docs](https://boto3.readthedocs.io/en/latest/reference/customizations/s3.html#boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS)
for more information.

`acl` and `cache_control` are exposed explicitly for convenience, and can be used in URLs.
It is important to URL-Escape the `cache_control` value in a URL, as it may contain special characters.

```python
import fs, fs.mirror
with open fs.open_fs('s3://example?acl=public-read&cache_control=max-age%3D2592000%2Cpublic') as miniofs
    fs.mirror.mirror('/path/to/mirror', miniofs)
```


## S3 URLs

You can get a public URL to a file on a S3 bucket as follows:

```python
movie_url = miniofs.geturl('example.mov')
```

## Documentation

- [PyFilesystem Wiki](https://www.pyfilesystem.org)
- [MINIOFS Reference](http://fs-miniofs.readthedocs.io/en/latest/)
- [PyFilesystem Reference](https://docs.pyfilesystem.org/en/latest/reference/base.html)
