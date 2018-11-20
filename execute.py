# Test

# Setting
import sys
import os
sys.path.append(os.getcwd())
from config import *
from models import *
from keras.preprocessing.image import ImageDataGenerator


# 테스트 모델
model = ResNet50(input_shape=(64, 64, 3), classes=29)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy', 'top_k_categorical_accuracy'])
model.load_weights('data/weights/1.0.h5')

# MySQL Connection 연결
conn = pymysql.connect(host='ec2-52-34-245-98.us-west-2.compute.amazonaws.com',
                       user='pmauser', password='gongmo2018',
                       db='PhoneInfo', charset='utf8')

cursor = conn.cursor()

# SQL문 실행
sql = "select * from PhoneInfo"
cursor.execute(sql)


# Signal 처리
while True:
    rows = cursor.fetchall()
    past = len(rows)
    sleep(1)

    rows = cursor.fetchall()
    current = len(rows)
    id = str(rows[-1][0])
    if past == current:
        # img = rows[-1][0]    # 현재는 ID를 출력함, img가 (64, 64)임을 가정함
        # img = image.load_img('data/test/phi/test.jpg', target_size=(64, 64))
        img_blob = rows[-1][2]

        im = base64.b64decode(img_blob)
        img = Image.open(BytesIO(im))
        img_input = image.img_to_array(img)/255.

        INPUT = K.expand_dims(img_input, axis=0)
        output = model.predict(INPUT, steps=1)     # model output: (1, 29)
        result = np.argsort(output[0])[::-1][0:6]  # 예측 번호(기호)를 담은 np.array, (6, )

        update_sql = """UPDATE PhoneInfo SET Result1=%s, Result2=%s, Result3=%s, Result4=%s, Result5=%s, Result6=%s WHERE Nickname=%s"""
        cursor.execute(update_sql, (int(result[0]), int(result[1]), int(result[2]), int(result[3]), int(result[4]), int(result[5]), id))
        conn.commit()



# DB 연결 닫기
# conn.close()


"""
imageFile = open('data/test/phi/phi.jpg', "rb")
test1 = base64.b64encode(imageFile.read())
imageFile = open('data/output1.blob', "wb")
imageFile.write(test1)
imageFile.close()

imageFile = open('data/test/Delta/delta.jpg', "rb")
test2 = base64.b64encode(imageFile.read())
imageFile = open('data/output2.blob', "wb")
imageFile.write(test2)
imageFile.close()
"""

# blob로 변환한 파일 저장
# im = base64.b64decode(text)
# png_recovered = Image.open(BytesIO(im))
# png_recovered.save("data/output.jpg")
