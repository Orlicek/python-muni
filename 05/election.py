import json
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, LabelSet
from numpy import pi

def share_to_angle(share):
    return (share/100) * (2*pi)

with open('election.json') as data_file:    
    data = json.load(data_file)

sorted_data = list(sorted(data, key=lambda k: k.get('share'), reverse = True))
share = [party.get('share') for party in sorted_data]
colors = [party.get('color') if party.get('color') else '#909090' for party in sorted_data]


p = figure(x_range = (-1, len(data)))
p.vbar(x = list(range(0,len(data))), top = share, width = 0.7, color=colors)
#show(p)


#PART 2

below_one_percent = {
    'share': 0,
    'short': 'below 1%',
    'color': '#909090'
}
new_data = []
for party in reversed(sorted_data):
    if party.get('share') < 1.0:
        below_one_percent['share'] += party.get('share')
    else:
        index = sorted_data.index(party)
        new_data = sorted_data[:index]
        break

new_data.append(below_one_percent)

new_share = [party.get('share') for party in new_data]
new_colors = [party.get('color') if party.get('color') else '#909090' for party in new_data]
new_labels = [party.get('short') for party in new_data]

source = ColumnDataSource(dict(x=list(range(0, len(new_data))), top=new_share, label=new_labels, colors=new_colors))

labels = LabelSet(x='x', text='label', level='glyph', y_offset=0, x_offset=-13.5, y='top', source=source, render_mode='canvas')
p = figure(x_range = (-1, len(new_data)))
p.vbar(color='colors', x='x', top='top', bottom=0, width=0.7, source = source)
p.add_layout(labels)
show(p)


#PART 3
for party in new_data:
    print(share_to_angle(party.get('share')))

angle_source = ColumnDataSource(data = {
    'start': [],
    'end':[],
    'color': new_colors,
    'label': new_labels
})
p = figure()
p.wedge(
    x = 0,
    y = 0,
    radius = 5,
    start_angle = 'start',
    end_angle = 'end',
    color = 'color',
    legend = 'label',
    source = angle_source
)
