# https://github.com/Fukuda-B/BrainF-ck_py

class BrainFuck():
    
    def __init__(self, code, option):
        self.parsed = "" # parsed code
        self.code = BrainFuck.origin(self, code) # no comment code
        self.option = option # debug option
        self.error = "" # output error
        self.arr = [0] # memory value
        self.maxShift = 0 # max pointer position
        self.shift = 0 # pointer position
        self.i = 0 # counter
        self.debug = [] # debug result
        self.out = [] # output (list)
        self.out_asc = "" # output string
        self.limit = 2**16 # max loop

    def bf_main(self, code:str):
        """ Exec BrainF*ck """
        i, tx, arr, shift = \
            0, code, self.arr, self.shift
        if not tx: return
        while 1:
            # print(f'{tx[i]} @{self.shift} {self.arr} {i} {tx}')
            if self.option == 1: self.debug.append(f'{tx[i]} @{self.shift} {self.arr}') # debug
            elif self.option == 2: self.debug.append(f'{tx[i]} @{self.shift} {self.arr} {i} {tx}') # debug
            elif self.option == 3: self.debug.append(f'{tx[i]} @{self.shift}/{shift} {self.arr}/{arr} {i} {tx}') # full debug
            if tx[i] != '[' and tx[i] != ']': self.parsed += tx[i]          

            vs = str(tx[i])
            if vs == '+': self.arr[self.shift] = (self.arr[self.shift]+1) if self.arr[self.shift] < 255 else 0 # 255未満ならインクリメント、255以上なら0
            elif vs == '-': self.arr[self.shift] = (self.arr[self.shift]-1) if self.arr[self.shift] > 0 else 255 # 0より大きい場合はデクリメント、0未満なら255
            elif vs == '>': # ポインタをインクリメント (+)
                if len(self.arr) <= self.shift+1: self.arr.append(0)
                self.shift += 1
                if self.shift > self.maxShift: self.maxShift = self.shift
            elif vs == '<': # ポインタをデクリメント(-)
                self.shift -= 1
                if self.shift < 0:
                    self.error = 'Out of range of array Error'
                    break
            elif vs == '.': # 出力の追加
                self.out.append(self.arr[self.shift])
            elif vs == '[':
                c_cnt, l_cnt = 1, 1
                while(c_cnt != 0):
                    vvs = tx[i+l_cnt]
                    if vvs == '[': c_cnt += 1
                    if vvs == ']': c_cnt -= 1
                    l_cnt += 1
                    if i+l_cnt > len(tx):
                        self.error = ' ] are missing.'
                        break

                lc = 0
                while self.arr[self.shift] > 0:
                    self.arr = BrainFuck.bf_main(self, tx[i+1:i+l_cnt-1])
                    lc += 1
                    if lc > self.limit:
                        self.error = 'The loop limit has been exceeded.'
                        break
                i += l_cnt-1

            i += 1
            if i >= len(tx):
                self.i += i
                break
            elif len(self.error)>0: return self.arr
        return self.arr

    def bf_res(self):
        o_debug = '\n'.join(self.debug)
        return f'code:\n{self.code}\n\noutput:\n{self.out_asc}\n\nerror:\n{self.error}\n\nparsed:\n{self.parsed}\n\ndebug: mode={self.option}\n{o_debug}'

    def bf(self):
        """Exec BrainF*ck"""
        res = BrainFuck.bf_main(self, self.code)
        buf = []
        for i in self.out:
            buf.append(chr(i))
        self.out_asc = ''.join(buf)
        if self.option == 4: self.debug = f'```c\nOutput: {self.out_asc}\nError: {self.error}\nArray: {self.arr}\nParsed: {self.parsed}\nStep: {len(self.parsed)}\n```'
        return self

    # delete comment
    def origin(self, tx):
        return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '>', '<', '+', '-'], tx))
