from tensorflow import keras
import tensorflow as tf
import ml.parameter as p


def get_generator():
    ipt1 = tf.keras.Input(shape=p.ipt)
    ipt2 = tf.keras.Input(shape=p.ipt)

    cv1 = keras.layers.Conv2D(filters=3, kernel_size=p.c1_l1_kernel, strides=p.c1_l1_stride,
                              activation=tf.nn.relu, padding='SAME')(ipt1)
    cv2 = keras.layers.Conv2D(filters=4, kernel_size=p.c1_l2_kernel, strides=p.c1_l2_stride,
                              activation=tf.nn.relu, padding='SAME')(cv1)
    d1 = keras.layers.Dropout(0.3, noise_shape=None, seed=None)(cv2)
    cv3 = keras.layers.Conv2D(filters=5, kernel_size=p.c1_l3_kernel, strides=p.c1_l3_stride,
                              activation=tf.nn.relu, padding='SAME')(d1)

    cv4 = keras.layers.Conv2D(filters=3, kernel_size=p.c2_l1_kernel, strides=p.c1_l1_stride,
                              activation=tf.nn.relu, padding='SAME')(ipt2)
    cv5 = keras.layers.Conv2D(filters=4, kernel_size=p.c2_l2_kernel, strides=p.c1_l2_stride,
                              activation=tf.nn.relu, padding='SAME')(cv4)
    d2 = keras.layers.Dropout(0.3, noise_shape=None, seed=None)(cv5)
    cv6 = keras.layers.Conv2D(filters=5, kernel_size=p.c2_l3_kernel, strides=p.c1_l3_stride,
                              activation=tf.nn.relu, padding='SAME')(d2)

    mix = tf.concat((cv3, cv6), 3)

    ct1 = keras.layers.Conv2DTranspose(filters=5, kernel_size=p.ct_l1_kernel,
                                       strides=p.ct_l1_stride, activation=tf.nn.relu, padding='SAME')(mix)
    ct2 = keras.layers.Conv2DTranspose(filters=4, kernel_size=p.ct_l2_kernel, strides=p.ct_l2_stride,
                                       activation=tf.nn.relu, padding='SAME')(ct1)
    output = keras.layers.Conv2DTranspose(filters=3, kernel_size=p.ct_l3_kernel, strides=p.ct_l3_stride,
                                          activation=tf.nn.relu, padding='SAME')(ct2)

    model = keras.Model(inputs=[ipt1, ipt2], outputs=output)

    return model


def get_discriminator():
    ipt = tf.keras.Input(shape=p.ipt2)

    cv1 = keras.layers.Conv2D(input_shape=p.ipt, filters=3, kernel_size=p.c3_l1_kernel, strides=p.c3_l1_stride,
                              activation=tf.nn.relu, padding='SAME')(ipt)
    cv2 = keras.layers.Conv2D(filters=4, kernel_size=p.c3_l2_kernel, strides=p.c3_l2_stride, activation=tf.nn.relu,
                              padding='SAME')(cv1)
    d1 = keras.layers.Dropout(0.3, noise_shape=None, seed=None)(cv2)
    cv3 = keras.layers.Conv2D(filters=4, kernel_size=p.c3_l3_kernel, strides=p.c3_l3_stride, activation=tf.nn.relu,
                              padding='SAME')(d1)
    cv4 = keras.layers.Conv2D(filters=5, kernel_size=p.c3_l4_kernel, strides=p.c3_l4_stride, activation=tf.nn.relu,
                              padding='SAME')(cv3)
    d2 = keras.layers.Dropout(0.3, noise_shape=None, seed=None)(cv4)
    cv5 = keras.layers.Conv2D(filters=5, kernel_size=p.c3_l5_kernel, strides=p.c3_l5_stride, activation=tf.nn.relu,
                              padding='SAME')(d2)
    fc = keras.layers.Flatten()(cv5)
    ds = keras.layers.Dense(10, activation=tf.nn.softmax)(fc)
    output = keras.layers.Dense(1, activation=tf.nn.sigmoid)(ds)

    model = keras.Model(inputs=ipt, outputs=output)

    return model
