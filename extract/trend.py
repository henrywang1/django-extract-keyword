from collections import Counter
from collections import defaultdict
import pytrends
from pytrends.request import TrendReq
pytrends = TrendReq(hl='zh-tw', tz=360)

def getTopKRelated(keyword, k=4):
    print('keyword={0}'.format(keyword))
    pytrends.build_payload([keyword], cat=0, timeframe='today 1-m', geo='', gprop='')
    ret = list(pytrends.related_topics().values())[0]
    return set(ret.title[0:k].values) if ret is not None else None

def extend_result(item_list, dict_suggest, dict_relate):
    all_relate = [list(dict_relate[key]) for key in item_list if dict_relate[key]]
    all_relate = [ll for l in all_relate for ll in l if len(ll)>1]
    all_relate = Counter(all_relate).most_common()
    all_relate = [item[0] for item in all_relate if item[0] not in item_list]
    return (item_list+all_relate)[:5]

def word_related(the_list):
    ret = [] #這個只是拿來看兩兩關係
    dict_suggest = {}
    dict_relate = {}
    for i in the_list:
        suggestions = []
        topRelated = dict_relate.get(i)
        if topRelated is None: 
            topRelated = dict_relate[i] = getTopKRelated(i, 3)

        suggestions = dict_suggest.get(i)
        if suggestions is None: 
            suggestions = dict_suggest[i] = set([s['title'] for s in pytrends.suggestions(i)][:3])       
        suggestions_or_related = suggestions | topRelated if topRelated else suggestions
        ret.append((i, suggestions_or_related))

    group = []
    dict_word = {} 
    for i, item in enumerate(ret):
        if item[0] in dict_word: #有組了
            continue

        candidate = []
        related_words = []
        found = False
        for successor in ret[i+1:]:
            #找後面的 intersction 看有沒有有組的
            intersection = (item[1].intersection(successor[1]))
            if intersection:
                if successor[0] in dict_word: #.get(successor[0]) is not None: #這個對象有組別了 就跟他一組
                    idx = dict_word.get(successor[0])
                    group[idx].append(item[0])
                    related_words[idx].append(intersection)
                    dict_word[item[0]] = idx
                    found=True
                    break
                else:
                    candidate.append(successor[0])
        if not found:
            candidate = [item[0]] + candidate
            group.append(candidate)
            related_words.append(item[1])
            for c in candidate:
                dict_word[c] = (len(group)-1)
    
    
    v = defaultdict(list)
    for key, value in sorted(dict_word.items()):
        v[value].append(key)
    result = list(v.values())
    result = [extend_result(r, dict_suggest, dict_relate) for r in result]
    result_list = []
    for r in result:
        if len(r)<2:
            continue
        pytrends.build_payload(r, cat=0, timeframe='today 1-m')
        interest_over_time_df = pytrends.interest_over_time()
        interest_over_time_df = interest_over_time_df.mean()[:-1].sort_values(ascending=False)
        interest_over_time_df = interest_over_time_df.map(lambda x: '%2.1f' % x)
        result_list.append(interest_over_time_df.to_dict())
    return result_list
