How to release
==============

PyInstaller
-----------

For the `BAG_<tool>.1file.spec` files, you need to verify that the following parameters are passed to the ``EXE()`` function:

* ``console=False``: to avoid that a console window is opened at run-time for standard I/O
* ``debug=False``: to avoid that the boot-loader issues progress messages while initializing and starting the bundled app

