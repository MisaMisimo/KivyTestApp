# KivyTestApp

## Lessons Learned

### Setup

1. Setup Tutorial which worked for me:  
[Python Development Setup with Windows 10, Ubuntu Subsystem, GWSL & VS Code](https://www.youtube.com/watch?v=iJUM306kqHA)

2. When using GWSL we can't use LibGL Indirect.  
 To get around this we can use the shell comand 
```sh
export "LIBGL_ALWAYS_INDIRECT=0"
```

### Development Tips


1. We can detect if App is running on android or linux with:<sub>[[Source]](https://stackoverflow.com/questions/48019043/python-detect-android)<sub>
```python
from kivy.utils import platform
if (platform == 'android')":
   # Do something
```
2. To get top level directory path in android, use the following:<sub>[[Source]](https://stackoverflow.com/questions/64849485/why-is-filemanager-not-working-on-android-kivymd)
```python
import android
    from android.storage import primary_external_storage_path
    from android.permissions import request_permissions, Permission
```

## Useful Links
| Description | Link |
| --- | --- |
| Android Permissions | https://developer.android.com/reference/android/Manifest.permission| 
| KivyMD Docs | https://kivymd.readthedocs.io/en/1.0.2/getting-started/|
