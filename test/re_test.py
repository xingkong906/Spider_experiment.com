import re

pattern = re.compile(r'>\$(.*?)<')
str = '<h4 class="set-width">$6,000<br/><small>goal</small></h4>'
print(pattern.search(str).group(1))
