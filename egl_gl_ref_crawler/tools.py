import re

class TagStrTools:
    def get_description(tag):
        tmp = re.sub('<.+?>', '', str(tag), 0).strip()
        tmp = re.sub('\n', '', tmp, 0).strip()
        tmp = re.sub(' +',' ', tmp, 0).strip()
        return tmp

class RstTools:
    def addElement(indent_space, title, contents):
        element = ""
        element += indent_space + title + "\n\n"
        for content in contents:
            if type(content) == list:
                for item in content:
                    element += indent_space*2 + item[0] + '\n'
                    element += indent_space*3 + item[1] + "\n\n"
            else:
                element += indent_space*2 + content + "\n\n"
        
        return element
    
    def addCodeBlock(indent_space, type, code):
        codeBlock = ""
        codeBlock += indent_space + "**Functions & Parameters**\n\n"
        codeBlock += indent_space*2 + ".. code-block:: " + type + "\n"
        codeBlock += indent_space*2 + "  " + ":linenos:\n\n"
        return codeBlock