# 수학 기호 인식 모델

# Setting
import sys
import os
sys.path.append(os.getcwd())
from config import *
from models import *
from keras.preprocessing.image import ImageDataGenerator

# GPU 체크
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())

# Data Load
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

#train_generator = train_datagen.flow_from_directory('data/train', target_size=(64, 64), batch_size=128, class_mode='categorical')
#val_generator = val_datagen.flow_from_directory('data/val', target_size=(64, 64), batch_size=128, class_mode='categorical')

train_generator = train_datagen.flow_from_directory('data/train', target_size=(64, 64), batch_size=128, class_mode='categorical')
val_generator = val_datagen.flow_from_directory('data/val', target_size=(64, 64), batch_size=128, class_mode='categorical')
test_generator = test_datagen.flow_from_directory('data/test', target_size=(64, 64), batch_size=1, class_mode='categorical')


# Class 확인
print('Your Class: ', '\n', val_generator.class_indices)

# Model Define
# K.set_learning_phase(1)
K.set_image_data_format('channels_last')

# 학습
# 모델 컴파일 및 학습과정 설정
# 정확도는 Accuracy와 Top5 Accuracy를 이용하여 추적함
model = ResNet50(input_shape=(64, 64, 3), classes=29)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy', 'top_k_categorical_accuracy'])
early_stop = EarlyStopping(monitor='val_loss', min_delta=0, patience=5, verbose=0, mode='auto')

history = model.fit_generator(train_generator, steps_per_epoch=353, epochs=1,
                              validation_data=val_generator, validation_steps=3, callbacks=[early_stop])

# 학습과정 살펴보기
# show_loss_graph(history=history)

# Weight 저장
# model.save_weights('data/weights/WEIGHTS.h5')
# model.load_weights('data/weights/1.0.h5')
