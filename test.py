import numpy as np
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue, JoinableQueue
import multiprocessing as mp


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
        
    def beispiel(self, work_q, result_q):
        """ Testbeispiel. Muss mit creat_testdata zusammen funktionieren!
        
        """
        while True:
            work = work_q.get()
            print 'test'

            def norm(x, mean, sd):
                norm = []
                for i in range(x.size):
                    norm += [1.0/(sd*np.sqrt(2*np.pi))*np.exp(-(x[i] - mean)**2/(2*sd**2))]
                return np.array(norm)
            i, x, y_real = work #self.create_testdata()
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
            print plsq
            y_est = norm(x, plsq[0][0], plsq[0][2]) + norm(x, plsq[0][1], plsq[0][3])
            """
            plt.plot(x, y_real, label='Real Data')
            plt.plot(x, y_init, 'r.', label='Starting Guess')
            plt.plot(x, y_est, 'g.', label='Fitted')
            plt.legend()
            plt.show()
            """
            
            result_q.put([i, plsq])
            work_q.task_done()
        
        
    def multi_beispiel(self):
        num_workers = 2
        work_q = JoinableQueue()
        n = 10
        result_q = mp.Queue()    

        #put tasks into queue
        for i in xrange(n):
            x, y = self.create_testdata()
            _work = (i, x, y)
            work_q.put(_work)

        
        #start end setup workers
        workers = []
        for i in range(num_workers):
            workers.append(Process(target=self.beispiel, args=(work_q, result_q)))
            
        for w in workers:
            print w
            w.daemon = True
            w.start()
        work_q.join()
        
        n_result = result_q.qsize()
        for result in xrange(n_result):
            _t = result_q.get()
            print _t

        """            
        for i in xrange(n):
            p = Process(target=self.beispiel, args=(i, q,))
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
        """
        
        
        print 'finished'


if __name__ == "__main__":

    myfitter = Fitter()
    myfitter.multi_beispiel()