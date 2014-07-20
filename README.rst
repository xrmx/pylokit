pylokit
=======

A python CFFI wrapper for LibreOfficeKit. Tested with both cpython2 and
cpython3, need confirmation but should work fine in pypy too.

Requirements
------------

An installation of LibreOffice >= 4.3.0 is required on the same machine

Installation
------------

.. code:: bash

    pip install pylokit

Example
-------

A basic conversion from a rtf file to a doc:

.. code:: python

    from pylokit import Office

    lo_path = "/path/to/libreoffice/program/dir"

    lo = Office(lo_path)
    doc = lo.documentLoad("myfile.rtf")
    doc.saveAs("myfile.doc")

Same conversion passing an explicit format and filter options:

.. code:: python

    from pylokit import Office

    lo_path = "/path/to/libreoffice/program/dir"

    lo = Office(lo_path)
    doc = lo.documentLoad("myfile.rtf")
    doc.saveAs("myfile.doc", fmt="docx", options="skipImages")

