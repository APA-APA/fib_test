
# coding: utf-8

# # Test writing and read binary
# 
# https://www.johnny-lin.com/cdat_tips/tips_fileio/bin_array.html

# In[16]:


import numpy as np

newFileBytes = [128, 3, 2555.232, 0, 64.888]

a=np.array(newFileBytes, dtype=np.float32)

print a
f=open('APA_test_binary.dat','w+b')

f.write(a)
f.close()


# In[17]:


f=open('APA_test_binary.dat','rb')
s=f.read(-1)
b=np.frombuffer(s, dtype=np.float32)
print b
f.close()

