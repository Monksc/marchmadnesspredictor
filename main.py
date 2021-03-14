import tensorflow as tf
import keras
import numpy as np
import pandas as pd
import make_data as mdata
import bracket

print(tf.version.VERSION)

def makeModel(input_len, output_len):

    model = keras.Sequential([
        keras.layers.Dense(output_len, activation='sigmoid', input_shape=(input_len, )),
        # keras.layers.Dense(64, activation='sigmoid'),
        # keras.layers.Dense(64, activation='sigmoid'),
        # keras.layers.Dense(64, activation='sigmoid'),
        # keras.layers.Dense(output_len, activation='sigmoid'),
    ])
    
    metrics = [
        keras.metrics.TruePositives(name='tp'),
        keras.metrics.FalsePositives(name='fp'),
        keras.metrics.TrueNegatives(name='tn'),
        keras.metrics.FalseNegatives(name='fn'),
        keras.metrics.BinaryAccuracy(name='accuracy'),
        keras.metrics.Precision(name='precision'),
        keras.metrics.Recall(name='recall'),
        keras.metrics.AUC(name='auc'),
    ]
    
    model.compile(
        optimizer=keras.optimizers.Adam(lr=1e-3),
        loss=keras.losses.BinaryCrossentropy(),
        metrics=metrics)


    model.load_weights('saved_model/model1.ckpt')

    return model


def train():
    
    m, training_inputs, training_outputs, testing_inputs, testing_outputs = mdata.getData()
    print('SHAPES')
    print(training_inputs.shape, training_outputs.shape, testing_inputs.shape, testing_outputs.shape)
    model = makeModel(training_inputs.shape[1], training_outputs.shape[1])

    model.fit(training_inputs, training_outputs, batch_size=128, epochs=128, verbose=1)

    results = model.evaluate(testing_inputs, testing_outputs, batch_size=len(testing_inputs), verbose=0)
    for name, value in zip(model.metrics_names, results):
        print(name, ': ', value)

    model.save_weights("saved_model/model1.ckpt")

    return m

def predictGame(m, model):
    def predict(team1, team2):
        inputs = mdata.getInputs(m, 2019, team1, team2)

        return model.predict(inputs)[0][0]

    return predict

def convertTeamToStr(m):
    def convert(teamId):
        if teamId in m.teamid_to_teamname:
            return m.teamid_to_teamname[teamId]
        return teamId + '-unknown'

    return convert

if __name__ == "__main__":

    # m = train()
    m, inputs, outputs, _, _ = mdata.getData()
    model = makeModel(inputs.shape[1], outputs.shape[1])
    b = bracket.Bracket([
        # East
        1181, 1295, 
        1416, 1433, 
        1251, 1280, 
        1439, 1387, 
        1268, 1125, 
        1261, 1463, 
        1278, 1257, 
        1277, 1133, 

        # West
        1211, 1192, 
        1124, 1393, 
        1293, 1266, 
        1199, 1436, 
        1138, 1113, 
        1403, 1297, 
        1196, 1305, 
        1276, 1285, 

        # South
        1438, 1205, 
        1328, 1279, 
        1332, 1458, 
        1414, 1243, 
        1437, 1388, 
        1345, 1330, 
        1234, 1153, 
        1397, 1159, 

        # Midwest
        1314, 1233, 
        1449, 1429, 
        1120, 1308, 
        1242, 1318, 
        1326, 1235, 
        1222, 1209, 
        1459, 1371, 
        1246, 1101, 
    ], predictGame(m, model), convertTeamToStr(m))

    b.playTourne()


