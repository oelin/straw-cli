import os
import sys
import argparse
from etaprogress.progress import ProgressBar
import straw


parser = argparse.ArgumentParser(
        prog='straw-cli',
        description='Extract images from PDF files!',
)


parser.add_argument('source', help='Source PDF file.')
parser.add_argument('-d', '--destination', default='.', help='Destination directory.')
parser.add_argument('-p', '--prefix', default='', help='Prefix for saved image file names.')


def main():
        arguments = parser.parse_args()
        source, destination = arguments.source, arguments.destination

        source = os.path.abspath(source)
        destination = os.path.abspath(destination)


        if not os.path.isfile(source):
                return print('straw-cli: error: file does not exist at source path.')


        if not os.path.isdir(destination):
                return print('straw-cli: error: directory does not exist at destination path.')


        try:
                print(f'straw-cli: info: extracting images from {os.path.basename(source)}...')

                images = straw.extract_images(source)
                total = len(images)
                progress = ProgressBar(total, max_width=40)

                if total < 1:
                        return print(f'straw-cli: info: no images found in source PDF.')

                print(f'straw-cli: info: found {total} images.')
                print(f'straw-cli: info: saving to {destination}...')

                for i, image in enumerate(images):

                        progress.numerator = i + 1
                        print(progress, end='\r')

                        with open(destination + '/' + arguments.prefix + image.name, 'wb') as file:
                                file.write(image.data)
        except Exception as e:
                print(e)
                return print('straw-cli: error: unable to extract images.')


if __name__ == '__main__':
        main()
