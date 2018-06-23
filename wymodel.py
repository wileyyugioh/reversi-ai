# https://medium.freecodecamp.org/deep-reinforcement-learning-where-to-start-291fb0058c01

from keras.optimizers import SGD
from keras.layers import concatenate, Conv2D, Dense, Dropout, Flatten, Input, Reshape
from keras.models import Model


def baseline_model():
    board_input = Input(batch_shape=(None, 64), name="board_input")
    board_reshape = Reshape((8, 8, 1))(board_input)

    color_input = Input(batch_shape=(None, 1), name="color_input")

    x = Conv2D(32, (2, 2), activation="relu", padding="same")(board_reshape)
    x = Conv2D(64, (2, 2), activation="relu", padding="same")(x)
    x = Flatten()(x)
    x = concatenate([color_input, x])
    x = Dense(1024, activation="relu")(x)
    predictions = Dense(64)(x)

    model = Model(inputs=[board_input, color_input], outputs=[predictions])
    model.compile(SGD(lr=.1), "mse")
    return model
