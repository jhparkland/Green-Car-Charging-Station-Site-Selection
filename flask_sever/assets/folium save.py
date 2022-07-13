import folium

my_pos = [35.1154117, 128.9675937]
## open street map
map_osm = folium.Map(
    location= my_pos,
    zoom_start=17
)
html = '''<body style="background-color:#A0B3C4;">
        <iframe src="fig4.html" style="background-color: #E9EEF6 "font-family:'NanumSquare'; " width="850" height="400"  frameborder="0" >
        </body>
        '''

iframe = folium.IFrame(html,
                       width=100,
                       height=100)
popup = folium.Popup(folium.Html(html, script=True, width=850, height=400))
folium.Marker(my_pos, popup=popup).add_to(map_osm)
map_osm.save('map3.html')
