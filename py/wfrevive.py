# -*- coding: utf-8 -*-
"""wfrevive.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z3xETs-l-TbBvINIcVAe-BUNTTtlu0hE

# WFのアイコンが震えない問題の解消対応用手順書兼クエリ発行スクリプト
各セルの左上の▶アイコンをクリック
テキストエリアはダブルクリックで編集モードになります（Markdown記法・Texが使えます）

### 要改修項目：
- なし

### FB・改修リクエスト:
- （随時追記してください）

### 改修履歴：
- (11/17) datasourceの全タイプに対応

### 補足
prep_datasourceが存在しないときは、画面上でデータソースを開いてレコードの存在を確認すると、prep_datasourceが作成されることがある。
WFのバージョンが1個しかない場合はこれを実行してprep_datasource_XXXX_wfverを作る。
"""

account=0
wf_v=-1
wf_id=-1

print("---手順１：ID入力--------")

while(1):
    try:
        account=int(input("\taccount_id:"))
        break
    except ValueError as e:
        pass

while(1):
    try:
        wf_v=int(input("\tworkflow_version_id:"))
        break
    except ValueError as e:
        pass
    finally:
        if wf_v ==-1:
            break
if wf_v == -1:
    while(1):
        try:
            wf_id=int(input("\tworkflow_id:"))
            break
        except ValueError as e:
            pass
        finally:
            if wf_id ==-1:
                break

if wf_v==-1 and wf_id==-1:
    print("workflow_versionを調べてください")
    exit()
elif wf_v==-1 and wf_id>0:
    print("↓のクエリでWFバージョンIDを確認")
    print("use prd_preparation_{};".format(account))
    print("SELECT * FROM workflow_versions WHERE workflow_id={};".format(wf_id))
    while(1):
        try:
            wf_v=int(input("workflow_version_id:"))
            break
        except ValueError as e:
            pass
        finally:
            if wf_v > 0:
                break
else:
    print("↓のクエリで対象のWFバージョンのステータスを確認")
    print("use prd_preparation_{};".format(account))
    print("SELECT * FROM workflow_versions WHERE id={};".format(wf_v))
# input("press enter to next.")
print('Go to next code cell.')
# print(account,wf_v)

"""### テスト用
クエリ結果サンプル：
| 13401 | "prep_datasource_file_429_39"  | 
| 13402 | "prep_datasource_file_429_155" | 
| 13403 | "prep_datasource_file_429_243" | 
| 13404 | "prep_datasource_file_429_16"  |
| 13405 | "prep_datasource_file_429_159" |
| 13424 | "prep_datasource_file_429_34"  | 
| 13434 | "prep_datasource_file_429_243" | 
| 13440 | "prep_datasource_file_429_243" | 
| 13452 | "prep_datasource_file_429_16"  | 
| 13474 | "prep_datasource_file_429_262" | 
| 13475 | "prep_datasource_file_429_262" | 
| 13487 | "prep_datasource_file_429_16"  | 
| 13497 | "prep_datasource_file_429_16"  | 
| 13508 | "prep_datasource_act_429_40"  |
"""

print("\n---手順２：mysqlでタスクテーブルが参照するデータソースを調べる---")
print("2-1:ジョブを確認")
print("SELECT * FROM jobs WHERE workflow_version_id={};\n".format(wf_v))
#_= input("press enter to next.")
print("\n2-2:タスクを確認")
print("SELECT * FROM tasks WHERE job_id IN (SELECT id FROM jobs WHERE workflow_version_id={}) AND task_type='sampling_table';\n".format(wf_v))
#_=input("press enter to next.")
print("\n2-3:prep_taskとprep_datasource_XXXXの関係を確認")
print('SELECT id, table_schema->"$.table_name" AS table_name FROM tasks WHERE job_id IN (SELECT id FROM jobs WHERE workflow_version_id={} and task_type="sampling_table");\n'.format(wf_v))
#_=input("press enter to next.")

task_dsf = {}
ds_ids = []
ds_types = {}
print("クエリ結果を貼り付け(ヘッダ行は省略)")
tmp_line = input().replace(' ','').replace('|','').split('"')
print(tmp_line)

i=0
while i<len(tmp_line)-1:
    task_dsf[int(tmp_line[i])]=tmp_line[i+1]
    tmp_dsid = int(tmp_line[i+1].split('_')[4])
    ds_type = tmp_line[i+1].split('_')[2]
    
    if tmp_dsid not in ds_ids:
      ds_ids.append(tmp_dsid)
      ds_types[tmp_dsid] = ds_type
    i+=2
ds_ids.sort()
print('taskテーブルの個数：',len(task_dsf),'個')
print(task_dsf)
print(ds_ids)
print(ds_types)
# input("press enter to next.")
print('Go to next code cell.')

print("\n-------------ここからポスグレ---------------")
# PGPASSWORD=y7LyE7Plad7BeBW7 psql -h prd-preparation-data02.aurora.rds.bdash.inside -U bdash-admin prd_preparation_preview_;
print("---手順３：psqlでprep_datasource_xxの存在を確認---")
print("テーブルの有無を確認する。")
print("なければ直前のWFバージョンのprep_datasource_fileから作成する")
for ds_id in ds_ids:
    print("SELECT COUNT(*) FROM prep_datasource_{};".format(ds_id))
print("prep_datasourceテーブルがなければ作成する")
while(1):
    print("他のWFバージョンのprep_datasource_XXXXを探す -1を入力して抜ける")
    mk_ds_id = 0
    try:
        mk_ds_id = int(input("データソースID:"))
        if mk_ds_id in ds_ids:
            '''
            query = "SELECT CAST(REPLACE(REPLACE(relname,'prep_datasource_{}_',''),'_{}','') AS INTEGER) AS wf_ver, ".format(mk_ds_id)+\
                    "relname AS table_name FROM pg_stat_user_tables " +\
                    " WHERE relname LIKE 'prep_datasource_file_%' AND relname LIKE '%_{}'".format(mk_ds_id) +\
                    " ORDER BY wf_ver DESC;"'''
            #query = "SELECT relname AS table_name FROM pg_stat_user_tables WHERE relname LIKE 'prep_datasource_file_%' AND relname LIKE '%_{}';".format(mk_ds_id)
            query = "SELECT MAX(wf_ver) FROM (SELECT CAST(REPLACE(REPLACE(relname,'prep_datasource_{0}_',''),'_{1}','') AS INTEGER) AS wf_ver\n \
                     FROM pg_stat_user_tables WHERE relname LIKE 'prep_datasource_{0}_%' AND relname LIKE '%\_{1}') AS dsfs;".format(ds_types[mk_ds_id],mk_ds_id)
            print(query)
            print("作成元のWFバージョンを確認してテーブルを作成する")
            prev_wf = input('previous wf ver. id:')
            print("CREATE TABLE prep_datasource_{0} (LIKE prep_datasource_{1}_{2}_{0});".format(mk_ds_id, ds_types[mk_ds_id], prev_wf))
            print("トランザクション開始")
            print("SELECT COUNT(*) FROM prep_datasource_{};".format(mk_ds_id))
            print("INSERT INTO prep_datasource_{0} SELECT * FROM prep_datasource_{1}_{2}_{0};".format(mk_ds_id, ds_types[mk_ds_id], prev_wf))
            print("レコード数を確認してコミット")
            input("press enter to next.")
    except ValueError as e:
        print('error: '+e)
    finally:
        if mk_ds_id < 0:
            break
print('Go to next code cell.')

print("\n---手順４：prep_datasource_XXXX_xx_xxの確認と作成---")
print("prep_datasource_XXXX_xx_xxを作成する")
for ds_id in ds_ids:
    print("CREATE TABLE IF NOT EXISTS prep_datasource_{0}_{1}_{2} (LIKE prep_datasource_{2});".format(ds_types[ds_id], wf_v, ds_id))
input("press enter to next.")

print("prep_datasource_XXXXにレコードを挿入する")
print("トランザクション開始")
input("press enter to next.")
print("各テーブルのレコード数の確認")
for ds_id in ds_ids:
    print("SELECT COUNT(*) FROM prep_datasource_{0}_{1}_{2};".format(ds_types[ds_id],wf_v,ds_id))
input("press enter to next.")
print()

print("下記の中から件数が0のテーブルにレコードを挿入する")
for ds_id in ds_ids:
    print("INSERT INTO prep_datasource_{0}_{1}_{2} SELECT * FROM prep_datasource_{2};".format(ds_types[ds_id],wf_v,ds_id))
input("press enter to next.")
print()

print("各テーブルのレコード数を再度確認")
for ds_id in ds_ids:
    print("SELECT COUNT(*) FROM prep_datasource_{0}_{1}_{2};".format(ds_types[ds_id],wf_v,ds_id))
input("press enter to next.")
print('コミット\n')
input("press enter to next.")
print('Go to next code cell.')

print("---手順５：prep_task_xxの確認と作成---")
print("下記のクエリを実行し、prep_taskを作成する")
for k,v in task_dsf.items():
    print("CREATE TABLE IF NOT EXISTS prep_task_{0} (LIKE {1});".format(k,v))
print(input("press enter to next."))
print()

print("下記のクエリを実行し、prep_taskにレコードを挿入する")
print("トランザクション開始")
input("press enter to next.")
print("各テーブルのレコード数の確認")
for k in task_dsf.keys():
    print("SELECT COUNT(*) FROM prep_task_{};".format(k))
input("press enter to next.")
print()

print("下記の中から件数が0のテーブルにレコードを挿入する")
for k,v in task_dsf.items():
    print("INSERT INTO prep_task_{0} SELECT * FROM {1};".format(k,v))
input("press enter to next.")
print()

print("再度レコード数を確認する")
for k in task_dsf.keys():
    print("SELECT COUNT(*) FROM prep_task_{};".format(k))
input("press enter to next.")
print('\nコミット')
input("press enter to next.")

print("\n再度レコード数を確認する")
for k in task_dsf.keys():
    print("SELECT COUNT(*) FROM prep_task_{};".format(k))

print("\n終わり")
