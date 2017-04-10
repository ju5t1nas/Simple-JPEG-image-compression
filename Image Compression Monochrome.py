import scipy.misc as sm
import numpy as nm

#Lets make a class called image.
#Here we will put everything that works.

class image:
    def __init__(self, imageName, greyscaleToggle):
        #create a quick way to get the name of the image
        self.name = str(imageName)
        #Chech whether greyscaleToggle is a boolean
        #If it is, then set self.grey to what it is,
        #Else set to false
        if isinstance(greyscaleToggle, bool):
            self.grey = greyscaleToggle
        else:
            self.grey = False

        #We read the picture using imread
        self.pic = sm.imread(self.name, self.grey)
        # We create a new matrix of the compressed image and initially set it equal to original
        self.compressed = self.pic

        #So we don't have to call sm.shape a bunch, I make a quick self.dim
        self.evenShape()

        # We can easily find the mean of a greyscale image:
        if self.grey == True:
            self.mean = self.pic.mean()

    #I have not tested it for coloured photos, but I am pretty sure it should not work
    def evenShape(self):
        self.dim = self.compressed.shape
        #We make a variable to mark whether shape of the image is even.
        #What I mean is whether the amount of rows and columns are both even.
        even = False

        #We check whether both num of rows and col. is even
        if self.dim[0] % 2 == 0 and self.dim[1] % 2 == 0:
            even = True
        #If not, we reshape the picture.
        if even == False:
            #We now need to delete either a row or column
            #Preferable we delete last row or column

            #Check whether number of rows is even
            if self.dim[0] % 2 != 0:
                #We delete the last row and replace the old image with the new one.
                self. pic = nm.delete(self.pic, self.dim[0]-1, 0)
            #Check whether number of columns is even
            elif self.dim[1] % 2 != 0:
                #We delete the last colum and replace the opd image with the new one.
                self.pic = nm.delete(self.pic, self.dim[1]-1, 1)

        #One last sanity check whether the image is evenly shaped
        if self.dim[0] % 2 == 0 and self.dim[1] % 2 == 0:
            return True

    #This produces the matrices for mean compression
    #You can choose whether you want a matrix for compression with preservation of data for reversal or not
    def meanMat(self, revertible):
        self.dim = self.compressed.shape
        #We check whether 'revertable' is bool type
        if not isinstance(revertible, bool):
            #We will raise exception later
            revertible = True
        #I will name the matrices Mr and Mc.
        #They stand for Martix for Rows and Matrix for Columns.
        #If we want a revertable matric we create a larger matrix.
        if revertible == True:
            #We create a matrix of all zeroes
            self.Mr = nm.zeros((self.dim[0], self.dim[0]))
        #If we do not want revertable, we create a smaller matrix
        elif revertible == False:
            #We create a matrix of all zeroes
            self.Mr = nm.zeros((int(self.dim[0] / 2), self.dim[0]))

        # We start replacing some entries in the matrix with what is supposed to be there.
        for i in range(int(self.dim[0] / 2)):
            self.Mr[i][i * 2] = 1 / 2
            self.Mr[i][i * 2 + 1] = 1 / 2
            #If we have a larger matrix, we add elements needed for reversal
            if revertible == True:
                self.Mr[i + int(self.dim[0] / 2)][i * 2] = -1 / 2
                self.Mr[i + int(self.dim[0] / 2)][i * 2 + 1] = 1 / 2

        #Same logic as before.
        if revertible == True:
            self.Mc = nm.zeros((self.dim[1], self.dim[1]))
        elif revertible == False:
            self.Mc = nm.zeros((int(self.dim[1] / 2), self.dim[1]))
        # We start replacing some entries in the matrix with what is supposed to be there.
        for i in range(int(self.dim[1] / 2)):
            self.Mc[i][i * 2] = 1 / 2
            self.Mc[i][i * 2 + 1] = 1 / 2
            if revertible == True:
                self.Mc[i + int(self.dim[1] / 2)][i * 2] = -1 / 2
                self.Mc[i + int(self.dim[1] / 2)][i * 2 + 1] = 1 / 2

    #Finally, the mathod for compression.
    def compression(self, revertible, times):
        #We check whether 'revertible' is bool type
        if not isinstance(revertible, bool):
            #We set revertible to true
            revertible = True
        #We check whether the number of times to run compression is an int.
        if not isinstance(times, int):
            times = 1
        #We compress for the amount of times we want
        for i in range(times):
            # We call the meanMat method so that each time the compression matrices are the correct size.
            self.meanMat(revertible)
            #We compress through matrix multiplication
            self.compressed = nm.dot(nm.dot(self.Mr, self.compressed), self.Mc.transpose())
        #We save a new compressed image
        sm.imsave('compressed' + self.name, self.compressed)



#picture = image("pic.jpg", True)
#print(picture.waveMat())
#picture.compression(False, 1)
