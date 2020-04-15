from tensorflow import keras
import tensorflow as tf
import ml.parameter as p
import ml.model as model
from random import randint
import numpy as np
import cv2
import os


def prep_train():
    face_idx = randint(1, 24)
    emotion_idx = randint(1, 24)
    while face_idx == emotion_idx:
        emotion_idx = randint(1, 24)

    face_dir = "../data/" + str(face_idx)
    emotion_dir = "../data/" + str(emotion_idx)

    face_list = os.listdir(face_dir)
    emotion_list = os.listdir(emotion_dir)

    fv_idx = "0" + str(randint(1, 8))
    ev_idx = "0" + str(randint(1, 8))

    face_set = list()
    valid_set = list()
    for i_name in face_list:
        if i_name.startswith(fv_idx):
            img = cv2.imread(face_dir + "/" + i_name)
            face_set.append(img)
        if i_name.startswith(ev_idx):
            img = cv2.imread(face_dir + "/" + i_name)
            valid_set.append(img)
    emotion_set = list()
    for i_name in emotion_list:
        if i_name.startswith(ev_idx):
            img = cv2.imread(emotion_dir + "/" + i_name)
            emotion_set.append(img)

    batch_size = np.min((len(face_set), len(emotion_set), len(valid_set)))
    face_set = np.array(face_set[0:batch_size])
    emotion_set = np.array(emotion_set[0:batch_size])
    valid_set = np.array(valid_set[0:batch_size])
    valid_label = np.ones((batch_size,))
    err_set = 0.05 * np.random.random(np.shape(valid_set))
    err_label = np.zeros((batch_size,))
    return face_set, emotion_set, valid_set, valid_label, err_set, err_label, batch_size


if __name__ == "__main__":
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.compat.v1.Session(config=config)
    tf.compat.v1.keras.backend.set_session(sess)

    generator = model.get_generator()
    discriminator = model.get_discriminator()

    if os.path.isfile(p.g_model + ".index"):
        generator.load_weights(p.g_model)
    if os.path.isfile(p.d_model + ".index"):
        discriminator.load_weights(p.d_model)

    discriminator.compile(loss='binary_crossentropy', optimizer=keras.optimizers.Adam(lr=p.d_lr), metrics=['accuracy'])

    for i in range(p.train_times):
        f_s, e_s, valid_s, valid_l, err_s, err_l, b_s = prep_train()
        ipt1 = tf.keras.Input(shape=p.ipt)
        ipt2 = tf.keras.Input(shape=p.ipt)
        result = generator([ipt1, ipt2])
        combine = tf.concat((result, valid_s), 3)
        discriminator.trainable = False
        validity = discriminator(combine)
        gan = keras.Model([ipt1, ipt2], validity)
        gan.compile(loss='binary_crossentropy', optimizer=keras.optimizers.Adam(lr=p.d_lr), metrics=['accuracy'])

        d_loss_real = discriminator.train_on_batch(tf.concat((valid_s, valid_s), 3), valid_l)
        d_loss_err = discriminator.train_on_batch(tf.concat((err_s, valid_s), 3), err_l)
        print(str(d_loss_real) + " " + str(d_loss_err))
        g_loss = gan.train_on_batch([f_s, e_s], valid_l)
        print(g_loss)

        if i % 100 == 0:
            generator.save_weights(p.g_model)
            discriminator.save_weights(p.d_model)

