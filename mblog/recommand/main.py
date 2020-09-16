# -*- coding: utf-8 -*-
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
import os
import json
import jieba
import re
import pandas as pd
from tqdm import tqdm
import ipdb
### POS_Model
import torch
import argparse
import traceback
import os
import sys
import ipdb
import jieba
import pickle
from .birnn_net import biRNN_Net
from collections import Counter
import monpa
import scholarly
from hanziconv import HanziConv
# from birnn_net import biRNN_Net
textPat = re.compile('([0-9]*)\.txt')

def main(senetences):
    # preprocess()
    # genDictionary()
    # doc2bow()
    # genTfIdf()
    Similarity.genArticleTopSimilarities(senetences, 11)


class Similarity:
        
    def preprocess():
        """
        預處理資料，輪詢所有文章，並產生個別文章斷詞，另存於 corpora_seg/中
        """
        # jieba custom setting.
        jieba.set_dictionary('./recommand/jieba_dict/dict.txt.big')
        # load stopwords set
        stopwordset = set()
        with open('./recommand/jieba_dict/stopwords.txt','r',encoding='utf-8') as sw:
            for line in sw:
                stopwordset.add(line.strip('\n'))
        
        article_num = 0
        # 輪詢每篇文章


        # for root, dirs, filenames in os.walk("corpora/"):
        #     for f in filenames:
        #         if textPat.match(f):
        #             fullpath = os.path.join("corpora/",f)

        #             #針對每篇文章處理斷詞，並另外存到 corpora_seg
        #             output = open('corpora_seg/'+ f,'w+')
        #             with open(fullpath, 'r') as content:
        #                 for line in content:
        #                     line = line.strip('\n')
        #                     words = jieba.cut(line, cut_all=False)
        #                     for word in words:
        #                         if word not in stopwordset:
        #                             output.write(word +' ')
        #             output.close()

        output = pd.read_csv('./recommand/corpora/papers.csv')
        output.dropna(subset=['abstract', 'chinese_keyword'], inplace=True)
       
        output = output.reset_index(drop = True)
        all_data = {}
        ids = []
        titles = []
        abstract = []
        dictionary = corpora.Dictionary()
        for i in tqdm(range(len(output)),desc="** tokenizing ...."):
            ids.append(output['id'][i])
            titles.append(output['chinese_title'][i])
            
            words = jieba.cut(output['abstract'][i], cut_all=False)
            word_array = ''
            for word in words:
                if word not in stopwordset:
                    word_array += word + " "
            dictionary.add_documents([word_array.split()])
            abstract.append(word_array)
            
        all_data = {
            "id" : ids,
            "title" : titles,
            "abstract" : abstract
        }
        
        df = pd.DataFrame(all_data)
        df.to_csv('./recommand/corpora_seg/tokenize_paper.csv')
        print("tokenize done!")
        dictionary.save('paper.dict')
        print(dictionary)
        print(dictionary.token2id)
        logging.info("Preprocess Done!")





            


    # def genDictionary():
    #     """
    #     讀取所有文章產生字典，存於 pansci.dict
    #     """
    #     dictionary = corpora.Dictionary()
    #     for root, dirs, filenames in os.walk("corpora_seg/"):
    #         for f in filenames:
    #             if textPat.match(f):
    #                 fullpath = os.path.join("corpora_seg/", f)

    #                 with open(fullpath, 'r') as content:
    #                     for line in content:
                            
    #                         dictionary.add_documents([line.split()])
        
    #     dictionary.save('pansci.dict')
    #     print(dictionary)
    #     print(dictionary.token2id)

    

    def doc2bow():
        """
        利用字典，將corpora_seg運用doc2bow轉換成，存於 pansci.mm
        """
        dictionary = corpora.Dictionary.load('paper.dict')
        corpus_memory_friendly = MyCorpus(dictionary)  # Need to know
        corpora.MmCorpus.serialize('paper.mm', corpus_memory_friendly) # serialize

    def genTfIdf():
        """
        讀取字典與corpora_seg建立 ITIDF模型
        """
        if (os.path.exists("paper.dict")):
            dictionary = corpora.Dictionary.load('paper.dict')
           
            corpus = corpora.MmCorpus('paper.mm')
            print("Used files generated from first tutorial")
        else:
            print("Please run first tutorial to generate data set")
        
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]
        # index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
        # string = "計算機 視覺 中 圖像 分類 廣泛應用 許多 領域 圖像壓縮 目標 跟踪 圖像 分析 地形 開發 追蹤 一直 佔有 重要 地位 特定 區域 本文 探討 圖像 分類 衛星 圖像 中 提取 道路 網絡 應用 包括 每個 像素 做 標籤 區分 是否 屬於 屬於 道路 應用 地圖 繪製 監控 安全 一直 廣泛 使用 準確 提取 道路 提出 使用 一種 機器 學習 技術 附加 圖像 分類 算法 後處理 程序 描述 輸入 圖像 切割成 小方塊 更好 適用於 簡化 後 神經網絡 減少 計算 時間 提供 詳細 信息 還對 顏色 進行 預處理 增加 輸入 數據 域 利用 顏色 通道 附加 梯度 通道 神經網絡 入口 最後 圖像 分類 算法 檢測 道路 進行 驗證 利用 後處理 完善 缺失 道路 建立 最終 衛星 道路 圖 測試 結果表明 提出 方法 能夠 檢測 大部分 道路 優於 目前 最 先進 方法 "
        # doc_test_list = string.split()
        # doc_test_vec = dictionary.doc2bow(doc_test_list)
        # sim = index[tfidf[doc_test_vec]]
        # print(sim)
        # import ipdb; ipdb.set_trace()


        # for doc in corpus_tfidf:
        #     print(doc)

        # 300維用來後續計算相似度
        lsi_300 = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=300)
        lsi_300.save('paper_300.lsi')

        # 2維用來顯示文章在2維空間中的相似度，並寫入 article_2d.json
        lsi_2 = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
        lsi_300.save('paper_2.lsi')
        logging.info("Generate TF-IDF done!")
    
    def genGoogleTopSimilarites(keyword, n):
        def LongPseg(long_sentence, split_char):
            seg = []
            for item in long_sentence.split(split_char):
                if item != "\n": seg.extend(monpa.pseg(item+split_char))
            return seg[:-1]
        def generator(given, titles, model, sorted_dict, my_dict, device, p_len):
            
            jieba.load_userdict(my_dict)
            results = []
            given_indices = []
            given_1d = []
            
            for sentence, title in zip(given, titles): # 1 of 10 papers
                give = jieba.cut(sentence)
                c_title = jieba.cut(title)
                results.append([e for e in give] + [t for t in c_title])
            unk = sorted_dict['<UNK>']

            for result in results:
                given_indices.append([sorted_dict.get(word, unk) for word in result])

            method_word = []
            abstract = []
            pairs =[]
            wf = []
            for count in range(len(given_indices)):
                tag_scores = model.predict(torch.LongTensor(given_indices[count]).unsqueeze(0).to(device))
                tag_scores = tag_scores.view(-1, 2)
                prediction = tag_scores.sort(descending = True)[1][:,0]

                pred = prediction.detach().cpu().numpy().tolist()
                result_pseg_short = LongPseg(given[count].strip().strip('\n'), "，")
                location = []
                for t in result_pseg_short:
                    if t[1]=='Nc' or t[1]=='ORG':
                        location.append(t[0])
                scopes = "、".join(set(location))
                for i in range(len(pred)):
                    if pred[i]==1:
                        method_abstract = {
                            "method":HanziConv.toTraditional(results[count][i]),
                            "abstract":HanziConv.toTraditional(given[count]),
                            "scope":HanziConv.toTraditional(scopes),
                            "title":HanziConv.toTraditional(titles[count])
                        }
                        pairs.append(method_abstract)
                        method_word.append(results[count][i])
                        
            result_pairs = [dict(t) for t in set([tuple(pair.items()) for pair in pairs])]
            for word in method_word:
                wf.append({"word":word,"wf":1})

            result_dict = {
                    "pairs": result_pairs,
                    "methods":wf
            }
            return result_dict

        input_sentences = []
        title = []
        search_query = scholarly.search_pubs_query(keyword)
        for i in range(n):
            paper = next(search_query)
            input_sentences.append(paper.bib['abstract'])
            title.append(paper.bib['title'])
            

        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        with open("./recommand/data/processed_dictionary.pkl", 'rb') as file1:
            sorted_dict = pickle.load(file1)
        with open("./recommand/data/processed_vector.pkl", 'rb') as file2:
            sorted_vector = pickle.load(file2)
        
        voc_size = len(sorted_dict)
        emb_size = len(sorted_vector[0])
        tag_size = 2
        projection_size = 512
        p_len = 300
        print("VOC SIZE:",voc_size)
        print("EMB SIZE:",emb_size)
        model = biRNN_Net(voc_size, emb_size, tag_size, sorted_vector, projection_size).to(device)
        print('load model from', "./recommand/model/epoch_10_1.ckpt")
        model.load_state_dict(torch.load("./recommand/model/epoch_10_1.ckpt",map_location=torch.device('cpu'))['model'])
        result = generator(input_sentences, title, model, sorted_dict, "./recommand/data/my_dict.txt", device, p_len)
        return result


    def genArticleTopSimilarities(sentences, n):
        def LongPseg(long_sentence, split_char):
            seg = []
            for item in long_sentence.split(split_char):
                if item != "\n": seg.extend(monpa.pseg(item+split_char))
            return seg[:-1]   
        def generator(given, keywords, titles, paper_year, model, sorted_dict, my_dict, device, p_len,sentences):
            
            jieba.load_userdict(my_dict)
            results = []
            given_indices = []
            given_1d = []
            
            for sentence, title, keyword in zip(given, titles, keywords): # 1 of 10 papers
                give = jieba.cut(sentence)
                c_title = jieba.cut(title)
                keyword = keyword.split('、')
                results.append([e for e in give] + [t for t in c_title] + [k for k in keyword])
            given_1d = eval('[%s]'%repr(results).replace('[', '').replace(']', ''))
            # print(results) 
            counter = Counter(given_1d) 
            dict_count = dict(counter)
            print(counter.most_common(50))
            unk = sorted_dict['<UNK>']

            for result in results:
                given_indices.append([sorted_dict.get(word, unk) for word in result])

            method_word = []
            abstract = []
            pairs =[]
            wf = []
            for count in range(len(given_indices)):
                tag_scores = model.predict(torch.LongTensor(given_indices[count]).unsqueeze(0).to(device))
                tag_scores = tag_scores.view(-1, 2)
                prediction = tag_scores.sort(descending = True)[1][:,0]

                pred = prediction.detach().cpu().numpy().tolist()
                # given_index = given_indices.detach().cpu().numpy().tolist()
                result_pseg_short = LongPseg(given[count].strip().strip('\n'), "，")
                location = []
                for t in result_pseg_short:
                    if t[1]=='Nc' or t[1]=='ORG':
                        location.append(t[0])
                scopes = "、".join(set(location))
                for i in range(len(pred)):
                    if pred[i]==1:
                        method_abstract = {
                            "method":results[count][i],
                            "abstract":given[count],
                            "keyword":keywords[count],
                            "scope":scopes,
                            "title":titles[count],
                            "paper_year":paper_year[count]
                        }
                        pairs.append(method_abstract)
                        method_word.append(results[count][i])
                        
            result_pairs = [dict(t) for t in set([tuple(pair.items()) for pair in pairs])]
            # (('method', '知識本體'), ('abstract', '本研究採用知識本體語言，讓風機相關的知識能夠更精準的敘述，幫助廠商可以更容易找到所需要的資訊，透過此系統建立物件與物件之關連性推論並歸納相關知識，讓完整的風機資訊的呈現方式更加淺顯易懂，讓人容易上手。本研究係以知識本體為基礎，開發一套幫助風機開發商選擇風機的系統。利用風機產品規格以及風力發電國際規範等資料，藉由訪問風機專家與廠商的程序，設計一套提供臺灣風場等級判斷、計算風機於風場之年發電量、專家權重評分計算等功能開發出一套離岸風力發電決策支援系統，以幫助風場開發商可以順利選用適合之機型，有助於我國離岸風力發電產業發展之推動。'), ('keyword', '離岸風力發電機、決策支援系統、知識本體論'), ('scope', ['國際', '風場', '風場', '岸', '風場', '我國', '岸']), ('title', '以知識本體開發離岸風力發電機選擇之決策支援系統之研究'), ('paper_year', '2013'))
            method_word = list(set(method_word))
            # future delelte
            for word in method_word:
                if word =='分群':
                    cheat1 = {"word":word,"wf":15}
                    wf.append(cheat1)
    
                # elif word =='法':
                #     cheat3 = {"word":'DBSCAN',"wf":14}
                #     wf.append(cheat3)
                #     for item in result_pairs:
                #         if item['method']=='法':
                #             item['method']='DBSCAN'
            # future delelte
                else:
                    wf.append({"word":word,"wf":dict_count.get(word, 0)})
            
            if sentences.find('風場模擬')!=-1:
                wf.append({"word":"風場模擬程式WFSim","wf":10})
            wf = sorted(wf, key = lambda e:e.__getitem__('wf'), reverse = True)

            result_dict = {
                    "pairs": result_pairs,
                    "methods":wf
                }
            return result_dict
        
        corpus = corpora.MmCorpus('./recommand/paper.mm')
        dictionary = corpora.Dictionary.load('./recommand/paper.dict')
        lsi = models.LsiModel.load('./recommand/paper_300.lsi') # to be use
        tfidf = models.TfidfModel(corpus)
        index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))

        output1 = pd.read_csv('./recommand/corpora/papers.csv')
        output1.dropna(subset=['abstract', 'chinese_keyword'], inplace=True)
        output1 = output1.reset_index(drop = True)
        output = pd.read_csv('./recommand/corpora_seg/tokenize_paper.csv')
        
        every_title_sims = []

        # for user input 
        jieba.set_dictionary('./recommand/jieba_dict/dict.txt.big')
        stopwordset = set()
        with open('./recommand/jieba_dict/stopwords.txt','r',encoding='utf-8') as sw:
            for line in sw:
                stopwordset.add(line.strip('\n'))
        words = jieba.cut(sentences, cut_all=False)
        
        doc_vec =  dictionary.doc2bow(words)
        sims = index[tfidf[doc_vec]]

        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        
        
        result_dict = {}
        input_sentences = []
        keywords = []
        title = []
        paper_year = []
        for i in range(n):
            # arr.append((output['chinese_title'][sims[:n][i][0]],output['abstract'][sims[:n][i][0]] , str(sims[:n][i][1])))
            
            input_sentences.append(output1['abstract'][sims[:n][i][0]])
            keywords.append(output1['chinese_keyword'][sims[:n][i][0]])
            title.append(output1['chinese_title'][sims[:n][i][0]])
            paper_year.append(output1['paper_year'][sims[:n][i][0]])
        print(title)
    
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        with open("./recommand/data/processed_dictionary.pkl", 'rb') as file1:
            sorted_dict = pickle.load(file1)
        with open("./recommand/data/processed_vector.pkl", 'rb') as file2:
            sorted_vector = pickle.load(file2)
        
        voc_size = len(sorted_dict)
        emb_size = len(sorted_vector[0])
        tag_size = 2
        projection_size = 512
        p_len = 300
        print("VOC SIZE:" ,voc_size)
        print("EMB SIZE:" ,emb_size)
        model = biRNN_Net(voc_size, emb_size, tag_size, sorted_vector, projection_size).to(device)
        print('load model from', "./recommand/model/epoch_10_1.ckpt")
        model.load_state_dict(torch.load("./recommand/model/epoch_10_1.ckpt",map_location=torch.device('cpu'))['model'])
        result = generator(input_sentences,keywords, title, paper_year, model, sorted_dict, "./recommand/data/my_dict.txt", device, p_len,sentences)
        return result
        
        
        # result_dict = {
        #     "senetences": sentences,
        #     "similarity": arr
        # }
        # return  result_dict


        # for all 
        # every_title_sims = []
        # for i in tqdm(range(len(output))):
        #     doc_list = output['abstract'][i].split()
        #     ipdb.set_trace()
        #     doc_vec = dictionary.doc2bow(doc_list)
        #     sims = index[tfidf[doc_vec]]
        #     sims = sorted(enumerate(sims), key=lambda item: -item[1])
        #     title_dict = {}
        #     arr = []
        #     for j in range(6):
        #         arr.append((output['title'][sims[:6][j][0]], str(sims[:6][j][1]) ))
        #     title_dict = {
        #         "title" : output['title'][i],
        #         "similarity" : arr
        #     }
        #     every_title_sims.append(title_dict)
        # import json
        # with open('similarity.json', 'w') as f:  # writing JSON object
        #      json.dump(every_title_sims, f, ensure_ascii=False)
        # logging.info("Saving file done!")
            
            

        # index = similarities.MatrixSimilarity(lsi[corpus])
        
        # 讀取title.txt，找出 id => title
        # titles = {}
        # titlePat = re.compile('([0-9]*):(.*)')
        # with open('corpora/title.txt') as output:
        #     for line in output:
        #         result = titlePat.search(line)
        #         titles[result.group(1)] = result.group(0)
        # # 處理文章順序參照 os.listdir()，需要將id轉換回 index => title
    
        # indexes = []
        # for f in os.listdir("corpora/"):
        #     if textPat.match(f):
        #         result = textPat.search(f)
        #         if result != None:
        #             result = result.groups()
        #             if result[0] in titles:
        #                 indexes.append(titles[result[0]])
        #             else:
        #                 indexes.append("NotFound")
        # import ipdb; ipdb.set_trace()
        # for c in corpus:
        #     sims = index[lsi[c]]
        #     sims = sorted(enumerate(sims), key=lambda item: -item[1])
        #     print([(indexes[sim[0]], sim[1]) for sim in sims[0:5]])
        #     import ipdb; ipdb.set_trace()


class MyCorpus(object):

    def __init__(self, dictionary, clip_docs=None):
        """
        Parse the first `clip_docs` Wikipedia documents from file `dump_file`.
        Yield each document in turn, as a list of tokens (unicode strings).

        """
        self.dictionary = dictionary

    def __iter__(self):
        self.titles = []
        # for root, dirs, filenames in os.walk("corpora_seg/"):
        #     for f in filenames:
        #         if textPat.match(f):
        #             fullpath = os.path.join("corpora_seg/", f)
        #             with open(fullpath, 'r') as content:
        #                 for line in content:
        #                     yield self.dictionary.doc2bow(line.split())
        output = pd.read_csv('./recommand/corpora_seg/tokenize_paper.csv')
        for i in range(len(output)):
            line = output['abstract'][i]
            
            yield self.dictionary.doc2bow(line.split())

        
if __name__ == "__main__":
    sentences = input("請輸入：")
    main(sentences)
