import pandas as pd

class DataSource:
    def get_data():
        pass

class RedditDataset(DataSource):
    def __init__(self, filename):                
        self.columns = ["prev_idx", "body", "score", "parent_id", "id", "created_date", "retrieved_date", "removed"]
        # self.columns = ["","X","BODY","REMOVED"]
        self.filename = filename
    def _get_dataframe(self, filename):
        dataset = pd.read_csv(
            filename,
            names=self.columns,
            skiprows=1,
            encoding='ISO-8859-1'
        )
        return dataset
    def get_data(self):
        dataset = self._get_dataframe(self.filename)        
        body_key = 'body'
        # body_key = 'BODY'
        return dataset[body_key]   
    def get_labels(self):
        dataset = self._get_dataframe(self.filename)
        removed_key = 'removed'
        # removed_key = 'REMOVED'
        return dataset[removed_key]

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