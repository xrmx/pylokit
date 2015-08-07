pylokit
=======

A python CFFI wrapper for LibreOfficeKit. Tested in cpython2,
cpython3, and pypy.

Requirements
------------

An installation of LibreOffice >= 4.3.0 is required on the same machine.

If you are using cpython you need *libffi-dev* in order to compile CFFI.

Installation
------------

.. code:: bash

    pip install pylokit

Examples
--------

A basic conversion from a rtf file to a doc:

.. code:: python

    from pylokit import Office
    import os

    lo_path = "/path/to/libreoffice/program/dir"

    with Office(lo_path) as lo:
        with lo.documentLoad("myfile.rtf") as doc:
            doc.saveAs("myfile.doc")

    os._exit(0)

Same conversion passing an explicit format and filter options:

.. code:: python

    from pylokit import Office
    import os

    lo_path = "/path/to/libreoffice/program/dir"

    with Office(lo_path) as lo:
        with lo.documentLoad("myfile.rtf") as doc:
            doc.saveAs("myfile.doc", fmt="docx", options="skipImages")

    os._exit(0)

The usage of a context manager is needed to properly handle LibreOfficeKit
file locking.
The use of _exit() instead of default exit() is required because in some
circumstances LibreOffice segfaults on process exit.

Acknowledgements
----------------

Project inspired by Olly Betts' `lloconv <https://github.com/ojwb/lloconv>`_.
