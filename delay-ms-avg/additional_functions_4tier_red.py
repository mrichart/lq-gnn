import tensorflow as tf

def normalization(feature, feature_name):
    if feature_name == 'num_threads':
        feature = (feature - 2.69) / 1.69
    elif feature_name == 'num_cores':
        feature = (feature - 1.91) / 1.48
    elif feature_name == 'proc_delay':
        feature = (feature - 233) / 997
    elif feature_name == 'load':
        feature = (feature - 1774) / 2610
    elif feature_name == 'ms_avg_rt':
        feature = tf.math.log(feature)
    return feature


def denormalization(feature, feature_name):
    if feature_name == 'ms_avg_rt':
        feature = tf.math.exp(feature)
    return feature
