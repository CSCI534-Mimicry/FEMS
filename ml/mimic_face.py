import tensorflow as tf
import ml.parameter as p
import ml.model as model
import numpy as np
import cv2
import os

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


def handle_input(f1, f2):
    l1, l2 = list(), list()
    face_raw = cv2.imread(f1)
    img = face_raw[0:300, 50:350]
    face = cv2.resize(img, (128, 128))
    l1.append(face)
    emotion = cv2.imread(f2)
    l2.append(emotion)
    f_l, e_l = np.array(l1), np.array(l2)
    return f_l.astype("float32"), e_l.astype("float32")


def handle_output(img, path):
    cv2.imencode('.jpg', img)[1].tofile(path)


def handle_predict(face, emotion):
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.compat.v1.Session(config=config)
    tf.compat.v1.keras.backend.set_session(sess)
    generator = model.get_generator()
    if os.path.isfile(p.g_model + ".index"):
        generator.load_weights(p.g_model)
    result = generator.predict([face, emotion])
    return np.array(result, dtype=np.uint8)[0]


if __name__ == "__main__":
    file1 = "../data/1/01-0.jpg"
    file2 = "../data/3/05-0.jpg"
    f, e = handle_input(file1, file2)
    r = np.array(handle_predict(f, e), dtype=np.uint8)[0]
    handle_output(r, "test.jpg")
    cv2.imshow("r", r)
    cv2.waitKey(0)
