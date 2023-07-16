from datetime import datetime
import pandas as pd
import batch

def test_prepare_data():
    def dt(hour, minute, second=0):
        return datetime(2022, 1, 1, hour, minute, second)

    data = [
        (None, None, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2), dt(1, 10)),
        (1, 2, dt(2, 2), dt(2, 3)),
        (None, 1, dt(1, 2, 0), dt(1, 2, 50)),
        (2, 3, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),     
    ]

    expected_data = [
        ('-1', '-1', dt(1, 2), dt(1, 10), 8.0),
        ('1', '-1', dt(1, 2), dt(1, 10), 8.0),
        ('1', '2', dt(2, 2), dt(2, 3), 1.0),
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    categorical = ['PULocationID', 'DOLocationID']

    df = pd.DataFrame(data, columns=columns)
    expected_df = pd.DataFrame(expected_data, columns=columns+['duration'])

    df_output = batch.prepare_data(df, categorical)
   
    diff_df = expected_df.compare(df_output[columns+['duration']])
    print(df_output.head())
    print(df_output.dtypes)
    print(expected_df.head())
    print(expected_df.dtypes)

    print(diff_df.head())
    #expected_df.equals(df_output[columns+['duration']])

    assert len(diff_df) == 0
