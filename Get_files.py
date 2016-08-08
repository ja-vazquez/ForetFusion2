
import fitsio
import os, sys
import mechanize
import pandas as pd
from base64 import b64encode




def read_subset_fits(file_name):
    """Read the subsample of spAll we are interested in. Return a DataFrame"""
    if not os.path.isfile(file_name):
        sys.exit('File not found: {}'.format(file_name))

    print 'Reading file...'
    df = pd.read_csv(file_name, sep=',')
    return df




def read_fits(file_name, columns):
    """Read selected columns in the spAll file. Return a DataFrame"""
    file_name += '.fits'
    if not os.path.isfile(file_name):
        sys.exit('File not found: {}'.format(file_name))

    fits          = fitsio.FITS(file_name)
    fits_columns  = columns

    #http://stackoverflow.com/questions/30283836/
    # creating-pandas-dataframe-from-numpy-array-leads-to-strange-errors
    d  = {col: fits[1][col].read().byteswap().newbyteorder() for col in fits_columns}
    df = pd.DataFrame(d)
    return df




def get_bnl_files(plate, file_name):
    """nasty hack, but change it later"""
    print 'Getting file {} from the bnl'.format(file_name)
    os.system('scp astro:/data/boss/v5_10_0/spectra/{}/{} .'.format(plate, file_name))
    return 0




def get_web_files(plate, file_name, passwd):
    print 'Getting file {} from the web'.format(file_name)
    url = 'https://data.sdss.org/sas/ebosswork/eboss/spectro/redux/v5_10_0/spectra/{}/{}'.format(plate, file_name)
    username = 'sdss'
    password = '{}'.format(passwd)

    # I have had to add a carriage return ('%s:%s\n'), but
    # you may not have to.
    b64login = b64encode('%s:%s' % (username, password))

    br = mechanize.Browser()
    br.set_handle_robots(False)

    br.addheaders.append(
      ('Authorization', 'Basic %s' % b64login )
    )
    br.open(url)
    r = br.response()
    data = r.read()

    with open('%s'%(file_name),'wb') as output:
          output.write(data)

    return 0