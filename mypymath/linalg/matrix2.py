class Matrix2:
    def __init__(self,
                 elements=None,
                 a11=None, a12=None,
                 a21=None, a22=None):
        """
            | a11 a12 |
        A = | a21 a22 |
        elements = (a11, a12, a21, a22)
        """
        if not None in (a11, a12, a22, a21):
                self.a11 = a11
                self.a12 = a12
                self.a21 = a21
                self.a22 = a22
        elif elements is not None and len(elements) == 4:
            self.a11 = elements[0]
            self.a12 = elements[1]
            self.a21 = elements[2]
            self.a22 = elements[3]
        else:
            print('Error in Matrix2.init:',
                  'incorrect args!')
            return

    def det(self):
        return self.a11 * self.a22 - self.a21 * self.a21

