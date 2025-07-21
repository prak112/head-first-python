def normalize(v, smin, smax, tmin, tmax):
  """Returns a normalized and transformed value, t_v, within the provided range of tmin-tmax, for a given value of 'v' within the range of smin-smax.

  tmin, tmax - Target value range
  smin, smax - Source value range
  
  Based on the technique described here:
  http://james-ramsden.com/map-a-value-from-one-number-scale-to-another-formula-and-c-code/
  """

  # transformation range within 0-1
  if tmin == 0 and tmax == 1: 
    return (round((v - smin) / (smax - smin)), 2)
  else:
    t_v = (tmin) + ((tmax - tmin) * ((v - smin) / (smax - smin)))
    return (round(t_v, 2))
  