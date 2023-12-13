from load_models_langidentify_multi import language_identify 
import glob, sys, codecs


files = glob.glob(sys.argv[1]+'/*.txt')


for _file in files:
    if '_' not in _file.split('/')[-1]:
        print (_file)
        langs = []
        inp = []
        _inp = []
        data = []
        count = 1
        _lang = []
        for line in codecs.open(_file):
            line=line.strip()
            inp.append(line)
            if len(line.split())>20:
                _inp.append(" ".join(line.split()[:20]))
            else:
                _inp.append(line)
            count = count + 1
            if count % 30 == 0:
                t_lang = language_identify(_inp)
                for u in t_lang:
                    _lang.append(u)
                _inp = []

        if _inp!=[]:
            t_lang = language_identify(_inp)
            for u in t_lang:
                _lang.append(u)

        for i,j in zip(inp, _lang):
            #print (i,j['langPrediction'][0]['langCode'])
            _langc = j
            langs.append(_langc)
            print(str(_langc)+'\t'+i)
            data.append(str(_langc)+'\t'+i)

        olang = max(langs,key=langs.count)
        _name = _file.split('/')[-1]
        ofile = olang+'_'+_name
        pofile = _file.replace(_name, ofile)
        pout = open(pofile,'w')
        for i in data:
            pout.write(i+'\n')
        pout.close()
        print (pofile)

