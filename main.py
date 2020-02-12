from olxparser import OLXParser


parser = OLXParser('https://www.olx.ua/elektronika/')

try:
    parser.parse()
except KeyboardInterrupt:
    print('\nSaving results...')
    parser.save_ads()
