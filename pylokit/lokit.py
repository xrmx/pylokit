# Python cffi wrapper for LibreOfficeKit
#
# Copyright (C) 2014 Riccardo Magliocchetti
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from cffi import FFI
import six
import os


TARGET_LIB = ("libsofficeapp.so", "libmergedlo.so")

LOKIT_CDEFS = """
typedef struct _LibreOfficeKit LibreOfficeKit;
typedef struct _LibreOfficeKitClass LibreOfficeKitClass;

typedef struct _LibreOfficeKitDocument LibreOfficeKitDocument;
typedef struct _LibreOfficeKitDocumentClass LibreOfficeKitDocumentClass;

struct _LibreOfficeKit
{
    LibreOfficeKitClass* pClass;
};

struct _LibreOfficeKitClass
{
  size_t  nSize;

  void                    (*destroy)       (LibreOfficeKit *pThis);
  LibreOfficeKitDocument* (*documentLoad)  (LibreOfficeKit *pThis, const char *pURL);
  char*                   (*getError)      (LibreOfficeKit *pThis);
};

struct _LibreOfficeKitDocument
{
    LibreOfficeKitDocumentClass* pClass;
};

struct _LibreOfficeKitDocumentClass
{
  size_t  nSize;

  void (*destroy)   (LibreOfficeKitDocument* pThis);
  int (*saveAs)     (LibreOfficeKitDocument* pThis,
                     const char *pUrl,
                     const char *pFormat,
                     const char *pFilterOptions);
};
LibreOfficeKit *libreofficekit_hook(const char* install_path);
"""


class LoKitInitializeError(Exception):
    pass


class LoKitImportError(Exception):
    pass


class LoKitExportError(Exception):
    pass


class Document(object):
    def __init__(self, doc, office):
        self.doc = doc
        self.office = office

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.doc.pClass.destroy(self.doc)

    def saveAs(self, url, fmt=None, options=None):
        ffi = self.office.ffi
        if fmt:
            fmt = six.b(fmt)
        else:
            fmt = ffi.NULL
        if options:
            options = six.b(options)
        else:
            options = ffi.NULL
        saved = self.doc.pClass.saveAs(self.doc, six.b(url), fmt, options)
        if not saved:
            raise LoKitExportError(self.office.getError())
        return saved


class Office(object):
    def __init__(self, lo_path):
        ffi = FFI()
        ffi.cdef(LOKIT_CDEFS)
        lo = None
        for lib in TARGET_LIB:
            libsoffice = os.path.join(lo_path, lib)
            if os.path.exists(libsoffice):
                lo = ffi.dlopen(libsoffice)
                break

        if not lo:
            raise LoKitInitializeError("Failed to initialize LibreOfficeKit")

        self.ffi = ffi
        self.lokit = lo.libreofficekit_hook(six.b(lo_path))

    def documentLoad(self, url):
        doc = self.lokit.pClass.documentLoad(self.lokit, six.b(url))
        if not doc:
            raise LoKitImportError(self.getError())
        return Document(doc, self)

    def getError(self):
        return self.ffi.string(self.lokit.pClass.getError(self.lokit))

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        if hasattr(self, "lokit"):
            self.lokit.pClass.destroy(self.lokit)
