from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'barrel-finder', 'src.barrel_finder.urls', name='barrel_finder'),
)
