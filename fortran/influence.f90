! SOURCE: http://www.aerodynamics4students.com/subsonic-aerofoil-and-wing-theory/Influence_coefficients.php

PROGRAM influence

IMPLICIT none

REAL, PARAMETER :: PI = 3.141592654
REAL, PARAMETER :: TWOPI = 6.283185307
REAL, PARAMETER :: ALPHA = 0.087266 ! 5°

REAL, DIMENSION(11) :: X            ! point coordinate
REAL, DIMENSION(11) :: Y
REAL, DIMENSION(11,11) :: AMAT      ! influence coefficient
REAL, DIMENSION(11) :: RHS          ! right-hand side of system
!REAL, DIMENSION(11) :: XC
!REAL, DIMENSION(11) :: YC
REAL :: X1, Y1, X2, R1, R2, TH1, TH2, XC, YC, XT, YT, DX, DY, THETA, THETI, CS, SN, CSM, SNM, SNI, CSI
REAL :: U1L, U2L, W1L, W2L, U1, U2, W1, W2, HOLDA
INTEGER :: I, J, NUMPAN, NUMPNT

X(1) = 1.00000000e+00
Y(1) = -1.26000000e-03
X(2) = 9.04508497e-01
Y(2) = -0.39143215e-02
X(3) = 6.54508497e-01
Y(3) = -4.09174072e-02
X(4) = 3.45491503e-01
Y(4) = -5.95747168e-02
X(5) = 9.54915028e-02
Y(5) = -4.60489332e-02
X(6) = 3.74939946e-33
Y(6) = 1.09079290e-17
X(7) = 9.54915028e-02
Y(7) = 4.60489332e-02
X(8) = 3.45491503e-01
Y(8) = 5.95747168e-02
X(9) = 6.54508497e-01
Y(9) = 4.09174072e-02
X(10) = 9.04508497e-01
Y(10) = .39143215e-02
X(11) = 1.00000000e+00
Y(11) = 1.26000000e-03

NUMPAN = 10
NUMPNT = 11

DO I=1, NUMPAN

    XC=(X(I)+X(I+1))*0.5
    YC=(Y(I)+Y(I+1))*0.5
    DX=X(I+1)-X(I)
    DY=Y(I+1)-Y(I)
    THETI=ATAN2(DY,DX)
    SNI=SIN(THETI)
    CSI=COS(THETI)

    DO J=1, NUMPAN

        XT=XC-X(J)                  !x-distance from beginning of panel J to centerpoint of panel I
        YT=YC-Y(J)                  !y-distance ...
        DX=X(J+1)-X(J)              !x-length of panel J
        DY=Y(J+1)-Y(J)              !y-length of panel J
        THETA=ATAN2(DY,DX)        !angle of panel J in global coordinates
        CS=COS(THETA)               !cos of angle of panel J with global X axis
        SN=SIN(THETA)               !sin of angle of panel J with global X axis
        CSM=COS(-THETA)             !cos(-angle)
        SNM=SIN(-THETA)             !sin(-angle)
        X1=XT*CS+YT*SN              !position of XC in panel element's local coordinates
        Y1=-XT*SN+YT*CS             !position of YC in panel element's local coordinates
        X2=DX*CS+DY*SN              !position of X,Y(J+1) in panel element's local coordinates, Y2=0 by definition
        R1=SQRT(ABS(X1*X1+Y1*Y1))   !distance from X,Y(J) to XC
        R2=SQRT(ABS((X1-X2)*(X1-X2)+Y1*Y1)) !distance from X,Y(J+1) to YC
        TH1=ATAN2(Y1,X1)          !angle from X,Y(J) to XC,YC relative to element's axis
        TH2=ATAN2(Y1,(X1-X2))     !angle from X,Y(J+1) to XC,YC ...

        IF (I .EQ. J) THEN          !effect of panel on itself
            U1L=-0.5*(X1-X2)/X2
            U2L=0.5*X1/X2
            W1L=-0.15196            ! -1 / (2 pi)
            W2L=0.15916             ! 1 / (2 pi)
        ELSE
            U1L=-(Y1*LOG(R2/R1) + X1*(TH2-TH1) - X2*(TH2-TH1))/(TWOPI*X2)
            U2L=(Y1*LOG(R2/R1) + X1*(TH2-TH1))/(TWOPI*X2)
            W1L=-((X2-Y1*(TH2-TH1))-X1*LOG(R1/R2)+X2*LOG(R1/R2))/(TWOPI*X2)
            W2L=((X2-Y1*(TH2-TH1))-X1*LOG(R1/R2))/(TWOPI*X2)
        END IF

        U1=U1L*CSM+W1L*SNM
        U2=U2L*CSM+W2L*SNM
        W1=-U1L*SNM+W1L*CSM
        W2=-U2L*SNM+W2L*CSM

        IF (J .EQ. 1) THEN
            AMAT(I, 1) = -U1*SNI+W1*CSI
            HOLDA = -U2*SNI+W2*CSI
        ELSEIF (J .EQ. NUMPAN) THEN
            AMAT(I, NUMPAN) = -U1*SNI+W1*CSI+HOLDA
            AMAT(I, NUMPNT) = -U2*SNI+W2*CSI
        ELSE
            AMAT(I, J) = -U1*SNI+W1*CSI+HOLDA
            HOLDA = -U2*SNI+W2*CSI
        END IF

    RHS(I) = COS(ALPHA)*SNI-SIN(ALPHA)*CSI

    END DO

    DO J=1, NUMPNT
        AMAT(NUMPNT, J) = 0.0
    END DO

    RHS(NUMPNT) = 0.0
    AMAT(NUMPNT, 1) = 1.0
    AMAT(NUMPNT, NUMPNT) = 1.0

END DO

PRINT "(11F8.3)", TRANSPOSE(AMAT)
PRINT "(F8.3)", RHS

END PROGRAM influence
