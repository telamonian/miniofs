# coding: utf-8
"""Defines the MINIOFS Opener."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__all__ = ["MINIOFSOpener"]

from fs.opener import Opener
from fs.opener.errors import OpenerError

from ._miniofs import MINIOFS


class MINIOFSOpener(Opener):
    protocols = ["minio"]

    def open_fs(self, fs_url, parse_result, writeable, create, cwd):
        bucket_name, _, dir_path = parse_result.resource.partition("/")
        if not bucket_name:
            raise OpenerError("invalid bucket name in '{}'".format(fs_url))
        strict = (
            parse_result.params["strict"] == "1"
            if "strict" in parse_result.params
            else True
        )
        miniofs = MINIOFS(
            bucket_name,
            dir_path=dir_path or "/",
            aws_access_key_id=parse_result.username or None,
            aws_secret_access_key=parse_result.password or None,
            endpoint_url=parse_result.params.get("endpoint_url", None),
            acl=parse_result.params.get("acl", None),
            cache_control=parse_result.params.get("cache_control", None),
            strict=strict,
        )
        return miniofs
