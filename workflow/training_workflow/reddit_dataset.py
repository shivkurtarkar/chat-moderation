import pandas as pd

class DataSource:
    def get_data():
        pass

class RedditDataset(DataSource):
    def __init__(self, data_dir, filename):        
        self.data_dir= data_dir
        self.columns = ["prev_idx", "body", "score", "parent_id", "id", "created_date", "retrieved_date", "removed"]
        self.filename = filename
    def _get_dataframe(self, name):
        dataset_filename = f'{self.data_dir}/{name}'
        dataset = pd.read_csv(
            dataset_filename,
            names=self.columns,
            skiprows=1,
            encoding='ISO-8859-1'
        )
        return dataset
    def get_data(self):
        dataset = self._get_dataframe(self.filename)        
        return dataset['body']   
    def get_labels(self):
        dataset = self._get_dataframe(self.filename)
        return dataset['removed']

if __name__ == '__main__':
    train_dataset = 'reddit_200k_train.csv'
    test_dataset = 'reddit_200k_test.csv'
    DATASET_DIR='../../data/reddit'    

    train_dataset = RedditDataset(DATASET_DIR, train_dataset)
    X_train = train_dataset.get_data()
    y_train = train_dataset.get_labels()
    print(X_train)
    test_dataset = RedditDataset(DATASET_DIR, test_dataset)
    X_test = test_dataset.get_data()
    y_test = test_dataset.get_labels()
    print(X_test)