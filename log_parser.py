import re # library of regular expressions

# example
line = '172.16.0.3 - - [25/Sep/2002:14:04:19 +0200] "GET / HTTP/1.1" 401 - "" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.1) Gecko/20020827"'
regex = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) - "(.*?)" "(.*?)"'
print re.match(regex, line).groups()
# ('172.16.0.3', '25/Sep/2002:14:04:19 +0200', 'GET / HTTP/1.1', '401', '', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.1) Gecko/20020827')

# Parse Apache Logs to Create a Pandas Dataframe
import  pandaspandas

try:
    from urllib.parse import unquote # Python 3
except ImportError:
    from urllib import unquote       # Python 2

# TODO
# file path
file_path = '/data/access.log'

def parseApacheLogs(filename):
    fields = ['host', 'identity', 'user', 'time_part1', 'time_part2', 'cmd_path_proto', 'http_code', 'response_bytes', 'referer', 'user_agent', 'unkown']
    data = pandas.read_csv(filename, compression='gzip', sep=' ', header=None, names=fields, na_values=['-'])

    # Panda's parser mistakenly splits the date into two columns, so we must concatenate them
    time = data.time_part1 + data.time_part2
    time_trimmed = time.map(lambda s: s.strip('[]').split('-')[0]) # Drop the timezone for simplicity
    data['time'] = pandas.to_datetime(time_trimmed, format='%d/%b/%Y:%H:%M:%S')

    # Split column `cmd_path_proto` into three columns(command, path, protocol), and decode the URL (ex: '%20' => ' ')
    data['command'], data['path'], data['protocol'] = zip(*data['cmd_path_proto'].str.split().tolist())
    data['path'] = data['path'].map(lambda s: unquote(s))
    
    # Drop the fixed columns and any empty ones
    data1 = data.drop(['time_part1', 'time_part2', 'cmd_path_proto'], axis=1)
    return data1.dropna(axis=1, how='all')

logs = parseApacheLogs(file_path)
logs[:3]

# TODO
logs.to_csv(output_file_name, sep='\t', encoding='utf-8')
