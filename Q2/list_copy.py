
# Analyze the sample code that copies one list to another. Does it work correctly? Argue.
# L = [1, 2, 3]
# X = L

L = [1, 2, 3]
X = L

# The variable X is assigned to the same object as L, the problem is that it is assigned like a pointer in c++
# so if we change the value of L, we are changing the value of X too, because they are pointing to the same object
# for example, if you are to add a value to L, it is also added to X
L.append(4)
print(L) # [1, 2, 3, 4]
print(X) # [1, 2, 3, 4]

# In the following code, it is shown that bot have the same address: 
print(id(L)) #4376368576
print(id(X)) #4376368576


#To bypass this problem 
# we can use the copy() method
X = L.copy()
L.append(5)
print(L) #[1, 2, 3, 4, 5]
print(X) #[1, 2, 3, 4]
print(id(L)) #4537161472
print(id(X)) #4538129600

# Now X has a different address, this means that it 
# has took up a new space in memory to store the data of L up to the point of the copy.

# Other ways of copying X, without this issue:
X = L[:] 
X = list(L)
