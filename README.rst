HydrOffice BAG Tools
====================

.. image:: https://github.com/hydroffice/hyo2_bag/raw/master/hyo2/bag/media/favicon.png
    :alt: logo

|

.. image:: https://img.shields.io/pypi/v/hyo2.bag.svg
    :target: https://pypi.python.org/pypi/hyo2.bag
    :alt: PyPi version

.. image:: https://github.com/hydroffice/hyo2_bag/actions/workflows/bag_on_windows.yml/badge.svg
    :target: https://github.com/hydroffice/hyo2_bag/actions/workflows/bag_on_windows.yml
    :alt: Windows

.. image:: https://github.com/hydroffice/hyo2_bag/actions/workflows/bag_on_linux.yml/badge.svg
    :target: https://github.com/hydroffice/hyo2_bag/actions/workflows/bag_on_linux.yml
    :alt: Linux

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
    :target: https://www.hydroffice.org/manuals/bag/index.html
    :alt: Latest Documentation

.. image:: https://app.codacy.com/project/badge/Grade/b39ce4141d3e412fa789c7d5ee4971f3
    :target: https://app.codacy.com/gh/hydroffice/hyo2_bag/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade
    :alt: codacy

.. image:: https://coveralls.io/repos/github/hydroffice/hyo2_bag/badge.svg?branch=master
    :target: https://coveralls.io/github/hydroffice/hyo2_bag?branch=master
    :alt: coverall

|

* GitHub: `https://github.com/hydroffice/hyo2_bag <https://github.com/hydroffice/hyo2_bag>`_
* Project page: `url <https://www.hydroffice.org/bag>`_
* License: LGPLv3 or IA license (See `Dual license <https://www.hydroffice.org/license/>`_)

|

General Info
------------

HydrOffice is a research development environment for ocean mapping. It provides a collection of hydro-packages, each of them dealing with a specific issue of the field.
The main goal is to speed up both algorithms testing and research-2-operation.

The BAG Tools hydro-package collects tools for working with BAG files. BAG is a data format by the `ONS-WG <http://www.opennavsurf.org/>`_ (Open Navigation Surface Working Group).


Dependencies
------------

For the BAG library, you will need:

* ``python`` *[>=3.5]*
* ``numpy``
* ``h5py``
* ``lxml``
* ``gdal``
* ``PyInstaller`` *[for freezing the tools]*

For running some of the example scripts, you might also need:

* ``matplotlib``
