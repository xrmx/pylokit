import unittest
import os

from lokit import Office, LoKitInitializeError, LoKitImportError, LoKitExportError


class LokitTest(unittest.TestCase):
    def setUp(self):
        self.lo_path = os.getenv('LO_PATH', '/usr/lib/libreoffice/program/')

    def test_init_no_lo_path(self):
        self.assertRaises(LoKitInitializeError, Office, "wronglopath")

    def test_init(self):
        lo = Office(self.lo_path)
        self.assertIsNotNone(lo)

    def test_no_input_file(self):
        lo = Office(self.lo_path)
        self.assertRaises(LoKitImportError, lo.documentLoad, "foo")

    def test_no_output_file(self):
        lo = Office(self.lo_path)
        doc = lo.documentLoad("tests/foo.doc")
        self.assertRaises(LoKitExportError, doc.saveAs, "")
        del doc

    def test_wrong_filter(self):
        lo = Office(self.lo_path)
        doc = lo.documentLoad("tests/foo.doc")
        self.assertRaises(LoKitExportError, doc.saveAs, "tests/out.rtf", fmt="foobar")
        del doc

    def test_wrong_options(self):
        lo = Office(self.lo_path)
        doc = lo.documentLoad("tests/foo.doc")
        self.assertRaises(LoKitExportError, doc.saveAs, "tests/out.rtf", options="foobar")
        del doc

    def test_filter_and_options(self):
        lo = Office(self.lo_path)
        doc = lo.documentLoad("tests/foo.doc")
        doc.saveAs("tests/out.docx", fmt="docx", options="SkipImages")
        os.unlink("tests/out.docx")
        del doc

    def test_multiple_calls(self):
        lo = Office(self.lo_path)
        doc = lo.documentLoad("tests/foo.doc")
        doc.saveAs("tests/out.docx", fmt="docx", options="SkipImages")
        doc.saveAs("tests/out.pdf")
        os.unlink("tests/out.docx")
        os.unlink("tests/out.pdf")
        doc = lo.documentLoad("tests/foo.doc")
        doc.saveAs("tests/out.pdf")
        os.unlink("tests/out.pdf")
        del doc

    def tearDown(self):
        assert os.path.exists("tests/.~lock.foo.doc#") == False


if __name__ == '__main__':
    unittest.main()
