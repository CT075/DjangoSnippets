import os
import datetime

from django.conf import settings
from django.shortcuts import render, render_to_response

# various stuff for the directory display code

class FileData(object):
    __slots__ = ['name', 'iname', 'slink', 'size', 'last_mod', 'path']
    def __init__(self, root, obj):
        self.slink = obj.is_symlink()
        self.name = obj.name
        self.path = os.path.join(root, self.name)
        self.iname = ("0" if obj.is_dir() else "1") + obj.name
        stats = obj.stat()
        self.size = stats.st_size
        self.last_mod = datetime.datetime.fromtimestamp(stats.st_mtime)

def display_dir(root):
    if settings.DEBUG:
        static_root = os.path.relpath(
            root,
            max(filter(
                lambda s:root.startswith(s), settings.STATICFILES_DIRS
            ), key=len)
        )
    else:
        static_root = os.path.relpath(root, settings.STATIC_ROOT)
    def display_dir_inner(request, path):
        files = []
        dirs = []
        fullpath = os.path.join(root, path)
        for obj in os.scandir(fullpath):
            fileobj = FileData(path, obj)
            if obj.is_dir(follow_symlinks=False): dirs.append(fileobj)
            else: files.append(fileobj)
        return render_to_response('folDIR.html', {
            'files' : files,
            'dirs' : dirs,
            # DO NOT dirname the full path. By only taking the dirname of the
            # relative path, we make it easy for our url processor to isolate
            # the information it needs to.
            'prev' : os.path.dirname(path),
            'dirroot' : static_root
        })
    return display_dir_inner

