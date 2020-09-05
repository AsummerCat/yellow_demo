data = '''
[settings]
default = yellow_download.settings
[deploy]
# url = http://localhost:6800/
project = yellow_download
'''

with open('scrapy.cfg', 'w') as f:
    f.write(data)