import winsound
import re
def create_regEx(regEx: str) ->str:
    if regEx:
        regEx = regEx.lower()
        regEx_updated = ''
        for i in regEx:
            match i:
                case 'a':
                    i = '[aá]'
                case 'á':
                    i = '[aá]'
                case 'e':
                    i = '[eé]'
                case 'é':
                    i = '[eé]'
                case 'i':
                    i = '[ií]'
                case 'í':
                    i = '[ií]'
                case 'o':
                    i = '[oó]'
                case 'ó':
                    i = '[oó]'
                case 'u':
                    i = '[uú]'
                case 'ú':
                    i = '[uú]'
            regEx_updated = regEx_updated+i
        return(regEx_updated)

def formatPhoneNo(currentNo:str)->str:
    if currentNo:
        currentNo = re.findall(r"\d+",currentNo)[0] 
        try:
            if len(currentNo) > 10:
                formatNo = formatNo[0:10]
                winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
            else: formatNo = currentNo
            match len(formatNo):
                case 10:
                    PhoneNo = '(%s) %s-%s' % tuple(re.findall(r'\d{4}$|\d{3}',str(formatNo)))
                case 9:
                    PhoneNo = '(%s) %s-%s' % tuple(re.findall(r'\d{3}',str(formatNo)))
                case 8:
                    PhoneNo = '(%s) %s-%s' % tuple(re.findall(r'\d{3}|\d{2}',str(formatNo)))
                case 7:
                    PhoneNo = '(%s) %s-%s' % tuple(re.findall(r'\d{3}|\d',str(formatNo)))
                case 6:
                    PhoneNo = '(%s) %s' % tuple(re.findall(r'\d{3}',str(formatNo)))
                case 5:
                    PhoneNo = '(%s) %s' % tuple(re.findall(r'\d{3}|\d{2}',str(formatNo)))
                case 4:
                    PhoneNo = '(%s) %s' % tuple(re.findall(r'\d{3}|\d',str(formatNo)))
            return PhoneNo
        except:
            return currentNo