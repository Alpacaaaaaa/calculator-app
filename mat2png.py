'''
本文件是使用matplotlib以latex渲染矩阵生成png图片的实现。
！！！重要问题：太慢了，画个png出来大概要两三秒，如果画成svg的话更慢（时间翻倍）
寻求更好的办法
更新：优化图片尺寸估计参数
'''

import os
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.rc('mathtext', fontset='cm')
mpl.rcParams['text.usetex'] = True

#将tex公式（最好是矩阵）渲染成png格式图片.入口参数：string formula为tex公式代码，size为行与列维度（总的，如果是多个矩阵就是各矩阵行数和与列数和）
def mat2png(formula, size = None, name = 'ans'):
    # formula = None
    w,h =  (3,3) if size is None else size
    w += formula.count('matrix')
    mpl.rcParams['font.size'] = 4 - formula.count('matrix')*0.5
    size = (w*0.15 + 0.2*formula.count('^{-1}'),h*0.1)
    fig = plt.figure(figsize=size, facecolor=(250/255, 250/255, 250/255))
    fig.text(0, 0.5, formula)
    path = name + '.png'  # 文件路径
    if os.path.exists(path):  # 如果文件存在
        os.remove(path)  
    fig.savefig('ans.png', dpi = 400)
if __name__ == '__main__':
    mat2png(r'$$\left[ \matrix{ 12 & 5 & 2 \cr 20 & 4 & 8 \cr 2 & 4 & 3 \cr 7 & 1 & 10 \cr} \right]$$',(4,3))