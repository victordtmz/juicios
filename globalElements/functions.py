def create_regEx(regEx):
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