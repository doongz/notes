# Tensor

ref: https://www.guru99.com/tensor-tensorflow.html#3

## What is a Tensor?

Tensorflow’s name is directly derived from its core framework: Tensor. In Tensorflow, all the computations involve tensors. A tensor is a vector or matrix of n-dimensions that represents all types of data. All values in a tensor hold identical data type with a known (or partially known) shape. The shape of the data is the dimensionality of the matrix or array.

A tensor can be originated from the input data or the result of a computation. In TensorFlow, all the operations are conducted inside a graph. The graph is a set of computation that takes place successively. Each operation is called an op node and are connected to each other.

The graph outlines the ops and connections between the nodes. However, it does not display the values. The edge of the nodes is the tensor, i.e., a way to populate the operation with data.

In Machine Learning, models are feed with a list of objects called feature vectors. A feature vector can be of any data type. The feature vector will usually be the primary input to populate a tensor. These values will flow into an op node through the tensor and the result of this operation/computation will create a new tensor which in turn will be used in a new operation. All these operations can be viewed in the graph.

## Representation of a Tensor

In TensorFlow, a tensor is a collection of feature vectors (i.e., array) of n-dimensions. For instance, if we have a 2×3 matrix with values from 1 to 6, we write:

![Representation of a Tensor](../imgs/080418_1250_WhatisaTens111.png)

Representation of a Tensor

TensorFlow represents this matrix as:

```
[[1, 2, 3], 
   [4, 5, 6]]
```

If we create a three-dimensional matrix with values from 1 to 8, we have:

![img](../imgs/080418_1250_WhatisaTens2.png)

TensorFlow represents this matrix as:

```
[ [[1, 2],  
       [[3, 4],  
       [[5, 6],  
       [[7,8] ]
```

**Note:** A tensor can be represented with a scalar or can have a shape of more than three dimensions. It is just more complicated to visualize higher dimension level.

## Types of Tensor

In TensorFlow, all the computations pass through one or more tensors. A tf.tensor is an object with three properties:

- A unique label (name)
- A dimension (shape)
- A data type (dtype)

Each operation you will do with TensorFlow involves the manipulation of a tensor. There are four main tensor type you can create:

- tf.Variable
- tf.constant
- tf.placeholder
- tf.SparseTensor

In this tutorial, you will learn how to create a tf.constant and a tf.Variable.

Before we go through the tutorial, make sure you activate the conda environment with TensorFlow. We named this environment hello-tf.

**For MacOS user:**

```
source activate hello-tf
```

**For Windows user:**

```
activate hello-tf
```

After you have done that, you are ready to import tensorflow

```
# Import tf
import tensorflow as tf
```

## Create a tensor of n-dimension

You begin with the creation of a tensor with one dimension, namely a scalar.

To create a tensor, you can use tf.constant() as shown in the below TensorFlow tensor shape example:

```
tf.constant(value, dtype, name = "")
arguments

- `value`: Value of n dimension to define the tensor. Optional
- `dtype`: Define the type of data:    
    - `tf.string`: String variable    
    - `tf.float32`: Float variable    
    - `tf.int16`: Integer variable
- "name": Name of the tensor. Optional. By default, `Const_1:0`
```

To create a tensor of dimension 0, run the following code

```
## rank 0
# Default name
r1 = tf.constant(1, tf.int16) 
print(r1)			
```

**Output**

```
Tensor("Const:0", shape=(), dtype=int16)
```

![Example of Creating a tensor of n-dimension](../imgs/080418_1250_WhatisaTens3.png)

```
# Named my_scalar
r2 = tf.constant(1, tf.int16, name = "my_scalar") 
print(r2)
```

**Output**

```
Tensor("my_scalar:0", shape=(), dtype=int16)
```

Each tensor is displayed by the tensor name. Each tensor object is defined with tensor attributes like a unique label (name), a dimension (shape) and TensorFlow data types (dtype).

You can define a tensor with decimal values or with a string by changing the type of data.

```
# Decimal
r1_decimal = tf.constant(1.12345, tf.float32)
print(r1_decimal)
# String
r1_string = tf.constant("Guru99", tf.string)
print(r1_string)
```

**Output**

```
Tensor("Const_1:0", shape=(), dtype=float32)
Tensor("Const_2:0", shape=(), dtype=string)
```

A tensor of dimension 1 can be created as follow:

```
## Rank 1r1_vector = tf.constant([1,3,5], tf.int16)
print(r1_vector)
r2_boolean = tf.constant([True, True, False], tf.bool)
print(r2_boolean)
```

**Output**

```
Tensor("Const_3:0", shape=(3,), dtype=int16)
Tensor("Const_4:0", shape=(3,), dtype=bool)
```

You can notice the TensorFlow shape is only composed of 1 column.

To create an array of 2 tensor dimensions, you need to close the brackets after each row. Check the Keras Tensor shape example below

```
## Rank 2
r2_matrix = tf.constant([ [1, 2],
                          [3, 4] ],tf.int16)
print(r2_matrix)
```

**Output**

```
Tensor("Const_5:0", shape=(2, 2), dtype=int16)
```

The matrix has 2 rows and 2 columns filled with values 1, 2, 3, 4.

A matrix with 3 dimensions is constructed by adding another level with the brackets.

```
## Rank 3
r3_matrix = tf.constant([ [[1, 2],
                           [3, 4], 
                           [5, 6]] ], tf.int16)
print(r3_matrix)
```

**Output**

```
Tensor("Const_6:0", shape=(1, 3, 2), dtype=int16)
```

The matrix looks like the picture two.

## Shape of tensor

When you print tensor, TensorFlow guesses the shape. However, you can get the shape of the tensor with the TensorFlow shape property.

Below, you construct a matrix filled with a number from 10 to 15 and you check the shape of m_shape

```
# Shape of tensor
m_shape = tf.constant([ [10, 11],
                        [12, 13],
                        [14, 15] ]                      
                     ) 
m_shape.shape
```

**Output**

```
TensorShape([Dimension(3), Dimension(2)])
```

The matrix has 3 rows and 2 columns.

TensorFlow has useful commands to create a vector or a matrix filled with 0 or 1. For instance, if you want to create a 1-D tensor with a specific shape of 10, filled with 0, you can run the code below:

```
# Create a vector of 0
print(tf.zeros(10))
```

**Output**

```
Tensor("zeros:0", shape=(10,), dtype=float32)
```

The property works for matrix as well. Here, you create a 10×10 matrix filled with 1

```
# Create a vector of 1
print(tf.ones([10, 10]))
```

**Output**

```
Tensor("ones:0", shape=(10, 10), dtype=float32)
```

You can use the shape of a given matrix to make a vector of ones. The matrix m_shape is a 3×2 dimensions. You can create a tensor with 3 rows filled by one’s with the following code:

```
# Create a vector of ones with the same number of rows as m_shape
print(tf.ones(m_shape.shape[0]))
```

**Output**

```
Tensor("ones_1:0", shape=(3,), dtype=float32)
```

If you pass the value 1 into the bracket, you can construct a vector of ones equals to the number of columns in the matrix m_shape.

```
# Create a vector of ones with the same number of column as m_shape
print(tf.ones(m_shape.shape[1]))
```

**Output**

```
Tensor("ones_2:0", shape=(2,), dtype=float32)
```

Finally, you can create a matrix 3×2 with only one’s

```
print(tf.ones(m_shape.shape))
```

**Output**

```
Tensor("ones_3:0", shape=(3, 2), dtype=float32)
```

## Type of data

The second property of a tensor is the type of data. A tensor can only have one type of data at a time. A tensor can only have one type of data. You can return the type with the property dtype.

```
print(m_shape.dtype)
```

**Output**

```
<dtype: 'int32'>
```

In some occasions, you want to change the type of data. In TensorFlow, it is possible with tf.cast method.

**Example**

Below, a float tensor is converted to integer using you use the method cast.

```
# Change type of data
type_float = tf.constant(3.123456789, tf.float32)
type_int = tf.cast(type_float, dtype=tf.int32)
print(type_float.dtype)
print(type_int.dtype)
```

**Output**

```
<dtype: 'float32'>
<dtype: 'int32'>
```

TensorFlow chooses the type of data automatically when the argument is not specified during the creation of the tensor. TensorFlow will guess what is the most likely types of data. For instance, if you pass a text, it will guess it is a string and convert it to string.

## Creating operator

### Some Useful TensorFlow operators

You know how to create a tensor with TensorFlow. It is time to learn how to perform mathematical operations.

TensorFlow contains all the basic operations. You can begin with a simple one. You will use TensorFlow method to compute the square of a number. This operation is straightforward because only one argument is required to construct the tensor.

The square of a number is constructed with tf.sqrt(x) with x as a floating number.

```
x = tf.constant([2.0], dtype = tf.float32)
print(tf.sqrt(x))
```

**Output**

```
Tensor("Sqrt:0", shape=(1,), dtype=float32)
```

**Note:** The output returned a tensor object and not the result of the square of 2. In the example, you print the definition of the tensor and not the actual evaluation of the operation. In the next section, you will learn how TensorFlow works to execute the operations.

Following is a list of commonly used operations. The idea is the same. Each operation requires one or more arguments.

- tf.add(a, b)
- tf.substract(a, b)
- tf.multiply(a, b)
- tf.div(a, b)
- tf.pow(a, b)
- tf.exp(a)
- tf.sqrt(a)

**Example**

```
# Add
tensor_a = tf.constant([[1,2]], dtype = tf.int32)
tensor_b = tf.constant([[3, 4]], dtype = tf.int32)

tensor_add = tf.add(tensor_a, tensor_b)print(tensor_add)
```

**Output**

```
Tensor("Add:0", shape=(1, 2), dtype=int32)
```

Code Explanation

Create two tensors:

- one tensor with 1 and 2
- one tensor with 3 and 4

You add up both tensors.

**Notice**: that both tensors need to have the same shape. You can execute a multiplication over the two tensors.

```
# Multiply
tensor_multiply = tf.multiply(tensor_a, tensor_b)
print(tensor_multiply)
```

**Output**

```
Tensor("Mul:0", shape=(1, 2), dtype=int32)
```

## Variables

So far, you have only created constant tensors. It is not of great use. Data always arrive with different values, to capture this, you can use the Variable class. It will represent a node where the values always change.

To create a variable, you can use tf.get_variable() method

```
tf.get_variable(name = "", values, dtype, initializer)
argument
- `name = ""`: Name of the variable
- `values`: Dimension of the tensor
- `dtype`: Type of data. Optional
- `initializer`: How to initialize the tensor. Optional
If initializer is specified, there is no need to include the `values` as the shape of `initializer` is used.
```

For instance, the code below creates a two-dimensional variable with two random values. By default, TensorFlow returns a random value. You name the variable var

```
# Create a Variable
## Create 2 Randomized values
var = tf.get_variable("var", [1, 2])
print(var.shape)
```

**Output**

```
(1, 2)
```

In the second example, you create a variable with one row and two columns. You need to use [1,2] to create the dimension of the variable

The initials values of this tensor are zero. For instance, when you train a model, you need to have initial values to compute the weight of the features. Below, you set these initial value to zero.

```
var_init_1 = tf.get_variable("var_init_1", [1, 2], dtype=tf.int32,  initializer=tf.zeros_initializer)
print(var_init_1.shape)
```

**Output**

```
(1, 2)
```

You can pass the values of a constant tensor in a variable. You create a constant tensor with the method tf.constant(). You use this tensor to initialize the variable.

The first values of the variable are 10, 20, 30 and 40. The new tensor will have a shape of 2×2.

```
# Create a 2x2 matrixtensor_const = tf.constant([[10, 20],
[30, 40]])
# Initialize the first value of the tensor equals to tensor_const
var_init_2 = tf.get_variable("var_init_2", dtype=tf.int32,  initializer=tensor_const)
print(var_init_2.shape)
```

**Output**

```
(2, 2)
```

## Placeholder

A placeholder has the purpose of feeding the tensor. Placeholder is used to initialize the data to flow inside the tensors. To supply a placeholder, you need to use the method feed_dict. The placeholder will be fed only within a session.

In the next example, you will see how to create a placeholder with the method tf.placeholder. In the next session, you will learn to fed a placeholder with actual tensor value.

The syntax is:

```
tf.placeholder(dtype,shape=None,name=None )
arguments:
- `dtype`: Type of data
- `shape`: dimension of the placeholder. Optional. By default, shape of the data
- `name`: Name of the placeholder. Optional			
data_placeholder_a = tf.placeholder(tf.float32, name = "data_placeholder_a")
print(data_placeholder_a)
```

**Output**

```
Tensor("data_placeholder_a:0", dtype=float32)
```

## Session

TensorFlow works around 3 main components:

- **Graph**
- **Tensor**
- **Session**

| Components | Descritption                                                 |
| ---------- | ------------------------------------------------------------ |
| Graph      | The graph is fundamental in TensorFlow. All of the mathematical operations (ops) are performed inside a graph. You can imagine a graph as a project where every operations are done. The nodes represent these ops, they can absorb or create new tensors. |
| Tensor     | A tensor represents the data that progress between operations. You saw previously how to initialize a tensor. The difference between a constant and variable is the initial values of a variable will change over time. |
| Session    | A session will execute the operation from the graph. To feed the graph with the values of a tensor, you need to open a session. Inside a session, you must run an operator to create an output. |

Graphs and sessions are independent. You can run a session and get the values to use later for further computations.

In the example below, you will:

- Create two tensors
- Create an operation
- Open a session
- Print the result

**Step 1)** You create two tensors x and y

```
## Create, run  and evaluate a session
x = tf.constant([2])
y = tf.constant([4])
```

**Step 2)** You create the operator by multiplying x and y

```
## Create operator
multiply = tf.multiply(x, y)
```

**Step 3)** You open a session. All the computations will happen within the session. When you are done, you need to close the session.

```
## Create a session to run the code
sess = tf.Session()result_1 = sess.run(multiply)
print(result_1)
sess.close()
```

**Output**

```
[8]
```

Code explanation

- tf.Session(): Open a session. All the operations will flow within the sessions
- run(multiply): execute the operation created in step 2.
- print(result_1): Finally, you can print the result
- close(): Close the session

The result shows 8, which is the multiplication of x and y.

Another way to create a session is inside a block. The advantage is it automatically closes the session.

```
with tf.Session() as sess:    
result_2 = multiply.eval()
print(result_2)
```

**Output**

```
[8]
```

In a context of the session, you can use the eval() method to execute the operation. It is equivalent to run(). It makes the code more readable.

You can create a session and see the values inside the tensors you created so far.

```
## Check the tensors created before
sess = tf.Session()
print(sess.run(r1))
print(sess.run(r2_matrix))
print(sess.run(r3_matrix))
```

**Output**

```
1
[[1 2] 
 [3 4]]
[[[1 2]  
  [3 4]  
  [5 6]]]
```

Variables are empty by default, even after you create a tensor. You need to initialize the variable if you want to use the variable. The object tf.global_variables_initializer() needs to be called to initialize the values of a variable. This object will explicitly initialize all the variables. This is helpful before you train a model.

You can check the values of the variables you created before. Note that you need to use run to evaluate the tensor

```
sess.run(tf.global_variables_initializer())
print(sess.run(var))
print(sess.run(var_init_1))
print(sess.run(var_init_2))
```

**Output**

```
[[-0.05356491  0.75867283]]
[[0 0]]
[[10 20] 
 [30 40]]
```

You can use the placeholder you created before and feed it with actual value. You need to pass the data into the method feed_dict.

For example, you will take the power of 2 of the placeholder data_placeholder_a.

```
import numpy as np
power_a = tf.pow(data_placeholder_a, 2)
with tf.Session() as sess:  
data = np.random.rand(1, 10)  
print(sess.run(power_a, feed_dict={data_placeholder_a: data}))  # Will succeed.
```

Code Explanation

- import numpy as np: Import numpy library to create the data
- tf.pow(data_placeholder_a, 2): Create the ops
- np.random.rand(1, 10): Create a random array of data
- feed_dict={data_placeholder_a: data}: Feed the placeholder with data

**Output**

```
[[0.05478134 0.27213147 0.8803037  0.0398424  0.21172127 0.01444725  0.02584014 0.3763949  0.66022706 0.7565559 ]]
```

## Graph

TensorFlow depends on a genius approach to render the operation. All the computations are represented with a dataflow scheme. The dataflow graph has been developed to see to data dependencies between individual operation. Mathematical formula or algorithm are made of a number of successive operations. A graph is a convenient way to visualize how the computations are coordinated.

The graph shows a **node** and an **edge**. The node is the representation of a operation, i.e. the unit of computation. The edge is the tensor, it can produce a new tensor or consume the input data. It depends on the dependencies between individual operation.

The structure of the graph connects together the operations (i.e. the nodes) and how those are operation are feed. Note that the graph does not display the output of the operations, it only helps to visualize the connection between individual operations.

Let’s see an example.

Imagine you want to evaluate the following function:

![img](https://www.guru99.com/images/1/080418_1250_WhatisaTens41.jpg)

TensorFlow will create a graph to execute the function. The graph looks like this:



![TensorFlow Graph example](../imgs/080418_1250_WhatisaTens4.png)

TensorFlow Graph example





You can easily see the path that the tensors will take to reach the final destination.

For instance, you can see the operation add cannot be done before and . The graph explains that it will:

1. compute and :
2. add 1) together
3. add to 2)
4. add 3) to

```
x = tf.get_variable("x", dtype=tf.int32,  initializer=tf.constant([5]))
z = tf.get_variable("z", dtype=tf.int32,  initializer=tf.constant([6]))
c = tf.constant([5], name =	"constant")square = tf.constant([2], name =	"square")
f = tf.multiply(x, z) + tf.pow(x, square) + z + c
```

Code Explanation

- x: Initialize a variable called x with a constant value of 5
- z: Initialize a variable called z with a constant value of 6
- c: Initialize a constant tensor called c with a constant value of 5
- square: Initialize a constant tensor called square with a constant value of 2
- f: Construct the operator

In this example, we choose to keep the values of the variables fixed. We also created a constant tensor called c which is the constant parameter in the function f. It takes a fixed value of 5. In the graph, you can see this parameter in the tensor called constant.

We also constructed a constant tensor for the power in the operator tf.pow(). It is not necessary. We did it so that you can see the name of the tensor in the graph. It is the circle called square.

From the graph, you can understand what will happen of the tensors and how it can return an output of 66.

The code below evaluate the function in a session.

```
init = tf.global_variables_initializer() # prepare to initialize all variables
with tf.Session() as sess:    
	init.run() # Initialize x and y    
    function_result = f.eval()
print(function_result)
```

**Output**

```
[66]
```

## Summary

TensorFlow works around:

- **Graph**: Computational environment containing the operations and tensors
- **Tensors**: Represents the data (or value) that will flow in the graph. It is the edge in the graph
- **Sessions**: Allow the execution of the operations

Create a constant tensor

| constant | object                                             |
| -------- | -------------------------------------------------- |
| D0       | tf.constant(1, tf.int16)                           |
| D1       | tf.constant([1,3,5], tf.int16)                     |
| D2       | tf.constant([ [1, 2], [3, 4] ],tf.int16)           |
| D3       | tf.constant([ [[1, 2],[3, 4], [5, 6]] ], tf.int16) |

Create an operator

| Create an operator | Object            |
| ------------------ | ----------------- |
| a+b                | tf.add(a, b)      |
| a*b                | tf.multiply(a, b) |

Create a variable tensor

| Create a variable       | object                                                       |
| ----------------------- | ------------------------------------------------------------ |
| randomized value        | tf.get_variable(“var”, [1, 2])                               |
| initialized first value | tf.get_variable(“var_init_2”, dtype=tf.int32, initializer=[ [1, 2], [3, 4] ]) |

Open a session

| Session           | object                     |
| ----------------- | -------------------------- |
| Create a session  | tf.Session()               |
| Run a session     | tf.Session.run()           |
| Evaluate a tensor | variable_name.eval()       |
| Close a session   | sess.close()               |
| Session by block  | with tf.Session() as sess: |