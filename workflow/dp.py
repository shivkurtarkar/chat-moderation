"""
Design patterns for machine learning pipeline

Adapter Pattern:
    decouple from external services
Factory Pattern
    decouple from data sources
Strategy Pattern
    decouple from algorithm
"""

class DataSource:
    """
        Use adapter for data source
        without adapter you have to write data fetching logic directly in main function
        if tommorow there is no database then you have to make changes to main function that
        can break your code.
        if you abstract away database into an adapter
        main function is only aware of existance of data source
        which has interface get_data which gives data but main function is not
        aware of where the data is comming from.
    """
    def __init__(self):
        """ Initialize data Source"""
        pass
    def get_data(self):
        """Get Data from source"""
        pass


"""
Factory pattern 
    use factory pattern on data sources
    instead of non descrete technical implementation like sql source or file source your can get domain specific class
    customer from factory class customer source.

"""

class Model:
    """
        Strategy pattern is an abstration of algorithmic dependency
        main function only deals with model predict interfaces

        strategy pattern also have a coherence        
    """
    def predict(self, data):
        """
            feature = transform(data)
            return self.model.predict(feature)
        """
        pass



if __name__=="__main__":

    source = kafkaSource()
    sink = MongoSink()

    model = Model()
    for data in source.read():
        pred = model.predict(data)
        sink.write(pred)
    
    # ====
    source = kafkaSource()
    sink = MongoSink()

    model = Model()
    def dosomething(data):        
        pred = model.predict(data)
        sink.write(pred)
    
    # source.subscribe(callback=dosomething)

    with threadPool(process=2) as pool:
        pool.map(dosomething, sink)
    

