[app]
# (str) Title of your application
title = Project 1

# (str) Package name
package.name = project

# (str) Package domain
package.domain = org.test

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (leave empty to include all files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy==2.1.0,opencv-python-headless,numpy,pillow,requests

# (str) Supported orientations
orientation = portrait

# (list) Permissions
android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
# (int) Log level
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
