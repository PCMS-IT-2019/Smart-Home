#input json directly from baidu-api response
def get_action(response):
    act = {
        'target': '',
        'action': '',
        'para': None
    }

    #if len(response['items'])

    for i in response["items"]:
        # 检测普通动宾句式（例如：打开灯）
        if (i['deprel'] == 'VOB'):
            act['target'] = i['word']
            act['action'] = response["items"][i['head'] - 1]['word']

        # 检测把字句式（例如：把灯打开）
        if (i['postag'] == 'p' and i['deprel'] == 'BA'):
            act['action'] = response['items'][i['head'] - 1]['word']
            for j in response['items']:
                if (j['head'] == i['id']): act['target'] = j['word']

        # 检测句子中的参数（例如：把空调调至20度）
        for k in response['items']:
            if (k['head'] == i['id'] and k['deprel'] == 'CMP'):
                for l in response['items']:
                    if (l['head'] == k['id']): act['para'] = l['word']

    if (act['target'] == '' or act['action'] == ''):
        last = response['items'][len(response['items'])-1]
        if(last['postag']) == 'v':
            act['action'] = last['word'][0]
            act['target'] = last['word'][1:]

    return act

if __name__ == "__main__":
    exit (get_action())





