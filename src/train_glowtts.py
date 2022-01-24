import os

# Trainer: Where the ✨️ happens.
# TrainingArgs: Defines the set of arguments of the Trainer.
from TTS.trainer import Trainer, TrainingArgs

# GlowTTSConfig: all model related values for training, validating and testing.
from TTS.tts.configs.glow_tts_config import GlowTTSConfig

# BaseDatasetConfig: defines name, formatter and path of the dataset.
from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.glow_tts import GlowTTS
from TTS.utils.audio import AudioProcessor

# we use the same path as this script as our training folder.
# output_path = os.path.dirname(os.path.abspath(__file__))
output_path = '/media/popos/Barracuda/Models/TTS_new/trained'
dataset_path = "/media/popos/Barracuda/Datasets/MAIL_LABS_TTS/it_IT/by_book/female/lisa_caputo/malavoglia"

# DEFINE DATASET CONFIG
# Set LJSpeech as our target dataset and define its path.
# You can also use a simple Dict to define the dataset and pass it to your custom formatter.
dataset_config = BaseDatasetConfig(
    name="ljspeech", meta_file_train="metadata.csv", path=dataset_path,
)

# INITIALIZE THE TRAINING CONFIGURATION
# Configure the model. Every config class inherits the BaseTTSConfig.
config = GlowTTSConfig(
    batch_size=128,
    eval_batch_size=16,
    num_loader_workers=4,
    num_eval_loader_workers=4,
    run_eval=True,
    test_delay_epochs=-1,
    epochs=1000,
    text_cleaner="phoneme_cleaners",
    use_phonemes=False,
    phoneme_language="it-it",
    phoneme_cache_path=os.path.join(output_path, "phoneme_cache"),
    print_step=25,
    print_eval=False,
    mixed_precision=True,
    output_path=output_path,
    datasets=[dataset_config],
)

config.audio['sample_rate'] = 16000

# INITIALIZE THE AUDIO PROCESSOR
# Audio processor is used for feature extraction and audio I/O.
# It mainly serves to the dataloader and the training loggers.
ap = AudioProcessor(**config.audio.to_dict())

# LOAD DATA SAMPLES
# Each sample is a list of ```[text, audio_file_path, speaker_name]```
# You can define your custom sample loader returning the list of samples.
# Or define your custom formatter and pass it to the `load_tts_samples`.
# Check `TTS.tts.datasets.load_tts_samples` for more details.
train_samples, eval_samples = load_tts_samples(dataset_config, eval_split=True)

# INITIALIZE THE MODEL
# Models take a config object and a speaker manager as input
# Config defines the details of the model like the number of layers, the size of the embedding, etc.
# Speaker manager is used by multi-speaker models.
model = GlowTTS(config, speaker_manager=None)

# INITIALIZE THE TRAINER
# Trainer provides a generic API to train all the 🐸TTS models with all its perks like mixed-precision training,
# distributed training, etc.
targs = TrainingArgs()
trainer = Trainer(
    targs,
    config,
    output_path,
    model=model,
    train_samples=train_samples,
    eval_samples=eval_samples,
    training_assets={"audio_processor": ap},  # assets are objetcs used by the models but not class members.
)

print(trainer.output_path)
directory = os.path.dirname(trainer.output_path)
if not os.path.exists(directory):
    os.makedirs(directory)
logfilepath = os.path.join(trainer.output_path, 'trainer_0_log.txt')
with open(logfilepath, 'w'):
    os.utime(logfilepath, None)
print('!!!!',logfilepath)

# AND... 3,2,1... 🚀
trainer.fit()
