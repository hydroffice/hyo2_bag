How to release
==============


Documentation
-------------

The documentation is built using ``sphinx``:

* ``pip install sphinx sphinx-autobuild``

To create the documentation in html format:

* ``make html``

To create the documentation in PDF format:

* ``make latexpdf``


PyInstaller
-----------

From the root folder, run the command:

* ``pyinstaller --clean -y freeze\BAG_<tool>.1file.spec``

For the `BAG_<tool>.1file.spec` files, you need to verify that the following parameters are passed to the ``EXE()`` function:

* ``console=False``: to avoid that a console window is opened at run-time for standard I/O
* ``debug=False``: to avoid that the boot-loader issues progress messages while initializing and starting the bundled app


PyPi
----

Some instructions can be found `here <https://packaging.python.org/tutorials/packaging-projects/>`_:

* ``pip install --upgrade build``
* ``py -m build``
* ``pip install --upgrade twine``
* ``twine upload --repository pypi dist/*``

Remember to set the API token in the `.pypirc` setup file.