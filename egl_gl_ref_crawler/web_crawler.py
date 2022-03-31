from tools import TagStrTools, RstTools
import requests
from bs4 import BeautifulSoup

# url = "https://www.khronos.org/registry/EGL/sdk/docs/man/html/eglCreateContext.xhtml"
url = "https://www.khronos.org/registry/EGL/sdk/docs/man/html/eglDestroyContext.xhtml"

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

else:
    print(response.status_code)

# name
apiName = soup.select_one('div.refentry').get('id')
apiInfo = soup.select_one('div.refnamediv p')
apiInfo = TagStrTools.get_description(str(apiInfo))
print(apiName)
# print(apiInfo)

# function proto type
trs = soup.select('table.funcprototype-table tr')
funcProtoType = []
for i in range(0, len(trs)):
    tds = trs[i].find_all('td')
    tdData = []
    
    for j in range(0, len(tds)):
        element = TagStrTools.get_description(str(tds[j]))
        tdData.append(element)
    
    funcProtoType.append(tdData)
# print(funcProtoType)

# function parameter
paramList = soup.select_one('div.refsect1#parameters')
dts = paramList.find_all('dt')
dds = paramList.find_all('dd')
params = []
for i in range (0, len(dts)):
    params.append((TagStrTools.get_description(str(dts[i])), TagStrTools.get_description(str(dds[i]))))
# print(params)

# function description
descriptionSect = soup.select_one('div.refsect1#description')
descriptionSect = descriptionSect.findNext().findNextSiblings()
descriptions = []
for desc in descriptionSect:
    if desc.find("dl", "variablelist") != None:
        dts = desc.find_all('dt')
        dds = desc.find_all('dd')
        constants = []
        for i in range (0, len(dts)):
            constants.append((TagStrTools.get_description(str(dts[i])), TagStrTools.get_description(str(dds[i]))))
        descriptions.append(constants)
    else:
        descriptions.append(TagStrTools.get_description(desc))
# print(descriptions)

# function error
errorSect = soup.select('div.refsect1#errors p')
errors = []
for error in errorSect:
    errors.append(TagStrTools.get_description(error))
print(errors)

##############
# make rst doc
##############
TAB_SPACE = "    "
rstDoc = ""

# api name
rstDoc += apiName + '\n'
for i in range(0, len(apiName)):
    rstDoc += "^"
rstDoc += '\n'

# function info
rstDoc += ".. function:: " + apiName + "()\n\n"
rstDoc += TAB_SPACE + apiInfo + "\n\n"

# Functional Requirements
rstDoc += RstTools.addElement(TAB_SPACE, "**Functional Requirements**", descriptions)

# Responses to abnormal situations, including
contents = []
if len(errors) == 0:
    contents.append("If abnormal data is set, the driver should return an error. The generic error codes are described at the :ref:`Generic Error Codes <v4l-dvb-apis:gen-errors>` chapter.")
else:
    contents = errors
rstDoc += RstTools.addElement(TAB_SPACE, "**Responses to abnormal situations, including**", contents)

# Performance Requirements
contents = ["It depends on the system environment, but it usually takes less than 500ms."]
rstDoc += RstTools.addElement(TAB_SPACE, "**Performance Requirements**", contents)

# Constraints
contents = ["Should be supported khronos OpenGL2.1 and EGL1.4."]
rstDoc += RstTools.addElement(TAB_SPACE, "**Constraints**", contents)

# Functions & Parameters
rstDoc += TAB_SPACE + "**Functions & Parameters**\n\n"
rstDoc += TAB_SPACE*2 + ".. code-block:: cpp\n"
rstDoc += TAB_SPACE*2 + "  " + ":linenos:"

# Return Value
rstDoc += TAB_SPACE + "**Return Value**\n\n"

# Example
rstDoc += TAB_SPACE + "**Example**\n\n"


print(rstDoc)