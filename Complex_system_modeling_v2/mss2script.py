import numpy as np
import pandas as pd
import copy
from openpyxl import load_workbook
'''
print("Enter file name: ")
name=input()
print("Enter name of sheet with basic probabilities: ")
sht=input()
print("enter quantity of parameters")
quantity_of_parametres=int(input())
'''

alts_2_sheet="Sheet4"# лист в основній таблиці де зберігаються альтернативи другого етапу
quant_alts2=5 # кількість альтернатив на другому етапі
quantity_of_parametres=6 #кількість альтернатив на першому етапі
quantity_of_alternatives=[2,5,2,5,7,4]# кількість альтернатив по кожному фактору в основній таблиці(к-ть рядків)
output_file="output1.xlsx"
# ЗЧИТАТИ ТАБЛИЦЮ ПОЧАТКОВИХ ЙМОВІРНОСТЕЙ
path_1=["Форін МСС 2.xlsx", "Sheet1"] # Основна таблиця
path_temp=["Book1.xlsx","Sheet1","Sheet2"] # Перехресна таблиця з Book1

#########################################
#########################################
#########################################
######################################### Далі все автоматизовано має бути
#########################################
#########################################
alts_w_prob=[]
parameters_alts=[]
for i in range(quantity_of_parametres):
    temp_df=pd.read_excel(
        path_1[0],
        sheet_name=path_1[1],
        usecols=chr(ord("A")+2*i)+":"+chr(ord("B")+2*i),
        skiprows=1,
        nrows=quantity_of_alternatives[i],
        header=None
    )
    alts_w_prob.append(pd.Series(data=temp_df.iloc[:,1].values,index=temp_df.iloc[:,0].values))
for i in range(len(alts_w_prob)):
    temp=[]
    for j in range(len(alts_w_prob[i].index)):
        temp.append(alts_w_prob[i].index[j])
    parameters_alts.append(copy.deepcopy(temp))

temp_df=pd.read_excel(
    path_1[0],
    sheet_name=path_1[1],
    usecols="A:"+chr(ord("A")+(2*quantity_of_parametres-1)),
    nrows=1,
    header=None,
    na_filter=False
)
parameters=[]
for i in range(quantity_of_parametres):
    parameters.append(temp_df.at[0,2*i])
conf_table_power=1
for i in parameters_alts:
    conf_table_power=conf_table_power*len(i)
print(conf_table_power)
print(parameters)
print(parameters_alts)

# конструювання першої таблиці
temp_cols=[]
cluster_size=conf_table_power
prev_cluster_size=cluster_size
for i in range(len(parameters_alts)):
    temp=[]
    prev_cluster_size=cluster_size
    cluster_size=cluster_size/len(parameters_alts[i])
    for l in range(int(conf_table_power/prev_cluster_size)):
        for j in range(int(prev_cluster_size/cluster_size)):
            for k in range(int(cluster_size)):
                temp.append(parameters_alts[i][j])
    temp_cols.append(copy.deepcopy(temp))

#construct dict to create conf_table
dict={}
for i in range(len(parameters)):
    dict.update({parameters[i]:temp_cols[i]})
# додання колонок результатів
dict.update({"P":np.zeros(conf_table_power)})
dict.update({"C":np.zeros(conf_table_power)})
dict.update({"P*C":np.zeros(conf_table_power)})
dict.update({"Нормоване P*C":np.zeros(conf_table_power)})
conf_table=pd.DataFrame(dict)


'''
test=pd.read_excel("output.xlsx", sheet_name="Sheet1")
print(test)
for i in range(len(test)):
    if test.at[i,"Тип ураження"]=="Укус тварин/комах":
        test.at[i,"Тип ураження"]="Укуси тварин/комах"


for i in range(len(conf_table)):
    for j in conf_table.columns:
        if conf_table.at[i,j]!=test.at[i,j]:
            print(i,j)

conf_table.to_excel(output_file,index=False)
print(conf_table.at[112,"Тип ураження"])
print(test.at[112,"Тип ураження"])
'''
# Витягнути таблицю зв'язків
bounds=pd.read_excel(path_temp[0], sheet_name=path_temp[1],index_col=0)

# Прорахунок P
for i in range(len(conf_table)):
    temp_p=1
    for col in range(len(parameters)):
        temp_p=temp_p*alts_w_prob[col][conf_table.at[i,conf_table.columns[col]]]
    conf_table.at[i,"P"]=temp_p
#print(alts_w_prob[0]["Так"])

#  Прорахунок C
for row in range(len(conf_table)):
    temp_c=1
    for i in range(len(parameters)-1):
        for j in range(i+1,len(parameters)):
            temp_c=temp_c*(1+bounds.at[conf_table.at[row,conf_table.columns[j]],conf_table.at[row,conf_table.columns[i]]])
    conf_table.at[row,"C"]=temp_c
#Прорахунок P*C
for i in range(len(conf_table)):
    conf_table.at[i,"P*C"]=conf_table.at[i,"P"]*conf_table.at[i,"C"]
# Підрахунок норми та нормування
norm=0
for i in range(len(conf_table)):
    norm=norm+conf_table.at[i,"P*C"]
for i in range(len(conf_table)):
    conf_table.at[i,"Нормоване P*C"]=conf_table.at[i,"P*C"]/norm
# Вивід
conf_table.to_excel(output_file, index=False)




#Обнулення базових ймовірностей
for i in range(len(alts_w_prob)):
    for key in alts_w_prob[i].index:
        alts_w_prob[i][key]=0


#Перерахунок ймовірностей з урахуванням взаємозв'язків

for i in range(len(conf_table)):
    for par in range(len(alts_w_prob)):
        for key in alts_w_prob[par].index:
            if conf_table.at[i,conf_table.columns[par]]==key:
                alts_w_prob[par][key]=alts_w_prob[par][key]+conf_table.at[i,"Нормоване P*C"]


wb=load_workbook(output_file)
if "Sheet2" not in wb.sheetnames:
    wb.create_sheet("Sheet2")
ws=wb["Sheet2"]

start_row=2

for start_col in range(len(alts_w_prob)):
    for i, (index, value) in enumerate(alts_w_prob[start_col].items()):
        ws.cell(row=start_row+i, column=2*start_col+1, value=index)
        ws.cell(row=start_row+i, column=2*start_col+2,value=value)
wb.save(output_file)

temp_df=pd.read_excel(
    path_1[0],
    sheet_name=alts_2_sheet,
    nrows=quant_alts2,
    header=None
)


# Створення другої таблиці конфігурації
alts_2=[]
for i in range(len(temp_df)):
    alts_2.append(temp_df.at[i,0])

dict={}
for i in range(len(alts_2)):
    dict.update({alts_2[i]:np.ones(len(conf_table))})
conf_table_2R=pd.DataFrame(dict)
temp_df=pd.read_excel(path_1[0], sheet_name=path_1[1], nrows=1, header=None)
# Допоміжна таблиця конфігурацій першого етапу
dict1={}
for i in range(len(quantity_of_alternatives)):
    dict1.update({temp_df.at[0,2*i]:conf_table[conf_table.columns[i]].to_list()})
configurs=pd.DataFrame(dict1)

# Таблиця взаємозв'язків ситуація-рішення
bounds_2=pd.read_excel(path_temp[0], sheet_name=path_temp[2], index_col=0)
# Обрахунок ймовірності зв'язку
for i in range(len(conf_table_2R)):
    for col in conf_table_2R.columns:
        for conf in configurs.columns:
            conf_table_2R.at[i,col]=conf_table_2R.at[i,col]*(1+bounds_2.at[configurs.at[i,conf],col])
with pd.ExcelWriter(output_file, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    conf_table_2R.to_excel(writer, sheet_name="Sheet3", index=False)
# Нормування
sums_to_norm=[]
for i, row in conf_table_2R.iterrows():
    sums_to_norm.append(row.sum())
sums_to_norm=np.array(sums_to_norm)


for i in range(len(conf_table_2R)):
    for col in conf_table_2R.columns:
        conf_table_2R.at[i,col]=conf_table_2R.at[i,col]/sums_to_norm[i]
# сумарна ймовірність успіху при прийняті рішень у кожній ситуації має бути 1

with pd.ExcelWriter(output_file, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
    conf_table_2R.to_excel(writer, sheet_name="Sheet3", index=False, startrow=0, startcol=6)
# Домноження на Нормоване P*C
for i in range(len(conf_table)):
    for col in conf_table_2R.columns:
        conf_table_2R.at[i,col]=conf_table_2R.at[i,col]*conf_table.at[i,"Нормоване P*C"]

with pd.ExcelWriter(output_file, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
    conf_table_2R.to_excel(writer, sheet_name="Sheet3", index=False, startrow=0, startcol=12)


# Підрахунок ефективності рішень
temp_sol=[]
temp_success=[]
for col in conf_table_2R.columns:
    temp_sol.append(col)
    temp_success.append(conf_table_2R[col].sum())
dict3={
    "Рішення":temp_sol,
    "Успіх": temp_success
}
result_df=pd.DataFrame(dict3)
with pd.ExcelWriter(output_file, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
    result_df.to_excel(writer, sheet_name="Sheet4", index=False)