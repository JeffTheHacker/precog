import logging
import pdb
import tensorflow as tf

import interface
import bijection.esp_bijection as esp_bijection
import utils.tensor_util as tensoru
import utils.log_util as logu
import utils.class_util as classu

log = logging.getLogger(__file__)

class FixedMuFixedIBijection(esp_bijection.ESPJointTrajectoryBijectionMixin, interface.ESPJointTrajectoryBijection):
    @logu.log_wrapi()
    def __init__(self, A):
        self.eye = tf.Variable(initial_value=tf.tile(tf.constant([1., 1.], dtype=tf.float32)[None], (A, 1)), trainable=True)
        self.mu = tf.Variable(initial_value=tf.tile(tf.constant([0., 0.], dtype=tf.float32)[None], (A, 1)), trainable=True)
        # self.eye = tf.Variable(initial_value=tf.eye(batch_shape=(A,), num_rows=2, dtype=tf.float32), trainable=True)
        self._A = A
        
    @property
    def A(self):
        return self._A

    @property
    def variables(self):
        return [self.eye, self.mu]

    def _prepare(self, batch_shape):
        assert(isinstance(batch_shape, tuple))
        self.batch_shape = batch_shape
    
    def __repr__(self):
        return self.__class__.__name__ + "()"

    def get_Itile(self):
        eye = tf.stack([tf.diag(tf.maximum(self.eye[a], 1e-5)) for a in range(self.A)], axis=0)
        for i in range(len(self.batch_shape)):
            eye = tf.expand_dims(eye, 0)
        return tf.tile(eye, self.batch_shape + (1, 1, 1))

    def get_mutile(self):
        mu = self.mu
        for i in range(len(self.batch_shape)):
            mu = tf.expand_dims(mu, 0)
        return tf.tile(mu, self.batch_shape + (1, 1))

    def step_generate(self, S_history, *args, **kwargs):
        """Use m_t=0 and sigma_t=I. For debug purposes.

        :param S_history: 
        :returns: 
        :rtype: 

        """
        m_t = self.get_mutile()
        sigma_t = self.get_Itile()
        return m_t, sigma_t
