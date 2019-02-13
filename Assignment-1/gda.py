import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import linalg
from decimal import Decimal

def read_params():
  x_data = pd.read_csv("q4x.dat",header=None,sep="\s+",dtype=float)
  y_data = pd.read_csv("q4y.dat",header=None,sep="\s+")
  x = np.asmatrix(np.array(x_data))
  y = np.asmatrix(np.array(y_data))
  x = normalize(x)
  y = modify(y)
  return (x,y)

def normalize(mat):
  mean = np.mean(mat,axis=0)
  var = np.var(mat,axis=0)
  mat-=mean
  for i in range (len(mat)):
    mat[i,:] = np.divide(mat[i,:],var)
  z = 1 + np.zeros((mat.shape[0],1),dtype=float)
  z = np.hstack((z,mat))
  return z

def modify(y):
  z = np.asmatrix(np.zeros((y.shape[0],y.shape[1]),dtype=int,order='F'))
  for i in range(len(y)):
    if(y[i,0]=='Alaska'):
      z[i,0] = 1
    else:
      z[i,0] = 0
  return z

def compute_covariance_matrix(class_data,mean_mat,var_mat):
  z = np.dot((class_data-mean_mat).transpose(),(class_data-mean_mat))
  return z/len(class_data)

def plot_linear(class_0,class_1,mu_0,mu_1,sigma,sigma_0,sigma_1):
  plt.scatter(np.array(class_1)[:,1],np.array(class_1)[:,2],c='g',label='Alaska (y==1)')
  plt.scatter(np.array(class_0)[:,1],np.array(class_0)[:,2],c='r',label='Canada (y==0)')
  plt.xlabel('Growth ring diameters in fresh water')
  plt.ylabel('Growth ring diameters in marine water')
  plt.title('Gaussian Discriminant Analysis')

  const_term = np.dot(np.dot(mu_0.transpose(),np.linalg.pinv(sigma)),mu_0) - np.dot(np.dot(mu_1.transpose(),np.linalg.pinv(sigma)),mu_1)
  x_coeff = 2*np.dot((mu_1.transpose()-mu_0.transpose()),np.linalg.pinv(sigma))
  x1 = np.linspace(-0.1,0.1,20)
  x2 = -1*(x_coeff[0,0]+const_term[0,0]+x_coeff[0,1]*x1)/x_coeff[0,2]
  plt.plot(x1,x2,label='Linear Hypothesis')
  
  x_coeff = 2*(np.dot(mu_1.transpose(),np.linalg.pinv(sigma_1))-np.dot(mu_0.transpose(),np.linalg.pinv(sigma_0)))
  x_2coeff = np.linalg.pinv(sigma_0) - np.linalg.pinv(sigma_1)
  size = 500
  threshold = 0.01
  class_fin = []
  y = np.asmatrix(np.zeros((size,size),dtype=float))
  x1 = np.linspace(-0.1,0.1,size)
  x2 = np.linspace(-0.1,0.1,size)
  x,y = np.meshgrid(x1,x2)
  for i in range(size):
    for j in range(size):
      vec = np.asmatrix([[1],[x1[i]],[x2[j]]])
      y[i,j] = np.dot(np.dot(vec.transpose(),x_2coeff),vec) + np.dot(x_coeff,vec) + const_term
      if abs(y[i,j])<threshold:
        class_fin.append([[x1[i]],[x2[j]]])
  
  new_x,new_y = zip(*sorted(zip(np.array(class_fin)[:,0],np.array(class_fin)[:,1])))
  plt.plot(new_x,new_y,'-',c='y',label='Quadratic Hypothesis')
  plt.plot(np.array(class_fin)[:,0],np.array(class_fin)[:,1])
  plt.legend()
  plt.savefig('gda.png',dpi=200)

def main():
  (x,y) = read_params()
  class_0 = []
  class_1 = []
  for i in range(len(x)):
    if y[i]==0:
      class_0.append([x[i,0],x[i,1],x[i,2]])
    else:
      class_1.append([x[i,0],x[i,1],x[i,2]])

  mean_0 = np.mean(class_0,axis=0)
  mean_1 = np.mean(class_1,axis=0)
  var_0 = np.var(class_0,axis=0)
  var_1 = np.var(class_1,axis=0)
  covariance_matrix_0 = compute_covariance_matrix(class_0,mean_0,var_0)
  covariance_matrix_1 = compute_covariance_matrix(class_1,mean_1,var_1)
  covariance_matrix = compute_covariance_matrix(x,np.mean(x,axis=0),np.var(x,axis=0))
  plot_linear(class_0,class_1,mean_0,mean_1,covariance_matrix,covariance_matrix_0,covariance_matrix_1)
  
if __name__ == "__main__":
	main()