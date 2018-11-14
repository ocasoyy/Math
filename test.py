# Test

# Setting
import sys
import os
sys.path.append(os.getcwd())
from config import *
from models import *
from keras.preprocessing.image import ImageDataGenerator

# Data Load
test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory('data/test', target_size=(64, 64), batch_size=1, class_mode='categorical')


# 테스트 모델
model = ResNet50(input_shape=(64, 64, 3), classes=29)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy', 'top_k_categorical_accuracy'])
model.load_weights('data/weights/1.0.h5')

def main(model):
    """
    :param model: trained ResNet50
    :return: 테스트 결과 출력
    """
    output = model.predict_generator(test_generator, verbose=0)
    dic = test_generator.class_indices
    idx = np.argsort(output, axis=1)[0][::-1][0]
    indices = np.argsort(output, axis=1)[0][::-1][0:6]

    print("Test 이미지는", list(dic.keys())[idx], "입니다")
    print("==============================================")
    print("찾으시는 기호는 아래 중에 있습니다.")
    for index in indices:
        print(list(dic.keys())[index])


if __name__ == '__main__':
    main(model=model)
