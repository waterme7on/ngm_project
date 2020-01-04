# -*- coding: utf-8 -*-

import jieba
import csv
import networkx as nx
import jieba.posseg as jp
import json
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['Source Han Sans TW', 'sans-serif']

def read_file(file_name, output_file):
    '''
    数据预处理：结巴分词、提取人名机构、建立社交网络图
    '''
    entity_relation = {}
    extract_type = ['nr',  'nrfg',  'nrt']
    extract_attri = ['title', 'text']
    '''
        'nr': '人名',
        'nrfg': '人名',
        'nrt': '外国人名',
        'ns': '地名',
        'nt': '机构团体',
        'nz': '其他专名',
    '''
    with open(file_name, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            extract_attri = [row.index(attri) for attri in extract_attri]
            break
        for i,row in enumerate(reader):
            tmp_entity = set()
            # 提取实体：对文章和标题进行分词
            for attri in extract_attri:
                cut_result = jp.cut(row[attri])
                # 提取文章和标题中出现的实体
                for word, flag in cut_result:
                    if flag in extract_type:
                        tmp_entity.add(word)

            # # 统计热门人名和机构
            # for entity in tmp_entity:
            #     try:
            #         entity_relation[entity] += len(tmp_entity)-1
            #     except:
            #         entity_relation[entity] = len(tmp_entity)-1

            # 统计联系
            for entity in tmp_entity:
                for other in tmp_entity:
                    # other等于自己，则相当于统计文章数
                    try:
                        entity_relation[entity][other] += 1
                    except:
                        try:
                            entity_relation[entity][other] = 1
                        except:
                            entity_relation[entity] = {}
                            entity_relation[entity][other] = 1
            if i % 1000 == 0:
              print(i)
              break

    print(entity_relation)
    # 保存数据
    json_str = json.dumps(entity_relation, ensure_ascii=False, indent=2)
    with open(output_file, 'w') as json_file:
        json_file.write(json_str)

def closest_neighbour(er, k):
    '''
    图的验证：输出前k个联系最紧密的邻居
    '''
    input_str=''
    while(True):
        input_str = input('输入结点名称（输入quit退出）: ')
        if input_str == 'quit':
            break
        try:
            # 检索邻居并排序
            tmp = er[input_str]
            tmp = sorted(tmp.items(), key=lambda item: item[1], reverse=True)
            # 输出关系最强的k个邻居
            cnt = 0
            for elem in tmp:
                if elem[0] == input_str:
                    continue
                print(elem)
                cnt += 1
                if cnt == 10:
                    break
        except Exception as e:
            print("Error:", e)

def read_json(json_file_name):
    '''
    读取json文件并转换为dict
    '''
    with open(json_file_name, 'r') as f:
        dict_data = json.load(f)
        return dict_data

def create_graph(er):
    '''
    生成图
    '''
    G = nx.Graph()
    # G.add_nodes_from(er.keys())
    for entity in er.keys():
        for relation in er[entity]:
            if entity == relation:
                continue
            G.add_edge(entity, relation, weight=er[entity][relation])
    # nx.draw(G, with_labels=False,node_color='red')
    # pos = nx.random_layout(G)
    # nx.draw(G, pos=nx.random_layout(G), node_color='b')
    # nx.draw(G,pos = pos,node_color = 'b',edge_color='r',with_labels = True，font_size =18,node_size =20)
    # plt.figure(figsize=(50, 50))
    # plt.show()
    # plt.savefig("graph.png")
    return G

def graph_stat(G):
    '''
    图的统计：结点数、边数、连通分支数、极大连通分支
    '''
    print('结点数：', len(G.nodes))
    print('边数：', len(G.edges))
    cc = list(nx.connected_components(G))
    cc = sorted(cc, key=lambda elem:len(elem), reverse=True)
    print('连通分支数：', len(cc)) 
    print('极大连通分支：', len(cc[0]))


##########################################
#
# 数据处理：导出为json
# file_name = "ruc_news.txt"
# output_file = "er.json"
# read_file(file_name, output_file)
# print("read data finished.")

# json_file = "hotspot.json"
# d = read_json(json_file)
# d = sorted(d.items(), key=lambda item:item[1], reverse=True)
# print('热门人物')
# for k in range(50):
#     print(d[k])
# # print(d[:50])

print('start')
# 生成图数据
json_file_name = "er.json"
er = read_json(json_file_name)
G = create_graph(er)
print("create graph.")


# # 图的验证
# print("图的验证")
# closest_neighbour(er, 10)

# 图的统计
# print("graph stat.")
# graph_stat(G)

# # 任务一：Pagerank算法得出排名前20的结点
# page_rank=nx.pagerank(G,alpha=0.85)
# page_rank = sorted(page_rank.items(), key=lambda item:item[1], reverse=True)
# print('task 1:Pagerank')
# print(page_rank[:100])


# # 任务三：节点的聚集系数计算
# clustering_factor = nx.clustering(G)
# clustering_factor = sorted(clustering_factor.items(), key=lambda item:item[1], reverse=True)
# print('task 3:聚集系数')
# print(clustering_factor[:100])


# 任务二：结点中心性计算
betweenness = nx.betweenness_centrality(G)
betweenness = sorted(betweenness.items(), key=lambda item:item[1], reverse=True)
print('task 2:中心性')
print(betweenness[:100])
