function Idown=downsampling(I,m,filter)
% Downsample the square image I by a factor of m
[N,M]=size(I);
% Apply ideal filter
w=1/m;
F=fftshift(fft2(I));
if strcmp(filter, 'FILTER_ON') == true
    for i=1:N
        for j=1:N
            r2=(i-round(N/2))^2+(j-round(N/2))^2;

            if (r2>round((N/2*w)^2)) F(i,j)=0; end; %ojo w=1/m
        end;
    end;

end;

Idown=real(ifft2(fftshift(F)));
% Now downsample
Idown=imresize(Idown,[N/m,N/m],'nearest');
