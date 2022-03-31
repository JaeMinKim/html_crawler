import re

class TagStrTools:
    def get_description(tag):
        tmp = re.sub('<.+?>', '', str(tag), 0).strip()
        tmp = re.sub('\n', '', tmp, 0).strip()
        tmp = re.sub(' +',' ', tmp, 0).strip()
        return tmp