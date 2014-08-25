from lokit import Office
import argparse
import os

LO_PATH = "/opt/libreoffice4.3/program"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='lokitconv.py',
            description='Requires LibreOffice 4.3.0')
    parser.add_argument('-f', '--format',
            help='Known formats include:\
                For text documents: doc docx fodt html odt ott pdf txt xhtml')
    parser.add_argument('-o', '--options',
            help='Filter options, known options include: SkipImages')
    parser.add_argument('input_file')
    parser.add_argument('output_file')

    args = parser.parse_args()
    lo_path = os.getenv('LO_PATH', LO_PATH)
    lo = Office(lo_path)
    doc = lo.documentLoad(args.input_file)
    doc.saveAs(args.output_file, fmt=args.format, options=args.options)

    os._exit(0)
