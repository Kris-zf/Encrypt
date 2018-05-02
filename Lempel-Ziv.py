# -*- coding:utf-8 -*-
# Lempel-Ziv算法
# 待压缩字符串
my_str = """Discover new ways to build better—now with a free 14-day trial.
                The latest apps that help you and your team build software better, together.
                Automate your code review with style, quality, security, and test‑coverage checks when you need them.
                Automatically build and test your code as you push it to GitHub, preventing bugs from being deployed
                 to production.
                Monitor the impact of your code changes. Measure performance, track errors, and analyze your 
                application."""
# 码表
codeword_dictionary = {}
# 待压缩字符串长度
str_len = len(my_str)
# 码字最大长度
dict_maxlen = 1
# 将解析文本段的位置(下一次解析文本的起点)
now_index = 0
# 码表的最大索引
max_index = 0

compressed_str = ""

while now_index < str_len:

    # 向后移动步长
    my_step = 0
    #  向前匹配长度
    now_len = dict_maxlen
    if now_len > str_len - now_index:
        now_len = str_len - now_index
    # 查找到的码表索引
    cw_addr = 0
    while now_len > 0:
        cw_index = codeword_dictionary.get(my_str[now_index:now_index + now_len])
        if cw_index is not None:
            # 找到码字
            cw_addr = cw_index
            my_step = now_len
            break
        now_len -= 1
    if cw_addr == 0:
        # 没有找到码字，增加新的码字
        max_index += 1
        my_step = 1
        codeword_dictionary[my_str[now_index:now_index + my_step]] = max_index
        print(f"don't find the Code word,add Code word:{my_str[now_index:now_index+my_step]} index:{max_index:d}")
    else:
        # 找到码字
        max_index += 1
        codeword_dictionary[my_str[now_index:now_index + my_step + 1]] = max_index
        if my_step + 1 > dict_maxlen:
            dict_maxlen = my_step + 1
            print("find the Code word:%s add Code word:%s index :%d" % (
            my_str[now_index:now_index + now_len], my_str[now_index:now_index + my_step + 1], max_index)
                  )


    # 计算压缩后的结果
    cwdindex = '%d' % cw_addr
    if cw_addr == 0:
        cwlater = my_str[now_index:now_index+1]
        now_index += 1
    else:
        now_index += my_step
        cwlater = my_str[now_index:now_index+1]
        now_index += 1
    cw = cwdindex + cwlater
    compressed_str+=cw

print("\n----------------------\n")
print(my_str)
print("\n**********************\n")
print(compressed_str)
print("\n----------------------\n")