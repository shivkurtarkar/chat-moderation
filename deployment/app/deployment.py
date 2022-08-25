from flask import Flask, request, jsonify
from reddit_classifier import RedditClassifier
from transformers import TokenizerTransformer, PreprocessingTransformer
import pickle

import mlflow
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType


def load_pickle(filename):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)


RUN_ID = '316eae0f743b4692a9bcb5149e77407d'
MLFLOW_TRACKING_URI = 'http://172.18.0.2:31989'
# MLFLOW_TRACKING_URI ='http://0.0.0.0:5000'
EXPERIMENT = 'text-moderation-model'
TOKENIZER_PATH = '../../workflow/output/tokenizer.pkl'


mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
# client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
# experiment = client.get_experiment_by_name(EXPERIMENT)
# print(experiment)
# latest_runs = client.search_runs(
#     experiment_ids=experiment.experiment_id,
#     filter_string="",
#     run_view_type=ViewType.ACTIVE_ONLY,
#     max_results=10
# )
# print(latest_runs)
# exit()

# Load model as a PyFuncModel.
logged_model = f'runs:/{RUN_ID}/model'
loaded_model = mlflow.pyfunc.load_model(logged_model)


loaded_tokenizer = load_pickle(TOKENIZER_PATH)
transformer = TokenizerTransformer(
    loaded_tokenizer, 
    next_transformer=PreprocessingTransformer()
)
reddit_classifier = RedditClassifier(transformer, loaded_model)


app = Flask('message-moderation')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    message = request.get_json()
    
    body = message['body']
    
    pred = reddit_classifier.predict([body])
    pred = pred.tolist()[0]
    result = {
        'score': pred,
        'model_version': RUN_ID
    }
    print(result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)