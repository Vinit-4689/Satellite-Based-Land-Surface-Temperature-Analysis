#NDVI Calculation
def add_ndvi(image):
    ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')
    return image.addBands(ndvi)

#LST CALCULATION
def calculate_lst(image):
    # Step 1: Convert Thermal Band (Band 10) to Radiance
    radiance = image.select('ST_B10').multiply(0.00341802).add(149.0)

    # Step 2: Brightness Temperature
    bt = radiance.rename('BT')

    # Step 3: NDVI
    ndvi = image.select('NDVI')

    # Step 4: Emissivity Calculation
    ndvi_min = 0.2
    ndvi_max = 0.5

    pv = ((ndvi.subtract(ndvi_min))
          .divide(ndvi_max - ndvi_min)
          .pow(2))

    emissivity = pv.multiply(0.004).add(0.986).rename('EM')

    # Step 5: LST Calculation
    lst = bt.expression(
        '(BT / (1 + (0.00115 * BT / 1.4388) * log(EM))) - 273.15',
        {
            'BT': bt,
            'EM': emissivity
        }).rename('LST')

    return image.addBands(lst)

#Apply Full Pipeline
