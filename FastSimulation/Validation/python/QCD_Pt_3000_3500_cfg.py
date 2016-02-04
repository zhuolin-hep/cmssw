# The following comments couldn't be translated into the new config version:

# Work-around because of a bug in HLT 
# Reconstruction sequence
import FWCore.ParameterSet.Config as cms

process = cms.Process("HLT")
process.load("Configuration.Generator.PythiaUESettings_cfi")

# Famos sequences (With HLT)
process.load("FastSimulation.Configuration.CommonInputsFake_cff")

process.load("FastSimulation.Configuration.FamosSequences_cff")

# L1 Emulator and HLT Setup
process.load("FastSimulation.HighLevelTrigger.common.HLTSetup_cff")

process.load("PhysicsTools.HepMCCandAlgos.genEventWeight_cfi")

process.load("PhysicsTools.HepMCCandAlgos.genEventScale_cfi")

# HLT paths
process.load("HLTrigger.Configuration.main.HLTpaths_cff")

# To write out events 
process.load("FastSimulation.Configuration.EventContent_cff")

# Keep the logging output to a nice level #
process.load("FWCore.MessageService.MessageLogger_cfi")

process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.2 $'),
    name = cms.untracked.string('$Source: /afs/cern.ch/user/c/cvscmssw/public/CMSSW/CMSSW/FastSimulation/Validation/python/Attic/QCD_Pt_3000_3500_cfg.py,v $'),
    annotation = cms.untracked.string('RelVal FastSim QCD with pt hat 3000-3500GeV')
)
process.ReleaseValidation = cms.untracked.PSet(
    eventsPerJob = cms.untracked.uint32(1000),
    totalNumberOfEvents = cms.untracked.uint32(25000),
    primaryDatasetName = cms.untracked.string('RelValFastSimQCD_Pt_3000_3500')
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    # This is to initialize the random engines of Famos
    moduleSeeds = cms.PSet(
        l1ParamMuons = cms.untracked.uint32(54525),
        caloRecHits = cms.untracked.uint32(654321),
        MuonSimHits = cms.untracked.uint32(97531),
        muonCSCDigis = cms.untracked.uint32(525432),
        muonDTDigis = cms.untracked.uint32(67673876),
        famosSimHits = cms.untracked.uint32(13579),
        paramMuons = cms.untracked.uint32(54525),
        famosPileUp = cms.untracked.uint32(918273),
        VtxSmeared = cms.untracked.uint32(123456789),
        muonRPCDigis = cms.untracked.uint32(524964),
        siTrackerGaussianSmearingRecHits = cms.untracked.uint32(24680)
    ),
    # This is to initialize the random engine of the source
    sourceSeed = cms.untracked.uint32(123456789)
)

process.source = cms.Source("PythiaSource",
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    filterEfficiency = cms.untracked.double(1.0),
    PythiaParameters = cms.PSet(
        process.pythiaUESettingsBlock,
        processParameters = cms.vstring('MSEL=1 ! QCD hight pT processes', 
            'CKIN(3)=3000. ! minimum pt hat for hard interactions', 
            'CKIN(4)=3500. ! maximum pt hat for hard interactions'),
        # This is a vector of ParameterSet names to be read, in this order
        parameterSets = cms.vstring('pythiaUESettings', 
            'processParameters')
    )
)

process.Timing = cms.Service("Timing")

process.o1 = cms.OutputModule("PoolOutputModule",
    process.FEVTSIMEventContent,
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RECO')
    ),
    fileName = cms.untracked.string('FEVTWithHLT.root')
)

process.simulation = cms.Path(process.simulationWithFamos+process.genEventScale+process.genEventWeight)
process.hltEnd = cms.Sequence(process.dummyModule)
process.reconstruction = cms.Path(process.doCalo+process.towerMakerForAll+process.reconstructionWithFamos)
process.outpath = cms.EndPath(process.o1)
process.famosPileUp.UseTRandomEngine = True
process.famosSimHits.UseTRandomEngine = True
process.siTrackerGaussianSmearingRecHits.UseTRandomEngine = True
process.caloRecHits.UseTRandomEngine = True
process.paramMuons.UseTRandomEngine = True
process.famosPileUp.PileUpSimulator.averageNumber = 0.0
process.load("Configuration.StandardSequences.MagneticField_40T_cff")
#process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.VolumeBasedMagneticFieldESProducer.useParametrizedTrackerField = True
process.famosSimHits.SimulateCalorimetry = True
process.famosSimHits.SimulateTracking = True
process.MessageLogger.destinations = ['detailedInfo.txt']

