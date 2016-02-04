#ifndef PerigeeLinearizedTrackState_H
#define PerigeeLinearizedTrackState_H

#include "RecoVertex/VertexPrimitives/interface/LinearizedTrackState.h"
#include "TrackingTools/PatternTools/interface/TSCPBuilderNoMaterial.h"
#include "DataFormats/GeometrySurface/interface/ReferenceCounted.h"
#include "RecoVertex/VertexPrimitives/interface/LinearizedTrackState.h"
#include "Math/SMatrix.h"
#include "DataFormats/CLHEP/interface/Migration.h"

/** Calculates and stores the ImpactPointMeasurement of the
 *  impact point (point of closest approach in 3D) to the
 *  given linearization point.
 *  (see V.Karimaki, HIP-1997-77 / EXP)
 *
 *  Computes the parameters of the trajectory state at the transverse
 *  point of closest approach (in the global transverse plane) to
 *  the linearization point, and the jacobiam matrices.
 *  (see R.Fruehwirth et al. Data Analysis Techniques in HEP Experiments
 *  Second Edition, Cambridge University Press 2000, or
 *  R.Fruehwirth et al. Vertex reconstruction and track bundling at the LEP
 *  collider using robust algorithms. Computer Physics Communications 96
 *  (1996) 189-208).
 *
 *  Both are done `on-demand' to improve CPU performance.
 *
 *  This particular implementation works with "perigee"
 *  helix parametrization:
 *  see Billoir et al. NIM in PR A311(1992) 139-150
 */

class PerigeeLinearizedTrackState : public LinearizedTrackState<5> {


public:

  /** Friend class properly dealing with creation
   *  of reference-counted pointers to LinearizedTrack objects
   */
  friend class LinearizedTrackStateFactory;
  typedef ReferenceCountingPointer<LinearizedTrackState<5> > RefCountedLinearizedTrackState;

  /**
   * Returns a new linearized state with respect to a new linearization point.
   * A new object of the same type is returned, without change to the existing one.
   */
  virtual  RefCountedLinearizedTrackState stateWithNewLinearizationPoint
    (const GlobalPoint & newLP) const;


  /**
   * The point at which the track state has been linearized
   */
  const GlobalPoint & linearizationPoint() const { return theLinPoint; }

  virtual reco::TransientTrack track() const { return theTrack; }

  const TrajectoryStateOnSurface state() const { return theTSOS; }

  /** Method returning the constant term of the Taylor expansion
   *  of the measurement equation
   */
  const AlgebraicVector5 & constantTerm() const;

  /** Method returning the Position Jacobian from the Taylor expansion
   *  (Matrix A)
   */
  const AlgebraicMatrix53 & positionJacobian() const;

  /** Method returning the Momentum Jacobian from the Taylor expansion
   *  (Matrix B)
   */
  const AlgebraicMatrix53 & momentumJacobian() const;

  /** Method returning the parameters of the Taylor expansion
   */
  const AlgebraicVector5 & parametersFromExpansion() const;

  /** Method returning the track state at the point of closest approach
   *  to the linearization point, in the transverse plane (a.k.a.
   *  transverse impact point).
   */
  const TrajectoryStateClosestToPoint & predictedState() const;

  /** Method returning the parameters of the track state at the
   *  transverse impact point.
   */
  AlgebraicVector5 predictedStateParameters() const;

  /** Method returning the momentum part of the parameters of the track state
   *  at the linearization point.
   */
  virtual AlgebraicVector3 predictedStateMomentumParameters() const;

  /** Method returning the weight matrix of the track state at the
   *  transverse impact point.
   * The error variable is 0 in case of success.
   */
  AlgebraicSymMatrix55 predictedStateWeight(int & error) const;

  /** Method returning the covariance matrix of the track state at the
   *  transverse impact point.
   */
  AlgebraicSymMatrix55 predictedStateError() const;

  /** Method returning the momentum covariance matrix of the track state at the
   *  transverse impact point.
   */
  AlgebraicSymMatrix33 predictedStateMomentumError() const;

//   /** Method returning the impact point measurement
//    */
//   ImpactPointMeasurement impactPointMeasurement() const;

  TrackCharge charge() const {return theCharge;}

  bool hasError() const;

  bool operator ==(LinearizedTrackState<5> & other)const;

  bool operator ==(ReferenceCountingPointer<LinearizedTrackState<5> >& other)const;

  /** Creates the correct refitted state according to the results of the
   *  track refit.
   */
  virtual RefCountedRefittedTrackState createRefittedTrackState(
  	const GlobalPoint & vertexPosition,
	const AlgebraicVector3 & vectorParameters,
	const AlgebraicSymMatrix66 & covarianceMatrix) const;


  virtual AlgebraicVector5 refittedParamFromEquation(
	const RefCountedRefittedTrackState & theRefittedState) const;

  virtual double weightInMixture() const {return theTSOS.weight();}

  virtual void inline checkParameters(AlgebraicVector5 & parameters) const;

  virtual std::vector<ReferenceCountingPointer<LinearizedTrackState<5> > > components()
  									const;

  virtual bool isValid() const;

private:

  /** Constructor with the linearization point and the track.
   *  Private, can only be used by LinearizedTrackFactory.
   */
   PerigeeLinearizedTrackState(const GlobalPoint & linP, const reco::TransientTrack & track, 
  	const TrajectoryStateOnSurface& tsos)
     : theLinPoint(linP), theTrack(track), jacobiansAvailable(false),
       // impactPointAvailable(false), 
       theCharge(theTrack.charge()), theTSOS(tsos) {}

  /** Method calculating the track parameters and the Jacobians.
   */
  void computeJacobians() const;
  /** Method calculating the track parameters and the Jacobians for charged particles.
   */
  void computeChargedJacobians() const;
  /** Method calculating the track parameters and the Jacobians for neutral particles.
   */
  void computeNeutralJacobians() const;
  /** Method calculating the 3D impact point measurement
   */
  void compute3DImpactPoint() const;

  GlobalPoint theLinPoint;
  reco::TransientTrack theTrack;

  mutable bool jacobiansAvailable;
  mutable AlgebraicMatrix53 thePositionJacobian, theMomentumJacobian;
  mutable TrajectoryStateClosestToPoint thePredState;
  mutable AlgebraicVector5 theConstantTerm;
  mutable AlgebraicVector5 theExpandedParams;

//   ImpactPointMeasurementExtractor theIPMExtractor;
  TSCPBuilderNoMaterial builder;
//   mutable bool impactPointAvailable;
//   mutable ImpactPointMeasurement the3DImpactPoint;
  TrackCharge theCharge;
  const TrajectoryStateOnSurface theTSOS;
};

#endif
