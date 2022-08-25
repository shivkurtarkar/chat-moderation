# export KAGGLE_USERNAME=datadinosaur
# export KAGGLE_KEY=xxxxxxxxxxxxxx
import argparse

def download_from_kaggle(dataset, output_dir, unzip):
    import  kaggle
    import os
    print("starting ...")
    print(os.listdir())
    print(os.listdir("/home/newuser"))    
    kaggle.api.authenticate()    
    kaggle.api.dataset_download_files(dataset, path = output_dir, unzip=unzip)
    print(os.listdir(output_dir))
    print("Dataset downloaded successfully")




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dataset',
        help='Kaggle dataset name.'
    )
    parser.add_argument(
        '--output_dir',
        help='Output directory where dataset will be downloaded.'
    )
    parser.add_argument(
        '--unzip',
        help='Should unzip data.',
        default=True
    )
    # dataset = 'areeves87/rscience-popular-comment-removal'
    # output_dir = './output'

    args = parser.parse_args()
    download_from_kaggle(args.dataset, args.output_dir, args.unzip)