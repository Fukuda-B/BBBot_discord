"""
BrainF-ck.py

[ Compiler specification ]
Based on Brainfuck (bf20041219),

Characteristic behavior
Incrementing 255 will set it to 0.
Decrementing 0 will set it to 255.

"""

# ----- Main
class BrainFuck():

    # self, ソースコード, デバッグオプション
    def bf(self, tx:str, option):
        """Exec BrainF*ck"""
        tx = BrainFuck.origin(self, tx) # コメントなしのコード
        shift = 0 # ポインタ保持変数
        maxShift = 0
        arr = [0]
        out = [] # 出力
        Error = ""
        i = 0 # コードの解析位置
        debug = "" # ステップデバッグ
        while 1:

            if option == 1: debug += str(tx[i])+" @"+str(shift)+" "+str(arr)+"\n" # Debug
    
            vs = str(tx[i])
            if vs == '+': # 255未満ならインクリメント、255以上なら0
                arr[shift] += 1 if arr[shift] < 255 else 0
            elif vs == '-': # 0より大きい場合はデクリメント、0未満なら255
                arr[shift] -= 1 if arr[shift] > 0 else 255
            elif vs == '>': # ポインタをインクリメント (+)
                if len(arr) <= shift+1: arr.append(0)
                shift += 1
                if shift > maxShift : maxShift = shift
            elif vs == '<': # ポインタをデクリメント(-)
                shift -= 1
                if shift < 0:
                    Error = "Out of range of array Error"
                    break
            elif vs == '.': # 出力の追加
                out.append(arr[shift])
            elif vs == '[':
                if arr[shift] != 0:
                    c_cnt, res_loop = 0, "" # ループチェッカー, ループの展開した結果
                    s_ptr, e_ptr = i, 0 # 開始ポインタ, 終了ポインタ
                    l_cnt = 0 # ループカウンタ
                    while(c_cnt != 0 or l_cnt == 0):
                        vvs = tx[i+l_cnt] # コード解析用
                        if vvs == '[': c_cnt += 1
                        if vvs == ']': c_cnt -= 1
                        l_cnt += 1
                        if i+l_cnt > len(tx):
                            Error = "Corresponding brackets are missing."
                            break
                    e_ptr = i + l_cnt
                    if e_ptr > 0:
                        for j in range(arr[shift]):
                            res_loop += tx[(i+1):(e_ptr-1)]
                    tx = str(tx[:(s_ptr)]) + str(res_loop) + str(tx[(e_ptr):]) # コード展開
                    i -= 1 # コード展開により "[" 1命令文減るため、戻す
                else: # "[" かつポインタの指す値が0だった場合
                    while 1:
                        i += 1
                        if tx[i] == ']': break
                        if i > len(tx):
                            Error = "Corresponding brackets are missing."
                            break
            i += 1
            # print(tx, arr, i)
            # print(tx[i], arr, arr[shift], "||", tx[i+1])
            if i >= len(tx): break
            # elif vs == ',':

        # ASCII Decode
        result = ""
        for i in range(len(out)):
            result += chr(out[i])

        # 出力, エラー, 結果,
        # 展開後のコード, ステップ数
        return result, Error, out,\
        tx, len(tx), debug

    # コメント削除
    def origin(self, tx):
        return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '>', '<', '+', '-'], tx))
