# -*- coding: utf-8 -*-
import os, sys,xlrd,codecs, math

pp=os.getcwd()
yao_ming_list=[]
yao_xing_list=[]
yao_dict = {}			# 药名-出现次数(即权重)字典 {'麻黄':4 ，‘桂枝’：22， }
relationships = {}	# 关系字典 {  '麻黄'： { '桂枝'：2，‘生甘草’：3} ,    }
lineYaos = []		# 每段内药物关系       


da_ta = xlrd.open_workbook('%s\\yao_ming_xing_wei.xlsx'% (pp))
table_ling = da_ta.sheets()[0]
hangshu_ling = table_ling.nrows

for i in range(0,hangshu_ling):
        print(i)
        row_ling_data=table_ling.row_values(i)
        yao_ming=table_ling.cell_value(i,0)
        yao_xing=table_ling.cell_value(i,2)
        yao_ming_list.append(yao_ming)
        yao_xing_list.append(yao_xing)


#print(yao_ming_list,yao_xing_list)

with codecs.open("%s\\chu_fang.txt"% (pp), "r", "utf8") as f:
	for line in f.readlines():
                #print(line)
                
                
                wo_rds = line.split( )
                lineYaos.append([])
                for wo_rd in wo_rds:
                        if wo_rd in yao_ming_list:
                                lineYaos[-1].append(wo_rd)
                                if yao_dict.get(wo_rd) is None:
                                        yao_dict[wo_rd] = 0
                                        relationships[wo_rd]  = {} 
                                yao_dict[wo_rd] +=1
                                #print(wo_rd)


#print(yao_dict,lineYaos)

for line in lineYaos:
        for yao0 in line:
                for yao1 in line:
                        if yao0 == yao1:
                                continue
                        if relationships[yao0].get(yao1) is None:
                                relationships[yao0][yao1]=1
                        else:
                                relationships[yao0][yao1] = relationships[yao0][yao1] + 1


#print(relationships)


with codecs.open("%s\\node.txt"% (pp), "w", "gbk") as f:
        f.write("Id Label Weight Yaoxing\r\n")
        for yao_er, yao_er_cishu in yao_dict.items():
                xuhao_yaoming=yao_ming_list.index(yao_er)
                yaoxing_node=yao_xing_list[xuhao_yaoming]
                f.write(yao_er + " " + yao_er + " "+ str(yao_er_cishu) + " " + yaoxing_node + "\r\n")


with codecs.open("%s\\edge.txt"% (pp), "w", "gbk") as f:
        f.write("Source Target Weight\r\n")
        for zhu_yao, edges in relationships.items():
                for fu_yao, pin_ci in edges.items():
                        if pin_ci > 0:
                                f.write(zhu_yao + " " + fu_yao + " " + str(pin_ci) + "\r\n")

os.rename("%s\\node.txt"% (pp),"%s\\node.csv"% (pp))
os.rename("%s\\edge.txt"% (pp),"%s\\edge.csv"% (pp))
