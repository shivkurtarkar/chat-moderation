# export KAGGLE_USERNAME=datadinosaur
# export KAGGLE_KEY=xxxxxxxxxxxxxx
import  kaggle
kaggle.api.authenticate()
dataset = 'areeves87/rscience-popular-comment-removal'
kaggle.api.dataset_download_files(dataset, path = './output', unzip=True)