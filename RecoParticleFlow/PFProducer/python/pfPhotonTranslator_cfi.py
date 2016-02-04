import FWCore.ParameterSet.Config as cms

#from RecoParticleFlow.PFProducer.pfPhotonTranslatorMVACut_cfi import *
from RecoEgamma.PhotonIdentification.isolationCalculator_cfi import *

pfPhotonTranslator = cms.EDProducer("PFPhotonTranslator",
                                    #PFCandidate = cms.InputTag("particleFlow"),
                                    PFCandidate = cms.InputTag("pfSelectedPhotons"),
                                    PFBasicClusters = cms.string("pfphot"),
                                    PFPreshowerClusters = cms.string("pfphot"),
                                    PFSuperClusters = cms.string("pfphot"),
                                    PFPhotonCores = cms.string("pfphot"),
                                    PFPhotons = cms.string("pfphot"),
                                    primaryVertexProducer = cms.string("offlinePrimaryVerticesWithBS"),
                                    isolationValues = cms.PSet(
                                      pfChargedHadrons = cms.InputTag('isoValPhotonWithCharged'),
                                      pfPhotons = cms.InputTag('isoValPhotonWithPhotons'),
                                      pfNeutralHadrons= cms.InputTag('isoValPhotonWithNeutral')
                                      ),
                                    barrelEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                                    endcapEcalHits = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                                    hcalTowers = cms.InputTag("towerMaker"),       
                                    hOverEConeSize = cms.double(0.15)
                                    )
