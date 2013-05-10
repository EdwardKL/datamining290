import csv

prologue = '''vg.parse.spec({
  "width": 400,
  "height": 200,
  "padding": {"top": 10, "left": 30, "bottom": 20, "right": 10},
  "data": [
    {
      "name": "table",
      "values": ['''
middle = '''
]
    }
  ],
  "scales": [
    {"name":"x", "type":"ordinal", "range":"width", "domain":{"data":"table", "field":"data.x"}},
    {"name":"y", "range":"height", "nice":true, "domain":{"data":"table", "field":"data.y"}}
  ],
  "axes": [
    {"type":"x", "scale":"x"},
    {"type":"y", "scale":"y"}
  ],
  "marks": [
    {
      "type": "rect",
      "from": {"data":"table"},
      "properties": {
        "enter": {
          "x": {"scale":"x", "field":"data.x"},
          "width": {"scale":"x", "band":true, "offset":-1},
          "y": {"scale":"y", "field":"data.y"},
          "y2": {"scale":"y", "value":0}
        },
        "update": { "fill": {"value":"steelblue"} },
        "hover": { "fill": {"value":"red"} }
      }
    }
  ]
}, function(chart) {
    self.view = chart({el:"#'''
epilogue = '''"}).update();
});'''
tables = {}

def isNum(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

with open('star_results.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    start = True
    type = ""
    for row in reader:
        if start:
            start = False
            continue
        if len(row) > 0:
            if 'Type' in row[0]:
                type = row[0]
                tables[row[0]] = {"no":[], "yes":[]}
            elif isNum(row[0]):
                tables[type][row[2]].append(row)

js = ""
                
ids = []                
for type, rdic in tables.iteritems():
    for restrict, rows in rdic.iteritems():
        if len(rows) == 0:
            continue
        id = ''.join(type.split())+restrict
        id = ''.join(id.split(":"))
        if restrict == "no":
            ids.append((id, type))
        else:
            ids.append((id, type + " (Restricted to Restaurants)"))
        js += prologue
        start = True
        for row in rows:
            if start:
                start = False
            else:
                js += ","
            label = "("+str(row[0]) +", "+str(row[1])+")"
            js += "{'x':'"+label+"', 'y':"+str(row[5])+"}"
        js += middle
        js += id
        js += epilogue
        
        
html_start = '''<html>
<head>
<title>Vega Visualization</title>
</head>
<body>'''

html_end = '''
    <script src="d3.v2.min.js"></script>
    <script src="vega.min.js"></script>
    <script src="viz.js"></script>

</body>
</html>'''

html = html_start
for id, name in ids:
    html += "<h4>"+name+"</h4>"
    html += "<div id='"+id+"'></div>"
html += html_end
f = open("viz.html","w")
f.write(html)
f.close()

f = open("viz.js", "w")
f.write(js)
f.close()

            
            