import os
import re
import boto3
import numpy as np
import random as rm
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
from s3fs.core import S3FileSystem
import environ


class BECFigure():

    all = []

    def __init__(self,) -> None:
        credentials = self.getCredentials()

        self.s3_fs = S3FileSystem(
            key=credentials['AWS_ACCESS_KEY_ID'],
            secret=credentials['AWS_SECRET_ACCESS_KEY'],
        )

        self.s3_r = boto3.resource(
            's3',
            aws_access_key_id=credentials['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=credentials['AWS_SECRET_ACCESS_KEY'],
        )

        self.BUCKET_NAME = credentials['AWS_STORAGE_BUCKET_NAME']
        self.BASE_DIR = f'{self.BUCKET_NAME}/static/blog/npy'
        self.NPY_DIR = f'{self.BASE_DIR}/BECtff'
        self.MATRICES_DIR = f'{self.BASE_DIR}/str_matrices'

        BECFigure.all.append(self)

    def s3_listdir(self, path) -> list[str]:
        i = path.find("/")
        bucket_name = path[:i]
        file_name = path[i+1:]
        bucket = self.s3_r.Bucket(bucket_name)
        return [e.key for e in bucket.objects.all() if e.key.startswith(file_name)]

    def load(self, path) -> np.array:
        return np.load(self.s3_fs.open(path))

    def getCredentials(self) -> dict:
        env = environ.Env()
        BASE_DIR = '/'
        environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

        credentials = {
            'SECRET_KEY': env('SECRET_KEY'),
            'AWS_ACCESS_KEY_ID': env('AWS_ACCESS_KEY_ID'),
            'AWS_SECRET_ACCESS_KEY': env('AWS_SECRET_ACCESS_KEY'),
            'AWS_STORAGE_BUCKET_NAME': env('AWS_STORAGE_BUCKET_NAME'),
            'AWS_S3_REGION_NAME': env('AWS_S3_REGION_NAME'),
        }

        return credentials

    def word2matrix(self, word) -> np.array:
        L = len(word)
        kerning_filling_path = f"{self.MATRICES_DIR}/{ord(' ')}.npy"
        kerning_filling = self.load(kerning_filling_path)
        matrices_list = [kerning_filling]

        for index in range(L):
            string = word[index]
            matrix_path = f"{self.MATRICES_DIR}/{ord(string)}.npy"
            matrix = self.load(matrix_path)
            matrices_list.append(matrix)
            matrices_list.append(kerning_filling)

        return np.hstack(matrices_list)

    def word2od(self, word, randomize=True, alignement='center') -> np.array:
        Lines = re.split('\n', word)
        matrices = []

        for Line in Lines:
            matrix = self.word2matrix(Line)
            OD = []
            for column in matrix.T:
                name = ''.join(column.astype(int).astype(str))
                name_path = f"{self.NPY_DIR}/{name}"
                files_name = sorted(self.s3_listdir(name_path))
                rand_index = -1
                if randomize:
                    rand_index = rm.randint(0, len(files_name)-1)
                od_path = f"{self.BUCKET_NAME}/{files_name[rand_index]}"
                od = self.load(od_path).T
                if name != 7 * '0':
                    OD.append(od / (np.max(od)))
                else:
                    OD.append(od / 1.5)
            matrices.append(np.hstack(OD))

        return np.vstack(self.justification(matrices, alignement=alignement))

    def justification(self, arrays, alignement='center') -> list:
        new_arrays = []
        max_w = np.max([x.shape[1] for x in arrays])

        for x in arrays:
            if x.shape[1] < max_w:
                new_x = np.zeros((arrays[0].shape[0], max_w))
                missing = max_w - x.shape[1]
                if alignement == 'center':
                    left_fill = int(missing/2)
                elif alignement == 'left':
                    left_fill = 0
                elif alignement == 'right':
                    left_fill = max_w - x.shape[1]
                new_x[:, left_fill:left_fill+x.shape[1]] = x
                new_arrays.append(new_x)
            else:
                new_arrays.append(x)

        return new_arrays

    def makeFig(
        self,
        string,
        cmap,
        vmin,
        vmax,
        randomize,
        alignement,
        hovertemplate,
        autosize,
        width,
        height,
        showlegend,
        coloraxis_showscale,
        margin,
        paper_bgcolor,
        plot_bgcolor,
        xaxes_visible,
        xaxes_showticklabels,
        yaxes_visible,
        yaxes_showticklabels
    ) -> go.Figure:

        od = np.array(self.word2od(string, randomize, alignement))

        fig = px.imshow(
            od,
            color_continuous_scale=cmap,
            range_color=(vmin, vmax)
        )

        fig.update_traces(hovertemplate=hovertemplate)

        fig.update_layout(
            autosize=autosize,
            width=width,
            height=height,
            showlegend=showlegend,
            coloraxis_showscale=coloraxis_showscale,
            margin=margin,
            paper_bgcolor=paper_bgcolor,
            plot_bgcolor=plot_bgcolor
        )

        fig.update_xaxes(
            visible=xaxes_visible,
            showticklabels=xaxes_showticklabels
        )

        fig.update_yaxes(
            visible=yaxes_visible,
            showticklabels=yaxes_showticklabels
        )

        return fig

# file_name = f'static/blog/npy/BECtff/0000000/0000000_fidelity1.npy'
# fidelity = np.load(s3.open(f'{BUCKET_NAME}/{file_name}'))
# print(fidelity)
# od = np.array(word2od(string, randomize=randomize, alignement=alignement))


fig_params = {
    "string": "Gabriel Chatelain",
    "randomize": True,
    "alignement": 'center',
    "vmax": 0.6,
    "vmin": 0.08,
    "hovertemplate": "You can zoom on this figure<br> optical density: %{z}<extra></extra>",
    "cmap": ['rgb(40, 40, 40)', 'rgb(200, 200, 200)'],
    "autosize": False,
    "width": 1000,
    "height": 140,
    "showlegend": False,
    "coloraxis_showscale": False,
    "margin": {
        "t": 0,
        "b": 0,
        "l": 0,
        "r": 0,
    },
    "paper_bgcolor": 'rgba(0,0,0,0)',
    "plot_bgcolor": 'rgba(0,0,0,0)',
    "xaxes_visible": False,
    "xaxes_showticklabels": False,
    "yaxes_visible": False,
    "yaxes_showticklabels": False
}

# fig_dark = makeFig(od, cmap_dark, vmin, vmax)

bec_figure = BECFigure()
plot_div_dark = plot(
    bec_figure.makeFig(**fig_params),
    output_type='div',
    include_plotlyjs=False,
    show_link=False,
    link_text=""
)
