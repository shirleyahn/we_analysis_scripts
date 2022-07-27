import h5py
import numpy
import matplotlib
import matplotlib.pyplot as pyplot

def convert_to_step(dataset):
    return numpy.hstack((numpy.array(0.0),
                        numpy.repeat(dataset, 2),
                        numpy.array(0.0)
                        ))

class DurationHistogram(object):
    def __init__(self):
        pass

    def from_list(self, kinetics_path_list, fstate, firstiter, lastiter, **kwargs):
        weights = []
        durations = []
        for path in kinetics_path_list: 
            #print('Loading {:s}'.format(path))
            print('iter, seg')
            kinetics_file = h5py.File(path, 'r')
            if lastiter is not None:
                where = numpy.where(
                    numpy.logical_and(kinetics_file['durations'][firstiter-1:lastiter]['weight'] > 0,
                                      kinetics_file['durations'][firstiter-1:lastiter]['fstate'] == fstate))
                d = kinetics_file['durations'][firstiter-1:lastiter]['duration']
                w = kinetics_file['durations'][firstiter-1:lastiter]['weight']
                s = kinetics_file['durations'][firstiter-1:lastiter]['seg_id']
            else:
                where = numpy.where(
                    numpy.logical_and(kinetics_file['durations']['weight'] > 0,
                                      kinetics_file['durations']['fstate'] == fstate))
                d = kinetics_file['durations']['duration'] 
                w = kinetics_file['durations']['weight']
                s = kinetics_file['durations']['seg_id']
            for i in range(where[1].shape[0]):
                weight = w[where[0][i],where[1][i]]
                duration = d[where[0][i],where[1][i]]
                segid = s[where[0][i],where[1][i]]
                if duration > 0:
                    durations.append(duration)
                else:
                    durations.append(where[0][i])
                weights.append(weight)
                print(where[0][i]+1, segid)

        weights = numpy.array(weights)
        durations = numpy.array(durations)
        print('weights')
        print(weights)
        print('duration')
        print(durations)
        print('durations mean')
        print(numpy.mean(durations))
        print('durations min')
        print(numpy.min(durations))
        print('durations max')
        print(numpy.max(durations))
        print('number of pathways')
        print(len(durations))

        self.histogram(durations, weights, firstiter=firstiter, lastiter=lastiter, **kwargs)
        return

    def integrate(self, hist, edges, lb=None, ub=None):
        if lb is None:
           lb = edges[0]

        if ub is None:
           ub = edges[-1]

        integral = 0.0
       
        setbreak = False
        for i, leftedge in enumerate(edges[:-1]):
            if leftedge >= lb:
                rightedge = edges[i+1] 
                if rightedge > ub:
                    rightedge = ub
                    setbreak = True
                delta = rightedge-leftedge 
                integral += hist[i]*delta
                if setbreak:
                    break

        return integral

    def normalize_density(self):
        integral = self.integrate(self.hist, self.edges)
        #print("normalizing event duration distribution by factor: {:f}".format(integral))
        self.hist /= integral
        return 
         
    def histogram(self, durations, weights, binwidth=1, lastiter=None,  
                  correction=True, **kwargs):
        lb = 0
        ub = numpy.ceil(durations.max()) 
        #edges = numpy.arange(lb, ub+binwidth, binwidth, dtype=float)
        edges = numpy.arange(lb, lastiter+binwidth, binwidth, dtype=float)
        #print('edges')
        #print(edges)
        hist, _ = numpy.histogram(durations, weights=weights, bins=edges,
                                  density=True)
        #print('correction')
        #print(correction)
        if correction:
            halfwidth = binwidth/2
            factors = 1/numpy.arange(lastiter-halfwidth, lb-halfwidth, 
                                     -1*binwidth, dtype=float)
            hist = hist*factors#[:hist.shape[0]] 
        #print('kwargs')
        #print(kwargs)
        self.hist = hist
        self.edges = edges
        self.normalize_density()
         
        return

    def plot_hist(self, outpath='durations.png', color='black', 
                  log=False, ax=None):
        matplotlib.rcParams['font.size'] = 16
        linewidth=1.5
        
        if ax is None:
            fig, ax = pyplot.subplots() 
            fig.set_size_inches(9.68,8)
        else:
            fig = pyplot.gcf()

        if log:
            ax.plot(numpy.repeat(self.edges, 2), numpy.log(convert_to_step(self.hist)), 
                    color=color)
        else:
            ax.plot(numpy.repeat(self.edges, 2), convert_to_step(self.hist), color=color)
        for kw in ('top', 'right'):
            ax.spines[kw].set_visible(False)
        for kw in ('bottom', 'left'):
            ax.spines[kw].set_linewidth(linewidth)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.tick_params(direction='out', width=linewidth)
        ax.set_xlabel('duration time (WE iterations)')
        ax.set_title('Event Duration Time Distribution')
        if log:
            ax.set_ylabel('log(probability density)')
        else:
            ax.set_ylabel('probability density')
        if not log:
            ax.set_ylim(0, self.hist.max()*1.2)

        #fig.subplots_adjust(bottom=0.1, left=0.25)
        pyplot.savefig(outpath)


def main():

    pathlist = ['direct.h5']
    h = DurationHistogram()
    h.from_list(pathlist, correction=True, fstate=1, firstiter=1, lastiter=600, binwidth=10)
    h.plot_hist(color='blue')
    

if __name__ == "__main__":
    main()
