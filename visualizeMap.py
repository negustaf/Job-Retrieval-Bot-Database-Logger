import plotly.graph_objects as go
import pandas as pd
import os
#works

def visualise(path,csvName):
    df = pd.read_csv(path+r'\\'+csvName)
    #df.head()

    df['text'] = df['Location'] + ' ' + (df['Postings']).astype(str)+' postings'
    limits = [(0,5),(6,10),(11,15),(16,20),(21,3000)]
    colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
    scale = 100

    fig = go.Figure()

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[lim[0]:lim[1]]
        fig.add_trace(go.Scattergeo(
            locationmode = 'USA-states',
            lon = df_sub['Longitude'],
            lat = df_sub['Latitude'],
            text = df_sub['text'],
            marker = dict(
                size = df_sub['Postings']*scale,
                color = colors[i],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode = 'area'
            ),
            name = '{0} - {1}'.format(lim[0],lim[1])))

    fig.update_layout(
            title_text = 'Automotive Engineering Job Postings<br>(Click legend to toggle traces)',
            showlegend = True,
            geo = dict(
                scope = 'usa',
                landcolor = 'rgb(217, 217, 217)',
            )
        )

    fig.show()







if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    visualise(path,"data_analyst_map_info.csv")