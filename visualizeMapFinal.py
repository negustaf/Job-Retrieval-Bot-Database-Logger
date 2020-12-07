import plotly.graph_objects as go
import pandas as pd
import os
#works

def visualise(path,csv1Name,csv2Name):
    df = pd.read_csv(path+r'\\'+csv1Name)
    #df.head()

    df['text'] = df['Location'] + ' ' + (df['Postings']).astype(str)+' postings'
    limits = [(0,3000)]
    colors = ["royalblue"]
    scale = 100

    fig = go.Figure()

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[lim[0]:lim[1]]
        #print(df_sub)
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
            #name = '{0} - {1}'.format(lim[0],lim[1])))
            name = "Data Analyst Postings"))
    
    
    df = pd.read_csv(path+r'\\'+csv2Name)
    #df.head()

    df['text'] = df['Location'] + ' ' + (df['Postings']).astype(str)+' postings'
    limits = [(0,3000)]
    colors = ["crimson"]
    scale = 100

    

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[lim[0]:lim[1]]
        #print(df_sub)
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
            #name = '{0} - {1}'.format(lim[0],lim[1])))
            name = 'UX Designer Postings'))
    fig.update_layout(
            title_text = 'Job Postings<br>(Click legend to toggle traces)',
            showlegend = True,
            geo = dict(
                scope = 'usa',
                landcolor = 'rgb(217, 217, 217)',
            )
        )

    fig.show()







if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    visualise(path,"data_analyst_map_info.csv", "ux_designer_map_info.csv")