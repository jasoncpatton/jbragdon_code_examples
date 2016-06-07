library(fda)
library(plyr)

# load data
load('taudata.Rdata')

# taudata is a DataFrame with columns:
# county year day hour tau tau_dqx

# loop over unique counties
for(thiscounty in unique(taudata$county)) {

  # loop over unique years
  for(thisyear in unique(taudata$year)) {

    # subset taudata for this county and this year
    tausubset <- subset(taudata, county==thiscounty & year==thisyear)

    # combine day and hour into single variable (x = day + hour/24)
    tausubset$x <- tausubset$day + tausubset$hour/24

    # create range from first to last day
    dayrange <- c(min(tausubset$x), max(tausubset$x))

    # set number of basis vectors (like number of waves in a Fourier series) (**arbitrary**)
    nbasis <- 301

    # create basis
    basisobj <- create.fourier.basis(dayrange, nbasis)

    # set roughness penalty (larger = smoother) (**arbitrary**)
    lambda <- 10^4
    fdParobj <- fdPar(basisobj, Lfdobj=int2Lfd(2), lambda)

    # fit data
    thisfit <- smooth.basis(tausubset$x, tausubset$tau, fdParobj)

    # get fit values for every 12 hours (every 0.5 day)
    dayvec <- seq(min(dayrange), max(dayrange), 0.5)
    taufit <- eval.fd(dayvec, thisfit$fd)
    fitdf <- data.frame(day=dayvec, tau=taufit)

    # write to file under fit_tau_data directory
    filename = paste('fit_tau_data/', thiscounty, '_', thisyear, '_.csv', sep='')
    write.table(fitdf, file=filename, sep=',', row.names=FALSE)

  }
}
