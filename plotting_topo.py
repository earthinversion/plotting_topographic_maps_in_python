from mpl_toolkits.basemap import shiftgrid
import numpy as np



def plot_topo(map,cmap='terrain',zorder=0,lonextent=(0,20),latextent=(35,60),plotstyle='pmesh'):
    minlon,maxlon = lonextent
    minlat,maxlat = latextent
    minlon,maxlon = minlon-1,maxlon+1
    minlat,maxlat = minlat-1,maxlat+1
    #20 minute bathymetry/topography data
    etopo = np.loadtxt('topo/etopo20data.gz')
    lons  = np.loadtxt('topo/etopo20lons.gz')
    lats  = np.loadtxt('topo/etopo20lats.gz')
    # shift data so lons go from -180 to 180 instead of 20 to 380.
    etopo,lons = shiftgrid(180.,etopo,lons,start=False)
    lons_col_index = np.where((lons>minlon) & (lons<maxlon))[0]
    lats_col_index = np.where((lats>minlat) & (lats<maxlat))[0]
 
    etopo_sl = etopo[lats_col_index[0]:lats_col_index[-1]+1,lons_col_index[0]:lons_col_index[-1]+1]
    lons_sl = lons[lons_col_index[0]:lons_col_index[-1]+1]
    lats_sl = lats[lats_col_index[0]:lats_col_index[-1]+1]
    lons_sl, lats_sl = np.meshgrid(lons_sl,lats_sl)
    if plotstyle=='pmesh':
        cs = map.contourf(lons_sl, lats_sl, etopo_sl, 50,latlon=True,zorder=zorder, cmap=cmap,alpha=0.5, extend="both")
        limits = cs.get_clim()
        cs = map.pcolormesh(lons_sl,lats_sl,etopo_sl,cmap=cmap,latlon=True,shading='gouraud',zorder=zorder,alpha=0.4,antialiased=1,vmin=limits[0],vmax=limits[1],linewidth=0)
    elif plotstyle=='contf':
        cs = map.contourf(lons_sl, lats_sl, etopo_sl, 50,latlon=True,zorder=zorder, cmap=cmap,alpha=0.4, extend="both")
    return cs


import netCDF4
def plot_topo_netcdf(map,etopo_file,cmap='terrain',zorder=0,lonextent=(0,20),latextent=(35,60)):
    f = netCDF4.Dataset(etopo_file)
    lons = f.variables['x'][:]
    lats = f.variables['y'][:]
    etopo = f.variables['z'][:]

    minlon,maxlon = lonextent
    minlat,maxlat = latextent
    minlon,maxlon = minlon-1,maxlon+1
    minlat,maxlat = minlat-1,maxlat+1

    lons_col_index = np.where((lons>minlon) & (lons<maxlon))[0]
    lats_col_index = np.where((lats>minlat) & (lats<maxlat))[0]

    etopo_sl = etopo[lats_col_index[0]:lats_col_index[-1]+1,lons_col_index[0]:lons_col_index[-1]+1]
    lons_sl = lons[lons_col_index[0]:lons_col_index[-1]+1]
    lats_sl = lats[lats_col_index[0]:lats_col_index[-1]+1]
    lons_sl, lats_sl = np.meshgrid(lons_sl,lats_sl)
    cs = map.contourf(lons_sl, lats_sl, etopo_sl, 100,latlon=True,zorder=zorder, cmap=cmap,alpha=0.6, extend="both")
    return cs
    