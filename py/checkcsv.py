# coding: utf-8
import sys
import ast
import re
from datetime import datetime

pattern_date = '[1-9][0-9]{3}-[0-1][0-9]-[0-3][0-9]'
pattern_datetime =  '[1-9][0-9]{3}-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]'
# compile後match
repat_date = re.compile(pattern_date)
repat_dt = re.compile(pattern_datetime)
err_cnt = 0 # エラー箇所数
err_limit = 100 # これ以上エラーが見つかったらチェック処理を打ち切る

def judge_double(k,l,value):
    global err_cnt
    try:
        if value != '':
            val = float(value)
            if value[0] == '0':
                print('{0}行{1}列：1文字目が0の値>>{2}'.format(k, l, value))
                err_cnt += 1
    except:
        print('{0}行{1}列：小数型に変換できない文字列>>{2}'.format(k, l, value))
        err_cnt += 1
    finally:
        pass

def judge_bigint(k,l,value):
    global err_cnt
    try:
        if value != '':
            val = int(value)
            if value[0] == '0' or value[0:2] == '-0':
                print('{0}行{1}列：1文字目が0の値>>{2}'.format(k,l,value))
                err_cnt += 1
    except:
        print('{0}行{1}列：整数型に変換できない文字列>>{2}'.format(k,l,value))
        err_cnt += 1
    finally:
        pass
def judge_boolean(k,l,value):
    global err_cnt
    try:
        if value.upper() not in ['TRUE','FALSE']:
            print('{0}行{1}列：真偽値型に変換できません。>>{2}'.format(k,l,value))
            err_cnt += 1
    except TypeError as e:
        print('{0}行{1}列：真偽値型にNULLは許容されません。'.format(k,l))
        err_cnt += 1


def judge_date(k,l,value):
    global err_cnt
    result = re.fullmatch(repat_date,value)
    if result is None:
        print('{0}行{1}列：日付型のフォーマット違反>>{2}'.format(k,l,value))
        err_cnt += 1
    else:
        try:
            day = datetime.strptime(value, "%Y-%m-%d")
        except:
            print('{0}行{1}列：日付型のフォーマット違反>>{2}'.format(k, l, value))
            err_cnt += 1
        finally:
            pass
def judge_timestamp(k,l,value):
    global err_cnt
    result = re.match(repat_dt,value)
    if result is None:
        print('{0}行{1}列：日時型のフォーマット違反>>{2}'.format(k, l, value))
        err_cnt += 1
    else:
        try:
            day = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except:
            print('{0}行{1}列：日時型のフォーマット違反>>{2}'.format(k, l, value))
            err_cnt += 1
        finally:
            pass


if __name__=="__main__":
    args = sys.argv
    # コマンドライン引数にファイル名,文字コード,データソースID
    # ダブルクオーテーションで囲まれていないファイルは非対応
    file_name = args[1]
    print(file_name)
    encoding = args[2]
    print(encoding)
    if encoding in ["utf-8","shift-jis"]:
        print("encoding : " + args[2])
    else:
        print("文字コードは'utf-8','shift-jis'のいずれかを指定してください。")
        exit()

    dsid = args[3] # データソースID
    schema = {}
    lines = []

    with open(file_name, 'r', encoding=encoding) as f:
        record = ""
        for row in f.readlines():
            record += row.strip()
            if record[-1] == '"':
                lines.append(record)
                record = ''
            else:
                record += '\n'
        if len(record)>0:
            lines.append(record)

    if len(dsid)>0:
        print ('データソースID:{}のtable_schemaまたはrecreate_schemaの値をペーストしてください。'.format(dsid))
        while(1):
            try:
                # テスト用　
                # {"columns": [{"column_name": "column_1", "column_type": "text", "primary_key": true, "column_label": "テキスト", "sort_order_key": 0, "column_header_name": "テキスト"}, {"column_name": "column_2", "column_type": "bigint", "primary_key": false, "column_label": "整数", "sort_order_key": 0, "column_header_name": "整数"}, {"column_name": "column_3", "column_type": "double", "primary_key": false, "column_label": "小数", "sort_order_key": 0, "column_header_name": "小数"}, {"column_name": "column_4", "column_type": "date", "primary_key": false, "column_label": "日付", "sort_order_key": 0, "column_header_name": "日付"}, {"column_name": "column_5", "column_type": "timestamp", "primary_key": false, "column_label": "日時", "sort_order_key": 0, "column_header_name": "日時"}, {"column_name": "column_6", "column_type": "boolean", "primary_key": false, "column_label": "真偽値", "sort_order_key": 0, "column_header_name": "真偽値"}], "table_name": "prep_table_3", "table_label": "テーブル_3"}
                line = input('schema : ').strip().replace('true,','True,').replace('false,','False,')
                # print (type(line))
                #schema = json.loads(line)
                schema = ast.literal_eval(line)
                # print(schema)

                col_1 = '列番'
                col_2 = 'column_name'
                col_3 = 'column_label'
                col_4 = 'column_type'
                col_5 = 'primary_key'
                print(col_1, col_2, col_3, col_4, col_5)
                i = 1
                for row in schema['columns']:
                    # print(row)
                    print(i, row[col_2], row[col_3], row[col_4], row[col_5])
                    i += 1

                # ヘッダ行の確認
                header = lines[0].strip()[1:-1].split('","')

                for j in range(len(schema['columns'])):
                    if header[j] != schema['columns'][j]['column_label']:
                        print('Column name does not match: ', lines[0][j], schema['columns'][j]['column_label'])
                print('header check has completed.')
                break
            except Exception as e:
                print (e)
                if input('＋ボタンへの取り込みですか？(y/n)：') == 'y':
                    break
            finally:
                pass

    # レコード行のチェック
    k = 1
    columns = len(lines[0].strip()[1:-1].split('","')) # ヘッダ行のカラム数
    maybe_boolean = [['TRUE','FALSE',''] for i in range(columns)]  # boolean型かもしれないカラム
    # print(maybe_boolean)
    for record_line in lines[1:]:
        record = record_line[1:-1].split('","')
        print(record)
        # カラム数のチェック
        length = len(record)
        if length != columns:
            print('{0}行目：ヘッダのカラム数({1})と異なります。>>({2}カラム)'.format(k,columns,l))
            exit()

        l = 1
        for val in record:
            # データソースに取り込む場合
            if schema != {}:
                c_type = schema['columns'][l-1]['column_type']
                # print(c_type)
                if c_type == 'bigint':
                    judge_bigint(k, l, val)
                elif c_type == 'double':
                    judge_double(k, l, val)
                elif c_type == 'boolean':
                    judge_boolean(k, l, val)
                elif c_type == 'date':
                    judge_date(k, l, val)
                elif c_type == 'timestamp':
                    judge_timestamp(k, l, val)
            else:
                # ＋ボタンに入る場合
                if val.upper() in ['TRUE','FALSE','']:
                    # print(k,l)
                    maybe_boolean[l-1].remove(val.upper())
            l += 1
        if err_cnt > err_limit:
            print('エラー箇所が{}を超えたのでチェックを打ち切ります。'.format(err_limit))
            break
        k += 1

    m = 1
    # print(maybe_boolean)
    for c in maybe_boolean:
        if '' not in c and len(c) < 2:
            print('{}カラム目は真偽値と空文字を含んでいます。'.format(m))
        m += 1

    print("end.")
