class Matrix4:
    def __init__(self,
                 elements=None,
                 a11=None, a12=None, a13=None, a14 = None,
                 a21=None, a22=None, a23=None, a24 = None,
                 a31=None, a32=None, a33=None, a34 = None,
                 a41=None, a42=None, a43=None, a44 = None):
        """
            | a11 a12 a13 a14 |
        A = | a21 a22 a23 a24 |
            | a31 a32 a33 a34 |
            | a41 a42 a43 a44 |

        elements = (a11, a12, a13, a14,
                    a21, a22, a23, a24,
                    a31, a32, a33, a34,
                    a41, a42, a43, a44)

        """
        if not None in (a11, a12, a13, a14, a21, a22, a23, a24,
                        a31, a32, a33, a34, a41, a42, a43, a44):
            self.a11 = a11
            self.a12 = a12
            self.a13 = a13
            self.a14 = a14
            self.a21 = a21
            self.a22 = a22
            self.a23 = a23
            self.a24 = a24
            self.a31 = a31
            self.a32 = a32
            self.a33 = a33
            self.a34 = a34
            self.a41 = a41
            self.a42 = a42
            self.a43 = a43
            self.a44 = a44
        elif elements is not None and len(elements) == 16:
            self.a11 = elements[0]
            self.a12 = elements[1]
            self.a13 = elements[2]
            self.a14 = elements[3]
            self.a21 = elements[4]
            self.a22 = elements[5]
            self.a23 = elements[6]
            self.a24 = elements[7]
            self.a31 = elements[8]
            self.a32 = elements[9]
            self.a33 = elements[10]
            self.a34 = elements[11]
            self.a41 = elements[12]
            self.a42 = elements[13]
            self.a43 = elements[14]
            self.a44 = elements[15]
        else:
            print('Error in Matrix4.init:',
                  'incorrect args!')
            return

    def det(self):
        minor11 = (self.a22 * (self.a33 * self.a44 - self.a43 * self.a34) -
                   self.a23 * (self.a32 * self.a44 - self.a42 * self.a34) +
                   self.a24 * (self.a42 * self.a43 - self.a42 * self.a33))
        minor12 = (self.a21 * (self.a33 * self.a44 - self.a34 * self.a43) -
                   self.a23 * (self.a31 * self.a44 - self.a41 * self.a34) +
                   self.a24 * (self.a31 * self.a43 - self.a41 * self.a33))
        minor13 = (self.a21 * (self.a32 * self.a44 - self.a34 * self.a42) -
                   self.a22 * (self.a31 * self.a44 - self.a41 * self.a34) +
                   self.a34 * (self.a31 * self.a42 - self.a32 * self.a41))
        minor14 = (self.a21 * (self.a32 * self.a43 - self.a33 * self.a42) -
                   self.a22 * (self.a31 * self.a43 - self.a33 * self.a41) +
                   self.a23 * (self.a31 * self.a42 - self.a32 * self.a41))
        return (self.a11 * minor11 -
                self.a21 * minor21 +
                self.a31 * minor31 -
                self.a41 * minor41)
