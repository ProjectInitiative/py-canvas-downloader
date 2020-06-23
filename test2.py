import argparse

parser = argparse.ArgumentParser(description='... saves many files together...')
parser.add_argument('--extract', '-x',
                    action='store_true',
                    help='extract files from an archive')
parser.add_argument('--verbose', '-v',
                    action='store_true',
                    help='verbosely list files processed')
parser.add_argument('--file', '-f',
                    # dest='file', -- only needed if the long form isn't first
                    help='use archive file or device ARCHIVE')

options = parser.parse_args()
if options.extract:
    print('yay')
if options.verbose:
    print('yay')
if options.file:
    print('yay')
