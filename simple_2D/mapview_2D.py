import pygmt
import pandas as pd

cat = pd.read_csv("catalog.csv") # load your catalog file

spacing = 0.05 # optional
minlatitude = cat.latitude - spacing
maxlatitude = cat.latitude + spacing
minlongitude= cat.longitude - spacing
maxlongitude= cat.longitude + spacing

# define the region
region = [
    minlongitude,
    maxlongitude,
    minlatitude,
    maxlatitude,
]


fig = pygmt.Figure()
pygmt.config(MAP_FRAME_TYPE="plain", FORMAT_GEO_MAP="ddd.xx") 
projection = "M18c"
fig.basemap(region=region, projection=projection, frame=['a'],
                map_scale="g-116.84/33+w50k")
fig.coast(region=region, water="skyblue", shorelines="0.5p", land = "LIGHTGRAY" )

path2faults = "Faults.txt" # Optional: Load your fault file. If not, comment this section
fig.plot(
    data=path2faults,
    pen="1.25p,black",
)
# create the colormap. Either download from an open source or use GMTs
pygmt.makecpt(cmap="curvature.cpt", 
            series=[cat.z.min(), cat.z.max()], reverse=False)

ms = "c0.1c"
fig.plot(x=cat.logitude, y=cat.latitude, fill=cat.z, 
         size= [0.09]*len(cat.z), style = 'cc',cmap=True,
         pen="0.10p,gray40"
         )

# choose your event for focal mechanism
idx_max = cat.magnitude.idxmax()
main = cat.iloc[idx_max]
focal_mechanism = dict(strike=307, dip=80, rake=-171, magnitude=main.magnitude)
fig.meca(focal_mechanism, scale="0.7c", longitude=main.longitude, latitude=main.latitude
            , depth=main.z, G = "gray")

fig.text(x=-116.50,y=33.48, text= f"2013 M4.7 Anza Borrego Earthquake",fill = 'white' ,
         font="12p,Helvetica-Bold,black")
fig.basemap(map_scale="g-116.50/33.462+w3.0k+f+u", box = '+p1p,black+gwhite')
fig.colorbar(frame="xaf+lTime since Mainshock (day)",
            position="g-116.53/33.45+w6c/0.5c+h",box='+p1p,black+gwhite')

fig.show()
