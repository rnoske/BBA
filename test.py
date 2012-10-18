import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue

class Fitter():
    """ Class for fitting data
    
    """
    
    def create_testdata(self):
        """ creates two gaussion functions as testdata
        
        Returns:
            np.array testdata
        
        """
        # Setting up test data
        def norm(x, mean, sd):
          norm = []
          for i in range(x.size):
              norm += [1.0/(sd*np.sqrt(2*np.pi))*np.exp(-(x[i] - mean)**2/(2*sd**2))]
          return np.array(norm)
        
        mean1, mean2 = 0, -2
        std1, std2 = 0.5, 1 
        
        x = np.linspace(-20, 20, 500)
        y_real = norm(x, mean1, std1) + norm(x, mean2, std2)
        return x, y_real
        
    def beispiel(self, i, q):
        """ Testbeispiel. Muss mit creat_testdata zusammen funktionieren!
        
        """
        def norm(x, mean, sd):
            norm = []
            for i in range(x.size):
                norm += [1.0/(sd*np.sqrt(2*np.pi))*np.exp(-(x[i] - mean)**2/(2*sd**2))]
            return np.array(norm)
        x, y_real = self.create_testdata()
        # Solving
        m, dm, sd1, sd2 = [5, 10, 1, 1]
        p = [m, dm, sd1, sd2] # Initial guesses for leastsq
        y_init = norm(x, m, sd1) + norm(x, m + dm, sd2) # For final comparison plot
        
        def res(p, y, x):
            m, dm, sd1, sd2 = p
            m1 = m
            m2 = m1 + dm
            y_fit = norm(x, m1, sd1) + norm(x, m2, sd2)
            err = y - y_fit
            return err
        
        plsq = leastsq(res, p, args = (y_real, x))        
        y_est = norm(x, plsq[0][0], plsq[0][2]) + norm(x, plsq[0][1], plsq[0][3])
        """
        plt.plot(x, y_real, label='Real Data')
        plt.plot(x, y_init, 'r.', label='Starting Guess')
        plt.plot(x, y_est, 'g.', label='Fitted')
        plt.legend()
        plt.show()
        """
        
        q.put([i, plsq])
        
        
    def multi_beispiel(self):
        jobs = []
        n = 10
        q = Queue()
        for i in xrange(n):
            p = Process(target=self.beispiel, args=(i, q,))
            jobs.append(p)
            p.start()
        
        
        _tarr =[]
        for i in xrange(n):
            _tmp = q.get()
            _tarr.append(_tmp)
            print _tmp
        p.join()
        
        print _tarr
        _tarr.sort()
        print _tarr
        
        
        
        print 'finished'


if __name__ == "__main__":

    myfitter = Fitter()
    myfitter.multi_beispiel()