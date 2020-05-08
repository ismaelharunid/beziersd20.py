from helpers import trange

class SampleMixin(object):
  
  _sample_threshold = 1.0
  
  @property
  def sample_threshold(self): return self._sample_threshold
  
  @sample_threshold.setter
  def sample_threshold(self, threshold):
    self._sample_threshold = float(threshold)
  
  def sample(self,samples,start=0.0,stop=1.0):
    """Samples a segment or path a given number of times, returning a list of Point objects.
    Remember that for a Bezier path, the points are not guaranteed to be distributed
    at regular intervals along the path. If you want to space your points regularly,
    use the `regularSample` method instead.

.. figure:: sampling.png
   :scale: 50 %
   :alt: sample versus regularSample

   In the figure, the green ticks are generated by `sample`. These are evenly
   distributed by curve time, but because of the curvature of the curve, there
   are concentrations of samples around the tighter parts of the curve.

   The red ticks are generated by `regularSample`, which evenly spaces the
   samples along the length of the curve.

    """
    return [ self.pointAtTime(t) for t in trange(samples, start, stop) ]

  def regularSample(self,samples,start=0.0,stop=1.0):
    """Samples a segment or path a given number of times, returning a list of Point objects,
    but ensuring that the points are regularly distributed along the length
    of the curve. This is an expensive operation because I am a lazy programmer."""

    return [ self.pointAtTime(t) for t in self.regularSampleTValue(samples, start, stop) ]

  def regularSampleTValue(self,samples,start=0.0,stop=1.0):
    """Sometimes you don't want the points, you just want a set of time values (t) which
    represent regular spaced samples along the curve. Use this method to get a list of time
    values instead of Point objects."""
    # Build LUT; could cache it *if* we knew when to invalidate
    #TODO:
    # * adjust each time if outside resonable error.  I think the error threshold should 
    #   be stored in the base calss it it isn't already.
    length = self.length
    if length == 0: return []
    lut = [ self.self.lengthAtTime(t) for t in trange(samples, start, stop) ]
    desiredLength = 0.0
    rSamples = []
    while desiredLength < length:
      while len(lut) > 0 and lut[0][1] < desiredLength:
        lut.pop(0)
      if len(lut) == 0:
        break
      #BAD: lut[0][0] may not be very accurate sometimes, and only slightly accurate often
      rSamples.append(lut[0][0])
      desiredLength += length / samples
    if rSamples[-1] != 1.0:
      rSamples.append(1.0)
    return rSamples
