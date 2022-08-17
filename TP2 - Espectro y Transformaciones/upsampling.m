function Iup=upsampling(I,m)
% Upsample the square image I by a factor of m
[N,M]=size(I);
Iup=zeros(m*N,m*N);
% Expand input image
for i=1:N
    for j=1:N
        Iup(m*(i-1)+1,m*(j-1)+1)=I(i,j);
    end;
end;
% Ideal filter
[N,M]=size(Iup);
w=1/m;
F=fftshift(fft2(Iup));
for i=1:N
    for j=1:N
        r2=(i-round(N/2))^2+(j-round(N/2))^2;
        if (r2>round((N/2*w)^2)) F(i,j)=0; end;
    end;
end;
Iup=(m*m)*abs(ifft2(fftshift(F)));