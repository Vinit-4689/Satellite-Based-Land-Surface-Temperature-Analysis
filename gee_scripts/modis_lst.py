#Load MODIS LST Dataset
def load_modis(roi):
    collection = (ee.ImageCollection('MODIS/061/MOD11A2')
                  .filterBounds(roi)
                  .filterDate('2022-01-01', '2022-12-31'))
    return collection


#Convert MODIS LST to Celsius
def process_modis(collection):
    def convert(image):
        lst = image.select('LST_Day_1km') \
                   .multiply(0.02) \
                   .subtract(273.15) \
                   .rename('LST')
        return lst.copyProperties(image, ['system:time_start'])
    
    return collection.map(convert)
