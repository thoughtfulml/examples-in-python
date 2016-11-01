#load library for multivariate normal
library(mvtnorm)
#load Old Faithful data frame
data(faithful)

#setup grid for plotting
xpts <- seq(from=1,to=6,length.out=100)
ypts <- seq(from=40,to=100,length.out=100)

#initial parameter estimates (chosen to be deliberately bad)
theta <- list(
             tau=c(0.5,0.5),
             mu1=c(2.8,75),
             mu2=c(3.6,58),
             sigma1=matrix(c(0.8,7,7,70),ncol=2),
             sigma2=matrix(c(0.8,7,7,70),ncol=2)
             )

#E step: calculates conditional probabilities for latent variables
E.step <- function(theta)
 t(apply(cbind(
     theta$tau[1] * dmvnorm(faithful,mean=theta$mu1,sigma=theta$sigma1),
     theta$tau[2] * dmvnorm(faithful,mean=theta$mu2,sigma=theta$sigma2)
     ),1,function(x) x/sum(x)))
#M step: calculates the parameter estimates which maximise Q
M.step <- function(T) list(
 tau= apply(T,2,mean),
 mu1= apply(faithful,2,weighted.mean,T[,1]),
 mu2= apply(faithful,2,weighted.mean,T[,2]),
 sigma1= cov.wt(faithful,T[,1])$cov,
 sigma2= cov.wt(faithful,T[,2])$cov)

#function to plot current data
plot.em <- function(theta){
 mixture.contour <- outer(xpts,ypts,function(x,y) {
   theta$tau[1]*dmvnorm(cbind(x,y),mean=theta$mu1,sigma=theta$sigma1) + theta$tau[2]*dmvnorm(cbind(x,y),mean=theta$mu2,sigma=theta$sigma2)
   })
 contour(xpts,ypts,mixture.contour,nlevels=5,drawlabel=FALSE,col="red",xlab="Eruption time (mins)",ylab="Waiting time (mins)",main="Waiting time vs Eruption time of the Old Faithful geyser")
 points(faithful)
}

#plot initial contours
iter <- 1
png(filename=paste("em",formatC(iter,width=4,flag="0"),".png",sep=""))
plot.em(theta)
dev.off()

#run EM and plot
for (iter in 2:30){
 T <- E.step(theta)
 theta <- M.step(T)
 png(filename=paste("em",formatC(iter,width=4,flag="0"),".png",sep=""))
 plot.em(theta)
 dev.off()
}
