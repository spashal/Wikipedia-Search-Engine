import re

fields = ['infobox', 'category', 'links', 'references', 'body']

def field_segregator(text):
    arr = {}
    temp = ''
    for j in range(5):
        arr[fields[j]] = []
        beginning = 0
        if j == 0:
            for st in re.finditer('\{\{Infobox', text):
                temp += text[beginning:st.start()]
                ctr = 0
                end = -1
                for i in range(st.start()+10, len(text)):
                    if text[i] == '}' and ctr == -1:
                        end = i-1
                        beginning = end+2
                        break
                    elif text[i] == '}':
                        ctr -= 1
                    elif text[i] == '{':
                        ctr += 1
                end = min(end, len(text))
                tokens = re.split(r'[^A-Za-z0-9]+', text[st.start()+10:end])
                arr[fields[j]] = tokens
            temp += text[beginning:]
    
        elif j == 1:
            temp = ''
            length = len("[[category:")
            beginning = 0
            for st in re.finditer("\[\[Category:.*\]\]", text):
                arr[fields[j]] = re.split(r'[^A-Za-z0-9]+', st[0][length:-2])
                temp += (text[beginning:st.start()])
                beginning = st.end()
            temp += text[beginning:]
        elif j == 2:
            temp = ''
            beginning = 0
            # assuming that {{reflist}} is not supposed to be a part of references
            for st in re.finditer('==\s*External links\s*==', text):
                end = 0
                for tt in re.finditer('\{\{', text[st.start()+10:]):
                    end = tt.start()
                    break
                temp += (text[beginning:st.start()])
                arr[fields[j]] = re.split(r'[^A-Za-z0-9]+', text[st.start()+14:end-2])
                beginning = end
            temp += text[beginning:]
        elif j == 3:
            temp = ''
            beginning = 0
            # bibliography needs to end with == or [[
            for st in re.finditer('==\s*Bibliograpy\s*==', text):
                end = 0
                for tt in re.finditer('(\{\{)|(==)', text[st.start()+25:]):
                    end = tt.start()
                    break
                temp += (text[beginning:st.start()])
                arr[fields[j]] = re.split(r'[^A-Za-z0-9]+', text[st.start()+20:end-2])

                beginning = end
            temp += text[beginning:]
            text = temp
            temp = ''
            beginning = 0
            # references need to end with {{
            for st in re.finditer('==\s*Rerences\s*==', text):
                end = 0
                for tt in re.finditer('\{\{', text[st.start()+20:]):
                    end = tt.start()
                    break
                temp += (text[beginning:st.start()])
                arr[fields[j]] += re.split(r'[^A-Za-z0-9]+', text[st.start()+20:end-2])
                beginning = end
            temp += text[beginning:]
            text = temp
            temp = ''
            beginning = 0
            for st in re.finditer('==\s*Notes\s*==', text):
                end = 0
                for tt in re.finditer('(\{\{)|(==)', text[st.start()+10:]):
                    end = tt.start()
                    break
                temp += (text[beginning:st.start()])
                arr[fields[j]] += re.split(r'[^A-Za-z0-9]+', text[st.start()+10:end-2])
                beginning = end
            temp += text[beginning:]

        else:
            arr[fields[j]] += re.split(r'[^A-Za-z0-9]+', text)


        text = temp

    return arr

