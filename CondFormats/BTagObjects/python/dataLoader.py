import itertools
import ROOT
ROOT.gSystem.Load('libCondFormatsBTagObjects')


ETA_MIN = -2.4
ETA_MAX = 2.4
PT_MIN = 20.
PT_MAX = 1000.
DISCR_MIN = 0.
DISCR_MAX = 1.


class DataLoader(object):
    def __init__(self, csv_data):

        print "Loading csv data"

        # list of entries
        ens = []
        for l in csv_data:
            if not l.strip():
                continue  # skip empty lines
            try:
                ens.append(ROOT.BTagEntry(l))
            except TypeError:
                raise RuntimeError("Error: can not interpret line: " + l)
        self.entries = ens

        # sets of fixed data
        self.ops = set(e.params.operatingPoint for e in ens)
        self.flavs = set(e.params.jetFlavor for e in ens)
        self.meass = set(e.params.measurementType for e in ens)
        self.syss = set(e.params.sysType for e in ens)
        self.etas = set((e.params.etaMin, e.params.etaMax) for e in ens)
        self.pts = set((e.params.ptMin, e.params.ptMax) for e in ens)
        self.discrs = set((e.params.discrMin, e.params.discrMax) for e in ens)

        # test points for variable data (using bound +- epsilon)
        eps = 1e-4
        eta_test_points = list(itertools.ifilter(
            lambda x: ETA_MIN < x < ETA_MAX,
            itertools.chain(
                (a + eps for a, _ in self.etas),
                (a - eps for a, _ in self.etas),
                (b + eps for _, b in self.etas),
                (b - eps for _, b in self.etas),
                (ETA_MIN + eps, ETA_MAX - eps),
            )
        ))
        abseta_test_points = list(itertools.ifilter(
            lambda x: 0. < x < ETA_MAX,
            itertools.chain(
                (a + eps for a, _ in self.etas),
                (a - eps for a, _ in self.etas),
                (b + eps for _, b in self.etas),
                (b - eps for _, b in self.etas),
                (eps, ETA_MAX - eps),
            )
        ))
        pt_test_points = list(itertools.ifilter(
            lambda x: PT_MIN < x < PT_MAX,
            itertools.chain(
                (a + eps for a, _ in self.pts),
                (a - eps for a, _ in self.pts),
                (b + eps for _, b in self.pts),
                (b - eps for _, b in self.pts),
                (PT_MIN + eps, PT_MAX - eps),
            )
        ))
        discr_test_points = list(itertools.ifilter(
            lambda x: DISCR_MIN < x < DISCR_MAX,
            itertools.chain(
                (a + eps for a, _ in self.discrs),
                (a - eps for a, _ in self.discrs),
                (b + eps for _, b in self.discrs),
                (b - eps for _, b in self.discrs),
                (DISCR_MIN + eps, DISCR_MAX - eps),
            )
        ))
        # use sets
        self.eta_test_points = set(round(f, 5) for f in eta_test_points)
        self.abseta_test_points = set(round(f, 5) for f in abseta_test_points)
        self.pt_test_points = set(round(f, 5) for f in pt_test_points)
        self.discr_test_points = set(round(f, 5) for f in discr_test_points)

        print "Loading csv data done"

    def print_data(self):
        print "\nFound operating points (need at least 0, 1, 2):"
        print self.ops

        print "\nFound jet flavors (need 0, 1, 2):"
        print self.flavs

        print "\nFound measurement types (at least 'comb'):"
        print self.meass

        print "\nFound sys types (need at least 'central', 'up', 'down'; " \
              "also 'up_SYS'/'down_SYS' compatibility is checked):"
        print self.syss

        print "\nFound eta ranges: (need everything covered from %g or 0. " \
              "up to %g):" % (ETA_MIN, ETA_MAX)
        print self.etas

        print "\nFound pt ranges: (need everything covered from %g " \
              "to %g):" % (PT_MIN, PT_MAX)
        print self.pts

        print "\nFound discr ranges: (only needed for operatingPoint==3, " \
              "covered from %g to %g):" % (DISCR_MIN, DISCR_MAX)
        print self.discrs

        print "\nTest points for eta (bounds +- epsilon):"
        print self.eta_test_points

        print "\nTest points for pt (bounds +- epsilon):"
        print self.pt_test_points

        print "\nTest points for discr (bounds +- epsilon):"
        print self.discr_test_points
        print ""
