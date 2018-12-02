Development cheatsheet
======================


Useful git commands
-------------------

Syncing a fork (without SourceTree)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add a remote that points to the upstream repo (from the forked project folder):

* ``git remote -v`` (check before and after if the remote is present)
* ``git remote add upstream https://github.com/HDFGroup/hdf-compass``

Fetching from the remote repository:

* ``git branch -va`` (check all the available branches)
* ``git fetch upstream``

Merging with the upstream repository:

* ``git checkout master`` (to switch to ``master`` branch)
* ``git merge upstream/master``

Finally:

* :``git push origin master``

Reset the fork
~~~~~~~~~~~~~~

* ``git remote add upstream https://github.com/HDFGroup/hdf-compass``
* ``git fetch upstream``
* ``git branch backup``
* ``git checkout upstream/master -B master``
* ``git push --force``

In case of need to retrieve the original code status:

* ``git checkout backup``


Documentation
-------------

The documentation is built using ``sphinx``:

* ``pip install sphinx sphinx-autobuild``

For the first time, the documentation template is created in the 'docs' folder:

* ``mkdir docs``
* ``cd docs``
* ``sphinx-quickstart``

To update the API documentation:

* ``sphinx-apidoc -f -o docs/api hydroffice hydroffice/bag/scripts``


PyPi
----

Some instructions can be found `here <https://packaging.python.org/tutorials/packaging-projects/>`_:

* ``python setup.py sdist bdist_wheel``
* ``pip install twine``
* ``twine upload dist/*``
