from builtins import range
from builtins import object
import numpy as np

from cs231n.layers import *
from cs231n.layer_utils import *


class TwoLayerNet(object):
    """
    A two-layer fully-connected neural network with ReLU nonlinearity and
    softmax loss that uses a modular layer design. We assume an input dimension
    of D, a hidden dimension of H, and perform classification over C classes.

    The architecure should be affine - relu - affine - softmax.

    Note that this class does not implement gradient descent; instead, it
    will interact with a separate Solver object that is responsible for running
    optimization.

    The learnable parameters of the model are stored in the dictionary
    self.params that maps parameter names to numpy arrays.
    """

    def __init__(self, input_dim=3*32*32, hidden_dim=100, num_classes=10,
                 weight_scale=1e-3, reg=0.0):
        """
        Initialize a new network.

        D = 3072
        H = 100
        C = 10

        Inputs:
        - input_dim: An integer giving the size of the input
        - hidden_dim: An integer giving the size of the hidden layer
        - num_classes: An integer giving the number of classes to classify
        - dropout: Scalar between 0 and 1 giving dropout strength.
        - weight_scale: Scalar giving the standard deviation for random
          initialization of the weights.
        - reg: Scalar giving L2 regularization strength.
        """
        self.params = {}
        self.reg = reg

        # Added in by Seankala. You need this if you want to use affine_backward.
        self.cache = {}

        ############################################################################
        # TO-DO: Initialize the weights and biases of the two-layer net. Weights    #
        # should be initialized from a Gaussian with standard deviation equal to   #
        # weight_scale, and biases should be initialized to zero. All weights and  #
        # biases should be stored in the dictionary self.params, with first layer  #
        # weights and biases using the keys 'W1' and 'b1' and second layer weights #
        # and biases using the keys 'W2' and 'b2'.                                 #
        ############################################################################
        
        # W1 -> (D, H)
        # b1 -> (H,)
        # W2 -> (H, C)
        # b2 -> (C,)

        D = input_dim
        H = hidden_dim
        C = num_classes

        # The mean of the Normal distribution was not specified, so we assume they are
        #   zero-centered.
        # loc -> mean, scale -> standard deviation. Check the documentation for more info.
        W1 = np.random.normal(loc=0.0, scale=weight_scale, size=(D, H))
        b1 = np.zeros(shape=(H,))
        W2 = np.random.normal(loc=0.0, scale=weight_scale, size=(H, C))
        b2 = np.zeros(shape=(C,))

        self.params['W1'] = W1
        self.params['b1'] = b1
        self.params['W2'] = W2
        self.params['b2'] = b2

        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################


    def loss(self, X, y=None):
        """
        Compute loss and gradient for a minibatch of data.

        Inputs:
        - X: Array of input data of shape (N, d_1, ..., d_k)
        - y: Array of labels, of shape (N,). y[i] gives the label for X[i].

        Returns:
        If y is None, then run a test-time forward pass of the model and return:
        - scores: Array of shape (N, C) giving classification scores, where
          scores[i, c] is the classification score for X[i] and class c.

        If y is not None, then run a training-time forward and backward pass and
        return a tuple of:
        - loss: Scalar value giving the loss
        - grads: Dictionary with the same keys as self.params, mapping parameter
          names to gradients of the loss with respect to those parameters.
        """
        scores = None
        ############################################################################
        # TO-DO: Implement the forward pass for the two-layer net, computing the    #
        # class scores for X and storing them in the scores variable.              #
        ############################################################################

        # X -> (N, D)
        # W1 -> (D, H)
        # b1 -> (H,)
        # W2 -> (H, C)
        # b2 -> (C,)

        N = X.shape[0]
        W1 = self.params['W1']
        b1 = self.params['b1']
        W2 = self.params['W2']
        b2 = self.params['b2']

        # Compute forward pass through network.

        ################## Method 1: Compute the old-fashioned way. ################
        #X = np.reshape(X, (N, -1))
        #H0 = np.matmul(X, W1) # (N, D) x (D, H) = (N, H)
        #H1 = H0 + b1 # (N, H) + (H,) = (N, H)
        #H2 = np.matmul(H1, W2) # (N, H) x (H, C) = (N, C)
        #Z = H2 + b2 # (N, C) + (C,) = (N, C)
        #
        #scores = Z
        ############################################################################

        ################## Method 2: Compute using the given functions. ############
        H1, self.cache['H1'] = affine_forward(X, W1, b1)
        Z, self.cache['Z'] = affine_forward(H1, W2, b2)

        scores = Z
        ############################################################################

        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # If y is None then we are in test mode so just return scores
        if y is None:
            return scores

        loss, grads = 0, {}
        ############################################################################
        # TO-DO: Implement the backward pass for the two-layer net. Store the loss  #
        # in the loss variable and gradients in the grads dictionary. Compute data #
        # loss using softmax, and make sure that grads[k] holds the gradients for  #
        # self.params[k]. Don't forget to add L2 regularization!                   #
        #                                                                          #
        # NOTE: To ensure that your implementation matches ours and you pass the   #
        # automated tests, make sure that your L2 regularization includes a factor #
        # of 0.5 to simplify the expression for the gradient.                      #
        ############################################################################
        
        # Compute loss and add regularization.
        # If you look at the last few lines of softmax_loss, you'll know why dZ is
        #   computed using that function.
        loss, dZ = softmax_loss(scores, y)

        reg_term_W1 = 0.5 * self.reg * np.sum(W1 * W1)
        reg_term_W2 = 0.5 * self.reg * np.sum(W2 * W2)
        
        loss += reg_term_W1 + reg_term_W2


        ################## Method 1: Compute the old-fashioned way. ################
        #db2 = np.sum(dZ, axis=0) # (C,)
        #dH2 = dZ # (N, C)
        #dW2 = np.matmul(H1.T, dH2) # (H, N) x (N, C) = (H, C)
        #dH1 = np.matmul(dH2, W2.T) # (N, C) x (C, H) = (N, H)
        #db1 = np.sum(dH1, axis=0) # (H,)
        #dH0 = dH1 # (N, H)
        #dW1 = np.matmul(X.T, dH0) # (D, N) x (N, H) = (D, H)
        #dX = np.matmul(dH0, W1.T) # (N, H) x (H, D) = (N, D)
        ############################################################################

        ################## Method 2: Compute using the given functions. ############
        dH2, dW2, db2 = affine_backward(dZ, self.cache['Z'])
        dH1, dW1, db1 = affine_backward(dH2, self.cache['H1'])
        ############################################################################

        # Store gradients.
        grads['W1'] = dW1
        grads['b1'] = db1
        grads['W2'] = dW2
        grads['b2'] = db2

        # Perform regularization.
        grads['W1'] += self.reg * W1
        grads['W2'] += self.reg * W2

        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads


class FullyConnectedNet(object):
    """
    A fully-connected neural network with an arbitrary number of hidden layers,
    ReLU nonlinearities, and a softmax loss function. This will also implement
    dropout and batch normalization as options. For a network with L layers,
    the architecture will be

    {affine - [batch norm] - relu - [dropout]} x (L - 1) - affine - softmax

    where batch normalization and dropout are optional, and the {...} block is
    repeated L - 1 times.

    Similar to the TwoLayerNet above, learnable parameters are stored in the
    self.params dictionary and will be learned using the Solver class.
    """

    def __init__(self, hidden_dims, input_dim=3*32*32, num_classes=10,
                 dropout=0, use_batchnorm=False, reg=0.0,
                 weight_scale=1e-2, dtype=np.float32, seed=None):
        """
        Initialize a new FullyConnectedNet.

        Inputs:
        - hidden_dims: A list of integers giving the size of each hidden layer.
        - input_dim: An integer giving the size of the input.
        - num_classes: An integer giving the number of classes to classify.
        - dropout: Scalar between 0 and 1 giving dropout strength. If dropout=0 then
          the network should not use dropout at all.
        - use_batchnorm: Whether or not the network should use batch normalization.
        - reg: Scalar giving L2 regularization strength.
        - weight_scale: Scalar giving the standard deviation for random
          initialization of the weights.
        - dtype: A numpy datatype object; all computations will be performed using
          this datatype. float32 is faster but less accurate, so you should use
          float64 for numeric gradient checking.
        - seed: If not None, then pass this random seed to the dropout layers. This
          will make the dropout layers deteriminstic so we can gradient check the
          model.
        """
        self.use_batchnorm = use_batchnorm
        self.use_dropout = dropout > 0
        self.reg = reg
        self.num_layers = 1 + len(hidden_dims)
        self.dtype = dtype
        self.params = {}

        self.fc_cache = {} # Added in by Seankala.
        self.relu_cache = {} # Added in by Seankala.
        self.bn_cache = {} # Added in by Seankala.
        self.dropout_cache = {} # Added in by Seankala.

        ############################################################################
        # TO-DO: Initialize the parameters of the network, storing all values in    #
        # the self.params dictionary. Store weights and biases for the first layer #
        # in W1 and b1; for the second layer use W2 and b2, etc. Weights should be #
        # initialized from a normal distribution with standard deviation equal to  #
        # weight_scale and biases should be initialized to zero.                   #
        #                                                                          #
        # When using batch normalization, store scale and shift parameters for the #
        # first layer in gamma1 and beta1; for the second layer use gamma2 and     #
        # beta2, etc. Scale parameters should be initialized to one and shift      #
        # parameters should be initialized to zero.                                #
        ############################################################################

        D = input_dim
        C = num_classes

        for i in range(self.num_layers - 1):
            if i == 0: # Initialization for first layer.
                H = hidden_dims[i]
                W_curr = np.random.normal(loc=0.0, scale=weight_scale, size=(D, H))
                b_curr = np.zeros(shape=(H,))
                self.params['W{}'.format(i + 1)] = W_curr
                self.params['b{}'.format(i + 1)] = b_curr

                if self.use_batchnorm:
                    self.bn_cache['gamma{}'.format(i + 1)] = np.ones(shape=(H,))
                    self.bn_cache['beta{}'.format(i + 1)] = np.zeros(shape=(H,))

                next_dim = H
            else: # Initialization for intermediate layers.
                H = hidden_dims[i]
                W_curr = np.random.normal(loc=0.0, scale=weight_scale, size=(next_dim, H))
                b_curr = np.zeros(shape=(H,))
                self.params['W{}'.format(i + 1)] = W_curr
                self.params['b{}'.format(i + 1)] = b_curr

                if self.use_batchnorm:
                    self.bn_cache['gamma{}'.format(i + 1)] = np.ones(shape=(H,))
                    self.bn_cache['beta{}'.format(i + 1)] = np.ones(shape=(H,))

                next_dim = H

        # Initialization for last layer.
        W_last = np.random.normal(loc=0.0, scale=weight_scale, size=(next_dim, C))
        b_last = np.zeros(shape=(C,))
        self.params['W{}'.format(self.num_layers)] = W_last
        self.params['b{}'.format(self.num_layers)] = b_last

        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # When using dropout we need to pass a dropout_param dictionary to each
        # dropout layer so that the layer knows the dropout probability and the mode
        # (train / test). You can pass the same dropout_param to each dropout layer.
        self.dropout_param = {}
        if self.use_dropout:
            self.dropout_param = {'mode': 'train', 'p': dropout}
            if seed is not None:
                self.dropout_param['seed'] = seed

        # With batch normalization we need to keep track of running means and
        # variances, so we need to pass a special bn_param object to each batch
        # normalization layer. You should pass self.bn_params[0] to the forward pass
        # of the first batch normalization layer, self.bn_params[1] to the forward
        # pass of the second batch normalization layer, etc.
        self.bn_params = []
        if self.use_batchnorm:
            self.bn_params = [{'mode': 'train'} for i in range(self.num_layers - 1)]

        # Cast all parameters to the correct datatype
        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)


    def loss(self, X, y=None):
        """
        Compute loss and gradient for the fully-connected net.

        Input / output: Same as TwoLayerNet above.
        """
        X = X.astype(self.dtype)
        mode = 'test' if y is None else 'train'

        # Set train/test mode for batchnorm params and dropout param since they
        # behave differently during training and testing.
        if self.use_dropout:
            self.dropout_param['mode'] = mode
        if self.use_batchnorm:
            for bn_param in self.bn_params:
                bn_param['mode'] = mode

        scores = None
        ############################################################################
        # TO-DO: Implement the forward pass for the fully-connected net, computing  #
        # the class scores for X and storing them in the scores variable.          #
        #                                                                          #
        # When using dropout, you'll need to pass self.dropout_param to each       #
        # dropout forward pass.                                                    #
        #                                                                          #
        # When using batch normalization, you'll need to pass self.bn_params[0] to #
        # the forward pass for the first batch normalization layer, pass           #
        # self.bn_params[1] to the forward pass for the second batch normalization #
        # layer, etc.                                                              #
        ############################################################################

        for i in range(self.num_layers - 1):
            W_curr = self.params['W{}'.format(i + 1)]
            b_curr = self.params['b{}'.format(i + 1)]

            # These two functions are one pass. We repeat this (L - 1) times.
            hidden_out, self.fc_cache['l{}'.format(i + 1)] = affine_forward(X, W_curr, b_curr)

            # Add in batch normalization before the ReLU nonlinearity.
            if self.use_batchnorm:
                gamma = self.bn_cache['gamma{}'.format(i + 1)]
                beta = self.bn_cache['gamma{}'.format(i + 1)]
                hidden_out, self.bn_cache['l{}'.format(i + 1)] = batchnorm_forward(hidden_out, gamma, beta, self.bn_params[i])

            relu_out, self.relu_cache['l{}'.format(i + 1)] = relu_forward(hidden_out)

            if self.use_dropout:
                relu_out, self.dropout_cache['l{}'.format(i + 1)] = dropout_forward(relu_out, self.dropout_param)

            # Copy the new X to use in the next iteration.
            X = relu_out.copy()
        # After looping through the affine-ReLU blocks (L - 1) times, compute the scores for the output.
        W_last = self.params['W{}'.format(self.num_layers)]
        b_last = self.params['b{}'.format(self.num_layers)]
        scores, self.fc_cache['last'] = affine_forward(X, W_last, b_last)

        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # If test mode return early
        if mode == 'test':
            return scores

        loss, grads = 0.0, {}
        ############################################################################
        # TO-DO: Implement the backward pass for the fully-connected net. Store the #
        # loss in the loss variable and gradients in the grads dictionary. Compute #
        # data loss using softmax, and make sure that grads[k] holds the gradients #
        # for self.params[k]. Don't forget to add L2 regularization!               #
        #                                                                          #
        # When using batch normalization, you don't need to regularize the scale   #
        # and shift parameters.                                                    #
        #                                                                          #
        # NOTE: To ensure that your implementation matches ours and you pass the   #
        # automated tests, make sure that your L2 regularization includes a factor #
        # of 0.5 to simplify the expression for the gradient.                      #
        ############################################################################

        # I initially had a 0.5 term being multiplied to (self.reg * W_curr) when storing
        #   the gradients. This was causing the subsequent gradients to have high relative
        #   error. Adding in the 0.5 term once in the loss is enough.

        # Compute loss, output gradient, and L2 regularization.
        loss, dZ = softmax_loss(scores, y)

        for i in range(self.num_layers, 0, -1):
            W_curr = self.params['W{}'.format(i)]
            b_curr = self.params['b{}'.format(i)]
            reg_term = 0.5 * self.reg * np.sum(W_curr * W_curr)
            loss += reg_term

            if i == self.num_layers: # Last output layer.
                dX, dW, db = affine_backward(dZ, self.fc_cache['last'])
                grads['W{}'.format(i)] = dW + (self.reg * W_curr)
                grads['b{}'.format(i)] = db
            else:
                if self.use_dropout:
                    dX = dropout_backward(dX, self.dropout_cache['l{}'.format(i)])

                dReLU = relu_backward(dX, self.relu_cache['l{}'.format(i)])

                if self.use_batchnorm:
                    bn_cache = self.bn_cache['l{}'.format(i)]
                    dReLU, _, _ = batchnorm_backward(dReLU, bn_cache)

                dX, dW, db = affine_backward(dReLU, self.fc_cache['l{}'.format(i)])
                grads['W{}'.format(i)] = dW + (self.reg * W_curr)
                grads['b{}'.format(i)] = db

        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads
