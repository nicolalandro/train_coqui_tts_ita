# train_coqui_tts_ita
My guide to create an italian TTS with Coqui

## Prepare the enviroment
* clone this repo and go with a terminal inside
* create a venv
```
python3.8 -m venv venv
source ven/bin/activate
# or for fish shell
source ven/bin/activate.fish
```
* clone the coqui repo (I use c63bb481e95bd4a1ff978947d8e3e6c0bfb4177f sha version) and install all libs
```
git clone https://github.com/coqui-ai/TTS.git
cd TTS
pip install -r requirements.txt
python setup.py install
cd ..
```

## Train the model
* modify the train_glowtts.py with the correct dataset_path and output_path, eventually change the batch size if you do not have nought ram into GPU
```
# activate venv
PYTORCH_CUDA_ALLOC_CONF="max_split_size_mb:25" CUDA_VISIBLE_DEVICES=1 python src/train_glowtts.py
```

## Use trained model
* predict one text from commandline
```
CUDA_VISIBLE_DEVICES=0 tts --text "Ciao Pippo" --model_path "OUTPUT_PATH/best_model.pth.tar" --config_path "OUTPUT_PATH/config.json"
```
* run a prediction server to play with the trained model
```
CUDA_VISIBLE_DEVICES=0 tts-server --model_path "OUTPUT_PATH/best_model.pth.tar" --config_path "OUTPUT_PATH/config.json"
```

## Results
|Model|Dataset|
|----|------|
|[glowtts](https://huggingface.co/z-uo/glowtts-male-it/tree/main)|[male-LJSpeech-italian](https://huggingface.co/datasets/z-uo/male-LJSpeech-italian)|
|[glowtts](https://huggingface.co/z-uo/glowtts-female-it/tree/main)|[female-LJSpeech-italian](https://huggingface.co/datasets/z-uo/female-LJSpeech-italian)|
|[vits](https://huggingface.co/z-uo/vits-male-it)|[male-LJSpeech-italian](https://huggingface.co/datasets/z-uo/male-LJSpeech-italian)|
|[vits](https://huggingface.co/z-uo/vits-female-it)|[female-LJSpeech-italian](https://huggingface.co/datasets/z-uo/female-LJSpeech-italian)|

