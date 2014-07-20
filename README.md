# pylokit

A python CFFI wrapper for LibreOfficeKit. LibreOfficeKit is available since LibreOffice
4.3.0.

## Installation

```bash
pip install pylokit
```

## Example

```python
from pylokit import Office

lo_path = "/path/to/libreoffice/program/dir"

lo = Office(lo_path)
doc = lo.documentLoad("myfile.rtf")
doc.saveAs("myfile.doc", fmt="docx", options=None)
```
