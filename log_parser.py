# import re # library of regular expressions

# example
# line = '172.16.0.3 - - [25/Sep/2002:14:04:19 +0200] "GET / HTTP/1.1" 401 - "" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.1) Gecko/20020827"'
# regex = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) - "(.*?)" "(.*?)"'
# print re.match(regex, line).groups()
# ('172.16.0.3', '25/Sep/2002:14:04:19 +0200', 'GET / HTTP/1.1', '401', '', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.1) Gecko/20020827')

# Reference: https://www.loganalyzer.net/log-analyzer/apache-combined-log.html
# APACHE/NCSA COMBINED LOG FORMAT
# A "combined" log file format is like this: 
# 216.67.1.91 - leon [01/Jul/2002:12:11:52 +0000] "GET /index.html HTTP/1.1" 200 431"http://www.loganalyzer.net/" "Mozilla/4.05 [en] (WinNT; I)" "USERID=CustomerA;IMPID=01234" 
# <host> <identity> <username> <date:time> <request> <statuscode> <bytes> <referrer> <user_agent> <cookie>
# date:time ([01/Jul/2002:12:11:52 +0000] in the example) 
# The date and time stamp of the HTTP request. 
# The fields in the date/time field are: [dd/MMM/yyyy:hh:mm:ss +-hhmm] 
# +-hhmm is the time zone 


# Parse Apache Logs to Create a Pandas Dataframe
import  pandas
import binascii
from urllib.parse import unquote # Python 3
# from urllib import unquote       # Python 2
# TODO
# file path
file_path = './access_log'

def convert_str(ss):
    x = eval('b"' + ss + '"')
    return x.decode('shift-jis')

# Preprocessing of Apache Logs
# 1. parse Apache Logs
def parseApacheLogs(filename):
    fields = ['host', 'identity', 'user', 'time_part1', 'time_part2', 'cmd_path_proto', 'http_code', 'response_bytes', 'referer', 'user_agent', 'unkown']
    # data = pandas.read_csv(filename, compression='gzip', sep=' ', header=None, names=fields, na_values=['-'])
    data = pandas.read_csv(filename, encoding='utf-8', sep=' ', header=None, names=fields, na_values=['-'])
    data['unkown'] = data['unkown'].map(lambda s : convert_str(s))

    # Panda's parser mistakenly splits the date into two columns, so we must concatenate them
    time = data.time_part1 + data.time_part2
    time_trimmed = time.map(lambda s: s.strip('[]').split('+')[0]) # Drop the timezone for simplicity
    data['time'] = pandas.to_datetime(time_trimmed, format='%d/%b/%Y:%H:%M:%S')

    # Split column `cmd_path_proto` into three columns(command, path, protocol), and decode the URL (ex: '%20' => ' ')
    data['command'], data['path'], data['protocol'] = zip(*data['cmd_path_proto'].str.split().tolist())
    data['path'] = data['path'].map(lambda s: unquote(s))
    # Drop the fixed columns and any empty ones
    data1 = data.drop(['time_part1', 'time_part2', 'cmd_path_proto'], axis=1)
    return data1.dropna(axis=1, how='all')

logs = parseApacheLogs(file_path)
logs[:3]

# 2. extract the website's Logs 

logs.to_csv('./output_access_log.csv', sep=',', encoding='shift-jis')

# 2.1 delete the logs about images and so on(.jpg, .git, .pgn, .css, .js, .pl)

# 2.2  delete the logs about google crawlers and other tool


# 3. count the data I want

# 3.1 count unique user
# user_count = df['identity'].unique()

# 3.2 count session: same user's view is in 30 minutes from last page view shoule be seen as same session 
# 


# Reference: 
# 1. アクセスログデータの前処理、ユーザIDとセッションの生成、URLの集約 (https://www.marketechlabo.com/access-log-data-preparation/)

# OTHER
# binary to shift-jis
# b = b'\x82h'
# s = b.decode('shift-jis')
# print(s)

