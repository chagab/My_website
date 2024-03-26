from .utils import *
import plotly.express as px
from plotly.offline import plot


# width = 29.7
# dpi = 100
# save = True
# cmap = "Blues_r"
# show = True
# format = 'png'

def makeFig(array, cmap, vmin, vmax):
    fig = px.imshow(
        array,
        color_continuous_scale=cmap,
        range_color=(vmin, vmax)
    )
    fig.update_traces(
        # hovertemplate="x: %{x} <br> y: %{y} <br> z: %{z} <br> color: %{color}"
        hovertemplate="You can zoom on this figure<br> optical density: %{z}<extra></extra>",
        # name="",
    )

    fig.update_layout(
        autosize=False,
        width=1000,
        height=140,
        showlegend=False,
        coloraxis_showscale=False,
        margin={
            "t": 0,
            "b": 0,
            "l": 0,
            "r": 0,
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    fig.update_xaxes(
        visible=False,
        showticklabels=False
    )
    fig.update_yaxes(
        visible=False,
        showticklabels=False
    )

    return fig


string = "Gabriel Chatelain"
randomize = True
alignement = 'center'
od = np.array(word2od(string, randomize=randomize, alignement=alignement))
vmax = 0.6
vmin = 0.08
cmap_dark = ['rgb(40, 40, 40)', 'rgb(200, 200, 200)']
cmap_light = ['rgb(200, 200, 200)', 'rgb(40, 40, 40)']

fig_dark = makeFig(od, cmap_dark, vmin, vmax)
fig_light = makeFig(od, cmap_light, vmin, vmax)

plot_div_dark = plot(
    fig_dark,
    output_type='div',
    include_plotlyjs=False,
    show_link=False,
    link_text=""
)
# plot_div_light = plot(fig_light, output_type='div')
