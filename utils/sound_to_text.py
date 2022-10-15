import os
import shutil
import time

import speech_recognition as sr
import soundfile as sf

from utils.logger import logger_v2t


def conversion(f_name, ex):
    data, samplerate = sf.read(f_name + ex)
    sf.write(f_name + '.wav', data, samplerate)

    return f_name + '.wav'


def recognition(f_name):
    rec = sr.Recognizer()

    f = sr.AudioFile(f_name)
    with f as f:
        audio = rec.record(f)
        text = rec.recognize_google(audio, language='ru-RU')

    return text


def main():
    files = os.listdir('medias/input')
    if len(files) > 0:
        for file in files:
            if file.endswith('.ogg'):
                f_name = file[:len(file) - file[::-1].index('.') - 1]

                logger_v2t.info(f'{file} start conversion')
                path = conversion('medias/input/' + f_name, '.ogg')

                logger_v2t.info(f'{file} start recognition')
                text = recognition(path)

                with open(f'medias/out/{f_name}.txt', 'w', encoding='utf-8') as f:
                    f.write(text)
                    f.write('\nREADY')

                t = time.time()
                os.mkdir(f'archive/{t}_{f_name}')
                shutil.move(f'medias/input/{file}', f'archive/{t}_{f_name}/input.ogg')
                os.remove(f'medias/input/{f_name}.wav')
                shutil.copy(f'medias/out/{f_name}.txt', f'archive/{t}_{f_name}/out.txt')

                logger_v2t.info(f'{file} recognition finished')

    time.sleep(5)
    main()
