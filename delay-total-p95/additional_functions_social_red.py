import tensorflow as tf

def normalization(feature, feature_name):
    if feature_name == 'num_threads':
        feature = (feature - 4.36) / 2.72
    elif feature_name == 'num_cores':
        feature = (feature - 4.32) / 2.68
    elif feature_name == 'proc_delay':
        feature = (feature - 254) / 1318
    elif feature_name == 'load':
        feature = (feature - 1213) / 1689
    elif feature_name == 'total_p95_rt':
        feature = tf.math.log(feature)
    return feature


def denormalization(feature, feature_name):
    if feature_name == 'total_p95_rt':
        feature = tf.math.exp(feature)
    return feature
