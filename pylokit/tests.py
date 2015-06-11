import unittest
import os

from lokit import Office, LoKitInitializeError, LoKitImportError, LoKitExportError

TEST_DIR = os.path.dirname(__file__)

class LokitTest(unittest.TestCase):
    def setUp(self):
        self.lo_path = os.getenv('LO_PATH', '/usr/lib/libreoffice/program/')
        self.test_doc = self._to_abspath("tests/foo.doc")
        self.test_out_rtf = self._to_abspath("tests/out.rtf")
        self.test_out_docx = self._to_abspath("tests/out.docx")
        self.test_out_pdf = self._to_abspath("tests/out.pdf")
        self.test_lockfile = self._to_abspath(".~lock.foo.doc#")

    def _to_abspath(self, path):
        return os.path.abspath(os.path.join(TEST_DIR, path))

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
        with lo.documentLoad(self.test_doc) as doc:
            self.assertRaises(LoKitExportError, doc.saveAs, "")

    def test_wrong_filter(self):
        with Office(self.lo_path) as lo:
            with lo.documentLoad(self.test_doc) as doc:
                self.assertRaises(LoKitExportError, doc.saveAs, self.test_out_rtf, fmt="foobar")

    def test_wrong_options(self):
        with Office(self.lo_path) as lo:
            with lo.documentLoad(self.test_doc) as doc:
                self.assertRaises(LoKitExportError, doc.saveAs, self.test_out_rtf, options="foobar")

    def test_filter_and_options(self):
        with Office(self.lo_path) as lo:
            with lo.documentLoad(self.test_doc) as doc:
                doc.saveAs(self.test_out_docx, fmt="docx", options="SkipImages")
                os.unlink(self.test_out_docx)

    def test_multiple_calls(self):
        with Office(self.lo_path) as lo:
            with lo.documentLoad(self.test_doc) as doc:
                doc.saveAs(self.test_out_docx, fmt="docx", options="SkipImages")
                doc.saveAs(self.test_out_pdf)
                os.unlink(self.test_out_docx)
                os.unlink(self.test_out_pdf)
            with lo.documentLoad(self.test_doc) as doc:
                doc.saveAs(self.test_out_pdf)
                os.unlink(self.test_out_pdf)

    def tearDown(self):
        assert os.path.exists(self.test_lockfile) == False


if __name__ == '__main__':
    unittest.main()
