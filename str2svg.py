from io import BytesIO
import matplotlib.pyplot as plt
# matplotlib: force computer modern font set
plt.rc('mathtext', fontset='cm')

#将tex公式渲染成SVG格式图片.入口参数：string formula为tex公式代码，fontsize为字号，dpi为分辨率，越小越清晰
def tex2svg(formula, fontsize=12, dpi=1):
    fig = plt.figure(figsize=(0.001, 0.001))
    fig.text(0, 0, r'${}$'.format(formula), fontsize=fontsize)

    output = BytesIO()
    fig.savefig(output, dpi=dpi, transparent=True, format='svg',
                bbox_inches='tight', pad_inches=0.0)
    plt.close(fig)

    output.seek(0)
    return output.read()