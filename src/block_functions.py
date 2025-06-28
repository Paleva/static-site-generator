
def markdown_to_blocks(markdown: str):
    strings = markdown.split('\n')
    paragraphs = []
    temp = ''
    for idx in range(len(strings)):
        if len(strings[idx]) == 0 and idx == 0:
            continue
        if len(strings[idx]) == 0:
            paragraphs.append(temp)
            temp = ''
        else:
            if strings[idx+1] == '':
                temp += strings[idx]
            else:
                temp += strings[idx] + '\n'
    
    
    return [paragraph for paragraph in paragraphs if len(paragraph)!=0]