dvmnorm <- function (x, mean = rep(0, p), sigma = diag(p), log = FALSE)
{
    if (is.vector(x))
        x <- matrix(x, ncol = length(x))
    p <- ncol(x)
    if (!missing(mean)) {
        if (!is.null(dim(mean)))
            dim(mean) <- NULL
        if (length(mean) != p)
            stop("mean and sigma have non-conforming size")
    }
    if (!missing(sigma)) {
        if (p != ncol(sigma))
            stop("x and sigma have non-conforming size")
        if (!isSymmetric(sigma, tol = sqrt(.Machine$double.eps),
            check.attributes = FALSE))
            stop("sigma must be a symmetric matrix")
    }
    dec <- tryCatch(chol(sigma), error = function(e) e)
    if (inherits(dec, "error")) {
        x.is.mu <- colSums(t(x) != mean) == 0
        logretval <- rep.int(-Inf, nrow(x))
        logretval[x.is.mu] <- Inf
    }
    else {
        tmp <- backsolve(dec, t(x) - mean, transpose = TRUE)
        rss <- colSums(tmp^2)
        logretval <- -sum(log(diag(dec))) - 0.5 * p * log(2 *
            pi) - 0.5 * rss
    }
    names(logretval) <- rownames(x)
    if (log)
        logretval
    else exp(logretval)
}