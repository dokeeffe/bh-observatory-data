import glob
import pandas as pd

def load_all(pattern):
    allFiles = glob.glob(pattern)
    frame = pd.DataFrame()
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_,index_col=None, header=0)
        list_.append(df)
    frame = pd.concat(list_)
    return frame

if __name__ == '__main__':
    frame = load_all('*.csv')
    # rs = frame[frame['filter'] == 'PV'].sort_values(['ra','dec']).head(100)
    rs = frame[(frame['dec'] > 36.4841) & (frame['dec'] < 36.4842) & (frame['ra'] > 250.4089) & (frame['ra'] < 250.4090) ].sort_values(['ra','dec']).head(100)
    print rs[['aperture_sum','date','ra','dec', 'filter']]