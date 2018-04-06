class Matrix3:
    def __init__(self,
                 elements=None,
                 a11=None, a12=None, a13=None,
                 a21=None, a22=None, a23=None,
                 a31=None, a32=None, a33=None):
        """
            | a11 a12 a13 |
        A = | a21 a22 a23 |
            | a31 a32 a33 |

        elements = (a11, a12, a13, a21, a22, a23, a31, a32, a33)

        """
        if not None in (a11, a12, a13, a21, a22, a23, a31, a32, a33):
                self.a11 = a11
                self.a12 = a12
                self.a13 = a13
                self.a21 = a21
                self.a22 = a22
                self.a23 = a23
                self.a31 = a31
                self.a32 = a32
                self.a33 = a33
        elif elements is not None and len(elements) == 9:
            self.a11 = elements[0]
            self.a12 = elements[1]
            self.a13 = elements[2]
            self.a21 = elements[3]
            self.a22 = elements[4]
            self.a23 = elements[5]
            self.a31 = elements[6]
            self.a32 = elements[7]
            self.a33 = elements[8]
        else:
            print('Error in Matrix3.init:',
                  'incorrect args!')
            return

    def det(self):
        minor11 = self.a22 * self.a33 - self.a23 * self.a32
        minor12 = self.a21 * self.a33 - self.a23 * self.a31
        minor13 = self.a21 * self.a32 - self.a22 * self.a31
        return (self.a11 * minor11 -
                self.a12 * minor12 +
                self.a13 * minor13)
