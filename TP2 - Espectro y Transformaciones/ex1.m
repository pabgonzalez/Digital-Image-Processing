clear all;
close all;
% h=[0 1/6 0 ; 1/6 1/3 1/6 ; 0 1/6 0 ];
%  h = fspecial('disk');                %% LOW pass 
 h = fspecial('unsharp');              %% Hi pass

freqz2(h);

% construyo una imagen (que es una delta en 0)
% suficientemente grande para poder bien el espectro

N=256;
big=zeros(N);       %make a big image
big(N/2,N/2)=1;     %unit impulse

h1=conv2(big,h);    %make conv with the filter ==> 

figure
%freqz2(h1);        %takes long time

S = fft2(h1);       %Spectrum
SM=abs(S);          %Modulo

imshow(fftshift(SM/max(max(SM)))); % show spect


figure

IMd = log(1+abs(SM));
imshow(fftshift(IMd/max(max(IMd)))); % show spect log scale
